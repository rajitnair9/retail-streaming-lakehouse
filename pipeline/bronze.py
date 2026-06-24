from pyspark import pipelines as dp
from pyspark.sql.functions import col, from_json, current_timestamp
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, IntegerType
)

# Schema of incoming Kafka JSON event
ORDER_SCHEMA = StructType([
    StructField("order_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("customer_name", StringType()),
    StructField("customer_email", StringType()),
    StructField("customer_phone", StringType()),
    StructField("store_id", StringType()),
    StructField("product_id", StringType()),
    StructField("product_name", StringType()),
    StructField("category", StringType()),
    StructField("quantity", IntegerType()),
    StructField("unit_price", DoubleType()),
    StructField("discount", DoubleType()),
    StructField("total_amount", DoubleType()),
    StructField("payment_method", StringType()),
    StructField("order_status", StringType()),
    StructField("event_timestamp", StringType()),
])

BOOTSTRAP_SERVER = "d8tmi8v73bb9jgbebg00.any.us-east-1.mpx.prd.cloud.redpanda.com:9092"
TOPIC = "retail-orders"
USERNAME = "producer-user"

@dp.table(
    name="bronze_orders",
    comment="Raw retail order events ingested from Redpanda via Kafka connector",
    table_properties={"quality": "bronze"}
)
def bronze_orders():
    return (
        spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", BOOTSTRAP_SERVER)
            .option("subscribe", TOPIC)
            .option("startingOffsets", "earliest")
            .option("kafka.security.protocol", "SASL_SSL")
            .option("kafka.sasl.mechanism", "SCRAM-SHA-256")
            .option("kafka.sasl.jaas.config",
                f'org.apache.kafka.common.security.scram.ScramLoginModule required '
                f'username="{USERNAME}" '
                f'password="{{{{secrets/redpanda/password}}}}";'
            )
            .load()
            .select(
                col("offset"),
                col("timestamp").alias("kafka_timestamp"),
                from_json(col("value").cast("string"), ORDER_SCHEMA).alias("data"),
                current_timestamp().alias("ingested_at")
            )
            .select(
                "offset",
                "kafka_timestamp",
                "data.*",
                "ingested_at"
            )
    )