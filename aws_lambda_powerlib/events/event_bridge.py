from __future__ import annotations

from dataclasses import dataclass

from .event import Event


@dataclass
class EventBridgeEvent(Event):
    """Event class for EventBridge events."""

    version: str
    id: str
    detail_type: str
    source: str
    account: str
    time: str
    region: str
    resources: list[str]
    detail: dict

    @classmethod
    def from_lambda_event(cls, event: dict) -> EventBridgeEvent:
        return cls(
            raw_event=event,
            version=event.get('version'),
            id=event.get('id'),
            detail_type=event.get('detail-type'),
            source=event.get('source'),
            account=event.get('account'),
            time=event.get('time'),
            region=event.get('region'),
            resources=event.get('resources'),
            detail=event.get('detail'),
        )
