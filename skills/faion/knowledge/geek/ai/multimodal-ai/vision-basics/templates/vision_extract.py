"""
Vision extraction: analyze_image_url, analyze_local_image, structured_analysis, VisualQA.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Optional

from openai import OpenAI
from pydantic import BaseModel


client = OpenAI()

MEDIA_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def _encode_local(image_path: str) -> tuple[str, str]:
    """Read image, return (base64_data, media_type). Does NOT resize — use prepare_image for that."""
    with open(image_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode()
    media_type = MEDIA_TYPES.get(Path(image_path).suffix.lower(), "image/jpeg")
    return data, media_type


def analyze_image_url(image_url: str, prompt: str = "Describe this image in detail.") -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_url}},
        ]}],
    )
    return response.choices[0].message.content


def analyze_local_image(image_path: str, prompt: str = "Describe this image in detail.") -> str:
    data, media_type = _encode_local(image_path)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{data}"}},
        ]}],
    )
    return response.choices[0].message.content


class DetectedObject(BaseModel):
    name: str
    confidence: float
    description: str


class ImageAnalysis(BaseModel):
    description: str
    objects: list[DetectedObject]
    colors: list[str]
    mood: str
    text_content: Optional[str]
    tags: list[str]
    confidence: str  # "high" | "low"


def structured_analysis(image_path: str, max_retries: int = 2) -> ImageAnalysis:
    """Get structured analysis with parse-with-retry on JSON failure."""
    data, media_type = _encode_local(image_path)
    prompt = (
        "Analyze this image and return JSON with: description, objects (name, confidence 0-1, description), "
        "colors, mood, text_content (or null), tags, confidence (high|low). "
        "Set confidence to low if any field required significant interpretation."
    )
    for attempt in range(max_retries):
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{data}"}},
            ]}],
        )
        try:
            return ImageAnalysis(**json.loads(response.choices[0].message.content))
        except Exception as e:
            prompt = f"Previous response caused parse error: {e}. Return valid JSON with all required fields."
    raise ValueError("structured_analysis failed after retries")


class VisualQA:
    """Stateful visual Q&A: image included only in first turn."""

    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self._history: list[dict] = []
        self._image_data: str | None = None
        self._media_type: str = "image/jpeg"

    def set_image(self, image_path: str) -> None:
        self._image_data, self._media_type = _encode_local(image_path)
        self._history = []

    def ask(self, question: str) -> str:
        if not self._image_data:
            raise ValueError("No image set. Call set_image() first.")
        if not self._history:
            # First turn: include image
            user_msg: dict = {"role": "user", "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": f"data:{self._media_type};base64,{self._image_data}"}},
            ]}
        else:
            user_msg = {"role": "user", "content": question}
        messages = self._history + [user_msg]
        response = client.chat.completions.create(model=self.model, messages=messages)
        answer = response.choices[0].message.content
        self._history.extend([user_msg, {"role": "assistant", "content": answer}])
        return answer
