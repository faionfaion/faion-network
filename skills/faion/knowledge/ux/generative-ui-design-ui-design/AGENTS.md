# Generative UI Design

## Summary

**One-sentence:** Produces an ideation-phase UI spec from a feature brief by generating 5–10 layout variants (v0, Claude Artifacts, Galileo, Uizard, Relume) and selecting one for hand-off, with explicit not-production-ready labelling.

**One-paragraph:** Generative UI tools accelerate ideation and rapid prototyping but do not produce production-ready output. Claude Artifacts is the only agent-native path (agent generates inline, human reviews, agent iterates on feedback). This methodology produces an ideation spec with 5–10 generated variants, a selected layout, a refinement-required list, and a hand-off package marked not-production-ready so engineering does not consume it directly.

**Ефективно для:** PM / designer на ideation phase, що потребує 5–10 variants за день і refinement шлях до production.

## Applies If (ALL must hold)

- Pre-design ideation: generating 5–10 variants from a feature brief before any human design work.
- Stakeholder feedback needed on layout direction before committing design hours.
- Output is explicitly an ideation artefact, not a production handoff.

## Skip If (ANY kills it)

- Need production-ready output — generative UI is ideation-only.
- Brand-system constraint is rigid and generators do not honour tokens.
- Stakeholders expect generated output to ship as-is.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Feature brief | markdown | PM |
| Constraints (brand tokens, must-not-have) | JSON | design |
| Selected generators | list (v0 / artifacts / galileo / uizard / relume) | design |
| Stakeholder review channel | URL | ops |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[ai-design-assistant-patterns]] | Assistant pattern boundary. |
| [[ai-enhanced-design-systems]] | Token / DS constraint context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end. | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-spec` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/ideation-spec.json` | JSON skeleton: brief_id + variants + selection + rationale + refinement list. |
| `templates/generator-prompt.md` | Prompt skeleton with brand-token + must-not-have injection slots. |
| `templates/_smoke-test.json` | Filled checkout-redesign ideation spec. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-generative-ui-design.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[ai-design-assistant-patterns]]
- [[ai-enhanced-design-systems]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the spec; mis-routing leads to producing the wrong artefact shape.
