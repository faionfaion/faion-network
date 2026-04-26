# Agent Integration — Usability Testing

## When to use
- Synthesizing session recordings or transcripts into structured findings with severity ratings
- Generating test plans and session scripts from a feature spec or user story set
- Drafting recruitment screeners for a given user persona definition
- Analyzing think-aloud transcripts to surface friction points and mental model mismatches
- Producing a prioritized findings report from raw note data after sessions conclude

## When NOT to use
- As a substitute for actual observation — agents cannot watch sessions in real-time or probe nuance the way a human facilitator does
- When sample size is below 3 participants; no pattern detection is meaningful at that scale
- For quantitative benchmarking studies (large N, SUS scoring) where statistical rigor trumps qualitative synthesis
- When the product has not yet reached a wireframe or prototype stage — nothing testable yet

## Where it fails / limitations
- Agent synthesis of think-aloud transcripts misses non-verbal cues (hesitation, facial expression, body language) that often signal the most important friction
- Automated severity ratings are unreliable without grounding in actual task success/failure data; agents over-weight verbally expressed confusion
- Participant recruitment cannot be fully automated — screening validity requires human judgment on edge cases
- Findings reports generated without ground truth video timestamps are hard for teams to verify and may be dismissed
- Agents cannot distinguish a usability problem from a participant's personal preference without cross-participant pattern confirmation

## Agentic workflow
An agent reads a feature spec or design document and generates a complete test plan (objectives, tasks, metrics, session script) as markdown. After sessions are conducted by a human facilitator, the agent receives session notes or transcripts and synthesizes findings: grouping observations by task, rating severity by frequency and impact, and drafting recommendations. A final pass produces an executive summary and a ranked action list for the engineering backlog.

### Recommended subagents
- `faion-sdd-executor-agent` — links usability findings back to SDD spec acceptance criteria, flagging which ACs are at risk
- General-purpose synthesis agent — groups raw observation notes by theme, deduplicates, and formats the findings report

### Prompt pattern
```
You are a UX research assistant. Given the feature spec below, write a usability test plan including:
- 3-5 research objectives
- 4-6 realistic task scenarios (no hints in wording)
- success criteria per task
- post-task questions
- a 5-point satisfaction scale
Output as markdown following the Test Plan Template structure.
```

```
You are analyzing usability test notes. Each note is tagged [P1]..[P8] for participant.
Group observations by task. For each group, identify: problem description, frequency (N of 8), severity (Critical/High/Medium/Low using NNG criteria), and one concrete recommendation.
Return as a findings report with a summary table at the top.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ffmpeg` | Trim session recordings, extract audio for transcription | `apt install ffmpeg` / ffmpeg.org |
| `whisper` (OpenAI) | Transcribe session audio to text for agent analysis | `pip install openai-whisper` / github.com/openai/whisper |
| `jq` | Process JSON exports from remote testing platforms | `apt install jq` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Maze | SaaS | Yes — REST API | Unmoderated tests; exports task metrics (completion rate, time, misclick rate) as JSON |
| UserTesting | SaaS | Partial | Recordings + transcripts available via API; transcript quality varies |
| Optimal Workshop (Reframer) | SaaS | Partial | Tag-based note analysis; no public API for note import |
| Lookback | SaaS | Partial | Session recordings; limited API surface |
| Dovetail | SaaS | Yes — API | Tag, cluster, and query qualitative data; best-in-class for agent-driven synthesis |
| Otter.ai | SaaS | Yes | Auto-transcribes sessions; exports to text for downstream analysis |

## Templates & scripts
See `templates.md` for the full Test Plan Template and Session Script Template.

```python
# Minimal severity scorer for findings from session notes
# Input: list of dicts with keys: observation, participants_affected (int), task_blocked (bool)
# Output: severity label

def severity(obs: dict, total_participants: int = 5) -> str:
    pct = obs["participants_affected"] / total_participants
    blocked = obs.get("task_blocked", False)
    if blocked and pct >= 0.6:
        return "Critical"
    if blocked or pct >= 0.6:
        return "High"
    if pct >= 0.4:
        return "Medium"
    return "Low"
```

## Best practices
- Write tasks as scenarios, not instructions — "You need to update your shipping address" beats "Go to Account Settings"
- Pilot the test with one internal participant before the real sessions; catches broken prototypes and unclear tasks
- Record sessions even for unmoderated tests — raw video is the audit trail when stakeholders dispute findings
- Aim for 5 participants per distinct user segment, not 5 total across segments
- Separate observation (what happened) from inference (why it happened) in notes; agents can infer later from clean observation data
- Prioritize findings by severity before effort — a Critical finding that takes 30 minutes to fix outranks a Low finding requiring a redesign

## AI-agent gotchas
- Agents asked to generate tasks will sometimes include solution hints ("click the settings icon") — always review task wording before use
- LLM synthesis treats all observations as equally weighted unless explicitly told to weight by frequency; specify "weight by participant count" in the prompt
- Agents will hallucinate participant quotes if given sparse notes; instruct them to mark inferences as [INFERRED] and quotes as [VERBATIM]
- Human-in-the-loop required for severity classification of Critical findings before they go into the backlog — stakes are too high for unreviewed AI judgment
- Synthesis agents tend to over-surface novel observations and under-surface common ones; counter this by prefixing notes with participant count tags

## References
- https://www.nngroup.com/articles/usability-testing-101/
- https://sensible.com/rocket-surgery-made-easy/
- https://www.interaction-design.org/literature/article/how-to-conduct-usability-testing
- https://www.nngroup.com/articles/remote-usability-tests/
- https://dovetail.com/research/usability-testing/
