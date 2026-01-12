import requests
from datetime import datetime, timezone

MARKETS_URL = "https://gamma-api.polymarket.com/markets"
ORDERBOOK_URL = "https://clob.polymarket.com/book"


def fetch_markets():
    r = requests.get(MARKETS_URL)
    r.raise_for_status()
    return r.json()


def fetch_orderbook(token_id: str):
    r = requests.get(ORDERBOOK_URL, params={"token_id": token_id})
    r.raise_for_status()
    return r.json()


def best_ask(orderbook: dict):
    asks = orderbook.get("asks", [])
    if not asks:
        return None, None
    return float(asks[0]["price"]), float(asks[0]["size"])


def read_polymarket():
    snapshots = []
    markets = fetch_markets()

    for m in markets:
        if not m.get("active"):
            continue
        if len(m.get("outcomes", [])) != 2:
            continue

        yes_token = m["outcomes"][0]["token_id"]
        no_token = m["outcomes"][1]["token_id"]

        yes_book = fetch_orderbook(yes_token)
        no_book = fetch_orderbook(no_token)

        yes_ask, yes_size = best_ask(yes_book)
        no_ask, no_size = best_ask(no_book)

        if None in (yes_ask, no_ask):
            continue

        snapshots.append({
            "market_id": m["id"],
            "question": m["question"],
            "yes_ask": yes_ask,
            "yes_size": yes_size,
            "no_ask": no_ask,
            "no_size": no_size,
            "end_date": datetime.fromisoformat(m["end_date"]).replace(tzinfo=timezone.utc),
            "resolution": m.get("resolution", "")
        })

    return snapshots
