#!/usr/bin/env python3
"""cr-router.py — assign approval tier from a change request YAML file.

YAML schema (change_request.yaml):
  id: CR-2024-015
  impact:
    schedule_days: 8
    cost_usd: 4000
    risk: low   # low | medium | high

Tier rules:
  - risk=high          → CCB (regardless of size)
  - days<=1 & cost<=500  → PM
  - days<=5 & cost<=5000 → Sponsor
  - else               → CCB

Usage: python cr-router.py change_request.yaml
"""
import sys
import yaml

TIERS = [
    {"name": "PM",      "max_days": 1,    "max_usd": 500},
    {"name": "Sponsor", "max_days": 5,    "max_usd": 5_000},
    {"name": "CCB",     "max_days": None, "max_usd": None},
]


def route(cr: dict) -> str:
    impact = cr.get("impact", {})
    days = impact.get("schedule_days", 0)
    cost = impact.get("cost_usd", 0)
    risk = impact.get("risk", "low").lower()

    if risk == "high":
        return "CCB"

    for tier in TIERS:
        if tier["max_days"] is None:
            return tier["name"]
        if days <= tier["max_days"] and cost <= tier["max_usd"]:
            return tier["name"]

    return "CCB"


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: cr-router.py <change_request.yaml>")

    cr = yaml.safe_load(open(sys.argv[1]))
    tier = route(cr)
    impact = cr.get("impact", {})
    print(f"{cr['id']}: route to {tier}")
    print(f"  Days: {impact.get('schedule_days', 0)}, "
          f"Cost: ${impact.get('cost_usd', 0):,}, "
          f"Risk: {impact.get('risk', 'low')}")


if __name__ == "__main__":
    main()
