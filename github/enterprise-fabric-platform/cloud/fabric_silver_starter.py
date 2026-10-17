"""Fabric notebook starter, NOT cloud-tested. Attach a personal lab Lakehouse.

Upload the three synthetic JSONL files to Files/portfolio_orders/.
This rebuilds from all files; incremental orchestration/bronze/checkpoint is NOT implemented here.
Use only this synthetic lab folder. Runtime supplies spark and Delta Lake.
"""
from pyspark.sql import functions as F, Window
from pyspark.sql.types import StructType, StructField, LongType, StringType
from delta.tables import DeltaTable

spark.conf.set('spark.sql.ansi.enabled', 'false')
schema = StructType([StructField('event_id',LongType()),StructField('order_id',LongType()),
    StructField('operation',StringType()),StructField('order_date',StringType()),
    StructField('region',StringType()),StructField('product_id',LongType()),
    StructField('quantity',LongType()),StructField('unit_price_cents',LongType()),
    StructField('_corrupt_record',StringType())])
raw=spark.read.schema(schema).option('mode','PERMISSIVE').json('Files/portfolio_orders/*.jsonl').cache()
raw.count()  # materialize before inspecting corrupt rows
if raw.filter(F.col('_corrupt_record').isNotNull() | F.col('event_id').isNull() | (F.col('event_id')<=0)).count():
    raise ValueError('Malformed records / event IDs: stop and inspect original source files')
cols=[c for c in raw.columns if c!='_corrupt_record']
distinct=raw.select(cols).dropDuplicates()
if distinct.groupBy('event_id').count().filter('count > 1').count():
    raise ValueError('Conflicting event IDs')
valid=(F.col('order_id')>0)&(F.col('product_id')>0)&F.col('quantity').between(1,100000)&F.col('unit_price_cents').between(0,100000000)&F.col('region').isin('East','West','South','Central')&F.col('operation').isin('UPSERT','DELETE')&(F.date_format(F.to_date('order_date'),'yyyy-MM-dd')==F.col('order_date'))
checked=distinct.withColumn('valid',F.coalesce(valid,F.lit(False)))
checked.filter(~F.col('valid')).write.format('delta').mode('overwrite').saveAsTable('portfolio_quarantine')
latest=(checked.filter('valid').drop('valid').withColumn('rn',F.row_number().over(Window.partitionBy('order_id').orderBy(F.desc('event_id')))).filter('rn=1').drop('rn').withColumn('is_deleted',F.col('operation')=='DELETE'))
name='portfolio_silver_orders'
if not spark.catalog.tableExists(name):
    latest.write.format('delta').saveAsTable(name)
else:
    (DeltaTable.forName(spark,name).alias('t').merge(latest.alias('s'),'t.order_id=s.order_id')
     .whenMatchedUpdateAll(condition='s.event_id > t.event_id').whenNotMatchedInsertAll().execute())
current=spark.table(name).filter('not is_deleted')
current.select('order_id','order_date','region','product_id','quantity','unit_price_cents',
               (F.col('quantity')*F.col('unit_price_cents')).alias('revenue_cents')).write.format('delta').mode('overwrite').saveAsTable('portfolio_gold_orders')
assert current.count()==5, 'Synthetic fixture expected 5 active orders'
assert current.select(F.sum(F.col('quantity')*F.col('unit_price_cents'))).first()[0]==16500
# Exact unknown-field validation, bronze retention, sequence-gap checks, audit and
# multi-table publication are required before calling this the cloud equivalent.
