# Custom LLM Guardrails Pipeline

## Summary

**One-sentence:** Builds a custom Python guardrails module (PIIDetector + PromptInjectionDetector + ContentModerator + HallucinationDetector) wired as a tiered pipeline with `process_input` / `process_output` / `run` entry points.

**One-paragraph:** When NeMo and Guardrails AI are too opinionated or too heavy, the custom path is a four-component Python module with explicit tier ordering: regex-based PII masking, compiled regex injection patterns, OpenAI moderation API, and LLM-as-judge hallucination check. Composed into `GuardrailsPipeline` with `process_input → call_llm → process_output`. Returns a typed `GuardrailResult` with `is_safe`, `violations[]`, and pre/post snapshots. Output of this methodology is the working code skeleton, not a plan.

**Ефективно для:**

- Тіньові stack-и (FastAPI / LangChain / LlamaIndex) — guardrails встромляєш як middleware, без зайвої залежності.
- Tight latency budget — кожен tier під твоїм контролем, можна вимикати дорогі по конфігу.
- Specific business rules (валюти, регуляторні словники) — простіше написати свій regex, ніж навчати валідатор Guardrails Hub.
- Lightweight deploys (edge / serverless) — мінімум залежностей, мінімум cold-start.

## Applies If (ALL must hold)

- Plan from `guardrails-concepts` declares `framework=custom` for at least one rail.
- Team owns Python stack and can maintain regex + API integration code.
- Latency budget requires per-tier short-circuit (one framework can't tune granularly enough).

## Skip If (ANY kills it)

- Multi-turn dialog control needed — NeMo Colang is purpose-built; building it from scratch is years of work.
- Team wants validator library iteration — Guardrails Hub ecosystem is faster than custom regex.
- Plan picked `framework=nemo` or `guardrails-ai` for all rails — no custom code needed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `guardrail-plan.json` | JSON | `guardrails-concepts` methodology output |
| Python ≥ 3.11 stack | runtime | project requirements |
| OpenAI API key (for moderation + judge) | env var | secrets manager |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `guardrails-concepts` | Defines which rails go into custom layer vs other frameworks. |
| `prompt-injection-defense` | Source of injection regex patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: 4-component split, regex-only-tier1, async-where-independent, none-means-block, typed-result, tiered-short-circuit | 1100 |
| `content/02-output-contract.xml` | essential | Schema for `GuardrailResult` (Python dataclass + JSON shape) | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: blocking-sync-await, leaky-pii-regex, judge-on-every-call, no-config-toggle | 800 |
| `content/04-procedure.xml` | essential | 7-step build procedure: detectors → moderator → judge → config → pipeline → middleware → smoke-test | 900 |
| `content/05-examples.xml` | essential | End-to-end FastAPI integration with config and middleware | 600 |
| `content/06-decision-tree.xml` | essential | Component-inclusion decision tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold_module` | haiku | Template-fill from skeleton; deterministic. |
| `tune_regex_set` | sonnet | Pattern coverage needs reasoning over threat list. |
| `review_security` | opus | Adversarial review; injection bypass surface; cost justified. |

## Templates

| File | Purpose |
|------|---------|
| `templates/guardrails_pipeline.py` | Full pipeline class skeleton |
| `templates/_smoke-test.py` | Minimum runnable end-to-end test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-guardrails-custom-pipeline.py` | Validate produced `GuardrailResult` JSON against the schema | After integration test; pre-deploy gate |

## Related

- [[guardrails-concepts]] — plan that picks `custom` for the rail
- [[guardrails-testing]] — adversarial harness this pipeline must survive
- [[prompt-injection-defense]] — pattern library this pipeline imports

## Decision tree

See `content/06-decision-tree.xml`. Branches on data sensitivity (PII y/n), trust boundary (external users y/n), and latency budget. Leaves toggle component flags in `GuardrailConfig`.
