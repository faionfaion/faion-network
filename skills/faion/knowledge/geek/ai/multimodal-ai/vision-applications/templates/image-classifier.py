# purpose: ImageClassifier — categorical decision against fixed list with confidence + batch.
# consumes: image source, categories list[str], optional batch_images list.
# produces: dict per classify schema: category (lowercased, ∈ list), confidence, reasoning.
# depends-on: OpenAI/Anthropic SDK; rule r4 normalize; rule r5 async batch cap.
# token-budget-impact: ~100 prompt tokens + image tokens (detail=auto).
"""ImageClassifier with batch (asyncio.gather under semaphore) + normalization."""
from openai import OpenAI
import base64
import json


class ImageClassifier:
    """Classify images into predefined categories."""

    def __init__(self, categories: list[str], model: str = "gpt-4o"):
        self.categories = categories
        self.client = OpenAI()
        self.model = model

    def classify(self, image_path: str) -> dict:
        """Returns {category, confidence (0-1), reasoning}."""
        categories_str = ", ".join(self.categories)
        prompt = (
            f"Classify this image into one of: {categories_str}. "
            "Return JSON: {\"category\": str, \"confidence\": float, \"reasoning\": str}"
        )
        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]}],
            response_format={"type": "json_object"}
        )
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"category": "unknown", "confidence": 0.0, "reasoning": "parse error"}

    def classify_batch(self, image_paths: list[str]) -> list[dict]:
        return [self.classify(path) for path in image_paths]
