"""Small, testable API-to-landing ETL ingestion example."""
from __future__ import annotations

import argparse
import json
import logging
import os
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

LOGGER = logging.getLogger("data_ingestion")


def fetch_records(base_url: str, resource: str, timeout: int = 20,
                  max_retries: int = 3) -> list[dict[str, Any]]:
    """Fetch records from a REST endpoint with bounded retries."""
    url = f"{base_url.rstrip('/')}/{resource.lstrip('/')}"
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, list) or not all(isinstance(x, dict) for x in payload):
                raise ValueError("Expected a JSON array of objects")
            LOGGER.info("Fetched %d records from %s", len(payload), url)
            return payload
        except (requests.RequestException, ValueError):
            if attempt >= max_retries:
                LOGGER.exception("API ingestion failed after %d attempts", attempt + 1)
                raise
            wait_seconds = min(2 ** attempt, 8)
            LOGGER.warning("Attempt %d failed; retrying in %ss", attempt + 1, wait_seconds)
            time.sleep(wait_seconds)
    return []


def normalize_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize API records into a stable raw-event envelope."""
    normalized = []
    for record in records:
        if record.get("id") is None:
            LOGGER.warning("Skipping record without id")
            continue
        normalized.append({
            "event_id": str(record["id"]),
            "source_system": "rest_api",
            "payload": record,
        })
    return normalized


def write_jsonl(records: list[dict[str, Any]], output_path: str) -> int:
    """Write newline-delimited JSON to a landing file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    LOGGER.info("Wrote %d records to %s", len(records), path)
    return len(records)


def run(output_path: str) -> int:
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    base_url = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
    resource = os.getenv("API_RESOURCE", "posts")
    timeout = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20"))
    retries = int(os.getenv("MAX_RETRIES", "3"))
    records = fetch_records(base_url, resource, timeout, retries)
    return write_jsonl(normalize_records(records), output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="REST API to JSONL landing pipeline")
    parser.add_argument("--output", default="data/landing/events.jsonl")
    args = parser.parse_args()
    run(args.output)
