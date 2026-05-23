---
slug: ci-prod-readiness-gates
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a single copy-paste CI config that bundles perf-budget, a11y, SLO-instrumentation, dep-vuln, lint, and license gates with a defensible blocking policy.
content_id: "5fa7d9af69eb9300"
complexity: medium
produces: config
est_tokens: 4300
tags: [ci, prod-readiness, gates, lint-floor, dep-vuln]
---
# CI Prod-Readiness Gates

## Summary

**One-sentence:** Produces a single copy-paste CI config that bundles perf-budget, a11y, SLO-instrumentation, dep-vuln, lint, and license gates with a defensible blocking policy.

**One-paragraph:** Bundles perf-budget, a11y, SLO-instrumentation, dep-vuln, lint, license gates into a single CI job definition the dev can copy-paste. Gates start as non-blocking (advisory) for 2 weeks, then ratchet to blocking. Each gate has a documented owner and an exception path (label-based bypass with audit log). Output: `.github/workflows/prod-readiness.yml` (or GitLab CI snippet) plus a `prod-readiness.yaml` budget file consumed by the job.

**Ефективно для:**

- Single CI gate замість 6 розкиданих jobs.
- Perf-budget + a11y + dep-vuln + lint + license — одне місце.
- Non-blocking → blocking ratchet (2 тижні shadow mode).
- Label-based exception path з audit log.

## Applies If (ALL must hold)

- Task is an instance of role-software-developer/Make Production Readiness a PR-Level Concern OR adjacent.
- Operator has Prerequisites available before starting.
- Output consumed by downstream PR pipeline.
- Tier == pro or higher.

## Skip If (ANY kills it)

- Team already maintains an equivalent prod-readiness gate.
- Greenfield prototype with no production users.
- Single-language script repo where the 6 gates do not apply.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing CI provider (GHA/GitLab) | YAML | repo |
| Perf budget for the surface | JSON | ops decision |
| Dep-vuln tool (Snyk/Dependabot/Trivy) | config | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[software-developer]] | Operating context for PR-level concerns |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-budget-file` | sonnet | Author prod-readiness.yaml thresholds per surface. |
| `draft-gates-yml` | sonnet | Bundle 6 gates into one CI job. |
| `review-for-compliance` | opus | Cross-gate synthesis when license + dep-vuln conflict. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prod-readiness.yml` | GitHub Actions workflow bundling all 6 gates. |
| `templates/prod-readiness.yaml` | Budget config consumed by the gates. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ci-prod-readiness-gates.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |
| `scripts/validate-ci-prod-readiness-gates.py` | Validator script. | after subagent returns, before downstream consumer reads |

## Related

- [[capacity-bottleneck-checklist]]
- [[code-review-slo-and-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. Tree routes between shipping a new gate, flipping a gate to blocking, or rolling back based on shadow-mode noise rate.
