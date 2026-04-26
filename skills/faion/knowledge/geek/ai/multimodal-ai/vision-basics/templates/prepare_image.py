"""
Image preprocessing: resize to 1024px long edge and base64-encode for VLM API calls.
Reduces token cost by 50-70% vs. full-size images with minimal quality loss for text/diagram tasks.
Anthropic limit: 5MB per image. OpenAI limit: 20MB per image.
"""
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
