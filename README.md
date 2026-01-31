# Autonomous AI Decision & Optimization Platform

A production-style, end-to-end **Autonomous AI Decision System** that ingests real-time events, builds features, predicts risk, optimizes actions using reinforcement learning, and produces final decisions with safety rules.

This project is designed to reflect **senior-level ML systems and MLOps practices** and mirrors real-world production architectures.

---

## 🎯 Why This Project

This project demonstrates how modern AI systems are built **beyond notebooks and toy datasets**:

- Streaming data pipelines
- Real-time feature stores
- Multiple ML paradigms working together
- Decision optimization, not just prediction
- Safety rules, fallbacks, and production mindset

It is intentionally designed as a **systems-first AI project**, not a model-only demo.

---

## 🚀 What This System Does

- Ingests real-time events using **Apache Kafka**
- Builds rolling, time-windowed features in **Redis**
- Detects anomalies using **Isolation Forest**
- Predicts risk using **Deep Learning (PyTorch)**
- Chooses optimal actions using **Reinforcement Learning (PPO)**
- Applies **hard safety rules & fallbacks**
- Outputs a final decision

### Decision Codes

| Code | Meaning   |
|----:|-----------|
| 0   | Allow     |
| 1   | Throttle  |
| 2   | Block     |

---

## 🧠 High-Level Architecture

```
Event → Kafka → Feature Store (Redis)
                     ↓
              Isolation Forest (baseline)
                     ↓
             Deep Learning Risk Model
                     ↓
           Reinforcement Learning Agent
                     ↓
           Rule Engine + Fallback
                     ↓
               Final Decision
```

---

## 🧰 Tech Stack (100% Free)

### Infrastructure

* Docker & Docker Compose
* Apache Kafka
* Redis OSS
* PostgreSQL (planned)

### ML / AI

* Scikit-learn (Isolation Forest)
* PyTorch (Deep Learning)
* Stable-Baselines3 (Reinforcement Learning)

### Serving & Observability (planned)

* FastAPI
* Prometheus
* Grafana

---

## 📁 Repository Structure

```
ai-decision-platform/
│
├── ingestion/
│   └── kafka_consumer/
│       ├── __init__.py
│       ├── consumer.py
│       └── schemas/
│           ├── __init__.py
│           └── event.py
│
├── feature_store/
│   ├── __init__.py
│   ├── redis_client.py
│   ├── window_aggregations.py
│   └── feature_extractor.py
│
├── ml/
│   ├── baseline_models/
│   │   └── isolation_forest.py
│   ├── deep_learning/
│   │   ├── model.py
│   │   ├── train.py
│   │   └── infer.py
│   └── reinforcement_learning/
│       ├── environment.py
│       └── agent.py
│
├── decision-engine/
│   ├── decision_logic.py
│   ├── rule_engine.py
│   ├── fallback.py
│   └── test_decision.py
│
├── docker-compose.yml
├── README.md
└── docs/
```

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites

* Python 3.10+
* Docker & Docker Compose
* Git

Verify:

```bash
docker --version
python --version
```

---

### 2️⃣ Clone & Setup Virtual Environment

```bash
git clone <repo-url>
cd ai-decision-platform
python -m venv .venv
```

Activate:

* **Windows**

```powershell
.\.venv\Scripts\activate
```

* **macOS / Linux**

```bash
source .venv/bin/activate
```

---

### 3️⃣ Install Python Dependencies

```bash
pip install kafka-python redis scikit-learn numpy torch stable-baselines3 gymnasium joblib
```

---

### 4️⃣ Start Infrastructure

```bash
docker compose up -d
```

Services started:

* Kafka
* Zookeeper
* Redis
* PostgreSQL

---

## ▶️ Running the System

### 1️⃣ Start Kafka Consumer

```bash
python -m ingestion.kafka_consumer.consumer
```

---

### 2️⃣ Send Test Events

```bash
docker exec -it <kafka_container> kafka-console-producer \
  --topic events \
  --bootstrap-server localhost:9092
```

Example event:

{
  "event_id": "1",
  "entity_id": "123",
  "event_type": "action",
  "value": 10,
  "timestamp": "2026-01-30T12:00:00Z"
}

---

### 3️⃣ Verify Feature Store

```bash
docker exec -it <redis_container> redis-cli
```

```redis
HGETALL features:123
```

---

### 4️⃣ Train Baseline ML (Isolation Forest)

```bash
python ml/baseline_models/isolation_forest.py
```

---

### 5️⃣ Train Deep Learning Risk Model

```bash
python ml/deep_learning/train.py
```

---

### 6️⃣ Train Reinforcement Learning Agent

```bash
python ml/reinforcement_learning/agent.py
```

---

### 7️⃣ Test Decision Engine

```bash
python decision-engine/test_decision.py
```

Output:

```
0 | 1 | 2
```
