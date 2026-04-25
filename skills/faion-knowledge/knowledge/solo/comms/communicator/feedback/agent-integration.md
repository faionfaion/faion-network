# Agent Integration — Giving & Receiving Feedback

## When to use
- Drafting SBI (Situation-Behavior-Impact) feedback statements from raw notes or a situation description
- Converting vague performance feedback ("this is bad") into specific, observable, behavior-anchored statements
- Generating code-review feedback that follows SBI rather than opinion ("This is bad code" → SBI equivalent)
- Producing EEC (Example-Effect-Continue) positive feedback from performance data or peer notes
- Creating feedback templates pre-configured for specific contexts (code review, presentation, missed deadline)

## When NOT to use
- Delivering feedback live — agent-drafted scripts must be reviewed and personalized before use; mechanical delivery damages trust
- High-stakes performance improvement plans or termination conversations — these require HR and legal review, not LLM drafting
- Receiving feedback on behalf of a human — the LEARN framework (Listen, Explore, Acknowledge, Reflect, Next) requires genuine human engagement
- When the root cause of the behavior is unknown — SBI without the SBII Intent Inquiry step can attribute blame incorrectly

## Where it fails / limitations
- SBI generation without first-hand situational context produces plausible-sounding but potentially inaccurate statements
- Agents will soften feedback toward Ruinous Empathy unless explicitly prompted to be direct — the path of least resistance for an LLM is vague kindness
- The Radical Candor quadrant placement ("You're in Obnoxious Aggression territory") requires judgment about human relationships and history that agents cannot assess
- Feedback timing rules (within 48 hours, never public) are process constraints agents cannot enforce — they can only document them
- SBII "Intent Inquiry" step requires a real two-way conversation; agents can draft the inquiry question but cannot conduct the follow-up

## Agentic workflow
An agent receives a situation description, observable behavior description, and measurable impact. It produces: (1) an SBI-formatted feedback statement, (2) an optional SBII version with an intent inquiry question appended, (3) a Radical Candor quadrant check (flags if the draft leans toward Ruinous Empathy or Obnoxious Aggression), (4) a suggested follow-up check-in question. For positive feedback, agent receives an example and produces an EEC statement with a specific continuation prompt.

### Recommended subagents
- General Claude Sonnet call — SBI/EEC drafting; structured output, low hallucination risk when given real situation data
- General Claude Haiku call — bulk conversion of raw feedback notes to SBI format; mechanical transformation task

### Prompt pattern
SBI drafting:
```
Draft feedback using the SBI model.
Situation: <SPECIFIC_CONTEXT>
Behavior: <OBSERVABLE_ACTION_ONLY — no personality judgments>
Impact: <MEASURABLE_EFFECT_ON_TEAM_PROJECT_RELATIONSHIP>
Output: One paragraph SBI statement, direct but respectful.
Then: Flag if the statement includes personality adjectives (must not).
Then: Add one SBII intent inquiry question.
```

Vague feedback conversion:
```
Convert this vague feedback into an SBI statement.
Original: "<VAGUE_FEEDBACK>"
Context: <WHAT_HAPPENED>
Constraints: Observable behavior only. No adjectives describing character.
Output: SBI statement + one follow-up question.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `notion-cli` / Notion API | Store feedback records with SBI structure as database entries | https://developers.notion.com |
| `15five` API | Performance feedback platform with structured review cycles | https://www.15five.com/api |
| `lattice` API | Goals + feedback + reviews in one platform | https://lattice.com/api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| 15Five | SaaS | Yes — REST API | Weekly check-ins + SBI-compatible feedback fields |
| Lattice | SaaS | Yes — REST API | Full performance management; agent can draft feedback entries |
| Notion | SaaS | Yes — REST API | Custom feedback databases; agent writes structured records |
| GitHub PR review | SaaS | Yes — REST API | Agent posts SBI-formatted review comments via PR review API |
| Linear | SaaS | Yes — REST API | Link feedback to issues for code-review context |

## Templates & scripts
See `templates.md` for positive and constructive feedback templates.

Bulk SBI formatter (code review batch):
```python
def format_sbi_code_review(
    pr_title: str,
    observation: str,
    impact: str,
    suggestion: str,
) -> str:
    """Formats a single PR observation as SBI + recommendation."""
    return (
        f"In this PR ({pr_title}), when {observation}, "
        f"{impact}. "
        f"Going forward: {suggestion}"
    )

# Example usage:
comment = format_sbi_code_review(
    pr_title="auth refactor #142",
    observation="the token validation logic was duplicated across 3 handlers",
    impact="I spent 15 minutes tracing which version was authoritative, "
          "and the inconsistency creates a security risk if one copy gets patched",
    suggestion="extract to a single validate_token() utility and import it",
)
```

## Best practices
- Run a "personality adjective check" on every drafted SBI statement — any word describing character ("careless," "unreliable," "brilliant") must be removed; replace with observable behavior.
- For code-review feedback specifically: frame the Situation as the PR context, not the person ("In PR #142, when the auth logic was duplicated..." not "When you duplicated auth logic...").
- Positive feedback via EEC should be as specific as constructive feedback — vague praise ("great job!") is as useless as vague criticism; the agent should generate specific EEC, not generic affirmation.
- The 2-minute rule applies to agent drafting too: if the feedback can be drafted in 2 minutes of agent time, do it immediately while context is fresh; don't batch feedback for the end-of-sprint.
- Radical Candor check: after drafting, ask the agent "Does this read as caring about the person's growth, or just criticizing?" — if the latter, add one sentence about why the behavior matters to the person's development.

## AI-agent gotchas
- Agents default toward Ruinous Empathy (too soft) unless specifically prompted to "be direct." Even with that instruction, they will add hedging language ("you might consider," "perhaps") — remove it in review.
- Feedback sandwich ("positive → negative → positive") is deprecated in the methodology but agents frequently produce it because it's the most common pattern in training data; explicitly prohibit it in the prompt.
- The SBII Intent Inquiry ("Help me understand what you were trying to do?") is powerful but an agent cannot conduct the follow-up conversation; it can only draft the opening question.
- Human checkpoint required: before sending any agent-drafted feedback to a real person, a human must verify the Situation and Behavior descriptions are accurate — factual errors in feedback are far more damaging than no feedback.
- Agents will sometimes reverse SBI into IBS (lead with impact, then behavior, then situation) — enforce order explicitly in the prompt format.

## References
- Scott, K. (2017). Radical Candor. St. Martin's Press.
- Center for Creative Leadership — SBI Model: https://www.ccl.org/articles/leading-effectively-articles/give-effective-feedback-with-the-sbi-model/
- Harvard Business Review — The Feedback Fallacy: https://hbr.org/2019/03/the-feedback-fallacy
- 15Five API docs: https://apidocs.15five.com
