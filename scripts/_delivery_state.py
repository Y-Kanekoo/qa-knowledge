"""Opt-in durable notification state. No state is initialized or sent implicitly.

This adapter uses an existing file on a dedicated GitHub branch. Missing or
invalid state fails closed; callers must not replace it with an empty ledger.
"""

import base64
import binascii
import copy
import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from urllib.parse import quote

import requests


class StateError(RuntimeError):
    """State could not be safely read or persisted. Never includes HTTP bodies."""


class StateConflict(StateError):
    """The read version was superseded by another writer."""


@dataclass(frozen=True)
class Snapshot:
    version: str
    state: dict


class StateStore(Protocol):
    def read(self) -> Snapshot: ...

    def compare_and_swap(self, snapshot: Snapshot, state: dict) -> None: ...


def validate_destination(destination: str) -> None:
    """Use stable logical names, never webhook URLs or tokens, as destinations."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,99}", destination):
        raise StateError("Invalid logical destination name")


def validate_state(state: dict) -> None:
    """Reject unknown versions, malformed state, and arbitrary stored content."""
    try:
        if set(state) != {"schema_version", "destinations"} or state["schema_version"] != 1:
            raise ValueError
        if not isinstance(state["destinations"], dict):
            raise ValueError
        for destination, deliveries in state["destinations"].items():
            validate_destination(destination)
            if not isinstance(deliveries, dict):
                raise ValueError
            for key, record in deliveries.items():
                if not re.fullmatch(r"[a-f0-9]{64}", key):
                    raise ValueError
                if set(record) != {"status", "attempt_id", "updated_at"}:
                    raise ValueError
                if record["status"] not in {"pending", "delivered", "retryable"}:
                    raise ValueError
                if not re.fullmatch(r"[a-f0-9]{32}", record["attempt_id"]):
                    raise ValueError
                stamp = datetime.fromisoformat(record["updated_at"])
                if stamp.tzinfo is None:
                    raise ValueError
    except (TypeError, ValueError, KeyError, AttributeError):
        raise StateError("Invalid delivery state; restore or reconcile it before sending") from None


class GitHubContentsStateStore:
    """Compare-and-swap a pre-created JSON ledger with GitHub's blob SHA.

    An existing GITHUB_TOKEN with contents:write is required by the eventual
    caller. This module never reads credentials from disk or initializes state.
    """

    def __init__(self, repository: str, branch: str, path: str, token: str, session=None) -> None:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise StateError("Invalid repository name")
        if not token or not branch or not path or any(part in {"", ".", ".."} for part in path.split("/")):
            raise StateError("Repository state configuration is incomplete")
        self.url = f"https://api.github.com/repos/{repository}/contents/{quote(path, safe='/')}"
        self.branch = branch
        self.session = session or requests.Session()
        self.headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

    def _request(self, method: str, **kwargs):
        try:
            return self.session.request(
                method, self.url, headers=self.headers, timeout=30, allow_redirects=False, **kwargs,
            )
        except requests.RequestException:
            raise StateError("State request failed; delivery remains unconfirmed") from None

    def read(self) -> Snapshot:
        response = self._request("GET", params={"ref": self.branch})
        if response.status_code != 200:
            raise StateError(f"State unavailable (HTTP {response.status_code}); no empty-state fallback")
        try:
            body = response.json()
            if body.get("encoding") != "base64" or not re.fullmatch(r"[a-f0-9]{40,64}", body["sha"]):
                raise ValueError
            content = base64.b64decode("".join(body["content"].split()), validate=True)
            state = json.loads(content)
            validate_state(state)
            return Snapshot(body["sha"], state)
        except (ValueError, KeyError, TypeError, AttributeError, binascii.Error):
            raise StateError("Unreadable delivery state; no empty-state fallback") from None

    def compare_and_swap(self, snapshot: Snapshot, state: dict) -> None:
        validate_state(state)
        # Copy/serialize before transmission; callers cannot change the request
        # body while another worker is committing a different receipt.
        content = json.dumps(copy.deepcopy(state), sort_keys=True).encode()
        response = self._request("PUT", json={
            "message": "chore: update RSS delivery receipts",
            "branch": self.branch,
            "sha": snapshot.version,
            "content": base64.b64encode(content).decode(),
        })
        if response.status_code == 409:
            raise StateConflict("State changed concurrently")
        if response.status_code != 200:
            raise StateError(f"State write unconfirmed (HTTP {response.status_code})")
