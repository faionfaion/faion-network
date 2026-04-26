#!/usr/bin/env python3
"""discovery_cadence.py — emit this week's discovery checklist as JSON.

Output (stdout): JSON checklist with daily/weekly/biweekly/quarterly tasks.
No arguments needed.
"""
import datetime
import json
import sys


def main() -> None:
    today = datetime.date.today()
    iso = today.isocalendar()
    week_id = f"{iso.year}-W{iso.week:02d}"

    checklist = {
        "week": week_id,
        "daily": [
            "Review support ticket triage digest",
            "Scan analytics for anomalies (>2 sigma from baseline)",
        ],
        "weekly": [
            "Run 1-3 user interviews (recruit across segments, not just active users)",
            "Synthesize prior 7 days of feedback into themes using controlled vocabulary",
            "Review competitor changelogs and pricing pages",
            "Draft 3 interview question scripts for next week",
        ],
        "biweekly": [
            "Diff current opportunity themes against roadmap",
            "Propose roadmap adds/removes/re-prioritizations with opportunity citations",
            "Human reviews and records decision + rationale",
        ],
        "quarterly": [
            "Re-baseline theme vocabulary (require approval for any changes)",
            "Audit interview sample: who has not been interviewed in 90 days?",
            "Review discovery tooling and automation health",
        ],
        "automation_required": [
            "Daily analytics anomaly check via scheduled job",
            "Weekly feedback ingestion from support / app store / in-app channels",
            "PII redaction pre-pass before any LLM synthesis",
        ],
    }

    print(json.dumps(checklist, indent=2))


if __name__ == "__main__":
    main()
