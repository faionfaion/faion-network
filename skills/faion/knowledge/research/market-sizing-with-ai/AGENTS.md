# Market Sizing with AI Research Tools

## Summary

**One-sentence:** Three-method market sizing (top-down, bottom-up, value-theory) using AI tools for source gathering with citation-backed estimates and reconciliation across the three methods.

**One-paragraph:** Three-method market sizing (top-down, bottom-up, value-theory) using AI tools for source gathering with citation-backed estimates and reconciliation across the three methods. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Швидкий TAM/SAM/SOM для pitch deck або quarterly planning.
- Three-method triangulation (top-down, bottom-up, value-theory).
- Citation-backed з recency filter — без 2022 чисел у 2026 звіті.
- Reconcile differences explicit — не вибираєш зручніший number.

## Applies If (ALL must hold)

- Потрібен TAM/SAM/SOM з citations за 1-3 дні (не консультантський звіт за тижні).
- Доступний Perplexity Pro або similar tool з recency filter.
- Stakes ≥ $50k decision (investor pitch, hiring plan, market entry).

## Skip If (ANY kills it)

- PhD-rigour systematic market study — потрібен McKinsey / Gartner, не AI shortcut.
- Niche ринок без публічних чисел — bottom-up з 1-1 інтерв'ю краще.
- Внутрішнє planning без external comm — груба оцінка достатня.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| market definition | one paragraph — what counts in/out | PM |
| year horizon | int (e.g. 2026) | strategy |
| currency | ISO 4217 | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-research-tools]] | tool selection decided |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure (input/action/output/decision-gate) | 900 |
| `content/05-examples.xml` | essential | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule in 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| classify-input | sonnet | Light judgment; identifies branch in decision tree. |
| draft-output | sonnet | Drafting the output artefact per schema. |
| validate-output | haiku | Mechanical schema validation via script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/market-sizing-report.md` | Final report skeleton with three estimates + reconciliation |
| `templates/market-sizing.json` | Machine-readable estimate matching schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-market-sizing-with-ai.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[ai-research-tools]]
- [[perplexity-ai-research]]
- [[ai-research-tool-categories]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Are stakes >= $10k AND public market figures exist?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
