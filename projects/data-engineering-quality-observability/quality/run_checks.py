from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import datetime, timezone

from quality.checks import check_duplicate_ids, validate_event


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    events = [
        json.loads(line)
        for line in Path(args.input).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    row_results = [
        {"row_number": index, "errors": validate_event(event)}
        for index, event in enumerate(events, start=1)
    ]
    duplicates = check_duplicate_ids(events)
    invalid_rows = sum(bool(row["errors"]) for row in row_results)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "records_received": len(events),
        "invalid_records": invalid_rows,
        "duplicate_event_ids": duplicates,
        "status": "FAILED" if invalid_rows or duplicates else "PASSED",
        "row_results": row_results,
    }

    output = Path(args.report)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in (
        "records_received", "invalid_records", "duplicate_event_ids", "status"
    )}, indent=2))
    return 1 if report["status"] == "FAILED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
