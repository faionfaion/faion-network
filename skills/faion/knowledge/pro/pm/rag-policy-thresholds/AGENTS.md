---
slug: rag-policy-thresholds
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Defines Red/Amber/Green project-health thresholds (numeric, published, evidence-anchored) so PM status reporting stops being judgment and starts being a tool; emits typed `RAGPolicy` per project with named inputs + thresholds + decision rule + refresh cadence.
content_id: "c7380f62da1a4259"
complexity: medium
produces: decision-record
est_tokens: 3500
tags: [pm, pro, rag, status-reporting, project-health, thresholds]
---
# RAG Policy Thresholds

## Summary

**One-sentence:** A typed RAG (Red/Amber/Green) policy that pins numeric thresholds per signal (schedule variance, budget variance, defect escape rate, blocker count) so PM status reporting becomes a reproducible decision rule instead of weekly gut-call.

**One-paragraph:** PM status reporting is dominated by "I feel this is Amber" — bias, fatigue, and stakeholder pressure all push the colour. This methodology pins a `RAGPolicy` per project: named numeric inputs, published thresholds (no "significant" or "material" without a number), a default action per colour, and a quarterly review. Output is a typed decision-record that downstream stakeholder reports cite by version + last_reviewed. Refresh cadence ≤ 90 days; reviews remove unused thresholds and add new ones tied to incident history.

**Ефективно для:**

- Weekly PM client / leadership status reporting across multiple projects with consistent rules.
- Distressed-project rescue trigger (Red colour fires escalation playbook).
- Audit defensibility: every colour ties to a published numeric threshold.
- Quarterly review: thresholds tied to actual incident history, not vibes.

## Applies If (ALL must hold)

- Project has measurable signals (schedule, budget, defect-escape, blockers).
- A PM owns the artefact (or escalates to named role).
- Reporting cadence is recurring (weekly / fortnightly).
- Stakeholders accept numeric thresholds as the source of truth.

## Skip If (ANY kills it)

- One-shot project with no recurrence.
- < 3 reports per year — review cadence costs more than it returns.
- Regulated context mandating a specific status framework — adopt that template.
- No named owner.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Signal sources (telemetry / Jira / git) | API tokens | platform |
| Incident / postmortem corpus | Markdown | engineering |
| Reporting calendar | calendar invite | PM |
| Previous quarter RAG outcomes | JSON | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[value-stream-management]] | Flow + DORA metrics feed RAG signal inputs. |
| [[team-morale-pulse-survey]] | eNPS / clarity feed the team-health signal. |
| [[proposal-red-team-checklist]] | Red trigger inputs into the next proposal's red-team. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: explicit trigger, bounded output, evidence-anchored, named owner, iteration loop | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `RAGPolicy` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: cargo-cult, ownership ambiguity, drift, example-text leakage, no outcome review, trigger drift | ~900 |
| `content/04-procedure.xml` | medium | 5-step: scaffold → set thresholds → publish → run weekly → quarterly review | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: signal value vs threshold → colour + escalation rule | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `set-thresholds` | sonnet | Per-signal judgment anchored in incident history. |
| `compute-colour` | haiku | Mechanical threshold comparison. |
| `outcome-review-synthesis` | opus | Cross-quarter calibration. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | RAG policy skeleton with default thresholds |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum viable filled `RAGPolicy` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-policy-thresholds.py` | Validate `RAGPolicy`: numeric thresholds, named inputs, evidence, owner | Pre-merge |
| `scripts/staleness-check.py` | Flag policies whose `last_reviewed` > 90 days | Weekly cron |

## Related

- [[value-stream-management]]
- [[team-morale-pulse-survey]]
- [[regulatory-uncertainty-buffer]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps signal values to colour + default action — Green continues, Amber triggers PM review, Red triggers escalation playbook. Every leaf references a rule from `01-core-rules.xml`.
