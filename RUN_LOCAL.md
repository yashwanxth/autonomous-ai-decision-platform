# Autonomous AI Decision Platform – Local Run Guide

This document provides **step-by-step instructions** to run the project locally, including **exact terminal commands**, **service verification**, and **all supported input data formats** that can be used to trigger decisions.

---

## 1. Prerequisites (MANDATORY)

Ensure the following are installed **before proceeding**:

### System Requirements
- OS: Windows (WSL2 recommended), macOS, or Linux
- RAM: Minimum **8 GB** (16 GB recommended)
- Disk: At least **10 GB free**

### Software
| Tool | Required Version | Check Command |
|---|---|---|
| Docker | >= 24.x | `docker --version` |
| Docker Compose | >= v2 | `docker compose version` |
| Python | 3.11 or 3.12 | `python --version` |
| Git | Latest | `git --version` |

---

## 2. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd ai-decision-platform
```

Project root should contain:
- `docker-compose.yml`
- `decision_engine/`
- `feature_store/`
- `ml/`
- `api.py` (or `main.py`)

---

## 3. Environment Variables

Create a `.env` file in the project root:

```env
POSTGRES_HOST=postgres
POSTGRES_DB=decision_platform
POSTGRES_USER=ai
POSTGRES_PASSWORD=ai

REDIS_HOST=redis
REDIS_PORT=6379

KAFKA_BOOTSTRAP_SERVERS=kafka:9092
```

---

## 4. Start Infrastructure (Docker)

### Build Containers
```bash
docker compose build
```

### Start Services
```bash
docker compose up -d
```

### Verify Containers
```bash
docker compose ps
```

You should see:
- decision-api (running)
- postgres
- redis
- kafka
- zookeeper
- prometheus
- grafana

---

## 5. Database Setup

### Enter Postgres Container
```bash
docker exec -it postgres psql -U ai -d decision_platform
```

### Create Tables
```sql
CREATE TABLE decisions (
  id SERIAL PRIMARY KEY,
  entity_id TEXT,
  action INT,
  risk FLOAT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE outcomes (
  id SERIAL PRIMARY KEY,
  decision_id INT REFERENCES decisions(id),
  outcome TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE rewards (
  id SERIAL PRIMARY KEY,
  decision_id INT REFERENCES decisions(id),
  reward FLOAT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

Exit:
```sql
\q
```

---

## 6. Populate Feature Store (REDIS)

### Enter Redis Container
```bash
docker exec -it redis redis-cli
```

### Add Entity Features

```bash
HSET features:201 \
  count_1m 10 \
  count_5m 25 \
  avg_value_1m 200
```

Exit:
```bash
exit
```

---

## 7. Send Events via Kafka (Optional)

```bash
docker exec -it kafka kafka-console-producer \
  --topic events \
  --bootstrap-server kafka:9092
```

Example messages:
```json
{"event_id":"1","entity_id":"201","event_type":"action","value":100,"timestamp":"2026-01-30T12:00:00Z"}
{"event_id":"2","entity_id":"201","event_type":"action","value":300,"timestamp":"2026-01-30T12:00:10Z"}
```

---

## 8. Call Decision API

### Health Check
```bash
curl http://localhost:8000/health
```

### Make a Decision
```bash
curl -X POST http://localhost:8000/decide \
  -H "Content-Type: application/json" \
  -d '{"entity_id":"201"}'
```

### Example Response
```json
{
  "entity_id": "201",
  "action": 0,
  "risk": 0.12,
  "explanation": "Low risk entity. Allow action chosen."
}
```

---

## 9. Supported Decision Inputs (IMPORTANT)

The model can make decisions based on the following **data types**:

### 1. Redis Feature Store (Primary)
| Feature | Description |
|---|---|
| count_1m | Number of actions in last 1 min |
| count_5m | Number of actions in last 5 min |
| avg_value_1m | Avg transaction value |

### 2. Deep Learning Model Input
- Normalized feature vector
- Risk score ∈ [0, 1]

### 3. Reinforcement Learning State
```text
[risk, count_1m, count_5m]
```

### 4. Rule Engine Overrides
- High risk → force block
- Medium risk → throttle
- Low risk → allow

### 5. Fallback
Triggered when:
- Redis data missing
- Model unavailable
- Exception occurs

---

## 10. Record Outcome (RL Feedback Loop)

```bash
curl -X POST http://localhost:8000/outcome \
  -H "Content-Type: application/json" \
  -d '{"decision_id":1,"outcome":"fraud"}'
```

### Reward Mapping
| Action | Outcome | Reward |
|---|---|---|
| allow | success | +1 |
| allow | fraud | -5 |
| block | fraud | +2 |
| block | success | -3 |
| throttle | any | -0.1 |

---

## 11. Metrics & Monitoring

### Prometheus
```bash
http://localhost:9090
```

### Grafana
```bash
http://localhost:3000
```
Default credentials:
- user: admin
- password: admin

---

## 12. Stopping the Project

```bash
docker compose down
```

---

## 13. Common Failures & Fixes

### decision-api exits immediately
- Check duplicate Prometheus metrics
- Ensure Postgres host is `postgres`, not `localhost`

### Empty decision output
- Redis feature missing
- PPO model file missing

---

## 14. You Are Done

At this point:
- Decisions are served via FastAPI
- Metrics are exported
- RL feedback loop is active
- System is production-structured

---

END OF DOCUMENT

