"""
purpose: Starter Gemini Python client showing one-shot generate + streaming + chat + JSON output.
consumes: gemini-config-basic.json + os.environ['GEMINI_API_KEY']
produces: model text / streamed chunks / chat-session messages
depends-on: content/01-core-rules.xml
token-budget-impact: per-call cost; bounded by max_output_tokens
"""
from __future__ import annotations

import os

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


def make_client():
    if genai is None:
        raise SystemExit("google-genai required: pip install google-genai")
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def generate_once(client, cfg: dict, prompt: str) -> str:
    resp = client.models.generate_content(
        model=cfg["model"],
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=cfg["temperature"],
            max_output_tokens=cfg["max_output_tokens"],
            response_mime_type=cfg.get("response_mime_type", "text/plain"),
        ),
    )
    return resp.text


def stream(client, cfg: dict, prompt: str):
    for chunk in client.models.generate_content_stream(
        model=cfg["model"],
        contents=prompt,
        config=types.GenerateContentConfig(temperature=cfg["temperature"], max_output_tokens=cfg["max_output_tokens"]),
    ):
        yield chunk.text


def chat_session(client, cfg: dict, history_cap_chars: int = 60000):
    chat = client.chats.create(model=cfg["model"])

    def send(message: str) -> str:
        resp = chat.send_message(message)
        # Trim history to budget (FIFO).
        while sum(len(h.parts[0].text) for h in chat.get_history()) > history_cap_chars:
            chat.get_history().pop(0)
        return resp.text

    return send
