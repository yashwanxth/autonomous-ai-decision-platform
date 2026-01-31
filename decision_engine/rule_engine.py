def apply_rules(risk: float, action: int):
    # Hard safety rule
    if risk > 0.9:
        return 2  # force block

    return int(action)
