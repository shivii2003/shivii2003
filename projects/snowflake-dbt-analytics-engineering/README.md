# Snowflake + dbt Analytics Engineering

> Portfolio case study: a reproducible analytics-engineering example. This is an independent demonstration project, not a Cisco or HCLTech client implementation.

## Business scenario
A retail business receives daily order and customer extracts. Analysts need trusted, deduplicated models for revenue, customer activity, and product performance.

## Architecture
```text
Raw files / source tables
        |
        v
Snowflake RAW schema
        |
        v
dbt staging models  --> source freshness + schema tests
        |
        v
dbt intermediate models
        |
        v
dbt marts (facts + dimensions)
        |
        v
BI / analytics consumers
```

## Skills demonstrated
- Snowflake database, schema, warehouse and role design
- dbt sources, staging/intermediate/mart layering
- Incremental model pattern and unique-key strategy
- Jinja macros and reusable SQL
- Data tests: not_null, unique, relationships, accepted_values
- Snapshot strategy for tracking customer attribute changes
- Documentation, lineage and CI validation

## Repository map
- `models/staging/`: source-aligned cleanup and standardisation
- `models/intermediate/`: reusable business logic
- `models/marts/`: facts and dimensions
- `macros/`: reusable SQL/Jinja helpers
- `snapshots/`: slowly changing dimension example
- `tests/`: business-rule and reconciliation tests
- `sql/`: Snowflake setup and operational SQL

## Run locally
1. Install dbt Core and the Snowflake adapter.
2. Copy `profiles.yml.example` into your dbt profile directory and configure credentials through environment variables.
3. Run `dbt deps`, `dbt debug`, `dbt seed`, `dbt build`.
4. Review generated docs using `dbt docs generate` and `dbt docs serve`.

Never commit credentials, private datasets, or production connection details.

## Engineering decisions
- Keep source cleaning separate from business transformations.
- Use incremental processing only where a reliable change timestamp and unique key exist.
- Test grain and join relationships to prevent fan-out.
- Treat freshness and reconciliation checks as deployment gates.

## Next enhancements
Add Snowflake query-history monitoring, cost-aware warehouse sizing, deployment environments, and CI jobs against a non-production account.

## Connect
[LinkedIn — Shivam Mathur](https://www.linkedin.com/in/shivam-mathur-172751289)
