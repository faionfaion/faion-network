# ci_collector.py — schedule via cron hourly
# Input: watchlist.yaml (competitors with urls and signal types)
# Output: events.ndjson (one JSON event per delta detected)
import json, hashlib, pathlib, datetime, httpx, yaml

WATCH = yaml.safe_load(open("watchlist.yaml"))
STATE = pathlib.Path(".ci_state"); STATE.mkdir(exist_ok=True)
EVENTS = pathlib.Path("events.ndjson")


def fetch(url: str) -> str:
    """Fetch URL via Jina reader for LLM-ready text extraction."""
    r = httpx.get(f"https://r.jina.ai/{url}", timeout=30)
    r.raise_for_status()
    return r.text


def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def emit(event: dict) -> None:
    event["ts"] = datetime.datetime.utcnow().isoformat() + "Z"
    with EVENTS.open("a") as f:
        f.write(json.dumps(event) + "\n")


for competitor in WATCH["competitors"]:
    for url in competitor["urls"]:
        try:
            body = fetch(url)
        except Exception as e:
            emit({"competitor": competitor["name"], "url": url, "error": str(e)})
            continue
        fp_path = STATE / hashlib.md5(url.encode()).hexdigest()
        prev = fp_path.read_text() if fp_path.exists() else ""
        cur = fingerprint(body)
        if cur != prev:
            emit({
                "competitor": competitor["name"],
                "url": url,
                "signal_type": competitor.get("type", "site"),
                "excerpt": body[:2000],
            })
            fp_path.write_text(cur)
