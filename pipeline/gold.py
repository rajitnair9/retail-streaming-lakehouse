from pyspark import pipelines as dp
from pyspark.sql.functions import col, sum, count, avg, date_trunc

@dp.table(
    name="gold_sales_by_store",
    comment="Aggregated sales metrics by store and hour",
    table_properties={"quality": "gold"}
)
def gold_sales_by_store():
    return (
        dp.read_stream("silver_orders")
            .where(col("order_status") == "CONFIRMED")
            .groupBy(
                date_trunc("hour", col("event_timestamp")).alias("event_hour"),
                col("store_id")
            )
            .agg(
                sum("total_amount").alias("total_revenue"),
                count("order_id").alias("total_orders"),
                avg("total_amount").alias("avg_order_value"),
                sum("quantity").alias("total_units_sold")
            )
    )

@dp.table(
    name="gold_sales_by_category",
    comment="Aggregated sales metrics by product category and hour",
    table_properties={"quality": "gold"}
)
def gold_sales_by_category():
    return (
        dp.read_stream("silver_orders")
            .where(col("order_status") == "CONFIRMED")
            .groupBy(
                date_trunc("hour", col("event_timestamp")).alias("event_hour"),
                col("category")
            )
            .agg(
                sum("total_amount").alias("total_revenue"),
                count("order_id").alias("total_orders"),
                avg("total_amount").alias("avg_order_value"),
                sum("quantity").alias("total_units_sold")
            )
    )

@dp.table(
    name="gold_payment_method_summary",
    comment="Order count and revenue breakdown by payment method",
    table_properties={"quality": "gold"}
)
def gold_payment_method_summary():
    return (
        dp.read_stream("silver_orders")
            .where(col("order_status") == "CONFIRMED")
            .groupBy(
                date_trunc("hour", col("event_timestamp")).alias("event_hour"),
                col("payment_method")
            )
            .agg(
                sum("total_amount").alias("total_revenue"),
                count("order_id").alias("total_orders")
            )
    )