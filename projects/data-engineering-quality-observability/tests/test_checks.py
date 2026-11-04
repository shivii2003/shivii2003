from quality.checks import check_duplicate_ids, validate_event


def test_valid_event_passes():
    event = {
        "event_id": "evt-100",
        "event_type": "order_created",
        "event_timestamp": "2026-01-01T10:00:00+00:00",
    }
    assert validate_event(event) == []


def test_missing_required_field_is_reported():
    event = {"event_id": "evt-101", "event_type": "login"}
    assert "missing_required_field:event_timestamp" in validate_event(event)


def test_duplicate_ids_are_detected():
    events = [{"event_id": "x"}, {"event_id": "y"}, {"event_id": "x"}]
    assert check_duplicate_ids(events) == ["x"]
