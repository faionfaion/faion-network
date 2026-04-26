# Agent Integration — AI Design Assistant Patterns

## When to use
- Defining how an AI assistant should surface inside a design tool (sidebar, modal, inline) for a product feature
- Auditing an existing AI assistant UX for interaction pattern anti-patterns
- Generating design specifications for contextual, generative, or review-type AI assistants
- Selecting which assistant pattern (sidebar / modal / inline) fits a given task complexity

## When NOT to use
- When the AI capability itself is undefined — choose the capability first, then the interaction pattern
- Fully automated pipelines where no human interaction is expected during the AI task
- Mobile-first interfaces with minimal screen real estate where persistent sidebar degrades UX
- When the task is purely mechanical and needs no conversational affordance (batch export, resize)

## Where it fails / limitations
- Sidebar assistant pattern causes context switch fatigue on small screens or narrow viewports
- Modal assistant breaks flow when users need to reference canvas content during generation — use inline instead
- Inline suggestions are intrusive if triggered too eagerly; over-suggesting reduces trust in AI output
- Documentation/auto-spec assistants produce verbose output that developers reject without summary layer
- No widely adopted interaction standard for AI assistants in design tools — each tool invents its own pattern

## Agentic workflow
Claude agents can generate interaction pattern specifications for a new AI assistant feature: given a description of the AI capability and user task, the agent selects the appropriate pattern (sidebar / modal / inline), produces a component spec with trigger conditions, response formats, and fallback states, and flags human-in-loop checkpoints. The agent cannot test the pattern in a live design tool; a human must validate the spec in a prototype before shipping.

### Recommended subagents
- `haiku` — pattern selection heuristics, checklist generation, component naming
- `sonnet` — full interaction spec with trigger logic, error states, copy guidelines, human-in-loop map

### Prompt pattern
```
You are specifying an AI assistant interaction pattern for a [tool type: design tool / IDE / CMS].
AI capability: [e.g., "suggests component variants based on selected element"].
User task context: [e.g., "mid-flow, canvas active, user has selected a card component"].
Select the best pattern from: sidebar / modal / inline.
Output: (1) pattern choice with rationale, (2) trigger condition, (3) response format spec, (4) 3 error/fallback states.
```

```
Review this AI assistant spec for anti-patterns: [paste spec].
Check for: (1) missing fallback when AI returns no result, (2) over-eager trigger conditions,
(3) missing human confirmation step for destructive actions, (4) copy that implies AI certainty.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `storybook` | Document and preview assistant pattern components in isolation | npx storybook@latest init |
| `figma-rest-api` | Read current selection context for sidebar assistant prototypes | https://www.figma.com/developers/api |
| `axe-cli` | Audit assistant panel for accessibility (focus trapping in modals) | npm i -g axe-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma AI (native) | SaaS | No API | Best reference for contextual sidebar pattern (in-product) |
| GitHub Copilot Chat | SaaS | No | Inline pattern reference for IDE context; non-designable |
| Notion AI | SaaS | No | Inline and modal pattern reference; slash-command trigger model |
| Intercom Fin | SaaS | Partial | Conversational modal assistant; REST API for content, not UX |
| Vercel v0 | SaaS | Yes (API) | Modal pattern example (prompt → generated output); REST API |

## Templates & scripts
AI assistant pattern decision matrix — agent can populate and return this:

```markdown
| Criterion              | Sidebar | Modal | Inline |
|------------------------|---------|-------|--------|
| Task duration          | Long (>30s) | Medium (5–30s) | Short (<5s) |
| Canvas reference needed| Yes     | No    | No     |
| Disrupts current flow  | Low     | High  | Low    |
| Output type            | Multi-item | Single output | Single suggestion |
| Destructive action     | Never   | Always confirm | Never |
| Screen real estate     | Wide    | Any   | Narrow ok |
```

Pattern spec template (agent fills per feature):
```
Pattern: [sidebar | modal | inline]
Trigger: [event that opens assistant]
Context passed to AI: [list of design context fields]
Response format: [structured / freeform / list]
Max response wait: [Xms before skeleton/timeout state]
Fallback state: [what to show if AI returns empty / error]
Human confirmation: [required before / after AI action]
```

## Best practices
- Use sidebar for any AI task exceeding ~15 seconds or requiring iterative conversation
- Use modal for single-shot high-stakes generation (e.g., "generate entire screen from prompt") — modal signals intentionality
- Use inline for micro-suggestions triggered by selection (rename layer, suggest alt text) — must be dismissible with Escape
- Always show what context the AI received ("Based on your selected component: Button/Primary") — reduces distrust
- Never use AI-generated copy for error states without human review — AI errors inside AI assistants are especially damaging to trust
- Provide a "why did AI suggest this?" affordance for non-obvious suggestions

## AI-agent gotchas
- Agents specifying trigger conditions tend to over-trigger (every selection change) — enforce debounce and explicit user intent requirements in the spec
- LLM-generated copy for AI assistant UI ("Ask me anything!") sets unrealistic expectations; human copy review is mandatory
- Agents do not account for undo/redo semantics of AI actions in design tools — specify undo behavior explicitly
- Modal pattern specs from agents often omit focus trap and keyboard dismiss — flag as accessibility blocker

## References
- https://www.figma.com/blog/ai/ (Figma AI design blog)
- https://www.nngroup.com/articles/ai-design-tools/ (NNGroup human-AI collaboration)
- https://www.smashingmagazine.com/2025/01/ai-design-assistants/ (Design assistant UX principles)
- https://www.interaction-design.org/literature/article/ai-design-assistants (IDF reference)
- https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ (Modal accessibility pattern)
