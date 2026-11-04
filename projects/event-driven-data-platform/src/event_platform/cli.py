"""Command-line entry point for local event processing."""
from __future__ import annotations

import argparse
from pathlib import Path

from event_platform.io import read_jsonl, write_jsonl
from event_platform.processor import process_events


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and route order events")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    events = read_jsonl(args.input)
    accepted, rejected = process_events(events)
    write_jsonl(args.output / "accepted.jsonl", accepted)
    write_jsonl(args.output / "dead_letter.jsonl", rejected)
    print(f"processed={len(events)} accepted={len(accepted)} rejected={len(rejected)}")


if __name__ == "__main__":
    main()
