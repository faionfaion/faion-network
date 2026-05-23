# purpose: refresh VUI adoption metrics via Anthropic web_search; emit vui_market_brief.json
# consumes: ANTHROPIC_API_KEY env var, METRICS list, TRUSTED_SOURCES allowlist
# produces: vui_market_brief.json conforming to content/02-output-contract.xml
# depends-on: anthropic SDK >= 0.40, content/01-core-rules.xml allowlist
# token-budget-impact: ~3000 tokens per refresh (web search tool + JSON synthesis)
"""refresh-script.py - refresh VUI market statistics via Claude web_search."""
from __future__ import annotations

import datetime
import json
import pathlib
import re
import sys

try:
    import anthropic
except ImportError:
    sys.stderr.write("pip install anthropic\n")
    sys.exit(2)

METRICS = [
    "voice assistants in use globally (total devices or users)",
    "percentage of internet queries using voice search",
    "percentage of US adults using voice assistants",
    "percentage of US households with smart speakers",
    "percentage of users preferring voice over typing for some tasks",
]

TRUSTED_SOURCES = [
    "statista.com",
    "voicebot.ai",
    "edisonresearch.com",
    "nngroup.com",
    "pewresearch.org",
    "gartner.com",
]


def refresh() -> dict:
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{
            "role": "user",
            "content": (
                f"Find most recent (2025-2026) figures for each metric below. "
                f"Restrict sources to: {', '.join(TRUSTED_SOURCES)}. "
                "Reject sources older than 18 months unless no newer primary source exists. "
                "Reject SEO listicles; require primary research sources only.\n\n"
                "Metrics:\n" + "\n".join(f"- {m}" for m in METRICS) + "\n\n"
                "Return JSON array of: [{metric, value, year, source_url, geo, denominator, confidence}]"
            ),
        }],
    )
    text = msg.content[-1].text
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        data = json.loads(match.group()) if match else []
    return {
        "refreshed_at": datetime.date.today().isoformat(),
        "model": "claude-opus-4-7",
        "data": data,
        "platforms": [
            {"name": "Alexa", "reach_by_geo": {}, "sdk_health": "maintained"},
            {"name": "Google Assistant", "reach_by_geo": {}, "sdk_health": "maintained"},
            {"name": "Siri", "reach_by_geo": {}, "sdk_health": "maintained"},
            {"name": "Bixby", "reach_by_geo": {}, "sdk_health": "maintained"},
            {"name": "Custom LLM-VUI", "reach_by_geo": {}, "sdk_health": "active"},
        ],
    }


if __name__ == "__main__":
    out = refresh()
    pathlib.Path("vui_market_brief.json").write_text(json.dumps(out, indent=2))
    sys.stdout.write(f"refreshed {len(out['data'])} metrics @ {out['refreshed_at']}\n")
