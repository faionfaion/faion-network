---
id: vision-basics
name: "Image Analysis - Core Concepts"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
parent: image-analysis-vision
---

# Image Analysis - Core Concepts

## Overview

Vision capabilities enable LLMs to understand, analyze, and describe images. This document covers core concepts, model comparison, and basic implementation patterns.

## Vision Model Comparison

| Model | Max Images | Image Size | Capabilities |
|-------|------------|------------|--------------|
| GPT-4o | 20 | 20MB | Comprehensive understanding |
| GPT-4o-mini | 20 | 20MB | Faster, cost-effective |
| Claude 3.5 Sonnet | 20 | 20MB | Detailed analysis |
| Gemini 1.5 Pro | 3600 | 20MB | Large context, video |

## Image Input Methods

| Method | Use Case |
|--------|----------|
| URL | Public images |
| Base64 | Local files, private images |
| File upload | API-specific handling |

## Basic Implementation

### Single Image Analysis

```python
from openai import OpenAI
import base64
from pathlib import Path

client = OpenAI()

def analyze_image_url(
    image_url: str,
    prompt: str = "Describe this image in detail."
) -> str:
    """Analyze image from URL."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content

def analyze_local_image(
    image_path: str,
    prompt: str = "Describe this image in detail."
) -> str:
    """Analyze local image file."""
    # Read and encode image
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode()

    # Determine media type
    suffix = Path(image_path).suffix.lower()
    media_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }
    media_type = media_types.get(suffix, "image/jpeg")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{image_data}"
                        }
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content
```

### Multiple Image Analysis

```python
def compare_images(
    image_paths: list[str],
    prompt: str = "Compare these images and describe their differences."
) -> str:
    """Analyze and compare multiple images."""
    content = [{"type": "text", "text": prompt}]

    for path in image_paths:
        with open(path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()

        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_data}"
            }
        })

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}]
    )
    return response.choices[0].message.content

def analyze_image_sequence(
    image_paths: list[str],
    prompt: str = "Describe what's happening in this sequence of images."
) -> str:
    """Analyze a sequence of images (e.g., storyboard)."""
    content = [{"type": "text", "text": prompt}]

    for i, path in enumerate(image_paths):
        with open(path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()

        content.append({
            "type": "text",
            "text": f"Image {i + 1}:"
        })
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_data}"
            }
        })

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}]
    )
    return response.choices[0].message.content
```

### Structured Image Analysis

```python
from pydantic import BaseModel, Field
from typing import List, Optional
import json

class BoundingBox(BaseModel):
    x: float
    y: float
    width: float
    height: float

class DetectedObject(BaseModel):
    name: str
    confidence: float
    bounding_box: Optional[BoundingBox] = None
    description: str

class ImageAnalysis(BaseModel):
    description: str
    objects: List[DetectedObject]
    colors: List[str]
    mood: str
    text_content: Optional[str] = None
    tags: List[str]

def structured_analysis(image_path: str) -> ImageAnalysis:
    """Get structured analysis of an image."""
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode()

    prompt = """Analyze this image and return structured JSON with:
- description: Overall description
- objects: List of detected objects with name, confidence (0-1), description
- colors: Dominant colors
- mood: Overall mood/atmosphere
- text_content: Any text visible in the image (or null)
- tags: Relevant tags for categorization

Return valid JSON matching this structure."""

    response = client.chat.completions.create(
        model="gpt-4o",
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

    data = json.loads(response.choices[0].message.content)
    return ImageAnalysis(**data)
```

### Visual QA System

```python
class VisualQA:
    """Visual question answering system."""

    def __init__(self, model: str = "gpt-4o"):
        self.client = OpenAI()
        self.model = model
        self.conversation_history = []
        self.current_image = None

    def set_image(self, image_path: str):
        """Set the image for Q&A."""
        with open(image_path, "rb") as f:
            self.current_image = base64.standard_b64encode(f.read()).decode()
        self.conversation_history = []

    def ask(self, question: str) -> str:
        """Ask a question about the current image."""
        if not self.current_image:
            raise ValueError("No image set. Call set_image() first.")

        # Build messages
        messages = []

        # First message includes image
        if not self.conversation_history:
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{self.current_image}"
                        }
                    }
                ]
            })
        else:
            # Include history and new question
            messages = self.conversation_history.copy()
            messages.append({"role": "user", "content": question})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        answer = response.choices[0].message.content

        # Update history
        if not self.conversation_history:
            self.conversation_history.append(messages[0])
        else:
            self.conversation_history.append({"role": "user", "content": question})

        self.conversation_history.append({"role": "assistant", "content": answer})

        return answer

# Usage
vqa = VisualQA()
vqa.set_image("photo.jpg")
print(vqa.ask("What objects are in this image?"))
print(vqa.ask("What colors do you see?"))
print(vqa.ask("What is the mood of this image?"))
```

## Best Practices

1. **Image Quality**
   - Use appropriate resolution
   - Ensure good lighting/contrast
   - Crop to relevant content

2. **Prompting**
   - Be specific about what to analyze
   - Use structured output for consistency
   - Include context when relevant

3. **Performance**
   - Use "low" detail for simple tasks
   - Resize large images before sending
   - Batch similar analyses

4. **Error Handling**
   - Validate image formats
   - Handle API limits
   - Provide fallbacks

5. **Privacy**
   - Consider data sensitivity
   - Blur/mask personal information
   - Follow data retention policies

## Common Pitfalls

1. **Large Images** - Exceeding size limits
2. **Wrong Format** - Unsupported image types
3. **No Detail Control** - Wasting tokens on high-detail mode
4. **Vague Prompts** - Getting generic descriptions
5. **No Structured Output** - Difficult to parse results
6. **Missing Context** - Not providing enough background

## References

- [OpenAI Vision Guide](https://platform.openai.com/docs/guides/vision)
- [Claude Vision](https://docs.anthropic.com/en/docs/vision)
- [Gemini Vision](https://ai.google.dev/tutorials/python_quickstart#vision)
- Related: [vision-applications.md](vision-applications.md)
