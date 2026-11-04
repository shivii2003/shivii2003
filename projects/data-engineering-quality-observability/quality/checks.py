from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


REQUIRED_FIELDS = ("event_id", "event_type", "event_timestamp")


def validate_event(event: dict[str, Any]) -> list[str]:
    """Return validation errors for one event; an empty list means valid."""
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        value = event.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(f"missing_required_field:{field}")

    event_id = event.get("event_id")
    if event_id is not None and not isinstance(event_id, (str, int)):
        errors.append("invalid_event_id_type")

    timestamp = event.get("event_timestamp")
    if timestamp:
        try:
            parsed = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                errors.append("timestamp_missing_timezone")
        except ValueError:
            errors.append("invalid_event_timestamp")

    return errors


def check_duplicate_ids(events: list[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()

    for event in events:
        value = event.get("event_id")
        if value is None:
            continue
        key = str(value)
        if key in seen:
            duplicates.add(key)
        seen.add(key)

    return sorted(duplicates)


def freshness_minutes(latest_timestamp: str, now: datetime | None = None) -> float:
    latest = datetime.fromisoformat(latest_timestamp.replace("Z", "+00:00"))
    if latest.tzinfo is None:
        raise ValueError("latest_timestamp must include a timezone")
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        raise ValueError("now must include a timezone")
    return (current - latest).total_seconds() / 60
