---
id: guardrails-basics
name: "Guardrails Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Guardrails Basics

## Overview

Guardrails are safety mechanisms that validate, filter, and constrain LLM inputs and outputs. They protect against harmful content, ensure compliance, maintain quality, and prevent prompt injection attacks.

## When to Use

- Production LLM applications
- User-facing chatbots
- Content generation systems
- When handling sensitive data
- Regulated industries (healthcare, finance)
- Multi-tenant applications

## Key Concepts

### Guardrail Types

| Type | Purpose | When Applied |
|------|---------|--------------|
| Input Guardrails | Validate/sanitize user input | Before LLM call |
| Output Guardrails | Filter/validate LLM response | After LLM call |
| Structural | Ensure format compliance | After LLM call |
| Safety | Block harmful content | Both |
| Compliance | Regulatory requirements | Both |

### Defense Layers

```
User Input
    │
    ▼
Input Guardrails
  - Prompt injection detection
  - PII detection/redaction
  - Topic filtering
  - Length limits
    │
    ▼
LLM
    │
    ▼
Output Guardrails
  - Content moderation
  - Factuality checking
  - Format validation
  - Hallucination detection
    │
    ▼
Response
```

## Input Validation

```python
import re
from typing import Tuple, List
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_valid: bool
    sanitized_input: str
    violations: List[str]

class InputGuardrails:
    """Validate and sanitize user inputs."""

    def __init__(
        self,
        max_length: int = 4000,
        blocked_patterns: List[str] = None,
        pii_patterns: dict = None
    ):
        self.max_length = max_length
        self.blocked_patterns = blocked_patterns or []
        self.pii_patterns = pii_patterns or {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }

    def validate(self, text: str) -> ValidationResult:
        """Validate input text."""
        violations = []
        sanitized = text

        # Length check
        if len(text) > self.max_length:
            violations.append(f"Input exceeds max length ({self.max_length})")
            sanitized = sanitized[:self.max_length]

        # Check blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                violations.append(f"Blocked pattern detected")
                sanitized = re.sub(pattern, '[BLOCKED]', sanitized, flags=re.IGNORECASE)

        # PII detection
        for pii_type, pattern in self.pii_patterns.items():
            if re.search(pattern, text):
                violations.append(f"PII detected: {pii_type}")
                sanitized = re.sub(pattern, f'[{pii_type.upper()}_REDACTED]', sanitized)

        return ValidationResult(
            is_valid=len(violations) == 0,
            sanitized_input=sanitized,
            violations=violations
        )
```

## Prompt Injection Detection

```python
from typing import List, Tuple
import re

class PromptInjectionDetector:
    """Detect and block prompt injection attempts."""

    INJECTION_PATTERNS = [
        # Ignore instructions
        r'ignore\s+(all\s+)?(previous|above|prior)\s+(instructions?|prompts?)',
        r'disregard\s+(all\s+)?(previous|above)',
        # Role manipulation
        r'you\s+are\s+(now|actually)\s+a',
        r'pretend\s+(to\s+be|you\s+are)',
        r'act\s+as\s+(if|a)',
        # System prompt extraction
        r'(show|reveal|display|print|output)\s+(your|the)\s+(system\s+)?prompt',
        r'what\s+(is|are)\s+your\s+(instructions?|rules?)',
        # Jailbreak attempts
        r'(DAN|STAN|DUDE|KEVIN)\s+mode',
        r'developer\s+mode',
        r'bypass\s+(safety|filter)',
        # Code injection
        r'<\s*script',
        r'{{.*}}',  # Template injection
        r'\$\{.*\}',  # String interpolation
    ]

    def __init__(self, custom_patterns: List[str] = None):
        self.patterns = self.INJECTION_PATTERNS + (custom_patterns or [])

    def detect(self, text: str) -> Tuple[bool, List[str]]:
        """Detect prompt injection attempts."""
        detections = []

        for pattern in self.patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detections.append({
                    'pattern': pattern,
                    'matches': matches
                })

        return len(detections) > 0, detections

    def is_safe(self, text: str) -> bool:
        """Check if input is safe."""
        is_injection, _ = self.detect(text)
        return not is_injection
```

## Content Moderation

```python
from openai import OpenAI
from typing import Dict, List

client = OpenAI()

class ContentModerator:
    """Moderate content for safety."""

    CATEGORIES = [
        'hate', 'hate/threatening',
        'harassment', 'harassment/threatening',
        'self-harm', 'self-harm/intent', 'self-harm/instructions',
        'sexual', 'sexual/minors',
        'violence', 'violence/graphic'
    ]

    def __init__(
        self,
        threshold: float = 0.5,
        blocked_categories: List[str] = None
    ):
        self.threshold = threshold
        self.blocked_categories = blocked_categories or self.CATEGORIES

    def moderate(self, text: str) -> Dict:
        """Check content against moderation API."""
        response = client.moderations.create(input=text)
        result = response.results[0]

        flagged = []
        scores = {}

        for category in self.CATEGORIES:
            score = getattr(result.category_scores, category.replace('/', '_').replace('-', '_'))
            scores[category] = score

            if category in self.blocked_categories and score > self.threshold:
                flagged.append({
                    'category': category,
                    'score': score
                })

        return {
            'is_flagged': len(flagged) > 0,
            'flagged_categories': flagged,
            'scores': scores
        }

    def is_safe(self, text: str) -> bool:
        """Quick safety check."""
        result = self.moderate(text)
        return not result['is_flagged']
```

## Topic/Intent Classification

```python
from enum import Enum
from typing import List

class Intent(Enum):
    GENERAL = "general"
    HARMFUL = "harmful"
    PERSONAL_DATA = "personal_data"
    SYSTEM_MANIPULATION = "system_manipulation"
    OFF_TOPIC = "off_topic"

class IntentClassifier:
    """Classify user intent for filtering."""

    def __init__(
        self,
        client,
        allowed_topics: List[str] = None,
        model: str = "gpt-4o-mini"
    ):
        self.client = client
        self.model = model
        self.allowed_topics = allowed_topics

    def classify(self, text: str) -> Dict:
        """Classify the intent of user input."""
        topics_str = ", ".join(self.allowed_topics) if self.allowed_topics else "any"

        prompt = f"""Classify the intent of this message.

Allowed topics: {topics_str}

Message: {text}

Return JSON:
{{
    "intent": "general|harmful|personal_data|system_manipulation|off_topic",
    "is_allowed": true/false,
    "confidence": 0.0-1.0,
    "detected_topics": ["topic1", "topic2"],
    "reasoning": "..."
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
```

## Best Practices

1. **Defense in Depth**
   - Multiple layers of validation
   - Both input and output checks
   - Don't rely on single guardrail

2. **Graceful Degradation**
   - Provide helpful error messages
   - Fall back to safe responses
   - Log violations for analysis

3. **Performance**
   - Use fast checks first
   - Async validation when possible
   - Cache moderation results

4. **Testing**
   - Red team your guardrails
   - Test edge cases
   - Regular adversarial testing

5. **Monitoring**
   - Log all violations
   - Track false positives
   - Alert on patterns

## Common Pitfalls

1. **Over-filtering** - Blocking legitimate content
2. **Under-filtering** - Missing harmful content
3. **No Bypass Detection** - Missing creative injection attempts
4. **Static Rules** - Not updating for new threats
5. **Ignoring Context** - Same rules for all use cases
6. **No Logging** - Can't improve without data

## References

- [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation)
- [Guardrails AI](https://www.guardrailsai.com/)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)

## See Also

- [guardrails-implementation.md](guardrails-implementation.md) - Complete pipeline and advanced patterns

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Safety filter setup | sonnet | Security implementation |
| Output validation | haiku | Validation rules |
