# Agent Integration — Workflow: Specification Phase

## When to use
- Starting a new feature where requirements are unclear or only partially defined
- Aligning stakeholder expectations before any design or coding begins
- Existing codebase needs a constitution — tech decisions are implicit and undocumented
- Backlog grooming session where features need prioritization and DoR verification
- Roadmap needs a reality check against current feature status

## When NOT to use
- Feature is a bugfix with a single clear root cause — skip spec, go straight to task
- Requirements are fully documented elsewhere (existing PRD, user research report) — extract, don't re-elicit
- Constitution already exists and team agrees on it — skip Mode 1 discovery
- Rapid prototype/spike where requirements will change after seeing the output

## Where it fails / limitations
- Socratic dialogue requires human availability; automated pipelines cannot substitute
- Five Whys loops can spiral without a human to recognize when the real need is found
- AskUserQuestion is a synchronous checkpoint — multi-agent pipelines must pause here
- Backlog grooming phase depends on accurate feature status; stale `.aidocs/` breaks analysis
- Roadmap confidence levels (90/70/50%) are subjective — agents tend to over-estimate confidence

## Agentic workflow
A spec-phase orchestrator opens by reading existing context (`constitution.md`, completed features, related specs). It delegates Socratic dialogue to the main Claude session (not a subagent) because requirements elicitation requires real-time human response. Once requirements are captured, a Sonnet subagent drafts each spec section sequentially (problem → user stories → FR → NFR → AC → scope), showing each to the user before proceeding. A reviewer subagent (`faion-sdd-reviewer-agent mode: spec`) checks SMART compliance and traceability before the spec is saved and marked approved.

### Recommended subagents
- `faion-sdd-reviewer-agent (mode: spec)` — SMART criteria check, INVEST compliance, FR→US traceability
- `faion-sdd-executor-agent` — downstream; validates that spec is executable by attempting task estimation

### Prompt pattern
```
You are facilitating a specification session for feature {feature_name}.
Context: read constitution.md and features/done/ for established patterns.
Use Socratic dialogue: start with "Tell me about the problem. Who suffers and how?"
Apply Five Whys. Present A/B alternatives for each major decision.
Do NOT write the spec yet. Collect requirements only.
Stop and ask before each new section.
```

```
MODE: spec
Draft spec.md for feature {feature} using collected requirements: {requirements_summary}
Structure: problem statement → personas → user stories → FR-X → NFR-X → AC (Given-When-Then) → out of scope
Show each section for approval before continuing.
Save to: .aidocs/features/backlog/{NN}-{feature}/spec.md
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ls .aidocs/features/` | Survey feature status across lifecycle stages | built-in |
| `grep -l "status: approved"` | Find approved specs ready for design phase | built-in |
| `find .aidocs -name "spec.md"` | List all spec files for backlog audit | built-in |
| `wc -l spec.md` | Sanity-check spec length (good specs: 100-300 lines) | built-in |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes | REST API to sync FR-X items as issues; supports custom fields |
| Jira | SaaS | Yes | Confluence API for publishing specs; Jira API for issue creation |
| Notion | SaaS | Partial | Database API works; markdown→Notion formatting is lossy |
| ProductBoard | SaaS | Partial | Feature portal API; good for capturing user need evidence |
| GitHub Discussions | SaaS | Yes | `gh api` for programmatic discussion creation; good for async spec review |

## Templates & scripts
See `templates.md` and `template-spec.md` for the full spec template.

Backlog status auditor:
```bash
#!/usr/bin/env bash
# Print feature status table across all lifecycle stages
DOCS_DIR=".aidocs/features"
echo "| Stage | Feature | Spec | Design | Plan |"
echo "|-------|---------|------|--------|------|"
for stage in backlog todo in-progress done; do
  dir="$DOCS_DIR/$stage"
  [ -d "$dir" ] || continue
  for feature in "$dir"/*/; do
    name=$(basename "$feature")
    spec=$( [ -f "$feature/spec.md" ] && echo "yes" || echo "no" )
    design=$( [ -f "$feature/design.md" ] && echo "yes" || echo "no" )
    plan=$( [ -f "$feature/implementation-plan.md" ] && echo "yes" || echo "no" )
    echo "| $stage | $name | $spec | $design | $plan |"
  done
done
```

## Best practices
- Start every spec session with the problem statement, never the solution — ask "what pain?" before "what feature?"
- Always define at least two user personas; single-persona specs miss edge cases that surface during testing
- Write "Out of Scope" before closing the session — stakeholders add scope naturally; capture what's excluded while it's fresh
- Roadmap confidence levels must be explicit: "Now (90%)" items have tasks; "Later (50%)" items have only a problem statement
- Constitution Mode 1 (existing project): let codebase analysis lead, then validate with the team — do not write standards from memory
- Every FR must trace to at least one user story; orphaned FRs indicate gold-plating
- Backlog grooming output is a prioritized, DoR-verified list — not just a list of ideas

## AI-agent gotchas
- Agents interpret "Socratic dialogue" as asking one question then proceeding — enforce single-question pauses explicitly
- Five Whys loops need a termination condition; without one, agents hallucinate answers when humans stop responding
- Roadmap "Later" items must not get detailed specs prematurely — agents tend to over-specify because spec writing is their strength
- SMART requirement validation (Specific, Measurable, Achievable, Relevant, Time-bound) requires domain knowledge; Haiku fails on "Achievable" assessment
- Constitution anti-pattern: agents copy patterns from existing code without checking if those patterns are intentional standards or technical debt
- "I don't know" from users is valid input; agents must document uncertainty rather than interpolate an answer

## References
- [Requirements Engineering Fundamentals — IREB](https://www.ireb.org/en/cpre/fundamentals/)
- [User Story Mapping — Jeff Patton](https://www.jpattonassociates.com/user-story-mapping/)
- [Specification by Example — Gojko Adzic](https://gojko.net/books/specification-by-example/)
- [SMART Goals Framework](https://en.wikipedia.org/wiki/SMART_criteria)
- [MoSCoW prioritization method](https://www.productplan.com/glossary/moscow-prioritization/)
