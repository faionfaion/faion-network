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
    │
    ├── myapp/                          # Single-repo project
    │   ├── CLAUDE.md                   # Project instructions
    │   ├── src/                        # Source code
    │   ├── .git/                       # Git repository
    │   └── .aidocs/                    # SDD documentation
    │       ├── constitution.md
    │       ├── roadmap.md
    │       ├── product_docs/
    │       ├── backlog/
    │       │   ├── feature-001-auth/
    │       │   └── TASK-0001-setup.md
    │       ├── todo/
    │       ├── in-progress/
    │       └── done/
    │
    └── bigapp/                         # Multi-repo project
        ├── CLAUDE.md                   # Project overview
        ├── bigapp-fe/                  # Frontend repo
        │   ├── .git/
        │   └── src/
        ├── bigapp-be/                  # Backend repo
        │   ├── .git/
        │   └── src/
        └── .aidocs/                    # Shared SDD docs for all repos
            ├── constitution.md         # Covers FE + BE
            ├── roadmap.md
            ├── product_docs/
            ├── backlog/
            │   ├── feature-001-auth/   # May touch FE + BE
            │   └── TASK-0001-api.md
            ├── todo/
            ├── in-progress/
            └── done/
```

## Key Points

1. **Single `.claude/` directory** in `~/` contains everything
2. **Global components** (`faion-*`) are committed to faion-network repo
3. **Project components** (`{project}-*`) are gitignored
4. **Project CLAUDE.md** lives in project root (not in .claude)
5. **.aidocs/ location:**
   - **Single repo:** Inside repo root (alongside src/)
   - **Multi-repo:** Parent level (alongside repo folders)

## Why This Structure?

Claude Code always finds `~/.claude/` regardless of where you run it:
```bash
cd ~/Projects/myapp && claude    # Loads ~/.claude/ ✓
cd ~/Projects/another && claude  # Loads ~/.claude/ ✓
cd ~ && claude                   # Loads ~/.claude/ ✓
```

All skills/agents are always available, project-specific ones just need gitignore.

## .aidocs/ Placement Rules

**Decision tree:**

```
Does the project have multiple repos?
├─ NO (single repo)
│  └─ Place .aidocs/ INSIDE repo root
│     Example: myapp/.aidocs/
│
└─ YES (multiple repos: FE, BE, mobile, etc.)
   └─ Place .aidocs/ at PARENT level (alongside repos)
      Example: myapp/.aidocs/ + myapp/myapp-fe/ + myapp/myapp-be/
<<<<<<< HEAD
=======
```

**Why?**
- **Single repo:** .aidocs/ is versioned with code, easier to clone
- **Multi-repo:** .aidocs/ is shared, avoids duplication, single source of truth

**Examples:**

| Project Structure | .aidocs/ Location | Reason |
|-------------------|-------------------|--------|
| `myapp/` (monorepo) | `myapp/.aidocs/` | Single repo |
| `bigapp/bigapp-fe/` + `bigapp/bigapp-be/` | `bigapp/.aidocs/` | Multi-repo, shared docs |
| `faion-net/` (Gatsby) | `faion-net/.aidocs/` | Single repo |
| `scanmecard/scanmecard-web/` + `scanmecard/scanmecard-api/` | `scanmecard/.aidocs/` | Multi-repo |

## .aidocs Structure

SDD (Specification-Driven Development) documentation lives in project's `.aidocs/`:

```
.aidocs/
├── constitution.md                 # Immutable project principles
│   - Tech stack (for ALL repos in multi-repo setup)
│   - Code standards (linters, formatters)
│   - Testing requirements
│   - Git conventions
│   - Multi-repo: describes FE, BE, and shared standards
│
├── roadmap.md                      # High-level project roadmap
│
├── product_docs/                   # Product documentation
│   ├── prd.md                      # Product Requirements
│   ├── user-personas.md            # Target users
│   └── competitive-analysis.md     # Market research
│
├── backlog/                        # Ideas, not prioritized
│   ├── feature-001-auth/           # Feature folder
│   │   ├── spec.md                 # Functional requirements (FR-X)
│   │   ├── design.md               # Architecture decisions (AD-X)
│   │   └── implementation-plan.md  # Task breakdown
│   └── TASK-0001-setup.md          # Standalone task file
│
├── todo/                           # Specified, ready to implement
│   ├── feature-002-payments/
│   └── TASK-0005-database.md
│
├── in-progress/                    # Currently executing
│   ├── feature-003-dashboard/
│   └── TASK-0010-api.md
│
└── done/                           # Completed
    ├── feature-000-init/
    └── TASK-0000-scaffold.md
>>>>>>> claude
```

**Why?**
- **Single repo:** .aidocs/ is versioned with code, easier to clone
- **Multi-repo:** .aidocs/ is shared, avoids duplication, single source of truth

**Examples:**

| Project Structure | .aidocs/ Location | Reason |
|-------------------|-------------------|--------|
| `myapp/` (monorepo) | `myapp/.aidocs/` | Single repo |
| `bigapp/bigapp-fe/` + `bigapp/bigapp-be/` | `bigapp/.aidocs/` | Multi-repo, shared docs |
| `faion-net/` (Gatsby) | `faion-net/.aidocs/` | Single repo |
| `scanmecard/scanmecard-web/` + `scanmecard/scanmecard-api/` | `scanmecard/.aidocs/` | Multi-repo |

## .aidocs Structure

SDD (Specification-Driven Development) documentation lives in project's `.aidocs/`:

```
.aidocs/
├── constitution.md                 # Immutable project principles
│   - Tech stack (for ALL repos in multi-repo setup)
│   - Code standards (linters, formatters)
│   - Testing requirements
│   - Git conventions
│   - Multi-repo: describes FE, BE, and shared standards
│
├── roadmap.md                      # High-level project roadmap
│   - Feature timeline and phases
│   - Release schedule
│   - Success metrics and goals
│   - Platform metrics
│
├── product_docs/                   # Product planning & GTM
│   ├── article-lists/              # Editorial calendar
│   │   - Content planning
│   │   - Publishing schedule
│   │
│   ├── gtm-manifest/               # Go-to-market strategy
│   │   - Launch strategy
│   │   - Marketing channels
│   │   - Distribution plan
│   │
│   ├── seo/                        # SEO keywords & strategy
│   │   - Keyword research
│   │   - Content optimization
│   │   - Search strategy
│   │
│   └── [other product docs]        # PRD, personas, competitive analysis
│
├── content/                        # Content drafts & planning
│   └── articles/                   # Article drafts (MDX/Markdown)
│       - Blog posts
│       - Tutorials
│       - Documentation
│
├── improvements/                   # Feature proposals & enhancements
│   ├── README.md                   # Improvement tracking overview
│   └── AI-NNN-*.md                 # Individual improvement suggestions
│
├── backlog/                        # Ideas, ready for grooming
│   ├── feature-NNN-name/           # Feature folder
│   │   ├── README.md               # Feature overview & context
│   │   ├── spec.md                 # What to build (requirements, success criteria)
│   │   ├── design.md               # How to build (architecture, API contracts)
│   │   └── implementation-plan.md  # Task breakdown, dependencies, token estimates
│   └── TASK-NNNN-title.md          # Standalone task file
│
├── todo/                           # Specified, ready to execute
│   ├── feature-NNN-name/           # Feature folder (all docs ready)
│   └── TASK-NNNN-title.md          # Ready task
│
├── in-progress/                    # Currently executing
│   ├── feature-NNN-name/           # Feature being implemented
│   └── TASK-NNNN-title.md          # Task in progress
│
└── done/                           # Completed and verified
    ├── feature-NNN-name/           # Completed feature (archive)
    └── TASK-NNNN-title.md          # Completed task
```

### Documentation Types

| Document | Purpose | Content |
|----------|---------|---------|
| **constitution.md** | Project foundation | Tech stack, architecture decisions (ADRs), coding standards, multi-repo setup |
| **roadmap.md** | Strategic planning | Feature timeline, release schedule, success metrics, platform KPIs |
| **spec.md** | Requirements | What to build, functional requirements (FR-X), success criteria, acceptance tests |
| **design.md** | Architecture | How to build, technical decisions (AD-X), API contracts, data models, diagrams |
| **implementation-plan.md** | Execution plan | Task breakdown with dependencies, complexity estimates, token budgets |
| **README.md** | Feature overview | Context, motivation, high-level summary (in feature folders) |

### Folder Purposes

| Folder | Purpose |
|--------|---------|
| **product_docs/** | Product strategy, GTM planning, content calendar, SEO strategy |
| **content/** | Article drafts, blog posts, tutorials (MDX/Markdown) |
| **improvements/** | Feature enhancement proposals, suggestions from AI analysis |
| **backlog/** | Features in grooming phase, not yet ready for implementation |
| **todo/** | Fully specified features, ready to execute (spec/design/plan complete) |
| **in-progress/** | Currently executing features/tasks |
| **done/** | Completed and verified features/tasks (archive) |

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

**Feature Movement:**
- Features (folders `feature-NNN-name/`) move with their tasks
- Tasks (`TASK-NNNN-title.md`) can move independently
- Both follow the same lifecycle path

## Real-World Example: faion-net

Multi-repository project with shared `.aidocs/` structure:

```
~/Projects/faion-net/
├── CLAUDE.md                       # Project overview
├── .aidocs/                        # Shared SDD docs (ALL repos)
│   ├── constitution.md             # Tech stack (Gatsby + Django + Go)
│   ├── roadmap.md                  # Feature roadmap & metrics
│   │
│   ├── product_docs/               # Product & GTM
│   │   ├── article-lists/          # Editorial calendar
│   │   ├── gtm-manifest/           # Marketing strategy
│   │   └── seo/                    # SEO keywords
│   │
│   ├── content/                    # Content planning
│   │   └── articles/               # Blog post drafts
│   │
│   ├── improvements/               # Feature proposals
│   │   ├── README.md
│   │   └── AI-001-*.md
│   │
│   ├── backlog/
│   │   └── feature-026-knowledge-infrastructure/
│   │       ├── README.md
│   │       ├── spec.md
│   │       ├── design.md
│   │       └── implementation-plan.md
│   │
│   ├── todo/
│   │   └── feature-024-starter-kits/
│   │       ├── spec.md
│   │       ├── design.md
│   │       ├── implementation-plan.md
│   │       └── TASK-SK-*.md        # 5 tasks
│   │
│   └── done/
│       └── feature-025-cli-tool/
│           ├── spec.md
│           ├── design.md
│           ├── implementation-plan.md
│           └── TASK-CLI-*.md       # 7 completed tasks
│
├── faion-net-fe/                   # Frontend repo (Gatsby 5)
│   ├── .git/
│   ├── CLAUDE.md                   # FE-specific instructions
│   ├── content/                    # 502 MDX methodologies
│   └── src/
│
├── faion-net-be/                   # Backend repo (Django 5)
│   ├── .git/
│   ├── CLAUDE.md                   # BE-specific instructions
│   ├── apps/                       # 10 Django apps
│   └── manage.py
│
├── faion-cli/                      # CLI tool repo (Go)
│   ├── .git/
│   ├── cmd/                        # Commands
│   └── tui/                        # Bubble Tea TUI
│
└── faion-network-storybook/        # Component library (React)
    ├── .git/
    └── stories/                    # 62 components
```

**Key points:**
- One `.aidocs/` folder for ALL repositories
- `constitution.md` covers tech decisions for FE, BE, CLI, Storybook
- Features can touch multiple repos (e.g., Starter Kits = BE API + CLI download)
- Completed Feature 025 (CLI Tool) → moved from todo/ to done/ with all tasks
- Active Feature 024 (Starter Kits) → in todo/, executing TASK-SK-001

## Naming Conventions

### Global (Faion Network)

| Component | Pattern | Example |
|-----------|---------|---------|
| Skill (orchestrator) | `faion-net` | `faion-net` |
| Skill (role-based) | `faion-{role}` | `faion-software-developer`, `faion-ux-ui-designer` |
| Skill (process) | `faion-{process}` | `faion-sdd`, `faion-feature-executor` |
| Agent | `faion-{name}-agent` | `faion-task-YOLO-executor-opus-agent` |
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
| Feature folder | `feature-{NNN}-{name}` | `feature-001-auth`, `feature-025-dashboard` |
| Task file | `TASK-{NNNN}-{title}.md` | `TASK-0001-user-model.md`, `TASK-0150-api-endpoint.md` |

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

### New Single-Repo Project

```bash
# Create project directory
mkdir -p ~/Projects/myapp
cd ~/Projects/myapp

# Initialize git
git init

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

# Create .aidocs structure (inside repo)
mkdir -p .aidocs/{product_docs,backlog,todo,in-progress,done}
```

### New Multi-Repo Project

```bash
# Create project parent directory
mkdir -p ~/Projects/bigapp
cd ~/Projects/bigapp

# Create project CLAUDE.md
cat > CLAUDE.md << 'EOF'
# BigApp - Claude Instructions

## Project
- Name: BigApp
- Repos: bigapp-fe (React), bigapp-be (Django)
- Documentation: .aidocs/ (shared)

## Repositories
- **Frontend:** ./bigapp-fe/ - React + Vite
- **Backend:** ./bigapp-be/ - Django REST

## References
- [Directory Structure](~/.claude/docs/directory-structure.md)
EOF

# Create .aidocs structure (parent level, shared)
mkdir -p .aidocs/{product_docs,backlog,todo,in-progress,done}

# Clone or create repos
git clone <frontend-repo-url> bigapp-fe
git clone <backend-repo-url> bigapp-be
# OR
mkdir bigapp-fe && cd bigapp-fe && git init && cd ..
mkdir bigapp-be && cd bigapp-be && git init && cd ..

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
