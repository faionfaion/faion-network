# purpose: Resize image to 1024px long edge + base64 encode (rule r1, r2).
# consumes: file path or bytes; max_px parameter (default 1024).
# produces: (base64_str, media_type) tuple ready for VLM payload.
# depends-on: Pillow; provider-cap awareness (5 MB Anthropic, 20 MB OpenAI/Gemini).
# token-budget-impact: zero LLM tokens; reduces downstream image-token cost 50-70%.
"""Image preprocessing: resize 1024px + base64 + media-type detection."""
from __future__ import annotations

import base64
import io

from PIL import Image

FORMAT_TO_MEDIA_TYPE = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "WEBP": "image/webp",
    "GIF": "image/gif",
}


def prepare_image(path: str, max_px: int = 1024) -> tuple[str, str]:
    """
    Resize image to max_px on long edge and base64-encode.
    Returns (base64_data, media_type).
    Call this before any VLM API request with local images.
    """
    img = Image.open(path)
    img.thumbnail((max_px, max_px), Image.LANCZOS)
    buf = io.BytesIO()
    fmt = img.format or "PNG"
    img.save(buf, format=fmt)
    data = base64.standard_b64encode(buf.getvalue()).decode()
    media_type = FORMAT_TO_MEDIA_TYPE.get(fmt, "image/png")
    return data, media_type


def check_size_mb(path: str) -> float:
    """Return file size in MB. Check before API call: Anthropic max 5MB, OpenAI max 20MB."""
    from pathlib import Path
    return Path(path).stat().st_size / (1024 * 1024)
