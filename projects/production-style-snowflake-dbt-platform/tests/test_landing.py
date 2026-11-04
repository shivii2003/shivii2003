import json

from ingestion.landing import write_jsonl


def test_write_jsonl_adds_run_metadata(tmp_path):
    path, count, run_id = write_jsonl(
        [{"order_id": 10}, {"order_id": 11}],
        str(tmp_path),
        "orders",
        run_id="test-run",
    )
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    assert count == 2
    assert run_id == "test-run"
    assert rows[0]["record"]["order_id"] == 10
    assert rows[0]["_run_id"] == "test-run"
