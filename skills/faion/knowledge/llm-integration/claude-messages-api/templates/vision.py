# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

"""
Vision helpers for Claude Messages API — analyze local images and URLs.

Usage:
    answer = analyze_screenshot("screenshot.png", "What error is shown?")
    answer = analyze_image_url("https://example.com/chart.png", "Describe this chart")
"""
import base64
from pathlib import Path
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-20250514"

MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def analyze_screenshot(path: str, question: str, max_tokens: int = 1024) -> str:
    """Analyze a local image file using base64 encoding. Image placed before text."""
    p = Path(path)
    media_type = MIME_TYPES.get(p.suffix.lower(), "image/jpeg")
    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode()

    resp = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": data}},
            {"type": "text", "text": question},
        ]}],
    )
    return resp.content[0].text


def analyze_image_url(url: str, question: str, max_tokens: int = 1024) -> str:
    """Analyze an image from a URL. URL must be publicly accessible at inference time."""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "url", "url": url}},
            {"type": "text", "text": question},
        ]}],
    )
    return resp.content[0].text
