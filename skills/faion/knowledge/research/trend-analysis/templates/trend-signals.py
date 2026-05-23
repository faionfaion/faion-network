# purpose: Pull + normalize the 5 signal classes; emit JSON
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1500 tokens when loaded as context
# trend_signals.py — minimal multi-source trend collector
# Input: trend term as CLI argument
# Output: JSON with signals from Google Trends, HN Algolia, GitHub
# Usage: python trend_signals.py "AI agents"
import json, datetime as dt, sys
from pytrends.request import TrendReq
import requests


def google_trends(term: str) -> dict:
    p = TrendReq()
    p.build_payload([term], timeframe="today 12-m")
    df = p.interest_over_time()
    if df.empty:
        return {"yoy_pct": None, "last": None, "source": "google_trends"}
    last, first = df[term].iloc[-1], df[term].iloc[0]
    yoy = None if first == 0 else round((last - first) / first * 100, 1)
    return {"yoy_pct": yoy, "last": int(last), "source": "google_trends"}


def hn_hits(term: str) -> dict:
    since = int(dt.datetime.now().timestamp()) - 2592000  # 30 days
    r = requests.get(
        "https://hn.algolia.com/api/v1/search",
        params={"query": term, "tags": "story",
                "numericFilters": f"created_at_i>{since}"},
    ).json()
    return {"hits_30d": r.get("nbHits", 0), "source": "hacker_news"}


def gh_repos(term: str) -> dict:
    since = (dt.date.today() - dt.timedelta(days=180)).isoformat()
    r = requests.get(
        "https://api.github.com/search/repositories",
        params={"q": f"{term} created:>{since}", "sort": "stars", "order": "desc"},
    ).json()
    items = r.get("items") or [{}]
    return {
        "new_repos_180d": r.get("total_count", 0),
        "top_stars": items[0].get("stargazers_count", 0),
        "source": "github",
    }


def collect(term: str) -> dict:
    return {
        "term": term,
        "ts": dt.datetime.utcnow().isoformat() + "Z",
        "signals": [google_trends(term), hn_hits(term), gh_repos(term)],
    }


if __name__ == "__main__":
    term = sys.argv[1] if len(sys.argv) > 1 else "AI agents"
    print(json.dumps(collect(term), indent=2))
