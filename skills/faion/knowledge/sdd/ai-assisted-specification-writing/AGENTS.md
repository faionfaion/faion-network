# AI-Assisted Specification Writing

## Summary

**One-sentence:** Drafts a spec.md from product context using an LLM, with mandatory human review gates at structure / acceptance criteria / edge cases.

**One-paragraph:** AI-Assisted Specification Writing produces a spec that fixes a recurring decision in the sdd domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Швидкий чорновий spec.md з product context.
- Refine acceptance criteria за RAG-evidence з минулих фічей.
- Edge-case enumeration: LLM пропонує, людина фільтрує.
- Translation: product brief → SDD spec у фіксованому шаблоні.
- Onboarding: junior учить, як виглядає робочий spec.

## Applies If (ALL must hold)

- Product context (problem statement, persona, hypothesis) is documented.
- Team uses the SDD spec.md template as canonical.
- Human reviewer is available to gate AC and edge cases.

## Skip If (ANY kills it)

- Product context is undocumented — write the brief first.
- Spec must be authored by a specific human for regulatory reasons.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product brief | Markdown | PM |
| Persona summary | Markdown | researcher |
| Hypothesis register | JSON | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-assisted-specification-writing (sdd-planning)]] | planning-layer counterpart for plan output |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/05-examples.xml` | supplemental | One worked example end-to-end | 400 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ai-assisted-specification-writing` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | SDD spec.md skeleton with all required sections |
| `templates/spec-prompt.md` | LLM prompt template + reviewer checklist |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-assisted-specification-writing.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[definition-of-done-multi-role]]
- [[internal-rfc-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
