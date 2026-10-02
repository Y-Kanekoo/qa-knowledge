"""Mock-only tests for the durable GitHub Contents state adapter."""

import base64
import copy
import json
from unittest.mock import Mock

import pytest
import requests

from scripts._delivery_state import GitHubContentsStateStore, Snapshot, StateConflict, StateError, validate_state

EMPTY = {"schema_version": 1, "destinations": {}}
SHA = "a" * 40


def response(status=200, state=None, sha=SHA):
    body = {"encoding": "base64", "sha": sha,
            "content": base64.b64encode(json.dumps(state if state is not None else EMPTY).encode()).decode()}
    return Mock(status_code=status, json=Mock(return_value=body))


def store(session):
    return GitHubContentsStateStore("example/repo", "rss-state", "state.json", "synthetic-token", session)


def test_read_and_write_use_versioned_durable_branch():
    session = Mock()
    session.request.side_effect = [response(), response()]
    adapter = store(session)
    snapshot = adapter.read()
    assert snapshot == Snapshot(SHA, EMPTY)
    adapter.compare_and_swap(snapshot, EMPTY)
    read, write = session.request.call_args_list
    assert read.args[0] == "GET"
    assert read.kwargs["params"] == {"ref": "rss-state"}
    assert write.args[0] == "PUT"
    assert write.kwargs["json"]["sha"] == SHA
    assert write.kwargs["json"]["branch"] == "rss-state"
    assert json.loads(base64.b64decode(write.kwargs["json"]["content"])) == EMPTY
    assert read.kwargs["allow_redirects"] is False
    assert write.kwargs["allow_redirects"] is False


@pytest.mark.parametrize("status", [301, 401, 403, 404, 429, 500])
def test_unavailable_state_never_becomes_empty_state(status):
    session = Mock()
    session.request.return_value = response(status)
    with pytest.raises(StateError, match="no empty-state fallback"):
        store(session).read()
    assert session.request.call_count == 1


@pytest.mark.parametrize("state", [[], {}, {"schema_version": 2, "destinations": {}},
                                   {"schema_version": 1, "destinations": {"bad/name": {}}}])
def test_malformed_state_fails_closed(state):
    session = Mock()
    session.request.return_value = response(state=state)
    with pytest.raises(StateError):
        store(session).read()


def test_http_error_does_not_echo_credentials_or_response():
    session = Mock()
    session.request.side_effect = requests.ConnectionError("sensitive-value-in-error")
    with pytest.raises(StateError) as error:
        store(session).read()
    assert "sensitive-value" not in str(error.value)


def test_cas_conflict_is_distinct_from_unknown_write_failure():
    session = Mock()
    session.request.side_effect = [response(409), response(500)]
    adapter = store(session)
    with pytest.raises(StateConflict):
        adapter.compare_and_swap(Snapshot(SHA, EMPTY), EMPTY)
    with pytest.raises(StateError, match="unconfirmed"):
        adapter.compare_and_swap(Snapshot(SHA, EMPTY), EMPTY)


def test_state_does_not_accept_extra_content():
    with pytest.raises(StateError):
        validate_state({**EMPTY, "webhook": "never-store-this"})


def test_new_adapter_reads_previously_persisted_state():
    # This fake represents durable GitHub bytes across independently constructed
    # clients, not a local process cache or a claim of live API verification.
    durable = {"state": copy.deepcopy(EMPTY), "version": SHA}

    def request(method, url, **kwargs):
        if method == "GET":
            return response(state=durable["state"], sha=durable["version"])
        assert kwargs["json"]["sha"] == durable["version"]
        durable["state"] = json.loads(base64.b64decode(kwargs["json"]["content"]))
        durable["version"] = "b" * 40
        return response()

    session = Mock(request=Mock(side_effect=request))
    first = store(session)
    snapshot = first.read()
    state = {"schema_version": 1, "destinations": {"discord:qa-rss": {}}}
    first.compare_and_swap(snapshot, state)
    assert store(session).read() == Snapshot("b" * 40, state)
