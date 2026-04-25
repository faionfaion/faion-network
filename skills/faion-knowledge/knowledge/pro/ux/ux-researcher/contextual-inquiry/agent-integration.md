# Agent Integration — Contextual Inquiry

## When to use
- Discovery research where workflows, tools, and environment matter (clinical settings, factory floors, financial back-office, field ops).
- Mapping current-state tasks before redesign — capturing workarounds, shadow IT, tacit knowledge.
- Validating that a new product fits real work, not idealized work, before specification freeze.
- Investigating a quality/safety incident where reported procedure differs from actual practice.

## When NOT to use
- Quick usability feedback on a finished design — usability testing is faster and cheaper.
- Strangers-on-the-internet research where context cannot be observed (use diary studies or remote interviews).
- High-secrecy environments (defense, M&A) where observation is restricted — fall back to artifact analysis.
- Pure preference/attitudinal questions — surveys serve better.

## Where it fails / limitations
- Observer effect is real; participants perform their work for the researcher, missing the messy reality.
- Time-boxed (1-2 h) sessions miss low-frequency tasks (monthly close, quarterly audits) and emergencies.
- Master-apprentice framing assumes a single expert; team-based work needs a different choreography (multi-CI, role-switching).
- Remote variants lose physical artifacts (sticky notes, paper forms, whiteboard scribbles) that often hold the real workflow.
- Cultural and organizational sensitivities (union rules, HIPAA, GDPR special-category data) can block observation entirely.
- Analysis (affinity diagrams, sequence/flow/cultural models) is labor-heavy; teams skip it and the data dies in notebooks.

## Agentic workflow
LLM agents accelerate the labor-heavy back half (transcription, tagging, affinity clustering, model drafting), but the observation itself is human. Pipeline: (1) human researcher records in-environment session with consent + minimal cues, (2) `transcript-cleaner` agent normalizes ASR output and timestamps, (3) `observation-tagger` extracts actions/artifacts/breakdowns into structured rows, (4) `affinity-clusterer` proposes clusters with evidence, (5) `model-drafter` outputs sequence/flow/cultural model skeletons for human review. Always re-share interpretations with participants — agents cannot self-validate.

### Recommended subagents
- `transcript-cleaner` — haiku; fixes ASR errors, aligns speakers, redacts PII per vui-privacy-security.
- `observation-tagger` — sonnet; extracts {time, actor, action, artifact, tool, breakdown, quote} rows.
- `affinity-clusterer` — sonnet; clusters tagged rows across sessions, names clusters, surfaces outliers.
- `workflow-modeler` — sonnet; drafts sequence and flow models from tagged rows for designer review.
- `interview-coach` — sonnet; pre-session reviewer that critiques the observation guide for leading/loaded questions.

### Prompt pattern
```
You are observation-tagger. Read <transcript_segment_with_timestamps> and emit
JSON rows with shape {t, actor, action, artifact, tool, breakdown:bool, quote_verbatim,
inference:bool}. Mark anything not directly observed as inference:true. Quote text
must be verbatim from the transcript span. No editorializing.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisperx` | Speaker-diarized transcription with timestamps | github.com/m-bain/whisperX |
| `openai-whisper` | OSS transcription baseline | github.com/openai/whisper |
| `obs-cli` (OBS Studio remote) | Record screen + cam for remote CI sessions | obsproject.com |
| `dovetail` API | Tag transcripts, cluster across sessions | dovetail.com/api |
| `pandoc` | Convert tagged notes to readable reports | pandoc.org |
| `ffmpeg` | Trim, transcode, extract clips for evidence packs | ffmpeg.org |
| `presidio-cli` | Redact PII before tagging/sharing | microsoft.github.io/presidio |
| `airtable-cli` / `notion-cli` | Store the observation database | airtable.com / notion.so |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Dovetail | SaaS | Yes — REST + Insights API | Industry default for tagging/clustering |
| Condens | SaaS | Yes — REST | Lighter alternative |
| Notably | SaaS | Yes — REST | AI-native qualitative analysis |
| Lookback | SaaS | Yes — REST | Live session recording, remote CI |
| UserTesting | SaaS | Yes — REST | Recruitment + recorded remote sessions |
| Reduct | SaaS | Yes — REST | Transcript-first editing, share clips |
| Mural / Miro | SaaS | Yes — REST | Affinity walls, sequence/flow models |
| Loom + Zoom + Microsoft Teams | SaaS | Limited | Capture remote CI; export transcripts |

## Templates & scripts
See `templates.md` for observation guide and session notes templates. Tagging row schema:

```python
# ci_row.py — strict row shape for cross-session analysis
from dataclasses import dataclass, asdict
from typing import Optional
import json, sys

@dataclass
class CIRow:
    session_id: str
    t_seconds: float
    actor: str            # participant id or "researcher"
    action: str           # short verb phrase
    artifact: Optional[str]
    tool: Optional[str]
    breakdown: bool       # something didn't work
    workaround: bool
    quote_verbatim: Optional[str]
    inference: bool       # not directly observed
    tags: list[str]

def main():
    rows = [CIRow(**r) for r in json.load(sys.stdin)]
    for r in rows:
        if r.inference and not r.quote_verbatim:
            print(f"warn: {r.session_id}@{r.t_seconds} inference without quote")
    print(json.dumps([asdict(r) for r in rows]))

if __name__ == "__main__":
    main()
```

## Best practices
- Run a 1-hour pilot before the real round to fix observation-guide weaknesses; the second guide is always better.
- Capture artifacts physically (photos with consent) — workflows rarely live entirely on screens.
- Mark inferences as inferences in notes from the very first session; retroactive separation of observed vs inferred is impossible.
- Debrief within 30 minutes of the session, while peripheral memory is intact. Audio recording does not replace this.
- Sample for variation, not statistical validity: include shifts, regions, seniority, edge-case roles. 4-8 sessions is the sweet spot for one focus area.
- Share interim findings with participants ("member checking") to catch misinterpretations before downstream design work commits to them.
- Treat workarounds as system-design signals, not user errors. The fact that someone keeps paper notes is the finding.

## AI-agent gotchas
- LLMs paraphrase quotes silently. Lock the agent to verbatim mode and reject outputs containing strings not in the source.
- Affinity clustering with too-narrow embeddings collapses distinct themes. Use both lexical and semantic similarity, and force the agent to justify each cluster with at least 3 supporting rows.
- ASR garbles domain jargon (drug names, ticker symbols, internal codenames). Maintain a custom vocabulary list and run domain-aware correction.
- Privacy: observation captures bystanders, dictation, screen contents that are not the participant's. Redact before any LLM ingestion (presidio + manual review for screens).
- Remote CI screen recordings often include private windows briefly. Pre-trim before sharing with the agent or any third-party tool.
- "Cultural model" outputs from agents tend to caricature organizational dynamics. Demand evidence quotes and have a human review for tone/respect.
- Don't let an agent rank participants' competence — agents will judge "wrong" workflow as user error, missing that the system is wrong.
- Never substitute an LLM-simulated user for a real participant ("synthetic CI"). It produces convincing fiction with no environmental signal.

## References
- Beyer & Holtzblatt, "Contextual Design" (2nd ed.).
- Holtzblatt, Wendell, Wood, "Rapid Contextual Design".
- Goodman, Kuniavsky, Moed, "Observing the User Experience" (2nd ed.).
- Nielsen Norman Group — "Contextual Inquiry: Inspire Design by Observing Real Use" (nngroup.com/articles/contextual-inquiry/).
- Usability.gov — Contextual interview guide.
- Steve Portigal, "Interviewing Users" (companion methodology).
