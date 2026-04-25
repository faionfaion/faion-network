# Agent Integration — SDD Document Templates

## When to use
- Starting a new project: generate constitution.md and roadmap.md stubs before any code
- Adding a feature: scaffold spec.md → design.md → test-plan.md → implementation-plan.md in one agent pass
- When a human provides a rough feature description and wants a fully structured SDD folder immediately
- When bootstrapping a project that will be executed by `faion-sdd-executor-agent`

## When NOT to use
- Single-file bug fixes or one-liner patches (no SDD overhead needed)
- Vibe-coding / rapid throwaway prototypes where specs will be discarded
- When a feature already has complete SDD docs (check `.aidocs/` first before re-generating)
- When the constitution.md does not yet exist — create it first, templates depend on it for constraints

## Where it fails / limitations
- Templates are skeletons; agents must populate them with domain knowledge — blank placeholders block downstream agents
- Token budget table (100k rule) breaks down for tasks that require reading large existing codebases; the budget evaporates on context loading alone
- `task.md` stubs generated without reading the design.md produce mis-scoped tasks; order matters
- Feature folder naming collisions (`feature-024-starter-kits`) cause silent overwrites if an agent doesn't check first

## Agentic workflow
An agent reads the feature description, loads constitution.md for stack constraints, then generates the full document chain (spec → design → test-plan → implementation-plan → task stubs) in one pass. Each document is gated: the agent must validate completeness (FR-X numbering, AC present, AD-X decisions present) before creating the next. The final step populates task.md files and moves the feature folder to `.aidocs/todo/`.

### Recommended subagents
- `faion-sdd-executor-agent` — picks up the generated task files and executes them sequentially; relies on all templates being correctly populated before execution starts
- Haiku-tier subagent — mechanical form-fill for spec.md and task.md stubs from structured input
- Opus-tier subagent — architecture decisions in design.md, alternatives analysis, trade-off tables

### Prompt pattern
```
Read .aidocs/constitution.md and the feature brief below.
Generate the full SDD document chain for feature-NNN-<slug>:
1. spec.md (FR-X list, AC per FR)
2. design.md (AD-X decisions, file structure, API contracts)
3. test-plan.md (test cases per AC)
4. implementation-plan.md (task table, dependency order)
5. task stubs in todo/ (one TASK-NNN.md per task row)
Place all output in .aidocs/todo/feature-NNN-<slug>/.
Do not create files that already exist.
```

```
Validate this spec.md for completeness:
- Every FR-X has at least one AC
- AC statements are testable (pass/fail, not vague)
- No placeholder text remains
- References constitution.md constraints
List gaps, then fix them.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `markdownlint-cli2` | Lint generated template files for formatting errors | `npm i -g markdownlint-cli2` / [docs](https://github.com/DavidAnson/markdownlint-cli2) |
| `yq` | Parse and validate YAML frontmatter fields | `brew install yq` / [docs](https://mikefarah.gitbook.io/yq/) |
| `fd` | Find existing SDD folders before creating new ones | `brew install fd` / [docs](https://github.com/sharkdp/fd) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub / GitLab | SaaS | Yes | Templates live in repo; agents read via API or local clone |
| Notion | SaaS | Partial | API allows page creation; Markdown round-trip is lossy |
| Linear | SaaS | Yes | Linear MCP can push spec items as issues; no template rendering |
| Obsidian | OSS desktop | No | No headless API; templates only accessible via file system |

## Templates & scripts
See `templates.md` for the eight copy-paste templates (constitution, spec, design, test-plan, implementation-plan, task, roadmap, memory).

Scaffold script (creates full feature folder from template stubs):
```bash
#!/usr/bin/env bash
# Usage: ./scaffold-feature.sh 042 auth-refactor
set -euo pipefail
N=$1; SLUG=$2
DEST=".aidocs/todo/feature-${N}-${SLUG}"
mkdir -p "$DEST/todo" "$DEST/in-progress" "$DEST/done"
for doc in spec design test-plan implementation-plan; do
  cp "skills/faion-knowledge/knowledge/solo/sdd/sdd/templates/${doc}.md" "$DEST/${doc}.md"
done
echo "Created $DEST"
```

## Best practices
- Always generate spec.md before design.md; design decisions without requirements produce orphaned ADs
- Number FR-X and AD-X sequentially and never reuse numbers within a project (acts as immutable ID)
- Keep task.md files under 5k tokens; split large tasks rather than inflating a single file
- Add `updated: YYYY-MM-DD` to YAML frontmatter every time a document is modified by an agent
- Store templates in version control; never edit the skeleton in-place — copy then fill
- Delete empty placeholder sections rather than leaving them as `TBD` — LLMs treat `TBD` as real content

## AI-agent gotchas
- Agents skip the traceability check: always verify that each task.md references the implementation-plan row and design AD; without it, executor agents lose context
- LLMs generate plausible-looking AC that are actually untestable ("system is fast" vs "p95 < 200ms") — run a validation pass on generated specs before approving
- Token budget estimates in implementation-plan.md become stale after context is loaded; add 20k buffer for agents reading large codebases
- Agents writing multiple files in one turn may silently truncate later files when approaching context limits; generate documents in separate turns or verify file sizes
- Feature folder naming must be checked before creation — agents do not detect existing folders by default and will overwrite

## References
- [SDD Workflow Overview](../faion-sdd-planning/methodologies/sdd-workflow-overview.md)
- [Google Design Docs](https://www.industrialempathy.com/posts/design-docs-at-google/)
- [ADR GitHub](https://adr.github.io/)
- [Addy Osmani: LLM Coding Workflow](https://addyosmani.com/blog/ai-coding-workflow/)
