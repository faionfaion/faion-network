# Agent Integration — VUI Privacy and Security

## When to use
- Designing voice features that handle PII, health, financial, or auth-sensitive data.
- Drafting privacy disclosures, consent flows, and "what does X do with my voice" copy.
- Auditing existing VUI for missing trust indicators (listening LED, stop word, history view).
- Building agentic pipelines where ASR transcripts become LLM training/feedback inputs and need redaction first.

## When NOT to use
- Pure text chatbots — covered by general data-privacy methodologies, not VUI specifics.
- One-off internal tools with no user voice capture (e.g., agent-only TTS announcements).
- Compliance scoping (GDPR DPIA, HIPAA controls) — VUI principles inform but do not replace formal assessment.

## Where it fails / limitations
- Principles are jurisdiction-agnostic; GDPR Art.9, COPPA, HIPAA, EU AI Act voice biometrics rules require their own checklists.
- "Mask spoken sensitive data" is hard at TTS layer — most engines do not support inline redaction tokens; needs upstream substitution.
- Wake-word indicator design assumes hardware control (LED, ring); web/embedded VUI with no hardware affordance must use audio-only indicators.
- Voice biometric authentication is treated as one option; principles do not cover spoof/replay defense or liveness checks.

## Agentic workflow
Split privacy/security into a policy agent that decides "is this turn sensitive?" plus an executor agent that crafts the response respecting the policy. The policy agent reads intent + slot values + user profile flags and emits `{sensitive:bool, requires_auth:bool, mask_fields:[...], log_level:"redact"|"full"}`. The executor consumes that output and never sees raw sensitive values for logging paths. Redaction must happen pre-storage and pre-LLM-context, not post-hoc.

### Recommended subagents
- `vui-privacy-classifier` — haiku; binary/structured classification of utterances against a policy schema.
- `vui-redactor` — haiku; deterministic regex+LLM hybrid that masks PII in transcripts before downstream use.
- `consent-copywriter` — sonnet; drafts disclosure scripts tuned for plain-language readability.
- `auth-flow-designer` — sonnet; produces step-up auth dialogs (PIN, biometric, fallback) with branch coverage.

### Prompt pattern
```
You are vui-privacy-classifier. Given the user utterance and current slot map,
return STRICT JSON: {sensitive: bool, categories: [pii|health|financial|auth|other],
requires_step_up_auth: bool, mask_in_logs: [slot_names], rationale: <=20 words}.
Never echo the utterance text in fields other than `rationale`.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `presidio-cli` (Microsoft Presidio) | PII detection/redaction in transcripts | `pip install presidio-analyzer presidio-anonymizer` · microsoft.github.io/presidio |
| `aws cli` (Comprehend, Transcribe redaction) | Built-in PII/PHI redaction in ASR | docs.aws.amazon.com/transcribe/latest/dg/pii-redaction.html |
| `gcloud dlp` | Google DLP API for transcript scanning | cloud.google.com/dlp/docs/concepts-info-types |
| `op` (1Password CLI) | Pull voice-bot secrets at runtime, never in repo | developer.1password.com/docs/cli/ |
| `audit-cli` (custom) | Diff voice-history exports between releases for retention regressions | n/a — internal |
| `step` (smallstep) | Generate per-device certs for voice clients | smallstep.com/docs/step-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Microsoft Presidio | OSS | Yes — Python SDK + REST | Custom recognizers for domain PII (loyalty IDs, MRNs) |
| AWS Transcribe (PII redaction) | SaaS | Yes — REST + boto3 | Real-time and batch redaction modes |
| Google DLP | SaaS | Yes — REST | 100+ infoTypes; supports custom patterns |
| OneTrust / Transcend | SaaS | Partial — REST for DSAR ops | Use for "delete voice history" request automation |
| Pindrop / Nuance Gatekeeper | SaaS | Limited | Voice biometrics + spoof detection |
| Vault by HashiCorp | OSS | Yes — REST/CLI | Encrypt voice recordings at rest with envelope keys |

## Templates & scripts
See `templates.md` for consent-script and trust-indicator copy. Slot redaction snippet:

```python
# redact_slots.py — strip sensitive slots from transcript before LLM/log
import re

SENSITIVE = {"ssn", "card_number", "cvv", "dob", "mrn", "pin"}
PATTERNS = {
    "card_number": re.compile(r"\b(?:\d[ -]?){13,19}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone": re.compile(r"\+?\d[\d -]{8,14}\d"),
}

def redact(text: str, slots: dict) -> tuple[str, list[str]]:
    redacted_fields = []
    for slot, val in list(slots.items()):
        if slot in SENSITIVE and val:
            text = text.replace(str(val), f"<{slot.upper()}>")
            redacted_fields.append(slot)
    for label, pat in PATTERNS.items():
        if pat.search(text):
            text = pat.sub(f"<{label.upper()}>", text)
            redacted_fields.append(label)
    return text, redacted_fields
```

## Best practices
- Default to ephemeral memory for sensitive turns: keep them in the dialog manager only, never persist to logs or vector stores.
- Two-channel confirmation for destructive/irreversible operations: voice initiates, push notification or SMS confirms — voice spoofing alone cannot complete the action.
- Make the "stop listening" command work without wake word and without TTS reply (silent acknowledgement) so users feel they have a hard kill switch.
- Maintain a per-user "voice history" endpoint that reads from a separate auditable store; agents must never invent or summarize the history — only fetch.
- Run a quarterly red-team: prompt the agent to read back the last few turns or "remind me what I told you about my card." If it succeeds, the redaction layer is broken.
- Treat voice biometric IDs as biometric data under GDPR/CCPA — separate consent, separate retention clock, separate deletion API.

## AI-agent gotchas
- LLMs leak sensitive slots into "rationale" or "thought" fields. Forbid free-text reasoning that quotes user data; force structured outputs without echo.
- A model asked "is this sensitive?" without examples drifts — pin a few-shot block with positive and negative cases per category.
- Caching layers (LLM response cache, prompt cache) can re-emit redacted PII if the cache key is the redacted text but the value contains the original. Always cache on redacted outputs only.
- ASR transcripts may include partial redactions ("my card is four nine one two..."); regex misses these. Combine word-level NER with intent-aware slot deletion.
- Step-up auth must invalidate the cached LLM context after success — otherwise an attacker who passes auth once retains a "trusted" flag for the whole session.
- Voice history exports for DSAR must be human-readable transcripts, not opaque audio blobs. Pre-generate text alongside audio at ingest.
- Logs to observability tools (Datadog, Sentry) regularly contain prompt+response. Configure log scrubbers at the SDK layer; do not rely on agents to self-redact in logs.

## References
- NIST Privacy Framework — nist.gov/privacy-framework.
- GDPR Art. 9 (special-category biometric data) — gdpr-info.eu/art-9-gdpr/.
- "Voice Assistant Privacy" — Nielsen Norman Group, nngroup.com/articles/voice-privacy/.
- Microsoft Presidio docs — microsoft.github.io/presidio/.
- HIPAA Privacy Rule (45 CFR 164.530) for health-related voice apps.
- EU AI Act, Annex III high-risk uses (biometric identification).
