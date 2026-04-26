"""
mp_track.py — GA4 Measurement Protocol server-side event helper.

Use for server-side event tracking when client-side gtag is blocked by ad-blockers.
CRITICAL: Pass client_id from the browser _ga cookie — never generate a fresh UUID.
"""
import requests


def track_server_event(
    measurement_id: str,
    api_secret: str,
    client_id: str,
    event_name: str,
    params: dict | None = None,
) -> bool:
    """
    Send a single event to GA4 via Measurement Protocol.

    Args:
        measurement_id: G-XXXXXXXXXX format
        api_secret: API secret from GA4 Admin → Data Streams → Measurement Protocol
        client_id: Value from the _ga browser cookie (NOT a fresh UUID)
        event_name: Must be <= 40 chars
        params: Event parameters dict; max 25 keys, keys <= 40 chars, values <= 100 chars

    Returns:
        True if accepted (HTTP 204), False otherwise
    """
    url = (
        f"https://www.google-analytics.com/mp/collect"
        f"?measurement_id={measurement_id}&api_secret={api_secret}"
    )
    payload = {
        "client_id": client_id,
        "events": [{"name": event_name, "params": params or {}}],
    }
    response = requests.post(url, json=payload, timeout=5)
    return response.status_code == 204
