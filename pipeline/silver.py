from pyspark import pipelines as dp
from pyspark.sql.functions import col, to_timestamp, upper

@dp.table(
    name="silver_orders",
    comment="Cleaned and validated retail orders with data quality expectations",
    table_properties={"quality": "silver"}
)
@dp.expect("valid_order_id", "order_id IS NOT NULL")
@dp.expect("valid_customer_id", "customer_id IS NOT NULL")
@dp.expect("valid_total_amount", "total_amount > 0")
@dp.expect("valid_quantity", "quantity > 0 AND quantity <= 100")
@dp.expect_or_drop("valid_order_status", "order_status IN ('PLACED', 'CONFIRMED', 'CANCELLED')")
@dp.expect_or_fail("valid_product_id", "product_id IS NOT NULL")
def silver_orders():
    return (
        dp.read_stream("bronze_orders")
            .select(
                col("order_id"),
                col("customer_id"),
                col("customer_name"),
                col("customer_email"),
                col("customer_phone"),
                col("store_id"),
                col("product_id"),
                col("product_name"),
                col("category"),
                col("quantity").cast("integer"),
                col("unit_price").cast("double"),
                col("discount").cast("double"),
                col("total_amount").cast("double"),
                col("payment_method"),
                upper(col("order_status")).alias("order_status"),
                to_timestamp(col("event_timestamp")).alias("event_timestamp"),
                col("kafka_timestamp"),
                col("ingested_at")
            )
    )