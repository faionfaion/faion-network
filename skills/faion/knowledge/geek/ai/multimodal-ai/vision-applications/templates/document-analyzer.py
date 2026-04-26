"""DocumentAnalyzer and VisionService with config dataclass."""
from openai import OpenAI
from dataclasses import dataclass
from typing import Optional, Union, Any
from pathlib import Path
from enum import Enum
import base64
import json
import logging


class ImageSource(Enum):
    URL = "url"
    FILE = "file"
    BASE64 = "base64"


@dataclass
class VisionConfig:
    model: str = "gpt-4o"
    max_image_size_mb: int = 20
    detail: str = "auto"   # "low" | "high" | "auto"
    max_retries: int = 3
    timeout: int = 60


class DocumentAnalyzer:
    """Extract text and structured fields from documents."""

    def __init__(self, model: str = "gpt-4o"):
        self.client = OpenAI()
        self.model = model

    def extract_text(self, image_path: str) -> str:
        return self._analyze(image_path, "Extract all text. Maintain formatting where possible.")

    def extract_structured_data(self, image_path: str, fields: list[str]) -> dict:
        fields_str = ", ".join(fields)
        prompt = (
            f"Extract these fields: {fields_str}. "
            "Return JSON with field names as keys. Use null for missing fields."
        )
        response = self._analyze(image_path, prompt, json_mode=True)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {}

    def analyze_receipt(self, image_path: str) -> dict:
        prompt = (
            "Extract store_name, date, items (list of name/quantity/price), "
            "subtotal, tax, total, payment_method. Return JSON."
        )
        try:
            return json.loads(self._analyze(image_path, prompt, json_mode=True))
        except json.JSONDecodeError:
            return {}

    def _analyze(self, image_path: str, prompt: str, json_mode: bool = False) -> str:
        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]}]
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content


class VisionService:
    """Production vision service with size validation and retry."""

    MEDIA_TYPES = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp"
    }

    def __init__(self, config: Optional[VisionConfig] = None):
        self.config = config or VisionConfig()
        self.client = OpenAI()
        self.logger = logging.getLogger(__name__)

    def analyze(self, image: Union[str, Path], prompt: str,
                source_type: ImageSource = ImageSource.FILE,
                structured_output: bool = False) -> dict[str, Any]:
        try:
            image_content = self._prepare_image(image, source_type)
            messages = [{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": image_content, "detail": self.config.detail}}
            ]}]
            kwargs: dict[str, Any] = {
                "model": self.config.model,
                "messages": messages,
                "timeout": self.config.timeout
            }
            if structured_output:
                kwargs["response_format"] = {"type": "json_object"}

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
            return {"success": False, "error": str(e)}

    def _prepare_image(self, image: Union[str, Path], source_type: ImageSource) -> str:
        if source_type == ImageSource.URL:
            return str(image)
        if source_type == ImageSource.BASE64:
            return f"data:image/jpeg;base64,{image}"
        path = Path(image)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > self.config.max_image_size_mb:
            raise ValueError(f"Image too large: {size_mb:.1f}MB > {self.config.max_image_size_mb}MB")
        with open(path, "rb") as f:
            data = base64.standard_b64encode(f.read()).decode()
        media_type = self.MEDIA_TYPES.get(path.suffix.lower(), "image/jpeg")
        return f"data:{media_type};base64,{data}"
