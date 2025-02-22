from pyspark.sql import DataFrame
import psycopg2

def create_table_if_not_exists(table_name: str):
    conn = psycopg2.connect(
        dbname="financial_data",
        user="user",
        password="password",
        host="postgres",
        port="5432"
    )
    cursor = conn.cursor()
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        merchantId VARCHAR(255),
        totalAmount DOUBLE PRECISION,
        transactionCount BIGINT
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

def write_to_postgres(df: DataFrame, table_name: str):
    create_table_if_not_exists(table_name)
    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/financial_data") \
        .option("dbtable", table_name) \
        .option("user", "user") \
        .option("password", "password") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
