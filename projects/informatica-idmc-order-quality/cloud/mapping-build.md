# IDMC Cloud Data Integration implementation

Manual build specification, not a native export. Requires a CDI entitlement, appropriate connector and supported runtime. Native execution is pending.

Create project `OrderQuality` and a mapping with Source (orders.csv) → Expression (trim keys, uppercase currency, validate decimal scale) → Router (valid/invalid) → Aggregator or pre-target duplicate gate → accepted/rejected targets. Do not cast decimals to integer before checking fractional cents. Conflicting payloads for one source/order key must fail the batch; exact duplicates may collapse.

Configure mapping task parameters for source path, target connection and batch ID. Store credentials in IDMC connections. In a taskflow run staging first, then count/reconcile, then publish only on success. Capture source rows, duplicates, accepted/rejected rows, accepted amount, status and task ID. Keep raw values in restricted staging; do not include payloads in email alerts.

Fixture acceptance: 6 input rows = 2 accepted + 3 rejected + 1 exact duplicate. Accepted revenue = 20000 cents. IDMC expression syntax and decimal conversion must be validated in your tenant; Python is the reference contract only. Capture task logs and sanitized native mapping export after executing these cases.

For a Snowflake destination, use the licensed Snowflake Data Cloud connector. For SQL ELT mappings use Snowflake-native expression syntax as documented, not Informatica expressions. See the primary reference in README.

Debug exercise: change the duplicate O2 amount to 75.00. The entire local result must fail before publication. In IDMC validate that the failure branch also prevents certified target promotion.
