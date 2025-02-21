from pyspark.sql.functions import *

from jobs.spark_setup import KAFKA_BROKERS, SOURCE_TOPIC, transaction_schema, AGGREGATES_TOPIC, CHECKPOINT_DIR, \
    sparkSession

# Read from Kafka
kafka_stream = (sparkSession.readStream
                .format("kafka")
                .option('kafka.bootstrap.servers', KAFKA_BROKERS)
                .option('subscribe', SOURCE_TOPIC)
                .option('startingOffsets', 'latest')
                .option('failOnDataLoss', 'false')
                ).load()

transactions_df = (
    kafka_stream
    .selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), transaction_schema).alias("data"))
    .select("data.*")
)

transactions_df = (
    transactions_df.withColumn("transactionTime",
                               (col("transactionTime") / 1000).cast("timestamp"))
)

aggregate_df = (
    transactions_df.groupby("merchantId")
    .agg(
        sum("amount").alias("totalAmount"),
        count("*").alias("transactionCount")
    )
)

output_kafka = (
    aggregate_df.withColumn("key", col("merchantId").cast("string"))
    .withColumn("value", to_json(
        struct(
            col("merchantId"),
            col("totalAmount"),
            col("transactionCount")
        )
    ))
    .selectExpr("key", "value")
)

aggregates_query = (
    output_kafka
    .writeStream.format("kafka")
    .outputMode("update")
    .option("kafka.bootstrap.servers", KAFKA_BROKERS)
    .option("topic", AGGREGATES_TOPIC)
    .option("checkpointLocation", f"{CHECKPOINT_DIR}/aggregates")
)

aggregates_query.start().awaitTermination()
