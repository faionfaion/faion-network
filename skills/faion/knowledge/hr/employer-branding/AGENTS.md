# Employer Branding

## Summary

**One-sentence:** Strategy + execution for an employer brand (Glassdoor, LinkedIn, careers page, testimonials, content calendar) where every external asset traces to a named EVP pillar.

**One-paragraph:** Strategy + execution for an employer brand (Glassdoor, LinkedIn, careers page, testimonials, content calendar) where every external asset traces to a named EVP pillar. The methodology codifies the rules, output contract, and decision tree so two operators applying it independently produce comparable artefacts. Output is a versioned spec artefact a downstream agent or human reviewer can sign off without re-deriving the rationale.

**Ефективно для:**

- annual / quarterly employer-brand audit — scrape reviews, benchmark vs competitors.
- 4-12 week content calendar across LinkedIn, Instagram, careers blog.
- employee testimonials with quote attribution + redacted PII per legal.
- Glassdoor / Indeed review response within 48h SLA.
- talent community nurturing з rejected-but-strong кандидатами.

## Applies If (ALL must hold)

- annual or quarterly employer-brand audit: scrape reviews, benchmark vs. competitors, identify perception-reality gaps.
- producing a 4-12 week content calendar across LinkedIn, Instagram, careers blog.
- drafting and rotating employee testimonials from employee-supplied raw material.
- monitoring and responding to Glassdoor/Indeed/Comparably reviews within 48h SLA.

## Skip If (ANY kills it)

- no EVP or culture document exists — do `employee-value-proposition` methodology first.
- crisis comms (layoffs, PR incident) — switch to crisis-communication workflow.
- highly regulated industries where every external post requires compliance review before publication.
- sub-30-employee companies — the founder's voice is the brand.

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
| `templates/employer-branding.md` | Working spec skeleton with 5-line header |
| `templates/_smoke-test.md` | Minimum viable filled-in version for smoke testing |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-employer-branding.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[employee-value-proposition]]
- [[30-60-90-day-plan]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (presence of named consumer, scope cap, prior artefact, regulatory context) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
