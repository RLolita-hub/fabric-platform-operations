# Informatica IDMC Order Quality

Standardize order feeds and reject invalid data before certified targets.

**Status:** independently runnable Python reference implementation with synthetic data and tests. Native vendor deployment is pending. Local Python/SQLite execution is not evidence of Snowflake or Informatica runtime execution. No paid account is needed for this local demo.

## Run
From this project directory, with Python 3.10+:
```sh
python -m unittest discover -s tests -v
python src/mapping_contract.py
```
Expected: 2 accepted orders, 3 rejected rows, 1 duplicate, 20000 accepted cents.

## Architecture
Source CSV → expression validation → routing → duplicate gate → accepted/reject targets

## Contents
`src/`: executable contract; `data/`: synthetic fixtures; `tests/`: failure/edge cases; `cloud/`: native setup starter; `evidence/`: captured local results. This project runs without importing sibling project folders.

## Native deployment
See [cloud/mapping-build.md](cloud/mapping-build.md). Work in a dedicated DEV environment. Native Snowflake needs a warehouse, database/schema and least-privilege role; compute/storage may incur charges. IDMC needs suitable CDI connectors/runtime and entitlement; MDM SaaS requires its own entitlement. Do not assume every IDMC trial includes MDM. Store credentials in platform connections, never Git. Start with the synthetic inputs, run acceptance cases, capture native job/query IDs, and only then label deployment verified.

## Demonstration
Show the business problem, run tests, inspect output, introduce a bad record, rerun, and explain the exception. Capture screenshots of actual results under evidence/. No fabricated UI screenshots or production claims are supplied.

## Interview talking points
Explain the key, duplicate policy, rejection policy, retry behavior, recovery boundary and local-versus-native differences. Discuss why source data must be validated before a target write and why successful code execution alone does not establish business reconciliation.

## Limitations
These are small contract demos. Native connectors, scale/performance, access policies, monitoring and production deployment require separate validation. Review [design limitations](docs/limitations.md) before adapting.

## Related integrated project
[Customer 360: IDMC + MDM + Snowflake + Fabric + Power BI](../customer360-idmc-snowflake-fabric/README.md)

## References
[Snowflake MERGE](https://docs.snowflake.com/en/sql-reference/sql/merge) · [Informatica Business 360 mappings](https://docs.informatica.com/integration-cloud/cloud-data-integration-connectors/current-version/business-360-connector/mappings-with-business-360-connector-overview.html) · [Informatica Snowflake SQL ELT syntax](https://docs.informatica.com/integration-cloud/data-integration-free-and-paygo/current-version/snowflake-data-cloud-connector/part-3--sql-elt-with-snowflake-data-cloud-connector/mappings-in-sql-elt-mode-for-snowflake-data-cloud/functions-in-mappings-in-sql-elt-mode.html)
