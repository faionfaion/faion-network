# Ollama Setup and Model Management

## Summary

**One-sentence:** Installs Ollama and selects local models within RAM/VRAM constraints, producing a runbook that includes pulled models, quantisation choices, and HTTP endpoint smoke-test.

**One-paragraph:** Installs Ollama and selects local models within RAM/VRAM constraints, producing a runbook that includes pulled models, quantisation choices, and HTTP endpoint smoke-test. The methodology assumes the inputs in Prerequisites and produces a `config` artefact validated by `scripts/validate-ollama-setup-models.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** Developers setting up a local LLM workstation or laptop for offline experimentation and agent development.

## Applies If (ALL must hold)

- Data privacy requirements where no external API calls are permitted.
- Offline or air-gapped environments (IoT, edge, secure networks).
- High-volume classification or extraction tasks where zero marginal API cost matters.
- Development and testing — no API keys, no rate limits, no costs, no internet required.
- Custom fine-tuned models that must be deployed locally after training.

## Skip If (ANY kills it)

- Best-quality responses required — even largest local models (70B) trail frontier cloud models on complex reasoning.
- Hardware is unavailable: 7B needs 8GB VRAM or RAM; 70B needs 48GB — check before planning.
- Real-time latency requirements on small hardware — CPU inference is 5-20x slower than GPU.
- Multilingual tasks across more than 20 languages — local models lag cloud providers significantly.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[ollama-python-client]]` | Adjacent context the agent normally already has when this methodology fires. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules with rationale and source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples for the output artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix. | ~800 |
| `content/04-procedure.xml` | medium | Five-step procedure with decision-gates. | ~700 |
| `content/05-examples.xml` | medium | One end-to-end worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether the methodology applies, ending in rule refs. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-defaults` | sonnet | Bounded judgment from inputs. |
| `emit-config` | haiku | Template fill. |
| `validate-config` | haiku | Schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.yaml` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/config.yaml.tmpl` | YAML config skeleton with the required keys and bounded defaults. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ollama-setup-models.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[ollama-python-client]]
- [[ollama-deployment]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `ollama-setup-models` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
