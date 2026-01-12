from src.logic.yes_no import compute_raw_total

RESOLUTION_RISK_KEYWORDS = [
    "death",
    "dies",
    "sole discretion",
    "committee",
    "may determine",
    "consensus",
    "unforeseen",
    "dispute",
    "delay",
]


def has_resolution_risk(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in RESOLUTION_RISK_KEYWORDS)


def find_yes_no_arbs(snapshots, config):
    results = []

    threshold = config["strategies"]["yes_no"]["raw_total_threshold"]
    min_liq = config["strategies"]["yes_no"]["min_liquidity"]

    for s in snapshots:
        if s["yes_size"] < min_liq or s["no_size"] < min_liq:
            continue

        raw_total = compute_raw_total(s)
        if raw_total > threshold:
            continue

        results.append({
            **s,
            "raw_total": raw_total,
            "edge": 1.0 - raw_total,
            "resolution_risk": has_resolution_risk(s["resolution"]),
        })

    return results
