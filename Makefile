producer-python:
	python python-producer/main.py

producer-java:
	cd java-producer &&	gradle run

pyspark-consumer:
	docker exec -it spark-master spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 jobs/spark_processor.py

sql-spark-consumer:
	docker exec -it spark-master spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 jobs/spark_processor_sql.py

connect-postgres:
	docker exec -it postgres psql -U postgres -h localhost -d financial_data