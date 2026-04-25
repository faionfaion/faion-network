# Agent Integration — VUI Market Context

## When to use
- Strategy phase of a voice-product proposal: ground the deck in current adoption stats and platform tradeoffs.
- Platform-selection decision: choose Alexa vs Google Assistant vs Siri vs custom LLM-VUI based on developer surface and user reach in target geos.
- Quarterly brief refresh: market data ages fast; agents pull current numbers on demand instead of relying on stale README values.
- Investor / stakeholder primers: a one-page market context written from canonical sources (Statista, Voicebot.ai, NNg, Gartner).

## When NOT to use
- Implementation work — this methodology is descriptive market context, not how-to.
- Single-vendor decisions already locked — re-justifying Alexa when SKK is mandated wastes cycles.
- Real-time competitive intelligence — use a market-research methodology with monitoring loops instead.

## Where it fails / limitations
- The README's adoption numbers will go stale within 6-12 months; agents must re-fetch or flag the brief as dated.
- "Voice assistant" is conflated across platforms (smart speakers, phone assistants, in-car, embedded LLMs). Numbers from different sources are not comparable.
- Most public stats are US/EU-skewed; LATAM, MENA, APAC voice usage patterns are reported less consistently.
- LLM-only voice agents (ChatGPT Voice, Claude voice mode, Pi, etc.) are reshaping the landscape faster than the canonical 2024-25 sources track.

## Agentic workflow
This methodology is reference content, not a workflow. Drive it as: a research agent fetches the latest stats from named sources via WebSearch + WebFetch, normalizes them into the same schema as the existing README, and produces a delta report ("3 numbers changed since last brief"). A strategy agent then assembles the platform-comparison section keyed to the user's target geos, devices, and language coverage.

### Recommended subagents
- `faion-market-researcher` (from `pro/research/market-researcher`) — pulls and normalizes market stats.
- `faion-product-manager` — translates market context into a platform-selection recommendation.
- `faion-gtm-strategist` (from `pro/marketing/gtm-strategist`) — folds adoption stats into go-to-market positioning.
- `faion-ux-researcher-agent` — connects market patterns to user-research priorities (which segments, which contexts).

### Prompt pattern
Stat refresh:
```
Find the most recent (2025-2026) figures for: {metric_list}.
For each, return: value, year, source URL, geographic scope. Reject sources older than 18 months unless no newer source exists. Output as JSON.
```
Platform comparison:
```
Compare {platforms} on: developer SDK quality, supported locales, monetization, user reach in {target_geos}, openness to LLM integration. Output a markdown table + a 3-sentence recommendation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Inspect platform SDK repos for activity signals | `brew install gh` |
| Anthropic SDK + WebSearch tool | Live source-grounded refresh | https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/web-search-tool |
| `jq` | Parse market-data JSON exports | distro package |
| `markdown-it` / `pandoc` | Render briefs to PDF/HTML for stakeholders | `brew install pandoc` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Statista | SaaS | Partial — most behind paywall | Primary canonical source for voice adoption stats |
| Voicebot.ai | SaaS (free reports) | Yes — public RSS + reports | Tracks voice industry; free annual surveys |
| eMarketer / Insider Intelligence | SaaS | Partial — paywalled | Forecasts, demographic breakdowns |
| Gartner | SaaS | Partial — paywalled | Hype cycle, predictions |
| Edison Research | SaaS | Public PDFs | "Smart Audio Report" (now Infinite Dial) |
| Pew Research | Free | Yes | US adoption baselines |
| Alexa Skills Kit | SaaS | Yes — full SDK | Ecosystem comparison input |
| Google Actions | SaaS | Yes — full SDK; deprecated for some surfaces | Note: Google deprecated Conversational Actions in 2023 |
| SiriKit | SaaS | Limited — restricted intent set | Requires native iOS app; no third-party voice apps |
| Bixby Developer Studio | SaaS | Yes | Samsung-only; small reach outside Korea |
| OpenAI Realtime API / ElevenLabs Conversational | SaaS | Yes — APIs | Custom LLM-VUI route bypassing platform constraints |

## Templates & scripts
This is a reference doc; the relevant template is the comparison table in the README. Minimal refresh helper:

```python
# refresh_vui_brief.py
import anthropic, json, datetime, pathlib
METRICS = [
    "voice assistants in use globally",
    "% US adults using voice assistants",
    "% households with smart speakers",
    "voice search share of internet queries",
]
client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-opus-4-7", max_tokens=2000,
    tools=[{"type":"web_search_20250305","name":"web_search"}],
    messages=[{"role":"user","content":
        f"For each metric, return latest 2025-2026 figure with source URL: {METRICS}. "
        "JSON list of {metric, value, year, source_url, geo}."}],
)
out = {"refreshed_at": datetime.date.today().isoformat(),
       "data": json.loads(msg.content[-1].text)}
pathlib.Path("vui_market_brief.json").write_text(json.dumps(out, indent=2))
```

## Best practices
- Always cite the source year and geo with every stat; "62% use voice assistants" without scope is uselessly vague.
- Compare apples to apples: distinguish "smart speaker households" from "voice-assistant users" from "voice-search query share".
- Refresh quarterly minimum; voice adoption moved sharply post-LLM (ChatGPT Voice, Pi, Claude voice). Stats older than 12 months are likely wrong on direction, not just magnitude.
- For platform selection, weight reach by *target geo*, not global. Alexa dominates US smart speakers; Google Assistant dominates Android phones globally; Siri dominates iOS; none of these flips a wrong-platform decision.
- Treat LLM-native voice agents as a fifth platform, not a feature — they bypass skill stores and certification entirely.

## AI-agent gotchas
- LLMs hallucinate plausible-looking statistics with fake source URLs. Require the agent to return source URL + access date and verify URLs resolve.
- WebSearch results often surface SEO content farms (top results = "10 voice assistant statistics" listicles citing each other). Restrict trusted-source list explicitly: Statista, NNg, Gartner, Edison/NPR, Pew, Voicebot.
- Stats expressed in different units (devices vs users vs households) get mixed in synthesis. Normalize to a single denominator before comparison.
- Market briefs go stale silently. Stamp every brief with `refreshed_at` and refuse to publish if older than 90 days.
- Geographic scope mismatch: a "US adoption" stat used as "global" inflates by 3-5x. Always validate geo before reusing.

## References
- Voicebot.ai — Voice Assistant Statistics: https://www.voicebot.ai/voice-assistant-statistics/
- Edison Research — Infinite Dial: https://www.edisonresearch.com/the-infinite-dial-2024/
- Nielsen Norman Group — Voice Interaction: https://www.nngroup.com/articles/voice-interaction/
- Statista — Voice Assistants topic: https://www.statista.com/topics/4642/voice-assistants/
- Pew Research — Mobile fact sheet: https://www.pewresearch.org/internet/fact-sheet/mobile/
- OpenAI Realtime API: https://platform.openai.com/docs/guides/realtime
