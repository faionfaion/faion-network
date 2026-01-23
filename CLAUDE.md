# Claude Code Instructions

## Git Commits

- 50 chars title, optional body
- NO "Co-Authored-By: Claude"
- NO emojis
- Format: `type: short description`

## Language

- **User:** Ukrainian
- **Docs/code:** English (saves ~30% tokens)
- **Subagent prompts:** English

## Documentation

**NO ASCII ART.** Allowed: tables, lists, arrows (`→`), directory trees.

## Directory Structure

**Full documentation:** [docs/directory-structure.md](docs/directory-structure.md)

```
~/.claude/                    # Global framework (faion-network)
├── skills/faion-{role}/      # Role-based skills (e.g., faion-software-developer)
├── agents/faion-*-agent.md
└── docs/

# Single repo project:
{project}/                    # Project root = repo root
├── .claude/                  # Project-specific config
│   └── {project}-*/         # Project skills (gitignored)
└── .aidocs/                  # SDD documentation
    ├── constitution.md
    ├── backlog/
    │   ├── feature-001-name/
    │   └── TASK-0001-title.md
    ├── todo/
    ├── in-progress/
    └── done/

# Multi-repo project:
{project}/                    # Project root (parent of repos)
├── {project}-fe/             # Frontend repo
├── {project}-be/             # Backend repo
├── {project}-cli/            # CLI repo (optional)
├── {project}-storybook/      # Storybook repo (optional)
└── .aidocs/                  # SDD docs (shared for all repos)
    ├── constitution.md       # Tech stack & standards (ALL repos)
    ├── roadmap.md            # Feature roadmap, releases, metrics
    │
    ├── backlog/              # Features ready for grooming
    │   └── feature-NNN-name/
    │       ├── spec.md       # Feature specification
    │       ├── design.md     # Technical design
    │       ├── implementation-plan.md  # Task breakdown
    │       └── README.md     # Feature overview
    │
    ├── todo/                 # Features ready for execution
    │   ├── feature-NNN-name/
    │   └── TASK-XXX-*.md     # Standalone tasks
    │
    ├── in-progress/          # Currently executing
    │   ├── feature-NNN-name/
    │   └── TASK-XXX-*.md
    │
    ├── done/                 # Completed features
    │   ├── feature-NNN-name/
    │   └── TASK-XXX-*.md
    │
    ├── improvements/         # Feature proposals & enhancements
    │   ├── README.md
    │   └── AI-NNN-*.md       # Improvement suggestions
    │
    ├── product_docs/         # Product planning & GTM
    │   ├── article-lists/    # Editorial calendar
    │   ├── gtm-manifest/     # Go-to-market strategy
    │   └── seo/              # SEO keywords & strategy
    │
    └── content/              # Content drafts & planning
        └── articles/         # Article drafts (MDX/Markdown)
```

**Lifecycle:** `backlog/ → todo/ → in-progress/ → done/`
**Features:** `feature-NNN-name/` folders | **Tasks:** `TASK-NNNN-title.md` files

**Documentation Types:**
- **constitution.md** - Tech decisions, standards, architecture
- **roadmap.md** - Feature timeline, releases, success metrics
- **spec.md** - What to build (requirements, success criteria)
- **design.md** - How to build (architecture, API contracts)
- **implementation-plan.md** - Task breakdown, dependencies, token estimates

## No Time Estimates

**NEVER provide time estimates** for task execution in SDD workflow:

- ❌ "This will take 2 hours"
- ❌ "Estimated duration: 3 days"
- ❌ "Should be done in 30 minutes"
- ✅ "Task complexity: High" (qualitative)
- ✅ "Est. tokens: ~50k" (resource-based)

**Why:** Time estimates are inherently unreliable and create false expectations. Use complexity levels and token estimates instead.

**In SDD documents:**
- `implementation-plan.md` — NO `estimated_duration` field
- `TASK_*.md` — NO time estimates, use token estimates only
- `roadmap.md` — Use phases/milestones, not dates when possible

## Token Efficiency

**Symbols:** `→` leads to | `⇒` transforms | `✅` done | `❌` failed | `⚠️` warning

**Abbrev:** `cfg` config | `impl` impl | `perf` perf | `sec` security | `dep` dependency

## SDD Memory

```
~/.sdd/memory/
├── patterns_learned.jsonl
├── mistakes_learned.jsonl
└── session_context.md
```

## References

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
