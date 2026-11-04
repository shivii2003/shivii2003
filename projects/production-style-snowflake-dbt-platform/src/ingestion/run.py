from __future__ import annotations

import argparse
import logging
import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

from ingestion.client import ApiClient
from ingestion.landing import write_jsonl

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("orders_ingestion")


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", default="orders")
    parser.add_argument("--updated-since")
    args = parser.parse_args()

    base_url = os.environ["API_BASE_URL"]
    token = os.environ["API_TOKEN"]
    overlap = int(os.getenv("API_OVERLAP_MINUTES", "15"))
    updated_since = args.updated_since or (
        datetime.now(timezone.utc) - timedelta(minutes=overlap)
    ).isoformat()

    client = ApiClient(
        base_url=base_url,
        token=token,
        timeout_seconds=int(os.getenv("API_TIMEOUT_SECONDS", "30")),
        max_retries=int(os.getenv("API_MAX_RETRIES", "4")),
        page_size=int(os.getenv("API_PAGE_SIZE", "200")),
    )

    records = list(client.fetch_records(args.endpoint, updated_since))
    path, count, run_id = write_jsonl(
        records,
        os.getenv("LANDING_DIR", "data/landing"),
        args.endpoint.replace("/", "_"),
    )
    logger.info(
        "ingestion_complete run_id=%s source=%s rows=%s landing_file=%s",
        run_id, args.endpoint, count, path
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
