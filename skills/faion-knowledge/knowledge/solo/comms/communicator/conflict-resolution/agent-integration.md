# Agent Integration — Conflict Resolution

## When to use
- Drafting an NVC-structured message to address a recurring team behavior (late deliveries, skipped reviews, missed SLAs)
- Preparing a structured mediation agenda for a team retrospective where two parties have a documented disagreement
- Converting an emotionally charged draft message into an observation-based, non-evaluative version before sending
- Coaching a manager to select the right Thomas-Kilmann conflict mode for a specific situation

## When NOT to use
- Active real-time conflict where a human mediator must be present — written NVC scripts cannot replace live dialogue
- Legal disputes or HR formal complaints where documented communication must follow legal protocols
- Anonymous feedback systems where the goal is data aggregation, not dialogue

## Where it fails / limitations
- NVC requires the receiver to engage in good faith; an agent can draft NVC-structured messages, but the human must decide whether the relationship context supports that approach
- Thomas-Kilmann mode selection depends on organizational culture, power dynamics, and relationship history that an agent cannot verify from a text prompt
- De-escalation scripts written by an agent may feel scripted or patronizing if used verbatim — they are drafts for human adaptation, not final messages
- Cross-cultural conflict resolution has different norms for directness, face-saving, and authority respect that general frameworks do not account for

## Agentic workflow
An agent assists conflict resolution by transforming a raw, emotionally charged message draft into an NVC-structured version: it identifies evaluations disguised as observations, replaces them with factual observations, and adds a need and specific request. For mode selection, the agent receives the situation parameters (stakes, relationship importance, time available, power dynamics) and outputs a ranked recommendation with rationale. Mediation agendas are generated from a structured brief: parties, positions, shared interests, ground rules.

### Recommended subagents
- `faion-sdd-executor-agent` — suitable for driving multi-step conflict documentation tasks (situation capture → NVC draft → review checklist)

### Prompt pattern
```
Rewrite the following message using Nonviolent Communication (NVC) format.
Original message: "<paste draft>"
Target audience: <colleague / manager / direct report>
Apply the 4 steps:
1. Observation: replace evaluations with specific, factual observations
2. Feeling: identify the specific emotion (not a thought disguised as a feeling)
3. Need: name the universal need behind the feeling
4. Request: make a specific, positive, doable request
Output: the rewritten message only, no commentary.
```

```
Given this conflict situation, recommend the best Thomas-Kilmann conflict mode.
Situation: <describe the conflict>
Stakes: <high / medium / low>
Relationship importance: <long-term partner / short-term / one-off>
Time available: <urgent / moderate / flexible>
Power balance: <equal / I have more / they have more>
Output: recommended mode, one-sentence rationale, one alternative mode to consider.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| No standard CLI tools specific to conflict resolution | — | — |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion / Confluence | SaaS | Partial | Agent drafts mediation agendas and conflict logs; human manages meeting scheduling and follow-up |
| Loom | SaaS | No | Async video messaging useful for sensitive feedback but not programmable |
| Slido / Mentimeter | SaaS | Partial | Anonymous team pulse surveys surface conflict signals; agent can generate survey questions |
| 15Five / Lattice | SaaS | Partial | Performance and feedback platforms; agent can draft NVC-structured feedback entries |

## Templates & scripts
See `templates.md` for NVC message template, mediation agenda, and conflict resolution process checklist.

NVC message draft template (inline):
```
Subject: [Topic] — clarifying conversation request

When [specific, observable behavior / event with date or frequency]...
I feel [emotion word — not "I feel that..."]...
because I need [universal need: predictability / respect / support / clarity]...

Would you be willing to [specific, positive, doable action]?

I'm available to discuss this [proposed time / channel].
```

## Best practices
- NVC messages should reference a specific instance with a date or measurable fact, not a pattern ("the last 3 Monday reports" not "always")
- Mode selection matters more than script quality; choosing Competing when Collaborating is appropriate produces short-term compliance and long-term resentment
- De-escalation requires the agent-drafted script to be internalized and paraphrased by the human — verbatim reading sounds scripted and reduces trust
- Address conflicts when stakes are low — a small behavior addressed early via NVC is far easier than a full mediation after resentment has built up
- Written conflict communication (email/Slack) is only appropriate for setting up a conversation, not for the conversation itself; agent-drafted messages should always end with a request to meet

## AI-agent gotchas
- Agents may produce NVC messages that are technically correct but too formal or clinical for the relationship context — tone calibration requires human judgment
- Feeling word selection is a known failure point: agents often output "I feel that you..." (a thought) instead of a genuine emotion word; validate output against the NVC feeling vocabulary
- Human checkpoint required before sending any conflict-related message drafted by an agent — the agent cannot know the full relationship history, power dynamics, or organizational context
- Agents asked to select a conflict mode may default to "Collaborating" in all scenarios because it sounds positive — push back and supply accurate situation parameters
- Do not use agents to draft messages in active, escalated conflicts; human judgment about tone and timing is irreplaceable in high-stakes situations

## References
- https://www.mindtools.com/CommSkll/ConflictResolution.htm
- https://www.pon.harvard.edu/category/research_projects/conflict-resolution/
- Marshall Rosenberg, "Nonviolent Communication: A Language of Life" (PuddleDancer Press)
- Kenneth Thomas & Ralph Kilmann, "Thomas-Kilmann Conflict Mode Instrument" (CPP, Inc.)
