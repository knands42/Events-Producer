# DataEngineering-1Billion-Rows-Per-Hour

A project that simulates how to build a complete workflow to persist 1 billion rows per hour.

## Project Overview

This project is designed for learning purposes and involves the following components:
- A Python producer sending data to Kafka
- A Java producer sending data to Kafka
- Data being consumed by Apache Spark

## Steps Involved

1. **Python Producer**: Generates and sends data to a Kafka topic.
2. **Java Producer**: Generates and sends data to a Kafka topic.
3. **Kafka**: Acts as the message broker to handle the data streams.
4. **Apache Spark**: Consumes data from Kafka, processes it, and persists it.

## How to Execute the Project

1. **Boot the project**:
   ```sh
   docker compose up --build --force-recreate
   ```

2. **Run the Python Producer**:
    ```sh
    make producer-python
    ```

3. **Run the Java Producer**:
    ```sh
    make producer-java
    ```

4. **Run PySpark Consumer**:
    ```sh
    make pyspark-consumer
    ```

## Useful Links

- [Kafka Topics](http://localhost:8080)
- [Spark Jobs](http://localhost:4040)
- [Grafana](http://localhost:3000)
- [Prometheus](https://localhost:9090)

## Credits

Tutorial made possible by following [1 Billion Records per Hour](https://www.youtube.com/watch?v=d6AFh31fO7Y&t=3s) Youtube channel