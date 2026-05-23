# Synthetic Users

## Summary

**One-sentence:** Generates a labelled synthetic-user response panel for directional hypothesis triage, always followed by real-user validation before any product decision.

**One-paragraph:** Synthetic Users produces a report that fixes a recurring decision in the research domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Тригер гіпотез: швидко відкинути ідеї до того, як вкладати тиждень у живі інтерв'ю.
- Стрес-тест опитувальника: знайти неоднозначні питання до польового запуску.
- Edge-case probing: змусити персон вигадувати adversarial відповіді.
- Briefing baseline: чорнова рамка дослідження, яку коректує живий researcher.
- Pre-mortem на концепт: 'що б сказала особа X на цю фічу?'

## Applies If (ALL must hold)

- Early ideation: directional signal needed before real users can be recruited.
- Hypothesis stress-testing as a fast pre-filter.
- Low-stakes concept validation where the cost of being wrong is recoverable.

## Skip If (ANY kills it)

- Go/no-go product decisions — synthetic data cannot replace real demand signal.
- Demand forecasting or pricing — synthetic willingness-to-pay is biased high.
- Final pre-launch validation — at least one real-user round is required.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Persona brief | Markdown | researcher |
| Survey instrument or interview guide | Markdown / JSON | researcher |
| Hypothesis register | JSON list | PM / researcher |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-persona-building]] | synthetic users consume persona profiles |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/05-examples.xml` | supplemental | One worked example end-to-end | 400 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-synthetic-users` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/synthetic-panel-report.md` | Markdown report skeleton with persona table + response panel + validation plan |
| `templates/synthetic-response.schema.json` | JSON Schema for an individual synthetic response row |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-synthetic-users.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[ai-persona-building]]
- [[ai-interview-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
