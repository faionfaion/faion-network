# Agent Integration — Guardrails Basics

## When to use
- Building a user-facing chatbot or LLM API endpoint that accepts untrusted input
- Regulated industry (healthcare, finance, legal) with compliance requirements for content filtering
- Multi-tenant applications where one tenant's input must not influence another's context
- The system prompt contains sensitive instructions that must not be extracted via prompt injection
- Content generation pipelines where output quality and format must be validated before delivery

## When NOT to use
- Internal developer tooling with no external users — guardrails add latency and maintenance cost for no benefit
- Prototype / proof-of-concept stage — implement guardrails before production, not before demo
- The task explicitly requires generating edge-case or adversarial content (red-teaming, security research) — guardrails block the legitimate use case
- You only need output format validation (JSON schema) — use structured output mode in the LLM API instead, which is lighter than a guardrail pipeline

## Where it fails / limitations
- Regex-based prompt injection detection has high false-positive rates; legitimate business prompts containing "ignore previous" (e.g., "ignore previous invoices") get flagged
- OpenAI Moderation API only covers English well; multilingual content has significantly higher false-negative rates
- Intent classification via LLM adds 300-800ms latency per request; not suitable for real-time streaming responses
- Guardrails that block on suspicion without logging the reason make debugging impossible — silent refusals frustrate users and operators
- Context-free guardrails fail on multi-turn conversations where harmful intent builds across several messages; each turn looks clean in isolation

## Agentic workflow
A subagent building a guardrail pipeline should layer checks from fastest to slowest: length → regex injection detection → moderation API → intent classification (LLM). Only escalate to the next layer if the previous layer passes. For output guardrails, the subagent should validate JSON schema compliance first, then run moderation on the generated text. Violations must be logged with the violation type, sanitized input, and timestamp — never log the raw blocked content.

### Recommended subagents
- `faion-sdd-executor-agent` — implement `InputGuardrails`, `PromptInjectionDetector`, `ContentModerator` as SDD tasks with test coverage for evasion patterns
- `password-scrubber-agent` — validate that PII detection patterns correctly redact test data before committing

### Prompt pattern
```
Classify the intent of this user message. Allowed topics: {allowed_topics}.
Return JSON: {"intent": "general|harmful|off_topic", "is_allowed": true/false, "confidence": 0.0-1.0}.
Message: {message}
```

```
You are a safety check agent. Given the following LLM output, check:
1. Does it contain PII (email, phone, SSN, credit card)?
2. Does it contain instructions for harmful activities?
Return JSON: {"is_safe": true/false, "violations": ["type1", "type2"]}.
Output: {llm_output}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pip install guardrails-ai` | Guardrails AI framework with validators | [guardrailsai.com](https://www.guardrailsai.com/) |
| `pip install nemo-guardrails` | NVIDIA NeMo Guardrails (flow-based) | [GitHub](https://github.com/NVIDIA/NeMo-Guardrails) |
| `pip install presidio-analyzer` | Microsoft Presidio PII detection | [GitHub](https://github.com/microsoft/presidio) |
| `pip install openai` | OpenAI Moderation API access | [pypi](https://pypi.org/project/openai/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Moderation API | SaaS | Yes | Free with OpenAI account; 11 harm categories; English-first |
| Guardrails AI | OSS | Yes | Python framework; validator hub; works with any LLM |
| NeMo Guardrails | OSS | Yes | Flow-based runtime; good for multi-turn conversation guardrails |
| Microsoft Presidio | OSS | Yes | PII detection + anonymization; multilingual; self-hostable |
| Lakera Guard | SaaS | Yes | Prompt injection detection API; low-latency (<100ms) |
| AWS Bedrock Guardrails | SaaS | Yes | Managed; integrates with Bedrock-hosted models only |

## Templates & scripts
See `templates.md` for `InputGuardrails`, `PromptInjectionDetector`, and `ContentModerator` class templates.

Inline layered check (≤25 lines):
```python
def check_input(text: str, detector, moderator, max_len: int = 4000) -> dict:
    """Run layered input checks, fast to slow."""
    if len(text) > max_len:
        return {"safe": False, "reason": "length_exceeded"}
    is_injection, _ = detector.detect(text)
    if is_injection:
        return {"safe": False, "reason": "prompt_injection"}
    mod = moderator.moderate(text)
    if mod["is_flagged"]:
        return {"safe": False, "reason": "moderation", "categories": mod["flagged_categories"]}
    return {"safe": True}
```

## Best practices
- Order guardrail checks by speed: regex/length (microseconds) → moderation API (50-200ms) → LLM classifier (300-800ms); fail fast
- Log every violation with type, user ID, and sanitized input (never raw); this data is required for both debugging and compliance audits
- Red-team your own guardrails quarterly; adversarial techniques evolve and static patterns become stale
- Separate input guardrails from output guardrails in the code; they have different failure modes and different on-call owners
- Avoid blocking users without explanation; return a generic refusal message that does not reveal which guardrail triggered (prevent fingerprinting the filter)

## AI-agent gotchas
- Prompt injection via tool results: if an agent fetches external data (web pages, database rows) and includes it in the next LLM call, the fetched content can contain injection payloads — run injection detection on all external data before it enters the context
- Multi-turn injection: a user spreading a harmful instruction across 5 harmless-looking turns defeats per-turn guardrails; consider a sliding-window check over the last N turns
- Human checkpoint needed before adjusting moderation thresholds; lowering a threshold in response to false positives can open real attack vectors — require a second reviewer for any threshold change in production
- Guardrail latency accumulates; two LLM-based guardrails (input + output) at 500ms each add 1s to every request — measure P95 latency impact before enabling in streaming contexts
- `PromptInjectionDetector` regex patterns must be escaped correctly for `re.IGNORECASE`; test each pattern independently against known evasions (Unicode lookalikes, whitespace normalization) before adding to production

## References
- [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation)
- [Guardrails AI docs](https://www.guardrailsai.com/docs)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [NeMo Guardrails GitHub](https://github.com/NVIDIA/NeMo-Guardrails)
- [Microsoft Presidio](https://microsoft.github.io/presidio/)
- [Lakera Guard](https://www.lakera.ai/blog/guide-to-prompt-injection)
