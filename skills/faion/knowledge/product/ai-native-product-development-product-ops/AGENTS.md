# AI-Native Product Development Operating Model

## Summary

**One-sentence:** Restructures product discovery, delivery, and ops around AI as a first-class material — eval-driven specs, prompt versioning, guardrail review, and dual-loop telemetry (model + product).

**One-paragraph:** Restructures product discovery, delivery, and ops around AI as a first-class material — eval-driven specs, prompt versioning, guardrail review, and dual-loop telemetry (model + product). The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Команда переходить від 'AI-фіча' до 'AI-native product' з eval-first циклом.
- Промпт-версіонінг + diff review нарівні зі звичайним кодом.
- Guardrail review board перед production-rollout AI-функцій.
- Telemetry два контури: model metrics (faithfulness, refusal) + product metrics (retention, NPS).

## Applies If (ALL must hold)

- Продукт має ≥1 LLM-фічу в production АБО планує її в наступні 30 днів.
- Команда ≥3 людей (product/eng/ux) — потрібна формалізація процесу.
- Бюджет на eval automation + observability (~$5k/мес мінімум).

## Skip If (ANY kills it)

- Static rule-based product без LLM — overkill.
- Solo prototype фази discovery — застосовувати після першого користувача.
- B2C з низькою stakes per query і без compliance вимог.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| product spec | Markdown PRD with AI-feature section | product manager |
| eval set | JSONL questions+expected outputs | QA / ML eng |
| guardrail policy | YAML allow/deny list | trust & safety |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-feature-trust-metrics]] | trust metric definitions agreed |

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
| `templates/ai-feature-prd.md` | AI-feature PRD skeleton with eval + guardrail sections baked in |
| `templates/guardrail-review-checklist.yaml` | Reviewable guardrail checklist with sign-off slots |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-native-product-development.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[ai-feature-trust-metrics]]
- [[rag-eval-strategy]]
- [[vendor-evaluation-scorecard]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Does the feature include LLM/AI behavior in production?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
