from event_platform.processor import process_events, validate_event


def event(**overrides):
    base = {
        "event_id": "evt-1001",
        "order_id": "ord-1001",
        "customer_id": "cust-7",
        "event_type": "ORDER_CREATED",
        "amount": "1299.5",
        "currency": "inr",
        "event_timestamp": "2026-10-10T10:30:00+00:00",
    }
    return {**base, **overrides}


def test_valid_event_is_normalised():
    result = validate_event(event())
    assert result.accepted
    assert result.record["amount"] == "1299.50"
    assert result.record["currency"] == "INR"


def test_missing_required_field_is_rejected():
    payload = event()
    payload.pop("customer_id")
    result = validate_event(payload)
    assert not result.accepted
    assert "missing_fields" in result.reason


def test_negative_amount_is_rejected():
    result = validate_event(event(amount="-1"))
    assert not result.accepted
    assert result.reason == "negative_amount"


def test_duplicate_event_id_is_dead_lettered():
    accepted, rejected = process_events([event(), event(order_id="ord-duplicate")])
    assert len(accepted) == 1
    assert len(rejected) == 1
    assert rejected[0]["reason"] == "duplicate_event_id"


def test_invalid_event_type_is_rejected():
    result = validate_event(event(event_type="UNKNOWN"))
    assert not result.accepted
    assert result.reason == "invalid_event_type"

def test_timestamp_without_timezone_is_rejected():
    result = validate_event(event(event_timestamp="2026-10-10T10:30:00"))
    assert not result.accepted
    assert result.reason == "timestamp_timezone_required"


def test_invalid_amount_is_rejected():
    result = validate_event(event(amount="not-a-number"))
    assert not result.accepted
    assert result.reason == "invalid_amount"


def test_empty_required_string_is_rejected():
    result = validate_event(event(order_id="  "))
    assert not result.accepted
    assert result.reason == "invalid_order_id"
