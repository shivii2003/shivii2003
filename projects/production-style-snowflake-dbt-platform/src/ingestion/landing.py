from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from uuid import uuid4


def write_jsonl(
    records: Iterable[dict],
    landing_dir: str,
    source_name: str,
    run_id: str | None = None,
) -> tuple[Path, int, str]:
    """Write immutable JSONL batch partitioned by UTC ingestion date."""
    current_run_id = run_id or str(uuid4())
    now = datetime.now(timezone.utc)
    folder = Path(landing_dir) / source_name / f"ingest_date={now:%Y-%m-%d}"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"run_id={current_run_id}.jsonl"
    count = 0
    with path.open("x", encoding="utf-8") as stream:
        for record in records:
            enriched = {
                "record": record,
                "_ingested_at": now.isoformat(),
                "_run_id": current_run_id,
                "_source": source_name,
            }
            stream.write(json.dumps(enriched, separators=(",", ":")) + "\n")
            count += 1
    return path, count, current_run_id
