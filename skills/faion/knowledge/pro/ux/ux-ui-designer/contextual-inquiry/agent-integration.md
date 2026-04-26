# Agent Integration — Contextual Inquiry

## When to use
- Discovery phase for B2B / enterprise tools where workflow is opaque to outsiders.
- Investigating reported "low adoption" — observed workarounds usually explain it better than survey data.
- Domains with heavy tacit knowledge (clinicians, traders, factory operators, customer-support agents).
- Pre-redesign of legacy systems with shadow IT (Excel exports, sticky notes, side databases).
- Validating personas drafted from secondary research before committing engineering budget.

## When NOT to use
- Quick directional feedback on a hi-fi prototype — use moderated usability test instead.
- Public, walk-up consumer flows where every session is short and self-contained — analytics + intercept survey is cheaper.
- Highly regulated environments where observation requires months of compliance review you can't afford.
- A/B comparison of two candidate designs — wrong instrument; method is generative, not evaluative.
- Single-session "ride-along" with no analysis budget — produces anecdotes, not insight.

## Where it fails / limitations
- Hawthorne effect: presence of researcher + recording changes behavior, especially first 20 min.
- Hard to scale beyond ~8 participants; statistical generalization is invalid.
- Remote variants lose ~40% of environmental signal (peripheral artifacts, noise, interruptions).
- Confidential workflows (PII, M&A, healthcare PHI) often block recording or transcript export to LLMs.
- Cultural mismatch: master-apprentice framing reads as patronizing in some hierarchical org cultures.

## Agentic workflow
Treat the agent as a research-ops assistant, not the field investigator. A human runs the session; subagents handle preparation, transcript ingestion, affinity coding, model synthesis, and cross-session pattern detection. Keep a hard human-in-loop checkpoint between raw transcript and any insight artifact — LLMs hallucinate quotes and over-generalize from single sessions.

### Recommended subagents
- `faion-ux-researcher-agent` — drafts focus statement, observation guide, screener, and consent script from a one-paragraph brief.
- `faion-usability-agent` — secondary pass on transcripts to flag breakdowns, workarounds, and contradictions between stated and observed behavior.
- `password-scrubber-agent` — run on every transcript before sending to any external API (PII/PHI/credentials in field recordings is the rule, not exception).

### Prompt pattern
```
You are preparing a contextual inquiry observation guide.
Focus: <focus statement, ≤2 sentences>
Domain: <industry + role>
Constraints: 90-min session, in-situ, semi-structured, master-apprentice framing.
Output: opening script, 6 focus areas, 8 probe questions, observation checklist, debrief template.
```

```
You are coding a contextual inquiry transcript.
Mark each observation with: {action | artifact | breakdown | workaround | quote | interpretation}.
Never invent quotes. If a quote is paraphrased in the source, label it [paraphrase].
Output JSONL, one observation per line.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisperx` | Forced-aligned transcription with speaker diarization for field recordings | https://github.com/m-bain/whisperX |
| `ffmpeg` | Trim, downmix, redact audio segments before transcription | https://ffmpeg.org |
| `obsidian` + `dataview` | Local markdown notes + queryable affinity tags | https://obsidian.md |
| `taguette` | Free OSS qualitative coding (BYO server, no SaaS data leak) | https://www.taguette.org |
| `pandoc` | Convert field notes (md/docx) to a normalized corpus for LLM ingestion | https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Dovetail | SaaS | Yes — REST API + tags export | Best for enterprise teams; supports highlight reels, AI summaries (verify before quoting). |
| Reduct.video | SaaS | Partial | Transcript-as-video; export JSON for agent processing. |
| Condens | SaaS | Partial | EU-hosted, GDPR-friendly; strong tagging API. |
| Notably | SaaS | Yes | AI-assisted analysis; treat AI tags as draft, not final. |
| Lookback | SaaS | Limited | Live observation, weak export API. |
| Taguette | OSS self-host | Yes (raw DB) | Best for confidential domains; SQLite backend, easy to script. |
| MAXQDA / NVivo / ATLAS.ti | Commercial desktop | No (manual export) | Academic standard; no native agent integration. |

## Templates & scripts
See `templates.md` for observation guide and session notes. Inline helper to bootstrap a per-participant folder:

```bash
#!/usr/bin/env bash
# bootstrap-ci-session.sh — create participant folder skeleton
set -euo pipefail
STUDY="${1:?study slug}"
PID="${2:?participant id}"
DIR="research/$STUDY/$PID"
mkdir -p "$DIR"/{audio,video,artifacts,notes,transcripts,redacted}
cat > "$DIR/notes/session.md" <<MD
# CI Session — $PID
**Date:**
**Duration:**
**Location:**

## Environment
## Workflow
## Quotes
## Breakdowns
## Workarounds
## Interpretations
## Follow-ups
MD
echo "Created $DIR"
```

## Best practices
- Run a 30-minute pilot with an internal stakeholder before the first real participant — it surfaces logistics bugs, not insight.
- Capture artifacts (screenshots, photos of paper, redacted spreadsheet exports) — they outlive memory and quote ambiguity.
- Hold the immediate-debrief sacred: 15 minutes within an hour of the session, before context decays. No exceptions.
- Triangulate stated vs. observed behavior in your notes column-by-column; the gap is where the real insight lives.
- Stop at 6–8 participants per role; if signal still saturates, scope was too broad — split the study.
- Build the affinity diagram on physical wall or Miro before letting an LLM cluster — it reveals researcher bias the LLM will hide.

## AI-agent gotchas
- LLMs invent participant quotes. Always run a quote-presence check (substring search in transcript) before any artifact ships.
- Never feed raw audio/video to a third-party API without an explicit data-handling addendum — field recordings frequently contain PHI/PII the participant forgot to redact.
- Master-apprentice framing breaks if the agent generates leading probe questions ("wouldn't it be easier if…"). Pin the prompt: probes must be open and past-tense.
- Affinity clustering by LLM tends to collapse rare-but-critical observations into majority themes. Force a "singletons" output bucket.
- Cultural and tacit knowledge degrade in translation; if sessions are non-English, transcribe in source language and translate quotes only at reporting time.
- Insight inflation: agents will produce 30 "insights" from 5 sessions. Cap output at 1 insight per 2 hours of observation as a sanity rail.

## References
- Beyer & Holtzblatt, *Contextual Design* (2nd ed., 2016).
- Holtzblatt, Wendell, Wood, *Rapid Contextual Design* (2005).
- Nielsen Norman Group, *Contextual Inquiry: Inspire Design by Observing and Interviewing Users in Their Context* (2019). https://www.nngroup.com/articles/contextual-inquiry/
- Interaction Design Foundation, *How to Conduct Contextual Inquiries*. https://www.interaction-design.org/literature/article/how-to-conduct-contextual-inquiries
- Goodman, Kuniavsky, Moed, *Observing the User Experience* (2nd ed., 2012).
