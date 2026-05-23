# Perplexity AI Research Workflow

## Summary

**One-sentence:** Decompose-execute-synthesize Perplexity Pro Search workflow: atomic sub-queries, recency filters, per-claim confidence ratings, and human verification before publication.

**One-paragraph:** Decompose-execute-synthesize Perplexity Pro Search workflow: atomic sub-queries, recency filters, per-claim confidence ratings, and human verification before publication. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Compound research question → атомарні sub-queries по одному факту.
- search_recency_filter='year' проти 2022-числен у 2026 звіті.
- Confidence H/M/L per claim з кількості та якості джерел.
- Human verification gate ДО downstream pipeline — без auto-publish.

## Applies If (ALL must hold)

- Питання вимагає live web data (post-cutoff events, current prices).
- ≥5 web sources потрібно synthesizувати з citations.
- Доступний Perplexity Pro API key АБО web UI з sonar-pro моделлю.

## Skip If (ANY kills it)

- Питання має одне authoritative джерело — fetch напряму.
- Confidential competitive research — leaks query intent через Perplexity сервери.
- Reasoning task — Perplexity retrieves, не reasons.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| research question | compound question, may have sub-parts | PI |
| Perplexity API key | env var PPLX_API_KEY | secrets |
| budget cap | USD/run | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-research-tools]] | Perplexity confirmed as the right tool |

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
| `templates/research-report.md` | Final research report skeleton |
| `templates/perplexity_research.py` | Runnable Perplexity batch caller |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-perplexity-ai-research.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[ai-research-tools]]
- [[ai-research-tool-categories]]
- [[market-sizing-with-ai]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Does the question need live web data with citations?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
