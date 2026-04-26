# Agent Integration — Stakeholder Communication

## When to use
- Preparing an interview guide for a stakeholder discovery session (requirements gathering, user research, product feedback)
- Mapping stakeholders by power/interest before a project kickoff to determine communication frequency and channel per quadrant
- Drafting post-meeting validation summaries that stakeholders must confirm before work proceeds
- Generating Socratic question sequences to probe a vague requirement like "make it faster" or "improve UX"

## When NOT to use
- Replacing live dialogue — agent-generated questions are preparation aids, not substitutes for real conversations
- Stakeholder situations with high political sensitivity where each word choice carries organizational weight and must be chosen by a human with full context
- Legal or contractual negotiations where communication must follow specific protocol

## Where it fails / limitations
- The five dialogue modes require selection based on relationship context and stakeholder personality — agents recommend modes based on situation parameters alone, which may be incomplete
- Validation summaries drafted by agents may paraphrase requirements inaccurately if the source transcript is ambiguous; stakeholder confirmation of the summary is mandatory before proceeding
- Brainstorm facilitation prompts work well as preparation but live facilitation requires real-time adaptation that agents cannot provide
- Power/Interest grid placement requires organizational knowledge an agent cannot infer from a brief description

## Agentic workflow
An agent supports stakeholder communication in the preparation and documentation phases. Pre-session: the agent receives stakeholder profile (role, known interests, concerns, dialogue mode needed) and generates a structured interview guide or brainstorm facilitation plan. Post-session: the agent receives a transcript or notes and produces a structured validation summary (requirements captured, ambiguities flagged, next steps) for stakeholder sign-off. The agent can also generate Socratic question chains from a vague requirement to help the human probe deeper in a live conversation.

### Recommended subagents
- `faion-sdd-executor-agent` — drives structured discovery documentation tasks (meeting prep → session notes → validation summary → requirement card)

### Prompt pattern
```
Generate a stakeholder interview guide using Mode 1 (Interview Protocol).
Stakeholder: <Name, Role>
Project context: <1-2 sentences>
Known interests/concerns: <bullet list>
Questions needed: 8-12 total
Include: context → problem → impact → goal → constraints → priority sequence.
For each question, note the question type (open / probing / clarifying / hypothetical / summary).
```

```
A stakeholder said: "<vague requirement>"
Generate a Socratic question chain (6-8 questions) to uncover the real need.
Cover: definition, assumption, evidence, boundary, metric, implication.
Output as a numbered list. Each question on one line. No preamble.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| No specific CLI tools | — | — |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion / Confluence | SaaS | Partial | Agent drafts meeting prep templates and validation summaries; stakeholder review and confirmation still human |
| Otter.ai / Fireflies | SaaS | Partial | Transcribes meeting audio; agent post-processes transcript to extract requirements and ambiguities |
| Miro | SaaS | No | Brainstorm facilitation board; visual collaboration requires human operation |
| Linear / Jira | SaaS | Partial | Agent generates requirement cards from validated summaries; ticket creation can be automated |
| Loom | SaaS | No | Async video stakeholder updates; not programmable for content generation |

## Templates & scripts
See `templates.md` for meeting prep template, requirement capture card, and post-meeting validation email template.

Post-meeting validation email template (inline):
```
Subject: Summary — [Meeting Topic] — please confirm

Hi [Name],

Thank you for the session. Here is what I captured:

Problem/Need:
- [Specific need 1]
- [Specific need 2]

Success criteria:
- [How we'll know we succeeded]

Constraints:
- [Known limitations]

Open questions / ambiguities flagged:
- [Item requiring clarification]

Next steps:
- [Action] — [Owner] — [Date]

Please reply to confirm this is accurate, or correct anything I missed.
```

## Best practices
- Always select the dialogue mode before generating questions — Interview questions and Socratic questions have fundamentally different structures and mixing them produces incoherent sessions
- Validation summaries must be sent within 24 hours of a meeting while the stakeholder's memory is fresh; an agent can draft immediately post-session but a human should review before sending
- Clarification questions for vague terms ("real-time", "user-friendly", "scalable") must offer interpretations A/B/C rather than open-ended restatement — agents should generate multiple-choice clarifications, not just "what do you mean?"
- For "Changing" stakeholder type, log every requirement change with a timestamp and the stakeholder's name in the requirement capture card — agent-generated logs are admissible as a paper trail
- Post-session, flag ambiguities explicitly in the validation summary — do not silently resolve them with a default interpretation

## AI-agent gotchas
- Agents generating interview guides default to generic questions ("What are your goals?") unless the stakeholder role and project context are provided in specific detail
- Transcription-based requirement extraction fails when multiple stakeholders talk over each other or use domain jargon; human annotation of key exchanges improves accuracy significantly
- Socratic question chains must not be used in sequence without human adaptation — using them verbatim in a live conversation feels interrogative and damages rapport
- Human checkpoint required before sending any validation summary — the agent may misparaphrase a nuanced requirement, and stakeholder sign-off on a wrong summary creates downstream rework
- Power/Interest grid assignments must be reviewed by a human with organizational context; an agent using only job titles will misplace politically influential stakeholders who have informal power

## References
- https://www.pmi.org/learning/library/stakeholder-engagement-plan-6090
- https://hbr.org/topic/subject/stakeholder-management
- https://www.mindtools.com/pages/article/newPPM_07.htm
