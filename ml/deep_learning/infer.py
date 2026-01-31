import torch
from redis import Redis
from ml.deep_learning.model import RiskMLP

FEATURE_KEYS = ["count_1m", "count_5m", "avg_value_1m"]

def get_redis():
    return Redis(host="localhost", port=6379, decode_responses=True)

def predict_risk(entity_id: str):
    r = get_redis()
    features = r.hgetall(f"features:{entity_id}")

    x = torch.tensor(
        [[float(features[k]) for k in FEATURE_KEYS]],
        dtype=torch.float32
    )

    model = RiskMLP()
    model.load_state_dict(torch.load("risk_mlp.pt"))
    model.eval()

    with torch.no_grad():
        risk = model(x).item()

    return risk

if __name__ == "__main__":
    print(predict_risk("201"))
