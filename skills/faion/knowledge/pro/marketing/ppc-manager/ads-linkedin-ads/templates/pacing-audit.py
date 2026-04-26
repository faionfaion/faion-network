"""
pacing_audit.py — flag LinkedIn campaigns spending too fast or too slow vs. daily cap

Input (via environment):
    LI_ACCESS_TOKEN: OAuth access token
    LI_AD_ACCOUNT_URN: e.g. urn:li:sponsoredAccount:123456789

Input (function args):
    campaign_id (str): LinkedIn campaign ID
    daily_cap_usd (float): expected daily spend in USD

Output:
    dict with keys:
        campaign (str), spend (float), expected (float),
        variance (float, positive = overpacing)

Usage:
    from pacing_audit import audit
    result = audit("987654321", 100.0)
    if result["variance"] > 0.2:
        print(f"OVERPACING: {result['campaign']} spending {result['spend']:.2f}")
    elif result["variance"] < -0.2:
        print(f"UNDERPACING: {result['campaign']} spending {result['spend']:.2f}")
"""

import datetime as dt
import os

import requests

TOKEN = os.environ["LI_ACCESS_TOKEN"]
LINKEDIN_VERSION = "202410"


def fetch_today_spend(campaign_id: str) -> float:
    today = dt.date.today()
    url = (
        f"https://api.linkedin.com/rest/adAnalytics?q=analytics"
        f"&pivot=CAMPAIGN"
        f"&campaigns=List(urn%3Ali%3AsponsoredCampaign%3A{campaign_id})"
        f"&dateRange=(start:(year:{today.year},month:{today.month},day:{today.day}))"
        f"&fields=costInLocalCurrency,impressions,clicks"
    )
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "LinkedIn-Version": LINKEDIN_VERSION,
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    elements = data.get("elements", [])
    if not elements:
        return 0.0
    return float(elements[0].get("costInLocalCurrency", 0))


def audit(campaign_id: str, daily_cap_usd: float) -> dict:
    """Compare actual spend to expected spend for the current hour of day."""
    spend = fetch_today_spend(campaign_id)
    hour_pct = dt.datetime.now().hour / 24
    expected = daily_cap_usd * hour_pct
    variance = (spend - expected) / max(expected, 1)
    return {
        "campaign": campaign_id,
        "spend": spend,
        "expected": expected,
        "variance": round(variance, 3),
    }
