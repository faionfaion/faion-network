---
slug: guardrails-nemo
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a NeMo Guardrails config (`config.yml` + Colang flows + custom actions) covering input/jailbreak/topic/output/fact-check rails for a multi-turn dialog application.
content_id: "5d2a48631b723bc3"
complexity: deep
produces: config
est_tokens: 4500
tags: [nemo-guardrails, colang, dialog-control, nvidia, llm-safety]
---
# NeMo Guardrails — Colang Dialog Flow Control

## Summary

**One-sentence:** Writes a NeMo Guardrails config (YAML + Colang) with input rail (self-check + jailbreak + topic), output rail (self-check + fact-check), and custom Python actions registered via `rails.register_action()`.

**One-paragraph:** NeMo is the right answer when conversation state matters and dialog policy must be auditable. The Colang DSL defines user intents, bot canonical forms, and flows that wire them. Built-in rails (`check jailbreak`, `check facts`, `mask sensitive data`) cover hard cases; custom `@action()` Python functions handle business-specific checks. Output of this methodology is the `config/` directory: `config.yml` + `rails/*.co` + `actions.py` — ready to load via `RailsConfig.from_path("./config")`.

**Ефективно для:**

- Multi-turn flows (замовлення → статус → повернення) — стан між turns тримає Colang state machine, не твій код.
- Enterprise дзвінки де dialog policy має бути версійованою — Colang файли йдуть в git, ревʼюються як політики.
- RAG-системи з обовʼязковим fact-check — built-in `check facts` rail знімає галюцинації без зайвої логіки.
- Multi-agent — кожен агент має свій dialog rail, не лізе в чужий.

## Applies If (ALL must hold)

- Application has multi-turn conversational flows where state across turns drives policy.
- Python + LangChain / LlamaIndex stack already present; team can run an extra LLM call per turn for Colang runtime.
- Policy needs to be auditable / version-controlled outside application code.

## Skip If (ANY kills it)

- Single-turn API (`POST /generate` → response) — Colang overhead unjustified; use Guardrails AI.
- Output-validation only need (schema enforcement) — Guardrails AI lighter and more direct.
- Team has no NVIDIA infra or Python dialog expertise — setup cost too high.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `guardrail-plan.json` | JSON | `guardrails-concepts` (must have `framework=nemo` for at least one rail) |
| Conversation flow diagram | Markdown / state machine | product spec |
| Knowledge base (for fact-check) | local docs / vector DB | RAG setup |
| OpenAI / NIM model + key | env var | secrets manager |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `guardrails-concepts` | Plan declares which rails go to NeMo. |
| `llm-decision-framework` | Model selection drives the `models:` block in `config.yml`. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: config-from-path, separated-flows, canonical-intents, async-actions, register-before-generate, kb-grounded-facts | 1100 |
| `content/02-output-contract.xml` | essential | Schema for `config/config.yml` + Colang file structure + actions module | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: inline-config-prod, missing-canonical-examples, sync-action-blocks-loop, no-fact-check-on-rag | 800 |
| `content/04-procedure.xml` | essential | 7 steps: scaffold config dir → write Colang intents → wire flows → add jailbreak action → add fact-check action → register → smoke | 900 |
| `content/05-examples.xml` | essential | Worked example: support bot with order + refund flows | 600 |
| `content/06-decision-tree.xml` | essential | Rail-mix decision tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold_config_dir` | haiku | Templated layout; deterministic. |
| `write_colang_flows` | sonnet | DSL synthesis from flow diagram. |
| `tune_jailbreak_prompts` | opus | Adversarial; cost justified for high-stakes deployment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yml` | Models + rails YAML skeleton |
| `templates/rails-jailbreak.co` | Colang jailbreak flow skeleton |
| `templates/actions.py` | `@action()` Python skeleton |
| `templates/_smoke-test.py` | Minimum runnable smoke |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-guardrails-nemo.py` | Validate `config.yml` shape (models, rails.input.flows, rails.output.flows, prompts list) | Pre-deploy gate |

## Related

- [[guardrails-concepts]] — plan that picks NeMo
- [[guardrails-custom-pipeline]] — for the rails NeMo doesn't own
- [[guardrails-testing]] — adversarial harness

## Decision tree

See `content/06-decision-tree.xml`. Branches on flow complexity (single-turn / multi-turn / RAG) and policy auditability requirement.
