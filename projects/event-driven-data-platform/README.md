# Event-Driven Data Platform — Portfolio Project

[![Tests](https://github.com/shivii2003/shivii2003/actions/workflows/event-platform-tests.yml/badge.svg)](https://github.com/shivii2003/shivii2003/actions/workflows/event-platform-tests.yml)

> Independent engineering case study. This is a local, testable reference implementation, not a production client deployment.

## Scenario
A commerce platform emits order events from multiple services. The data platform must validate incoming payloads, deduplicate events, route invalid records to a dead-letter stream, and expose warehouse-ready records for Snowflake and dbt.

## Architecture
```text
Order service / REST events
        |
        v
Python event ingestion API
        |
        v
Schema validation + idempotency
        |                         |
        v                         v
Accepted JSONL stream        Dead-letter JSONL
        |
        v
Snowflake RAW tables
        |
        v
dbt staging -> incremental facts -> analytics marts
        |
        v
BI / downstream consumers
```

## Engineering features
- Typed event contract and required-field validation
- Idempotency using `event_id`
- Explicit accepted / rejected outcomes with reason codes
- Append-only JSONL sink for replayable local development
- Snowflake DDL and MERGE pattern for warehouse ingestion
- dbt staging model and incremental fact model
- Unit tests for valid, invalid, duplicate and replayed events, plus JSONL I/O edge cases
- Pytest coverage reporting in local runs and GitHub Actions

## Run locally
Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python -m event_platform.cli --input sample/orders.jsonl --output build
```

The local pipeline writes accepted records to `build/accepted.jsonl` and invalid records to `build/dead_letter.jsonl`. Re-running the same input is safe because event IDs are deduplicated within each run.

## Warehouse implementation
1. Review and execute `sql/00_raw_schema.sql` in a Snowflake development database.
2. Stage the accepted JSONL file using a secure internal/external stage.
3. Apply the MERGE pattern in `sql/01_merge_orders.sql`.
4. Configure dbt using `dbt/profiles.yml.example`.
5. Run `dbt debug` and `dbt build`.

## Repository layout
- `src/event_platform/`: contracts, validation, processing and CLI
- `tests/`: unit tests
- `sample/`: synthetic order events
- `sql/`: Snowflake RAW DDL and MERGE example
- `dbt/`: source, staging and mart models

## Validation status
The Python unit-test suite and coverage reporting are configured in GitHub Actions. Check the workflow badge above for the live run result; a green badge is required before describing the CI as passing. Snowflake and dbt require a separately configured development account and have not been run from this repository environment.

## Design notes
- Never treat a duplicate event as a new business transaction.
- Keep raw ingestion separate from business transformation.
- Preserve rejected payloads with machine-readable reasons for diagnosis.
- Do not log secrets or unnecessary personal data.
- Use synthetic data only in this repository.

## Connect
[LinkedIn — Shivam Mathur](https://www.linkedin.com/in/shivam-mathur-172751289) · [GitHub Profile](https://github.com/shivii2003)
