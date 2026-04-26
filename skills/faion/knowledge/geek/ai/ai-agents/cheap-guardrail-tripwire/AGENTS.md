# Cheap-Guardrail Tripwire Before Expensive Agent

## Summary

Run an `input_guardrail` (or equivalent pre-agent classifier) on a small/fast model — gpt-4o-mini, Haiku 4.5, gemini-flash-lite — BEFORE the main agent ever sees the request. The guardrail returns a structured verdict; if it sets `tripwire_triggered=True` (or its equivalent), the SDK raises an exception and the expensive agent loop is never invoked. Off-topic, jailbreak, abuse, and spam traffic short-circuit at ~1% of the cost of running the strong model. The guardrail itself must be one cheap call returning a typed schema — never a tool-using sub-agent.

## Why

Most production agents on Opus/GPT-5/o3 are dominated by adversarial or off-topic traffic — public endpoints commonly see 30-70% of requests that should never reach the strong model (jailbreaks, off-topic chat, repeated abuse, malformed inputs). The OpenAI Agents SDK ships `input_guardrails` and `output_guardrails` exactly for this; a tripwire raises `InputGuardrailTripwireTriggered` synchronously, costing zero tokens on the main model and zero side-effects from tool calls. Effective cost reduction is 10-100× on filtered traffic and the latency added by a Haiku-class call (~200ms) is negligible compared to the multi-second strong-model loop it prevents.

## When To Use

- Public-facing endpoints exposed to internet traffic (chatbots, support bots, search assistants).
- Any agent on a premium model where >10% of inputs are filterable cheaply (PII, off-topic, jailbreak, abuse).
- Policy enforcement that must run before any tool call has side effects (refund agents, write-capable agents, code-execution agents).
- High-volume APIs where a 1% cost reduction translates to material savings.

## When NOT To Use

- Internal pipelines with trusted callers — guardrail latency and complexity outweigh near-zero filter rate.
- Per the user's NERO rule: never downgrade the user's own LLM calls inside NERO to save cost — this pattern is for THIRD-PARTY products, not Ruslan's personal agents.
- Output guardrails on streaming responses — buffering the full response to classify breaks streaming and harms UX (open Agents SDK issue #495).
- Tasks where the cheap classifier's confidence is poorly calibrated for your domain — it will false-positive and reject legitimate traffic.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tripwire-rule.xml` | The rule: tripwire = cheap structured-output classifier raising before main agent; how to wire it in OpenAI Agents SDK and Anthropic. |
| `content/02-anti-patterns.xml` | Antipatterns: tool-using guardrail, output-guardrail-on-stream, guardrail using same model as the main agent. |

## Templates

| File | Purpose |
|------|---------|
| `templates/input_guardrail.py` | OpenAI Agents SDK `input_guardrail` decorator with a Pydantic verdict schema and a Haiku/mini-model classifier. |
