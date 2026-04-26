# Agent Integration — Focus Groups

## When to use
- Early-stage concept exploration before quantitative or solo-interview research.
- Generating reaction data on copy, naming, value props, packaging, or visual concepts.
- Mapping user vocabulary (how customers describe a problem in their own words).
- Recruiting stakeholder buy-in by letting PMs/execs observe live discussion.

## When NOT to use
- Usability testing — group dynamics drown individual task behavior.
- Sensitive or personal topics (health, finance, harassment) — social pressure distorts answers.
- Final decision-making — small N + groupthink ≠ representative.
- Anything you'd ship without a 1:1 follow-up — group consensus is unreliable signal.

## Where it fails / limitations
- 1-2 dominant voices dictate the "consensus" unless moderation is firm.
- Groupthink: people anchor on the first articulate opinion, suppressing dissent.
- Self-presentation bias: participants give socially desirable answers in front of peers.
- Online focus groups (Zoom) lose body language and create "speaking-order" awkwardness.
- Recruiting friction: 6-10 strangers same time slot is logistically expensive vs. async methods.

## Agentic workflow
Drive Claude to scaffold the discussion guide from research objectives, generate screener questions, and draft moderator probe ladders. After sessions, hand transcripts to a thematic-analysis agent that produces cross-group comparison tables and verbatim-quote bundles per theme. A separate "skeptic" agent flags moments of likely groupthink, dominant-voice capture, or facilitator-leading.

### Recommended subagents
- `faion-ux-researcher-agent` — guide drafting, theme synthesis, cross-group comparison.
- `faion-usability-agent` — sanity-check tasks against research goals.
- A custom `transcript-themer` — chunk transcripts, embed, cluster, output theme tree with quote citations.

### Prompt pattern
```
Goal: <research objective>. Audience: <segment>.
Draft a 90-min discussion guide: warm-up, 3 core topics with probes,
concept reaction (15 min), wrap-up. Avoid leading phrasing. Include
"call on quiet participant" prompts at the 30/60-min marks.
```

```
Given <transcript JSON with speaker tags>, output:
- Themes (3-7) with frequency by speaker.
- Verbatim quotes per theme with timestamps.
- Suspected groupthink moments (anchor speaker + sequence of agreement).
- Surprises / contradictions vs. research goals.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisper` / `whisperx` | Local transcription with speaker diarization | `pip install whisperx` |
| `pyannote-audio` | Speaker diarization | `pip install pyannote.audio` |
| `otter-cli` (unofficial) | Pull Otter.ai transcripts via API | github.com/eml-tools/otter-api |
| `dovetail-cli` (REST) | Push tagged segments to Dovetail | dovetailapp.com/developers |
| `recall.ai` API | Auto-record Zoom/Meet/Teams sessions | docs.recall.ai |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| User Interviews | SaaS | Partial | Recruiting platform; CSV export of screened participants |
| Respondent.io | SaaS | Yes (REST) | Recruiting + scheduling API |
| dscout | SaaS | Yes | Async-first; agent can drive prompts |
| Dovetail | SaaS | Yes (REST) | Tag transcripts, generate themes |
| Reduct.video | SaaS | Yes | Searchable transcript w/ video clips |
| Zoom + Otter.ai | SaaS | Partial | Cheap baseline; manual transcript export |
| FocusVision (Forsta) | SaaS | No | Enterprise focus-group platform |
| Discuss.io | SaaS | Partial | Built for focus groups, recording included |
| Lookback | SaaS | Yes | Live observer rooms; agent listens via API |

## Templates & scripts
See `templates.md`. Inline transcript-to-theme stub (≤50 lines):

```python
import json, sys
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def themes(transcript_json, k=5):
    utts = json.load(open(transcript_json))
    texts = [u["text"] for u in utts if len(u["text"].split()) > 6]
    if len(texts) < k: return []
    X = TfidfVectorizer(stop_words="english", max_features=2000).fit_transform(texts)
    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X)
    out = {i: [] for i in range(k)}
    for label, t, u in zip(km.labels_, texts, utts):
        out[label].append({"speaker": u["speaker"], "text": t, "ts": u.get("ts")})
    return out

if __name__ == "__main__":
    for theme_id, items in themes(sys.argv[1]).items():
        speakers = Counter(x["speaker"] for x in items)
        print(f"Theme {theme_id} ({len(items)} utts, speakers={dict(speakers)})")
        for x in items[:3]: print(f"  {x['speaker']}: {x['text'][:120]}")
```

## Best practices
- Run at least 3 groups per segment — themes don't stabilize with 1-2.
- Stagger arrival 5 min before start to avoid pre-session "leader" bonding skewing dynamics.
- Use written-first exercises before discussion to capture initial individual opinions un-anchored.
- Compensate equally regardless of contribution; pay-for-talk corrupts data.
- Time-box concept reveal late (last 25%) so reactions aren't biased by early tangents.
- Always recruit one extra participant per group; ~20% no-show rate.

## AI-agent gotchas
- LLM theme synthesis collapses dissent; explicitly prompt for "minority views" and "contradictions".
- Auto-generated discussion guides over-rely on closed/leading questions ("Don't you think…?"); lint pass required.
- Speaker diarization mis-attributes overlapping speech, especially online — manual spot-check required.
- Human-in-loop checkpoint: a human researcher must review themes before they enter any decision artifact; LLMs hallucinate speaker quotes.
- PII and recordings: redact names/emails/health detail BEFORE handing transcripts to the model. Recordings often contain consent-scope drift — tag and segment accordingly.

## References
- Krueger & Casey — *Focus Groups: A Practical Guide for Applied Research*
- Donna Tedesco — *The Moderator's Survival Guide*
- Nielsen Norman Group — *When to Use Focus Groups* — nngroup.com/articles/focus-groups
- Interaction Design Foundation — *How to Conduct Focus Groups*
- *Just Enough Research* — Erika Hall
