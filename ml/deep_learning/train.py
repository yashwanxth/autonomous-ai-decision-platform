import numpy as np
import torch
import joblib
from redis import Redis
from ml.deep_learning.model import RiskMLP

FEATURE_KEYS = ["count_1m", "count_5m", "avg_value_1m"]

def get_redis():
    return Redis(host="localhost", port=6379, decode_responses=True)

def load_data():
    r = get_redis()
    X, y = [], []

    iso = joblib.load("isolation_forest.joblib")

    for key in r.scan_iter(match="features:*"):
        features = r.hgetall(key)
        try:
            row = np.array([[float(features[k]) for k in FEATURE_KEYS]])
            score = iso.predict(row)[0]
            label = 1.0 if score == -1 else 0.0

            X.append(row[0])
            y.append(label)
        except KeyError:
            continue

    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32).unsqueeze(1)

def train():
    X, y = load_data()

    model = RiskMLP()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = torch.nn.BCELoss()

    for epoch in range(100):
        optimizer.zero_grad()
        preds = model(X)
        loss = loss_fn(preds, y)
        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            print(f"Epoch {epoch} Loss {loss.item():.4f}")

    torch.save(model.state_dict(), "risk_mlp.pt")
    print("Risk model trained and saved.")

if __name__ == "__main__":
    train()
