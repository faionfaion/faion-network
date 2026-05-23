# Agency Contractor JD Template

## Summary

**One-sentence:** Outcomes-based contractor JD for micro-agencies; explicit deliverables, paid-trial gate, IP clause, payment cadence — not a full-time JD with 'contract' relabeled.

**One-paragraph:** Outcomes-based contractor JD for micro-agencies; explicit deliverables, paid-trial gate, IP clause, payment cadence — not a full-time JD with 'contract' relabeled. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned spec artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- micro-agency наймає contractor під real-client deliverable.
- JD — outcomes-based, не «responsibilities» список FT-style.
- paid-trial gate + acceptance criteria → no 6-week funnel.
- IP clause explicit з day 0 (work-for-hire + assignment).
- payment cadence + scope-change clause inline → reduce dispute risk.

## Applies If (ALL must hold)

- you are starting a new instance of the artefact addressed (kickoff, contract, brief, deck).
- the instance has a named owner and a target review date.
- filled fields will be read by humans outside the author's team.
- sensitive data is captured but redacted before broad sharing.

## Skip If (ANY kills it)

- first instance ever, no comparable past work — write freeform, extract a template after.
- one-off bespoke artefact (M&A, lawsuit) — template constrains the wrong axes.
- localized cultural or regulatory context the template does not encode.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering activity context | recent notes / tickets | operator's inbox / ticket tracker |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/comms/hr-recruiter/` | parent domain context (vocabulary, neighbouring methodologies) |

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
| `templates/agency-contractor-jd-template.md` | Working spec skeleton with 5-line header |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-contractor-jd-template.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[contractor-audition-flow]]
- [[contractor-onboarding-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
