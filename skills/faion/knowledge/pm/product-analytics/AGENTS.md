# Product Analytics

## Summary

**One-sentence:** Tracking-plan + funnel/cohort instrumentation discipline (AARRR / North Star) feeding agent-readable BI sources for activation diagnosis, weekly health digests, and experiment readouts.

**One-paragraph:** Versioned tracking plan with snake_case past-tense `object_action` events, a North Star + 2-3 input metrics with causal links, explicit anomaly rules for digests, and PII redaction at ingest. Agents author event specs, run rule-based anomaly scans, and synthesize cross-segment readouts. Output: tracking-plan YAML + per-event spec + weekly health digest.

**Ефективно для:**

- Pre-launch: tracking-plan drafted from spec, day-1 events ship з кодом.
- Activation diagnosis: drop у funnel + cohort table -> highest-leakage step.
- Scheduled product-health digest читає BI source і пише markdown із anomalies.
- Post-experiment readout: merge exposure logs + metric tables, flag Simpson-segment.

## Applies If (ALL must hold)

- Pre-launch: agent drafts the tracking plan from a feature spec.
- Activation diagnosis: drop in funnel data + cohort table.
- Weekly product-health digest: scheduled agent reads BI source, writes markdown summary with anomalies.
- Post-experiment readout: merge A/B exposure logs with metric tables.
- Tracking-plan audit before a vendor migration (e.g., GA4 -> PostHog).

## Skip If (ANY kills it)

- Pre-MVP with no live events.
- Product fully measured by external vendor (Stripe revenue) with no in-app behaviour.
- Compliance lockdown where event collection is legally restricted.
- Single-page marketing site without behavioural funnel.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec | markdown / Figma | PM |
| BI source | BigQuery / Snowflake / Postgres replica | data team |
| North Star + input metrics | documented | leadership / PM |
| PII inventory | list of fields | security / privacy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[experimentation-at-scale]] | Provides exposure-log conventions for post-experiment readouts. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: versioned tracking-plan, event naming, North Star tree, anomaly rule set, PII redaction at ingest | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for tracking-plan + per-event spec | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: untracked events, naming chaos, vanity metrics, late PII redaction | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: spec -> events -> metric tree -> digest rules -> validate | 800 |
| `content/05-examples.xml` | medium | Worked tracking plan + weekly health digest | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on event volume + vendor coverage | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `event-spec-author` | sonnet | Draft event spec from feature requirements. |
| `anomaly-scan` | haiku | Mechanical rule-based anomaly detection. |
| `post-experiment-readout` | opus | Cross-segment + Simpson-paradox detection. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tracking-plan.md.j2` | Tracking-plan skeleton with event table + version field. |
| `templates/tracking-plan.md` | Tracking-plan skeleton with event table + version field. Generated from `templates/tracking-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/tracking-plan-lint.sh` | Lint script for naming + ownership compliance. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-analytics.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[experimentation-at-scale]]
- [[product-led-growth]]
- [[feedback-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tracking-plan-lint.sh`

```bash
set -euo pipefail
#!/usr/bin/env bash
# tracking-plan-lint.sh — enforce naming + required fields on a markdown Tracking Plan.
# Usage: tracking-plan-lint.sh path/to/tracking-plan.md
# Checks: snake_case, object_action shape, non-empty trigger, non-empty properties.
set -euo pipefail
file="${1:?usage: tracking-plan-lint.sh PLAN.md}"
python3 - "$file" <<'PY'
import re, sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text()
errs = []
# Match table rows with at least 3 pipe-separated cells
row_re = re.compile(r"^\|\s*([a-zA-Z0-9_\[\]]+)\s*\|([^|]+)\|([^|]+)\|", re.M)
seen = {}
for m in row_re.finditer(src):
    name, trigger, props = (s.strip() for s in m.groups())
    # Skip header and separator rows
    if name.lower() in ("event", "property", "metric", "---", "object_action"):
        continue
    if name.startswith("[") or name.startswith("-"):
        continue
    # Check snake_case
    if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
        errs.append(f"{name}: not snake_case")
    # Check object_action shape (must have at least one underscore)
    if "_" not in name:
        errs.append(f"{name}: missing object_action shape (no underscore)")
    # Check non-empty trigger
    if not trigger or trigger.strip().startswith("TODO") or trigger.strip() == "—":
        errs.append(f"{name}: missing or TODO trigger")
    # Check non-empty properties
    if not props or props.strip().startswith("TODO") or props.strip() == "—":
        errs.append(f"{name}: missing or TODO properties")
    # Check for duplicates
    if name in seen:
        errs.append(f"{name}: duplicate event (first seen in: '{seen[name]}')")
    seen[name] = trigger.strip()[:40]

if errs:
    print("Tracking-plan lint errors:")
    for e in errs:
        print(f"  - {e}")
    sys.exit(1)
print(f"OK: {len(seen)} events validated.")
PY
```
