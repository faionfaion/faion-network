# Prompt Basics

## Summary

Core prompt engineering patterns: zero-shot, few-shot, chain-of-thought, self-consistency, and ReAct. The `PromptTemplate` dataclass encapsulates system prompt, user template with variables, and optional few-shot examples. The core rule: store prompt templates as code constants (not runtime strings) — this enables `git diff` on prompt changes and catches silent regressions when model versions update.

## Why

Inconsistent LLM outputs in production almost always trace to vague task descriptions, missing output format instructions, or undisciplined prompt construction. Structured templates with explicit role, constraints, and format instructions cut output variance without fine-tuning. Prompt injection via user-supplied content overrides system constraints without sanitization — a structural vulnerability, not a prompt-quality problem.

## When To Use

- Any pipeline step requiring consistent, parseable LLM output
- Before investing in fine-tuning — prompt engineering resolves most output consistency issues
- When agent inner-loop outputs are unreliable or hallucinating
- Setting up few-shot examples to teach a model a new output schema
- Encoding role, constraints, and output format into a reusable `PromptTemplate`

## When NOT To Use

- When task complexity genuinely requires multi-step reasoning — use Chain-of-Thought or ReAct instead
- When output schema must be guaranteed — use Structured Outputs with Pydantic
- When token budget is the bottleneck — elaborate system prompts eat context; prefer short system + structured output enforcement

## Content

| File | What's inside |
|------|---------------|
| `content/01-prompt-template.xml` | PromptTemplate class, zero-shot and few-shot patterns, format() method, usage examples |
| `content/02-system-prompts.xml` | System prompt patterns (assistant, code expert, data analyst, editor), create_system_prompt() builder |
| `content/03-advanced-patterns.xml` | Role-based expert prompt, structured output prompting with Pydantic schema, CoT and ReAct patterns |
| `content/04-checklist.xml` | Checklist for system prompt design, zero-shot, few-shot, CoT, constraint definition, testing iteration |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-template.py` | PromptTemplate dataclass with few-shot support and render() method |
| `templates/build-system.py` | build_system() helper that composes role + constraints + output format into a system prompt string |
