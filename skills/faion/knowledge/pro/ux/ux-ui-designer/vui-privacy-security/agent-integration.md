# Agent Integration — VUI Privacy and Security

## When to use
- Designing a voice agent that handles personal data (banking, health, identity, child profiles).
- Submitting an Alexa/Google Action for certification — privacy disclosures are mandatory and reviewed.
- Operating in regulated jurisdictions: GDPR (EU), HIPAA (US health), CCPA/CPRA (California), Illinois BIPA (biometric voice prints), EU AI Act (2026 high-risk classification for voice biometrics).
- Building voice flows in customer support that may capture card numbers, OTPs, or account secrets.

## When NOT to use
- These principles are non-optional for any production voice product. If skipping, document the risk acceptance.
- For internal-only voice prototypes with synthetic data, full disclosure flows can be deferred until external pilot.

## Where it fails / limitations
- Visual indicators ("listening" LED) don't help blind users; need audio + tactile confirmations.
- "Stop listening" commands fail when ASR is degraded; must always have a hardware/local kill (mute button) as backup.
- Voice-print biometrics under BIPA require written consent — many vendors silently enable speaker ID by default.
- LLM-based voice agents leak training-context and system-prompt content via creative jailbreaks; "private mode" UI does not prevent prompt-leak.
- Cloud transcripts persist on third-party infra (OpenAI, Google, AWS) — local "delete" doesn't always delete.

## Agentic workflow
Build a privacy-by-design pipeline: a subagent reviews flows for sensitive-data capture, a second drafts disclosure scripts compliant with target jurisdictions, and a third runs adversarial replay (jailbreaks, social-engineering) against the deployed agent. Mandatory human-in-the-loop: legal review of disclosure copy and DPIA sign-off before launch.

### Recommended subagents
- `vui-privacy-auditor` — scans dialog flow for PII capture, missing consent, weak auth.
- `vui-disclosure-writer` — drafts opt-in/opt-out scripts per jurisdiction (GDPR, HIPAA, CCPA).
- `vui-redteam-agent` — attempts jailbreaks, prompt-leak, and social-engineering attacks; logs failures.
- `pii-redactor` — strips PII from logs and transcripts before storage (use named-entity + regex hybrid).

### Prompt pattern
```
You are a VUI privacy auditor. For each dialog turn, output JSON:
{ turn, captures_pii: bool, pii_types[], consent_present: bool, sensitive_action: bool, recommendation }
PII types: name, email, phone, address, dob, ssn/inn, card, health, biometric, location, child.
If sensitive_action true (transfer, delete, change-password) require step-up auth in recommendation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `presidio-analyzer` / `presidio-anonymizer` | PII detection/redaction in transcripts | `pip install presidio-analyzer presidio-anonymizer` |
| `scrubadub` | Lightweight PII redaction | `pip install scrubadub` |
| `cryptography` (Fernet) | Encrypt voice transcripts at rest | `pip install cryptography` |
| `aws kms` / `gcloud kms` | Manage keys for encrypted voice payloads | cloud SDKs |
| `garak` | LLM red-team scanner — works on voice transcripts | `pip install garak` |
| `trufflehog` | Detect secrets in committed prompts/configs | `pip install trufflehog` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Realtime + Zero Data Retention | SaaS | Yes | Required for HIPAA/GDPR-sensitive prompts; opt-in via API. |
| AWS HealthLake + Lex | SaaS | Yes | HIPAA-eligible voice paths. |
| Twilio Voice + Verify | SaaS | Yes | Step-up auth (TOTP, push) for sensitive operations. |
| Vonage Verify | SaaS | Yes | Voice biometrics with explicit consent flows. |
| Mozilla Common Voice | OSS dataset | Yes | Diverse training data, transparent licensing. |
| Whisper.cpp self-host | OSS | Yes | Keep transcripts on-prem; no third-party dependency. |

## Templates & scripts
Inline disclosure-emit + sensitive-data redaction (≤40 lines).

```python
# vui_privacy.py
import re
DISCLOSURES = {
    "gdpr": "I'll record this conversation to help you. You can say 'stop recording' anytime, "
            "or ask 'what data do you keep?' I won't use this for ads.",
    "hipaa": "This call may discuss health information. I'll keep it confidential and you can "
             "request deletion at any time.",
}
PII_PATTERNS = {
    "card": re.compile(r"\b(?:\d[ -]?){13,19}\b"),
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "phone": re.compile(r"\b(?:\+?\d[\d -]{7,}\d)\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
}
def disclose(jurisdiction: str) -> str:
    return DISCLOSURES.get(jurisdiction, DISCLOSURES["gdpr"])
def redact(text: str) -> str:
    for label, pat in PII_PATTERNS.items():
        text = pat.sub(f"[{label}]", text)
    return text
```

## Best practices
- Treat the system prompt as semi-public — adversaries will extract it. Never embed real user PII or API secrets in it.
- Use ephemeral session IDs and rotate; never tie voice IDs to permanent user IDs without separate consent.
- Mask spoken back any data the user provided ("...the card ending 4321") — never re-read full numbers.
- Default to opt-out for voice-print biometrics; require explicit verbal + written consent under BIPA-equivalent laws.
- Implement step-up auth (OTP, TOTP, biometric) before any destructive or financial action — voice alone is too weak.

## AI-agent gotchas
- LLMs leak prior conversation context across turns; isolate user sessions explicitly and drop history at session end.
- Realtime API stores audio for abuse monitoring by default; enable Zero Data Retention for sensitive deployments and document it in the DPIA.
- Tool-call payloads often include unredacted PII in logs; redact at the tool boundary, not after persistence.
- "Private mode" prompts ("don't log this") cannot be enforced — always assume model and provider see everything.
- Adversaries use voice cloning to bypass speaker ID; require liveness or knowledge-factor for high-value actions.
- Human checkpoint: legal review for disclosure scripts; security review for transcript-handling pipeline; periodic red-team replay.

## References
- ICO guidance on voice-data and consent: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/
- HIPAA Security Rule overview: https://www.hhs.gov/hipaa/for-professionals/security/index.html
- Illinois BIPA full text: 740 ILCS 14.
- EU AI Act voice biometrics provisions: https://eur-lex.europa.eu/eli/reg/2024/1689
- OWASP LLM Top 10 (covers voice agents): https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Microsoft Presidio docs: https://microsoft.github.io/presidio/
