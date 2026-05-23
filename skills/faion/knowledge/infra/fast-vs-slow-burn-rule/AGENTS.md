# Fast vs Slow Burn Rule

## Summary

**One-sentence:** Multi-window multi-burn-rate alerting rule: configure 4 windows (1h fast, 6h sustained, 3d slow, 30d trend) with calibrated burn-rate thresholds so SLO violations alert at the right cadence.

**One-paragraph:** Single-window burn alerts produce false positives (every transient spike pages on-call) or false negatives (sustained slow burn never alerts). Google SRE's multi-window multi-burn-rate pattern uses 4 windows with calibrated thresholds: 1h × 14.4 burn-rate (page-now), 6h × 6 burn-rate (page-soon), 3d × 1 burn-rate (ticket), 30d × 0.1 trend (review). This methodology pins the threshold math + the PromQL templates + the alert routing so every SLO produces a coherent multi-window ruleset, not 50 ad-hoc alerts.

**Ефективно для:**

- Уникнення 50 ad-hoc alerts per SLO — 4 windows per SLO, точно.
- Calibrated thresholds: 1h × 14.4 не false-positives; 30d × 0.1 catches slow drift.
- Routing: 1h → page; 6h → page; 3d → ticket; 30d → review (no page).
- PromQL templates: copy-paste пер service-class без помилок calibration.

## Applies If (ALL must hold)

- SLOs defined with explicit objective + window
- Metric system (Prometheus / Datadog / Honeycomb) supports range queries with multiple windows
- Multi-window alerting supported (recording rules or native multi-window rules)
- Team commits to act on slow-burn (otherwise the slow window is noise)

## Skip If (ANY kills it)

- Single-SLO single-service shop — one-window may be enough
- Metric system without range queries — pick another methodology

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recording rules for SLI good/total counts | PrometheusRule | SRE |
| Alertmanager routing config | alertmanager.yaml | platform team |
| SLO target list per service | slo.yaml | service owners |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[slo-definition-template-per-service-class]] | SLIs this rule consumes |
| [[slo-burn-decision-matrix]] | Actions this rule triggers |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `threshold_math` | haiku | Arithmetic on SLO + window |
| `recording_rule_authoring` | sonnet | PromQL synthesis |
| `alertmanager_routing` | haiku | Mechanical YAML fill |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fast-vs-slow-burn-rule.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[slo-burn-decision-matrix]]
- [[slo-definition-template-per-service-class]]
- [[error-budget-policy-and-freeze-rules]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
