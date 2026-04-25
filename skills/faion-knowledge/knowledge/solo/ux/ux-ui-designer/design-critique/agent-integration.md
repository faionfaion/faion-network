# Agent Integration — Design Critique

## When to use
- Pre-session preparation: agent generates a structured critique brief from design goals, constraints, and design stage
- Async critique: agent reviews a design description (or Figma JSON/screenshot) against stated goals and produces structured feedback in the Observation → Principle → Impact → Suggestion format
- Post-session synthesis: agent organizes raw critique notes into prioritized action items and a decisions log
- Solo critique: designer uses agent as a structured sounding board when no human reviewers are available
- Training junior designers: agent models the feedback format, then humans refine it

## When NOT to use
- As a replacement for human critique sessions — design critique is partly a social process that builds alignment and shared design language; agent feedback skips that function
- When the design goals are undefined — agent critique without stated objectives degrades to preference-based feedback (exactly the problem critique is meant to solve)
- For final production-ready polish decisions — agent cannot assess micro-interaction feel, animation timing, or cross-device rendering
- When stakeholder buy-in is the primary goal — human-led critique creates co-ownership that agent feedback cannot

## Where it fails / limitations
- Agent cannot view Figma, Sketch, or image files natively without vision input; structured text descriptions or exported element lists are required
- Agent critique defaults to generic UX principles when product-specific context (user research, brand constraints, technical limits) is absent
- Feedback on "what's working well" is weak from agent — it tends to spend tokens on issues, not strengths
- Agent cannot replicate the back-and-forth clarification dynamic of a real critique ("What did you mean by X?"); it must work with what is provided
- Agent feedback may contradict organizational design system rules it is unaware of

## Agentic workflow
A Claude subagent receives: (1) a design brief (problem, user, constraints, stage), (2) design goals with success criteria, and (3) a description of the design (screen-by-screen walkthrough, element list, or annotated screenshot text). It outputs structured critique in the standardized format (Observation → Principle/Goal → Impact → Optional suggestion), organized by severity: Major concerns first, then Minor, then Positive observations. A second optional pass compresses the critique into a prioritized action item table for the presenter.

### Recommended subagents
- `faion-sdd-executor-agent` — manage critique sessions as structured SDD tasks with input/output artifacts
- General Claude subagent with reviewer role — generate the critique document from design description

### Prompt pattern
```
You are a UX design critic. Do not give preference-based feedback.
All feedback must follow: Observation → Principle or Goal → Impact → (Optional suggestion).

Design context:
- Problem: [what user problem is being solved]
- User: [who this is for]
- Constraints: [technical, business, timeline]
- Stage: [Exploration / Iteration / Polish]
- Design goals: [list with measurable success criteria]
- Feedback requested: [Directional / Refinement / Polish]

Design description:
[screen-by-screen or element-level description]

Output:
1. Major concerns (affect primary goals) — max 5
2. Minor concerns (affect secondary goals) — max 5
3. What is working well — at least 2 observations
4. Questions for the designer (for clarification, not judgment)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Figma REST API | Export frame/component tree as JSON for structured agent input | https://www.figma.com/developers/api (read-only token) |
| jq | Parse Figma JSON exports to extract element names, types, and hierarchy | `apt install jq` / https://jqlang.github.io/jq/ |
| Loom CLI (unofficial) | Share screen recordings of prototype walkthroughs for async critique | No official CLI; use web interface |
| Playwright | Screenshot specific flows in a live prototype for structured agent review | `npm install -D playwright` / https://playwright.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | Partial (REST, read-only) | Export frame structure; agent reads element tree, not rendered visuals without vision |
| Loom | SaaS | No | Async video critique; useful for human reviewers, not agent |
| Notion | SaaS | Yes (API) | Store critique sessions, action items, and decisions; agent writes structured output via API |
| Linear | SaaS | Yes (API) | Convert critique action items directly to design tickets |
| GitHub Discussions | OSS/SaaS | Yes (API) | Async critique threads for design work stored in repos; agent can post/parse via GitHub API |

## Templates & scripts
See `templates.md` for the Critique Session and Feedback Framework templates. Below is a Figma API script to extract a frame's element names for agent input:

```bash
#!/usr/bin/env bash
# figma-elements.sh — extract element names from a Figma file frame
# Requires: curl, jq
# Usage: bash figma-elements.sh <file-key> <node-id>
FIGMA_TOKEN="${FIGMA_TOKEN:?Set FIGMA_TOKEN env var}"
FILE_KEY="${1:?Usage: $0 <file-key> <node-id>}"
NODE_ID="${2:?}"

curl -s \
  -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/${FILE_KEY}/nodes?ids=${NODE_ID}" \
  | jq '
    [.nodes[].document
     | .. | objects
     | select(.type != null and .name != null)
     | {name: .name, type: .type, visible: (.visible // true)}]
    | unique_by(.name)
    | sort_by(.type)
  '
```

## Best practices
- Always include the design stage in the critique request — agent feedback calibrated for "Exploration" looks different from "Polish"
- Provide stated design goals with measurable success criteria; without them, agent critique defaults to generic heuristics
- Require the agent to limit feedback to 5 major concerns maximum — longer lists dilute priority and overwhelm the designer
- Run the Observation → Principle → Impact chain strictly; reject agent outputs that skip the principle/goal link
- Use agent critique output as a starting point for human review, not as the final critique record
- For solo work, ask agent to steelman the current design before critiquing — this surfaces the designer's own rationale explicitly

## AI-agent gotchas
- Agent will critique what it is told, not what is visually rendered — descriptions that omit interactive states, error states, or empty states will receive incomplete feedback
- Human-in-loop checkpoint: agent action items must be reviewed by a human designer before implementation; agent does not have authority to dictate design changes
- Agent feedback on "what's working" is often generic ("the layout is clear") — push back and require specific observations tied to goals
- Without explicit constraints provided, agent may suggest alternatives that are technically infeasible or contradict the design system
- Agent may critique design decisions that were already deliberate trade-offs; provide a list of "decisions already made, not open for discussion" to prevent churn

## References
- Adam Connor & Aaron Irizarry, *Discussing Design* (O'Reilly)
- Tom Greever, *Articulating Design Decisions* (O'Reilly, 2nd ed.)
- https://www.nngroup.com/articles/design-critiques/
- https://www.interaction-design.org/literature/article/how-to-run-a-design-critique
- https://basecamp.com/shapeup (Shape Up, for async critique patterns)
