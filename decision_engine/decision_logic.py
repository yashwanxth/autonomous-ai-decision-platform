import numpy as np
from stable_baselines3 import PPO
from ml.deep_learning.infer import predict_risk
from feature_store.redis_client import get_redis
from decision_engine.rule_engine import apply_rules
from decision_engine.fallback import fallback_decision

FEATURE_KEYS = ["count_1m", "count_5m"]

def decide(entity_id: str):
    try:
        r = get_redis()
        features = r.hgetall(f"features:{entity_id}")

        risk = predict_risk(entity_id)

        state = np.array([
            risk,
            float(features["count_1m"]),
            float(features["count_5m"]),
        ], dtype=np.float32)

        model = PPO.load("decision_agent")
        action, _ = model.predict(state)

        final_action = apply_rules(risk, action)
        return final_action

    except Exception:
        return fallback_decision()
