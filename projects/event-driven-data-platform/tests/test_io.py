import json

import pytest

from event_platform.io import read_jsonl, write_jsonl


def test_jsonl_round_trip(tmp_path):
    path = tmp_path / "nested" / "events.jsonl"
    records = [{"event_id": "evt-1", "amount": "10.00"}, {"event_id": "evt-2"}]

    write_jsonl(path, records)

    assert read_jsonl(path) == records


def test_blank_lines_are_ignored(tmp_path):
    path = tmp_path / "events.jsonl"
    path.write_text('{"event_id":"evt-1"}\n\n', encoding="utf-8")

    assert read_jsonl(path) == [{"event_id": "evt-1"}]


def test_invalid_json_reports_line_number(tmp_path):
    path = tmp_path / "events.jsonl"
    path.write_text('{"event_id":"evt-1"}\nnot-json\n', encoding="utf-8")

    with pytest.raises(ValueError, match="line 2"):
        read_jsonl(path)


def test_non_object_json_is_rejected(tmp_path):
    path = tmp_path / "events.jsonl"
    path.write_text(json.dumps(["not", "an", "object"]), encoding="utf-8")

    with pytest.raises(ValueError, match="Expected JSON object"):
        read_jsonl(path)
