"""Regression tests for cross-run, destination-scoped delivery deduplication."""

import copy
import threading
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock

import pytest

from scripts._delivery import Outcome, article_key, deliver_articles
from scripts._delivery_state import Snapshot, StateConflict, StateError

ARTICLE = {"url": "https://example.com/testing", "title": "Testing"}


class MemoryCAS:
    """Atomic fake; the production coordinator must use durable GitHub state."""

    def __init__(self):
        self.state = {"schema_version": 1, "destinations": {}}
        self.version = 0
        self.lock = threading.Lock()
        self.fail_write = None

    def read(self):
        with self.lock:
            return Snapshot(str(self.version), copy.deepcopy(self.state))

    def compare_and_swap(self, snapshot, state):
        with self.lock:
            if self.fail_write:
                raise self.fail_write
            if snapshot.version != str(self.version):
                raise StateConflict("Concurrent update")
            self.state = copy.deepcopy(state)
            self.version += 1


def record(store, destination="discord:qa-rss", article=ARTICLE):
    return store.state["destinations"][destination][article_key(article)]


def test_next_run_does_not_resend_delivered_articles():
    store, sender = MemoryCAS(), Mock(return_value=Outcome.CONFIRMED)
    first = deliver_articles(store, "discord:qa-rss", [ARTICLE], sender)
    second = deliver_articles(store, "discord:qa-rss", [ARTICLE], sender)
    assert first.delivered == 1
    assert second.already_delivered == 1
    assert first.complete and second.complete
    assert sender.call_count == 1
    assert record(store)["status"] == "delivered"


def test_destinations_and_normalized_urls_are_independent():
    store, sender = MemoryCAS(), Mock(return_value=Outcome.CONFIRMED)
    duplicate = {**ARTICLE, "url": ARTICLE["url"] + "?utm_source=rss"}
    articles = [ARTICLE, duplicate]
    original = copy.deepcopy(articles)
    deliver_articles(store, "discord:qa-rss", articles, sender)
    deliver_articles(store, "github:qa-rss-issues", articles, sender)
    assert sender.call_count == 2
    assert all(len(call.args[0]) == 1 for call in sender.call_args_list)
    assert articles == original
    assert len(store.state["destinations"]) == 2


def test_delivered_is_written_only_after_confirmed_send():
    store = MemoryCAS()

    def send(articles):
        assert record(store)["status"] == "pending"
        return Outcome.CONFIRMED

    deliver_articles(store, "discord:qa-rss", [ARTICLE], send)
    assert record(store)["status"] == "delivered"


@pytest.mark.parametrize("result", [Outcome.UNCERTAIN, True, False, None])
def test_uncertain_or_legacy_boolean_results_are_not_retried(result):
    store, sender = MemoryCAS(), Mock(return_value=result)
    first = deliver_articles(store, "discord:qa-rss", [ARTICLE], sender)
    second = deliver_articles(store, "discord:qa-rss", [ARTICLE], sender)
    assert first.pending == second.pending == 1
    assert not first.complete and not second.complete
    assert record(store)["status"] == "pending"
    assert sender.call_count == 1


def test_exception_after_possible_delivery_keeps_pending_without_error_text():
    store, sender = MemoryCAS(), Mock(side_effect=RuntimeError("sensitive-webhook-value"))
    report = deliver_articles(store, "discord:qa-rss", [ARTICLE], sender)
    assert report.pending == 1
    assert "sensitive" not in str(store.state)
    deliver_articles(store, "discord:qa-rss", [ARTICLE], sender)
    assert sender.call_count == 1


def test_definitive_rejection_is_retryable_next_run():
    store, sender = MemoryCAS(), Mock(side_effect=[Outcome.REJECTED, Outcome.CONFIRMED])
    first = deliver_articles(store, "discord:qa-rss", [ARTICLE], sender)
    assert first.rejected == 1
    assert record(store)["status"] == "retryable"
    second = deliver_articles(store, "discord:qa-rss", [ARTICLE], sender)
    assert second.delivered == 1
    assert record(store)["status"] == "delivered"


def test_partial_batch_failure_preserves_earlier_receipts_and_stops():
    store, sender = MemoryCAS(), Mock(side_effect=[Outcome.CONFIRMED, Outcome.REJECTED])
    articles = [{"url": f"https://example.com/{i}"} for i in range(21)]
    first = deliver_articles(store, "discord:qa-rss", articles, sender)
    assert (first.delivered, first.rejected, first.not_attempted) == (10, 10, 1)
    retry = Mock(return_value=Outcome.CONFIRMED)
    second = deliver_articles(store, "discord:qa-rss", articles, retry)
    assert (second.delivered, second.already_delivered) == (11, 10)
    assert [len(call.args[0]) for call in retry.call_args_list] == [10, 1]


def test_reservation_write_failure_prevents_send():
    store, sender = MemoryCAS(), Mock()
    store.fail_write = StateError("Storage unavailable")
    with pytest.raises(StateError):
        deliver_articles(store, "discord:qa-rss", [ARTICLE], sender)
    sender.assert_not_called()


def test_receipt_write_failure_never_resends_unconfirmed_delivery():
    store = MemoryCAS()

    def send(articles):
        store.fail_write = StateError("Response lost during state update")
        return Outcome.CONFIRMED

    with pytest.raises(StateError):
        deliver_articles(store, "discord:qa-rss", [ARTICLE], send)
    assert record(store)["status"] == "pending"
    store.fail_write = None
    retry = Mock()
    report = deliver_articles(store, "discord:qa-rss", [ARTICLE], retry)
    assert report.pending == 1
    retry.assert_not_called()


def test_missing_state_blocks_even_an_empty_run():
    store = Mock()
    store.read.side_effect = StateError("Missing state")
    with pytest.raises(StateError):
        deliver_articles(store, "discord:qa-rss", [], Mock())


def test_concurrent_runs_cannot_claim_the_same_article():
    store = MemoryCAS()
    sending, release = threading.Event(), threading.Event()

    def first_send(articles):
        sending.set()
        assert release.wait(3)
        return Outcome.CONFIRMED

    with ThreadPoolExecutor(max_workers=2) as workers:
        first = workers.submit(deliver_articles, store, "discord:qa-rss", [ARTICLE], first_send)
        assert sending.wait(3)
        second_sender = Mock()
        second = deliver_articles(store, "discord:qa-rss", [ARTICLE], second_sender)
        release.set()
        assert first.result().delivered == 1
    assert second.pending == 1
    second_sender.assert_not_called()


def test_conflict_reloads_and_merges_unrelated_destination_receipt():
    store = MemoryCAS()
    original = store.compare_and_swap
    conflicted = False

    def cas(snapshot, state):
        nonlocal conflicted
        if not conflicted:
            conflicted = True
            deliver_articles(store, "github:qa-rss", [ARTICLE], lambda batch: Outcome.CONFIRMED)
        original(snapshot, state)

    store.compare_and_swap = cas
    report = deliver_articles(store, "discord:qa-rss", [ARTICLE], lambda batch: Outcome.CONFIRMED)
    assert report.delivered == 1
    assert set(store.state["destinations"]) == {"discord:qa-rss", "github:qa-rss"}


def test_persistent_conflict_exhaustion_does_not_send():
    store, sender = MemoryCAS(), Mock()
    store.compare_and_swap = Mock(side_effect=StateConflict("Conflict"))
    with pytest.raises(StateConflict):
        deliver_articles(store, "discord:qa-rss", [ARTICLE], sender, conflict_retries=2)
    assert store.compare_and_swap.call_count == 2
    sender.assert_not_called()


def test_sender_cannot_mutate_original_articles():
    store = MemoryCAS()
    articles = [copy.deepcopy(ARTICLE)]

    def sender(batch):
        batch[0]["title"] = "changed"
        return Outcome.CONFIRMED

    deliver_articles(store, "discord:qa-rss", articles, sender)
    assert articles == [ARTICLE]


def test_simultaneous_claim_conflict_still_sends_only_once():
    store = MemoryCAS()
    barrier = threading.Barrier(2)
    original = store.compare_and_swap

    def cas(snapshot, state):
        if snapshot.version == "0":
            barrier.wait(timeout=3)
        original(snapshot, state)

    store.compare_and_swap = cas
    sender = Mock(return_value=Outcome.CONFIRMED)
    with ThreadPoolExecutor(max_workers=2) as workers:
        futures = [workers.submit(deliver_articles, store, "discord:qa-rss", [ARTICLE], sender) for _ in range(2)]
        reports = [future.result() for future in futures]
    assert sum(result.delivered for result in reports) == 1
    assert sender.call_count == 1
    assert record(store)["status"] == "delivered"


def test_finalization_conflict_preserves_both_confirmed_destinations():
    store = MemoryCAS()
    original = store.compare_and_swap
    conflicted = False

    def cas(snapshot, state):
        nonlocal conflicted
        records = state["destinations"].get("discord:qa-rss", {})
        if not conflicted and any(item["status"] == "delivered" for item in records.values()):
            conflicted = True
            deliver_articles(store, "github:qa-rss", [ARTICLE], lambda batch: Outcome.CONFIRMED)
        original(snapshot, state)

    store.compare_and_swap = cas
    deliver_articles(store, "discord:qa-rss", [ARTICLE], lambda batch: Outcome.CONFIRMED)
    assert record(store)["status"] == "delivered"
    assert record(store, "github:qa-rss")["status"] == "delivered"
