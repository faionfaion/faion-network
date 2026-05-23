# AI Research Tools Selection Map

## Summary

**One-sentence:** Selection map of concrete AI research tools (Perplexity, Elicit, Consensus, Scite, NotebookLM) matched to research-task shape, evidence requirements, and budget.

**One-paragraph:** Selection map of concrete AI research tools (Perplexity, Elicit, Consensus, Scite, NotebookLM) matched to research-task shape, evidence requirements, and budget. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Швидко обрати правильний tool під конкретне завдання дослідження.
- Перевірка ground-truth: Consensus / Scite з citation graph + study design.
- Synthesis над завантаженими джерелами: NotebookLM замість 'все в Claude'.
- Live market data + funding rounds: Perplexity Pro з recency filter.

## Applies If (ALL must hold)

- Завдання дослідження є чітким (research question + evidence type).
- Бюджет на subscription ($20-200/міс) АБО free-tier достатній.
- Час < 1 день на висновок — не повний systematic review.

## Skip If (ANY kills it)

- Внутрішні документи / приватні дані — потрібен RAG, не загальний tool.
- Open-ended exploration без research question — Brainstorm спочатку.
- Systematic review або PhD-level rigour — потрібен PRISMA, не AI shortcut.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| research question | one sentence | PI / PM |
| evidence type | one of {market data, scientific claim, opinion, summary} | research lead |
| budget | USD/mo | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-research-tool-categories]] | tool categories taxonomy loaded |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure (input/action/output/decision-gate) | 900 |
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
| `templates/research-decision.md` | Human-readable decision record |
| `templates/decision.json` | Machine-readable decision matching schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-research-tools.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[ai-research-tool-categories]]
- [[perplexity-ai-research]]
- [[market-sizing-with-ai]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Is there a sharp research question with a defined evidence_type?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
