# Image Analysis Code Examples

## OCR and Document Analysis

### Basic Text Extraction

```python
from openai import OpenAI
import base64

client = OpenAI()

def extract_text(image_path: str) -> str:
    """Extract all text from an image."""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract all text visible in this image. Maintain formatting where possible."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]
        }]
    )
    return response.choices[0].message.content
```

### Structured Document Extraction

```python
from openai import OpenAI
import base64
import json
from typing import List

client = OpenAI()

def extract_structured_data(image_path: str, fields: List[str]) -> dict:
    """Extract specific fields from a document image."""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    fields_str = ", ".join(fields)
    prompt = f"""Extract these fields from the document: {fields_str}

Return JSON with the field names as keys. Use null for missing fields."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]
        }],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# Usage
data = extract_structured_data("invoice.jpg", ["vendor_name", "invoice_number", "date", "total_amount"])
```

### Receipt Analysis

```python
def analyze_receipt(image_path: str) -> dict:
    """Extract structured data from a receipt."""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    prompt = """Analyze this receipt and extract:
- store_name
- date
- items: list of {name, quantity, price}
- subtotal
- tax
- total
- payment_method (if visible)

Return as JSON."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]
        }],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
```

### Form Extraction

```python
def analyze_form(image_path: str) -> dict:
    """Extract filled fields from a form."""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    prompt = """Analyze this form and extract all filled fields.
Return JSON with field names/labels as keys and filled values as values.
For checkboxes, use true/false.
For empty fields, use null."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]
        }],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
```

## Image Classification

```python
from typing import List, Dict

def classify_image(image_path: str, categories: List[str]) -> Dict:
    """Classify image into predefined categories."""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    categories_str = ", ".join(categories)
    prompt = f"""Classify this image into one of these categories: {categories_str}

Return JSON with:
- category: the best matching category
- confidence: confidence score (0-1)
- reasoning: brief explanation"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]
        }],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# Usage
result = classify_image("photo.jpg", ["landscape", "portrait", "product", "document", "screenshot"])
print(f"Category: {result['category']} ({result['confidence']:.0%})")
```

## Content Moderation

```python
def moderate_image(image_path: str) -> Dict:
    """Check image for inappropriate content."""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

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

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]
        }],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# Usage
result = moderate_image("user_upload.jpg")
if not result["is_safe"]:
    print(f"Warning: {result['severity']} - {result['details']}")
```

## Claude Vision API

```python
import anthropic
import base64

client = anthropic.Anthropic()

def analyze_with_claude(image_path: str, prompt: str) -> str:
    """Analyze image using Claude Vision."""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    # Determine media type
    suffix = image_path.lower().split(".")[-1]
    media_types = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp"
    }
    media_type = media_types.get(suffix, "image/jpeg")

    response = client.messages.create(
        model="claude-sonnet-4-5-20250514",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data
                    }
                },
                {"type": "text", "text": prompt}
            ]
        }]
    )
    return response.content[0].text
```

## Gemini Vision API

```python
import google.generativeai as genai
from PIL import Image

genai.configure(api_key="YOUR_API_KEY")

def analyze_with_gemini(image_path: str, prompt: str) -> str:
    """Analyze image using Gemini Vision."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    image = Image.open(image_path)

    response = model.generate_content([prompt, image])
    return response.text

def analyze_multiple_images(image_paths: list, prompt: str) -> str:
    """Analyze multiple images with Gemini (up to 3600 images)."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    images = [Image.open(path) for path in image_paths]

    response = model.generate_content([prompt] + images)
    return response.text
```

## Multi-Provider Fallback

```python
from typing import Optional, Dict, Any

class VisionService:
    """Vision service with multi-provider fallback."""

    def __init__(self):
        self.openai = OpenAI()
        self.anthropic = anthropic.Anthropic()

    def analyze(self, image_path: str, prompt: str) -> Dict[str, Any]:
        """Analyze with fallback between providers."""
        # Try OpenAI first
        try:
            result = self._analyze_openai(image_path, prompt)
            return {"success": True, "provider": "openai", "content": result}
        except Exception as e:
            print(f"OpenAI failed: {e}")

        # Fallback to Claude
        try:
            result = self._analyze_claude(image_path, prompt)
            return {"success": True, "provider": "claude", "content": result}
        except Exception as e:
            print(f"Claude failed: {e}")

        return {"success": False, "error": "All providers failed"}

    def _analyze_openai(self, image_path: str, prompt: str) -> str:
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        response = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]
            }]
        )
        return response.choices[0].message.content

    def _analyze_claude(self, image_path: str, prompt: str) -> str:
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        response = self.anthropic.messages.create(
            model="claude-sonnet-4-5-20250514",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_data}},
                    {"type": "text", "text": prompt}
                ]
            }]
        )
        return response.content[0].text
```

## Batch Processing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def batch_analyze(image_paths: list, prompt: str, max_workers: int = 5) -> list:
    """Analyze multiple images concurrently."""

    def analyze_single(path: str) -> dict:
        try:
            result = extract_text(path)
            return {"path": path, "success": True, "content": result}
        except Exception as e:
            return {"path": path, "success": False, "error": str(e)}

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        tasks = [loop.run_in_executor(executor, analyze_single, path) for path in image_paths]
        results = await asyncio.gather(*tasks)

    return results

# Usage
# results = asyncio.run(batch_analyze(["img1.jpg", "img2.jpg", "img3.jpg"], "Extract text"))
```
