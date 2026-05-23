"""
purpose: Production GuardrailsPipeline class — input checks, output validators+filters, structured audit.
consumes: LLM client + GuardrailConfig + user_input + system_prompt + retrieval context
produces: GuardrailResult (is_safe, filtered_output, violation_log entries)
depends-on: content/01-core-rules.xml r1, r3, r4, r6
token-budget-impact: per-call; LLM check only on accepted inputs when stakes flag is set

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
