# Kafka Event Producer Template

A high-performance, plug-and-play Kafka event producer template designed to generate and stream large volumes of events to Kafka topics. This template provides a ready-to-use solution for applications that need to test or demonstrate Kafka event streaming at scale.

## 🚀 Features

-   **High Throughput**: Configured to handle high-volume event streaming
-   **Easy Configuration**: Simple setup with Docker Compose
-   **Monitoring**: Built-in monitoring with Prometheus and Grafana
-   **Scalable**: Designed to be easily extended for custom event schemas and patterns

## 🛠️ Quick Start

1. **Clone the repository**

    ```sh
    git clone https://github.com/yourusername/events-producer-template.git
    cd events-producer-template
    ```

2. **Start the infrastructure**

    ```sh
    docker compose up -d
    ```

3. **Run a producer**
    ```sh
    make producer-java
    ```

## 📊 Monitoring

Access the following services (when running locally):

| Service    | URL                                            | Credentials |
| ---------- | ---------------------------------------------- | ----------- |
| Kafka UI   | [http://localhost:8080](http://localhost:8080) | -           |
| Grafana    | [http://localhost:3000](http://localhost:3000) | admin/admin |
| Prometheus | [http://localhost:9090](http://localhost:9090) | -           |


---

Inspired by [1 Billion Records per Hour](https://www.youtube.com/watch?v=d6AFh31fO7Y) tutorial
