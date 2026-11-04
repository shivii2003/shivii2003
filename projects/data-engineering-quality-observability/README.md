# Data Engineering Quality & Observability

> Independent portfolio case study showing how a data pipeline can fail safely and provide actionable operational signals. Not a production client system.

## Scenario
A scheduled ingestion job loads API events into a warehouse. The team needs to detect schema drift, duplicate business keys, missing required fields, late-arriving data, and unexpected volume changes before downstream reporting is affected.

## Quality dimensions
| Dimension | Example control | Expected response |
|---|---|---|
| Completeness | Required fields are populated | Quarantine invalid rows |
| Uniqueness | Event key is unique | Deduplicate or fail the batch |
| Validity | Timestamp and status are valid | Reject malformed records |
| Freshness | Latest event is within SLA | Alert on late data |
| Volume | Row count within baseline range | Warn and investigate |
| Reconciliation | Source and target counts align | Block promotion if mismatch |

## Components
- Python validation library with deterministic rule results
- SQL checks for duplicate keys, nulls and freshness
- JSON quality report suitable for CI artifacts
- Pytest unit tests
- GitHub Actions workflow for pull-request validation

## Suggested execution
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python quality/run_checks.py --input sample/events.jsonl --report reports/quality-report.json
```

## Operational principles
- Separate warning-level checks from release-blocking checks.
- Include batch ID, run ID, source name and check name in every result.
- Never log secrets or full sensitive payloads.
- Make checks deterministic and test them with both valid and invalid fixtures.

## Extension roadmap
Integrate Snowflake query history, dbt test artifacts, alert routing, and an orchestration layer such as Airflow or Dagster.
