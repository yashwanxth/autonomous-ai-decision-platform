# Autonomous AI Decision & Optimization Platform

A production-style, end-to-end **Autonomous AI Decision System** that ingests real-time events, builds features, predicts risk, optimizes actions using reinforcement learning, and produces final decisions with safety rules.

This project is designed at **senior ML systems / MLOps level** and mirrors real-world architectures.

---

## 🚀 What This System Does

* Ingests real-time events using **Apache Kafka**
* Builds rolling, time-windowed features in **Redis**
* Detects anomalies using **Isolation Forest**
* Predicts risk using **Deep Learning (PyTorch)**
* Chooses optimal actions using **Reinforcement Learning (PPO)**
* Applies **hard safety rules & fallbacks**
* Outputs a final decision:

  * `0 = Allow`
  * `1 = Throttle`
  * `2 = Block`

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

```json
{"event_id":"1","entity_id":"123","event_type":"action","value":10,"timestamp":"2026-01-30T12:00:00Z"}
```

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

---

## 🧪 Current Status

✅ Kafka ingestion working
✅ Redis feature store working
✅ Isolation Forest trained
✅ Risk prediction model trained
✅ RL agent trained
✅ Decision engine producing actions

---

## 🛣️ Roadmap

* FastAPI serving layer
* PostgreSQL outcome storage
* Online RL feedback loop
* LLM explainability (Ollama)
* Metrics & dashboards

---

## 🧠 Design Principles

* Fail fast on bad data
* ML is never blindly trusted
* Rules override learning
* Clear separation of concerns
* Production-first mindset

---

## 📌 How to Resume Work

If project context is lost, paste:

> **End-to-End Project Context document**

and say:

> **Continue from last completed phase**

---

## 📄 License

MIT (or add later)
