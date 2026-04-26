# Guardrails Basics

## Summary

Safety mechanisms that validate, filter, and constrain LLM inputs and outputs. Layers checks from fastest to slowest: length/regex → moderation API → LLM intent classifier. Applies to both input (before LLM call) and output (after LLM call) paths.

## Why

LLM applications face prompt injection, PII leakage, harmful content generation, and topic drift. A single guardrail layer is insufficient — adversarial inputs circumvent any single check. Defense-in-depth with ordered layers (microsecond regex first, 300–800ms LLM classifier last) catches most attacks while minimizing latency impact.

## When To Use

- Production user-facing chatbots accepting untrusted input
- Regulated industries (healthcare, finance, legal) with compliance requirements
- Multi-tenant apps where tenant input must not influence another tenant's context
- System prompts contain instructions that must not be extracted via prompt injection
- Content generation pipelines where output quality and format must be validated before delivery

## When NOT To Use

- Internal developer tooling with no external users — guardrails add latency and maintenance cost without benefit
- Prototype/PoC stage — implement before production, not before demo
- Red-teaming or security research that explicitly needs adversarial output generation
- Output format validation only (JSON schema) — use structured output mode in the LLM API instead, it's lighter

## Content

| File | What's inside |
|------|---------------|
| `content/01-input-guardrails.xml` | Input validation, PII detection/redaction, prompt injection detection patterns |
| `content/02-output-guardrails.xml` | Content moderation (OpenAI API), intent classification, layered check ordering |

## Templates

| File | Purpose |
|------|---------|
| `templates/input-guardrails.py` | `InputGuardrails` + `PromptInjectionDetector` class templates |
| `templates/layered-check.py` | Ordered fast-to-slow check function (≤25 lines) |

## Scripts

none
