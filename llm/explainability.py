import subprocess

def explain_decision(entity_id, risk, action, features):
    """
    Uses local Ollama (llama3) to explain a decision.
    """

    prompt = f"""
You are an AI decision auditor.

Entity ID: {entity_id}

Features:
- count_1m: {features['count_1m']}
- count_5m: {features['count_5m']}
- avg_value_1m: {features['avg_value_1m']}

Predicted Risk Score: {risk}

Action taken:
0 = allow
1 = throttle
2 = block

Explain:
1. Why this action was selected
2. Whether the decision is conservative or aggressive
3. Any potential risks or tradeoffs
"""

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()
