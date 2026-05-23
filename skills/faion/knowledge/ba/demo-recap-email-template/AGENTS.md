# Demo Recap Email Template

## Summary

**One-sentence:** Sprint-demo recap email skeleton that pins decisions made, scope deltas, open items, and named follow-ups so the client cannot retroactively reinterpret the demo.

**One-paragraph:** Demo Recap Email Template pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- Outsource sprint demos with foreign clients (timezone + language asymmetry).
- Fixed-bid engagements where scope drift bleeds margin.
- Hand-off windows when delivery BA differs from sales BA.
- Regulated engagements that need an audit trail of every shown feature.

## Applies If (ALL must hold)

- Outsource / consultancy BA runs client demos at least once per sprint.
- The client and the delivery team are in different organisations / legal entities.
- There is a recurring pattern of post-demo scope drift or 'I thought you said' disputes.
- You have email + ticket-system access for follow-up assignment.

## Skip If (ANY kills it)

- In-house team where demos are informal stand-up walkthroughs with no scope-creep risk.
- Demo is a one-off pitch where no follow-up exists.
- Client refuses written records — engagement risk dwarfs methodology benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Demo agenda | markdown | BA pre-demo prep doc |
| Demo recording / transcript | mp4 / txt | Zoom / Meet / Teams |
| Live-decision log | markdown | Facilitator notes during demo |
| Prior recap thread | email / doc | Last sprint's recap email |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source + skip rule | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-demo-recap-email-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/demo-recap-email-template.md` | Markdown spec skeleton with required sections + placeholders |
| `templates/demo-recap-email-template.schema.json` | JSON Schema for the structured spec output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-demo-recap-email-template.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
