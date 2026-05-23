---
slug: vendor-evaluation-scorecard
tier: geek
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Scorecard rubric for choosing AI vendors (LLM, vector DB, eval, observability) across quality, cost, lock-in, security, and SLA — produces a comparable score + decision artefact.
content_id: "a02b0892da1f8e61"
complexity: medium
produces: rubric
est_tokens: 4300
tags: [vendor-evaluation, rubric, ai-tooling, lock-in, procurement]
---
# Vendor Evaluation Scorecard for AI Tooling

## Summary

**One-sentence:** Scorecard rubric for choosing AI vendors (LLM, vector DB, eval, observability) across quality, cost, lock-in, security, and SLA — produces a comparable score + decision artefact.

**One-paragraph:** Scorecard rubric for choosing AI vendors (LLM, vector DB, eval, observability) across quality, cost, lock-in, security, and SLA — produces a comparable score + decision artefact. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Обираєш LLM-провайдера між OpenAI / Anthropic / Bedrock з compliance + lock-in factor.
- Vector DB shortlist: Qdrant vs Weaviate vs Pinecone + self-host vs SaaS.
- Eval / observability tools (Braintrust, LangSmith, Helicone) — порівняння за єдиною rubric.
- Procurement gate: pricing tier vs scale; SLA + DPA + SOC2 obov'yazkovi для enterprise.

## Applies If (ALL must hold)

- ≥2 vendors під розгляд для тієї ж функції.
- Контракт > $5k/рік або production-залежність.
- Доступний technical contact зі сторони вендора для уточнень.

## Skip If (ANY kills it)

- Один вендор з якого вже залежиш і немає реальної alternative.
- Free-tier prototype без production планів.
- Sub-$1k purchase — overhead rubric > value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| vendor shortlist | list of ≥2 vendors + URLs | research |
| requirements | Markdown spec — must/should/nice | product |
| budget cap | USD/month | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-research-tools]] | shortlist informed by tool-categories scan |

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
| `templates/scorecard.md` | Human-readable scorecard with five-axis table |
| `templates/scorecard.json` | Machine-readable scorecard matching schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vendor-evaluation-scorecard.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[ai-research-tools]]
- [[ai-research-tool-categories]]
- [[ai-native-product-development]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Are there ≥2 realistic vendors AND contract value ≥ $1k/yr?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
