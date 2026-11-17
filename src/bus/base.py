from abc import ABC, abstractmethod


class EventPublisher(ABC):
    @abstractmethod
    def publish(
        self, kind: str, payload: dict, event_id: str | None = None
    ) -> dict: ...
