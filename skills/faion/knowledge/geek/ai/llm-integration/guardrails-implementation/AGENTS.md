# Guardrails Implementation

## Summary

Complete implementation patterns for guardrails pipelines that validate, sanitize, and filter LLM inputs and outputs. Covers the `GuardrailsPipeline` class, output validation, hallucination detection via a second LLM call, PII scrubbing, prompt-injection detection, and the `guardrails-ai` library. The core rule: layer defense — fast rule-based checks first, slow LLM-based checks only for high-stakes outputs.

## Why

Public-facing LLM applications receive adversarial input and must not relay toxic, hallucinated, or PII-laden content downstream. A pipeline with no guardrails silently passes policy violations, leaks credentials, and produces unauditable output. Guardrails add structured violation logging, per-category detection, and an audit trail — requirements in regulated industries and multi-agent pipelines where one agent's bad output becomes another's poisoned input.

## When To Use

- Public-facing applications where users may submit adversarial or off-policy input
- Regulated industries (healthcare, finance, legal) with compliance output requirements
- Multi-agent pipelines where one agent's output feeds another — prevent cascading bad data
- Any app storing or transmitting user content through an LLM
- Applications where hallucinated facts could cause real harm (medical advice, legal citations)

## When NOT To Use

- Internal developer tools where all users are trusted — guardrails add latency and cost for no benefit
- Pure text transformation (translation, summarization of provided text) — hallucination guardrails irrelevant
- Prototype/PoC stages — implement before production, not during exploration
- When the guardrail check itself calls an LLM and latency budget is under 500ms — use rule-based checks only

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline.xml` | GuardrailsPipeline architecture, GuardrailConfig/GuardrailResult dataclasses, input and output processing steps, async variant |
| `content/02-validators.xml` | OutputGuardrails validator/filter pattern, common validators (profanity, JSON, length), HallucinationDetector LLM-based check |
| `content/03-checklist.xml` | Implementation checklist: framework setup, custom validators, production hardening, testing |
| `content/04-antipatterns.xml` | Key antipatterns: silent exception swallowing, running hallucination detection synchronously, trusting inter-agent messages implicitly |

## Templates

| File | Purpose |
|------|---------|
| `templates/guardrails-pipeline.py` | Production-ready GuardrailsPipeline class with GuardrailConfig and GuardrailResult |
| `templates/moderate-input.py` | Minimal fast input moderation combining rule-based injection check and OpenAI Moderation API |
