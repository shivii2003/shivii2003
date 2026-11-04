# End-to-End Data Engineering Platform (Portfolio Project)

> Independent portfolio project demonstrating skills relevant to a Data Engineer role: Python, SQL, Snowflake, dbt, AWS S3 concepts, API ingestion, data quality, GitHub Actions and CI/CD. This is a demonstration project, not Cisco or HCLTech client work.

## Architecture

```text
REST API / CSV source
        |
        v
Python ingestion (pagination, retries, structured logs)
        |
        v
Local landing / AWS S3 landing zone (configurable)
        |
        v
Snowflake RAW schema
        |
        v
dbt staging -> intermediate -> marts
        |
        +--> dbt tests / source freshness / documentation
        |
        v
Analytics-ready tables
```

## JD skill mapping

| Job requirement | Evidence in this project |
|---|---|
| Python | API client, retries, validation, structured logging |
| Advanced SQL | deduplication, window functions, incremental MERGE pattern |
| Snowflake | database/schema/table DDL and warehouse loading design |
| dbt | layered models, tests, sources, incremental model |
| ETL/ELT | API/CSV ingestion followed by warehouse transformations |
| AWS | S3 landing-zone integration design and configuration |
| Git + CI/CD | GitHub Actions for Python tests and dbt validation |
| Reliability | idempotent loads, data quality checks, error handling |
| APIs / microservices | separable ingestion module with a CLI entry point |

Matillion and Meltano are listed as preferred JD tools; this repository does not claim hands-on production use of either. An orchestration adapter can be added after validating the exact workflow.

## Repository layout

- `ingestion/`: API extraction, normalization and local landing
- `snowflake/`: warehouse bootstrap SQL
- `dbt/`: staging and mart transformations, schema tests
- `tests/`: Python unit tests
- `.github/workflows/`: CI checks

## Run locally

1. Python 3.11+
2. Create a virtual environment and install `requirements.txt`.
3. Copy `.env.example` to `.env` and configure a public demo API URL.
4. Run `python -m ingestion.pipeline --output data/landing/events.jsonl`.
5. Run `pytest`.

No credentials are committed. Snowflake and AWS execution require your own account and environment variables; never add secrets to Git.

## Snowflake/dbt execution

1. Execute `snowflake/00_create_objects.sql` in a development Snowflake account.
2. Configure a dbt profile using environment variables (see `dbt/profiles.yml.example`).
3. Configure the source in `dbt/models/staging/sources.yml`.
4. Run `dbt debug`, `dbt run`, and `dbt test` from the `dbt/` directory.

## Engineering decisions

- Keep extraction separate from warehouse transformation (ELT).
- Persist raw payloads before applying business logic.
- Use deterministic event IDs for deduplication.
- Make retries bounded and observable.
- Add tests at ingestion and warehouse-model layers.
- Keep secrets and environment-specific configuration outside version control.

## Next enhancements

- Add an AWS S3 storage adapter and Snowflake COPY INTO task.
- Add dbt snapshots, incremental marts and source freshness.
- Add deployment environments and protected approvals.
- Add orchestration with a JD-relevant scheduler after confirming tool access.

## Connect
[LinkedIn — Shivam Mathur](https://www.linkedin.com/in/shivam-mathur-172751289)
