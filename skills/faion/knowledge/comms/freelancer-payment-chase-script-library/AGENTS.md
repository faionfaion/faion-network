# Freelancer Payment Chase Script Library

## Summary

**One-sentence:** Escalation ladder of payment-chase emails (polite → firm → legal-mention) tuned to preserve the relationship while collecting.

**One-paragraph:** Escalation ladder of payment-chase emails (polite → firm → legal-mention) tuned to preserve the relationship while collecting. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned checklist artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- invoice прострочений, але relationship хочеш зберегти.
- ladder: polite (T+3) → firm (T+10) → legal-mention (T+30).
- кожен крок — typed input (invoice id, amount, contract clause).
- log send + response → дані для повторного аудиту контракту.
- stop-conditions: client paid OR ladder exhausted → handoff to legal.

## Applies If (ALL must hold)

- the triggering activity 'Invoice send + chase-up (role: p3-technical-freelancer)' shows up at least once per cycle.
- the operator has authority to act on the artefact (write access, sign-off rights).
- a named consumer exists for the output.
- an auditable source-of-truth is available for invoice + contract inputs.

## Skip If (ANY kills it)

- one-off, never-to-repeat work — methodology overhead does not pay back.
- no named consumer — the artefact will be orphaned.
- cannot access invoice / contract source-of-truth — paraphrased substitutes are worse than skipping.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/` | parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the checklist artefact + valid/invalid/forbidden examples | 900 |
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
| `templates/freelancer-payment-chase-script-library.md` | Working checklist skeleton with 5-line header |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-payment-chase-script-library.py` | Validate the checklist artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[freelancer-rate-raise-letter-template]]
- [[graceful-offboard-script]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
