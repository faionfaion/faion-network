# Agent Integration — Workflow: Design Phase

## When to use
- Approved `spec.md` exists and the feature needs a technical blueprint before coding starts
- Choosing between 2+ architecture options with real trade-offs (not obvious defaults)
- Codebase has existing patterns that new work must follow — design phase surfaces them
- Feature spans multiple services or data models requiring explicit data flow definition

## When NOT to use
- Spec is still in draft or unapproved — design decisions will be based on shifting requirements
- Tiny bugfixes or single-file changes where a full design doc adds zero value
- Pure infrastructure changes (server config, CI tweaks) that don't affect application architecture
- Greenfield spikes where the goal is learning, not committing to an approach

## Where it fails / limitations
- Architecture decisions made without running existing code can contradict hidden constraints
- Phase 9 (user review) is a synchronous human checkpoint — async agent pipelines stall here
- Codebase research via Grep/Glob misses runtime behavior (dynamic imports, factory patterns)
- Wave analysis speedup estimates are theoretical; I/O-bound tasks rarely parallelize as predicted
- The reviewer agent checks structure but cannot validate that AD choices are technically correct

## Agentic workflow
A planning orchestrator reads `spec.md` and `constitution.md`, then spawns a Sonnet subagent to research the codebase for existing patterns. An Opus subagent receives the research output and generates architecture decisions (AD-X entries) with explicit alternatives and rationale. The Sonnet agent then composes the full `design.md`, including component breakdown, data flow, file change list, and testing strategy. A final reviewer pass via `faion-sdd-reviewer-agent (mode: design)` checks FR coverage and AD structure before the document is saved.

### Recommended subagents
- `faion-sdd-executor-agent` — downstream consumer of design output; use to validate that design tasks are executable
- `faion-sdd-reviewer-agent (mode: design)` — structural review: FR coverage, AD context/options/rationale, constitution compliance

### Prompt pattern
```
Read spec.md and constitution.md for feature {feature}.
Research codebase: find similar models, services, views matching the FR requirements.
Output: list of reusable patterns, naming conventions, placement decisions.
Do not make architecture decisions — only report findings.
```

```
Given research findings: {findings}
Given spec requirements: {fr_list}
Make architecture decisions for feature {feature}.
Each AD must have: context, min 2 options with pros/cons, decision, rationale.
Output: AD-001 through AD-N in structured markdown.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `grep -r "class.*Model"` | Find existing model patterns in codebase | built-in |
| `tree -L 3` | Visualize component placement before deciding file structure | `apt install tree` |
| `mermaid-cli` (`mmdc`) | Render data flow diagrams from markdown to PNG | `npm i -g @mermaid-js/mermaid-cli` |
| `ast-grep` | Structural code search (find patterns regardless of naming) | `cargo install ast-grep` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Structurizr | OSS/SaaS | Yes | C4 model diagrams via DSL; can be generated from design docs |
| PlantUML | OSS | Yes | Component and sequence diagrams from text; Docker image available |
| Eraser.io | SaaS | Partial | AI-generated diagrams but no batch API |
| Confluence | SaaS | Partial | REST API for publishing design docs; lossy markdown rendering |
| GitHub Wiki | SaaS | Yes | `gh api` to push markdown design docs directly |

## Templates & scripts
See `templates.md` and `template-design.md` for the canonical `design.md` structure.

Inline dependency detection script for implicit task dependencies:
```python
import re
from pathlib import Path

def find_shared_files(task_files: list[Path]) -> dict[str, list[str]]:
    """Find files touched by multiple tasks — these create implicit dependencies."""
    file_to_tasks: dict[str, list[str]] = {}
    pattern = re.compile(r"^\|\s*(CREATE|MODIFY|DELETE)\s*\|\s*`([^`]+)`", re.MULTILINE)
    for task_file in task_files:
        task_id = task_file.stem
        text = task_file.read_text()
        for _, file_path in pattern.findall(text):
            file_to_tasks.setdefault(file_path, []).append(task_id)
    return {f: tasks for f, tasks in file_to_tasks.items() if len(tasks) > 1}
```

## Best practices
- Run codebase research as a separate subagent call before making AD decisions — mixing discovery and decision-making in one pass produces worse decisions
- Write the Files table (CREATE/MODIFY) before writing task descriptions — files are the ground truth of scope
- For API features, reference `contracts.md` rather than redefining endpoints in design — prevents drift
- Each AD must document at least one rejected alternative; this is the most valuable part for future agents
- Mark the critical path in the implementation plan before wave analysis — it determines which tasks block everything else
- Keep design.md under 800 lines; split into sub-docs if larger (agents lose coherence on very long docs)
- After reviewer approval, freeze design.md — changes after task creation cause cascading inconsistencies

## AI-agent gotchas
- Opus is required for AD decisions; Sonnet will produce plausible-sounding but shallow trade-off analysis
- Codebase research via Glob/Grep only finds static patterns; ask agent to also check git log for recent changes
- The "review with user" phase (Phase 9) is a hard human-in-the-loop checkpoint — design pipelines must pause here; do not auto-approve
- Wave analysis speedup calculations assume zero inter-task coordination cost; real speedup is 30-50% of theoretical
- Agents frequently omit the "Consequences" subsection from ADRs — enforce via reviewer checklist
- File change lists become stale when design is revised post-approval; version the design doc or lock it
- Do not parallelize the research and AD-decision phases — AD quality depends on complete research input

## References
- [Architecture Decision Records — Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Software Architecture Patterns — O'Reilly](https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/)
- [The C4 Model for Software Architecture](https://c4model.com/)
- [Dependency analysis in agile — Wave planning](https://www.scaledagileframework.com/pi-planning/)
