# purpose: ContentModerator — policy-category VLM call with severity + human-review gate.
# consumes: image source, policy_categories list, confidence_threshold (default 0.7).
# produces: dict per moderate schema: is_safe, flags, severity, needs_human_review.
# depends-on: OpenAI SDK; rule r4 normalization; rule r6 review threshold.
# token-budget-impact: ~150 prompt tokens + image tokens.
"""ContentModerator with severity normalization and human-review gate."""
from openai import OpenAI
import base64
import json


class ContentModerator:
    """Check images for policy violations. Never use as sole moderation layer."""

    PROMPT = """Analyze for policy violations.
Categories: violence, adult_content, hate_symbols, self_harm, illegal_activity.
Return JSON:
{
  "is_safe": true|false,
  "flags": [list of categories violated],
  "severity": "none" | "low" | "medium" | "high",
  "confidence": 0.0-1.0,
  "needs_human_review": true|false,
  "details": "brief explanation"
}
Set needs_human_review: true when confidence < 0.7.
Always use lowercase severity values."""

    def __init__(self, model: str = "gpt-4o"):
        self.client = OpenAI()
        self.model = model

    def moderate(self, image_path: str) -> dict:
        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": [
                {"type": "text", "text": self.PROMPT},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]}],
            response_format={"type": "json_object"}
        )
        try:
            result = json.loads(response.choices[0].message.content)
            # Normalize severity to lowercase — model occasionally returns uppercase
            if "severity" in result:
                result["severity"] = result["severity"].lower()
            return result
        except json.JSONDecodeError:
            return {"is_safe": False, "flags": [], "severity": "none",
                    "confidence": 0.0, "needs_human_review": True,
                    "details": "parse error"}
