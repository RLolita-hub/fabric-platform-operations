# Deployment and costs

## Local, zero cloud spend

Python 3.10+, terminal and optionally Git; no third-party Python dependencies. Extract the repository and follow README. Power BI Desktop is optional and requires a compatible Windows setup. CSV outputs can also be inspected in a spreadsheet, but that does not demonstrate Power BI implementation.

## GitHub publication

No GitHub destination is configured in this package. Create a public repository named `enterprise-fabric-platform` in your own account, without an initialized README. Replace YOUR_USERNAME below. Review tracked files before push; only synthetic input and evidence belong here.

```sh
git init
git add .
git diff --cached --stat
git commit -m "Add tested local retail pipeline and Fabric implementation plan"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/enterprise-fabric-platform.git
git push -u origin main
```

Use GitHub's normal sign-in/credential manager; never paste a token into a remote URL. In Actions, confirm the actual test run before adding a passing badge. Add topics: data-engineering, microsoft-fabric, azure-data-factory, python, sql, power-bi. Pin only after the README opens correctly and tests pass.

## Fabric learning deployment — separate acceptance gate

Prerequisites: personal/authorized lab Entra work or school account; Fabric-enabled tenant; workspace creation rights; trial or paid capacity. A standard Fabric trial lasts 60 days, but eligibility, available SKU and tenant restrictions vary. Do not assume a trial is available. Power BI sharing and viewing have separate licensing requirements. Check your actual account before provisioning.

1. Create a lab workspace and Lakehouse. Do not use the client's tenant or production workspace.
2. Upload data/*.jsonl under Lakehouse Files/portfolio_orders/.
3. Create a notebook, attach the Lakehouse, paste cloud/fabric_silver_starter.py. Run and capture runtime version, table counts and assertion outputs. This is a full-fixture rebuild prototype, not the local pipeline's full contract.
4. Inspect quarantine and silver tombstones. Run again and confirm the same current state. Add the missing exact-schema, gap, bronze, audit and checkpoint behaviors identified in the notebook comments before claiming parity.
5. Create a Warehouse. Execute only the DDL section of warehouse_starter.sql. Create a Fabric pipeline Copy activity from Lakehouse portfolio_gold_orders to Warehouse dbo.stg_orders, using full replacement for this small fixture.
6. Add pre-publication validation (five rows, 16,500 cents, no duplicate keys). Run the publication SQL only if it passes. Link the semantic model to the Warehouse gold tables and apply the Power BI instructions.
7. Add a Fabric Data Factory notebook activity, Copy activity, validation gate, SQL publication and semantic-model refresh; serialize runs. Export the real pipeline definition after configuration. No importable pipeline JSON is claimed in this package.
8. Only after this succeeds, add ADF + ADLS ingestion using a managed identity and least-privilege data access. Export and sanitize actual connections/pipelines; retain parameter templates, never credentials.
9. Capture a failed run before silver publication and another after silver but before gold. Demonstrate idempotent recovery without lost source offsets. Record actual capacity, input size, runtime and observed cost.
10. Stop schedules after demonstrations, review/delete unused paid resources, and export artifacts before trial expiry. A budget alert alone is not a spending cap.

ADF activity/integration-runtime usage, ADLS storage/transactions, Azure SQL/Synapse compute and Fabric paid capacity can incur costs. This package provisions none. Do not estimate cost without region, SKU, schedule and run volumes. Avoid a dedicated Synapse pool for an initial portfolio demo. Power Apps Developer Plan is for development/test, not production; premium connectors, hosted flows, Copilot Studio and LLM calls need separate entitlement/cost checks.

## Official references checked 2026-10-16

- https://learn.microsoft.com/en-us/fabric/fundamentals/fabric-trial
- https://learn.microsoft.com/en-us/fabric/enterprise/licenses
- https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-sql-analytics-endpoint
- https://learn.microsoft.com/en-us/fabric/data-factory/incremental-copy-job
- https://learn.microsoft.com/en-us/fabric/admin/metadata-scanning-setup
- https://learn.microsoft.com/en-us/power-platform/developer/plan
- https://docs.github.com/en/pages/quickstart

The Lakehouse SQL analytics endpoint is read-only over Delta data. Warehouse DML belongs in Warehouse; Spark writes Lakehouse Delta. Metadata scanning needs Fabric admin setup and read-only admin API authorization. Use synthetic scanner fixtures until a lab admin grants access.
