# Agent Integration — Design Critique

## When to use
- Before handoff from design to development, as a final quality gate against defined design principles
- During each design sprint iteration when you need structured feedback on a single direction
- When async critique is needed for distributed teams — a written structured format prevents opinion debates in Slack threads
- When onboarding junior designers who need a framework for giving and receiving feedback
- When a design decision has been contested by stakeholders and you need an objective evaluation against goals

## When NOT to use
- When the problem definition is still open; critique assumes a design direction exists — use brainstorming or co-design workshops instead
- For pixel-level polish feedback on a concept still in wireframe stage; match feedback stage to design fidelity
- When the critique group lacks context on the user, the problem, or the constraints — missing context makes feedback opinion-based regardless of the framework
- As a replacement for user testing; critique surfaces expert opinions, not actual user behavior

## Where it fails / limitations
- Without stated goals and design principles, critique sessions default to preference debates regardless of format
- Power dynamics suppress critique quality: junior designers do not give honest feedback to senior designers in hierarchical teams without explicit facilitation
- Async critique loses the clarifying question phase; written comments often assume rather than ask
- Critique generates feedback, but does not prioritize it — without a severity/priority signal, a designer may over-weight cosmetic comments and under-weight structural ones
- "Design by committee" failure mode: when everyone in the room redesigns rather than analyzes

## Agentic workflow
An agent is effective as an async critique participant: given the design goals, user context, constraints, and design screenshots, it can apply structured observation-principle-impact-suggestion feedback for each screen. It functions as an always-available, non-hierarchical reviewer that never softens feedback for social reasons. A human facilitator must still run live critique sessions and make final decisions about which feedback to incorporate.

Agents can also pre-process a design before a team critique: generate a structured question list that surfaces ambiguities, identify where the design departs from the existing design system, and flag accessibility violations.

### Recommended subagents
- `faion-sdd-executor-agent` — produce a structured critique document from a design brief and screenshots, flag principle violations
- General Claude subagent with vision — analyze design screenshots against specified goals and principles, apply observation-principle-impact-suggestion format

### Prompt pattern
```
You are a UX design critic. Review the attached design for [feature name].

Context:
- Problem: [What user problem this solves]
- User: [Target user description]
- Design stage: [Exploration / Iteration / Polish]
- Constraints: [Technical, business, timeline]
- Design principles to evaluate against: [List 3-5 principles]

For each screen, provide structured feedback using:
- Observation: what you see
- Principle: which design principle is relevant
- Impact: how this affects the user
- Suggestion (optional): a specific alternative

Do not give preference-based feedback. All feedback must connect to a stated principle or goal.
```

```
Review this design for accessibility and design system compliance:
Design system: [link or description]
Screens: [attached]

Flag: (a) components that deviate from the design system, (b) color contrast violations, (c) text below 16px on body copy, (d) interactive elements without clear visual affordance.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-cli` | Automated accessibility critique for shipped or prototyped interfaces | `npm i -g @axe-core/cli` / github.com/dequelabs/axe-core-npm |
| `contrast-ratio` (CLI) | Check foreground/background color contrast | Various; e.g. `npm i -g get-contrast` |
| `stylelint` | CSS/design token lint — flags deviation from design system tokens | `npm i -g stylelint` / stylelint.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | Partial (REST API) | Design file access; API can read frames, components, styles for system compliance check |
| Loom | SaaS | No | Video-based async critique walkthroughs; no programmatic API |
| Notion | SaaS | Yes (REST API) | Async critique documentation; agent can write structured critique pages |
| Linear | SaaS | Yes (REST API) | Convert critique action items to design tickets |
| Zeplin | SaaS | Partial (REST API) | Design handoff with annotations; API for reading spec data |

## Templates & scripts
See `templates.md` for critique session template (context, goals, notes, action items, decisions) and feedback framework template (observation-principle-impact-suggestion).

Inline: generate a critique agenda from a design brief:
```python
def gen_critique_agenda(
    feature: str,
    stage: str,
    duration_min: int = 45,
    screens: list[str] = None,
) -> str:
    """Generate a time-boxed critique agenda."""
    if stage == "exploration":
        feedback_type = "Directional (Is this the right approach?)"
        time_per_screen = 5
    elif stage == "iteration":
        feedback_type = "Refinement (How can this be better?)"
        time_per_screen = 8
    else:  # polish
        feedback_type = "Polish (Is this ready to ship?)"
        time_per_screen = 10

    screen_list = "\n".join(f"  - {s}: {time_per_screen} min" for s in (screens or []))
    return f"""
# Critique Agenda: {feature}
Duration: {duration_min} min | Stage: {stage} | Feedback type: {feedback_type}

- Context (5 min)
- Present work (10 min)
- Clarifying questions (5 min)
- Structured feedback by screen:
{screen_list}
- Prioritize action items (5 min)
- Wrap up & assign owners (5 min)
""".strip()
```

## Best practices
- Presenter states the type of feedback needed at the start (directional / refinement / polish) — this single step prevents the most common failure mode (polish feedback on an exploration design)
- Facilitator time-boxes per-screen discussion to prevent a single contentious screen from consuming the session
- Note-taker captures verbatim feedback, not paraphrases — verbatim quotes survive the "telephone effect" when referenced later
- Decision authority stays with the presenter; after the session, they write back to participants which feedback they incorporated and why they skipped the rest
- For async critique, require participants to use the observation-principle-impact-suggestion format — freeform comment threads devolve into preference debates
- Separate "critique of the problem framing" from "critique of the solution" — sometimes the right feedback is that the wrong problem is being solved

## AI-agent gotchas
- Agents will generate preference-based feedback if the principles are not explicitly stated; always supply the design principles list in the prompt
- Vision model feedback on color and contrast requires specifying the WCAG level target; without it, agents apply inconsistent standards
- Agents do not know your design system unless you describe it or provide it — all "design system compliance" checks require the design system to be included in context
- Agent critique will be biased toward common web/app patterns; non-standard interaction models will receive conservative feedback even when the non-standard approach is the right one
- Do not treat agent critique output as a final deliverable; use it as input to a human-facilitated session or as a starting draft for async critique documents

## References
- Connor, A. & Irizarry, A. "Discussing Design." O'Reilly, 2015.
- Greever, T. "Articulating Design Decisions." O'Reilly, 2015.
- NNg design critiques: https://www.nngroup.com/articles/design-critiques/
- IDF how to run a design critique: https://www.interaction-design.org/literature/article/how-to-run-a-design-critique
- Basecamp Shape Up (critique process): https://basecamp.com/shapeup
