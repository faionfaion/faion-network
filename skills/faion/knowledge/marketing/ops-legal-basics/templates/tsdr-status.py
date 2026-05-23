"""
USPTO TSDR trademark status lookup.

Input:  serial_number (str) — USPTO trademark serial number (8 digits)
Output: dict with mark name and current status description

IMPORTANT: This resolves a KNOWN serial number only.
For pre-launch availability searches, use the USPTO TESS web UI or the TESS API
with a proximity/phonetic search — exact serial lookup alone is insufficient
to determine whether a new mark conflicts with existing registrations.

Usage:
    status = tsdr_status("90123456")
    print(status)
"""

import requests


def tsdr_status(serial_number: str) -> dict:
    url = f"https://tsdr.uspto.gov/ts/cd/casestatus/sn{serial_number}/info.json"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return {"error": f"HTTP {r.status_code} — serial not found or TSDR unavailable"}
        data = r.json()
        trademarks = data.get("trademarks", [{}])
        if not trademarks:
            return {"error": "no trademark records returned"}
        tm = trademarks[0]
        status_block = tm.get("status", {})
        return {
            "serial": serial_number,
            "mark": status_block.get("markElement", "unknown"),
            "status": status_block.get("statusDescription", "unknown"),
            "status_code": status_block.get("statusCode", "unknown"),
        }
    except requests.RequestException as exc:
        return {"error": str(exc)}
