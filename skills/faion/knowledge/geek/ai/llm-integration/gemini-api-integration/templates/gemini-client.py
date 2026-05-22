"""
purpose: Reference Gemini integration with Files API + safety settings + retry.
consumes: gemini-config.json + media inputs
produces: model response with finish_reason + block_reason surfaced
depends-on: content/01-core-rules.xml; content/02-output-contract.xml
token-budget-impact: per-request cost depends on model + media size
"""
from __future__ import annotations

import time
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


def make_client(api_key: str):
    if genai is None:
        raise SystemExit("google-genai required: pip install google-genai")
    return genai.Client(api_key=api_key)


def upload_if_large(client, path: Path, threshold_kb: int = 10240):
    size_kb = path.stat().st_size / 1024
    if size_kb < threshold_kb:
        return path.read_bytes()
    return client.files.upload(file=str(path))


def call_with_retry(client, model: str, contents, gen_cfg: dict, safety: list[dict], max_attempts: int = 5) -> dict:
    for attempt in range(max_attempts):
        try:
            resp = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(**gen_cfg, safety_settings=[types.SafetySetting(**s) for s in safety]),
            )
            cand = resp.candidates[0]
            return {
                "text": resp.text if cand.finish_reason.name == "STOP" else "",
                "finish_reason": cand.finish_reason.name,
                "block_reason": getattr(resp.prompt_feedback, "block_reason", None),
            }
        except Exception as e:
            if "429" in str(e) and attempt < max_attempts - 1:
                time.sleep(min(2 ** attempt, 60))
                continue
            raise
    return {"text": "", "finish_reason": "RETRY_EXHAUSTED", "block_reason": None}
