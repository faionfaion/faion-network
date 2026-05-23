# Cheap-Guardrail Tripwire Before Expensive Agent

## Summary

**One-sentence:** Runs an input_guardrail on a small/fast model (Haiku, gpt-4o-mini, gemini-flash-lite) BEFORE the expensive agent loop; off-topic/jailbreak/abuse short-circuits at ~1% of the strong-model cost.

**One-paragraph:** A non-trivial fraction of inbound requests to any agent are off-topic, jailbreak attempts, abuse, or spam. Running the expensive main agent on them is pure waste. This methodology wires a guardrail step: one cheap LLM call that returns a structured `{tripwire_triggered: bool, reason: enum, confidence: float}` verdict. If tripped, the SDK raises and the main agent never runs. The guardrail must be a single call returning a typed schema — not a tool-using sub-agent.

**Ефективно для:** Команд, у яких на проді 20-40% запитів — це шумовий трафік (off-topic, prompt-injection attempts); за 1% від ціни сильної моделі guardrail відсіює це до того, як головний agent взагалі стартує.

## Applies If (ALL must hold)

- Main agent uses a relatively expensive model (sonnet/opus or equivalent).
- A pre-classifier (off-topic / jailbreak / abuse) can produce useful signal on plain input.
- A small/fast model is available (Haiku 4.5, gpt-4o-mini, gemini-flash-lite).
- The SDK supports input-guardrail hooks (OpenAI Agents SDK input_guardrail, Anthropic equivalent, custom).
- False positives can be reviewed by a named owner.

## Skip If (ANY kills it)

- Main model is itself cheap (haiku); guardrail won't save enough to justify.
- Inputs are highly trusted (internal pipeline, no user-supplied text).
- Every request needs full agent reasoning (e.g. semantic search dispatch).
- Guardrail false-positive rate is unbounded — refusing valid users is worse than waste.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Main agent endpoint | callable | Eng |
| Cheap model SDK | Haiku/mini config | Provider catalogue |
| Guardrail verdict schema | JSON Schema | Tech lead |
| Calibration set | ~100 labelled examples (legit vs noise) | QA |
| Named owner | handle | Eng |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/refusal-field-strict-schema/AGENTS.md` | Verdict shape is a refusal-style strict schema. |
| `geek/ai/ai-agents/structured-output-mode-picker/AGENTS.md` | Strict-mode SO for the verdict. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: cheap model only, typed verdict, one call, FP review | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the verdict + the config | ~600 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: expensive main? → cheap available? → calibration? → install/skip | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `verdict_call` | haiku / mini | The whole point — cheap. |
| `tune_thresholds` | sonnet | Per-deployment calibration. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the verdict. |
| `templates/output.example.json` | Filled example. |
| `templates/input_guardrail.py` | Python skeleton for the guardrail call. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate verdict shape on every call. | Inline per verdict. |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer: [[refusal-field-strict-schema]] — verdict shape pattern.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) is the main model expensive? (2) is a cheap classifier model available? (3) is a calibration set ready? Leaves point to "install guardrail", "calibrate first", or "skip".
