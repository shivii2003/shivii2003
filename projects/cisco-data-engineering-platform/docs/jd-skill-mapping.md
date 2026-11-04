# Cisco Data Engineer JD: Skill-to-evidence map

This document maps the job requirements discussed for the target role to concrete evidence in this independent portfolio project. It is not a claim of Cisco employment or client production deployment.

| JD area | Repository evidence | What a reviewer can inspect |
|---|---|---|
| Python | `ingestion/pipeline.py`, `tests/` | REST extraction, retries, validation, JSONL landing, unit tests |
| Advanced SQL | `dbt/models/` | Deduplication with `ROW_NUMBER`, typed projections, incremental model |
| Snowflake | `snowflake/00_create_objects.sql`, dbt profile example | Database/schema/table design and VARIANT raw payload |
| dbt | `dbt/` | Layered models, source definitions, schema tests |
| ETL/ELT | `ingestion/` + `dbt/` | Separate extraction/landing and warehouse transformations |
| AWS | `ingestion/s3_landing.py` | Optional S3 landing adapter using IAM/default credential chain |
| Git + CI/CD | `.github/workflows/ci.yml` | Automated test run on push and pull request |
| Reliability/performance | bounded retries, deterministic IDs, deduplication | Failure handling and duplicate control |
| API/microservices | ingestion module has a clear callable interface and CLI | Separation of ingestion responsibility from warehouse transforms |
| Agile/Jira | Suggested delivery breakdown below | Backlog-ready stories and acceptance criteria |

## Suggested Agile backlog

1. **Story: API ingestion** — As a data engineer, I can extract source records with bounded retries and structured logs. Acceptance: API failure is retried; malformed records are rejected; unit tests pass.
2. **Story: Raw landing** — As a data engineer, I can persist source payloads before transformation. Acceptance: JSONL output is deterministic and can optionally be uploaded to S3.
3. **Story: Warehouse modelling** — As an analyst, I can query deduplicated and typed event data. Acceptance: dbt models build and uniqueness/not-null tests pass.
4. **Story: CI quality gate** — As a team member, I want pull requests to run automated tests. Acceptance: GitHub Actions reports test status on pull requests.

## Preferred tools

Matillion and Meltano were listed as preferred in the JD. They are not falsely represented as implemented in this repository. Add a real orchestration integration only after building and testing it in an accessible environment.
