import gymnasium as gym
from gymnasium import spaces
import numpy as np

class DecisionEnv(gym.Env):
    """
    State:
      [risk_score, count_1m, count_5m]
    Actions:
      0 = allow
      1 = throttle
      2 = block
    """
    def __init__(self):
        super().__init__()
        self.observation_space = spaces.Box(
            low=0.0, high=1e6, shape=(3,), dtype=np.float32
        )
        self.action_space = spaces.Discrete(3)
        self.state = None

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.state = np.zeros(3, dtype=np.float32)
        return self.state, {}

    def step(self, action):
        risk, c1m, c5m = self.state

        # Simulated outcome (placeholder, will be replaced later)
        is_risky = risk > 0.6

        reward = self._reward(action, is_risky)

        terminated = True
        truncated = False
        info = {"is_risky": is_risky}

        return self.state, reward, terminated, truncated, info

    def _reward(self, action, is_risky):
        # Correct decisions
        if is_risky and action == 2:
            return +2.0
        if not is_risky and action == 0:
            return +1.0

        # False positives / negatives
        if not is_risky and action == 2:
            return -3.0
        if is_risky and action == 0:
            return -5.0

        # Throttle is neutral
        return -0.1
