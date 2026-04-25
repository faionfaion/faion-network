# Agent Integration — User Interviews

## When to use
- Generating a tailored interview guide from research objectives and user profile descriptions
- Analyzing and synthesizing interview transcripts or notes into themes, insight statements, and affinity groups
- Producing a research readout document (findings, quotes, recommendations) from raw session notes
- Identifying gaps in interview coverage after N sessions and suggesting targeted follow-up questions
- Screening participant profiles against recruitment criteria

## When NOT to use
- Conducting the interview itself — agent cannot replicate a human facilitator's rapport, body language reading, or real-time probing judgment
- Replacing user research entirely — agent synthesis of interview data is downstream of the data; without actual interviews the agent produces speculation, not insights
- Quantitative research goals (frequency, statistical significance) — interviews are qualitative; use surveys or A/B testing instead
- When participants cannot provide informed consent for their words to be processed by an AI system (check applicable privacy regulations)

## Where it fails / limitations
- Agent synthesis of notes depends on note quality; thin or evaluative notes ("user seemed confused") produce thin insights
- Agent cannot detect non-verbal cues (hesitation, body language, tone) that a skilled interviewer would flag as data
- Interview guides written by agent may default to generic UX questions; they require customization against specific product context
- Affinity mapping via agent produces thematic groups but loses the granular quote-level evidence that makes insights convincing to stakeholders
- Agent may introduce framing bias when rewriting insights — always verify synthesized statements against source quotes

## Agentic workflow
A Claude subagent receives research objectives, target user profile, and project context, and outputs a structured Interview Guide (intro script, warm-up, main question blocks, wrap-up). After interviews, a second agent pass receives raw session notes (one file per participant) and performs synthesis: extracts key quotes, identifies recurring themes, generates HMW (How Might We) questions, and produces an insight statement per theme in the `[User type] needs [need] because [motivation]. Currently, [pain point].` format.

### Recommended subagents
- `faion-sdd-executor-agent` — treat research synthesis as an SDD task with defined output document
- General Claude subagent with analyst role — theme extraction and affinity mapping from provided notes

### Prompt pattern
```
You are a UX researcher. Create an interview guide for the following:
- Research objective: [what we need to learn]
- Target user: [profile description]
- Product/context: [brief description]
- Interview duration: [minutes]

Output a structured guide with:
1. Intro script (verbatim, 2-3 sentences)
2. Warm-up questions (2, open-ended, not about the product)
3. Main topics (3 blocks, 2-3 questions each)
4. Probe suggestions per question (follow-up prompts)
5. Wrap-up questions (2)
Flag any question that could be leading.
```

```
You are a UX researcher synthesizing interview data.
Input: Notes from [N] user interviews (provided below, one section per participant).

Output:
1. Top 5 themes with frequency (how many participants mentioned it)
2. Per theme: 1-2 supporting quotes, 1 insight statement ([User] needs [X] because [Y]. Currently, [pain])
3. Surprising or contradictory findings that deserve follow-up
4. Recommended design implications (one bullet per theme)
5. Gaps: what questions remain unanswered after these N sessions?
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Whisper (OpenAI) | Local audio transcription of recorded interviews | `pip install openai-whisper` / https://github.com/openai/whisper |
| ffmpeg | Convert audio/video formats before transcription | `apt install ffmpeg` / https://ffmpeg.org |
| otter.ai CLI (unofficial) | Automated transcription service (no official CLI; use API) | https://otter.ai/developers |
| Dovetail | Qualitative research repository; no CLI, but REST API for importing transcripts and tagging | https://dovetail.com/developers/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| User Interviews (userinterviews.com) | SaaS | Partial (API) | Participant recruitment and scheduling; API for managing studies |
| Dovetail | SaaS | Yes (REST API) | Import transcripts, create highlights, tag themes via API; best qualitative repo for agent integration |
| Otter.ai | SaaS | Yes (API) | Automatic transcription; REST API for fetching transcript text |
| Maze | SaaS | Partial | Unmoderated research; interview-style question blocks; results export as CSV |
| Lookback | SaaS | No direct API | Moderated interview platform; session recordings exported manually |
| Notion | SaaS | Yes (API) | Store interview notes and synthesized findings; agent can create/update pages via API |
| Airtable | SaaS | Yes (API) | Track participants, sessions, and recruitment status programmatically |

## Templates & scripts
See `templates.md` for the Interview Guide and Interview Notes templates. Below is a shell script for batch-transcribing recorded sessions with Whisper:

```bash
#!/usr/bin/env bash
# transcribe-sessions.sh — batch-transcribe interview recordings
# Requires: whisper (pip install openai-whisper), ffmpeg
# Usage: bash transcribe-sessions.sh ./recordings/
INPUT_DIR="${1:?Usage: $0 <recordings-dir>}"
OUT_DIR="${INPUT_DIR}/transcripts"
mkdir -p "$OUT_DIR"

for f in "$INPUT_DIR"/*.{mp3,mp4,m4a,wav}; do
  [[ -f "$f" ]] || continue
  base=$(basename "${f%.*}")
  echo "Transcribing: $f"
  whisper "$f" \
    --model medium \
    --language en \
    --output_format txt \
    --output_dir "$OUT_DIR" \
    --fp16 False
  echo "  → $OUT_DIR/${base}.txt"
done
echo "Done. Transcripts in $OUT_DIR/"
```

## Best practices
- Write the research questions (what you need to learn) before writing interview questions (what you will ask) — this prevents guides that feel like surveys
- Pilot the guide with one internal teammate before running participant sessions; adjust question order and timing
- Record sessions (with consent) even when taking notes — transcripts enable quote-level analysis that notes miss
- 5-8 participants per distinct user segment is the practical threshold for theme saturation; do not over-recruit
- Present synthesis to stakeholders with verbatim quotes attached to each insight — data without evidence is not persuasive
- Separate "what users said" from "what we infer" in every insight statement — agent is particularly prone to collapsing this distinction

## AI-agent gotchas
- Agent-generated interview guides tend toward closed or mildly leading questions when the product context is provided — require explicit review for question neutrality before use
- Synthesis from notes is bounded by what the interviewer wrote down; if the interviewer summarized instead of quoting, the agent will synthesize summaries, not evidence
- Human-in-loop checkpoint: insight statements must be validated against source notes by the researcher before being shared with stakeholders or used for design decisions
- Agent may hallucinate quotes if asked to "find examples" without being given the actual transcript text; always provide verbatim source material
- Privacy: interview transcripts often contain PII; ensure transcripts are sanitized (participant names replaced with IDs) before passing to external LLM APIs

## References
- https://www.nngroup.com/articles/user-interviews/
- Steve Portigal, *Interviewing Users* (Rosenfeld Media, 2nd ed.)
- Rob Fitzpatrick, *The Mom Test* (self-published) — practical guide to avoiding leading questions
- https://www.interaction-design.org/literature/article/how-to-conduct-user-interviews
- https://www.userinterviews.com/ux-research-field-guide-chapter/user-interviews
