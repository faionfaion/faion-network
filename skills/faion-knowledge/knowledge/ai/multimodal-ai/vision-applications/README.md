---
id: vision-applications
name: "Image Analysis - Applications"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
parent: image-analysis-vision
---

# Image Analysis - Applications

## Overview

Advanced vision applications including OCR, document analysis, classification, content moderation, and production-grade services.

## When to Use

- Document and image analysis
- Visual question answering
- OCR and text extraction
- Content moderation
- Product image analysis
- Accessibility (image descriptions)
- Medical/scientific image analysis

## OCR and Document Analysis

```python
from openai import OpenAI
import base64
from typing import List, Dict
import json

class DocumentAnalyzer:
    """Analyze documents and extract text."""

    def __init__(self, model: str = "gpt-4o"):
        self.client = OpenAI()
        self.model = model

    def extract_text(self, image_path: str) -> str:
        """Extract all text from image."""
        return self._analyze(
            image_path,
            "Extract all text visible in this image. Maintain formatting where possible."
        )

    def extract_structured_data(
        self,
        image_path: str,
        fields: List[str]
    ) -> dict:
        """Extract specific fields from document."""
        fields_str = ", ".join(fields)
        prompt = f"""Extract these fields from the document: {fields_str}

Return JSON with the field names as keys. Use null for missing fields."""

        response = self._analyze(image_path, prompt, json_mode=True)
        return json.loads(response)

    def analyze_receipt(self, image_path: str) -> dict:
        """Analyze receipt and extract items."""
        prompt = """Analyze this receipt and extract:
- store_name
- date
- items: list of {name, quantity, price}
- subtotal
- tax
- total
- payment_method (if visible)

Return as JSON."""

        response = self._analyze(image_path, prompt, json_mode=True)
        return json.loads(response)

    def analyze_form(self, image_path: str) -> dict:
        """Analyze filled form."""
        prompt = """Analyze this form and extract all filled fields.
Return JSON with field names/labels as keys and filled values as values.
For checkboxes, use true/false.
For empty fields, use null."""

        response = self._analyze(image_path, prompt, json_mode=True)
        return json.loads(response)

    def _analyze(
        self,
        image_path: str,
        prompt: str,
        json_mode: bool = False
    ) -> str:
        """Internal analysis method."""
        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()

        kwargs = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ]
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
```

## Image Classification

```python
from typing import List, Dict

class ImageClassifier:
    """Classify images into categories."""

    def __init__(
        self,
        categories: List[str],
        model: str = "gpt-4o"
    ):
        self.categories = categories
        self.client = OpenAI()
        self.model = model

    def classify(
        self,
        image_path: str,
        return_confidence: bool = True
    ) -> Dict:
        """Classify image into predefined categories."""
        categories_str = ", ".join(self.categories)

        prompt = f"""Classify this image into one of these categories: {categories_str}

Return JSON with:
- category: the best matching category
- confidence: confidence score (0-1)
- reasoning: brief explanation"""

        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def classify_batch(
        self,
        image_paths: List[str]
    ) -> List[Dict]:
        """Classify multiple images."""
        return [self.classify(path) for path in image_paths]

# Usage
classifier = ImageClassifier(
    categories=["landscape", "portrait", "product", "document", "screenshot"]
)
result = classifier.classify("image.jpg")
print(f"Category: {result['category']}, Confidence: {result['confidence']}")
```

## Content Moderation

```python
class ContentModerator:
    """Moderate image content for safety."""

    def __init__(self, model: str = "gpt-4o"):
        self.client = OpenAI()
        self.model = model

    def moderate(self, image_path: str) -> Dict:
        """Check image for inappropriate content."""
        prompt = """Analyze this image for content moderation.

Check for:
- Violence or gore
- Adult/sexual content
- Hate symbols or imagery
- Dangerous activities
- Illegal content

Return JSON:
{
    "is_safe": true/false,
    "flags": [list of issues found],
    "severity": "none" | "low" | "medium" | "high",
    "details": "explanation"
}"""

        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
```

## Production Vision Service

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union
from enum import Enum
import logging
from pathlib import Path
import httpx

class ImageSource(Enum):
    URL = "url"
    FILE = "file"
    BASE64 = "base64"

@dataclass
class VisionConfig:
    model: str = "gpt-4o"
    max_image_size_mb: int = 20
    detail: str = "auto"  # "low", "high", "auto"
    max_retries: int = 3
    timeout: int = 60

class VisionService:
    """Production vision analysis service."""

    def __init__(self, config: Optional[VisionConfig] = None):
        self.config = config or VisionConfig()
        self.client = OpenAI()
        self.logger = logging.getLogger(__name__)

    def analyze(
        self,
        image: Union[str, Path],
        prompt: str,
        source_type: ImageSource = ImageSource.FILE,
        structured_output: bool = False
    ) -> Dict[str, Any]:
        """Analyze image with error handling."""
        try:
            # Prepare image content
            image_content = self._prepare_image(image, source_type)

            # Build request
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_content,
                                "detail": self.config.detail
                            }
                        }
                    ]
                }
            ]

            kwargs = {
                "model": self.config.model,
                "messages": messages,
                "timeout": self.config.timeout
            }

            if structured_output:
                kwargs["response_format"] = {"type": "json_object"}

            # Make request with retry
            for attempt in range(self.config.max_retries):
                try:
                    response = self.client.chat.completions.create(**kwargs)
                    content = response.choices[0].message.content

                    return {
                        "success": True,
                        "content": json.loads(content) if structured_output else content,
                        "usage": {
                            "prompt_tokens": response.usage.prompt_tokens,
                            "completion_tokens": response.usage.completion_tokens
                        }
                    }
                except Exception as e:
                    self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == self.config.max_retries - 1:
                        raise

        except Exception as e:
            self.logger.error(f"Vision analysis failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _prepare_image(
        self,
        image: Union[str, Path],
        source_type: ImageSource
    ) -> str:
        """Prepare image for API."""
        if source_type == ImageSource.URL:
            return str(image)

        elif source_type == ImageSource.BASE64:
            return f"data:image/jpeg;base64,{image}"

        else:  # FILE
            path = Path(image)
            if not path.exists():
                raise FileNotFoundError(f"Image not found: {path}")

            # Check size
            size_mb = path.stat().st_size / (1024 * 1024)
            if size_mb > self.config.max_image_size_mb:
                raise ValueError(f"Image too large: {size_mb:.1f}MB")

            # Read and encode
            with open(path, "rb") as f:
                data = base64.standard_b64encode(f.read()).decode()

            # Determine media type
            suffix = path.suffix.lower()
            media_types = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp"
            }
            media_type = media_types.get(suffix, "image/jpeg")

            return f"data:{media_type};base64,{data}"

    def batch_analyze(
        self,
        images: List[Union[str, Path]],
        prompt: str,
        source_type: ImageSource = ImageSource.FILE
    ) -> List[Dict]:
        """Analyze multiple images."""
        results = []
        for image in images:
            result = self.analyze(image, prompt, source_type)
            results.append(result)
        return results
```

## Usage Examples

### Document Analysis
```python
# Receipt processing
analyzer = DocumentAnalyzer()
receipt_data = analyzer.analyze_receipt("receipt.jpg")
print(f"Total: ${receipt_data['total']}")
print(f"Items: {len(receipt_data['items'])}")

# Form extraction
form_data = analyzer.analyze_form("application.png")
print(f"Name: {form_data['full_name']}")
```

### Image Classification
```python
# E-commerce product classification
classifier = ImageClassifier(
    categories=["clothing", "electronics", "furniture", "food", "other"]
)
result = classifier.classify("product.jpg")
print(f"Category: {result['category']} ({result['confidence']:.2%})")
```

### Content Moderation
```python
# User-uploaded content check
moderator = ContentModerator()
result = moderator.moderate("user_photo.jpg")

if not result["is_safe"]:
    print(f"Warning: {result['severity']} - {result['details']}")
    print(f"Flags: {', '.join(result['flags'])}")
```

### Production Service
```python
# Full production service
config = VisionConfig(
    model="gpt-4o",
    detail="high",
    max_retries=3
)
service = VisionService(config)

# Analyze product images
result = service.analyze(
    "product.jpg",
    "Describe this product and list its key features.",
    structured_output=True
)

if result["success"]:
    print(result["content"])
    print(f"Tokens: {result['usage']['prompt_tokens']} + {result['usage']['completion_tokens']}")
```

## References

- [OpenAI Vision Guide](https://platform.openai.com/docs/guides/vision)
- [Claude Vision](https://docs.anthropic.com/en/docs/vision)
- [Gemini Vision](https://ai.google.dev/tutorials/python_quickstart#vision)
- Related: [vision-basics.md](vision-basics.md)
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Analyze image content and objects | haiku | Pattern recognition and structured output |
| Compare multiple images for differences | sonnet | Complex visual analysis and reasoning |
| Build vision-based chatbot interface | sonnet | Code integration and architecture |

