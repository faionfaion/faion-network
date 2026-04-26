# Agent Integration — VUI Market Context

## When to use
- Drafting a "voice strategy" section in a product spec or pitch deck.
- Picking a target voice platform (Alexa vs. Google Assistant vs. custom LLM) for an MVP.
- Writing competitive landscape or TAM slides for a voice-feature business case.
- Briefing a new hire on the voice ecosystem before they design or build.

## When NOT to use
- Hands-on dialog or interaction design — see `core-vui-design-principles`, `vui-conversation-design`.
- Privacy/security architecture — see `vui-privacy-security`.
- Pure technical evaluation of ASR/NLU vendors — needs benchmark data, not market context.

## Where it fails / limitations
- Adoption stats are coarse and rarely segment by use intensity (62% "use" voice ≠ 62% rely on it).
- The platform table treats Siri/Bixby as developer-accessible; in reality access is gated and shrinking.
- Custom-LLM voice (OpenAI Realtime, Gemini Live, Pipecat) is reshaping the platform list faster than static stats can track.
- Numbers age in months, not years; any deck citing 2024 data without 2026 update is suspect.
- No regional breakdown — adoption in CIS/LATAM differs from US/EU by 20+ points.

## Agentic workflow
Use Claude as a market-research synthesizer: feed the latest 3-5 reports (Statista/Voicebot/Gartner/Edison/NN/g) and produce a cited fact-sheet plus a platform-comparison table. A second pass cross-checks each claim against the source and flags unsupported numbers. Avoid "training-data" recall — always pull fresh URLs via WebFetch and cite.

### Recommended subagents
- `faion-ux-researcher-agent` — synthesize fact-sheet from sources.
- A custom `market-fact-checker` — given a draft, locate a citation for each numeric claim or strike it.
- `faion-brainstorm` — generate platform-fit rationales per use case.

### Prompt pattern
```
Given <urls of 5 source reports>, produce a 1-page market fact-sheet:
- Adoption (region-segmented if available).
- Top 5 platforms with developer access status (open/restricted/closed).
- 3 disruptors (LLM-native voice).
- Each fact must include source URL + publication date.
Strike any claim without a source.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `httpie` / `curl` | Pull JSON from analytics APIs | httpie.io |
| `pandoc` | Convert market reports (PDF/HTML) to clean MD for analysis | pandoc.org |
| `gh api` | Pull voice-related repo trend data | cli.github.com |
| `npm-stat-cli` | Track npm download trends for `alexa-sdk`, `actions-on-google`, `pipecat-ai` | github.com/anvaka/npm-stat |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Statista API | SaaS | Yes (REST) | Paywalled; agent-driven pulls per metric |
| Voicebot.ai | News + reports | Partial | Authoritative voice industry analysis; manual scrape OK |
| Gartner | SaaS | No | License-gated, not agent-driven |
| SimilarWeb API | SaaS | Yes | Voice-app web traffic where applicable |
| Sensor Tower API | SaaS | Yes | Mobile voice-app installs |
| Crunchbase API | SaaS | Yes | Funding signal for voice startups |
| Google Trends (pytrends) | OSS wrapper | Yes | Free signal on voice-feature interest |

## Templates & scripts
Inline source-aggregator stub (≤50 lines):

```python
import json, re, sys, urllib.request
from datetime import datetime

CLAIMS = []
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "research-agent"})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")

def extract(url, html):
    pct = re.findall(r"(\d{1,3})\s*%[^.]{0,80}voice", html, re.I)
    bn = re.findall(r"(\d{1,3}(?:\.\d+)?)\s*billion[^.]{0,80}voice", html, re.I)
    for p in pct: CLAIMS.append({"src": url, "claim": f"{p}% voice", "type": "share"})
    for b in bn: CLAIMS.append({"src": url, "claim": f"{b}B voice", "type": "absolute"})

if __name__ == "__main__":
    for url in sys.argv[1:]:
        try: extract(url, fetch(url))
        except Exception as e: print(f"ERR {url}: {e}", file=sys.stderr)
    json.dump({"date": datetime.utcnow().isoformat(), "claims": CLAIMS}, sys.stdout, indent=2)
```

## Best practices
- Cite source AND publication date in every numeric claim; voice market shifts >20% YoY in some segments.
- Distinguish "users" / "active users" / "paying users" / "transactional users" — usually conflated.
- Show confidence: "Statista 2025: 62%" beats "industry says ~60%".
- For platform decision-making, weight developer access status higher than total install base — closed ecosystems waste investment.
- Always include LLM-native voice as a separate row; treating Realtime API as "just another platform" understates disruption.

## Brief-too-thin note
The methodology README is a market snapshot, not a process. Treat the agent integration as a "market briefing playbook": the agentic value is in keeping the snapshot current, cited, and segmented — not in producing novel design output.

## AI-agent gotchas
- LLMs hallucinate market numbers fluently — never accept a stat without a fetched URL + date.
- Knowledge cutoff bias: model defaults to 2023-2024 stats unless freshness is forced.
- Aggregator sites (Statista, eMarketer) often quote each other in a loop; trace to the primary survey before citing.
- Human-in-loop checkpoint: any number entering an investor deck or contract must be reviewed by a researcher.
- Don't let the agent extrapolate trends ("at this rate, 100% by 2030") — flag and remove.

## References
- Statista — *Voice Assistants Worldwide* — statista.com/topics/4642/voice-assistants
- Voicebot.ai — voicebot.ai/voice-assistant-statistics
- Edison Research / NPR — *Smart Speaker Consumer Adoption Report*
- Gartner — *Voice Technology Predictions*
- Nielsen Norman Group — *Voice Interaction UX*
