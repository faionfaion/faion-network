# Guardrails Implementation

## Summary

**One-sentence:** Produces a production guardrails pipeline — config dataclass + input/output validators + filters + structured violation log + audit trail + optional async fan-out.

**One-paragraph:** Public-facing LLM applications receive adversarial input and must not relay toxic, hallucinated, or PII-laden content downstream. The implementation pattern: a single GuardrailsPipeline class fed by a GuardrailConfig dataclass, with input checks ordered cheap-first (rule-based injection → API moderation → optional LLM checks), output checks separating validators (boolean accept/block) from filters (transform), and a structured violation log per call. Async variant fans out independent checks via ThreadPoolExecutor for high-throughput apps. Guardrail failures themselves must fail loudly — never swallow exceptions inside a validator.

**Ефективно для:** інженера, що піднімає safety-pipeline над клієнтським LLM-агентом — публічний chatbot, регульована галузь, multi-agent, де outputs feedback в inputs.

## Applies If (ALL must hold)

- Public-facing application accepting adversarial user input.
- Regulated context (healthcare/finance/legal) with compliance output requirements.
- Multi-agent pipeline where one agent's output feeds another.
- Latency budget allows ≥500ms of guardrail overhead.

## Skip If (ANY kills it)

- Internal trusted-only tool — adds latency for no benefit.
- Pure text transformation (translation/summarisation) — hallucination irrelevant.
- Prototype/PoC stage — wire before production, not during exploration.
- Sub-500ms latency budget — use rule-based checks only (see [[guardrails-basics]]).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Policy categories + thresholds | YAML/JSON | safety policy doc |
| Moderation API key (OpenAI / Perspective / Azure) | secret | secrets manager |
| Telemetry sink | URL | observability stack |
| Hallucination context store (optional) | retrieval API | RAG layer |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `[[guardrails-basics]]` | Defines the layered defense baseline. |
| `[[ai-failure-mode-taxonomy]]` | Names violation categories. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: config dataclass, ordered checks, validators-vs-filters, fail-loudly, async fan-out, structured violation log | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for guardrails-config + violation_log shape | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: hardcoded thresholds, silent except swallow, mixed validator+filter, sync N-check serial, no audit log | ~700 |
| `content/04-procedure.xml` | medium | Steps: define GuardrailConfig → wire input pipeline (rule→API→LLM) → wire output pipeline (validators→filters) → emit violation log → optional async fan-out. | ~800 |
| `content/06-decision-tree.xml` | essential | Public-facing + adversarial input? → run; internal trusted? → skip. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft-config-dataclass` | sonnet | Schema authoring. |
| `wire-pipeline-class` | sonnet | Mechanical class build. |
| `tune-hallucination-detector` | opus | Cross-input reasoning. |
| `lint-violation-log` | haiku | Pattern check. |

## Templates

| File | Purpose |
|---|---|
| `templates/guardrails-pipeline.py` | GuardrailConfig + GuardrailResult + GuardrailsPipeline reference class. |
| `templates/moderate-input.py` | Standalone input moderation function with cheap-first ordering. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-guardrails-implementation.py` | Validate guardrails-config.json — required fields, cheap-first ordering, fail_closed=true, async_fanout sane. | Pre-commit + CI. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[guardrails-basics]]
- [[ai-failure-mode-taxonomy]]
- [[prompt-engineering-security]]

## Decision tree

The tree at `content/06-decision-tree.xml` triages: public-facing AND adversarial input possible? → wire production pipeline; trusted-only or prototype? → skip. Walk it before introducing a guardrails layer to avoid the latency tax on tools that don't need it.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/guardrails-pipeline.py`

```python
GuardrailsPipeline — production guardrails for LLM input/output.

Usage:
    pipeline = GuardrailsPipeline(client, config=GuardrailConfig())
    result = pipeline.run(user_input, system_prompt, context)
    if result.is_safe:
        return result.filtered_output
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Callable


@dataclass
class GuardrailConfig:
    max_input_length: int = 4000
    max_output_length: int = 8000
    enable_pii_detection: bool = True
    enable_prompt_injection_detection: bool = True
    enable_content_moderation: bool = True
    enable_hallucination_detection: bool = False  # expensive — opt-in only
    blocked_topics: List[str] = field(default_factory=list)
    custom_validators: List[Callable] = field(default_factory=list)


@dataclass
class GuardrailResult:
    is_safe: bool
    input_modified: bool
    output_modified: bool
    original_input: str
    sanitized_input: str
    original_output: Optional[str]
    filtered_output: Optional[str]
    violations: List[Dict]
    metadata: Dict


INJECTION_SIGNALS = [
    "ignore previous instructions",
    "disregard your instructions",
    "you are now",
    "act as",
    "DAN",
]


def check_injection(text: str) -> tuple[bool, list[str]]:
    """Fast rule-based prompt injection check."""
    detections = [sig for sig in INJECTION_SIGNALS if sig.lower() in text.lower()]
    return bool(detections), detections
```

### `templates/moderate-input.py`

```python
Minimal fast input moderation: rule-based injection check + OpenAI Moderation API.

Usage:
    is_safe, reasons = moderate_input(user_text)
    if not is_safe:
        return {"error": "Input blocked", "reasons": reasons}
"""
import re
from openai import OpenAI

client = OpenAI()

INJECTION_PATTERNS = [
    "ignore previous instructions",
    "disregard your",
    "you are now",
    "act as",
]


def moderate_input(text: str) -> tuple[bool, list[str]]:
    """Returns (is_safe, reasons). Fast rule-based + OpenAI moderation."""
    issues = []

    # Rule-based injection check (microseconds)
    for pattern in INJECTION_PATTERNS:
        if pattern in text.lower():
            issues.append("prompt_injection_signal")
            break

    # API-based content moderation (~100ms, free)
    result = client.moderations.create(input=text)
    if result.results[0].flagged:
        cats = [k for k, v in result.results[0].categories.model_dump().items() if v]
        issues.append(f"moderation_flagged:{','.join(cats)}")

    return len(issues) == 0, issues
```
