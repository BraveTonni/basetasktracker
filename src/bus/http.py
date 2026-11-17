import json
import os
import urllib.error
import urllib.request

from src.bus.base import EventPublisher


class HttpEventPublisher(EventPublisher):
    def __init__(self, base_url: str, token: str, sender_id: str):
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._sender_id = sender_id

    @classmethod
    def from_env(cls) -> HttpEventPublisher:
        base_url = os.environ.get("EVENT_BUS_URL", "http://localhost:8000")
        token = os.environ.get("EVENT_BUS_TOKEN", "")
        sender_id = os.environ.get("EVENT_BUS_SENDER", "kanban")
        if not token:
            raise ValueError("EVENT_BUS_TOKEN is not set")
        return cls(base_url, token, sender_id)

    def publish(
        self, kind: str, payload: dict, event_id: str | None = None
    ) -> dict:
        body: dict = {
            "kind": kind,
            "sender_id": self._sender_id,
            "payload": payload,
        }
        if event_id is not None:
            body["event_id"] = event_id

        request = urllib.request.Request(
            f"{self._base_url}/v1/events",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8")
            raise RuntimeError(
                f"event bus rejected {kind}: {error.code} {detail}"
            ) from error
        except urllib.error.URLError as error:
            raise RuntimeError(
                f"event bus unreachable for {kind}: {error.reason}"
            ) from error
