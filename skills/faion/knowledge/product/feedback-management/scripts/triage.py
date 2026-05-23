#!/usr/bin/env python3
"""
triage.py — triage one feedback item via LLM with strict JSON schema output.

Usage:
  echo '{"source":"support","user_id":"usr_123","segment":"pro","text":"Can you add Slack integration?"}' | python triage.py

Input JSON: {source, user_id, segment, text}
Output JSON: {type, topic, sentiment, segment, severity, dedup_hash, source, user_id, suggested_backlog_link, rationale}

Taxonomy must be configured in TAXONOMY list below — treat changes as schema migrations.
PII note: text field must be stripped of email/phone/account IDs before calling this script.
Requires: anthropic Python SDK (pip install anthropic)
"""
import hashlib
import json
import os
import sys

TAXONOMY = [
    "onboarding",
    "billing",
    "integrations",
    "performance",
    "auth",
    "mobile",
    "core-feature",
    "other",
]

VALID_TYPES = ["bug", "request", "enhancement", "confusion", "praise", "complaint"]


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def dedup_hash(text: str) -> str:
    return hashlib.sha1(normalize(text).encode()).hexdigest()[:10]


def triage_via_llm(text: str, segment: str) -> dict:
    try:
        import anthropic
    except ImportError:
        sys.exit("Error: install anthropic SDK: pip install anthropic")

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    taxonomy_str = str(TAXONOMY)

    prompt = f"""Triage this feedback item. Output JSON only — no prose.

Feedback text: {text}
User segment: {segment}
Allowed topics: {taxonomy_str}

Output schema:
{{
  "type": "bug|request|enhancement|confusion|praise|complaint",
  "topic": "<one of the allowed topics>",
  "sentiment": "positive|neutral|negative",
  "severity": 1-5,
  "suggested_backlog_link": "<existing issue id or null>",
  "rationale": "<= 240 chars explaining the classification>"
}}

Rules:
- Use type "bug" if text contains: broken, can't, fails, doesn't work, error
- If topic would not fit any allowed topic, use "other"
- Do NOT invent topics outside the supplied list
- Return ONLY the JSON object, no markdown wrapping"""

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)


def main():
    raw = sys.stdin.read().strip()
    try:
        item = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"JSON parse error: {e}")

    required = ["source", "user_id", "segment", "text"]
    missing = [f for f in required if f not in item]
    if missing:
        sys.exit(f"Missing required fields: {missing}")

    result = triage_via_llm(item["text"], item.get("segment", "unknown"))

    # Validate output
    if result.get("topic") not in TAXONOMY:
        result["topic"] = "other"
    if result.get("type") not in VALID_TYPES:
        result["type"] = "enhancement"

    result["dedup_hash"] = dedup_hash(item["text"])
    result["source"] = item["source"]
    result["user_id"] = item["user_id"]

    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
