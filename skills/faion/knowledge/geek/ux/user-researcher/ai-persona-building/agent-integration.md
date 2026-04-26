# Agent Integration — AI Persona Building

## When to use
- Lightweight persona creation needed quickly for a small team without a dedicated researcher
- Prototyping phase where placeholder personas unblock design decisions before real data arrives
- Supplementing a thin data set with AI-expanded behavioral hypotheses for rapid validation planning
- Updating a single persona field (e.g., adding digital behavior column) across an existing persona library
- Generating persona documentation from an already-agreed behavioral cluster description

## When NOT to use
- No real user data exists and the team plans to treat AI output as ground truth
- Regulated domains (healthcare, finance) where persona inaccuracy could cause harm downstream
- Personas will directly drive hiring, pricing, or go-to-market budget allocation without human review
- The methodology required is full AI-Assisted Persona Building with clustering — use `ai-assisted-persona-building` instead (richer pipeline)

## Where it fails / limitations
- This methodology (thinner than `ai-assisted-persona-building`) has minimal data preprocessing — AI output quality is directly coupled to prompt quality
- Without structured input, LLM defaults to demographic stereotypes rather than behavioral segments
- Persona documentation agent (Haiku) is purely formatting; it cannot catch factual errors introduced upstream
- No built-in validation step — a single-pass output is prone to plausible-sounding fabrication
- JTBD integration requires deliberate prompt engineering; default outputs produce goal lists, not true JTBD statements

## Agentic workflow
A single Claude subagent (Sonnet) receives a structured description of user type, available data points, and JTBD context, then produces a persona card in Markdown. A second Haiku subagent formats the card into the team's documentation template. Because this methodology lacks a clustering step, the agent pipeline is shorter but the human review checkpoint before publication is more critical.

### Recommended subagents
- General Claude subagent (Sonnet) — persona synthesis from description + data points
- General Claude subagent (Haiku) — documentation formatting and template population

### Prompt pattern
```
You are a UX researcher. Create a persona for the following user type:
- Product: [product name and core value prop]
- User segment: [one-sentence description]
- Known data points: [bullet list of facts from analytics/interviews]
- JTBD: When [situation], I want to [motivation], So I can [outcome]

Output a persona card with sections: Name/Role, Demographics, Goals, Pain Points,
Behavior Patterns, Trigger Events, Representative Quote.
Only use the provided data points. Mark any inferred fields as [INFERRED — needs validation].
```

```
You are a documentation assistant. Format the following persona content into this template:
[paste team template structure]
Do not add or change any content — only reformat.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jq` | Preprocess any JSON analytics data before prompt injection | `apt install jq` |
| `pandoc` | Convert persona Markdown cards to Confluence/Notion-compatible HTML | `apt install pandoc` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion | SaaS | Yes — API | Store output persona cards; agents can create pages via API |
| Airtable | SaaS | Yes — REST API | Persona registry for team-wide access and incremental updates |
| Dovetail | SaaS | Partial — export only | Source of interview tags to feed into prompt |
| Figma (FigJam) | SaaS | No direct API | Manual step: paste persona card into FigJam template |

## Templates & scripts
See `templates.md` for the full persona card template structure.

Minimal persona generation script (wraps Claude API call):
```python
import anthropic, json, sys

SYSTEM = (
    "You are a UX researcher. Create data-backed user personas. "
    "Only use provided data. Mark inferred fields as [INFERRED]."
)

def build_persona(user_type: str, data_points: list[str], jtbd: str) -> str:
    client = anthropic.Anthropic()
    prompt = (
        f"User type: {user_type}\n"
        f"Data points:\n" + "\n".join(f"- {d}" for d in data_points) + "\n"
        f"JTBD: {jtbd}\n\n"
        "Output a persona card (Name/Role, Demographics, Goals, Pain Points, "
        "Behavior Patterns, Triggers, Quote)."
    )
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
        system=SYSTEM,
    )
    return msg.content[0].text

if __name__ == "__main__":
    spec = json.loads(sys.stdin.read())
    print(build_persona(spec["user_type"], spec["data_points"], spec["jtbd"]))
```

## Best practices
- Always supply at least 3 concrete data points per persona — zero-data prompts produce archetype stereotypes
- Require the LLM to tag all inferred fields explicitly; teams often treat untagged output as validated fact
- Limit persona scope to one primary goal — multi-goal personas produce unfocused design decisions
- Store the prompt + input alongside the output so personas can be regenerated as data improves
- Run a manual smell-test: does this persona remind you of a real user you have spoken to? If not, it is probably a hallucination
- Use this lightweight method only for early exploration; graduate to `ai-assisted-persona-building` once real cluster data exists

## AI-agent gotchas
- Haiku formatting agent must receive explicit template structure; without it, it reformats inconsistently across runs
- LLMs conflate "persona" with "user story" — explicitly forbid story format in the prompt
- Sonnet will occasionally collapse two distinct segments into one if the input description is ambiguous — require the agent to state the cluster boundary assumptions explicitly
- Human review is the only validation gate in this thin pipeline — do not skip it even under time pressure
- If the agent is asked to update an existing persona (add a field), pass the full existing persona JSON; partial context causes the agent to rewrite rather than extend

## References
- Nielsen Norman Group: https://www.nngroup.com/articles/persona/
- Clayton Christensen, "Competing Against Luck" (JTBD)
- Anthropic Claude API docs: https://docs.anthropic.com/en/api/messages
