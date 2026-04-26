# Agent Integration — SDD Document Templates

## When to use
- Bootstrapping any SDD artifact from scratch — always start from the relevant template rather than freeform markdown
- Onboarding a new project: the Constitution template captures tech stack and standards before any feature work begins
- When a subagent needs to produce a spec, design, task, or implementation plan and must output consistent structure
- Generating backlog items, roadmap entries, or confidence-check reports as part of a planning session

## When NOT to use
- When an SDD artifact already exists and only needs incremental updates — editing in place is cheaper than re-templating
- For one-off notes or research spikes that will not feed into task execution

## Where it fails / limitations
- The Constitution template is underspecified for multi-repo projects — add a "Repos" table listing each repo, its language, and its deploy target
- The Roadmap template uses "Now / Next / Later" quarters; for long-lived projects this drifts — prefer milestone labels over calendar quarters
- Token Estimation Guide values are approximate and assume average file sizes; generated code (e.g., GraphQL schema, Prisma client) can be 5–10x larger

## Agentic workflow
Agents use templates as output schemas: provide the template as part of the system prompt and instruct the agent to fill each section. This constrains output structure and prevents agents from inventing non-standard sections. For implementation plans, the wave/checkpoint structure in the template ensures the executor agent can process tasks in dependency order without re-reading the entire plan.

The Pattern Record and Mistake Record templates are designed for agent self-logging: after each task, the executor agent appends a record to `patterns.md` or `mistakes.md` in `.aidocs/memory/`.

### Recommended subagents
- `faion-sdd-executor-agent` — consumes implementation-plan template output directly; writes execution reports matching the template structure
- General Claude subagent (Sonnet) — fills spec/design/task templates from requirements input
- General Claude subagent (Haiku) — fills implementation plan task summary tables (low-complexity structured output)

### Prompt pattern
```
Fill this implementation plan template for feature <name>.
Use the design.md AD decisions as the source for task definitions.
Apply the 100k token rule: no task context estimate may exceed 100k tokens.
Output only the filled template — do not add sections not in the template.
```

```
Using the Confidence Check template, evaluate readiness to proceed from spec to design.
Score each check against these docs: [constitution.md, spec.md].
Output verdict: Proceed | Clarify | Stop, with specific gaps listed.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cookiecutter` | Scaffold SDD directory structure from template | `pip install cookiecutter` |
| `mustache` / `mo` | Fill markdown templates with variable substitution | https://github.com/nicowillis/mo |
| `jq` | Validate and transform Pattern/Mistake Record JSON | system package |
| `markdownlint` | Enforce template structure across generated files | `npm i -g markdownlint-cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub (template repos) | SaaS | Yes (gh CLI) | `gh repo create --template` to clone SDD structure; issues for backlog items |
| Notion (database templates) | SaaS | Partial | Good for roadmap/backlog visibility; REST API for programmatic creation |
| Linear (templates) | SaaS | Yes (API) | Issue templates map to backlog item template; cycles = waves |
| Obsidian (templates plugin) | OSS | No API | Local knowledge base; good for constitution + patterns storage |

## Templates & scripts
This methodology contains the templates themselves. Key sub-templates:
- `template-spec/README.md` — specification template (WHAT/WHY)
- `template-design.md` — design document template (HOW) — see `design-doc-writing-process/`
- `template-task.md` — task file template (executor input)
- Implementation Plan template — inline in `templates/README.md`

Directory scaffolding script for a new feature:
```bash
#!/usr/bin/env bash
# new-feature.sh FEATURE_SLUG DOCS_DIR
SLUG=${1:?usage: new-feature.sh feature-slug .aidocs}
DIR=${2:-.aidocs}/backlog/$SLUG
mkdir -p "$DIR"/{todo,in-progress,done}
cat > "$DIR/spec.md" << 'EOF'
# Feature: {Feature Name}
**Version:** 1.0
**Status:** Draft
EOF
cat > "$DIR/implementation-plan.md" << 'EOF'
# Implementation Plan: {Feature Name}
**Status:** Draft
EOF
echo "Created $DIR"
```

## Best practices
- Always use the template as-is for the first version; resist the urge to add custom sections until the standard ones are proven insufficient
- The Confidence Check template should be run at four explicit gates: Pre-Spec, Pre-Design, Pre-Task, Pre-Implementation — skip none
- Token Estimation Guide in `templates/README.md` is a floor, not a ceiling; add 20% buffer for test files
- Pattern Record and Mistake Record JSON templates should be stored in `.aidocs/memory/` and indexed — agents that cannot find prior patterns repeat mistakes
- Constitution is the only template that does not change per-feature; maintain one per project and reference it from every spec

## AI-agent gotchas
- Agents filling templates often leave `{placeholder}` text in non-obvious fields (e.g., "**Project:** {project-name}") — run a grep for `{` in generated docs before committing
- The Implementation Plan template's Dependency Graph section is frequently left as freetext; agents do not auto-detect circular deps — validate manually
- Execution reports written by `faion-sdd-executor-agent` may not match the TASK_*.md template structure if the task file deviates — strict template adherence prevents this
- "Est. tokens" fields in implementation plan tables are often optimistic by 30–50% in practice; add a review pass that stress-tests estimates against actual file sizes

## References
- https://github.com/nicowillis/mo — bash mustache for template filling
- https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository — GitHub template repos
- https://keepachangelog.com — CHANGELOG format referenced in Constitution template
- https://adr.github.io — Architecture Decision Records standard
