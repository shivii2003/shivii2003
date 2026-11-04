"""Validation and idempotent processing for order events."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any


@dataclass(frozen=True)
class ProcessResult:
    accepted: bool
    record: dict[str, Any] | None = None
    reason: str | None = None


REQUIRED_FIELDS = {"event_id", "order_id", "customer_id", "event_type", "amount", "currency", "event_timestamp"}
ALLOWED_EVENT_TYPES = {"ORDER_CREATED", "ORDER_UPDATED", "ORDER_CANCELLED"}


def validate_event(payload: dict[str, Any]) -> ProcessResult:
    missing = sorted(REQUIRED_FIELDS - payload.keys())
    if missing:
        return ProcessResult(False, reason=f"missing_fields:{','.join(missing)}")

    for key in ("event_id", "order_id", "customer_id", "currency"):
        if not isinstance(payload[key], str) or not payload[key].strip():
            return ProcessResult(False, reason=f"invalid_{key}")

    if payload["event_type"] not in ALLOWED_EVENT_TYPES:
        return ProcessResult(False, reason="invalid_event_type")

    try:
        amount = Decimal(str(payload["amount"]))
    except (InvalidOperation, ValueError):
        return ProcessResult(False, reason="invalid_amount")
    if amount < 0:
        return ProcessResult(False, reason="negative_amount")

    try:
        timestamp = datetime.fromisoformat(str(payload["event_timestamp"]).replace("Z", "+00:00"))
    except ValueError:
        return ProcessResult(False, reason="invalid_event_timestamp")
    if timestamp.tzinfo is None:
        return ProcessResult(False, reason="timestamp_timezone_required")

    clean = dict(payload)
    clean["amount"] = str(amount.quantize(Decimal("0.01")))
    clean["currency"] = payload["currency"].upper()
    clean["event_timestamp"] = timestamp.isoformat()
    return ProcessResult(True, record=clean)


def process_events(events: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return accepted and dead-letter events; first valid event_id wins."""
    seen: set[str] = set()
    accepted: list[dict[str, Any]] = []
    dead_letters: list[dict[str, Any]] = []

    for payload in events:
        result = validate_event(payload)
        if not result.accepted:
            dead_letters.append({"payload": payload, "reason": result.reason})
            continue

        assert result.record is not None
        event_id = result.record["event_id"]
        if event_id in seen:
            dead_letters.append({"payload": payload, "reason": "duplicate_event_id"})
            continue

        seen.add(event_id)
        accepted.append(result.record)

    return accepted, dead_letters
