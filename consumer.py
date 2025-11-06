from confluent_kafka import Consumer, TopicPartition
import json

def main():
    """Kafka consumer that reads messages from the orders topic"""
    
    print("Starting Kafka Consumer...")
    
    config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'order_consumer_group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True
    }
    
    consumer = Consumer(config)
    
    # Try consumer group subscription first
    consumer.subscribe(['orders'])
    
    print("Listening for messages...")
    
    message_found = False
    for i in range(10):  # Try for 10 seconds
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
            
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        
        # Success!
        try:
            order = json.loads(msg.value().decode('utf-8'))
            print(f"Received order: {order}")
            print(f"Offset: {msg.offset()}")
            message_found = True
            break
        except Exception as e:
            print(f"Decode error: {e}")
    
    # If subscription doesn't work, try manual assignment
    if not message_found:
        consumer.unsubscribe()
        partition = TopicPartition('orders', 0, 0)
        consumer.assign([partition])
        
        print("Trying manual partition assignment...")
        
        for i in range(5):
            msg = consumer.poll(timeout=2.0)
            
            if msg is None:
                continue
                
            if msg.error():
                print(f"Error: {msg.error()}")
                continue
            
            try:
                order = json.loads(msg.value().decode('utf-8'))
                print(f"Received order: {order}")
                print(f"Offset: {msg.offset()}")
                message_found = True
                break
            except Exception as e:
                print(f"Decode error: {e}")
    
    consumer.close()
    
    if message_found:
        print("Consumer working successfully!")
    else:
        print("No messages received.")

if __name__ == "__main__":
    main()