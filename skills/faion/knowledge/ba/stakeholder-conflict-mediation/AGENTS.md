# Stakeholder Conflict Mediation

## Summary

**One-sentence:** In-the-moment five-step loop (pause → reframe → isolate → propose → confirm) for the BA when a stakeholder conflict erupts mid-requirements-review.

**One-paragraph:** In-the-moment five-step loop (pause → reframe → isolate → propose → confirm) for the BA when a stakeholder conflict erupts mid-requirements-review. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned playbook-step artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- конфлікт спалахнув mid-review без попереднього scheduling.
- BA є facilitator / co-facilitator зустрічі.
- ≥2 стейкхолдери відкрито протистоять по конкретному requirement.
- у project charter названо escalation contact для unresolved conflicts.
- є ≥10 хв часу залишилось у зустрічі для одного циклу loop.

## Applies If (ALL must hold)

- conflict erupts during an active requirements review (not pre-scheduled mediation).
- the BA is the meeting facilitator or co-facilitator.
- at least two named stakeholders are taking opposing positions on a specific requirement.
- an escalation contact (sponsor, product head) is agreed in the project charter.

## Skip If (ANY kills it)

- pre-scheduled conflict meeting — use stakeholder-conflict-facilitation-script instead.
- conflict is interpersonal/political, not requirements-based — defer to HR/manager.
- meeting has under 10 minutes remaining — schedule a dedicated follow-up.
- no agreed escalation path exists — fix that first; the loop has no exit without it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the playbook-step artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, no judgement. |
| `synthesize-decision` | sonnet | Per-instance judgement against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stakeholder-conflict-mediation.md` | Working playbook-step skeleton with 5-line header |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-conflict-mediation.py` | Validate the playbook-step artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[stakeholder-conflict-facilitation-script]]
- [[decision-rationale-capture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
