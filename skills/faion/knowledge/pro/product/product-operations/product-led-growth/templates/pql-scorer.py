"""
pql-scorer.py — minimal PostHog PQL scorer.
Weights in-app events into a score and writes back as person property
so feature flags and sales-assist routing can consume it.

Usage: PH_HOST=https://app.posthog.com PH_KEY=phx_... python pql-scorer.py

Tune WEIGHTS per product. Recalibrate quarterly.
"""
import os, time, requests

HOST = os.environ["PH_HOST"].rstrip("/")
KEY = os.environ["PH_KEY"]

# Tune these weights per product; recalibrate quarterly.
# Use upgrade-intent events (limit warnings, team invites) not vanity events.
WEIGHTS = {
    "workspace_created":   3,
    "second_user_invited": 5,
    "integration_added":   4,
    "report_exported":     2,
    "limit_warning_seen":  6,  # strongest buying signal
}
SINCE = int(time.time()) - 14 * 86400  # last 14 days


def hog(path: str, **q):
    r = requests.get(
        f"{HOST}{path}",
        headers={"Authorization": f"Bearer {KEY}"},
        params=q,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


scores: dict[str, int] = {}
for evt, w in WEIGHTS.items():
    page = hog("/api/event/", event=evt, after=SINCE)
    for e in page.get("results", []):
        did = e.get("distinct_id")
        if did:
            scores[did] = scores.get(did, 0) + w

for did, score in scores.items():
    tier = "hot" if score >= 12 else "warm" if score >= 6 else "cold"
    requests.post(
        f"{HOST}/api/projects/@current/persons/",
        headers={"Authorization": f"Bearer {KEY}"},
        json={
            "distinct_id": did,
            "properties": {"pql_score": score, "pql_tier": tier},
        },
        timeout=30,
    )

print(f"scored {len(scores)} users")
