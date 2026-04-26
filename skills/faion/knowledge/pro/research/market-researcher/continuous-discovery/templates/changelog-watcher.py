"""
changelog-watcher.py — daily competitor changelog + pricing watcher.
Usage: python changelog-watcher.py
Reads: .aidocs/market-intel/competitor-registry.json
Writes: .aidocs/market-intel/signals.jsonl (append-only)
"""
from hashlib import sha256
from datetime import datetime, timedelta
import json, pathlib

# --- tool stubs (implement with Claude Agent SDK @tool decorator) ---

def fetch_changelog(url: str) -> dict:
    """Fetch changelog page, return {content: str, fetched_at: ISO}."""
    ...

def fetch_pricing(url: str, geos: list[str]) -> list[dict]:
    """Fetch pricing page per geo, return [{geo, content, fetched_at}]."""
    ...

def diff_block(prev: str, curr: str) -> dict:
    """Block-level diff (readability-extracted), return {changed: bool, delta: str}."""
    ...

def append_jsonl(path: str, row: dict) -> None:
    """Atomically append one JSON row to path."""
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(row) + "\n")

# --- watcher loop ---

SIGNALS_PATH = ".aidocs/market-intel/signals.jsonl"
REGISTRY_PATH = ".aidocs/market-intel/competitor-registry.json"
SINCE = (datetime.utcnow() - timedelta(hours=24)).isoformat()

registry = json.loads(pathlib.Path(REGISTRY_PATH).read_text())
for c in registry["competitors"]:
    # Changelog
    cl = fetch_changelog(c["changelog_url"])
    raw_hash = sha256(cl["content"].encode()).hexdigest()
    row = {
        "competitor_id": c["id"],
        "signal_type": "changelog",
        "source_url": c["changelog_url"],
        "fetched_at": cl["fetched_at"],
        "raw_hash": raw_hash,
        "severity": None,  # agent assigns 0-5
        "confidence": None,
        "delta": None,     # agent fills from diff_block
    }
    append_jsonl(SIGNALS_PATH, row)

    # Pricing per geo
    for geo_snap in fetch_pricing(c["pricing_url"], c["geos"]):
        ph = sha256(geo_snap["content"].encode()).hexdigest()
        append_jsonl(SIGNALS_PATH, {
            "competitor_id": c["id"],
            "signal_type": "pricing",
            "source_url": c["pricing_url"],
            "geo": geo_snap["geo"],
            "fetched_at": geo_snap["fetched_at"],
            "raw_hash": ph,
            "severity": None,
            "confidence": None,
            "delta": None,
        })
