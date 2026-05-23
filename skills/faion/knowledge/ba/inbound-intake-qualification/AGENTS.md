# Inbound Intake Qualification

## Summary

**One-sentence:** Five-question qualification rubric for inbound consulting leads: budget, decider, timeline, scope clarity, fit; emits qualify / reject / discovery-call routing.

**One-paragraph:** Inbound Intake Qualification pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- Solo consultant scaling lead volume past manual triage.
- Boutique agency owner protecting senior BA time.
- Inbound surge after a public talk / blog post / product launch.
- Switch from referral-only to paid-channel inbound.

## Applies If (ALL must hold)

- Solo BA / consultant receives at least 5 inbound leads per month.
- Lead quality is mixed — some convert, many waste discovery-call time.
- Engagement model is fixed-bid or T&M with a minimum.
- You have a CRM (or spreadsheet) where leads are tracked.

## Skip If (ANY kills it)

- Pure referral pipeline — every lead is pre-qualified by the referrer.
- Lead volume below 1/month — manual judgement is faster than a rubric.
- You take every lead regardless of fit (volume strategy).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inbound lead record | form submission / email | Website / inbox |
| Service catalogue | markdown | Your offering doc |
| Minimum engagement size | yaml | Your pricing model |
| Disqualification reasons log | csv | Prior leads |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-inbound-intake-qualification` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/inbound-intake-qualification.md` | Markdown rubric template with scoring axes + thresholds |
| `templates/inbound-intake-qualification.schema.json` | JSON Schema for the structured rubric output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-inbound-intake-qualification.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
