import json
import time
from kafka import KafkaProducer
from generate_events import generate_event
import os
from dotenv import load_dotenv

load_dotenv()

BOOTSTRAP_SERVER = "d8tmi8v73bb9jgbebg00.any.us-east-1.mpx.prd.cloud.redpanda.com:9092"
TOPIC = "retail-orders"
USERNAME = "producer-user"
PASSWORD = os.getenv("REDPANDA_PASSWORD")

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVER,
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-256",
    sasl_plain_username=USERNAME,
    sasl_plain_password=PASSWORD,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

print("Producer started. Sending events to Redpanda...")

try:
    while True:
        event = generate_event()
        future = producer.send(TOPIC, value=event)
        record_metadata = future.get(timeout=10)  # waits for actual confirmation
        producer.flush()
        print(f"Sent to partition {record_metadata.partition} offset {record_metadata.offset} | {event['order_id']} | {event['product_name']}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping producer...")
    producer.flush()
    producer.close()