from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, DoubleType, LongType, StructField, StructType

KAFKA_BROKERS = "localhost:29092,localhost:39092,localhost:49092"
SOURCE_TOPIC = "financial_transactions"
AGGREGATES_TOPIC = "transaction_aggregates"
ANOMALIES_TOPIC = "transaction_anomalies"
CHECKPOINT_DIR = "/mnt/spark-checkpoints"
STATES_DIR = "/mnt/spark-state"

sparkSession = (SparkSession.builder
         .appName("FinancialTransactionsProcessor")
         .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0")
         .config("spark.sql.streaming.checkpointLocation", CHECKPOINT_DIR)
         .config("spark.sql.streaming.stateStore.stateStoreDir", STATES_DIR)
         .config("spark.sql.shuffle.partitions", 20)
         ).getOrCreate()

sparkSession.sparkContext.setLogLevel("WARN")

transaction_schema = StructType([
    StructField('transactionId', StringType(), True),
    StructField('userId', StringType(), True),
    StructField('merchantId', StringType(), True),
    StructField('amount', DoubleType(), True),
    StructField('transactionTime', LongType(), True),
    StructField('transactionType', StringType(), True),
    StructField('location', StringType(), True),
    StructField('paymentMethod', StringType(), True),
    StructField('isInternational', StringType(), True),
    StructField('currency', StringType(), True),
])
