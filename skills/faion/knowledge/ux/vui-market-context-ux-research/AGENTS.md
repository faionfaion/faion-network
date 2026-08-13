# VUI Market Context

## Summary

**One-sentence:** Generates a one-page voice market brief with sourced adoption stats + platform comparison weighted by target geo.

**One-paragraph:** Voice market context grounds a platform-selection or stakeholder pitch in concrete, sourced figures rather than anecdote. Every statistic carries value + year + source URL + geographic scope; briefs older than 90 days are refused. Five platforms in scope: Alexa, Google Assistant, Siri, Bixby, custom LLM-VUI (treated as a distinct fifth category, not a feature). Refresh runs via Anthropic web_search against an explicit trusted-source allowlist (Statista, Voicebot.ai, Edison/Infinite Dial, NN/g, Pew, Gartner). Output is a markdown brief plus a JSON metric snapshot fit for re-use.

**Ефективно для:**

- Платформне рішення (Alexa vs Google vs Siri vs LLM-native) для voice-продукту на 2-річний горизонт.
- Quarterly refresh короткої довідки для stakeholder/investor deck — без застарілих цифр.
- Pitch до інвестора з обґрунтованими adoption-статистиками + scope per geo.
- Платформний trade-off-аналіз з акцентом на target geo, а не глобальну частку.

## Applies If (ALL must hold)

- Strategy phase of a voice-product proposal: ground the deck in current adoption stats and platform tradeoffs.
- Platform-selection decision: Alexa vs Google Assistant vs Siri vs custom LLM-VUI by developer surface and user reach in target geos.
- Quarterly brief refresh: market data ages fast — agents pull current numbers on demand instead of relying on stale README values.

## Skip If (ANY kills it)

- Implementation work — this methodology is descriptive market context, not how-to.
- Single-vendor decisions already locked — re-justification is not useful.
- Real-time competitive intelligence — use a market-research methodology with monitoring loops instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target geos list | YAML list of ISO country codes | product brief |
| Trusted source allowlist | text list | this methodology |
| ANTHROPIC_API_KEY | env var | provider account |
| Metric list | text list of ≥4 metrics | this methodology default |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[market-researcher]] | Upstream — supplies general market-data normalization rules |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: scoped-stat-fields, denominator-discipline, 90-day-freshness, trusted-source-allowlist, llm-native-as-platform | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for brief + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: hallucinated-stats, mixed-denominators, geo-scope-confusion, stale-brief | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure: collect → refresh → normalize → assemble → publish | 800 |
| `content/05-examples.xml` | essential | Worked brief example for a US+EU smart-speaker product | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree: brief age + scope completeness → action | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `refresh-metrics-from-web` | sonnet | Web search + JSON normalization, mechanical. |
| `assemble-brief-narrative` | sonnet | Light judgment composing per-geo narrative. |
| `validate-brief-schema` | haiku | Schema check is deterministic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/refresh-script.py` | Anthropic web_search refresh runner emitting `vui_market_brief.json` |
| `templates/brief.md` | Markdown brief skeleton with stats + platform comparison sections |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[market-researcher]]
- [[vui-conversation-design]]
- [[core-vui-design-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs (brief age, presence of geo scope, denominator type) to an action, each leaf referencing a rule from `01-core-rules.xml`. Use it when deciding whether to publish, refresh, or reject a candidate stat.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/refresh-script.py`

```python
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
```
