from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Event:
    """Base class for all lambda function events."""

    raw_event: dict

    @classmethod
    def from_lambda_event(cls, event: dict) -> Event:
        return cls(
            raw_event=event,
        )
