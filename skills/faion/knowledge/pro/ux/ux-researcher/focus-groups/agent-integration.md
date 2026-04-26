# Agent Integration — Focus Groups

## When to use
- Early concept exploration: get diverse reactions to multiple positioning angles before investing in a single direction.
- Language and terminology discovery: harvest the vocabulary your users actually use, then feed it into copy and search synonyms.
- Stakeholder buy-in: when leadership needs to "watch users" to believe research findings.
- Cross-segment comparison: 3-4 groups (current users, competitor users, non-users) reveal segment-specific objections.

## When NOT to use
- Usability testing — group dynamics suppress individual struggle; use moderated 1:1 sessions.
- Sensitive topics (health, finances, conflict, illegal use) — participants self-censor in groups.
- Behavior measurement — groups capture stated, not actual, behavior.
- Final go/no-go decisions — groupthink and dominant voices distort signal.
- Quantitative claims — N=8 per group is not statistically generalizable.

## Where it fails / limitations
- Dominant participants skew transcripts; LLM analysis without speaker diarization treats their views as group consensus.
- Online groups (Zoom) lose ~30% of nonverbal signal; energy and disagreement read flatter than in-person.
- Recruiters often deliver "professional respondents" who cycle across studies; screen aggressively or insights generalize to one demographic: people who like focus groups.
- LLM theme extraction over-clusters: nuanced disagreement collapses to a single theme unless you prompt for tension/dissent explicitly.
- Single-group findings are unsafe — minimum 2-3 groups per segment before any pattern claim.

## Agentic workflow
Agents operate around the human moderator, not as moderators. Pre-session: a research agent drafts the discussion guide from objectives, generates probing follow-ups, and screens recruits. Post-session: a transcription agent (Whisper + diarization) produces speaker-labeled transcripts; a synthesis agent extracts themes per segment with verbatim quotes; a comparison agent maps cross-group agreement/disagreement. A human signs off each theme before it lands in the report.

### Recommended subagents
- `faion-ux-researcher-agent` — drafts guide, designs probes, performs cross-group synthesis.
- `faion-content-marketer` — extracts user-language vocabulary for copy reuse.
- `faion-product-manager` — converts findings into prioritized opportunity statements.
- `faion-market-researcher` (from `pro/research/market-researcher`) — segments + recruitment screener logic.

### Prompt pattern
Theme extraction:
```
Transcript (speaker-labeled): {transcript}
Segment: {segment_name}
Extract 3-7 themes. For each: theme name, supporting quotes (with speaker ID), strength of consensus (unanimous/majority/split/minority). Flag any dominance pattern where one speaker drives a theme alone.
```
Cross-group comparison:
```
Themes from Group A ({segment}): {themes_a}
Themes from Group B ({segment}): {themes_b}
Identify: (1) shared themes, (2) segment-unique themes, (3) contradictions. Cite quote IDs.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| OpenAI Whisper / `whisper-cli` | Transcribe recordings locally | `pip install openai-whisper` |
| `pyannote.audio` | Speaker diarization (who said what) | `pip install pyannote.audio` |
| WhisperX | Whisper + diarization combined | `pip install whisperx` |
| `ffmpeg` | Extract audio from Zoom recordings | distro package |
| `yt-dlp` | Download recordings from links if needed | `pip install yt-dlp` |
| Anthropic SDK | Theme extraction with prompt caching across long transcripts | `pip install anthropic` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Zoom | SaaS | Partial — REST API for cloud recordings | Cheapest for online groups; export MP4+VTT |
| UserTesting Live Conversations | SaaS | Partial — API for sessions | Built-in note-taking, recruit panel |
| Discuss.io | SaaS | Yes — REST API | Purpose-built for online focus groups |
| Recollective | SaaS | Yes — API | Asynchronous + live group hybrid |
| dscout (Live) | SaaS | Yes — API | Diary + live group combo |
| Respondent.io | SaaS | Yes — API | High-quality recruitment, niche segments |
| User Interviews | SaaS | Yes — API | Recruitment panel, screener builder |
| Otter.ai / Fireflies | SaaS | Partial | Cloud transcription; check data residency before sending sensitive PII |
| Dovetail | SaaS | Yes — API | Tagging + theming workspace; agent-writable via API |
| EnjoyHQ / Marvin | SaaS | Yes | Research repository; agent can post quotes/themes |

## Templates & scripts
See `templates.md` for the discussion guide and note-taking template. Minimal post-session pipeline:

```bash
# focus_group_postprocess.sh
set -euo pipefail
SESSION="$1"   # path to mp4
WORK=out/$(basename "$SESSION" .mp4)
mkdir -p "$WORK"
ffmpeg -i "$SESSION" -vn -ac 1 -ar 16000 "$WORK/audio.wav"
whisperx "$WORK/audio.wav" --model large-v3 --diarize \
    --hf_token "$HF_TOKEN" --output_dir "$WORK"
python -c "
import json, anthropic, pathlib
client = anthropic.Anthropic()
transcript = pathlib.Path('$WORK/audio.json').read_text()
msg = client.messages.create(
    model='claude-opus-4-7', max_tokens=4000, temperature=0,
    messages=[{'role':'user','content':open('prompts/themes.txt').read()+transcript}])
pathlib.Path('$WORK/themes.json').write_text(msg.content[0].text)
"
```

## Best practices
- Run a minimum of 2 groups per segment; never report a finding from a single session.
- Brief the moderator separately from the agents — moderators need context-flexibility, not scripted prompts. Agents prepare the guide; humans run the room.
- Capture written first-impressions (silent post-it round) before group discussion to break anchoring on the first speaker's view.
- Tag transcripts with both speaker ID and segment label; filter analysis prompts by segment to surface cross-group contrasts.
- Run a "dissent prompt" pass explicitly: "What disagreement existed within this group?" — counters LLM bias toward consensus narratives.
- Compensate participants well ($75-150/90 min in US baseline; higher for B2B/specialist). Lowballing screens for low-quality respondents.

## AI-agent gotchas
- Whisper without diarization assigns all speech to one speaker → quote attribution becomes unreliable. Always run diarization for groups.
- Long transcripts (>50k tokens) require chunked summarization; without overlap windows, themes spanning chunk boundaries get lost. Use a 10-15% overlap.
- LLMs treat polite agreement ("yeah, that's right") as endorsement. Calibrate by counting unique speakers per theme, not utterance count.
- Auto-generated themes invent neat categories; force the model to also output a "messy/unclassified" bucket and review it manually.
- Privacy: never upload raw recordings to a third-party LLM endpoint without explicit consent in the participant agreement. Default to local Whisper for sensitive segments.
- Recruitment fraud (bots/repeats) is now common via global panels. Verify with a live screener call or short video task before slotting into a group.
- LLM-generated discussion guides over-rely on closed-ended phrasing. Always have the human researcher rewrite at least 30% of probes for openness.

## References
- Krueger, R. & Casey, M. — *Focus Groups: A Practical Guide for Applied Research* (Sage)
- Tedesco, D. & Tranquada, F. — *The Moderator's Survival Guide*
- Nielsen Norman Group — When to Use Focus Groups: https://www.nngroup.com/articles/focus-groups/
- User Interviews — Focus Groups in UX Research field guide: https://www.userinterviews.com/ux-research-field-guide-chapter/focus-groups
- WhisperX repo: https://github.com/m-bain/whisperX
