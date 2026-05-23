# Scope-Creep Firewall

## Summary

**One-sentence:** Per-engagement intake-and-classify gate that converts every new ask into change-order, no-op, in-scope-clarified, or backlog — never silently absorbed.

**One-paragraph:** Per-engagement intake-and-classify gate that converts every new ask into change-order, no-op, in-scope-clarified, or backlog — never silently absorbed. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned playbook-step artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- соло-оператор тримає один named «gate» для всіх нових запитів.
- ≤5-хвилинний triage кожного запиту з фіксованим default «change-order».
- weekly creep summary до клієнта → попередження замість скандалу.
- creep-trend per engagement → ранній сигнал нездорового контракту.
- інтеграція з email-pack для outbound фраз і з impact rubric для accepted CR.

## Applies If (ALL must hold)

- the engagement has a written scope (SOW, proposal, statement of work).
- the operator is solo or works with ≤2 collaborators (no PMO buffer).
- engagement length 4 weeks or longer.
- tier == pro or higher.

## Skip If (ANY kills it)

- engagement is explicitly time-and-materials with no scope cap and unlimited budget.
- client uses a formal change-control process the operator is already participating in.
- operator is in the final 5 business days of the engagement — switch to handover mode.

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
| `templates/scope-creep-firewall.md` | Working playbook-step skeleton with 5-line header |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-scope-creep-firewall.py` | Validate the playbook-step artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[scope-creep-email-language-pack]]
- [[change-request-impact-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
