def compute_raw_total(snapshot: dict) -> float:
    return snapshot["yes_ask"] + snapshot["no_ask"]
