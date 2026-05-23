# AI Research Tool Categories Taxonomy

## Summary

**One-sentence:** Taxonomy of AI research tool categories (live-web search, citation graphs, document Q&A, synthesis-over-uploaded-sources) with selection criteria and corpus-bias notes per category.

**One-paragraph:** Taxonomy of AI research tool categories (live-web search, citation graphs, document Q&A, synthesis-over-uploaded-sources) with selection criteria and corpus-bias notes per category. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Швидка orientation у landscape: live-web vs citation-graph vs document Q&A vs synthesis.
- Розуміння corpus bias кожної категорії (web bias, academic bias, vendor bias).
- Pre-condition before picking concrete tool — спочатку категорія, потім продукт.
- Бази навчання junior researchers щодо правильної tool-orientation.

## Applies If (ALL must hold)

- Новий research-проект і команді треба узгодити tool stack.
- Onboarding researcher має зрозуміти, що чим відрізняється.
- Аудит поточного workflow на corpus-bias gaps.

## Skip If (ANY kills it)

- Команда вже узгоджена на tool stack — категорії зайві.
- Single-shot research question — одразу до tool selection.
- Internal-only docs без зовнішніх джерел — таксономія не релевантна.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| research charter | one paragraph — scope and questions | research lead |
| current tool inventory | list of tools team uses | research ops |
| budget envelope | USD/mo | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| _none_ | This methodology does not require upstream context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
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
| `templates/categories.yaml` | Filled taxonomy ready for team adoption |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-research-tool-categories.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[ai-research-tools]]
- [[perplexity-ai-research]]
- [[market-sizing-with-ai]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Has the team already aligned on a research tool stack?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
