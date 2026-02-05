def fallback_decision():
    return {
        "entity_id": None,
        "risk": None,
        "action": 1,  # throttle
        "explanation": "Fallback decision applied due to system error."
    }
