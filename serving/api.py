from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import (
    Counter,
    Histogram,
    CollectorRegistry,
    generate_latest,
)
from starlette.responses import Response
import time
import psycopg2
import os

from decision_engine.decision_logic import decide

# ---------------- App ----------------
app = FastAPI(
    title="Autonomous AI Decision Platform",
    version="1.0.0",
)

# ---------------- Prometheus Registry (IMPORTANT FIX) ----------------
REGISTRY = CollectorRegistry(auto_describe=True)

REQUEST_COUNT = Counter(
    "decision_requests_total",
    "Total number of decision requests",
    registry=REGISTRY,
)

REQUEST_LATENCY = Histogram(
    "decision_request_latency_seconds",
    "Decision request latency",
    registry=REGISTRY,
)

# ---------------- Schemas ----------------
class DecisionRequest(BaseModel):
    entity_id: str


class DecisionResponse(BaseModel):
    entity_id: str | None
    action: int
    risk: float | None
    explanation: str


class OutcomeRequest(BaseModel):
    decision_id: int
    outcome: str  # success | fraud | false_positive


# ---------------- DB Helper ----------------
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        user=os.getenv("POSTGRES_USER", "ai"),
        password=os.getenv("POSTGRES_PASSWORD", "ai"),
        dbname=os.getenv("POSTGRES_DB", "decision_platform"),
    )


# ---------------- Routes ----------------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/decide", response_model=DecisionResponse)
def decide_entity(req: DecisionRequest):
    REQUEST_COUNT.inc()
    start = time.time()

    try:
        return decide(req.entity_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        REQUEST_LATENCY.observe(time.time() - start)


@app.post("/outcome")
def record_outcome(req: OutcomeRequest):
    """
    Records real-world outcome and computes reward for RL feedback
    """

    reward_map = {
        ("allow", "success"): 1,
        ("allow", "fraud"): -5,
        ("block", "fraud"): 2,
        ("block", "success"): -3,
        ("throttle", "success"): -0.1,
        ("throttle", "fraud"): -0.1,
    }

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT action FROM decisions WHERE id = %s",
            (req.decision_id,),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Decision not found")

        action_id = row[0]
        action_name = ["allow", "throttle", "block"][action_id]

        reward = reward_map.get(
            (action_name, req.outcome),
            -0.1,
        )

        cur.execute(
            "INSERT INTO outcomes (decision_id, outcome) VALUES (%s, %s)",
            (req.decision_id, req.outcome),
        )

        cur.execute(
            "INSERT INTO rewards (decision_id, reward) VALUES (%s, %s)",
            (req.decision_id, reward),
        )

        conn.commit()

        return {
            "decision_id": req.decision_id,
            "action": action_name,
            "outcome": req.outcome,
            "reward": reward,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(REGISTRY),
        media_type="text/plain",
    )
