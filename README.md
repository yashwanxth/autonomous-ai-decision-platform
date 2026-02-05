# Autonomous AI Decision & Optimization Platform — Notes & README

This file serves as the **primary README-style documentation** for the project, written in a **notes format** that is easy to revise, explain, and use during interviews. You can rename this file to `README.md` if you want to use it as the main repository README.

---

## Overview

A **production-grade, end-to-end Autonomous AI Decision System** that ingests real-time events, builds streaming features, predicts risk, optimizes actions using reinforcement learning, and produces **explainable decisions** with safety rules and real-world feedback loops.

This project mirrors how **real ML platforms** are built in domains like fintech, fraud detection, mobility, and large-scale decision automation.

---

## Why This Project

Most ML projects stop at model training. This system demonstrates how ML works **in production**:

* Streaming ingestion (Kafka)
* Real-time feature stores (Redis)
* Multiple ML paradigms working together
* Decision optimization, not just prediction
* Safety rules and fault tolerance
* Outcome-driven reinforcement learning
* Explainability using a **local LLM**
* APIs, metrics, and observability

This is a **systems-first AI project**, not a notebook demo.

---

## What the System Does

* Ingests real-time events using **Apache Kafka**
* Builds rolling, time-windowed features in **Redis**
* Detects anomalies using **Isolation Forest**
* Predicts risk using **Deep Learning (PyTorch)**
* Chooses optimal actions using **Reinforcement Learning (PPO)**
* Applies **hard safety rules & fallbacks**
* Stores decisions, outcomes, and rewards in **PostgreSQL**
* Learns from real outcomes via an **RL feedback loop**
* Generates human-readable explanations using **Ollama (local LLM)**
* Exposes decisions via **FastAPI**
* Publishes metrics via **Prometheus** and **Grafana**

---

## Decision Codes

| Code | Meaning  |
| ---: | -------- |
|    0 | Allow    |
|    1 | Throttle |
|    2 | Block    |

---

## High-Level Architecture

```
Event → Kafka → Feature Store (Redis)
                     ↓
              Isolation Forest
                     ↓
             Deep Learning Risk Model
                     ↓
           Reinforcement Learning Agent
                     ↓
           Rule Engine + Fallback
                     ↓
              Decision API (FastAPI)
                     ↓
           PostgreSQL (Decisions & Outcomes)
                     ↓
            RL Retraining (Feedback Loop)
                     ↓
        Local LLM Explainability (Ollama)
```

---

## Tech Stack (100% Free & Open Source)

### Infrastructure

* Docker & Docker Compose
* Apache Kafka
* Redis OSS
* PostgreSQL

### ML / AI

* Scikit-learn (Isolation Forest)
* PyTorch (Deep Learning Risk Model)
* Stable-Baselines3 (PPO Reinforcement Learning)
* Ollama + LLaMA 3 (Local LLM Explainability)

### Serving & Observability

* FastAPI
* Prometheus
* Grafana

---

## Repository Structure

```
ai-decision-platform/
│
├── ingestion/
│   └── kafka_consumer/
│       ├── consumer.py
│       └── schemas/
│           └── event.py
│
├── feature_store/
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
│       ├── agent.py
│       └── retrain.py
│
├── decision_engine/
│   ├── decision_logic.py
│   ├── rule_engine.py
│   ├── fallback.py
│   └── test_decision.py
│
├── llm/
│   └── explainability.py
│
├── serving/
│   └── api.py
│
├── observability/
│   ├── prometheus.yml
│   └── grafana-dashboards/
│       └── datasource.yml
│
├── Dockerfile.api
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── NOTES.md
```

---

## Setup & Run (Quick Start)

### Prerequisites

* Python 3.10+
* Docker & Docker Compose

---

### Run Everything (Recommended)

```bash
docker compose up --build
```

This starts:

* Kafka & Zookeeper
* Redis
* PostgreSQL
* FastAPI Decision API
* Prometheus & Grafana

---

## API Endpoints

### Health Check

```
GET /health
```

### Make a Decision

```
POST /decide
{
  "entity_id": "201"
}
```

Response:

```json
{
  "decision_id": 1,
  "entity_id": "201",
  "action": 0,
  "risk": 0.09,
  "explanation": "..."
}
```

### Submit Outcome (RL Feedback)

```
POST /outcome
{
  "decision_id": 1,
  "outcome": "success"
}
```

---

## ML Training (Run Once)

```bash
python ml/baseline_models/isolation_forest.py
python ml/deep_learning/train.py
python ml/reinforcement_learning/agent.py
```

Model artifacts are intentionally **not committed** to keep the repo reproducible.

---

## Reinforcement Learning Notes

* RL optimizes **long-term outcomes**, not single predictions
* Rewards are computed from real-world outcomes
* Retraining happens **offline** for safety

---

## Failure Handling

If any component fails:

* Missing features
* Model load error
* Redis or LLM unavailable

➡️ A **safe fallback decision** is returned.

This is intentional and production-safe.

---

## One-Minute Explanation

> I built an autonomous AI decision platform where events stream through Kafka into a Redis feature store. A deep learning model predicts risk, a PPO reinforcement learning agent selects optimal actions, and hard rules enforce safety. Decisions and outcomes are stored in PostgreSQL, enabling a real feedback loop where the RL agent learns from real-world results. The system is exposed via FastAPI, monitored with Prometheus and Grafana, and every decision is explained using a local LLM.

---