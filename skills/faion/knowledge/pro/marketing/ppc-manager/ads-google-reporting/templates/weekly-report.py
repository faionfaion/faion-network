"""
weekly_report.py — GAQL helpers for weekly performance reports and search terms triage

Functions:
    weekly_campaign_report(client, customer_id, days) -> list[dict]
        Returns campaign-level metrics for the last N days.
        All costs returned in currency (not micros).

    search_terms_for_negatives(client, customer_id, min_cost) -> list of GAQL rows
        Returns search terms with zero conversions and cost above threshold.
        Use to identify negative keyword candidates.

Usage:
    from weekly_report import weekly_campaign_report, search_terms_for_negatives
    rows = weekly_campaign_report(client, "1234567890", days=7)
    negatives = search_terms_for_negatives(client, "1234567890", min_cost=20)
"""

from google.ads.googleads.client import GoogleAdsClient  # noqa: F401


def weekly_campaign_report(client, customer_id: str, days: int = 7) -> list[dict]:
    """Pull campaign-level metrics for the last N days. Costs in currency (not micros)."""
    ga = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
            campaign.name,
            campaign.status,
            metrics.cost_micros,
            metrics.clicks,
            metrics.impressions,
            metrics.ctr,
            metrics.average_cpc,
            metrics.conversions,
            metrics.cost_per_conversion,
            metrics.search_impression_share
        FROM campaign
        WHERE segments.date DURING LAST_{days}_DAYS
          AND campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
    """
    rows = []
    for r in ga.search(customer_id=customer_id, query=query):
        conv = r.metrics.conversions
        cost = r.metrics.cost_micros / 1_000_000
        rows.append({
            "campaign": r.campaign.name,
            "status": r.campaign.status.name,
            "cost": cost,
            "clicks": r.metrics.clicks,
            "impressions": r.metrics.impressions,
            "ctr_pct": r.metrics.ctr * 100,
            "conv": conv,
            "cpa": cost / max(conv, 0.01),
            "impression_share_pct": r.metrics.search_impression_share * 100,
        })
    return rows


def search_terms_for_negatives(client, customer_id: str, min_cost: float = 20) -> list:
    """Return search terms with zero conversions and cost above min_cost USD."""
    ga = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
            search_term_view.search_term,
            campaign.id,
            campaign.name,
            ad_group.id,
            ad_group.name,
            metrics.cost_micros,
            metrics.conversions,
            metrics.clicks
        FROM search_term_view
        WHERE segments.date DURING LAST_7_DAYS
          AND metrics.cost_micros >= {int(min_cost * 1_000_000)}
          AND metrics.conversions = 0
        ORDER BY metrics.cost_micros DESC
        LIMIT 200
    """
    return list(ga.search(customer_id=customer_id, query=query))
