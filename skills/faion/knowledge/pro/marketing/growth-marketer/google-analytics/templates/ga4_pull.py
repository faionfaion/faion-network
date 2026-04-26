"""
ga4_pull.py — Daily top-events report via GA4 Data API.

Requires: pip install google-analytics-data
Auth: GOOGLE_APPLICATION_CREDENTIALS env var pointing to service account JSON.
"""
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest


def top_events(property_id: str, days: int = 7) -> list[dict]:
    """
    Pull top 10 events by count for the last N days.

    Args:
        property_id: GA4 numeric property ID (not the G-XXXX measurement ID)
        days: number of days to look back

    Returns:
        List of dicts with keys: event, count, users
    """
    client = BetaAnalyticsDataClient()
    req = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
        dimensions=[Dimension(name="eventName")],
        metrics=[Metric(name="eventCount"), Metric(name="totalUsers")],
        limit=10,
    )
    resp = client.run_report(req)
    return [
        {
            "event": r.dimension_values[0].value,
            "count": int(r.metric_values[0].value),
            "users": int(r.metric_values[1].value),
        }
        for r in resp.rows
    ]


# NOTE: Data API quota is 50 concurrent requests + 250k tokens/day per property.
# A haiku agent polling in a tight loop can exhaust this. Add caching or rate limiting.
