"""Fetch account equity + open options positions from Deribit (read-only key)
and write ONLY the derived, publish-safe display figures to
public/options/deribit_snapshot.json.

Credentials are read from a local key file OUTSIDE this repo (path passed as
an argument or via DERIBIT_KEY_FILE env var). The file's contents are never
printed. Only derived numbers are printed/written.

Key file format: two lines, plain text —
    <client_id>
    <client_secret>
"""
import os
import sys
import json
from datetime import datetime, timezone
import requests

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(REPO_ROOT, "public", "options", "deribit_snapshot.json")
BASE = "https://www.deribit.com/api/v2"


def load_credentials(key_file):
    with open(key_file, "r") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]
    if len(lines) < 2:
        raise ValueError("Key file must have two non-empty lines: client_id, then client_secret")
    return lines[0], lines[1]


def authenticate(client_id, client_secret):
    r = requests.get(f"{BASE}/public/auth", params={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }, timeout=15)
    r.raise_for_status()
    result = r.json()["result"]
    return result["access_token"]


def fetch_account_summary(token, currency="BTC"):
    r = requests.get(f"{BASE}/private/get_account_summary", params={
        "currency": currency, "extended": "true",
    }, headers={"Authorization": f"Bearer {token}"}, timeout=15)
    r.raise_for_status()
    return r.json()["result"]


def fetch_positions(token, currency="BTC", kind="option"):
    r = requests.get(f"{BASE}/private/get_positions", params={
        "currency": currency, "kind": kind,
    }, headers={"Authorization": f"Bearer {token}"}, timeout=15)
    r.raise_for_status()
    return r.json()["result"]


def fetch_index_price(currency="BTC"):
    r = requests.get(f"{BASE}/public/get_index_price", params={
        "index_name": f"{currency.lower()}_usd",
    }, timeout=15)
    r.raise_for_status()
    return r.json()["result"]["index_price"]


def build_snapshot(key_file, currency="BTC"):
    client_id, client_secret = load_credentials(key_file)
    token = authenticate(client_id, client_secret)

    summary = fetch_account_summary(token, currency)
    positions = fetch_positions(token, currency, "option")
    index_price = fetch_index_price(currency)

    equity_btc = summary.get("equity", 0.0)
    equity_usd = equity_btc * index_price

    open_positions = [
        {
            "instrument": p["instrument_name"],
            "direction": p["direction"],
            "size": p["size"],
            "mark_price": p.get("mark_price"),
            "unrealized_pnl": p.get("floating_profit_loss"),
        }
        for p in positions
        if p.get("size", 0) != 0
    ]

    snapshot = {
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        "currency": currency,
        "equity_usd": round(equity_usd, 2),
        "equity_btc": round(equity_btc, 4),
        "open_position_count": len(open_positions),
        "open_positions": open_positions,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

    print(f"Snapshot written to {OUT_PATH}")
    print(f"Equity: ${snapshot['equity_usd']:,.2f} ({snapshot['equity_btc']} BTC)")
    print(f"Open positions: {snapshot['open_position_count']}")


if __name__ == "__main__":
    key_file = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("DERIBIT_KEY_FILE")
    if not key_file:
        print("Usage: python deribit_snapshot.py <path-to-key-file>", file=sys.stderr)
        sys.exit(1)
    build_snapshot(key_file)
