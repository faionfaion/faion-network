# M-GEN-007: Content Moderation

## Overview

Content moderation ensures AI-generated content is safe, appropriate, and compliant with policies. This covers input filtering, output scanning, NSFW detection, and policy enforcement. Critical for any user-facing AI application.

**When to use:** Any AI application that generates content for users, especially public-facing products.

## Core Concepts

### 1. Moderation Layers

```
User Input → Pre-filter → AI Generation → Post-filter → Output
     ↓           ↓              ↓             ↓          ↓
  Validate   Block/Flag    Generate     Scan/Score   Deliver
  Sanitize   harmful       content      Check policy  or Block
```

### 2. Content Categories

| Category | Risk Level | Detection |
|----------|------------|-----------|
| **Violence** | High | Text + Image classifiers |
| **Sexual/NSFW** | High | Image + Text classifiers |
| **Hate speech** | High | Text classifiers |
| **Self-harm** | Critical | Text patterns + LLM |
| **Misinformation** | Medium | Fact-checking |
| **PII/Privacy** | High | Regex + NER |
| **Copyright** | Medium | Similarity detection |

### 3. Response Actions

| Severity | Action | User Message |
|----------|--------|--------------|
| **Low** | Log, continue | None |
| **Medium** | Flag for review | Warning shown |
| **High** | Block, log | Content blocked |
| **Critical** | Block, alert team | Immediate action |

## Best Practices

### 1. Implement Multi-Layer Moderation

```python
class ContentModerator:
    """Multi-layer content moderation system."""

    def __init__(self):
        self.input_filters = [
            PromptInjectionDetector(),
            PIIDetector(),
            BlocklistFilter()
        ]
        self.output_filters = [
            NSFWDetector(),
            ToxicityClassifier(),
            PoliciesChecker()
        ]

    async def moderate_input(self, content: str) -> dict:
        """Filter input before processing."""
        results = {"pass": True, "flags": [], "sanitized": content}

        for filter in self.input_filters:
            result = await filter.check(content)

            if result["flagged"]:
                results["flags"].append(result)
                results["pass"] = result["severity"] != "block"

                if result.get("sanitized"):
                    results["sanitized"] = result["sanitized"]

        return results

    async def moderate_output(self, content: str, content_type: str) -> dict:
        """Filter output before delivery."""
        results = {"pass": True, "flags": [], "modified": content}

        for filter in self.output_filters:
            if filter.supports(content_type):
                result = await filter.check(content)

                if result["flagged"]:
                    results["flags"].append(result)
                    results["pass"] = result["severity"] != "block"

        return results
```

### 2. Use OpenAI Moderation API

```python
from openai import OpenAI

client = OpenAI()

def check_moderation(text: str) -> dict:
    """Check text using OpenAI moderation endpoint."""

    response = client.moderations.create(input=text)
    result = response.results[0]

    return {
        "flagged": result.flagged,
        "categories": {
            cat: flagged
            for cat, flagged in result.categories.model_dump().items()
            if flagged
        },
        "scores": {
            cat: score
            for cat, score in result.category_scores.model_dump().items()
            if score > 0.1  # Only significant scores
        }
    }

# Example usage
def safe_generate(prompt: str) -> str:
    # Check input
    input_check = check_moderation(prompt)
    if input_check["flagged"]:
        return "I cannot process this request."

    # Generate
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    output = response.choices[0].message.content

    # Check output
    output_check = check_moderation(output)
    if output_check["flagged"]:
        return "I cannot provide this response."

    return output
```

### 3. Detect PII

```python
import re
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

class PIIDetector:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

        # Additional patterns
        self.patterns = {
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "credit_card": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        }

    def detect(self, text: str) -> dict:
        """Detect PII in text."""

        # Use Presidio for comprehensive detection
        results = self.analyzer.analyze(
            text=text,
            entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER",
                     "CREDIT_CARD", "US_SSN", "LOCATION"],
            language="en"
        )

        # Additional regex patterns
        additional = []
        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                additional.append({
                    "type": pii_type,
                    "value": match
                })

        return {
            "found": len(results) > 0 or len(additional) > 0,
            "presidio_results": [
                {"type": r.entity_type, "start": r.start, "end": r.end, "score": r.score}
                for r in results
            ],
            "pattern_results": additional
        }

    def anonymize(self, text: str) -> str:
        """Redact PII from text."""
        results = self.analyzer.analyze(text=text, language="en")
        anonymized = self.anonymizer.anonymize(text=text, analyzer_results=results)
        return anonymized.text
```

## Common Patterns

### Pattern 1: NSFW Image Detection

```python
import requests
from PIL import Image
import io

class NSFWImageDetector:
    """Detect NSFW content in images."""

    def __init__(self, provider: str = "local"):
        self.provider = provider

        if provider == "local":
            from transformers import pipeline
            self.classifier = pipeline(
                "image-classification",
                model="Falconsai/nsfw_image_detection"
            )

    async def check(self, image_path: str) -> dict:
        """Check image for NSFW content."""

        if self.provider == "local":
            return await self._check_local(image_path)
        elif self.provider == "aws":
            return await self._check_aws_rekognition(image_path)
        elif self.provider == "google":
            return await self._check_google_vision(image_path)

    async def _check_local(self, image_path: str) -> dict:
        """Check using local model."""
        image = Image.open(image_path)
        results = self.classifier(image)

        nsfw_score = next(
            (r["score"] for r in results if r["label"] == "nsfw"),
            0
        )

        return {
            "safe": nsfw_score < 0.5,
            "nsfw_score": nsfw_score,
            "labels": results,
            "action": "block" if nsfw_score > 0.7 else "warn" if nsfw_score > 0.5 else "pass"
        }

    async def _check_aws_rekognition(self, image_path: str) -> dict:
        """Check using AWS Rekognition."""
        import boto3

        client = boto3.client('rekognition')

        with open(image_path, 'rb') as f:
            image_bytes = f.read()

        response = client.detect_moderation_labels(
            Image={'Bytes': image_bytes},
            MinConfidence=50
        )

        labels = response['ModerationLabels']

        return {
            "safe": len(labels) == 0,
            "labels": [
                {"name": l['Name'], "confidence": l['Confidence']}
                for l in labels
            ],
            "action": "block" if any(l['Confidence'] > 80 for l in labels) else "pass"
        }
```

### Pattern 2: Toxicity Detection

```python
from transformers import pipeline

class ToxicityDetector:
    """Detect toxic/harmful text content."""

    def __init__(self):
        self.classifier = pipeline(
            "text-classification",
            model="unitary/toxic-bert",
            return_all_scores=True
        )

        self.thresholds = {
            "toxic": 0.5,
            "severe_toxic": 0.3,
            "obscene": 0.5,
            "threat": 0.3,
            "insult": 0.5,
            "identity_hate": 0.3
        }

    def check(self, text: str) -> dict:
        """Check text for toxicity."""

        results = self.classifier(text)[0]

        flagged_categories = {}
        max_score = 0

        for result in results:
            label = result["label"]
            score = result["score"]

            if label in self.thresholds and score > self.thresholds[label]:
                flagged_categories[label] = score

            max_score = max(max_score, score)

        severity = "block" if max_score > 0.8 else "warn" if max_score > 0.5 else "pass"

        return {
            "toxic": len(flagged_categories) > 0,
            "categories": flagged_categories,
            "max_score": max_score,
            "severity": severity
        }
```

### Pattern 3: Prompt Injection Detection

```python
class PromptInjectionDetector:
    """Detect prompt injection attempts."""

    def __init__(self, llm_client):
        self.llm = llm_client

        self.suspicious_patterns = [
            r"ignore (all )?(previous|prior|above)",
            r"disregard (all )?(previous|prior|instructions)",
            r"forget (everything|all|your instructions)",
            r"you are now",
            r"new instructions:",
            r"system prompt:",
            r"<\|.*\|>",  # Special tokens
            r"\[INST\]|\[/INST\]",
            r"###.*instruction"
        ]

    def check(self, text: str) -> dict:
        """Check for prompt injection."""

        # Pattern matching
        pattern_matches = []
        text_lower = text.lower()

        for pattern in self.suspicious_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                pattern_matches.append(pattern)

        # LLM-based detection for sophisticated attacks
        llm_check = self._llm_check(text)

        return {
            "flagged": len(pattern_matches) > 0 or llm_check["suspicious"],
            "pattern_matches": pattern_matches,
            "llm_analysis": llm_check,
            "severity": "block" if llm_check["confidence"] > 0.8 else "warn"
        }

    def _llm_check(self, text: str) -> dict:
        """Use LLM to detect sophisticated injection."""

        prompt = f"""
        Analyze if this text is attempting prompt injection:

        Text: {text}

        Signs of prompt injection:
        1. Attempts to override system instructions
        2. Claims to be a different AI or system
        3. Uses special formatting to manipulate
        4. Requests to reveal system prompts
        5. Attempts to change AI behavior/persona

        Return JSON: {{"suspicious": true/false, "confidence": 0-1, "reason": "..."}}
        """

        response = self.llm.generate(prompt, response_format="json")
        return json.loads(response)
```

### Pattern 4: Policy Compliance Checker

```python
class PolicyChecker:
    """Check content against custom policies."""

    def __init__(self, policies: list):
        self.policies = policies

    def check(self, content: str, context: dict = None) -> dict:
        """Check content against all policies."""

        violations = []

        for policy in self.policies:
            result = self._check_policy(content, policy, context)
            if result["violated"]:
                violations.append({
                    "policy": policy["name"],
                    "severity": policy["severity"],
                    "reason": result["reason"]
                })

        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "action": self._determine_action(violations)
        }

    def _check_policy(self, content: str, policy: dict, context: dict) -> dict:
        """Check single policy."""

        if policy["type"] == "keyword":
            for keyword in policy["keywords"]:
                if keyword.lower() in content.lower():
                    return {"violated": True, "reason": f"Contains '{keyword}'"}

        elif policy["type"] == "regex":
            for pattern in policy["patterns"]:
                if re.search(pattern, content, re.IGNORECASE):
                    return {"violated": True, "reason": f"Matches pattern"}

        elif policy["type"] == "semantic":
            # Use LLM for semantic checking
            return self._semantic_check(content, policy["description"])

        return {"violated": False}

    def _determine_action(self, violations: list) -> str:
        if any(v["severity"] == "critical" for v in violations):
            return "block"
        elif any(v["severity"] == "high" for v in violations):
            return "review"
        elif len(violations) > 0:
            return "warn"
        return "pass"

# Define policies
policies = [
    {
        "name": "no_medical_advice",
        "type": "semantic",
        "description": "Content should not provide specific medical diagnoses or treatment recommendations",
        "severity": "high"
    },
    {
        "name": "no_financial_promises",
        "type": "regex",
        "patterns": [r"guaranteed returns?", r"risk.?free investment"],
        "severity": "high"
    },
    {
        "name": "no_competitor_mentions",
        "type": "keyword",
        "keywords": ["CompetitorA", "CompetitorB"],
        "severity": "medium"
    }
]
```

### Pattern 5: Audit Logging

```python
import logging
from datetime import datetime

class ModerationAuditLogger:
    """Log all moderation decisions for audit."""

    def __init__(self, storage_backend):
        self.storage = storage_backend
        self.logger = logging.getLogger("moderation_audit")

    async def log_decision(
        self,
        request_id: str,
        user_id: str,
        content_type: str,
        input_content: str,
        output_content: str,
        moderation_result: dict,
        action_taken: str
    ):
        """Log moderation decision."""

        record = {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "content_type": content_type,
            "input_hash": hash(input_content),  # Don't store raw content
            "output_hash": hash(output_content) if output_content else None,
            "flags": moderation_result.get("flags", []),
            "scores": moderation_result.get("scores", {}),
            "action": action_taken,
            "blocked": action_taken == "block"
        }

        await self.storage.insert("moderation_logs", record)

        if action_taken == "block":
            self.logger.warning(f"Content blocked: {request_id}")
        elif moderation_result.get("flags"):
            self.logger.info(f"Content flagged: {request_id} - {moderation_result['flags']}")

    async def get_statistics(self, time_range: str = "24h") -> dict:
        """Get moderation statistics."""

        return await self.storage.aggregate("moderation_logs", {
            "total_requests": "count",
            "blocked_requests": "count where blocked=true",
            "flag_distribution": "group by flags",
            "action_distribution": "group by action"
        }, time_range)
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Output-only moderation | Harmful prompts processed | Filter inputs too |
| Binary decisions | No nuance | Use severity levels |
| No logging | Can't audit | Log all decisions |
| Static blocklists | Easy to bypass | Use semantic detection |
| Over-blocking | Poor UX | Tune thresholds carefully |

## Tools & References

### Related Skills
- faion-openai-api-skill
- faion-image-gen-skill

### Related Agents
- faion-multimodal-agent

### External Resources
- [OpenAI Moderation](https://platform.openai.com/docs/guides/moderation)
- [Presidio](https://github.com/microsoft/presidio) - PII detection
- [Perspective API](https://perspectiveapi.com/) - Toxicity
- [AWS Rekognition](https://aws.amazon.com/rekognition/) - Image moderation

## Checklist

- [ ] Identified content risk categories
- [ ] Implemented input filtering
- [ ] Implemented output filtering
- [ ] Added PII detection
- [ ] Added NSFW detection (if images)
- [ ] Added toxicity detection
- [ ] Defined custom policies
- [ ] Set up audit logging
- [ ] Configured severity thresholds
- [ ] Tested with adversarial inputs

---

*Methodology: M-GEN-007 | Category: Multimodal/Generation*
*Related: faion-multimodal-agent*
