# Image Analysis Templates

## Production Vision Service

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from pathlib import Path
import logging
import base64
import json

from openai import OpenAI

class ImageSource(Enum):
    URL = "url"
    FILE = "file"
    BASE64 = "base64"

@dataclass
class VisionConfig:
    """Configuration for vision service."""
    model: str = "gpt-4o"
    max_image_size_mb: int = 20
    detail: str = "auto"  # "low", "high", "auto"
    max_retries: int = 3
    timeout: int = 60
    temperature: float = 0.0  # Zero for deterministic extraction

@dataclass
class VisionResult:
    """Result from vision analysis."""
    success: bool
    content: Optional[Union[str, dict]] = None
    error: Optional[str] = None
    usage: Dict[str, int] = field(default_factory=dict)
    model: Optional[str] = None

class VisionService:
    """Production-grade vision analysis service."""

    MEDIA_TYPES = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }

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
    ) -> VisionResult:
        """Analyze image with error handling and retries."""
        try:
            image_content = self._prepare_image(image, source_type)

            messages = [{
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
            }]

            kwargs = {
                "model": self.config.model,
                "messages": messages,
                "timeout": self.config.timeout,
                "temperature": self.config.temperature
            }

            if structured_output:
                kwargs["response_format"] = {"type": "json_object"}

            # Retry loop
            last_error = None
            for attempt in range(self.config.max_retries):
                try:
                    response = self.client.chat.completions.create(**kwargs)
                    content = response.choices[0].message.content

                    return VisionResult(
                        success=True,
                        content=json.loads(content) if structured_output else content,
                        usage={
                            "prompt_tokens": response.usage.prompt_tokens,
                            "completion_tokens": response.usage.completion_tokens
                        },
                        model=response.model
                    )
                except Exception as e:
                    last_error = e
                    self.logger.warning(f"Attempt {attempt + 1}/{self.config.max_retries} failed: {e}")

            raise last_error

        except Exception as e:
            self.logger.error(f"Vision analysis failed: {e}")
            return VisionResult(success=False, error=str(e))

    def _prepare_image(self, image: Union[str, Path], source_type: ImageSource) -> str:
        """Prepare image for API request."""
        if source_type == ImageSource.URL:
            return str(image)

        if source_type == ImageSource.BASE64:
            return f"data:image/jpeg;base64,{image}"

        # FILE
        path = Path(image)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")

        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > self.config.max_image_size_mb:
            raise ValueError(f"Image too large: {size_mb:.1f}MB (max: {self.config.max_image_size_mb}MB)")

        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()

        media_type = self.MEDIA_TYPES.get(path.suffix.lower(), "image/jpeg")
        return f"data:{media_type};base64,{data}"

    def batch_analyze(
        self,
        images: List[Union[str, Path]],
        prompt: str,
        source_type: ImageSource = ImageSource.FILE
    ) -> List[VisionResult]:
        """Analyze multiple images sequentially."""
        return [self.analyze(img, prompt, source_type) for img in images]
```

## Document Analyzer Template

```python
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class DocumentField:
    """Definition of a field to extract."""
    name: str
    description: str
    required: bool = True
    field_type: str = "string"  # string, number, boolean, array

class DocumentAnalyzer:
    """Analyze documents and extract structured data."""

    def __init__(self, model: str = "gpt-4o"):
        self.service = VisionService(VisionConfig(model=model))

    def extract_fields(
        self,
        image_path: str,
        fields: List[DocumentField]
    ) -> Dict[str, Any]:
        """Extract specific fields from document."""
        field_descriptions = "\n".join([
            f"- {f.name} ({f.field_type}): {f.description}" + (" [REQUIRED]" if f.required else " [OPTIONAL]")
            for f in fields
        ])

        prompt = f"""Extract these fields from the document:

{field_descriptions}

Return JSON with field names as keys.
Use null for missing optional fields.
For required fields that cannot be found, use null and explain in an "_errors" array."""

        result = self.service.analyze(image_path, prompt, structured_output=True)

        if result.success:
            return result.content
        raise ValueError(f"Extraction failed: {result.error}")

    def analyze_invoice(self, image_path: str) -> Dict[str, Any]:
        """Extract invoice data."""
        fields = [
            DocumentField("vendor_name", "Name of the vendor/seller"),
            DocumentField("vendor_address", "Full address of vendor", required=False),
            DocumentField("invoice_number", "Invoice or reference number"),
            DocumentField("invoice_date", "Date of the invoice (YYYY-MM-DD format)"),
            DocumentField("due_date", "Payment due date (YYYY-MM-DD format)", required=False),
            DocumentField("line_items", "List of items with name, quantity, unit_price, total", field_type="array"),
            DocumentField("subtotal", "Subtotal before tax", field_type="number"),
            DocumentField("tax_amount", "Tax amount", field_type="number"),
            DocumentField("total_amount", "Total amount due", field_type="number"),
            DocumentField("currency", "Currency code (USD, EUR, etc.)"),
        ]
        return self.extract_fields(image_path, fields)

    def analyze_receipt(self, image_path: str) -> Dict[str, Any]:
        """Extract receipt data."""
        fields = [
            DocumentField("store_name", "Name of the store"),
            DocumentField("store_address", "Store address", required=False),
            DocumentField("date", "Transaction date (YYYY-MM-DD format)"),
            DocumentField("time", "Transaction time (HH:MM format)", required=False),
            DocumentField("items", "List of purchased items with name, quantity, price", field_type="array"),
            DocumentField("subtotal", "Subtotal before tax", field_type="number"),
            DocumentField("tax", "Tax amount", field_type="number"),
            DocumentField("total", "Total amount", field_type="number"),
            DocumentField("payment_method", "How payment was made", required=False),
            DocumentField("card_last_four", "Last 4 digits of card", required=False),
        ]
        return self.extract_fields(image_path, fields)

    def analyze_id_document(self, image_path: str) -> Dict[str, Any]:
        """Extract ID document data (passport, driver's license, etc.)."""
        fields = [
            DocumentField("document_type", "Type of ID (passport, driver_license, id_card)"),
            DocumentField("full_name", "Full name as shown"),
            DocumentField("date_of_birth", "Date of birth (YYYY-MM-DD format)"),
            DocumentField("document_number", "ID/document number"),
            DocumentField("expiry_date", "Expiration date (YYYY-MM-DD format)", required=False),
            DocumentField("issuing_country", "Country that issued the document"),
            DocumentField("nationality", "Nationality", required=False),
            DocumentField("gender", "Gender (M/F)", required=False),
        ]
        return self.extract_fields(image_path, fields)
```

## Image Classification Template

```python
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ClassificationResult:
    category: str
    confidence: float
    reasoning: str
    alternatives: Optional[List[Dict[str, float]]] = None

class ImageClassifier:
    """Classify images into predefined categories."""

    def __init__(self, categories: List[str], model: str = "gpt-4o"):
        self.categories = categories
        self.service = VisionService(VisionConfig(model=model))

    def classify(self, image_path: str, return_alternatives: bool = False) -> ClassificationResult:
        """Classify image into one of the predefined categories."""
        categories_str = ", ".join(self.categories)

        prompt = f"""Classify this image into one of these categories: {categories_str}

Return JSON with:
- category: the best matching category (must be one of the listed categories)
- confidence: confidence score from 0 to 1
- reasoning: brief explanation for the classification
{"- alternatives: list of other possible categories with their confidence scores" if return_alternatives else ""}"""

        result = self.service.analyze(image_path, prompt, structured_output=True)

        if not result.success:
            raise ValueError(f"Classification failed: {result.error}")

        data = result.content
        return ClassificationResult(
            category=data["category"],
            confidence=data["confidence"],
            reasoning=data["reasoning"],
            alternatives=data.get("alternatives")
        )

    def classify_batch(self, image_paths: List[str]) -> List[ClassificationResult]:
        """Classify multiple images."""
        return [self.classify(path) for path in image_paths]
```

## Content Moderation Template

```python
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class ModerationSeverity(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class ModerationResult:
    is_safe: bool
    flags: List[str]
    severity: ModerationSeverity
    details: str
    categories: Dict[str, bool]

class ContentModerator:
    """Moderate image content for safety."""

    CATEGORIES = [
        "violence",
        "gore",
        "adult_content",
        "hate_symbols",
        "dangerous_activities",
        "illegal_content",
        "self_harm",
        "harassment",
        "spam"
    ]

    def __init__(self, model: str = "gpt-4o"):
        self.service = VisionService(VisionConfig(model=model))

    def moderate(self, image_path: str) -> ModerationResult:
        """Check image for inappropriate content."""
        categories_str = ", ".join(self.CATEGORIES)

        prompt = f"""Analyze this image for content moderation.

Check for these categories: {categories_str}

Return JSON with:
- is_safe: boolean indicating if content is safe for general audiences
- flags: list of specific issues found (empty if none)
- severity: "none", "low", "medium", or "high"
- details: brief explanation of findings
- categories: object with each category as key and boolean as value (true if detected)"""

        result = self.service.analyze(image_path, prompt, structured_output=True)

        if not result.success:
            raise ValueError(f"Moderation failed: {result.error}")

        data = result.content
        return ModerationResult(
            is_safe=data["is_safe"],
            flags=data["flags"],
            severity=ModerationSeverity(data["severity"]),
            details=data["details"],
            categories=data["categories"]
        )

    def should_reject(self, result: ModerationResult) -> bool:
        """Determine if content should be rejected."""
        return result.severity in [ModerationSeverity.MEDIUM, ModerationSeverity.HIGH]

    def should_review(self, result: ModerationResult) -> bool:
        """Determine if content needs human review."""
        return result.severity == ModerationSeverity.LOW
```

## Accessibility Alt Text Generator

```python
from typing import Optional
from dataclasses import dataclass

@dataclass
class AltTextResult:
    short_description: str  # For alt attribute (125 chars max)
    long_description: str   # For extended description
    key_elements: list      # Main visual elements identified

class AltTextGenerator:
    """Generate accessible alt text for images."""

    def __init__(self, model: str = "gpt-4o"):
        self.service = VisionService(VisionConfig(model=model))

    def generate(self, image_path: str, context: Optional[str] = None) -> AltTextResult:
        """Generate alt text for an image."""
        context_note = f"\nContext: {context}" if context else ""

        prompt = f"""Generate accessible alt text for this image.{context_note}

Return JSON with:
- short_description: Concise alt text (max 125 characters) for screen readers
- long_description: Detailed description (2-3 sentences) for those who want more detail
- key_elements: List of main visual elements in the image

Guidelines:
- Be specific and descriptive
- Avoid "image of" or "picture of"
- Include relevant text visible in the image
- Describe the purpose/function if it's a functional image
- For decorative images, indicate if description should be empty"""

        result = self.service.analyze(image_path, prompt, structured_output=True)

        if not result.success:
            raise ValueError(f"Alt text generation failed: {result.error}")

        data = result.content
        return AltTextResult(
            short_description=data["short_description"][:125],
            long_description=data["long_description"],
            key_elements=data["key_elements"]
        )
```

## Usage Examples

```python
# Document Analysis
analyzer = DocumentAnalyzer()
invoice_data = analyzer.analyze_invoice("invoice.png")
print(f"Invoice #{invoice_data['invoice_number']}: ${invoice_data['total_amount']}")

# Image Classification
classifier = ImageClassifier(
    categories=["product_photo", "lifestyle", "infographic", "screenshot", "document"]
)
result = classifier.classify("marketing_image.jpg")
print(f"Category: {result.category} ({result.confidence:.0%})")

# Content Moderation
moderator = ContentModerator()
mod_result = moderator.moderate("user_upload.jpg")
if moderator.should_reject(mod_result):
    print(f"REJECTED: {mod_result.details}")
elif moderator.should_review(mod_result):
    print(f"NEEDS REVIEW: {mod_result.flags}")
else:
    print("APPROVED")

# Alt Text Generation
alt_gen = AltTextGenerator()
alt_text = alt_gen.generate("hero_image.jpg", context="Homepage hero section")
print(f'<img alt="{alt_text.short_description}" />')
```
