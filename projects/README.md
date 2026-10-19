# Separate projects and combined platform

Each folder is independently runnable and has its own README, synthetic data, tests, deployment notes and evidence. These are separate **project folders within this repository**, not separate GitHub repositories.

| Project | Focus | Local status | Native cloud status |
|---|---|---|---|
| [Snowflake Incremental Orders](snowflake-incremental-orders/) | Versioned upserts, tombstones, replay and late events | Executable reference + tests | SQL starter, unexecuted |
| [Informatica IDMC Order Quality](informatica-idmc-order-quality/) | Decimal validation, routing, deduplication and reconciliation | Executable contract + tests | CDI mapping build specification |
| [Informatica MDM Customer Mastering](informatica-mdm-customer-mastering/) | Golden records, source crosswalk and ambiguous matches | Executable model + tests | MDM SaaS configuration specification |
| [Combined Customer 360 Platform](customer360-idmc-snowflake-fabric/) | IDMC + MDM + Snowflake + Fabric + Power BI | Executable end-to-end local reference + tests | Native integration assets and guides |

Cloud licenses/accounts are required to validate vendor runtimes. No client data, production performance claims, or invented deployment screenshots are included.
