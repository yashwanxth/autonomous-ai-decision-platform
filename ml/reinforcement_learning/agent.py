from stable_baselines3 import PPO
from ml.reinforcement_learning.environment import DecisionEnv

def train_agent():
    env = DecisionEnv()

    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        n_steps=128,
        batch_size=64,
        gamma=0.99,
    )

    model.learn(total_timesteps=10_000)
    model.save("decision_agent")

    print("RL agent trained and saved.")

if __name__ == "__main__":
    train_agent()


def test_agent():
    from stable_baselines3 import PPO
    import numpy as np

    model = PPO.load("decision_agent")
    state = np.array([0.8, 5, 10], dtype=np.float32)

    action, _ = model.predict(state)
    print("Action:", action)

# test_agent()
