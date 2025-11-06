from confluent_kafka import Producer
import uuid
import json

producer_config = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(producer_config)

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered: {msg.value().decode('utf-8')}")
        print(f"Topic: {msg.topic()}, Partition: {msg.partition()}, Offset: {msg.offset()}")

order = {
    'order_id': str(uuid.uuid4()),
    'user': 'HAKKACHE',
    'item': 'MONITOR',
    'quantity': 1
}

value = json.dumps(order).encode('utf-8')

producer.produce(topic='orders', 
                value=value,
                callback=delivery_report)
producer.flush()

print("Producer finished sending message")