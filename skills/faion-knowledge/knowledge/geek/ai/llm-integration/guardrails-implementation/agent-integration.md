# Agent Integration — Guardrails Implementation

## When to use
- Public-facing LLM applications where users may submit adversarial or off-policy input
- Regulated industries (healthcare, finance, legal) where output must meet compliance standards
- Multi-agent pipelines where one agent's output becomes another's input — prevent cascading bad data
- Any application storing or transmitting user content through an LLM
- Applications where hallucinated facts could cause real harm (medical advice, legal citations)

## When NOT to use
- Internal developer tools where all users are trusted — guardrails add latency and cost for no benefit
- Pure text transformation tasks (translation, summarization of provided text) — hallucination guardrails are irrelevant
- Prototype/PoC stages — implement guardrails before production, not during exploration
- When the guardrail check itself calls an LLM — avoid if latency budget is <500ms; use rule-based checks instead

## Where it fails / limitations
- LLM-based hallucination detection is itself fallible — a hallucinating model checking another model's output may miss hallucinations
- Prompt injection detection has high false-positive rates on legitimate technical prompts (code, SQL, shell commands)
- OpenAI Moderation API covers toxicity/self-harm well but misses domain-specific policy violations (e.g., medical misinformation)
- Async guardrail pipelines add 200–800ms latency per call — unacceptable for real-time voice interfaces
- Custom validators that call external APIs (PII scanners, content classifiers) introduce external failure modes

## Agentic workflow
Guardrails wrap the agent's LLM call, not the agent itself. The `GuardrailsPipeline` sits between the user request and the LLM: input validation → LLM call → output validation → response. In multi-agent systems, guardrails run at the boundary between user-facing agents and internal agents — not on every inter-agent message, which would be too slow. Human-in-the-loop review should trigger when `violations` are non-empty but not severe enough to auto-block.

### Recommended subagents
- `password-scrubber-agent` — strips credentials and secrets from input before passing to LLM (related pattern)
- A dedicated `moderation-agent` that wraps `GuardrailsPipeline` and routes flagged requests to human review queue

### Prompt pattern
Input sanitization check (rule-based, fast):
```python
INJECTION_SIGNALS = ["ignore previous", "disregard instructions", "you are now", "act as", "DAN"]
def has_injection_signal(text: str) -> bool:
    return any(sig.lower() in text.lower() for sig in INJECTION_SIGNALS)
```

Hallucination check prompt (LLM-based, slow — use sparingly):
```
Given this context: {context}
And this response: {response}
List any claims in the response NOT supported by the context. Return JSON: {"unsupported": [...]}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `guardrails-ai` | Framework for LLM input/output validation with validators | `pip install guardrails-ai` / https://www.guardrailsai.com |
| `openai` (Moderation API) | Content moderation (toxicity, self-harm, violence) | built-in SDK / https://platform.openai.com/docs/guides/moderation |
| `presidio` (Microsoft) | PII detection and anonymization | `pip install presidio-analyzer presidio-anonymizer` / https://microsoft.github.io/presidio |
| `langchain` (callbacks) | Guardrail hooks at chain/agent step boundaries | `pip install langchain` |
| `rebuff` | Prompt injection detection service | https://github.com/protectai/rebuff |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Moderation API | SaaS | Yes | Free, fast, covers 11 harm categories |
| Guardrails AI | OSS + SaaS | Yes | 50+ pre-built validators; custom validators |
| Microsoft Presidio | OSS | Yes | Best-in-class PII detection, entity anonymization |
| AWS Comprehend | SaaS | Yes | PII + sentiment + entity recognition |
| Azure Content Safety | SaaS | Yes | Enterprise content moderation with audit logs |
| Lakera Guard | SaaS | Yes | Dedicated prompt injection detection API |
| Rebuff | OSS | Yes | Heuristic + semantic prompt injection detection |

## Templates & scripts
See `templates.md` for `GuardrailsPipeline` class. Minimal production-ready input check:

```python
import re
from openai import OpenAI

client = OpenAI()

def moderate_input(text: str) -> tuple[bool, list[str]]:
    """Returns (is_safe, reasons). Fast, rule-based + OpenAI moderation."""
    issues = []
    # Rule-based injection check
    injections = ["ignore previous instructions", "disregard your", "you are now", "act as"]
    if any(p in text.lower() for p in injections):
        issues.append("prompt_injection_signal")
    # API-based content check (adds ~100ms)
    result = client.moderations.create(input=text)
    if result.results[0].flagged:
        cats = [k for k, v in result.results[0].categories.model_dump().items() if v]
        issues.append(f"moderation_flagged:{','.join(cats)}")
    return len(issues) == 0, issues
```

## Best practices
- Layer defense: fast rule-based checks first, slow LLM-based checks only when needed
- OpenAI Moderation API is free and adds ~100ms — always run it before passing user input to a generation call
- Use Microsoft Presidio for PII detection; regex-only PII detection has unacceptably high false-negative rates
- Define a `GuardrailConfig` object at app startup — never hardcode thresholds inside validator functions
- Log every violation with the original input (truncated), violation type, and timestamp — this is your audit trail
- For hallucination detection, require a `context` document; without ground truth, hallucination detection is guesswork
- Set `enable_hallucination_detection=False` by default — it doubles cost and latency; enable only for high-stakes outputs

## AI-agent gotchas
- Guardrail pipeline must not catch exceptions silently — a failed guardrail check should fail loudly, not pass through
- Prompt injection detection has false positives on code snippets and SQL — whitelist technical contexts or use a separate code-aware detector
- An agent that retries on injection detection will retry forever if the user is genuinely adversarial — add a max-attempts block and escalate to human review
- Do not run hallucination detection synchronously in the request path for every call — queue it as async post-processing and surface results in a review UI
- Guardrail violations must be logged in a way that preserves privacy — hash or truncate the violating content before writing to logs
- Multi-agent pipelines that trust inter-agent messages implicitly are vulnerable to prompt injection through tool results — validate tool outputs too

## References
- https://www.guardrailsai.com/docs
- https://platform.openai.com/docs/guides/moderation
- https://microsoft.github.io/presidio/
- https://github.com/protectai/rebuff
- https://owasp.org/www-project-top-10-for-large-language-model-applications/ (OWASP LLM Top 10)
