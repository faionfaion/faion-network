---
id: guardrails-implementation
name: "Guardrails Implementation"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Guardrails Implementation

## Overview

Complete implementation patterns for guardrails pipelines, including output validation, hallucination detection, and using the Guardrails AI library.

## Output Validation

```python
from typing import List, Dict, Callable
import json

class OutputGuardrails:
    """Validate and filter LLM outputs."""

    def __init__(self):
        self.validators: List[Callable] = []
        self.filters: List[Callable] = []

    def add_validator(self, validator: Callable):
        """Add a validator function."""
        self.validators.append(validator)

    def add_filter(self, filter_func: Callable):
        """Add a filter function."""
        self.filters.append(filter_func)

    def validate(self, output: str) -> Tuple[bool, List[str]]:
        """Run all validators on output."""
        errors = []

        for validator in self.validators:
            try:
                is_valid, error = validator(output)
                if not is_valid:
                    errors.append(error)
            except Exception as e:
                errors.append(f"Validator error: {e}")

        return len(errors) == 0, errors

    def filter(self, output: str) -> str:
        """Apply all filters to output."""
        filtered = output

        for filter_func in self.filters:
            try:
                filtered = filter_func(filtered)
            except Exception as e:
                pass  # Skip failed filters

        return filtered

# Common validators
def validate_no_profanity(output: str) -> Tuple[bool, str]:
    """Check for profanity."""
    profanity_list = ['...']  # Add actual list
    for word in profanity_list:
        if word.lower() in output.lower():
            return False, f"Profanity detected: {word}"
    return True, ""

def validate_json_format(output: str) -> Tuple[bool, str]:
    """Validate JSON format."""
    try:
        json.loads(output)
        return True, ""
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

def validate_length(max_length: int):
    """Create length validator."""
    def validator(output: str) -> Tuple[bool, str]:
        if len(output) > max_length:
            return False, f"Output exceeds {max_length} characters"
        return True, ""
    return validator

# Common filters
def filter_remove_urls(output: str) -> str:
    """Remove URLs from output."""
    url_pattern = r'https?://\S+'
    return re.sub(url_pattern, '[URL REMOVED]', output)

def filter_remove_code_blocks(output: str) -> str:
    """Remove code blocks from output."""
    return re.sub(r'```[\s\S]*?```', '[CODE REMOVED]', output)
```

## Hallucination Detection

```python
class HallucinationDetector:
    """Detect potential hallucinations in LLM output."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def check_factuality(
        self,
        claim: str,
        context: str
    ) -> Dict:
        """Check if a claim is supported by context."""
        prompt = f"""Determine if the claim is supported by the context.

Context:
{context}

Claim:
{claim}

Respond with JSON:
{{
    "verdict": "supported" | "not_supported" | "partially_supported",
    "confidence": 0.0-1.0,
    "explanation": "..."
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def detect_hallucinations(
        self,
        output: str,
        context: str
    ) -> Dict:
        """Detect hallucinations in output given context."""
        prompt = f"""Analyze the response for potential hallucinations.
A hallucination is information not supported by the given context.

Context:
{context}

Response to analyze:
{output}

Return JSON:
{{
    "has_hallucinations": true/false,
    "hallucinated_claims": ["claim1", "claim2"],
    "supported_claims": ["claim1", "claim2"],
    "confidence": 0.0-1.0
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
```

## Complete Guardrails Pipeline

```python
from dataclasses import dataclass
from typing import Optional, List, Callable
import logging

@dataclass
class GuardrailConfig:
    max_input_length: int = 4000
    max_output_length: int = 8000
    enable_pii_detection: bool = True
    enable_prompt_injection_detection: bool = True
    enable_content_moderation: bool = True
    enable_hallucination_detection: bool = False
    blocked_topics: List[str] = None
    custom_validators: List[Callable] = None

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

class GuardrailsPipeline:
    """Complete guardrails pipeline for LLM applications."""

    def __init__(
        self,
        client,
        model: str = "gpt-4o",
        config: Optional[GuardrailConfig] = None
    ):
        self.client = client
        self.model = model
        self.config = config or GuardrailConfig()
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.input_guardrails = InputGuardrails(
            max_length=self.config.max_input_length
        )
        self.injection_detector = PromptInjectionDetector()
        self.content_moderator = ContentModerator()
        self.output_guardrails = OutputGuardrails()
        self.hallucination_detector = HallucinationDetector(client)

    def process_input(self, user_input: str) -> Tuple[str, List[Dict]]:
        """Process and validate user input."""
        violations = []
        sanitized = user_input

        # Length and PII check
        if self.config.enable_pii_detection:
            result = self.input_guardrails.validate(sanitized)
            if not result.is_valid:
                violations.extend([{"type": "input_validation", "detail": v} for v in result.violations])
            sanitized = result.sanitized_input

        # Prompt injection detection
        if self.config.enable_prompt_injection_detection:
            is_injection, detections = self.injection_detector.detect(sanitized)
            if is_injection:
                violations.append({
                    "type": "prompt_injection",
                    "detail": "Potential prompt injection detected",
                    "detections": detections
                })
                return None, violations  # Block the request

        # Content moderation
        if self.config.enable_content_moderation:
            moderation = self.content_moderator.moderate(sanitized)
            if moderation['is_flagged']:
                violations.append({
                    "type": "content_moderation",
                    "detail": "Content flagged by moderation",
                    "categories": moderation['flagged_categories']
                })
                return None, violations

        return sanitized, violations

    def process_output(
        self,
        output: str,
        context: str = None
    ) -> Tuple[str, List[Dict]]:
        """Process and validate LLM output."""
        violations = []
        filtered = output

        # Content moderation
        if self.config.enable_content_moderation:
            moderation = self.content_moderator.moderate(filtered)
            if moderation['is_flagged']:
                violations.append({
                    "type": "output_moderation",
                    "detail": "Output flagged by moderation",
                    "categories": moderation['flagged_categories']
                })
                # You might filter or block here
                filtered = "[Response filtered due to content policy]"

        # Hallucination detection
        if self.config.enable_hallucination_detection and context:
            hallucination_check = self.hallucination_detector.detect_hallucinations(
                filtered, context
            )
            if hallucination_check.get('has_hallucinations'):
                violations.append({
                    "type": "hallucination",
                    "detail": "Potential hallucinations detected",
                    "claims": hallucination_check.get('hallucinated_claims', [])
                })

        # Custom validators
        if self.config.custom_validators:
            for validator in self.config.custom_validators:
                is_valid, error = validator(filtered)
                if not is_valid:
                    violations.append({
                        "type": "custom_validation",
                        "detail": error
                    })

        # Output filters
        filtered = self.output_guardrails.filter(filtered)

        return filtered, violations

    def run(
        self,
        user_input: str,
        system_prompt: str = "",
        context: str = None
    ) -> GuardrailResult:
        """Run complete guardrails pipeline."""
        all_violations = []

        # Process input
        sanitized_input, input_violations = self.process_input(user_input)
        all_violations.extend(input_violations)

        if sanitized_input is None:
            # Input blocked
            return GuardrailResult(
                is_safe=False,
                input_modified=True,
                output_modified=False,
                original_input=user_input,
                sanitized_input="[BLOCKED]",
                original_output=None,
                filtered_output=None,
                violations=all_violations,
                metadata={"stage": "input_blocked"}
            )

        # Call LLM
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": sanitized_input})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        original_output = response.choices[0].message.content

        # Process output
        filtered_output, output_violations = self.process_output(
            original_output, context
        )
        all_violations.extend(output_violations)

        return GuardrailResult(
            is_safe=len(all_violations) == 0,
            input_modified=sanitized_input != user_input,
            output_modified=filtered_output != original_output,
            original_input=user_input,
            sanitized_input=sanitized_input,
            original_output=original_output,
            filtered_output=filtered_output,
            violations=all_violations,
            metadata={"model": self.model}
        )
```

## Using Guardrails Library

```python
# pip install guardrails-ai

from guardrails import Guard
from guardrails.validators import (
    ValidLength,
    ToxicLanguage,
    RegexMatch,
    ValidJSON
)

# Create guard with validators
guard = Guard().use_many(
    ValidLength(min=1, max=1000, on_fail="fix"),
    ToxicLanguage(threshold=0.5, on_fail="filter"),
)

# Use with LLM
result = guard(
    llm_api=openai.chat.completions.create,
    prompt="Tell me about AI safety",
    model="gpt-4o",
    max_tokens=500
)

if result.validation_passed:
    print(result.validated_output)
else:
    print(f"Validation failed: {result.validation_summary}")
```

## Usage Example

```python
from openai import OpenAI

client = OpenAI()

# Initialize pipeline
config = GuardrailConfig(
    enable_pii_detection=True,
    enable_prompt_injection_detection=True,
    enable_content_moderation=True,
    enable_hallucination_detection=True
)

pipeline = GuardrailsPipeline(client, config=config)

# Run with guardrails
result = pipeline.run(
    user_input="What are the benefits of AI?",
    system_prompt="You are a helpful AI assistant.",
    context="AI improves efficiency and automation."
)

if result.is_safe:
    print(f"Safe response: {result.filtered_output}")
else:
    print(f"Violations detected: {result.violations}")
```

## Performance Optimization

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncGuardrailsPipeline(GuardrailsPipeline):
    """Async version for better performance."""

    async def process_input_async(self, user_input: str):
        """Process input with parallel checks."""
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()

            # Run checks in parallel
            pii_check = loop.run_in_executor(
                executor,
                self.input_guardrails.validate,
                user_input
            )
            injection_check = loop.run_in_executor(
                executor,
                self.injection_detector.detect,
                user_input
            )
            moderation_check = loop.run_in_executor(
                executor,
                self.content_moderator.moderate,
                user_input
            )

            # Wait for all checks
            results = await asyncio.gather(
                pii_check,
                injection_check,
                moderation_check
            )

            return self._process_results(results)
```

## Monitoring and Logging

```python
import logging
from datetime import datetime

class GuardrailsMonitor:
    """Monitor guardrail violations."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.violations_count = {}

    def log_violation(self, result: GuardrailResult):
        """Log violation details."""
        if not result.is_safe:
            for violation in result.violations:
                violation_type = violation['type']

                # Count violations
                if violation_type not in self.violations_count:
                    self.violations_count[violation_type] = 0
                self.violations_count[violation_type] += 1

                # Log details
                self.logger.warning(
                    f"Guardrail violation: {violation_type}",
                    extra={
                        'timestamp': datetime.now().isoformat(),
                        'violation': violation,
                        'input': result.original_input[:100],
                        'metadata': result.metadata
                    }
                )

    def get_stats(self) -> Dict:
        """Get violation statistics."""
        return {
            'total_violations': sum(self.violations_count.values()),
            'by_type': self.violations_count
        }
```

## See Also

- [guardrails-basics.md](guardrails-basics.md) - Fundamentals and core concepts
- [prompt-basics.md](prompt-basics.md) - Prompt engineering best practices
- [rag-evaluation.md](rag-evaluation.md) - RAG evaluation metrics

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Custom guardrails | sonnet | Pattern implementation |
| Prompt injection prevention | opus | Security-critical design |
