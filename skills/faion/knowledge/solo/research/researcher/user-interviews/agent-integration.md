# Agent Integration — User Interviews

## When to use
- Pre-MVP discovery to surface latent jobs, pains, and current solutions.
- After launch when quantitative metrics show drop-off but root cause is unclear.
- Persona refinement and segmentation work.
- Pricing / packaging research when willingness to pay is unknown.

## When NOT to use
- For statistically significant claims — interviews surface themes, not percentages. Use surveys after themes stabilize.
- When you can already observe behavior (analytics, session recordings); behavioral data trumps stated experience.
- For commodity / well-understood markets where interviews repeat existing knowledge.
- As a substitute for behavioral validation — interviews don't prove anyone will pay.

## Where it fails / limitations
- Leading questions and pitch-mode are the universal failure mode; both humans and agents revert to them under pressure.
- Recall bias: respondents reconstruct past behavior optimistically. Always ask for the last specific instance.
- Sample bias from warm-network recruits skews positive; cold recruiting is harder but cleaner.
- 5-10 interviews is enough for thematic saturation only on narrow segments; cross-segment work needs 10-15 per segment.
- Interview fatigue after 3-4 sessions in a day → quality drops. Schedule with buffers.

## Agentic workflow
Treat interviews as a four-stage pipeline: recruit (outreach drafting + scheduling), conduct (script + live note-taking with the human leading), transcribe + tag (Whisper + LLM signal extraction), synthesize (cross-interview pattern analysis). Agents do not run live interviews — they prepare scripts, transcribe, and tag. Decision-making remains with the human.

### Recommended subagents
- `recruit-writer` (haiku) — drafts personalized outreach DMs/emails using LinkedIn/X profile context.
- `script-writer` (sonnet) — generates Mom Test-compliant scripts per segment + research goal.
- `transcriber-tagger` (sonnet) — runs Whisper diarization + tags pains/jobs/solutions/quotes.
- `pattern-synthesizer` (sonnet) — cross-interview thematic analysis with frequency counts.
- `faion-persona-builder-agent` (referenced in README) — maintains the persona deliverable.

### Prompt pattern
```
Role: script-writer.
Input: research_goals.md, segment_profile.md.
Output: 20-30 minute script with sections (warm-up, context, problem exploration, solutions tried, wrap-up).
Constraint: every problem-exploration question must reference a past specific event; no hypotheticals; no "would you".
Self-check: scan output for "would|imagine|hypothetically|do you think"; if any present, regenerate.
```

```
Role: transcriber-tagger.
Input: interview.wav (with diarization), segment_context.md.
Output JSON: {pains:[{quote, ts, severity:1-5}], current_solutions:[{tool, satisfaction:1-5}],
              jobs_to_be_done:[...], red_flags:[...], referrals_offered:[...]}.
Rule: never paraphrase pains — verbatim quotes only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisper.cpp` | Local high-accuracy transcription | https://github.com/ggerganov/whisper.cpp |
| `pyannote-audio` | Speaker diarization for who-said-what | https://github.com/pyannote/pyannote-audio |
| `ffmpeg` | Audio normalize/clip before Whisper | https://ffmpeg.org |
| `transcript-to-csv` (script) | Convert WebVTT to CSV with speaker col | custom |
| `nb` / `dasel` | Manage interview corpus + tags | https://github.com/xwmx/nb |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Calendly / Cal.com | SaaS+OSS | Yes (API) | Scheduling with timezone handling and consent text. |
| Riverside | SaaS | Yes (API) | Studio-quality recording + speaker tracks. |
| Descript | SaaS | Yes (API) | Transcription + cleanup; agent can pull snippets. |
| Otter.ai | SaaS | Limited API | Cheap transcription; lower quality than Whisper for technical terms. |
| Dovetail | SaaS | Yes (API) | Tag/cluster transcripts; built for research repos. |
| Notably / Marvin | SaaS | Yes (API) | AI synthesis across interview corpus. |
| Reduct.video | SaaS | Yes (API) | Video clip search + reels for sharing findings. |
| LinkedIn Recruiter | SaaS | Yes (limited API) | Targeted recruit; respect outreach limits. |
| User Interviews / Respondent | SaaS | Yes (API) | Paid recruit panels; agent can configure screeners. |

## Templates & scripts
See `templates.md` for Interview Script Template and Synthesis Template.

Inline post-interview synthesis stub (Python, ≤40 lines):
```python
import json, sys, glob
files = glob.glob(sys.argv[1] + "/*.json")
pains, sols, jobs = {}, {}, {}
for path in files:
    d = json.load(open(path))
    for p in d.get("pains", []):
        pains[p["quote"][:80]] = pains.get(p["quote"][:80], 0) + 1
    for s in d.get("current_solutions", []):
        sols[s["tool"]] = sols.get(s["tool"], 0) + 1
    for j in d.get("jobs_to_be_done", []):
        jobs[j[:80]] = jobs.get(j[:80], 0) + 1
print("Top pains:")
for k, v in sorted(pains.items(), key=lambda x: -x[1])[:10]:
    print(f"  {v:>3}  {k}")
print("Tool stack:")
for k, v in sorted(sols.items(), key=lambda x: -x[1])[:10]:
    print(f"  {v:>3}  {k}")
print("Jobs:")
for k, v in sorted(jobs.items(), key=lambda x: -x[1])[:10]:
    print(f"  {v:>3}  {k}")
```

## Best practices
- Record + transcribe everything (with consent) — memory after 4 interviews is worthless.
- End every interview with: "Who else should I talk to?" — referrals dominate cold recruiting.
- Synthesize after every 3 interviews, not at the end. Patterns inform follow-up scripts.
- Pre-write the script with red-flag checks ("would you", "do you think") and reject any question that fails.
- Tag pains by severity AND frequency separately — high-frequency-low-severity is noise; low-frequency-extreme is opportunity.
- Don't pitch your solution. If you must, save it for the last 2 minutes and frame as "here's what I'm playing with — what does it remind you of?".

## AI-agent gotchas
- LLMs naturally rephrase verbatim quotes into smoother prose — explicitly forbid paraphrasing in prompts.
- Whisper struggles with proper nouns and technical jargon; pre-prime with a glossary of likely terms.
- Diarization fails on overlapping speech; expect 5-10% mis-attribution; cross-check before quoting.
- Cross-interview synthesis hallucinates frequency ("most users said X"); require cited interview IDs per claim.
- Persona generation from <8 interviews is statistically meaningless; agents will produce confident personas anyway.
- Human-in-loop checkpoints: (1) script approval before any recruiting, (2) synthesis review before persona work, (3) referral chain audit (warm-only network = bias).

## References
- Rob Fitzpatrick, "The Mom Test" (canonical, ~150 pages, mandatory).
- Steve Portigal, "Interviewing Users" (2nd ed., 2023) — comprehensive practitioner guide.
- Erika Hall, "Just Enough Research" — fast, opinionated.
- Teresa Torres, "Continuous Discovery Habits" — interview cadence + opportunity solution trees.
- Indi Young, "Practical Empathy" / "Time to Listen" — listening sessions, deeper than user interviews.
- Nielsen Norman Group, "User Interview" articles — practical UX-focused guidance.
