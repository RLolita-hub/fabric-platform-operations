-- Snowflake DEV starter. Native execution pending; use a dedicated lab schema.
CREATE TABLE IF NOT EXISTS ORDER_EVENTS_STAGE(order_id VARCHAR, version NUMBER(18,0), amount_cents NUMBER(18,0), op VARCHAR);
CREATE TABLE IF NOT EXISTS ORDERS_CURRENT LIKE ORDER_EVENTS_STAGE;
ALTER SESSION SET ERROR_ON_NONDETERMINISTIC_MERGE=TRUE;
-- Before MERGE, orchestration MUST abort if any of these checks returns rows:
SELECT order_id,version FROM (SELECT DISTINCT * FROM ORDER_EVENTS_STAGE)
GROUP BY order_id,version HAVING COUNT(*)>1;
SELECT * FROM ORDER_EVENTS_STAGE WHERE order_id IS NULL OR order_id='' OR version IS NULL OR version<1 OR amount_cents IS NULL OR amount_cents<0 OR op IS NULL OR op NOT IN ('UPSERT','DELETE');
SELECT s.* FROM ORDER_EVENTS_STAGE s JOIN ORDERS_CURRENT t
ON s.order_id=t.order_id AND s.version=t.version
WHERE s.amount_cents<>t.amount_cents OR s.op<>t.op;
-- The above SELECTs are diagnostic gates, not automatic exceptions. Do not run
-- the MERGE until checks pass. Use a single writer and immutable validated stage.
MERGE INTO ORDERS_CURRENT t USING (
  SELECT * FROM ORDER_EVENTS_STAGE
  QUALIFY ROW_NUMBER() OVER(PARTITION BY order_id ORDER BY version DESC)=1
) s ON t.order_id=s.order_id
WHEN MATCHED AND s.version>t.version THEN UPDATE SET version=s.version,amount_cents=s.amount_cents,op=s.op
WHEN NOT MATCHED THEN INSERT(order_id,version,amount_cents,op) VALUES(s.order_id,s.version,s.amount_cents,s.op);
-- Retain tombstones to stop older updates resurrecting deleted orders.
CREATE OR REPLACE VIEW ACTIVE_ORDERS AS SELECT * FROM ORDERS_CURRENT WHERE op='UPSERT';
