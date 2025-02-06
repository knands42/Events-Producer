import json
import logging
import random
import multiprocessing
import time
import uuid

from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

KAFKA_BROKERS = "localhost:29092,localhost:39092,localhost:49092"
NUM_PARTITIONS = 5
REPLICATION_FACTOR = 3
TOPIC_NAME = 'financial_transactions'

logging.basicConfig(
    level=logging.INFO
)
logger = logging.getLogger(__name__)

producer_conf = {
    'bootstrap.servers': KAFKA_BROKERS,
    'queue.buffering.max.messages': 100000,
    'queue.buffering.max.kbytes': 512000,
    'batch.num.messages': 1000,
    'linger.ms': 50, # May delay throughput
    'acks': 1,
    # 'compression_type': 'gzip',
}

producer = Producer(producer_conf)


def create_topic(topic_name):
    admin_client = AdminClient({"bootstrap.servers": KAFKA_BROKERS})

    try:
        metadata = admin_client.list_topics(timeout=10)
        if topic_name not in metadata.topics:
            topic = NewTopic(
                topic=topic_name,
                num_partitions=NUM_PARTITIONS,
                replication_factor=REPLICATION_FACTOR,
            )

            fs = admin_client.create_topics([topic])
            for topic, future in fs.items():
                try:
                    future.result()
                    logger.info(f"Topic '{topic_name}' created successfully!")
                except Exception as e:
                    logger.error(f"Failed to create topic '{topic_name}': {e}")
        else:
            logger.info(f"Topic '{topic_name}' already exists!")
    except Exception as e:
        logger.error(f"Error creating topic: {e}")


def generate_transaction():
    return dict(
        transactionId=str(uuid.uuid4()),
        userId=f"user_{random.randint(1, 100)}",
        amount=round(random.uniform(50000, 150000)),
        transactionTime=int(time.time()),
        merchantId=random.choice(['merchant_1', 'merchant_2', 'merchant_3']),
        transactionType=random.choice(['purchase', 'refund']),
        location=f'location_{random.randint(1, 50)}',
        paymentMethod=random.choice(['credit_card', 'paypal', 'bank_transfer']),
        isInternational=random.choice(['True', 'False']),
        currency=random.choice(['USD', 'EUR', 'GBP'])
    )


def delivery_report(err, message):
    if err is not None:
        logger.error(f'Delivery failed for record {message.key()}')
    else:
        logger.info(f"Record {message.key()} successfully produced")


def produce_transaction(process_id):
    # Create a new producer instance for each process
    local_producer = Producer(producer_conf)
    
    start_time = time.time()
    records_sent = 0
    
    while True:
        transaction = generate_transaction()

        try:
            local_producer.produce(
                topic=TOPIC_NAME,
                key=transaction['userId'],
                value=json.dumps(transaction).encode('utf-8'),
                on_delivery=delivery_report
            )
            records_sent += 1
            
            # Calculate throughput every second
            elapsed_time = time.time() - start_time
            if elapsed_time >= 1:
                throughput = records_sent / elapsed_time
                logger.info(f"Process {process_id} - Throughput: {throughput:.2f} records/sec")
                records_sent = 0
                start_time = time.time()
                
            local_producer.flush()
        except Exception as e:
            logger.error(f"Error sending transaction: {e}")


def producer_data_in_parallel(num_processes):
    processes = []

    try:
        for i in range(num_processes):
            process = multiprocessing.Process(target=produce_transaction, args=(i,))
            process.daemon = True
            process.start()
            processes.append(process)

        # Keep the main process running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down producers...")
        for process in processes:
            process.terminate()
            process.join()
    except Exception as e:
        logger.error(f'Error message: {e}')


if __name__ == '__main__':
    # This guard is required for multiprocessing on Windows
    create_topic(TOPIC_NAME)
    producer_data_in_parallel(3)
