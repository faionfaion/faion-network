# Agent Integration — Usability Testing

## When to use
- Before a major launch when key flows (checkout, onboarding, signup) have not been observed with real users
- After a significant redesign to confirm that existing task completion rates are maintained
- When analytics show unexpected drop-offs but do not explain why
- When the team has competing design hypotheses and needs evidence to choose one
- When a new user segment is being targeted and their mental models are unknown

## When NOT to use
- To validate pixel-level visual choices — preference testing or five-second tests are more appropriate
- When fewer than 3 participants can be recruited — the noise-to-signal ratio is too high
- As a substitute for analytics: do not run sessions to confirm what quantitative data already shows clearly
- When the prototype or product being tested is broken — fix critical blockers first or participants cannot complete tasks

## Where it fails / limitations
- 5 participants reveal ~85% of usability issues but miss issues that occur with specific user segments; mix of segments requires 5 per segment
- Moderated sessions are biased by facilitator behavior — leading questions or rescue behavior invalidates findings
- Remote unmoderated tools (Maze, UserTesting) cannot follow up on unexpected behavior; rich insights require moderation
- Think-aloud protocol distorts natural task performance — users narrate instead of focusing, completing tasks more slowly than real use
- Participants perform better in tests than in real life because the test context removes distraction and fatigue

## Agentic workflow
Claude subagents are effective at two specific stages: (1) drafting test plans and task scenarios given a product description and research questions, and (2) analyzing session transcripts or notes to extract findings, assign severity ratings, and generate a prioritized report. Session facilitation itself is a human responsibility — agents cannot react to participant behavior in real time. Transcript analysis should be done per session first, then synthesized across sessions in a second agent call to avoid context overflow.

### Recommended subagents
- Any general-purpose Claude subagent (Sonnet or Opus) — generate test plan, write task scenarios, analyze transcripts
- `faion-sdd-executor-agent` — structure the resulting action items as implementation tasks after findings are prioritized

### Prompt pattern
```
You are a UX researcher. Given the product description and research questions below, write a usability test plan including:
1. 4–6 realistic task scenarios (no hints about the solution path)
2. Pre-task screening criteria
3. Post-task questions (SUS or custom 1–5 scale)
4. Metrics to record per task (success, time, errors, satisfaction)

Product: [description]
Research questions: [list]
Participant profile: [description]
```

```
You are analyzing usability test transcripts. For each session note below:
- Extract all usability issues observed
- Assign severity: critical | high | medium | low
- Count frequency across sessions
- Group issues by interface area
- Return JSON: [{ issue, severity, frequency, area, quote, recommendation }]

Sessions: [structured notes]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `obs-studio` | Record screen + audio for moderated sessions | [obsproject.com](https://obsproject.com) — free, cross-platform |
| `ffmpeg` | Batch-convert session recordings to a standard format | `apt install ffmpeg` / [ffmpeg.org](https://ffmpeg.org) |
| `whisper` (OpenAI) | Transcribe session recordings to text for analysis | `pip install openai-whisper` / [github.com/openai/whisper](https://github.com/openai/whisper) |
| `lookback-cli` (unofficial) | Download session data from Lookback platform | via REST API / [lookback.com/api](https://lookback.com) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Maze | SaaS | Yes — REST API | Unmoderated tests; agent can create tests and pull results via API |
| UserTesting | SaaS | Partial — API | Panel recruitment + recording; result export via API |
| Lookback | SaaS | Yes — API | Moderated + unmoderated; session recordings downloadable |
| Hotjar | SaaS | Yes — API | Session recordings + heatmaps; complements moderated sessions |
| Optimal Workshop | SaaS | Yes — API | First-click tests and tree tests alongside usability testing |
| Lyssna (UsabilityHub) | SaaS | Yes — API | Quick unmoderated tests; good for task validation at scale |

## Templates & scripts
See `README.md` for Test Plan and Session Script templates.

Script — transcribe all `.mp4` recordings in a directory using Whisper:
```bash
#!/usr/bin/env bash
# Usage: bash transcribe.sh ./recordings/
# Requires: pip install openai-whisper
INPUT_DIR="${1:-.}"
MODEL="${WHISPER_MODEL:-base}"
for f in "$INPUT_DIR"/*.mp4; do
  base="${f%.mp4}"
  if [ -f "${base}.txt" ]; then
    echo "Skip (exists): $f"
    continue
  fi
  echo "Transcribing: $f"
  whisper "$f" --model "$MODEL" --output_format txt --output_dir "$INPUT_DIR"
done
echo "Done. Transcripts in $INPUT_DIR"
```

## Best practices
- Write tasks as scenarios ("Imagine you need to...") not instructions ("Click the account button") — instruction wording tells participants where to go
- Pilot the test with one internal participant before the first real session; broken flows waste participant time
- Record task success as binary (completed without help) and time on task separately — mixing them obscures which metric matters
- For remote sessions, send the test link 10 minutes before the session and confirm the participant can access it
- Debrief with the whole team immediately after the final session while observations are fresh — do not wait for the written report
- Never fix mid-study: if a critical bug surfaces in session 1, pause and fix before sessions 2–5, or the remaining data is invalid

## AI-agent gotchas
- Agent-generated task scenarios often contain implicit hints ("use the search feature to find X") — human review of every task wording is mandatory
- Transcript analysis requires clean input: raw Zoom transcripts with crosstalk produce garbled text; clean up speaker labels before passing to agent
- Agents tend to inflate severity ratings — calibrate by asking the agent to justify each "critical" rating against the definition (user cannot complete the task at all)
- Frequency counts from agent analysis of fewer than 5 sessions are statistically meaningless; the agent should be instructed to flag low-frequency findings as "observed once — monitor"
- Consent and privacy: transcripts contain PII; do not pass raw participant names or identifying details to external LLM APIs without anonymization
- When synthesizing across sessions, run per-session analysis first in separate calls, then pass structured summaries to a synthesis call — do not pass all raw transcripts in one context

## References
- [Usability Testing 101 — NNG](https://www.nngroup.com/articles/usability-testing-101/)
- [Rocket Surgery Made Easy — Steve Krug](https://sensible.com/rocket-surgery-made-easy/)
- [Maze REST API Docs](https://developers.maze.co/)
- [OpenAI Whisper GitHub](https://github.com/openai/whisper)
- [Remote Usability Tests — NNG](https://www.nngroup.com/articles/remote-usability-tests/)
