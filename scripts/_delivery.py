"""Per-destination URL dedupe with durable reservations and delivery receipts.

This is an opt-in coordinator, not an enabled notification workflow. The caller
provides a durable CAS store and a sender that truthfully classifies outcomes.
"""

import copy
import hashlib
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum

from scripts._delivery_state import StateConflict, StateError, StateStore, validate_destination, validate_state
from scripts._url import normalize_url


class Outcome(Enum):
    CONFIRMED = "confirmed"  # Destination accepted the entire batch.
    REJECTED = "rejected"  # Definitive rejection; no item in the batch was sent.
    UNCERTAIN = "uncertain"  # Timeout/ambiguous result: do not automatically retry.


@dataclass
class DeliveryReport:
    delivered: int = 0
    already_delivered: int = 0
    pending: int = 0
    rejected: int = 0
    not_attempted: int = 0

    @property
    def complete(self) -> bool:
        return self.pending == 0 and self.rejected == 0 and self.not_attempted == 0


def article_key(article: dict) -> str:
    """Only canonical URL hashes, never article text or webhook credentials, persist."""
    url = article.get("url")
    if not isinstance(url, str) or not url.startswith(("https://", "http://")):
        raise StateError("Article requires an HTTP URL")
    return hashlib.sha256(normalize_url(url).encode()).hexdigest()


def _record(status: str, attempt_id: str) -> dict:
    return {"status": status, "attempt_id": attempt_id, "updated_at": datetime.now(UTC).isoformat()}


def _reserve(store, destination, batch, attempt_id, retries):
    for _ in range(retries):
        snapshot = store.read()
        validate_state(snapshot.state)
        state = copy.deepcopy(snapshot.state)
        records = state["destinations"].setdefault(destination, {})
        selected, already, pending = [], 0, 0
        for key, article in batch:
            current = records.get(key, {}).get("status")
            if current == "delivered":
                already += 1
            elif current == "pending":
                pending += 1
            else:
                selected.append((key, article))
                records[key] = _record("pending", attempt_id)
        if not selected:
            return selected, already, pending
        try:
            store.compare_and_swap(snapshot, state)
            return selected, already, pending
        except StateConflict:
            continue
    raise StateConflict("Could not reserve delivery after concurrent state changes")


def _finish(store, destination, selected, attempt_id, status, retries):
    for _ in range(retries):
        snapshot = store.read()
        validate_state(snapshot.state)
        state = copy.deepcopy(snapshot.state)
        records = state["destinations"].get(destination, {})
        for key, _article in selected:
            current = records.get(key, {})
            if current.get("status") != "pending" or current.get("attempt_id") != attempt_id:
                raise StateError("Delivery reservation changed; reconcile before retrying")
            records[key] = _record(status, attempt_id)
        try:
            store.compare_and_swap(snapshot, state)
            return
        except StateConflict:
            continue
    raise StateConflict("Could not persist delivery result; do not resend automatically")


def deliver_articles(
    store: StateStore,
    destination: str,
    articles: list[dict],
    send: Callable[[list[dict]], Outcome],
    *,
    batch_size: int = 10,
    conflict_retries: int = 3,
) -> DeliveryReport:
    """Deliver only unconfirmed URLs without modifying the collected articles.

    Pending reservations deliberately have no expiry. An interrupted/ambiguous
    attempt needs manual reconciliation; silently expiring it could duplicate a
    successfully delivered notification. State failure raises before a new send
    or leaves the completed send pending, never falsely marking it delivered.
    """
    validate_destination(destination)
    if not 1 <= batch_size <= 500 or conflict_retries < 1:
        raise ValueError("Invalid batch size or conflict retry count")
    unique = {}
    for article in articles:
        unique.setdefault(article_key(article), article)
    items = list(unique.items())
    report = DeliveryReport()
    # Even an empty result must not turn missing/corrupt state into success.
    validate_state(store.read().state)
    for offset in range(0, len(items), batch_size):
        attempt_id = uuid.uuid4().hex
        selected, already, pending = _reserve(
            store, destination, items[offset:offset + batch_size], attempt_id, conflict_retries,
        )
        report.already_delivered += already
        report.pending += pending
        if not selected:
            continue
        try:
            outcome = send([copy.deepcopy(article) for _key, article in selected])
        except Exception:
            # No exception body is safe to persist or log: it may contain secrets.
            outcome = Outcome.UNCERTAIN
        if outcome is Outcome.CONFIRMED:
            _finish(store, destination, selected, attempt_id, "delivered", conflict_retries)
            report.delivered += len(selected)
        elif outcome is Outcome.REJECTED:
            _finish(store, destination, selected, attempt_id, "retryable", conflict_retries)
            report.rejected += len(selected)
        else:
            report.pending += len(selected)
        if outcome is not Outcome.CONFIRMED:
            report.not_attempted = max(0, len(items) - offset - batch_size)
            break  # Do not flood a failing destination with later batches.
    return report
