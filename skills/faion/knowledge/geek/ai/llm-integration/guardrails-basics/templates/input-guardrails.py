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
