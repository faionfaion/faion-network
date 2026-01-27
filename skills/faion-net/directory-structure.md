# SDD Directory Structure

## Overview

```
.aidocs/
├── constitution.md           # Tech stack, principles, constraints
├── roadmap.md                # Feature timeline, releases, metrics
│
├── backlog/                  # Features in queue (needs grooming)
│   └── feature-NNN-name/
│       ├── README.md
│       └── spec.md           # Initial spec (may be incomplete)
│
├── todo/                     # Features ready for execution
│   └── feature-NNN-name/
│       ├── README.md
│       ├── spec.md           # Approved specification
│       ├── design.md         # Technical design
│       ├── implementation-plan.md
│       ├── todo/             # Tasks ready to start
│       │   ├── TASK-001-*.md
│       │   └── TASK-002-*.md
│       ├── in-progress/      # Tasks currently executing
│       └── done/             # Completed tasks
│
├── in-progress/              # Features being executed
│   └── feature-NNN-name/
│       ├── README.md
│       ├── spec.md
│       ├── design.md
│       ├── implementation-plan.md
│       ├── todo/             # Remaining tasks
│       ├── in-progress/      # Active tasks
│       │   └── TASK-003-*.md
│       └── done/             # Completed tasks
│           ├── TASK-001-*.md
│           └── TASK-002-*.md
│
├── done/                     # Completed features
│   └── feature-NNN-name/
│       ├── README.md
│       ├── spec.md
│       ├── design.md
│       ├── implementation-plan.md
│       ├── todo/             # Empty
│       ├── in-progress/      # Empty
│       └── done/             # All tasks here
│           ├── TASK-001-*.md
│           ├── TASK-002-*.md
│           └── TASK-003-*.md
│
├── improvements/             # Change requests, enhancements
│   ├── README.md
│   ├── CR-NNN-*.md           # Change requests
│   └── AI-NNN-*.md           # AI-suggested improvements
│
├── memory/                   # SDD memory (project-local)
│   ├── patterns.md           # Learned patterns
│   ├── mistakes.md           # Errors and solutions
│   ├── decisions.md          # Key decisions
│   └── session.md            # Current session state
│
├── product_docs/             # Product planning & GTM
│   ├── idea-validation.md
│   ├── prd.md
│   ├── market-research.md
│   ├── competitive-analysis.md
│   ├── user-personas.md
│   ├── pricing-research.md
│   ├── seo/
│   ├── article-lists/
│   └── gtm-manifest/
│
└── content/                  # Content drafts
    └── articles/
```

---

## Feature Lifecycle

```
backlog/ → todo/ → in-progress/ → done/
```

| Status | Feature Docs | Tasks |
|--------|--------------|-------|
| **backlog** | README, spec (draft) | None or draft tasks |
| **todo** | All docs complete | Tasks in `todo/` subfolder |
| **in-progress** | All docs | Tasks moving through subfolders |
| **done** | All docs | All tasks in `done/` subfolder |

---

## Task Lifecycle (inside feature)

```
feature-NNN-name/
├── todo/           → Tasks ready to start
├── in-progress/    → Tasks being executed (max 1-2 at a time)
└── done/           → Completed tasks
```

**Rule:** Feature moves to `done/` when ALL tasks are in `done/` subfolder.

---

## Key Files

| File | Purpose | Required In |
|------|---------|-------------|
| `README.md` | Feature overview, navigation | All statuses |
| `spec.md` | Requirements, acceptance criteria | All statuses |
| `design.md` | Technical architecture | todo+ |
| `implementation-plan.md` | Task breakdown | todo+ |
| `TASK-NNN-*.md` | Individual executable task | Inside feature |

---

## Feature Folder Structure

```
feature-NNN-name/
├── README.md                 # Overview, links, status
├── spec.md                   # What to build
├── design.md                 # How to build
├── implementation-plan.md    # Task breakdown
├── docs/                     # Supporting documentation (optional)
│   └── *.md
├── assets/                   # Implementation assets (optional)
│   ├── prompts/
│   ├── scripts/
│   └── templates/
├── todo/                     # Tasks ready to execute
│   └── TASK-NNN-slug.md
├── in-progress/              # Tasks being worked on
│   └── TASK-NNN-slug.md
└── done/                     # Completed tasks
    └── TASK-NNN-slug.md
```

---

## Task File Format

```markdown
---
type: task
task_id: NNN
feature: NNN-feature-name
title: "Task Title"
status: todo | in-progress | done
priority: P0 | P1 | P2
created: YYYY-MM-DD
completed: YYYY-MM-DD  # When done
est_tokens: ~Xk
---

# Task: Title

## Objective
{What this task accomplishes}

## Deliverables
- [ ] Deliverable 1
- [ ] Deliverable 2

## Technical Details
{Implementation specifics}

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Notes
{Any additional context}
```

---

## Naming Conventions

| Element | Format | Example |
|---------|--------|---------|
| Feature folder | `feature-NNN-slug` | `feature-028-cli-v2-orchestrator` |
| Task file | `TASK-NNN-slug.md` | `TASK-001-project-setup.md` |
| Change request | `CR-NNN-slug.md` | `CR-007-auth-improvements.md` |
| Improvement | `AI-NNN-slug.md` | `AI-003-performance-optimization.md` |

---

## Multi-Repo Projects

For projects with multiple repositories (FE + BE):

```
project/
├── CLAUDE.md                 # Project navigation
├── .aidocs/                  # Shared documentation (ALL repos)
│   ├── constitution.md       # Tech stack for ALL repos
│   ├── backlog/
│   ├── todo/
│   ├── in-progress/
│   └── done/
├── project-fe/               # Frontend repo
├── project-be/               # Backend repo
└── project-cli/              # CLI repo (optional)
```

Features in `.aidocs/` may touch one or multiple repos.

---

## Summary

1. **Features** move through: `backlog/ → todo/ → in-progress/ → done/`
2. **Tasks** live INSIDE feature folders with their own lifecycle subfolders
3. **Task lifecycle**: `todo/ → in-progress/ → done/` (inside feature)
4. **Feature is done** when all tasks are in `done/` subfolder
5. **No time estimates** - use complexity (Low/Medium/High) + token estimates
