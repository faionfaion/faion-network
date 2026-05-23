# Facilitation Anti-Patterns

## Summary

**One-sentence:** Rubric of six facilitation anti-patterns BA workshops must catch in real time, with detection cues + named counter-moves that defuse without humiliation.

**One-paragraph:** Facilitation Anti-Patterns pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- Cross-org elicitation workshops with sponsor + delivery + compliance.
- Discovery workshops where every minute is funded by a fixed-bid budget.
- Decision workshops where the deliverable is contractual (SoW change, design freeze).
- Retrospectives where psychological safety is fragile.

## Applies If (ALL must hold)

- BA facilitates synchronous workshops (elicitation, design, retro) with mixed stakeholders.
- At least one workshop has produced a deliverable later disputed as 'not what we agreed'.
- Sponsors and contributors are in the same room (or call) with material power asymmetry.
- There is a deliverable (BPMN, requirements, decision-record) on the line per session.

## Skip If (ANY kills it)

- Workshop is an informal brainstorm with no deliverable target.
- Group is fully peer (no sponsor / HiPPO present).
- Session is asynchronous only — anti-patterns are different there.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workshop agenda | markdown | BA prep doc |
| Participant role map | yaml | Stakeholder register |
| Decision template | markdown | BA toolkit |
| Recording consent | markdown | Legal / participants |

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
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-facilitation-anti-patterns` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/facilitation-anti-patterns.md` | Markdown rubric template with scoring axes + thresholds |
| `templates/facilitation-anti-patterns.schema.json` | JSON Schema for the structured rubric output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-facilitation-anti-patterns.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
