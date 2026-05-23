# ADR Consequence Evidence Binding

## Summary

**One-sentence:** Produces an ADR whose Consequences section is bound to measurable evidence (fitness function, KPI, test, log query) so the decision can be re-evaluated objectively.

**One-paragraph:** ADR Consequence Evidence Binding produces a decision-record that fixes a recurring decision in the sdd domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Архітектурне рішення з вимірюваним наслідком, не лише текстом.
- Decision re-evaluation: дивимось на binding evidence, а не memoir.
- ADR supersession detection: коли evidence показує, що рішення застаріло.
- Audit: regulator бачить cause→effect→evidence.
- Onboarding: junior читає ADR і одразу бачить, як його перевірити.

## Applies If (ALL must hold)

- Architectural decision has measurable consequences (latency, cost, error rate, complexity).
- Team has CI / monitoring capable of producing the evidence signal.
- Decision is expected to be re-evaluated at least once.

## Skip If (ANY kills it)

- Consequence is purely qualitative and cannot be measured.
- No CI / monitoring infrastructure exists to capture evidence.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Decision context | Markdown | architect |
| Measurable target list | JSON / Markdown | architect + dev lead |
| Evidence-source inventory | Markdown | DevOps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[adr-supersession-detection]] | evidence drives supersession detection |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-adr-consequence-evidence-binding` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ADR-evidence-template.md` | MADR-shape ADR template with evidence-binding section |
| `templates/evidence-anchor.schema.json` | JSON Schema for a single evidence-anchor entry |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-adr-consequence-evidence-binding.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[adr-supersession-detection]]
- [[architecture-repo-scaffolding-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
