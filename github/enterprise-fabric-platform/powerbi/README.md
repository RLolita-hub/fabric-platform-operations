# Build the first report — pending execution in Power BI Desktop

1. Run the local pipeline and export. In Desktop, import fact_orders, dim_region, dim_product and dim_date CSV files from build/exports.
2. Set order ID, product key, quantity and cents to whole numbers; date keys to Date; region to Text. Check delimiter and locale.
3. Create one-to-many, single-direction relationships from each dimension key to the matching fact key. Never join the dimension tables to each other. Disable automatic relationship assumptions if they create extra joins.
4. Add measures.dax, one measure at a time. Format Revenue/AOV as currency; counts as integers. This example is USD only.
5. Executive page: Revenue, Order Count, Units, AOV cards; regional revenue bar chart; order detail table. Do not fabricate a time-series trend from a one-day fixture. Expand the generator before a time-intelligence demonstration.
6. Operations page: import runs and quarantine CSVs; display failure status and rule counts. Audit metrics_json can be parsed in Power Query. Refresh exports after each local run.
7. Validate final total $165, five active orders, East $95, South $50, West $20. Batch 2's total before corrections is $125. The deleted order 102 must be absent.
8. Static RLS exercise: define EastReader on dim_region with `[region_key] = "East"`. View as role: $95 / three orders. Dynamic user-to-region security and service viewer tests belong in Project 3; Desktop View as is not a complete service security test.
9. Save your PBIX locally; inspect it for cached data and paths before publishing. This fixture is synthetic, but do not reuse an employer PBIX. Capture screenshots only after actual execution.

A real date dimension should cover every calendar day and have a declared fiscal calendar. The included sparse dimension is intentional for the first small test fixture; do not claim YTD support.
