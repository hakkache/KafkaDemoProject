# Kafka Demo Project

A simple Apache Kafka producer-consumer demonstration using Python and Docker.

## 📋 Overview

This project demonstrates basic Kafka messaging patterns with:
- **Producer**: Sends order messages to Kafka topic
- **Consumer**: Receives and processes order messages
- **Kafka**: Single-node Kafka cluster running in Docker

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Producer   │───▶│   Kafka     │───▶│  Consumer   │
│ (producer.py)│    │ (Docker)    │    │(consumer.py)│
└─────────────┘    └─────────────┘    └─────────────┘
```

## 📄 Message Schema

### Order Message Format
```json
{
  "order_id": "string (UUID)",
  "user": "string",
  "item": "string", 
  "quantity": "integer"
}
```

### Example Message
```json
{
  "order_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "user": "HAKKACHE",
  "item": "MONITOR",
  "quantity": 1
}
```

## 📁 Project Structure

```
KafkaDemoProject/
├── producer.py          # Kafka message producer
├── consumer.py          # Kafka message consumer
├── docker-compose.yml   # Kafka cluster configuration
├── requirements.txt     # Python dependencies
├── kafka-data/          # Kafka data directory (auto-created)
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Docker & Docker Compose
- pip (Python package manager)

### 1. Setup Environment

```bash
# Clone or navigate to project directory
cd KafkaDemoProject

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Kafka

```bash
# Start Kafka container
docker-compose up -d

# Verify Kafka is running
docker ps
```

### 3. Create Kafka Topic

```bash
# Create 'orders' topic
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --create --topic orders --partitions 1 --replication-factor 1

# Verify topic creation
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list
```

### 4. Run Producer & Consumer

```bash
# Terminal 1 - Start Consumer
python consumer.py

# Terminal 2 - Send Messages
python producer.py
```

## 📝 Script Explanations

### 🏭 Producer Script (`producer.py`)

**Purpose**: Sends order messages to the Kafka `orders` topic.

**Key Components**:
- **Configuration**: Connects to Kafka broker at `localhost:9092`
- **Message Creation**: Generates order with UUID, user, item, and quantity
- **Delivery Callback**: Confirms successful message delivery
- **Error Handling**: Reports delivery failures

**Message Flow**:
1. Creates order object with random UUID
2. Serializes to JSON and encodes as UTF-8
3. Sends to `orders` topic
4. Waits for delivery confirmation
5. Reports success/failure

**Example Output**:
```
Message delivered: {"order_id": "abc123...", "user": "HAKKACHE", "item": "MONITOR", "quantity": 1}
Topic: orders, Partition: 0, Offset: 42
Producer finished sending message
```

### 🏭 Consumer Script (`consumer.py`)

**Purpose**: Receives and processes messages from the Kafka `orders` topic.

**Key Components**:
- **Dual Strategy**: Consumer group subscription + manual partition assignment
- **Configuration**: Reads from earliest available messages
- **Auto-commit**: Automatically commits message offsets
- **Error Handling**: Graceful handling of connection and parsing errors

**Message Flow**:
1. **Strategy 1**: Try consumer group subscription (10 attempts)
2. **Strategy 2**: Fall back to manual partition assignment (5 attempts)
3. Parse JSON messages and display order details
4. Report success or failure

**Example Output**:
```
Starting Kafka Consumer...
Listening for messages...
Trying manual partition assignment...
Received order: {'order_id': 'abc123...', 'user': 'HAKKACHE', 'item': 'MONITOR', 'quantity': 1}
Offset: 42
Consumer working successfully!
```

### 🐳 Docker Configuration (`docker-compose.yml`)

**Purpose**: Single-node Kafka cluster with KRaft mode (no Zookeeper required).

**Key Settings**:
- **KRaft Mode**: Modern Kafka without Zookeeper dependency
- **Ports**: 9092 (client), 9093 (controller)
- **Persistence**: Data stored in `./kafka-data/` directory
- **Single Broker**: Replication factor of 1 for development

## ⚙️ Configuration Details

### Kafka Broker Configuration
- **Bootstrap Server**: `localhost:9092`
- **Topic**: `orders`
- **Partitions**: 1
- **Replication Factor**: 1

### Producer Configuration
```python
producer_config = {
    'bootstrap.servers': 'localhost:9092'
}
```

### Consumer Configuration
```python
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'order_consumer_group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True
}
```

## 🔧 Troubleshooting

### Common Issues

1. **Kafka Not Started**
   ```bash
   # Check if Kafka container is running
   docker ps
   
   # Start Kafka if not running
   docker-compose up -d
   ```

2. **Topic Doesn't Exist**
   ```bash
   # Create the orders topic
   docker exec kafka kafka-topics --bootstrap-server localhost:9092 --create --topic orders --partitions 1 --replication-factor 1
   ```

3. **Consumer Not Receiving Messages**
   - Ensure Kafka is running
   - Check if topic exists
   - The consumer uses dual strategy (subscription + manual assignment)

4. **Port Conflicts**
   - Ensure ports 9092 and 9093 are available
   - Stop other Kafka instances

### Verification Commands

```bash
# List topics
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list

# Check topic details
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic orders

# View messages in topic
docker exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic orders --from-beginning
```

## 🧪 Testing

### Manual Testing Flow
1. Start Kafka: `docker-compose up -d`
2. Create topic (if needed)
3. Start consumer: `python consumer.py`
4. Send message: `python producer.py`
5. Verify consumer receives message

### Expected Behavior
- Producer should show delivery confirmation
- Consumer should display received order details
- Both should complete without errors

## 🛠️ Development

### Adding Features
- **Message Validation**: Add schema validation with JSON Schema
- **Error Handling**: Implement retry mechanisms
- **Monitoring**: Add metrics and logging
- **Serialization**: Use Avro or Protobuf for better schema evolution

### Scaling Considerations
- Increase partitions for parallel processing
- Add multiple consumer instances
- Implement proper error handling and dead letter queues

## 📚 References

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Confluent Kafka Python Client](https://github.com/confluentinc/confluent-kafka-python)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 📄 License

This project is for demonstration purposes.