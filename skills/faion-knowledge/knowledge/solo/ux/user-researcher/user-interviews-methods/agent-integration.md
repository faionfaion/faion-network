# Agent Integration — User Interview Methods

## When to use
- Before building a new feature or product when validating a problem hypothesis
- When churn or low adoption is unexplained and qualitative signal is missing
- Designing the interview guide for a discovery sprint (5–15 interviews)
- Synthesizing transcripts from completed interviews into insight clusters
- Identifying follow-up interview candidates from existing community/customer lists

## When NOT to use
- When you need quantitative confidence (n < 10 gives no statistical power — use surveys for that)
- When the decision has already been made — interviews at this stage are rationalization theatre
- Replacing usability testing: interviews surface beliefs, not behaviors; watch users act instead
- When speed is the only constraint and even 3 interviews are not feasible — go straight to a fake door test

## Where it fails / limitations
- LLMs cannot conduct live interviews; they can only draft guides, simulate practice, and synthesize existing transcripts
- Transcript synthesis can miss sarcasm, hesitation, or emotional subtext that a human interviewer catches in-session
- Agents cannot recruit participants — that requires CRM/calendar access and human trust
- Confirmation bias is systemic: if the agent was given a one-sided brief, synthesized "insights" will skew toward that bias

## Agentic workflow
An agent is most useful in two phases: preparation (drafting the interview guide from a problem hypothesis) and synthesis (extracting themes, quotes, and patterns from transcripts). In the middle — the live interview itself — the human researcher runs the conversation. A preparation agent can also simulate a practice interviewee to help the researcher warm up; a synthesis agent can cluster responses into a findings report within minutes of a batch of interviews completing.

### Recommended subagents
- `faion-sdd-executor-agent` — run synthesis tasks within a structured SDD workflow
- Any general Claude subagent — draft interview guides, generate practice simulations, synthesize transcripts

### Prompt pattern
```
Draft a 45-minute user interview guide for validating the following problem hypothesis:
Hypothesis: <paste hypothesis>
Interview type: Problem (discovery)
Target segment: <paste segment description>
Output: warm-up questions, context questions (5), pain exploration questions (5), solution probing (3), wrap-up.
Do NOT include leading questions. Ask only about past behavior, not future intent.
```

```
You are a qualitative researcher. Given the following interview transcripts, identify:
1. Top 3 recurring pain themes with supporting quotes
2. Surprising findings (not in original hypothesis)
3. Segments who do NOT have this problem
Transcripts: <paste transcripts>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Otter.ai CLI (API) | Auto-transcription of recorded interviews | otter.ai (REST API; no official CLI) |
| Whisper (OpenAI) | Local audio transcription | `pip install openai-whisper` / github.com/openai/whisper |
| Dovetail API | Upload transcripts, tag, cluster insights | dovetail.com/api |
| Grain | Interview recording + highlights | grain.com (no CLI; Zapier integration) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Dovetail | SaaS | Yes (REST API) | Upload transcripts, query tags/themes, export insights |
| Notion | SaaS | Yes (API) | Store guides and findings; query pages via API |
| Calendly | SaaS | Partial (webhooks) | Agent can receive booking notifications; cannot create bookings as interviewee |
| Otter.ai | SaaS | Partial (REST API) | Retrieve transcripts after recording; upload audio |
| Whisper (local) | OSS | Yes | Agent can shell-call `whisper audio.mp3 --output_format txt` |
| UserTesting | SaaS | No | No public API; recordings are proprietary |

## Templates & scripts
See `templates.md` (or the embedded templates in `README.md`) for the Interview Script and Interview Guide.

Inline script — batch transcript theme extractor:
```python
# theme_extractor.py — count keyword themes across transcript files
import os, re
from collections import Counter

THEMES = ["frustrating", "hate", "can't figure out", "wish", "workaround", "too long", "confusing"]
folder = "./transcripts"

theme_counts = Counter()
for fname in os.listdir(folder):
    if fname.endswith(".txt"):
        text = open(os.path.join(folder, fname)).read().lower()
        for theme in THEMES:
            theme_counts[theme] += len(re.findall(re.escape(theme), text))

for theme, count in theme_counts.most_common():
    print(f"{count:3d}  {theme}")
```

## Best practices
- Write the hypothesis before the first interview; if it changes mid-session you are learning, not confirming
- Keep the guide to 5 core questions — pad with "tell me more" probes, not new questions
- Record with explicit consent; take sparse notes during so you stay present
- Do synthesis within 24 hours while memory is fresh; do not batch all synthesis to the end of 10 interviews
- Run at least one "enemy" interview: someone who should not be your customer; it sharpens problem definition
- Treat every "would you use this?" as a red flag answer — it is not data

## AI-agent gotchas
- Do not feed LLMs interview transcripts containing PII without scrubbing names first
- LLM synthesis of transcripts will surface the most frequent words — instruct it explicitly to also flag low-frequency but high-intensity signals
- A practice simulation (agent playing an interviewee) creates false confidence; use it only for question phrasing, not for outcome prediction
- Human checkpoint: the researcher must validate that synthesized insight clusters reflect what was actually said, not what sounds plausible
- Agents cannot assess body language, voice hesitation, or facial expression — qualitative signal is always incomplete when mediated by text transcripts

## References
- Rob Fitzpatrick, "The Mom Test" (momtestbook.com)
- https://www.nngroup.com/articles/user-interviews/
- Steve Portigal, "Interviewing Users" (rosenfeld media)
- https://www.intercom.com/blog/running-user-research-interviews/
- Erika Hall, "Just Enough Research" (A Book Apart)
