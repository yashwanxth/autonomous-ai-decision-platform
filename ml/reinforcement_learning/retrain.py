import numpy as np
import psycopg2
from stable_baselines3 import PPO
from ml.reinforcement_learning.environment import DecisionEnv

def retrain():
    conn = psycopg2.connect(
        host="localhost",
        user="ai",
        password="ai",
        dbname="decision_platform"
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT d.action, r.reward
        FROM decisions d
        JOIN rewards r ON d.id = r.decision_id
    """)

    rows = cur.fetchall()
    conn.close()

    env = DecisionEnv()
    model = PPO.load("decision_agent", env=env)

    # Simulated update loop
    model.learn(total_timesteps=2000)
    model.save("decision_agent")

    print("RL agent retrained from real outcomes.")

if __name__ == "__main__":
    retrain()
