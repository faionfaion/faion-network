# Freelancer Rate Raise Letter Template

## Summary

**One-sentence:** Battle-tested raise-announcement letter for retainer clients with grace-period framing — not a generic 'difficult-conversations' lecture.

**One-paragraph:** Battle-tested raise-announcement letter for retainer clients with grace-period framing — not a generic 'difficult-conversations' lecture. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned spec artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- quarterly rate review для retainer client.
- grace period framing замість «effective immediately».
- ціна обґрунтована value delta, не CPI.
- letter ships with churn-risk classifier (stay / negotiate / churn).
- post-letter follow-up на T+7 з конкретним path вперед.

## Applies If (ALL must hold)

- the triggering activity 'Quarterly rate adjustment review (role: p3-technical-freelancer)' shows up at least once per cycle.
- the operator has authority to act on the artefact.
- a named consumer exists for the output.
- an auditable source-of-truth (current rate, value delta) is available.

## Skip If (ANY kills it)

- one-off, never-to-repeat work — overhead does not pay back.
- no named consumer — the artefact will be orphaned.
- cannot access the source-of-truth — paraphrased substitutes are worse than skipping.

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
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the spec artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One worked example end-to-end | 800 |
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
| `templates/freelancer-rate-raise-letter-template.md` | Working spec skeleton with 5-line header |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-rate-raise-letter-template.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[freelancer-payment-chase-script-library]]
- [[graceful-offboard-script]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
