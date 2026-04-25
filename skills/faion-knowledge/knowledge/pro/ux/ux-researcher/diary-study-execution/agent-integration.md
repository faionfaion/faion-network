# Agent Integration — Diary Study Execution & Analysis

## When to use
- Multi-day diary study is already running and entries (text, photo, voice) are flowing into a single store the agent can read.
- Analyst needs cross-participant thematic + temporal coding of >50 entries with quote extraction and timeline charts.
- Mid-study quality monitoring: flag low-engagement participants, generic copy-paste entries, missed days.
- Producing the final report (executive summary, themes, temporal patterns, recommendations) from already-coded data.

## When NOT to use
- Recruitment, screening, or the kickoff onboarding call — these are human-trust steps; agents should not pretend to be researchers.
- Real-time participant chat / probing follow-up DMs while the study is live (PII handling + emotional sensitivity).
- Studies where entries are voice-only without transcription pipeline or photos without OCR/vision (no usable signal yet).
- N < 5 participants — pattern detection is unreliable; a human reads everything end-to-end faster.

## Where it fails / limitations
- LLM hallucinates "themes" when entries are sparse or low-quality; minor patterns get inflated to recurring findings.
- Temporal patterns (Day 3-5 frustration spike) are invisible to a single-pass summarizer — must be coded with explicit date metadata, not free-text dates.
- Cherry-picking and confirmation bias amplify in agents when the prompt mentions a hypothesis upfront. Always run the coding pass blind to prior hypotheses.
- Entry deduplication: a participant who copy-pastes near-identical entries inflates frequency counts; agent must compute string similarity before counting.
- PII leakage: photos of receipts, screens, or addresses end up in vision API logs. Strip / blur before upload.

## Agentic workflow
Stand up a directory `study-data/` with one subfolder per participant containing one Markdown file per day plus an `entries.csv` index (`participant_id,date,prompt_id,text,media_path,sentiment`). Run a `coder` subagent over each entry to assign theme codes + sentiment + context tags into a JSON sidecar. A `synthesizer` subagent then reads all sidecars, computes per-theme frequency, per-day sentiment timeline, and generates the report from `templates.md`. Keep a human-in-loop checkpoint between coding and synthesis: human reviews the codebook before themes are locked.

### Recommended subagents
- `diary-coder` — reads each entry, applies a fixed codebook (theme, sentiment, context, severity), writes `<entry>.codes.json`. Stateless, parallel-safe, haiku-class.
- `theme-synthesizer` — consumes all `.codes.json`, produces theme matrix + temporal chart data + quote bank. Sonnet-class for narrative quality.
- `qa-monitor` — daily cron job: counts entries per participant, flags <60% completion or text similarity >0.9 across entries.
- `faion-sdd-executor-agent` — drives the report writeup as an SDD task with the analysis template as the spec.

### Prompt pattern
Coding pass:
```
You are coding a single diary entry against a fixed codebook.
Codebook: <inline list of 6-12 themes with definitions>
Output strict JSON: {themes:[], sentiment:-1..1, context:"", quotes:[], severity:"low|med|high"}
Do not invent themes. If none fit, return themes=[].
Entry: <<<TEXT>>>
```

Synthesis pass:
```
Inputs: all coded entries (JSONL).
Tasks:
1) Per-theme: frequency, participants-touched, top 3 quotes (with participant + day).
2) Per-day: average sentiment, dominant theme.
3) Outliers: entries flagged severity=high.
Output: fill the analysis template literally; cite participant+day for every quote.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisper` (openai-whisper) | Voice-entry transcription before coding | `pip install openai-whisper` |
| `ffmpeg` | Voice/video normalization, silence trim | system package |
| `exiftool` | Strip GPS/EXIF from participant photos | apt / brew |
| `csvkit` (`csvstat`, `csvcut`) | Quick frequency stats on entry index | `pip install csvkit` |
| `pandoc` | Render report template to PDF/DOCX for stakeholders | system package |
| `gh` CLI | Track action items as issues from recommendations | `gh issue create` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| dscout | SaaS | Partial — has API for project & response export | Industry standard for diary studies; pull entries via API, code locally. |
| Indeemo | SaaS | Partial — exports CSV/MP4 | Mobile-first diary; agent consumes export, not live stream. |
| User Interviews | SaaS | Recruitment only | Use for participant pool, not analysis. |
| Dovetail | SaaS | Yes — REST API + tagging | Good store for coded entries; agent posts codes via API. |
| Notion / Airtable | SaaS | Yes — official APIs | Lightweight DIY diary backend; agent reads + writes columns. |
| EthOS by Dub | SaaS | Limited | Closed export, treat as data island. |

## Templates & scripts
See `templates.md` for participation summary, theme block, and report skeleton. Lightweight QA monitor:

```bash
#!/usr/bin/env bash
# qa-monitor.sh — flag low completion + suspected copy-paste
set -euo pipefail
INDEX="${1:?entries.csv required}"
EXPECTED_DAYS="${2:?}"

# Per-participant completion %
awk -F, 'NR>1{c[$1]++} END{for(p in c) printf "%s\t%d/%d\t%d%%\n", p, c[p], '"$EXPECTED_DAYS"', (c[p]*100)/'"$EXPECTED_DAYS"'}' "$INDEX" \
  | awk '$3+0 < 60 {print "LOW: "$0}'

# Suspected copy-paste: same text across days for one participant
awk -F, 'NR>1{key=$1"|"$4; n[key]++} END{for(k in n) if(n[k]>1) print "DUP: "k" x"n[k]}' "$INDEX"
```

## Best practices
- Lock the codebook before coding starts. Adding a theme mid-study invalidates earlier passes — re-run coder agent on full set.
- Force the coder to cite verbatim text fragments per theme; this lets the synthesizer pull real quotes without re-reading raw entries.
- Keep `participant_id` opaque (P01..P0N) in all agent contexts. Never feed real names to an LLM.
- Run two independent coder passes (different temperature seeds) on a 10% sample and compute Cohen's kappa. <0.6 means codebook is ambiguous.
- Tag every entry with its prompt type (signal-contingent vs event-contingent vs end-of-day) — temporal patterns differ wildly.
- Store agent-generated themes/quotes in a write-once log; never let synthesizer overwrite earlier coding decisions.

## AI-agent gotchas
- Diary entries are emotional, often venting. LLM safety filters may refuse to code entries about frustration, health, or family conflict. Pre-classify and route sensitive entries to a less-filtered local model or human.
- Memory bias: when the synthesizer sees themes from earlier participants, it tends to force later ones into the same buckets. Code each entry independently before synthesizing.
- "In-the-moment" claim is often false: participants reconstruct evenings. Agent should not treat timestamps as ground truth — use the entry's self-reported moment when available.
- Photo entries: EXIF leaks home address, work location, device serials. Strip before any vision-API call.
- Quote attribution must be exact verbatim. Agents paraphrase by default — explicitly require character-for-character quotes in the prompt and validate by substring match against source.
- Drop-off recovery: do NOT have the agent send the recovery DM. That conversation must be human; agent only flags the candidate.

## References
- Nielsen Norman Group — Diary Studies: Understanding Long-Term User Behavior
- dscout — People Nerds: Analyzing Diary Study Data
- Interaction Design Foundation — How to Analyze Qualitative Data from UX Research
- Smashing Magazine — Diary Study UX Research (2019)
- Csikszentmihalyi & Larson — Experience Sampling Method (foundational paper)
