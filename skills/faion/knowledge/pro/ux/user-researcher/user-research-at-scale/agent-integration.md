# Agent Integration — User Research at Scale

## When to use
- Product velocity outpaces a single research team — multiple squads need findings same-week, not month-later.
- Continuous-discovery operating model where every PM/designer is expected to run small studies, with researchers as enablers.
- High-volume unmoderated testing programmes (1k+ recordings/quarter) where AI-assisted analysis is a force multiplier.
- Multinational rollouts that require parallel sessions across regions/locales.
- Mature ResearchOps practice with a repository, intake, and recruitment infrastructure already in place.

## When NOT to use
- Pre-PMF startups with < 50 paying users — qualitative depth from a researcher trumps scale.
- Studies requiring sensitive populations (children, healthcare, accessibility) where panel quality and ethics review must dominate over throughput.
- Strategic generative research (problem framing) — small samples with senior researcher synthesis still wins.
- Regulated environments (HIPAA, GDPR with special-category data) where AI auto-tagging is restricted.

## Where it fails / limitations
- AI auto-tagging of sentiment is noisy on sarcasm, code-switching, and non-English transcripts; reported accuracy varies wildly by domain.
- "Synthetic users" (LLM-personas) are useful for prompts and edge-case generation, never for validating willingness-to-pay or behaviour.
- Panel quality (Userlytics, UserTesting) varies; large panels are not high-quality panels.
- Scale shifts the bottleneck from "who to talk to" to "what to do with insights" — without a repo strategy, scaling produces archived reports nobody reads.
- Multi-agent governance is immature; today most "AI co-pilot" features are single-call summarisers, not autonomous pipelines.

## Agentic workflow
Treat the system as an assembly line: recruit → moderate (human or unmoderated) → transcribe → tag → cluster → report → publish. Agents own transcription, tagging, clustering, and report drafting; humans own study design, ethics, interpretation, and stakeholder framing. Use a repository (Dovetail, Marvin, EnjoyHQ, Notably) as the single source of truth, and have agents push artefacts there with stable IDs. Run a "human verifier" subagent that samples 10% of agent-tagged segments per study and gates publication on agreement ≥ 90%.

### Recommended subagents
- A purpose-built `research-synthesiser` subagent: ingests transcripts + existing tag taxonomy, proposes new tags only when frequency ≥ N, emits affinity clusters with quotes.
- `faion-brainstorm` — converts a synthesis into stakeholder-specific framings (PM, design, exec).
- A `bias-watcher` subagent: flags leading questions in moderator scripts before recording starts.
- `faion-improver` — quarterly audit of repository signal-to-noise ratio (% of tagged segments referenced in shipped decisions).
- A `recruit-screener` subagent that drafts screener questions and grades panel responses for fraud signals.

### Prompt pattern
"Given 28 unmoderated session transcripts (file IDs `S1..S28`) and the tag taxonomy in `taxonomy.json`, tag every utterance. For each tag with ≥ 5 segments, output a cluster with: definition, 3 verbatim quotes (with timestamp), conflicting evidence if any. Do not invent new tags; if a segment fits none, mark `untagged` for human review."

"Score these 12 screener responses 0-1 for panel-fraud risk (copy-paste, gibberish, suspiciously fast, contradictory answers). Provide reasoning for any score > 0.5."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Dovetail API | Push notes/tags/highlights | https://developers.dovetail.com |
| Marvin (User Interviews) API | Repository ops | https://www.heymarvin.com |
| EnjoyHQ / Notably / Aurelius | Repo APIs | https://getenjoyhq.com / https://www.notably.ai |
| AssemblyAI / Deepgram / Whisper | Transcription + diarisation | https://www.assemblyai.com / https://deepgram.com |
| Maze API | Unmoderated study control | https://maze.co/developers |
| UserTesting API | Pull recordings, push briefs | https://api.usertesting.com |
| Userlytics API | Panel + sessions | https://www.userlytics.com |
| dscout API | Mobile diary + missions | https://dscout.com |
| Calendly / Iteratively | Scheduling automation | https://calendly.com |
| `whisperx` (OSS) | Local high-accuracy transcription | https://github.com/m-bain/whisperX |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| UserTesting | SaaS | Yes (REST API) | Largest panel, AI insights add-on |
| Userlytics | SaaS | Yes (REST API) | 2M+ panel, AI analytics |
| Maze | SaaS | Yes (REST API) | Survey + prototype testing, AI follow-ups |
| dscout | SaaS | Partial | Mobile ethnography at scale |
| Dovetail | SaaS | Yes (REST API + AI) | Repo with built-in AI tagging |
| Marvin | SaaS | Yes (REST API + AI) | Repo + recruit, strong AI coding |
| Notably | SaaS | Yes (REST API + AI) | AI-native repo |
| Sprig | SaaS | Yes (REST API) | In-product micro-surveys, AI summarise |
| Lookback | SaaS | Yes | Live moderated, weaker AI |
| Respondent.io | SaaS | Yes (REST API) | High-quality recruit, niche panels |
| EnjoyHQ | SaaS | Yes | Repo for organisations standardising on tags |

## Templates & scripts
See `templates.md` and `examples.md` for the at-scale operating model (RACI, intake form, repo schema).

Inline transcript-to-tags pipeline:

```python
# tag_session.py — Whisper + Anthropic for tagging at scale
import json, os, anthropic, whisperx
from pathlib import Path

TAX = json.loads(Path("taxonomy.json").read_text())
client = anthropic.Anthropic()

def transcribe(path: Path) -> list[dict]:
    model = whisperx.load_model("large-v3", "cuda", compute_type="float16")
    audio = whisperx.load_audio(str(path))
    return model.transcribe(audio, batch_size=16)["segments"]

def tag(segments: list[dict]) -> list[dict]:
    msg = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=4000,
        system="You tag user-research segments using ONLY the provided taxonomy. Never invent tags.",
        messages=[{"role": "user", "content": json.dumps({"taxonomy": TAX, "segments": segments})}],
    )
    return json.loads(msg.content[0].text)

if __name__ == "__main__":
    out = []
    for f in Path("sessions").glob("*.mp4"):
        segs = transcribe(f)
        out.append({"file": f.name, "tagged": tag(segs)})
    Path("tagged.json").write_text(json.dumps(out, indent=2))
```

## Best practices
- Standardise a repository tag taxonomy first; let no study propose new tags without a curator review.
- Stratify panels (role, geography, tenure) and report on stratification balance per study; "n=200 random" is a misleading scale claim.
- Pair every quantitative claim from unmoderated tools with at least three verbatim quotes; raw numbers without voice rarely change behaviour.
- Use AI for first-pass tagging only; human verification on a sampled 10% before publication.
- Build a "decisions ledger" linking tagged insights to shipped product changes; the ratio is the actual ROI of scaling.
- Cap unmoderated panel reliance at ~60-70% of mix; complement with moderated and longitudinal studies for depth.
- Localisation: transcribe in source language, translate after tagging, never the reverse — translation loses tag-relevant nuance.
- Watch for over-recruitment of "professional respondents"; rotate panels and audit completion times.

## AI-agent gotchas
- Auto-summarisers compress 30-minute interviews to one paragraph and lose disconfirming evidence; require quote retention.
- Sentiment models trained on product reviews mis-tag user-research segments (heavy use of past tense, hypothetical framing).
- LLM "synthetic users" are sycophantic; never use them to validate go/no-go decisions, only to seed prompts and edge cases.
- Diarisation errors mis-attribute moderator speech to participants, biasing tag distributions; always verify speaker tags before clustering.
- Multi-agent pipelines without idempotency reprocess the same recording when re-run, double-counting tags; require deduplication keys.
- GDPR/CCPA: agent pipelines must redact PII before storage; pair with `password-scrubber-agent` or equivalent before pushing transcripts to a repo.
- Beware of "AI follow-up question" features that ask leading questions; review generated probes before they ship to participants.

## References
- Teresa Torres — *Continuous Discovery Habits* (2021)
- Erika Hall — *Just Enough Research* (2nd ed., 2019)
- ResearchOps Community — *The Research Operations Field Book* — https://researchops.community
- Indi Young — *Time to Listen* (2022)
- WTR (We Trust Research) "Maturity Model" — https://wetrustresearch.com
- Dovetail "AI in research" guidelines — https://dovetail.com/research/
