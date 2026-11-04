from ingestion.pipeline import normalize_records, write_jsonl


def test_normalize_records_uses_string_event_id():
    result = normalize_records([{"id": 7, "title": "demo"}])
    assert result == [{
        "event_id": "7",
        "source_system": "rest_api",
        "payload": {"id": 7, "title": "demo"},
    }]


def test_normalize_records_skips_missing_id():
    assert normalize_records([{"title": "invalid"}]) == []


def test_write_jsonl_creates_parent_directory(tmp_path):
    output = tmp_path / "landing" / "events.jsonl"
    count = write_jsonl([{"event_id": "1"}], str(output))
    assert count == 1
    assert '"event_id": "1"' in output.read_text(encoding="utf-8")
