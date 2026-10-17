CREATE TABLE IF NOT EXISTS checkpoint(stream TEXT PRIMARY KEY, last_event_id INTEGER NOT NULL);
INSERT OR IGNORE INTO checkpoint VALUES ('orders',0);
CREATE TABLE IF NOT EXISTS bronze_events(event_id INTEGER PRIMARY KEY, payload TEXT NOT NULL, run_id TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS quarantine(event_id INTEGER PRIMARY KEY, reason TEXT NOT NULL, payload TEXT NOT NULL, run_id TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS runs(run_id TEXT PRIMARY KEY, started_utc TEXT, status TEXT, input_sha256 TEXT, metrics_json TEXT, error TEXT);
CREATE TABLE IF NOT EXISTS orders(
 order_id INTEGER PRIMARY KEY, order_date TEXT NOT NULL, region TEXT NOT NULL,
 product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, unit_price_cents INTEGER NOT NULL,
 is_deleted INTEGER NOT NULL CHECK(is_deleted IN (0,1)), last_event_id INTEGER NOT NULL, run_id TEXT NOT NULL);
CREATE VIEW IF NOT EXISTS fact_orders AS
 SELECT order_id, order_date AS date_key, region AS region_key, product_id AS product_key,
 quantity, unit_price_cents, quantity*unit_price_cents AS revenue_cents FROM orders WHERE is_deleted=0;
CREATE VIEW IF NOT EXISTS dim_region AS
 SELECT 'East' AS region_key UNION ALL SELECT 'West' UNION ALL SELECT 'South' UNION ALL SELECT 'Central';
CREATE VIEW IF NOT EXISTS dim_product AS
 SELECT DISTINCT product_id AS product_key, 'Synthetic product ' || product_id AS product_name FROM orders;
CREATE VIEW IF NOT EXISTS dim_date AS
 SELECT DISTINCT order_date AS date_key, substr(order_date,1,4) AS year, substr(order_date,1,7) AS month FROM orders;
CREATE VIEW IF NOT EXISTS sales_by_region AS
 SELECT region_key,COUNT(*) AS orders,SUM(quantity) AS units,SUM(revenue_cents) AS revenue_cents
 FROM fact_orders GROUP BY region_key;
