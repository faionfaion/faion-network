"""
variance_check.py — flag platform vs. warehouse attribution drift per channel

Input:
    rows: list of dicts with keys:
        channel (str), platform_conv (float), ga4_conv (float),
        warehouse_conv (float), spend (float)

Output:
    list of dicts with per-channel variance percentages and alert flag
    (alert=True when any variance exceeds 15%)

Usage:
    from variance_check import variance
    rows = [
        {"channel": "meta", "platform_conv": 100, "ga4_conv": 85,
         "warehouse_conv": 80, "spend": 5000},
        {"channel": "google", "platform_conv": 80, "ga4_conv": 70,
         "warehouse_conv": 75, "spend": 4000},
    ]
    results = variance(rows)
    for r in results:
        if r["alert"]:
            print(f"ALERT: {r['channel']} variance exceeds 15%")
"""

VARIANCE_THRESHOLD = 0.15


def variance(rows: list[dict]) -> list[dict]:
    """Compute platform-vs-warehouse and GA4-vs-warehouse variance per channel."""
    out = []
    for r in rows:
        pc = r["platform_conv"]
        gc = r["ga4_conv"]
        wc = r["warehouse_conv"]
        base = wc or 1

        platform_vs_wh = (pc - wc) / base
        ga4_vs_wh = (gc - wc) / base
        alert = abs(platform_vs_wh) > VARIANCE_THRESHOLD or abs(ga4_vs_wh) > VARIANCE_THRESHOLD

        out.append({
            "channel": r["channel"],
            "platform_vs_warehouse_pct": round(platform_vs_wh * 100, 1),
            "ga4_vs_warehouse_pct": round(ga4_vs_wh * 100, 1),
            "warehouse_cpa": round(r["spend"] / base, 2) if wc else None,
            "alert": alert,
        })
    return out
