# Agent Integration — LLM Guardrails

## When to use
- Any customer-facing LLM application where uncontrolled output could harm users or expose the business to liability
- Regulated domains: healthcare, finance, legal — where hallucinations or off-topic responses have compliance consequences
- Agent pipelines that execute tool calls or write to external systems — execution rails prevent unauthorized actions
- Multi-turn conversations where topic drift or persona breaking is a risk
- Applications handling PII — input/output rails must mask before logging and processing

## When NOT to use
- Internal developer tooling where trust is high and false positives waste time
- Latency-critical paths (< 50ms budget) — LLM-as-judge guardrails add 500ms+ and break the budget
- Guardrails add no value if the base model already refuses the content class (e.g., Claude refusing CSAM)
- Prototyping / local experimentation — premature guardrails slow iteration

## Where it fails / limitations
- LLM-based guardrails (NeMo, Llama Guard) are not deterministic — they can be bypassed via adversarial prompts
- False positives on edge cases frustrate legitimate users; tuning for precision hurts recall and vice versa
- Latency stacking: input rail + output rail + LLM-as-judge can add 2–4s to a pipeline
- Regex/rule-based rails are brittle against paraphrased attacks
- Guardrails AI's RAIL spec and NeMo's Colang DSL both have learning curves; misconfiguration silently fails to block
- Llama Guard classifies but does not transform — a blocked response still requires separate handling logic

## Agentic workflow
Claude subagents integrate guardrails as pre/post hooks around every LLM call. The input guardrail agent validates and sanitizes the user message (PII masking, injection detection, topic check) before forwarding to the core agent. The output guardrail agent receives the raw LLM response, runs content moderation and format validation, then either passes or replaces the response. For multi-agent systems, each worker agent runs its own execution rail before invoking tools.

### Recommended subagents
- `faion-sdd-executor-agent` — for implementing guardrail infrastructure as a tracked SDD feature
- General Claude subagent — can act as an LLM-as-judge guardrail when dedicated classifier is not available

### Prompt pattern
```xml
<guardrail-check>
  <role>Content safety classifier</role>
  <categories>violence, self-harm, pii, jailbreak, off-topic</categories>
  <input>{user_message}</input>
  <task>Classify each category as SAFE or UNSAFE. Return JSON:
  {"result": "safe"|"unsafe", "violations": [], "confidence": 0.0-1.0}</task>
</guardrail-check>
```

```python
# Tiered guardrail: fast rule check first, LLM only on ambiguous
def check_input(text: str) -> GuardrailResult:
    # Tier 1: regex (< 1ms)
    if INJECTION_PATTERN.search(text):
        return GuardrailResult(blocked=True, reason="injection_attempt")
    # Tier 2: classifier (10-50ms)
    if classifier.predict(text) == "unsafe":
        return GuardrailResult(blocked=True, reason="classifier_flagged")
    # Tier 3: LLM-as-judge only for borderline cases (500ms+)
    return GuardrailResult(blocked=False)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `nemoguardrails` | Full dialog-flow guardrails (NVIDIA) | `pip install nemoguardrails` · docs.nvidia.com/nemo/guardrails |
| `guardrails-ai` | Output validation, schema enforcement | `pip install guardrails-ai` · guardrailsai.com/docs |
| `llama-guard` | Safety classification model (Meta) | via `transformers` · huggingface.co/meta-llama/Llama-Guard-3 |
| `presidio` | PII detection and anonymization | `pip install presidio-analyzer presidio-anonymizer` · microsoft.github.io/presidio |
| `langchain` | ConstitutionalAI, output parsers | `pip install langchain` |
| `detoxify` | Toxicity scoring | `pip install detoxify` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| NeMo Guardrails | OSS | Yes — Python library | Colang DSL; strong dialog control; best with NVIDIA NIM |
| Guardrails AI | OSS/SaaS | Yes — Python library + Hub | 50+ validators; RAIL/Pydantic schemas |
| Llama Guard 3 | OSS (model) | Yes — via HF or local | Meta; safety classification; customizable taxonomy |
| Azure AI Content Safety | SaaS | Yes — REST | Hate, violence, self-harm, sexual; built-in severity levels |
| AWS Bedrock Guardrails | SaaS | Yes — Bedrock SDK | Native AWS; PII, grounding, blocked topics |
| Anthropic Claude (built-in) | SaaS | Implicit | Constitutional AI; refuse by default; configurable via system prompt |
| Lakera Guard | SaaS | Yes — REST | Prompt injection and jailbreak detection specialist |

## Templates & scripts
See `templates.md` for full NeMo Guardrails Colang configuration and Guardrails AI RAIL spec templates.

Inline: tiered input guardrail with PII masking (< 50 lines):

```python
import re
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

INJECTION_PATTERNS = [
    re.compile(r"ignore (all |previous |above )?instructions", re.I),
    re.compile(r"you are now", re.I),
    re.compile(r"DAN mode", re.I),
]

def process_input(text: str) -> tuple[str, list[str]]:
    violations = []
    # Injection check
    for pat in INJECTION_PATTERNS:
        if pat.search(text):
            violations.append("prompt_injection")
            break
    # PII masking
    results = analyzer.analyze(text=text, language="en")
    if results:
        violations.append("pii_detected")
        text = anonymizer.anonymize(text=text, analyzer_results=results).text
    return text, violations
```

## Best practices
- Apply tiered checking: regex → fast classifier → LLM-as-judge; stop at the first tier that fires
- Never log raw user input or raw LLM output; log sanitized versions with violation metadata only
- Set a block rate alert at > 5% — sudden spikes indicate adversarial targeting or a broken prompt
- Use async guardrail execution where possible — run input and context guardrails in parallel
- Test guardrails with adversarial datasets before production; red-team jailbreaks monthly
- Separate guardrail logic from business logic — rails should be swappable without touching agent prompts
- For multi-agent pipelines, apply execution rails before every tool call, not just at the conversation boundary

## AI-agent gotchas
- Agents can be convinced to relay blocked content indirectly — output rails must check the final response, not just per-turn outputs
- LLM-based guardrails are subject to the same prompt injection attacks they are meant to prevent; never trust user-supplied context in the guardrail prompt
- NeMo Guardrails requires a running LLM for the Colang runtime — adds infra dependency; budget for it in agent deployment
- Guardrails AI's retry-on-fail mechanism can cause agents to loop indefinitely — set `max_reasks=3` and handle the failure case explicitly
- Llama Guard returns a label but not a score — agents need secondary logic to handle the "unsafe" case gracefully rather than returning a raw error

## References
- https://docs.nvidia.com/nemo/guardrails/latest/index.html
- https://www.guardrailsai.com/docs
- https://huggingface.co/meta-llama/Llama-Guard-3-8B
- https://microsoft.github.io/presidio/
- https://arxiv.org/abs/2310.10501 (NeMo Guardrails paper)
- https://arxiv.org/abs/2312.06674 (Llama Guard paper)
- https://lakera.ai/blog/prompt-injection-attacks
