from src.bus.base import EventPublisher


class NullEventPublisher(EventPublisher):
    def publish(
        self, kind: str, payload: dict, event_id: str | None = None
    ) -> dict:
        return {}
