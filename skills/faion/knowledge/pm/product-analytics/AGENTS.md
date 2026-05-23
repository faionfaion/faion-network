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
| `templates/tracking-plan.md` | Tracking-plan skeleton with event table + version field. |
| `templates/tracking-plan-lint.sh` | Lint script for naming + ownership compliance. |
| `templates/event-spec.yaml` | Per-event spec template with properties + owner. |

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
