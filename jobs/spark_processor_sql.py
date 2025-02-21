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

# Parse JSON and create temporary view
kafka_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), transaction_schema).alias("data")) \
    .select("data.*") \
    .createOrReplaceTempView("raw_transactions")

# Convert timestamp and create another temporary view
sparkSession.sql("""
    CREATE OR REPLACE TEMPORARY VIEW transactions AS
    SELECT
          transactionId,
          userId,
          merchantId,
          amount,
          TIMESTAMP_SECONDS(CAST(transactionTime / 1000 AS LONG)) as transactionTime,
          transactionType,
          location,
          paymentMethod,
          isInternational,
          currency
    FROM raw_transactions
""")

# Create aggregates
aggregates_df = sparkSession.sql("""
    SELECT 
        merchantId,
        SUM(amount) as totalAmount,
        COUNT(*) as transactionCount
    FROM transactions
    GROUP BY merchantId
""")

# Prepare for kafka output
kafka_output = (
    aggregates_df.selectExpr(
        "CAST(merchantId AS STRING) AS key",
        "to_json(struct(merchantId, totalAmount, transactionCount))"
    )
)

aggregate_query = (
    kafka_output
    .writeStream
    .format("kafka")
    .outputMode("update")
    .option("kafka.bootstrap.servers", KAFKA_BROKERS)
    .option("topic", AGGREGATES_TOPIC)
    .option("checkpointLocation", f"{CHECKPOINT_DIR}/aggregates")
)

aggregate_query.start()

sparkSession.streams.awaitAnyTermination()
