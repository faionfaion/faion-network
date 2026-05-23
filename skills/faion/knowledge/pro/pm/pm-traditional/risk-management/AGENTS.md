---
slug: risk-management
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Structured PMBoK risk process that produces a register with named owners, observable triggers, P×I + EMV scores, and weekly review cadence.
content_id: "871a470deecd376e"
complexity: medium
produces: spec
est_tokens: 4500
tags: [risk-management, pmbok, contingency, emv, uncertainty]
---
# Risk Management

## Summary

**One-sentence:** Structured PMBoK risk process that produces a register with named owners, observable triggers, P×I + EMV scores, and weekly review cadence.

**One-paragraph:** Risk management identifies, scores, responds to, and monitors project uncertainty across both threats and opportunities. Every risk in the register carries a named owner, an observable trigger condition, a chosen response strategy, and a P×I score with source rationale. EMV rolls into a single contingency line that finance can defend; the register is reviewed weekly and risks are closed explicitly with outcomes. The methodology output is a versioned risk register artefact reviewed at each milestone.

**Ефективно для:**

- Multi-month delivery (>$10k or >2 weeks at risk) needing defensible contingency.
- Regulated / safety-critical / contractual work demanding audit-trail evidence.
- Cross-team programmes with vendor, tech, and resource interdependencies.
- Programmes with documented prior risk failures requiring stronger discipline.

## Applies If (ALL must hold)

- Delivery spans multiple months and surprises cost more than $10k or two weeks.
- Regulated, safety-critical, or contractual work where audit trail is mandatory.
- Cross-team programme with technical, vendor, and resource interdependencies.
- A quantitative contingency reserve must be defended to finance.

## Skip If (ANY kills it)

- Pure exploratory R&D or spike work — fail-fast learning beats register hygiene.
- Single-developer hobby projects — a RISKS.md checklist is sufficient.
- Sub-two-week features where ceremony cost exceeds expected loss.
- Pure Scrum teams with adequate impediment + retro coverage already.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Project charter + WBS | Markdown / .csv | scope-management |
| Cost-estimation baseline | spreadsheet | cost-estimation |
| HR attrition base-rate | table | HR / vendor SOWs |
| Historical risk archive | register exports | prior projects |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `wbs-creation` | Provides work packages used as risk anchor points. |
| `stakeholder-register` | Names accountable owners per risk. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — trigger, owner, scoring rationale, calibration cadence, closure discipline | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the register artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: identify → analyse → respond → monitor → close | 900 |
| `content/05-examples.xml` | optional | Worked example end-to-end (key-person risk, EMV $9k) | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on shape signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-risks-from-charter` | sonnet | Needs grounding in project artefacts; haiku invents generic risks. |
| `score-pi-and-emv` | sonnet | Anchors on base-rate evidence; demands rationale per score. |
| `diff-vs-prior-register` | haiku | Mechanical NEW/CHANGED/CLOSED/STALE diff. |
| `weekly-review-synthesis` | opus | Cross-week pattern + closure narratives for steering committee. |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-register.md` | PMBoK-aligned register with EMV-ready columns. |
| `templates/risk-response-plan.md` | Per-risk response plan attached to register row. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-risk-management.py` | Schema-validate the risk register JSON artefact. | Pre-commit + before steering review. |
| `scripts/emv.py` | Score the Markdown register; exit non-zero on critical untriaged risks. | Weekly cron + pre-steering-review. |

## Related

- [[risk-register]]
- [[schedule-development]]
- [[stakeholder-register]]
- [[wbs-creation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the risk-management input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
