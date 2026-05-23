"""
purpose: Base64 image-to-data-URL encoder for OpenAI vision message content.
consumes: filesystem path to PNG/JPEG/GIF/WebP image.
produces: data URL string ready for {"type": "image_url", "image_url": {"url": ...}}.
depends-on: stdlib only (base64, pathlib).
token-budget-impact: image tokens are 85 (low) or up to 1105 (high); set `detail` accordingly.
"""
import base64
from pathlib import Path

MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def encode_image_as_data_url(image_path: str) -> str:
    """Encode image file as base64 data URL for use in OpenAI vision requests."""
    path = Path(image_path)
    mime = MIME_TYPES.get(path.suffix.lower(), "image/jpeg")
    with open(image_path, "rb") as f:
        b64 = base64.standard_b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def encode_image_b64(image_path: str) -> tuple[str, str]:
    """Return (base64_data, mime_type) for use in Anthropic/Gemini vision requests."""
    path = Path(image_path)
    mime = MIME_TYPES.get(path.suffix.lower(), "image/jpeg")
    with open(image_path, "rb") as f:
        b64 = base64.standard_b64encode(f.read()).decode("utf-8")
    return b64, mime
