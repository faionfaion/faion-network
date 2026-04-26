"""
stakeholder-lint.py — lint a stakeholder register for known rot patterns.
Usage: python stakeholder-lint.py .aidocs/product_docs/stakeholder-register.md
Exit 0 = OK, 1 = FAIL (high-power under-engagement), 2 = WARN (other issues).
"""
import sys, pathlib, datetime, collections

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
rows = [r.strip() for r in src.splitlines() if r.startswith("|") and "---" not in r]
if not rows:
    print("FAIL: no table rows found"); sys.exit(1)

header = [c.strip().lower() for c in rows[0].strip("|").split("|")]
required = {"name", "role", "interest", "power", "attitude", "engagement", "owner"}
missing_cols = required - set(header)
if missing_cols:
    print(f"FAIL: missing columns: {sorted(missing_cols)}"); sys.exit(1)

idx = {c: header.index(c) for c in required}
issues: collections.Counter = collections.Counter()

for r in rows[1:]:
    cells = [c.strip() for c in r.strip("|").split("|")]
    if len(cells) < len(header):
        continue

    attitude = cells[idx["attitude"]].lower()
    power = cells[idx["power"]].lower()
    interest = cells[idx["interest"]].lower()
    engagement = cells[idx["engagement"]].lower()
    owner = cells[idx["owner"]].lower()

    if attitude in ("", "unknown", "tbd"):
        issues["attitude_unknown"] += 1
    if owner in ("", "tbd", "?", "team", "whole team"):
        issues["no_owner"] += 1
    if power == "high" and engagement in ("monitor", "informed"):
        issues["high_power_under_engaged"] += 1
    if interest == "low" and power == "low" and engagement == "partner":
        issues["over_engaged_low_low"] += 1

if issues:
    print(f"WARN ({datetime.date.today()}): {dict(issues)}")
    if "high_power_under_engaged" in issues:
        sys.exit(1)  # FAIL — this is a relationship risk
    sys.exit(2)      # WARN — fix before next review
else:
    print(f"OK: register lint passed ({datetime.date.today()})")
    sys.exit(0)
