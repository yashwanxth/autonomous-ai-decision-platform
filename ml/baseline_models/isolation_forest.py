import numpy as np
from redis import Redis
from sklearn.ensemble import IsolationForest
import joblib

REDIS_HOST = "localhost"
REDIS_PORT = 6379

FEATURE_KEYS = [
    "count_1m",
    "count_5m",
    "avg_value_1m",
]

def get_redis():
    return Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def load_feature_matrix():
    r = get_redis()
    X = []

    for key in r.scan_iter(match="features:*"):
        features = r.hgetall(key)
        try:
            row = [float(features[k]) for k in FEATURE_KEYS]
            X.append(row)
        except KeyError:
            continue

    return np.array(X)
import numpy as np
from redis import Redis
from sklearn.ensemble import IsolationForest
import joblib

REDIS_HOST = "localhost"
REDIS_PORT = 6379

FEATURE_KEYS = [
    "count_1m",
    "count_5m",
    "avg_value_1m",
]

def get_redis():
    return Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def load_feature_matrix():
    r = get_redis()
    X = []

    for key in r.scan_iter(match="features:*"):
        features = r.hgetall(key)
        try:
            row = [float(features[k]) for k in FEATURE_KEYS]
            X.append(row)
        except KeyError:
            continue

    return np.array(X)



def train_model():
    X = load_feature_matrix()

    if len(X) < 10:
        raise RuntimeError("Not enough data to train Isolation Forest")

    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42
    )

    model.fit(X)
    joblib.dump(model, "isolation_forest.joblib")
    print("Isolation Forest trained and saved.")

if __name__ == "__main__":
    train_model()
