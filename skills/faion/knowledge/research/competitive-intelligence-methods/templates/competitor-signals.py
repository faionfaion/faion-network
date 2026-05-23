"""
competitor-signals.py — minimal multi-source per-competitor signal collector.
Usage: python competitor-signals.py <name> <domain>
Outputs JSON with signals from HN, GitHub, ProductHunt, Wayback Machine.
"""
import json, sys, datetime as dt, requests
from urllib.parse import quote_plus


def hn(name: str) -> dict:
    r = requests.get(
        "https://hn.algolia.com/api/v1/search",
        params={"query": name, "tags": "story"},
        timeout=15,
    ).json()
    return {"source": "hacker_news", "hn_hits": r.get("nbHits", 0)}


def gh(name: str) -> dict:
    r = requests.get(
        "https://api.github.com/search/repositories",
        params={"q": name, "sort": "stars"},
        timeout=15,
    ).json()
    items = r.get("items") or []
    return {
        "source": "github",
        "gh_top_stars": items[0]["stargazers_count"] if items else 0,
        "gh_top_url": items[0]["html_url"] if items else "",
    }


def ph(name: str) -> dict:
    return {
        "source": "product_hunt",
        "ph_search_url": f"https://www.producthunt.com/search?q={quote_plus(name)}",
    }


def wayback(domain: str) -> dict:
    r = requests.get(
        f"http://archive.org/wayback/available?url={domain}/pricing",
        timeout=15,
    ).json()
    snap = (r.get("archived_snapshots") or {}).get("closest", {})
    return {
        "source": "wayback",
        "wayback_pricing_url": snap.get("url", ""),
        "wayback_timestamp": snap.get("timestamp", ""),
    }


def collect(name: str, domain: str) -> dict:
    return {
        "competitor": name,
        "domain": domain,
        "ts": dt.datetime.utcnow().isoformat(),
        "signals": [hn(name), gh(name), ph(name), wayback(domain)],
    }


if __name__ == "__main__":
    print(json.dumps(collect(sys.argv[1], sys.argv[2]), indent=2))
