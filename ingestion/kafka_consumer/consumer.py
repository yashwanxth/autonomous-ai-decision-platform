import json
from kafka import KafkaConsumer
from ingestion.kafka_consumer.schemas.event import Event
from feature_store.feature_extractor import update_features


def safe_json_deserializer(v):
    try:
        if not v:
            return None
        return json.loads(v.decode("utf-8"))
    except Exception:
        return None


consumer = KafkaConsumer(
    "events",
    bootstrap_servers="localhost:9092",
    value_deserializer=safe_json_deserializer,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
)

print("Kafka consumer started...")

for message in consumer:
    if message.value is None:
        continue

    try:
        event = Event(**message.value)
        update_features(
            entity_id=event.entity_id,
            value=event.value
        )
        print(f"Processed event {event.event_id}")
    except Exception as e:
        print("Error processing event:", e)
