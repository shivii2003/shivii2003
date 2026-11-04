# Production-Style Snowflake + dbt Data Platform

> Independent portfolio implementation for demonstrating data engineering patterns. This is not a Cisco or HCLTech client system and does not claim production deployment.

## Business use case
Ingest order events from a REST API, land immutable raw JSON, load Snowflake, transform with dbt, and publish trusted analytics marts. The design includes incremental processing, SCD Type 2 customer history, data-quality gates, orchestration, observability, and CI.

## Architecture
```text
REST API
  |
  v
Python ingestion (timeouts, retries, pagination, run metadata)
  |
  v
Object storage landing (JSONL, partitioned by ingestion date)
  |
  v
Snowflake RAW  --> COPY INTO / load audit
  |
  v
dbt staging --> intermediate --> marts
  |                |
  |                +--> SCD Type 2 customer dimension
  +--> source freshness + schema/data tests
  |
  v
Analytics consumers

Airflow schedules ingestion and dbt; GitHub Actions runs unit/static checks.
```

## Repository structure
- `src/ingestion/`: API client, pagination, retry, JSONL landing and run metadata
- `src/warehouse/`: Snowflake load orchestration helpers
- `sql/`: Snowflake database, stage, file format, COPY and audit DDL
- `dbt/`: source definitions, staging, incremental facts, SCD2 snapshots, marts and tests
- `dags/`: Airflow DAG
- `tests/`: unit tests with mocked HTTP responses
- `.github/workflows/`: CI validation

## Key engineering decisions
1. **Idempotency:** each source record has a stable business key; dbt incremental models use a unique key and MERGE.
2. **Late-arriving updates:** incremental extraction uses an overlap window; warehouse deduplication selects the newest source version.
3. **SCD Type 2:** dbt snapshot tracks customer attribute changes with validity intervals.
4. **Quality gates:** uniqueness, not-null, relationships, accepted values and freshness checks.
5. **Observability:** structured logs include run ID, source, page count, rows and elapsed time; secrets and payload bodies are never logged.
6. **Recoverability:** raw landing is immutable and partitioned by ingestion date; failed runs can be replayed.
7. **Security:** credentials are injected through environment variables / secret manager; no credentials are committed.

## Local setup
Requires Python 3.11+, Airflow 2.9+ (or its supported constraints), dbt Core with dbt-snowflake, and access to a Snowflake development account for warehouse execution.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest -q
```

Configure the environment variables in `.env` and dbt profile before running against your own development environment. Never commit `.env`.

## Run dbt
From the `dbt/` directory after configuring a profile:
```bash
dbt debug
dbt deps
dbt build
dbt docs generate
```

## Snowflake deployment sequence
1. Run `sql/00_setup.sql` using an appropriately privileged development role.
2. Create a storage integration / external stage according to your cloud provider's security policy.
3. Configure the named stage and file format in `sql/01_ingestion_objects.sql`.
4. Load a test batch using `sql/02_load_raw.sql`.
5. Validate row counts and load audit records before enabling scheduled runs.

## Airflow
Place `dags/orders_pipeline.py` in the Airflow DAG folder and configure the `orders_ingestion` connection/variables. The DAG is a reference orchestration example; adapt operators and credentials to your Airflow deployment.

## Validation status
Source code and configuration are committed as a portfolio example. A live Snowflake account, object-storage credentials, Airflow runtime and dbt adapter are not connected in this repository environment; therefore no live warehouse run or CI result is claimed.

## Roadmap
- Add cloud-specific external stage and storage integration deployment templates
- Add dbt unit tests and CI against a disposable warehouse
- Add alerting integration and operational SLO dashboards
- Add Terraform for repeatable infrastructure provisioning
