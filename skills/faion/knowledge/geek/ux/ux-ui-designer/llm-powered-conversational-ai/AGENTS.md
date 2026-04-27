# LLM-Powered Conversational AI

## Summary

Design and implementation methodology for conversational AI systems using LLMs — system prompt authoring with explicit topic boundaries, guardrail rules, fallback and escalation logic, and red-team testing for jailbreak vectors. Every production system prompt must define: allowed topics (list), forbidden topics (list), escalation triggers, and persona constraints.

## Why

LLMs handle multi-part and ambiguous queries that rule-based VUI cannot, but they hallucinate, drift from persona under adversarial input, and produce off-topic responses without guardrails. The methodology enforces the design decisions (topic scope, escalation, persona) that prevent these failure modes at deployment time rather than after user-visible incidents.

## When To Use

- Building a voice or chat assistant handling multi-part, ambiguous, or contextually dependent queries
- Replacing a rule-based IVR or FAQ bot where query diversity exceeds what a decision tree covers
- Designing a customer support agent that must maintain conversation history
- Integrating a conversational layer into an existing product (search, onboarding, help center)
- Prototyping dialogue flows before committing to a production NLU platform

## When NOT To Use

- Transaction-critical flows (payments, medical orders) without deterministic validation after each LLM turn
- Real-time phone IVR where latency >2s is unacceptable
- Regulated industries where every utterance must be pre-approved (financial advice, clinical diagnosis)
- Query space is small and fully enumerable — rule-based VUI is cheaper and more reliable
- Products without a moderation or content policy layer

## Content

| File | What's inside |
|------|---------------|
| `content/01-design-rules.xml` | System prompt structure rules, topic boundary requirements, guardrail patterns |
| `content/02-tools-and-gotchas.xml` | CLI tools, services, agent workflow, AI gotchas, best practices |

## Templates

| File | Purpose |
|------|---------|
| `templates/conversation-loop.py` | Minimal Anthropic SDK multi-turn conversation prototype |
| `templates/prompt-system-prompt-design.txt` | Agent prompt: generate production system prompt with guardrails and example dialogues |
| `templates/prompt-red-team.txt` | Agent prompt: red-team a system prompt for persona abandonment and data exfiltration |
