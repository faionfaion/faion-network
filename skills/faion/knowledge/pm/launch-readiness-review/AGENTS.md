# Launch Readiness Review

## Summary

**One-sentence:** Cross-functional 8-gate pre-launch readiness review (security, performance, observability, runbooks, on-call, legal, support enablement, comms tree) producing a hard go/no-go decision with remediation list.

**One-paragraph:** Eight gates with named owners, hard criteria, sequential T-7/T-3/T-1 readiness snapshots, and blocker veto. Output: LaunchReadiness JSON with per-gate status + go/no-go + open blockers + remediation owners. Built on Google SRE PRR + AWS Well-Architected + Cagan launch essays.

**Ефективно для:**

- Net-new продукт або service launch для зовнішніх клієнтів.
- Cross-functional команда >=3 з PM/eng/sec/support/legal.
- Launch window 4-12 тижнів наперед.
- Audit-вимоги (SOC2, ISO, HIPAA) із обов'язковими pre-launch sign-offs.

## Applies If (ALL must hold)

- Net-new product or service launch (not a bugfix release).
- Launch will hit external customers (not internal beta).
- Team size >=3 with cross-functional gates realistic.
- Launch date within next 4-12 weeks.

## Skip If (ANY kills it)

- Shipping a hotfix or minor feature — overhead exceeds value.
- Internal-only launch — only security + observability gates apply.
- Solo SaaS — use the lighter solo launch checklist.
- Launch already shipped — use launch-retro methodology instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Launch date | ISO date | PM |
| Gate owner roster | table {gate, owner, backup} | PM / org chart |
| SLO targets | YAML | SRE / engineering |
| Legal review | ToS / Privacy decision | counsel |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[release-planning]] | Provides the release calendar this review snaps to. |
| [[stakeholder-management]] | Names gate owners + escalation path. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: 8-gate coverage, named owner, hard criterion, blocker veto, T-7/T-3/T-1 snapshots | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for LaunchReadiness report | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: rubber-stamp, missing owner, partial sign-off, late-binding criteria, single snapshot | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: identify gates -> assign owners -> evaluate -> snapshot -> decide | 900 |
| `content/05-examples.xml` | medium | Worked review producing go-with-conditions decision | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on launch type + team size + window | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gate-owner-identification` | haiku | Lookup against org chart. |
| `criterion-evaluation` | sonnet | Bounded judgment per gate. |
| `go-no-go-synthesis` | opus | Cross-team decision needs careful reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/launch-readiness.json` | JSON skeleton for the LaunchReadiness report. |
| `templates/gate-criteria.yaml` | Hard criteria per gate (latency p95, runbook URLs, ToS sign-off, etc.). |
| `templates/comms-tree.md` | Customer + internal comms tree template. |
| `templates/run-readiness.py` | Pulls gate status from owners; assembles snapshot. |
| `templates/runbook-presence-check.py` | Verifies runbook URLs return 200 OK. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-launch-readiness-review.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[release-planning]]
- [[stakeholder-management]]
- [[product-explainability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
