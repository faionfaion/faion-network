# Guardrails Basics

## Summary

**One-sentence:** Produces a 4-layer defense-in-depth guardrails spec — regex pre-filter, length cap, output schema, LLM classifier last — with per-layer latency budget and order constraint.

**One-paragraph:** No single guardrail check holds against adversarial inputs. The minimum-viable shape is layered: (1) regex pre-filter for known PII / token patterns, microsecond cost; (2) length cap on inputs and outputs, microsecond cost; (3) output schema validation, sub-millisecond; (4) LLM classifier (last) for semantic checks, 300-800ms. Order matters — cheap deterministic checks reject 80% of bad inputs without paying the classifier cost. Track per-layer block rates in a dashboard; one layer accounting for 100% of blocks is a sign the others are misconfigured.

**Ефективно для:** customer-facing chat, regulated content pipelines, multi-tenant agents, output-validation gates.

## Applies If (ALL must hold)

- Application accepts untrusted user input OR produces public-facing output.
- Latency budget allows up to 1s of guardrail overhead.
- A named owner can maintain regex patterns + classifier prompt + threshold.
- A telemetry sink records per-layer block events.

## Skip If (ANY kills it)

- Internal-only tool with no external input.
- Prototype / demo — guardrails added before production, not before pitch.
- Output format only — use structured output (response_schema / tool_choice) instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| List of policy categories | doc | safety policy |
| Sample bad-input fixtures | JSONL | red team / eval |
| Classifier model + prompt | string | prompt repo |
| Telemetry sink | URL | observability |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `[[guardrails-implementation]]` | Sibling for advanced patterns (NeMo Guardrails, semantic router). |
| `[[ai-failure-mode-taxonomy]]` | Naming categories the guardrails defend. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 rules: layered, cheap-first order, per-layer block-rate dashboard, classifier last, fail-closed default | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for guardrails-spec.json: layers, thresholds, latency budget | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: single-layer, classifier-first, no telemetry, no fail-closed, classifier-as-detector-only | ~600 |
| `content/06-decision-tree.xml` | essential | Root: "untrusted input or public output?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Author regex patterns | sonnet | Pattern matching. |
| Author classifier prompt | opus | Adversarial wording. |
| Tune thresholds | sonnet | A/B from telemetry. |

## Templates

| File | Purpose |
|---|---|
| `templates/input-guardrails.py` | Layer-1 regex/PII/length pre-filter + prompt-injection detector. |
| `templates/layered-check.py` | Ordered 4-layer runner returning a structured dict. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-guardrails-basics.py` | Validates guardrails-spec.json: ≥4 layers, classifier is last, fail_closed default true. | Pre-commit on spec. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/llm-integration/`
- `[[guardrails-implementation]]`
- `[[indirect-prompt-injection-defense]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` checks whether layered guardrails apply: internal-only or prototype → skip; production + untrusted input → run the spec.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/input-guardrails.py`

```python
"""
# InputGuardrails + PromptInjectionDetector templates
# Usage: instantiate, call validate() / detect() before passing input to LLM

from dataclasses import dataclass, field
from typing import List, Tuple, Dict
import re


@dataclass
class ValidationResult:
    is_valid: bool
    sanitized_input: str
    violations: List[str]


PII_PATTERNS: Dict[str, str] = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
    'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
}

INJECTION_PATTERNS: List[str] = [
    r'ignore\s+(all\s+)?(previous|above|prior)\s+(instructions?|prompts?)',
    r'disregard\s+(all\s+)?(previous|above)',
    r'you\s+are\s+(now|actually)\s+a',
    r'pretend\s+(to\s+be|you\s+are)',
    r'(show|reveal|display|print)\s+(your|the)\s+(system\s+)?prompt',
    r'(DAN|STAN|DUDE|KEVIN)\s+mode',
    r'bypass\s+(safety|filter)',
    r'<\s*script',
    r'\$\{.*\}',
]


class InputGuardrails:
    def __init__(
        self,
        max_length: int = 4000,
        blocked_patterns: List[str] = None,
        pii_patterns: Dict[str, str] = None,
    ):
        self.max_length = max_length
        self.blocked_patterns = blocked_patterns or []
        self.pii_patterns = pii_patterns or PII_PATTERNS

    def validate(self, text: str) -> ValidationResult:
        violations: List[str] = []
        sanitized = text
        if len(text) > self.max_length:
            violations.append(f"Input exceeds max length ({self.max_length})")
            sanitized = sanitized[:self.max_length]
        for pattern in self.blocked_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                violations.append("Blocked pattern detected")
                sanitized = re.sub(pattern, '[BLOCKED]', sanitized, flags=re.IGNORECASE)
        for pii_type, pattern in self.pii_patterns.items():
            if re.search(pattern, text):
                violations.append(f"PII detected: {pii_type}")
                sanitized = re.sub(pattern, f'[{pii_type.upper()}_REDACTED]', sanitized)
        return ValidationResult(
            is_valid=len(violations) == 0,
            sanitized_input=sanitized,
            violations=violations,
        )


class PromptInjectionDetector:
    def __init__(self, custom_patterns: List[str] = None):
        self.patterns = INJECTION_PATTERNS + (custom_patterns or [])

    def detect(self, text: str) -> Tuple[bool, List[Dict]]:
        detections = []
        for pattern in self.patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detections.append({'pattern': pattern, 'matches': matches})
        return bool(detections), detections

    def is_safe(self, text: str) -> bool:
        injected, _ = self.detect(text)
        return not injected
```

### `templates/layered-check.py`

```python
"""
# Layered guardrail check: fast-to-slow ordering
# Requires: PromptInjectionDetector and a moderator with .moderate(text) -> dict

def check_input(text: str, detector, moderator, max_len: int = 4000) -> dict:
    """Run layered input checks from fastest to slowest.

    Returns {"safe": True} or {"safe": False, "reason": str, ...}
    Never raises — callers get a structured dict in all cases.
    """
    if len(text) > max_len:
        return {"safe": False, "reason": "length_exceeded"}
    is_injection, _ = detector.detect(text)
    if is_injection:
        return {"safe": False, "reason": "prompt_injection"}
    try:
        mod = moderator.moderate(text)
        if mod.get("is_flagged"):
            return {
                "safe": False,
                "reason": "moderation",
                "categories": mod.get("flagged_categories", []),
            }
    except Exception as exc:
        # Moderation API failure → log and fail open (or closed per policy)
        return {"safe": False, "reason": f"moderation_error: {exc}"}
    return {"safe": True}
```
