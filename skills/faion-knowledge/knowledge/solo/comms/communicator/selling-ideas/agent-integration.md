# Agent Integration — Selling Ideas

## When to use
- Drafting audience-specific pitch documents (exec / technical / finance / user / security) from a single idea brief
- Converting feature specs into SPIN-structured stakeholder narratives (Situation → Problem → Implication → Need-Payoff)
- Generating objection-handling scripts for a specific objection set before a live pitch
- Producing elevator pitch variants (10-second, 30-second, 2-minute) from a template brief
- Creating one-pager templates pre-filled from a structured idea input

## When NOT to use
- Live negotiation — agents can prepare but cannot adapt to in-room dynamics in real time
- Replacing human relationship-building; the Challenger Sale "take control" step requires earned trust that an agent cannot establish
- When the audience is unknown — pitch structure varies so much by persona that generic output is often worse than starting from scratch

## Where it fails / limitations
- SPIN question sequences need authentic human delivery; agent-written SPIN scripts read as interrogative rather than curious
- The Challenger Sale "Teach" step requires genuinely novel industry insight — agents will produce plausible-sounding but often generic "insights" that sophisticated buyers will recognize as boilerplate
- Objection handling scripts generated without real objection data tend to address imagined concerns, not actual ones
- Quantification ("40% lower TCO") requires real data; agents will hallucinate specifics if not given source numbers
- "Power phrases" (Weak → Strong word substitutions) are the easiest agent task but have the least impact if the underlying argument is weak

## Agentic workflow
An agent receives an idea brief (problem, solution, audience type, known objections, available metrics). It produces: (1) a SPIN question sequence to run before the pitch, (2) an audience-tailored pitch doc (problem → solution → impact → ask), (3) an objection-response map for up to 5 known objections using LAER, (4) an elevator pitch in three lengths. Each output is a separate section, clearly labeled, so the human can selectively use them.

### Recommended subagents
- General Claude Opus call — for Challenger Sale insight generation and complex persuasion structure; narrative quality matters here
- General Claude Sonnet call — for objection scripting and one-pager drafting; straightforward structured output

### Prompt pattern
Audience-specific pitch:
```
Draft a pitch for: <IDEA_BRIEF>.
Audience: <AUDIENCE_TYPE> (exec | technical | finance | user | security).
Available metrics: <METRICS>.
Structure: Problem (with numbers) → Solution → Impact → Ask.
Length: <TARGET_LENGTH> words.
Do not invent metrics. Mark any missing data as [DATA NEEDED].
```

SPIN question sequence:
```
Generate a SPIN question sequence for pitching: <IDEA>.
Target: <AUDIENCE_ROLE>.
Output 2 questions per stage (Situation, Problem, Implication, Need-Payoff).
Questions must feel curious, not interrogative.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandoc` | Convert agent-generated pitch markdown to PDF or PPTX | `brew install pandoc` / https://pandoc.org |
| `slides.com` CLI (unofficial) | Push markdown to presentation deck | REST API: https://slides.com/api |
| `marp` | Convert markdown pitch doc to slide deck | `npm install -g @marp-team/marp-cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion | SaaS | Yes — REST API | Store pitch variants and track which version was used per audience |
| Google Slides | SaaS | Yes — Google Slides API | Programmatic deck creation from agent-generated content |
| Pitch.com | SaaS | Partial — no public API | Manual paste; good for design-quality decks |
| HubSpot | SaaS | Yes — REST API | Log pitch interactions and objection tracking in CRM |
| Airtable | SaaS | Yes — REST API | Objection library: store, tag, and retrieve objection-response pairs |

## Templates & scripts
See `templates.md` for the one-pager template and presentation outline.

Objection response generator (structured):
```python
LAER_TEMPLATE = """
Objection: {objection}

L - Listen: [Do not interrupt. Let them finish.]
A - Acknowledge: {acknowledge}
E - Explore: {explore_question}
R - Respond: {response}
"""

def generate_laer(objection: str, context: dict) -> str:
    # context provides acknowledge, explore_question, response per objection
    return LAER_TEMPLATE.format(
        objection=objection,
        acknowledge=context.get("acknowledge", "That's a valid concern."),
        explore_question=context.get("explore", "Can you tell me more about what's driving that concern?"),
        response=context.get("response", "[Draft specific response here]"),
    )
```

## Best practices
- Always lead with the Problem, not the Solution — agents default to solution-first because specs are usually solution-first; explicitly reverse the order in the prompt.
- For executive pitches: one metric per slide, no more. An agent will fill space with data; trim ruthlessly.
- SPIN sequences work best when the Implication questions quantify cost ("How much engineering time does a rollback cost?") — ensure the brief includes actual cost data, even rough estimates.
- Build an objection library over time: after each pitch, log real objections raised and effective responses. Feed this library into future agent prompts.
- The Elevator Pitch 10-second version ("We help [WHO] [DO WHAT] [BETTER/FASTER/CHEAPER]") is the hardest to write well and the most important; dedicate a separate prompt pass to it.

## AI-agent gotchas
- Agents will invent specific percentages ("40% faster," "3x ROI") when not given real data — always mark claims as [DATA NEEDED] in the prompt and review before use.
- Challenger Sale "Teach" step output from agents tends toward generic industry trends rather than the specific, counter-intuitive insight that makes the technique effective; validate with actual research.
- "Ask" statements generated by agents are often weak ("Let's schedule a follow-up") — specify what type of commitment you want (time / budget / referral) in the prompt.
- Power-phrase substitutions (Weak → Strong) can sound aggressive if applied wholesale; human review needed to calibrate tone per audience.
- SPIN question sequences generated without audience context will produce Situation questions that are too broad and Implication questions too generic to create urgency.

## References
- Rackham, N. (1988). SPIN Selling. McGraw-Hill.
- Dixon, M. & Adamson, B. (2011). The Challenger Sale. Portfolio/Penguin.
- Harvard Business Review — Persuasion: https://hbr.org/topic/subject/persuasion
- Cialdini, R. (1984). Influence: The Psychology of Persuasion.
- Marp CLI docs: https://marp.app
