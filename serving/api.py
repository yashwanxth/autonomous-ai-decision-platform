from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response
import time
import psycopg2

from decision_engine.decision_logic import decide

app = FastAPI(
    title="Autonomous AI Decision Platform",
    version="1.0.0"
)

# -------- Metrics --------
REQUEST_COUNT = Counter(
    "decision_requests_total",
    "Total number of decision requests"
)

REQUEST_LATENCY = Histogram(
    "decision_request_latency_seconds",
    "Decision request latency"
)

# -------- Schemas --------
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


# -------- Routes --------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/decide", response_model=DecisionResponse)
def decide_entity(req: DecisionRequest):
    REQUEST_COUNT.inc()
    start = time.time()

    try:
        result = decide(req.entity_id)
        return result
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

    try:
        conn = psycopg2.connect(
            host="localhost",
            user="ai",
            password="ai",
            dbname="decision_platform"
        )
        cur = conn.cursor()

        # Fetch action for decision
        cur.execute(
            "SELECT action FROM decisions WHERE id = %s",
            (req.decision_id,)
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Decision not found")

        action_id = row[0]
        action_name = ["allow", "throttle", "block"][action_id]

        reward = reward_map.get(
            (action_name, req.outcome),
            -0.1
        )

        # Store outcome
        cur.execute(
            "INSERT INTO outcomes (decision_id, outcome) VALUES (%s, %s)",
            (req.decision_id, req.outcome)
        )

        # Store reward
        cur.execute(
            "INSERT INTO rewards (decision_id, reward) VALUES (%s, %s)",
            (req.decision_id, reward)
        )

        conn.commit()
        cur.close()
        conn.close()

        return {
            "decision_id": req.decision_id,
            "action": action_name,
            "outcome": req.outcome,
            "reward": reward
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response
import time
import psycopg2

from decision_engine.decision_logic import decide

app = FastAPI(
    title="Autonomous AI Decision Platform",
    version="1.0.0"
)

# -------- Metrics --------
REQUEST_COUNT = Counter(
    "decision_requests_total",
    "Total number of decision requests"
)

REQUEST_LATENCY = Histogram(
    "decision_request_latency_seconds",
    "Decision request latency"
)

# -------- Schemas --------
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


# -------- Routes --------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/decide", response_model=DecisionResponse)
def decide_entity(req: DecisionRequest):
    REQUEST_COUNT.inc()
    start = time.time()

    try:
        result = decide(req.entity_id)
        return result
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

    try:
        conn = psycopg2.connect(
            host="localhost",
            user="ai",
            password="ai",
            dbname="decision_platform"
        )
        cur = conn.cursor()

        # Fetch action for decision
        cur.execute(
            "SELECT action FROM decisions WHERE id = %s",
            (req.decision_id,)
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Decision not found")

        action_id = row[0]
        action_name = ["allow", "throttle", "block"][action_id]

        reward = reward_map.get(
            (action_name, req.outcome),
            -0.1
        )

        # Store outcome
        cur.execute(
            "INSERT INTO outcomes (decision_id, outcome) VALUES (%s, %s)",
            (req.decision_id, req.outcome)
        )

        # Store reward
        cur.execute(
            "INSERT INTO rewards (decision_id, reward) VALUES (%s, %s)",
            (req.decision_id, reward)
        )

        conn.commit()
        cur.close()
        conn.close()

        return {
            "decision_id": req.decision_id,
            "action": action_name,
            "outcome": req.outcome,
            "reward": reward
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )
