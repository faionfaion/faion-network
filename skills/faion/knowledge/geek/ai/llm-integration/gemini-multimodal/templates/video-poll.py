"""
purpose: Async video upload + polling loop with max-iteration guard and FAILED handling.
consumes: video path + Gemini client + poll_timeout_s
produces: ACTIVE file reference or raises on FAILED/cap
depends-on: content/01-core-rules.xml r2
token-budget-impact: zero — runtime side
"""
from __future__ import annotations

import time

try:
    from google import genai
except ImportError:
    genai = None


def upload_and_wait(client, path: str, poll_timeout_s: int = 300, interval_s: int = 5):
    if genai is None:
        raise SystemExit("google-genai required")
    file = client.files.upload(file=path)
    deadline = time.time() + poll_timeout_s
    while time.time() < deadline:
        f = client.files.get(name=file.name)
        if f.state.name == "ACTIVE":
            return f
        if f.state.name == "FAILED":
            raise RuntimeError(f"Files API upload failed: {f.name}")
        time.sleep(interval_s)
    raise TimeoutError(f"file did not become ACTIVE within {poll_timeout_s}s")
