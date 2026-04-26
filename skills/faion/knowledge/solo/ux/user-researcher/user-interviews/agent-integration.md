# Agent Integration — User Interviews

## When to use
- Problem discovery: before building anything, to understand what actually frustrates users
- Persona refinement: when you have a hypothesis about your customer but no behavioral data
- Feature prioritization: when analytics show a drop-off but not the reason
- Post-churn analysis: interviewing recently cancelled customers to identify root causes
- Concept testing: showing early wireframes or prototypes to get qualitative reaction

## When NOT to use
- When you need statistical significance — interviews are qualitative, not representative
- When you can observe behavior directly (analytics, session recordings are faster and less biased)
- When the team cannot act on qualitative findings (no backlog, no decision-maker involved)
- When participants have strong incentive to be positive (e.g., recruited from your paying customer list with a discount offer at stake)
- As a substitute for usability testing — interviews reveal problems, not whether users can navigate your UI

## Where it fails / limitations
- Participants describe what they think they do, not what they actually do — always follow up with "tell me the last time you did that"
- Small samples (fewer than 10) surface unique anecdotes that may not generalize to patterns
- Recruitment from social networks skews toward early adopters who are not representative of the mainstream market
- Remote interviews miss non-verbal cues that often contain the most honest signal
- Analysis paralysis: raw interview notes without a synthesis step produce a pile of data nobody uses

## Agentic workflow
Claude subagents can generate tailored interview scripts given research goals and target persona, draft outreach messages for participant recruitment, and synthesize raw interview transcripts into structured findings (pain point ranking, pattern table, representative quotes). Transcript synthesis is the highest-leverage agent task — a subagent can process 10 transcripts in one pass and return a filled Interview Synthesis template. Human researchers must conduct the actual interviews; the agent cannot replace live conversation.

### Recommended subagents
- `faion-persona-builder-agent` — generates interview script, analyzes transcripts, extracts pain-point patterns
- `faion-research-agent` (mode: validate) — cross-validates interview findings against public forum data

### Prompt pattern
```
Generate an interview script for the following research goal and target participant.
Follow The Mom Test principles: ask about past behavior, not hypothetical intent.
Do not include any question that starts with "Would you..." or "Do you think...".

Research goal: {goal}
Target: {persona description}
Duration: 25 minutes
```

```
Analyze the following interview transcripts. For each theme:
1. Count how many interviews mention it
2. Extract the single most representative verbatim quote
3. Rate pain severity: Critical / Moderate / Minor
4. Note any surprising insight that contradicts the research hypothesis

Hypothesis: {hypothesis}
Transcripts: {transcripts}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisper` (OpenAI) | Local transcription of recorded interviews | `pip install openai-whisper` |
| `assembly-ai` CLI | Cloud transcription with speaker diarization | assemblyai.com/docs |
| `otter.ai` | Live transcription + highlight extraction | otter.ai (no CLI, API available) |
| `dovetail` API | Research repository for tagging and synthesis | dovetail.com/api |
| `notion` API | Store and share interview notes + synthesis | developers.notion.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| AssemblyAI | SaaS | Yes | Speaker diarization; auto-chapters; REST API |
| Whisper (local) | OSS | Yes | Runs offline; no diarization without extras |
| Dovetail | SaaS | Partial | API for importing notes; tagging is manual |
| Grain | SaaS | No | Good for human highlight clips; no API |
| Calendly | SaaS | Yes | Scheduling API; auto-send invite links |
| Typeform | SaaS | Yes | Screener survey before interviews; API for responses |
| Respondent.io | SaaS | No | B2B participant recruitment; manual workflow |

## Templates & scripts
See `templates.md` for Interview Script and Interview Synthesis templates.

Inline helper — transcribe and extract quotes from interview recording:
```python
import whisper, json

def transcribe_interview(audio_path: str, research_topics: list[str]) -> dict:
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    transcript = result["text"]

    # Extract segments mentioning research topics
    quotes = []
    sentences = transcript.split(". ")
    for s in sentences:
        if any(topic.lower() in s.lower() for topic in research_topics):
            quotes.append(s.strip())

    return {
        "full_transcript": transcript,
        "relevant_quotes": quotes[:20],  # top 20 candidates for review
    }

output = transcribe_interview("interview_01.mp3", ["invoicing", "time tracking", "clients"])
print(json.dumps(output, indent=2))
```

## Best practices
- Always record with participant consent — notes taken during interviews miss 60-70% of the content
- Aim for 10-15 interviews per distinct user segment before looking for patterns; saturation typically occurs at 12 for a narrow problem space
- Send a "pre-interview brief" 24h before: what the call is about, that it is not a sales call, and that recording is requested — reduces no-shows and cold-start awkwardness
- Debrief immediately after each interview while memory is fresh; write the three most surprising things before opening your notes
- Use affinity diagramming for synthesis: cluster quotes by theme before counting — counting first anchors you to your initial categories
- Referrals from completed interviews are the highest-quality recruitment channel; always ask at the end

## AI-agent gotchas
- Agents generating interview scripts will often include hypothetical questions ("Would you pay for...?") unless explicitly forbidden — always include the Mom Test constraint in the prompt
- Transcript synthesis by LLM tends to emphasize dramatic quotes over frequent but mundane patterns; require the agent to report frequency counts alongside quotes
- Agents will hallucinate participant quotes if given partial or noisy transcripts; always pass clean transcripts and ask the agent to cite line numbers
- Recruitment message generation by agents is often too long and formal for cold outreach; specify a 5-sentence maximum
- Human checkpoint required after synthesis before the findings are used to make product decisions — agent synthesis surfaces patterns but cannot judge their strategic importance

## References
- Rob Fitzpatrick: *The Mom Test* — https://www.momtestbook.com
- Nielsen Norman Group: User Interviews — https://www.nngroup.com/articles/user-interviews/
- Steve Portigal: *Interviewing Users* (Rosenfeld Media)
- Whisper OSS: https://github.com/openai/whisper
- AssemblyAI Docs: https://www.assemblyai.com/docs
- Dovetail Research Repository: https://dovetail.com
