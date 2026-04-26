# Agent Integration — User Interviews

## When to use
- In the discovery phase when the problem space is unclear and you need to understand user behaviors and motivations before designing anything
- When you have a hypothesis about a user need and want to validate whether the underlying problem is real
- After launch when unexpected usage patterns emerge in analytics and you need to understand why
- When evaluating a design concept before committing to prototyping or development
- When you need direct quotes and stories to persuade stakeholders who discount internal assumptions

## When NOT to use
- When you need quantitative answers (how many? how often?) — use surveys or analytics
- When users cannot articulate the relevant behavior (e.g., subconscious decision-making, habitual actions) — use observation or diary studies instead
- When the research question is "do users prefer A or B?" — use preference testing or A/B testing
- When no one on the team has time to analyze the data; interviews generate qualitative data that requires synthesis time — collecting without analyzing is waste

## Where it fails / limitations
- Social desirability bias: participants say what they think the interviewer wants to hear, especially about sensitive behaviors
- Recall bias: asking about past behavior produces reconstructed memory, not accurate accounts; ask about recent specific events, not general patterns
- Hypothetical questions produce unreliable data; "would you use a feature that..." reliably overestimates intent
- 5-8 participants per segment reveals dominant themes but misses rare-but-important edge cases
- Interview findings cannot be generalized statistically to the broader population

## Agentic workflow
An agent is most useful in the preparation and synthesis phases, not the interview itself. Pre-interview: an agent can generate a draft interview guide from a research objective, review it for leading questions, and suggest probing follow-ups. Post-interview: an agent can transcribe recordings (with a transcription service), identify recurring themes across notes from multiple sessions, draft an affinity diagram structure, and produce an insight report draft.

The interview itself must be conducted by a human — rapport, real-time follow-up, and non-verbal cues cannot be replicated by an agent. A human must also validate synthesized themes before they are used to inform design decisions.

### Recommended subagents
- `faion-sdd-executor-agent` — generate interview guide from research objectives, synthesize interview notes into themed insights, draft a research findings report
- General Claude subagent — review draft questions for leading language, suggest probing follow-ups, generate insight statements from raw notes

### Prompt pattern
```
You are a UX researcher preparing an interview guide for the following research objective:
"[Research objective]"

Target participant: [Description of participant profile]

Generate:
1. 3-5 warm-up questions (low stakes, build rapport)
2. 8-12 main questions covering: [topics]
3. For each main question, suggest 1-2 probing follow-ups

Rules: No leading questions. No hypotheticals ("would you..."). Ask about specific past behavior, not general opinions.
```

```
Here are notes from [N] user interviews on the topic of [topic]:
[Paste notes]

Identify:
1. Recurring themes (present in 3+ interviews)
2. Outlier themes (1-2 interviews but significant)
3. Direct quotes that best illustrate each theme
4. Contradictions between participants

Format as an affinity map structure ready for team review.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisper` (OpenAI) | Local audio transcription of recorded interviews | `pip install openai-whisper` / github.com/openai/whisper |
| `ffmpeg` | Convert audio/video interview recordings to supported formats | `brew install ffmpeg` / ffmpeg.org |
| `otter.ai CLI` (unofficial) | Transcription service integration | Third-party wrappers; otter.ai |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| User Interviews | SaaS | Partial (API) | Participant recruitment panel; scheduling and screener management |
| Calendly | SaaS | Yes (REST API) | Interview scheduling automation; webhook-driven |
| Otter.ai | SaaS | Partial (export) | Auto-transcription; export as text for agent processing |
| Dovetail | SaaS | Partial (API) | Research repository; tag-based analysis; API for data access |
| Grain | SaaS | No | Video recording + AI highlights; no programmatic API |
| Lookback | SaaS | No | Live and recorded user research sessions |

## Templates & scripts
See `templates.md` for interview guide template (with introduction script, warm-up, main questions, wrap-up) and interview notes template (key quotes, observations, pain points, needs, behaviors, surprises).

Inline: batch-process interview notes into a theme frequency table:
```python
from collections import Counter

def theme_frequency(interviews: list[dict], min_count: int = 2) -> list[dict]:
    """
    interviews: list of {participant_id, themes: list[str]}
    Returns themes appearing in min_count or more interviews, sorted by frequency.
    """
    counter = Counter()
    for interview in interviews:
        for theme in set(interview.get("themes", [])):  # set: count per participant, not per mention
            counter[theme] += 1
    return [
        {"theme": theme, "count": count, "pct": round(count / len(interviews) * 100)}
        for theme, count in counter.most_common()
        if count >= min_count
    ]
```

## Best practices
- Record every session with explicit consent; memory and notes are unreliable for verbatim quotes, which are high-value for stakeholder communication
- Start with the most recent specific event ("Tell me about the last time you...") before asking about general patterns — specific events are more reliable than reconstructed summaries
- Silence is a tool; after a participant finishes an answer, wait 3-5 seconds before speaking — participants often add the most revealing information when they fill the silence
- Debrief immediately after each session while memory is fresh; notes degrade significantly within 24 hours
- Recruit participants who have done the relevant behavior recently (within 2-4 weeks) for episodic recall tasks; older experiences produce more reconstructed and less reliable data
- When synthesizing, distinguish between "what participants said" (observation) and "what it means" (interpretation) in your notes — conflating them bakes assumptions into research findings

## AI-agent gotchas
- Do not ask an agent to identify insights from raw notes without first validating the transcription accuracy — transcription errors propagate into analysis
- Agent-generated interview guides often include double-barreled questions ("How do you find the product and what do you like about it?") — always human-review the generated guide
- Agents default to generating leading questions when given a product brief with an implicit positive framing; prompt explicitly to check for leading language
- LLM synthesis can create "consensus illusions" — presenting a theme as universal when it appeared in 2 of 6 interviews; require the agent to state exact participant counts
- Agent affinity diagrams are useful starting points but collapse nuance; human review of the raw quotes is required before the themes are finalized

## References
- Portigal, S. "Interviewing Users." Rosenfeld Media, 2013.
- Fitzpatrick, R. "The Mom Test." Self-published, 2019. https://www.momtestbook.com/
- NNg user interviews: https://www.nngroup.com/articles/user-interviews/
- IDF how to conduct user interviews: https://www.interaction-design.org/literature/article/how-to-conduct-user-interviews
- User Interviews field guide: https://www.userinterviews.com/ux-research-field-guide-chapter/user-interviews
