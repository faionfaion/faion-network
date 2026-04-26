# Agent Integration — Difficult Conversations

## When to use
- Preparing a script for a performance issue conversation that must separate observable facts from interpretations
- Drafting a DESC-structured message to set a boundary (e.g. after-hours messaging norms, scope creep)
- Converting a reactive emotional draft into a STATE-structured, tentative, fact-based opening for a difficult conversation
- Running through a preparation checklist before a high-stakes conversation (saying no to a boss, addressing a peer conflict, raising a systemic problem)

## When NOT to use
- Active crisis conversations that require real-time de-escalation — agents cannot adapt to live emotional cues
- HR formal disciplinary processes where documented language must follow legal requirements
- Conversations involving power asymmetry (e.g. addressing a C-level executive) where organizational context and political judgment are required and an agent has neither
- Anonymous feedback or 360-review contexts where the goal is to protect identity, not drive a conversation

## Where it fails / limitations
- The Crucial Conversations framework requires the human to genuinely "Start with Heart" (know what they want) before the script is useful; a well-drafted script with a hidden agenda will fail in the conversation
- Agents can structure the STATE sequence correctly but cannot verify that the "facts" provided are truly factual and not the human's interpretations — human must do this pre-verification step
- Tone in text-based drafts reads differently than the same words spoken; agent-produced scripts may sound more aggressive or more passive than intended in live delivery
- WWWF commitment templates require follow-up scheduling that agents cannot initiate autonomously

## Agentic workflow
An agent assists difficult conversations in two phases: preparation and drafting. In the preparation phase, the agent receives the raw situation and runs through the Crucial Conversations preparation checklist, prompting the human to supply: what they want for each party, the factual observations (not stories), their contribution to the problem, and the other party's likely perspective. In the drafting phase, the agent generates a STATE-structured opening script and a DESC-structured message if a written boundary is appropriate. The agent should produce a draft, then perform a self-check: does every statement use observable facts? Is the request specific? Is there a genuine question inviting the other party's perspective?

### Recommended subagents
- `faion-sdd-executor-agent` — can sequence preparation → draft → self-review → revision steps for multi-iteration conversation prep

### Prompt pattern
```
Help me prepare for a difficult conversation using the Crucial Conversations framework.
Situation: <describe what happened, with specific facts>
What I want: for me: <goal>; for them: <goal>; for the relationship: <goal>
Facts (not stories): <list specific observable behaviors with dates/frequencies>
My contribution: <what role did I play>
Their likely perspective: <what might they be thinking/feeling>

Output:
1. Preparation checklist assessment (what's clear, what's missing)
2. STATE-structured opening script (3-5 sentences)
3. 2-3 AMPP questions to use when they respond
4. Potential safety risks to watch for and how to restore safety
```

```
Write a DESC script for the following boundary situation.
Situation: <describe specific behavior and its impact>
Target outcome: <what change I need>
Positive consequence if resolved: <what improves>
Negative consequence if unresolved: <what I will do>

Output the DESC script in 4 clearly labeled paragraphs. Keep it under 100 words.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| No specific CLI tools | — | — |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion / Confluence | SaaS | Partial | Agent drafts conversation prep docs; WWWF follow-up logs maintained by human |
| Lattice / 15Five | SaaS | Partial | Performance management platforms; agent drafts structured feedback entries for conversation prep |
| Calendly / Cal.com | SaaS | Partial | Scheduling follow-up after difficult conversations; agent can draft the calendar invite text |
| Loom | SaaS | No | Async video for sensitive messages; content must be delivered by human |

## Templates & scripts
See `templates.md` for Preparation Checklist, STATE script template, DESC script template, and WWWF commitment tracker.

WWWF commitment tracker (inline, post-conversation):
```
## Commitments from [Conversation Topic] — [Date]

| Who | What | By When | Follow-up |
|-----|------|---------|-----------|
| [Name] | [Specific action] | [Date] | [Check-in date/method] |
| [Name] | [Specific action] | [Date] | [Check-in date/method] |

Next check-in: [Date and channel]
```

## Best practices
- Separate facts from stories before writing anything — list raw observations (timestamps, measurable behaviors) and explicitly mark any interpretation as a "story to be tested"
- The STATE script must end with a genuine question, not a rhetorical one; "I'm open to hearing I've got this wrong" must be sincere or it breaks safety immediately
- DESC scripts are for written communication only (Slack, email) when a live conversation is not possible — they are not scripts to read aloud in a meeting
- Address issues early (3-5 day window from the event); agents drafted a week after the fact tend to produce scripts that reference stale context the other party has moved on from
- Prepare the fallback scenario (what you will do if the conversation goes poorly) before the conversation; agents can generate this as a separate section in the prep document

## AI-agent gotchas
- Agents may produce STATE scripts that are technically correct but too long for an opening — the opening should be deliverable in under 60 seconds; instruct the agent to keep the initial script to 3-5 sentences
- "Masking" safety violations (sarcasm, sugarcoating) are hard for agents to detect in human-provided drafts; human must self-assess the tone before input reaches the agent
- Human checkpoint required before using any agent-drafted script in a real conversation — verify every factual claim and that the tone matches the actual relationship
- Agents asked to prepare a "saying no to boss" script may produce overly deferential language that undermines the message; specify the desired assertiveness level explicitly
- AMPP questions generated by agents for live conversations must be memorized and paraphrased, not read from a list; reading questions in a difficult conversation destroys rapport

## References
- https://hbr.org/2017/05/how-to-have-difficult-conversations-when-you-dont-like-conflict
- https://www.mindtools.com/CommSkll/DiffConv.htm
- https://www.cruciallearning.com/crucial-conversations/
- Kerry Patterson et al., "Crucial Conversations: Tools for Talking When Stakes Are High" (McGraw-Hill)
