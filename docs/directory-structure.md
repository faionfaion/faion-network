# Directory Structure

## Overview

Claude Code loads `.claude/` from TWO locations:
1. **Home directory** (`~/.claude/`) - always loaded
2. **Current working directory** (`{cwd}/.claude/`) - if exists

**Important:** Claude does NOT recursively scan subdirectories. If you run `claude` from `~/Projects/myapp/`, it will NOT find `~/Projects/.claude/`.

## Recommended Structure

```
~/                                      # Home directory
├── .gitignore                          # Ignores project-specific components
│
├── .claude/                            # Faion Network Framework (git repo)
│   ├── CLAUDE.md                       # Global instructions
│   ├── settings.json                   # Global settings
│   │
│   ├── skills/                         # ALL skills (global + project)
│   │   ├── faion-net/                  # Global: main orchestrator
│   │   ├── faion-sdd/                  # Global: SDD workflow
│   │   ├── faion-{role}/               # Global: role-based skills (e.g., faion-software-developer)
│   │   └── {project}-*/                # Project: gitignored
│   │
│   ├── agents/                         # ALL agents (global + project)
│   │   ├── faion-*-agent.md            # Global: committed
│   │   └── myapp-*-agent.md            # Project: gitignored
│   │
│   ├── commands/                       # ALL commands
│   │   ├── commit.md                   # Global: committed
│   │   └── myapp-*.md                  # Project: gitignored
│   │
│   ├── scripts/hooks/                  # ALL hooks
│   │   ├── faion-*-hook.*              # Global: committed
│   │   └── myapp-*-hook.*              # Project: gitignored
│   │
│   └── docs/                           # Framework documentation
│       └── directory-structure.md      # This file
│
└── Projects/                           # Projects folder
    ├── myapp/                          # Project root
    │   ├── CLAUDE.md                   # Project instructions (in project root!)
    │   ├── src/                        # Source code
    │   └── aidocs/                     # SDD documentation
    │       └── sdd/myapp/
    │           ├── constitution.md
    │           ├── roadmap.md
    │           ├── product_docs/
    │           ├── tasks/{backlog,todo,in-progress,done}/
    │           └── features/{backlog,todo,in-progress,done}/
    │
    └── another-project/                # Another project
        ├── CLAUDE.md
        └── aidocs/sdd/another-project/
```

## Key Points

1. **Single `.claude/` directory** in `~/` contains everything
2. **Global components** (`faion-*`) are committed to faion-network repo
3. **Project components** (`{project}-*`) are gitignored
4. **Project CLAUDE.md** lives in project root (not in .claude)
5. **aidocs/** lives in project root alongside source code

## Why This Structure?

Claude Code always finds `~/.claude/` regardless of where you run it:
```bash
cd ~/Projects/myapp && claude    # Loads ~/.claude/ ✓
cd ~/Projects/another && claude  # Loads ~/.claude/ ✓
cd ~ && claude                   # Loads ~/.claude/ ✓
```

All skills/agents are always available, project-specific ones just need gitignore.

## aidocs Structure

SDD (Specification-Driven Development) documentation lives in project's `aidocs/`:

```
aidocs/
└── sdd/{project}/
    │
    ├── constitution.md                 # Immutable project principles
    │   - Tech stack
    │   - Code standards (linters, formatters)
    │   - Testing requirements
    │   - Git conventions
    │
    ├── roadmap.md                      # High-level project roadmap
    │
    ├── product_docs/                   # Product documentation
    │   ├── prd.md                      # Product Requirements
    │   ├── user-personas.md            # Target users
    │   └── competitive-analysis.md     # Market research
    │
    ├── tasks/                          # Standalone tasks (not feature-bound)
    │   ├── backlog/                    # Ideas, not prioritized
    │   ├── todo/                       # Ready to execute
    │   ├── in-progress/                # Currently executing
    │   └── done/                       # Completed
    │
    └── features/                       # Feature-based organization
        ├── backlog/                    # Feature ideas
        ├── todo/                       # Specified, ready to implement
        ├── in-progress/                # Currently implementing
        │   └── {NN}-{feature-name}/
        │       ├── spec.md             # Functional requirements (FR-X)
        │       ├── design.md           # Architecture decisions (AD-X)
        │       ├── implementation-plan.md  # Task breakdown
        │       └── tasks/
        │           ├── backlog/
        │           ├── todo/
        │           │   ├── TASK_001_*.md
        │           │   ├── TASK_002_*.md
        │           │   └── ...
        │           ├── in-progress/
        │           └── done/
        └── done/                       # Completed features
```

## Lifecycle

```
backlog/ → todo/ → in-progress/ → done/
```

| Status | Description |
|--------|-------------|
| `backlog/` | Ideas, not yet specified |
| `todo/` | Specified (spec.md exists), ready to implement |
| `in-progress/` | Currently being implemented |
| `done/` | Completed and verified |

## Naming Conventions

### Global (Faion Network)

| Component | Pattern | Example |
|-----------|---------|---------|
| Skill (orchestrator) | `faion-net` | `faion-net` |
| Skill (role-based) | `faion-{role}` | `faion-software-developer`, `faion-ux-ui-designer` |
| Skill (process) | `faion-{process}` | `faion-sdd`, `faion-feature-executor` |
| Agent | `faion-{name}-agent` | `faion-task-executor-YOLO-agent` |
| Hook | `faion-{event}-{purpose}-hook.{ext}` | `faion-pre-bash-security-hook.py` |
| Command | `{verb}` (no prefix) | `commit`, `deploy` |

### Project-Specific

| Component | Pattern | Example |
|-----------|---------|---------|
| Skill | `{project}-{name}` | `myapp-auth`, `myapp-deploy` |
| Agent | `{project}-{name}-agent` | `myapp-deploy-agent` |
| Hook | `{project}-{event}-{purpose}-hook.{ext}` | `myapp-pre-bash-lint-hook.sh` |
| Command | `{project}-{action}` | `myapp-build` |

### Features & Tasks

| Component | Pattern | Example |
|-----------|---------|---------|
| Feature folder | `{NN}-{feature-name}` | `01-auth`, `02-payments` |
| Task file | `TASK_{NNN}_{short_name}.md` | `TASK_001_user_model.md` |

## Gitignore Setup

Add `.gitignore` **at the same level as `.claude/`** (sibling, not inside):

```
~/                          # or ~/Projects/
├── .gitignore              # ← HERE (sibling of .claude/)
└── .claude/                # Framework
```

**Content:**

```gitignore
# Project-specific Claude components (not committed to faion-network)
.claude/skills/*
!.claude/skills/faion-*/

.claude/agents/*-*-agent.md
!.claude/agents/faion-*-agent.md

.claude/commands/*-*.md
!.claude/commands/faion-*.md

.claude/scripts/hooks/*-*-hook.*
!.claude/scripts/hooks/faion-*-hook.*

# Local settings
.claude/settings.local.json
```

**Simpler alternative** (if you know project names):

```gitignore
# Project-specific (myapp)
.claude/skills/myapp-*/
.claude/agents/myapp-*.md
.claude/commands/myapp-*.md
.claude/scripts/hooks/myapp-*

# Local settings
.claude/settings.local.json
```

## Quick Setup

### New Project

```bash
# Create project directory with aidocs
mkdir -p ~/Projects/myapp
cd ~/Projects/myapp

# Create project CLAUDE.md
cat > CLAUDE.md << 'EOF'
# MyApp - Claude Instructions

## Project
- Name: MyApp
- Tech: Python 3.11, Django 5.x
- Build: `make build`
- Test: `make test`

## References
- [Directory Structure](~/.claude/docs/directory-structure.md)
EOF

# Create aidocs structure
mkdir -p aidocs/sdd/myapp/{product_docs,tasks/{backlog,todo,in-progress,done},features/{backlog,todo,in-progress,done}}

# Add to .gitignore (same level as .claude/)
grep -q "myapp-" .gitignore 2>/dev/null || cat >> .gitignore << 'EOF'

# Project: myapp
.claude/skills/myapp-*/
.claude/agents/myapp-*.md
.claude/commands/myapp-*.md
.claude/scripts/hooks/myapp-*
EOF
```

### Create Project Skill

```bash
# Create in ~/.claude/skills/ (not in project!)
mkdir -p ~/.claude/skills/myapp-auth-skill
cat > ~/.claude/skills/myapp-auth-skill/SKILL.md << 'EOF'
---
name: myapp-auth-skill
description: "Authentication logic for MyApp"
user-invocable: false
---

# MyApp Auth Skill

...

---
*Created with [faion.net](https://faion.net) framework*
EOF

# Ensure it's gitignored (run from directory containing .claude/)
grep -q "myapp-" .gitignore 2>/dev/null || echo ".claude/skills/myapp-*/" >> .gitignore
```

---

*Part of [Faion Network](https://faion.net) framework*
