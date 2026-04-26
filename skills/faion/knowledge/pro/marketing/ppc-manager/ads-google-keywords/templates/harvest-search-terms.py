"""
harvest_search_terms.py

Pull queries that spent money in the last N days from a Google Ads campaign.
Output rows for human classification before applying as exact keywords or negatives.

Usage:
    python harvest_search_terms.py --customer-id 123-456-7890 --days 7 --min-clicks 3
"""

def harvest_search_terms(client, customer_id: str, days: int = 7, min_clicks: int = 3) -> list[dict]:
    """Pull queries with spend that are not yet keywords or negatives."""
    ga = client.get_service("GoogleAdsService")
    query = f"""
        SELECT search_term_view.search_term, search_term_view.status,
               campaign.name, ad_group.name,
               metrics.clicks, metrics.cost_micros, metrics.conversions
        FROM search_term_view
        WHERE segments.date DURING LAST_{days}_DAYS
          AND metrics.clicks >= {min_clicks}
    """
    rows = []
    for row in ga.search(customer_id=customer_id, query=query):
        rows.append({
            "query": row.search_term_view.search_term,
            "campaign": row.campaign.name,
            "ad_group": row.ad_group.name,
            "clicks": row.metrics.clicks,
            "cost": row.metrics.cost_micros / 1_000_000,
            "conversions": row.metrics.conversions,
            # NONE = not yet added; ADDED = already a keyword; EXCLUDED = already a negative
            "status": row.search_term_view.status.name,
        })
    # Pass rows to classifier (LLM or rule engine) — never auto-apply
    return rows
