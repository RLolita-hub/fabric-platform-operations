-- Run ONLY in a new Fabric Warehouse lab, not the Lakehouse SQL endpoint.
-- Unexecuted starter. First create tables; load staging with a Fabric Copy activity.
CREATE TABLE dbo.stg_orders (
 order_id BIGINT, order_date DATE, region VARCHAR(20), product_id BIGINT,
 quantity BIGINT, unit_price_cents BIGINT, revenue_cents BIGINT
);
CREATE TABLE dbo.fact_orders (
 order_id BIGINT, date_key DATE, region_key VARCHAR(20), product_key BIGINT,
 quantity BIGINT, unit_price_cents BIGINT, revenue_cents BIGINT
);
CREATE TABLE dbo.dim_region (region_key VARCHAR(20));
CREATE TABLE dbo.dim_product (product_key BIGINT, product_name VARCHAR(100));
CREATE TABLE dbo.dim_date (date_key DATE);
-- STOP HERE until Copy has loaded portfolio_gold_orders into dbo.stg_orders.
-- For this exact synthetic fixture, first check 5 rows and 16,500 cents.
SELECT COUNT(*) AS active_orders, SUM(revenue_cents) AS revenue_cents FROM dbo.stg_orders;
SELECT order_id, COUNT(*) AS duplicates FROM dbo.stg_orders GROUP BY order_id HAVING COUNT(*)>1;
-- Gate publication in the orchestrator on count=5, cents=16500, duplicates=0.
-- Run the following batch only after those checks pass; one publisher at a time.
BEGIN TRANSACTION;
DELETE FROM dbo.fact_orders;
DELETE FROM dbo.dim_region;
DELETE FROM dbo.dim_product;
DELETE FROM dbo.dim_date;
INSERT INTO dbo.fact_orders SELECT order_id,order_date,region,product_id,quantity,unit_price_cents,revenue_cents FROM dbo.stg_orders;
INSERT INTO dbo.dim_region SELECT DISTINCT region FROM dbo.stg_orders;
INSERT INTO dbo.dim_product SELECT DISTINCT product_id,CONCAT('Synthetic product ',product_id) FROM dbo.stg_orders;
INSERT INTO dbo.dim_date SELECT DISTINCT order_date FROM dbo.stg_orders;
COMMIT;
