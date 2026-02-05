import numpy as np
import psycopg2
from stable_baselines3 import PPO

from ml.deep_learning.infer import predict_risk
from feature_store.redis_client import get_redis
from decision_engine.rule_engine import apply_rules
from decision_engine.fallback import fallback_decision
from llm.explainability import explain_decision

# ✅ Load RL model ONCE
RL_MODEL = PPO.load("decision_agent")


def decide(entity_id: str):
    try:
        r = get_redis()
        features = r.hgetall(f"features:{entity_id}")

        # Safety check
        if not features:
            return fallback_decision()

        # 1. Risk prediction
        risk = predict_risk(entity_id)

        # 2. Build RL state
        state = np.array(
            [
                risk,
                float(features["count_1m"]),
                float(features["count_5m"]),
            ],
            dtype=np.float32
        )

        # 3. RL action
        action, _ = RL_MODEL.predict(state)

        # 4. Apply rules
        final_action = apply_rules(risk, action)

        # 5. Persist decision
        decision_id = save_decision(entity_id, final_action, risk)

        # 6. LLM explanation
        explanation = explain_decision(
            entity_id=entity_id,
            risk=risk,
            action=final_action,
            features={
                "count_1m": features["count_1m"],
                "count_5m": features["count_5m"],
                "avg_value_1m": features.get("avg_value_1m", 0),
            }
        )

        return {
            "decision_id": decision_id,
            "entity_id": entity_id,
            "risk": risk,
            "action": int(final_action),
            "explanation": explanation,
        }

    except Exception as e:
        print("Decision engine error:", e)
        return fallback_decision()


def save_decision(entity_id, action, risk):
    conn = psycopg2.connect(
        host="localhost",
        user="ai",
        password="ai",
        dbname="decision_platform",
    )
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO decisions (entity_id, action, risk)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (entity_id, action, risk),
    )

    decision_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return decision_id
