"""
purpose: Vertex AI init with ADC + GCS URI part construction for multimodal calls.
consumes: GCP project + region + media GCS URI
produces: Vertex client + Part list ready for generate_content
depends-on: content/01-core-rules.xml
token-budget-impact: zero — setup side
"""
from __future__ import annotations

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


def vertex_client(project: str, location: str = "us-central1"):
    if genai is None:
        raise SystemExit("google-genai required")
    return genai.Client(vertexai=True, project=project, location=location)


def gcs_part(uri: str, mime_type: str) -> "types.Part":
    if types is None:
        raise SystemExit("google-genai required")
    return types.Part.from_uri(file_uri=uri, mime_type=mime_type)
