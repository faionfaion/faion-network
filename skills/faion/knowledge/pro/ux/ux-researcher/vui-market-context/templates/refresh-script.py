"""
refresh-script.py — refresh VUI market statistics via Claude web_search tool.

Usage: python refresh-script.py
Output: vui_market_brief.json — {refreshed_at, data: [{metric, value, year, source_url, geo}]}

Requires: pip install anthropic
ANTHROPIC_API_KEY must be set in environment.
"""
import anthropic, json, datetime, pathlib

METRICS = [
    "voice assistants in use globally (total devices or users)",
    "percentage of internet users using voice search",
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

client = anthropic.Anthropic()

msg = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=2000,
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    messages=[{
        "role": "user",
        "content": (
            f"Find the most recent (2025-2026) figures for each metric below. "
            f"Restrict sources to: {', '.join(TRUSTED_SOURCES)}. "
            "Reject sources older than 18 months unless no newer primary source exists. "
            "Reject SEO listicles — require primary research sources only.\n\n"
            "Metrics:\n" + "\n".join(f"- {m}" for m in METRICS) + "\n\n"
            "Return JSON array of: "
            "[{metric, value, year, source_url, geo, confidence: high|medium|low}]"
        ),
    }],
)

# Extract JSON from last content block
data_text = msg.content[-1].text
try:
    data = json.loads(data_text)
except json.JSONDecodeError:
    import re
    match = re.search(r"\[.*\]", data_text, re.DOTALL)
    data = json.loads(match.group()) if match else []

out = {
    "refreshed_at": datetime.date.today().isoformat(),
    "model": "claude-opus-4-7",
    "data": data,
}

out_path = pathlib.Path("vui_market_brief.json")
out_path.write_text(json.dumps(out, indent=2))
print(f"Refreshed {len(data)} metrics → {out_path}")
print(f"Stamp: {out['refreshed_at']}")
