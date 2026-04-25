# Agent Integration — The Mom Test

## When to use
- Early customer discovery before any code is written — validating that a problem is real and frequent
- Screening interview transcripts to identify compliments vs. genuine signals
- Generating interview question scripts that avoid leading, future-hypothetical, or opinion-seeking phrasing
- Extracting commitment signals (time, money, referrals) from existing interview notes or CRM records

## When NOT to use
- Post-launch product analytics — Mom Test is a discovery tool, not a measurement tool
- B2B enterprise deals where procurement rules require formal RFPs; the conversational style reads as unprepared
- Quantitative surveys — the methodology is explicitly qualitative and single-subject
- When you already have paying customers with observable behavior; switch to churn/retention analysis instead

## Where it fails / limitations
- Agents can generate Mom Test-compliant questions but cannot actually conduct the interview — human presence is irreplaceable for reading body language, emotion, hesitation
- Pattern recognition across 5+ interviews requires human synthesis; an LLM can help but may hallucinate inter-interview patterns if transcripts are paraphrased
- The "80% listening" rule is a human behavioral constraint that has no equivalent in agent-driven async interviews
- Commitment escalation (time → reputation → money) requires trust built over a real interaction; agents cannot build that rapport in a single text exchange
- Transcripts fed to an LLM for analysis carry interviewer bias already baked in — if questions were leading, the analysis will be too

## Agentic workflow
An agent ingests a problem hypothesis and generates a Mom Test-compliant question bank (past-behavior, specific, non-leading). After interviews are conducted by a human, the agent receives raw transcripts and applies a signal extractor prompt: classify each statement as Problem Signal / Current Solution Signal / Commitment Signal / Compliment (discard) / Red Flag (hypothetical). A synthesis pass surfaces patterns across transcripts and updates the problem hypothesis.

### Recommended subagents
- General Claude Sonnet call — question generation and transcript analysis; Sonnet handles nuanced classification well
- `faion-knowledge` (researcher domain) — for user-interview methodology cross-reference

### Prompt pattern
Question generation:
```
You are helping with customer discovery using The Mom Test.
Problem hypothesis: <HYPOTHESIS>
Generate 10 interview questions. Rules:
- No opinion questions ("Do you think...")
- No future hypotheticals ("Would you...")
- No leading questions
- Ask about past behavior and specific experiences only
Output: numbered list of questions only.
```

Transcript analysis:
```
Classify each statement from this interview transcript.
Categories: PROBLEM_SIGNAL | CURRENT_SOLUTION | COMMITMENT | COMPLIMENT | RED_FLAG
Format: [CATEGORY] "exact quote"
Transcript: <TRANSCRIPT>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `otter.ai` CLI/API | Transcribe interview recordings automatically | https://otter.ai/api |
| `whisper` (OpenAI) | Local audio-to-text for interview recordings | `pip install openai-whisper` |
| `rev.com` API | Professional transcription with speaker diarization | https://www.rev.com/api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Otter.ai | SaaS | Yes — REST API | Auto-transcription + speaker ID; agent can ingest output JSON |
| Dovetail | SaaS | Partial — REST API | Qualitative research repo; agent can tag highlights via API |
| Notion | SaaS | Yes — REST API | Store interview notes; agent can write structured summaries |
| Airtable | SaaS | Yes — REST API | Track interviewee list and signal counts per hypothesis |
| Typeform | SaaS | Yes — REST API | Run async written Mom Test interviews; agent parses responses |

## Templates & scripts
See `templates.md` for the full Interview Template (Opening / Exploration / Digging / Closing).

Signal extraction helper (post-interview note processing):
```python
SIGNAL_TYPES = {
    "PROBLEM": ["struggle", "hard", "frustrating", "pain", "waste", "annoying"],
    "CURRENT_SOLUTION": ["I use", "we use", "currently", "right now", "we pay"],
    "COMMITMENT": ["introduce", "pilot", "deposit", "beta", "send you", "schedule"],
    "RED_FLAG": ["would", "might", "probably", "I think I'd", "generally"],
}

def classify_statements(statements: list[str]) -> list[dict]:
    results = []
    for s in statements:
        lower = s.lower()
        matched = [k for k, v in SIGNAL_TYPES.items() if any(w in lower for w in v)]
        results.append({"statement": s, "signals": matched or ["COMPLIMENT"]})
    return results
```

## Best practices
- Run the question generation pass before each interview, not once at project start — adapt based on what previous interviews revealed.
- After 5 interviews, run a cross-transcript synthesis pass and update a shared "problem hypothesis" doc before the next batch.
- Store exact quotes, never paraphrases — paraphrasing introduces agent bias during re-processing.
- Track the commitment escalation ladder per interviewee: Time → Reputation → Money. Anyone who only gives verbal compliments should be weighted near zero.
- Ask "Who else should I talk to?" at the end of every interview; this surfaces the strongest signal (high-trust referral) and expands the sample.

## AI-agent gotchas
- LLMs will generate compliant-looking questions that are still subtly leading ("What challenges have you faced with X?" implies X is challenging). Review question wording against the three Mom Test rules before use.
- Transcript summarization almost always loses nuance — agents tend to summarize away the specific words and dollar amounts that are the most valuable signals.
- An agent asked to "find patterns across 5 interviews" will hallucinate consensus if the transcripts are thin; require minimum quote count per pattern (e.g., 3+ independent mentions).
- Human checkpoint required: the agent cannot distinguish genuine enthusiasm from rehearsed politeness in text transcripts without tone markers.
- Never let the agent score "problem severity" on a 1-10 scale from text alone — it will produce confident-sounding numbers without valid basis.

## References
- Fitzpatrick, R. (2013). The Mom Test. Motiv Publishing.
- Y Combinator: How to Talk to Users — https://www.ycombinator.com/library/6g-how-to-talk-to-users
- First Round Review: The Right Way to Ask the Right Questions — https://review.firstround.com/the-right-way-to-ask-the-right-questions
- Dovetail qualitative analysis docs: https://developers.dovetail.com
