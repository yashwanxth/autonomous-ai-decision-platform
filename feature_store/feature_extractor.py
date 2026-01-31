import time
from feature_store.redis_client import get_redis
from feature_store.window_aggregations import prune_old_events

redis = get_redis()

def update_features(entity_id: str, value: float):
    now = time.time()

    events_key = f"events:{entity_id}"
    features_key = f"features:{entity_id}"

    # store raw event
    redis.zadd(events_key, {f"{now}:{value}": now})

    raw_events = [
        (float(m.split(":")[0]), float(m.split(":")[1]))
        for m in redis.zrange(events_key, 0, -1)
    ]

    events_1m = prune_old_events(raw_events, 60)
    events_5m = prune_old_events(raw_events, 300)

    features = {
        "count_1m": len(events_1m),
        "count_5m": len(events_5m),
        "avg_value_1m": (
            sum(v for _, v in events_1m) / len(events_1m)
            if events_1m else 0
        ),
        "last_event_ts": now
    }

    redis.hset(features_key, mapping=features)
