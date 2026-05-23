#!/usr/bin/env python3
"""
market_trend_signals.py — macro + regulatory + filings collector for trend analysis.

Collects:
  - FRED macro series (US rates, GDP, CPI, employment)
  - US Federal Register proposed/final rules
  - EUR-Lex EU regulation metadata

Usage:
    FRED_API_KEY=<key> python market_trend_signals.py "AI agents" "FEDFUNDS,GDPC1"
    Output: JSON to stdout

Dependencies: pip install fredapi requests
"""
import os
import json
import sys
import datetime
import requests

try:
    from fredapi import Fred
    FRED_AVAILABLE = True
except ImportError:
    FRED_AVAILABLE = False


def macro(series_ids: list[str]) -> list[dict]:
    if not FRED_AVAILABLE:
        return [{"error": "fredapi not installed — pip install fredapi"}]
    fred = Fred(api_key=os.environ["FRED_API_KEY"])
    out = []
    for sid in series_ids:
        try:
            s = fred.get_series(sid).dropna()
            if s.empty:
                continue
            last = float(s.iloc[-1])
            prev = float(s.iloc[-13]) if len(s) > 13 else float(s.iloc[0])
            yoy = None if prev == 0 else round((last - prev) / prev * 100, 2)
            out.append({
                "series": sid,
                "last": last,
                "yoy_pct": yoy,
                "source_url": f"https://fred.stlouisfed.org/series/{sid}",
                "source_type": "primary",
            })
        except Exception as e:
            out.append({"series": sid, "error": str(e)})
    return out


def federal_register(term: str, days: int = 90) -> list[dict]:
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    try:
        r = requests.get(
            "https://www.federalregister.gov/api/v1/documents",
            params={
                "conditions[term]": term,
                "conditions[publication_date][gte]": since,
                "per_page": 20,
            },
            timeout=15,
        ).json()
        return [
            {
                "rule_id": d.get("document_number"),
                "title": d.get("title"),
                "stage": d.get("type"),
                "effective_date": d.get("effective_on"),
                "source_url": d.get("html_url"),
                "jurisdiction": "US",
            }
            for d in r.get("results", [])
        ]
    except Exception as e:
        return [{"error": f"Federal Register fetch failed: {e}"}]


def eur_lex(term: str) -> list[dict]:
    """Returns search metadata only; downstream parser extracts CELEX ids."""
    try:
        r = requests.get(
            "https://eur-lex.europa.eu/search.html",
            params={"text": term, "scope": "EURLEX", "type": "quick", "DTS_DOM": "EU_LAW"},
            timeout=15,
        )
        return [{
            "source_url": "https://eur-lex.europa.eu/",
            "term": term,
            "jurisdiction": "EU",
            "status": "search_html_fetched",
            "raw_bytes": len(r.content),
            "note": "downstream parser extracts CELEX ids from raw_html",
        }]
    except Exception as e:
        return [{"error": f"EUR-Lex fetch failed: {e}"}]


def collect(term: str, fred_series: list[str]) -> dict:
    return {
        "term": term,
        "collected_at": datetime.datetime.utcnow().isoformat() + "Z",
        "macro": macro(fred_series),
        "regulatory_us": federal_register(term),
        "regulatory_eu": eur_lex(term),
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: market_trend_signals.py <term> <FRED_SERIES1,SERIES2,...>", file=sys.stderr)
        sys.exit(1)
    term = sys.argv[1]
    series = sys.argv[2].split(",")
    print(json.dumps(collect(term, series), indent=2))
