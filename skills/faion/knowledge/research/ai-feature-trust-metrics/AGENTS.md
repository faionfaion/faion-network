# AI-Feature Trust Metrics for Market Research

## Summary

**One-sentence:** Defines instrumentable trust metrics for an AI feature (perceived accuracy, transparency, recovery, fairness) and how to measure them via in-product probes + survey deltas.

**One-paragraph:** Defines instrumentable trust metrics for an AI feature (perceived accuracy, transparency, recovery, fairness) and how to measure them via in-product probes + survey deltas. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Запускаєш AI-фічу і потрібна trust-baseline до GA (vs post-launch noise).
- Instrumentable signals: thumbs, regen rate, undo rate, hover-on-citation rate.
- Survey deltas Likert до/після для perceived accuracy + fairness.
- Trust dashboard разом з product KPIs — щоб не вибирати між adoption та trust.

## Applies If (ALL must hold)

- AI-фіча у production або pre-GA з ≥100 unique users/week.
- Instrumentation pipeline (PostHog, Mixpanel) уже стоїть.
- Доступний канал для micro-surveys (1-2 пит/тиждень).

## Skip If (ANY kills it)

- Pre-prototype без real users — trust signals шум.
- Закрита B2B з 5 користувачами — на 1-1 інтерв'ю краще.
- AI-фіча без user-facing output (silent ranking) — нічого міряти.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| feature spec | PRD with AI section | PM |
| instrumentation map | events emitted by the feature | analytics |
| baseline survey results | CSV pre-launch | research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-native-product-development]] | AI-feature ops in place |

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
| `templates/trust-rubric.yaml` | Per-feature trust rubric |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-feature-trust-metrics.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[ai-native-product-development]]
- [[ai-research-tools]]
- [[interview-note-synthesis-ai]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Is the feature live with WAU >= 100 and instrumentation pipeline?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
