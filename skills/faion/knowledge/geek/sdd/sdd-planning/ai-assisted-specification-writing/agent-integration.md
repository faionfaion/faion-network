# Agent Integration — AI-Assisted Specification Writing (SDD Planning)

## When to use
- At the sdd-planning phase: translating a product concept or backlog item into a structured spec.md before the design phase starts
- When a feature ticket (e.g., Linear issue, Jira story) exists but the acceptance criteria are vague or missing
- For sprint planning: AI drafts specifications for upcoming sprint items so the team can review and approve them in advance
- When iterative refinement of a rough draft spec is needed — using an AI dialogue to progressively sharpen requirements
- For generating task breakdowns (implementation-plan.md) from an approved spec

## When NOT to use
- As a replacement for stakeholder discovery — AI cannot substitute for interviews, user research, or business requirements sessions
- When the spec is a regulatory artifact (e.g., FDA submission, GDPR DPA) — legal precision is beyond AI spec generation reliability
- For real-time collaborative specification during a meeting — the async AI drafting + human review loop is not suited for synchronous sessions
- When no product context is available — agent cannot invent a business model or market requirements

## Where it fails / limitations
- AI-generated specifications for novel product ideas (no analogous products) have a higher hallucination rate for requirements
- The Given-When-Then format produced by agents tends to describe happy-path scenarios by default — agents require explicit prompting to generate error path and boundary condition tests
- Agents cannot resolve ambiguous requirements without additional context; they default to the most common interpretation, which may not match intent
- Implementation plan task breakdown generated from spec frequently underestimates integration complexity between components
- 150-200 FR limit per single spec call is a practical limit for model consistency — beyond this, coherence degrades

## Agentic workflow
In the sdd-planning context, the agent operates at the planning layer: it reads the product intent or backlog item, generates a draft spec.md with FR list and acceptance criteria, then generates a draft implementation-plan.md with task breakdown and token estimates. The two-document output is staged for human review. After human approval, `faion-feature-executor` picks up the implementation-plan.md tasks and executes them sequentially. The planning agent should never proceed to creating implementation tasks without an explicit human approval signal on the spec.

### Recommended subagents
- `faion-sdd-execution` — validate spec quality against SDD patterns before human review
- `faion-feature-executor` — downstream executor of approved implementation plans generated from spec
- `faion-brainstorm` — for ambiguous or novel feature areas where requirements need diverge-converge cycles before spec drafting

### Prompt pattern
```xml
<task>Draft a spec.md and implementation-plan.md for this feature.</task>
<feature>{{feature_name}}</feature>
<intent>{{one_paragraph_description_of_what_it_should_do}}</intent>
<constraints>
  <technical>{{stack, existing APIs, DB schema constraints}}</technical>
  <business>{{scope limits, budget, regulatory}}</business>
  <out_of_scope>{{explicit exclusions}}</out_of_scope>
</constraints>
<output_format>
  1. spec.md: FR list (FR-1..N), edge cases, Given-When-Then ACs, dependencies, out-of-scope
  2. implementation-plan.md: phase breakdown, task list with token estimates, dependency order
  Note: no time estimates — token estimates only.
</output_format>
```

```xml
<task>Refine this draft specification based on review feedback.</task>
<current_spec>{{spec_content}}</current_spec>
<feedback>{{reviewer_comments}}</feedback>
<instructions>
  Update only the sections affected by feedback.
  Preserve all FRs not mentioned in feedback.
  Flag any feedback that contradicts existing requirements.
</instructions>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `markdownlint` | Validate spec.md and plan.md formatting | `npm i -g markdownlint-cli` / https://github.com/DavidAnson/markdownlint |
| `vale` | Prose style linting for spec language clarity | https://vale.sh/ |
| `git log --follow` | Track spec document revision history | system |
| `wc -l` | Quick check that spec stays within size limits | system |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes — REST API | Read issue descriptions as spec input; write generated tasks back as sub-issues |
| GitHub Issues | SaaS | Yes — REST API | Source for feature intent; agent can read issue body and generate spec |
| Notion | SaaS | Yes — API | Store and version spec.md documents; readable by agents via API |
| AWS Kiro | SaaS (IDE) | Partial — IDE plugin | Native spec→plan→execute flow; agent must operate inside IDE |
| Claude Code | OSS/local | Yes — native | Direct file write for spec.md and implementation-plan.md |

## Templates & scripts
See `templates.md` for spec.md and implementation-plan.md templates.

Linear issue → spec.md scaffold (requires LINEAR_API_KEY):
```bash
#!/bin/bash
# linear-to-spec.sh — scaffold spec.md from Linear issue
ISSUE_ID="${1:?Usage: $0 <ISSUE_ID>}"

ISSUE=$(curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"{ issue(id: \\\"$ISSUE_ID\\\") { title description priority labels { nodes { name } } } }\"}")

TITLE=$(echo "$ISSUE" | jq -r '.data.issue.title')
DESC=$(echo "$ISSUE" | jq -r '.data.issue.description')

cat <<EOF
# Spec: $TITLE

## Intent
$DESC

## Functional Requirements
- FR-1: [To be filled based on intent above]

## Out of Scope
- [To be determined]

## Acceptance Criteria
### FR-1
- Given ...
- When ...
- Then ...
EOF
```

## Best practices
- Separate the spec generation call from the implementation plan generation call — mixing both in one prompt degrades quality for both artifacts
- Include existing related specs as context (`Related specs: [link]`) so the agent can maintain consistent terminology and avoid duplicate requirements
- Explicitly prompt for error paths: "For each FR, also document what happens when the operation fails"
- Treat the first AI draft as a structured outline, not a finished spec — plan for at least one human refinement cycle
- Use token estimates (not time estimates) in implementation-plan.md tasks; this is enforced by the SDD methodology and the pre-commit hook
- Keep implementation-plan.md tasks small enough that each fits in a single agent session (~20-30k tokens execution budget per task)

## AI-agent gotchas
- Agents generating implementation plans from specs frequently create tasks without capturing their dependency order — tasks executed out of order will fail; always validate the dependency graph before execution
- When an agent refines a spec based on feedback, it may silently drop FRs that "seemed implied" by the feedback — always diff the before/after FR list after a refinement pass
- Planning agents tend to generate overly optimistic task granularity — a task described as "implement authentication" is not a single agent task; agents should flag tasks that are under-specified
- Agents cannot self-assess whether a spec is "good enough" for implementation to start — quality gates in `faion-sdd-execution` must be the formal acceptance signal, not the agent's own judgment
- Implementation plan token estimates generated by agents are approximations; actual token consumption varies by codebase complexity and context loading

## References
- https://kiro.dev/docs/specs/ — AWS Kiro spec-driven development
- https://addyosmani.com/blog/ai-coding-workflow/ — LLM Coding Workflow 2026 (Addy Osmani)
- https://githubnext.com/projects/copilot-workspace — GitHub Copilot Workspace spec workflow
- https://gojko.net/books/specification-by-example/ — Specification by Example
- https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1519437/full — LLM in Requirements Engineering (2025 systematic review)
