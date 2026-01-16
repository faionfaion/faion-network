---
description: "SDD Workflow Orchestrator - manage projects, features, specs, designs, implementation plans, tasks"
argument-hint: "[project] or [project/feature]"
hooks:
  PreToolUse:
    - matcher: ""
      hooks:
        - type: command
          command: ~/.claude/hooks/auto-update.sh
          once: true
---

# SDD Workflow Orchestrator

**Communication with user: User's language.**

## Workflow

```
IDEA DISCOVERY (optional):
  /faion-idea-discovery → brainstorm → validate pain → evaluate niche → idea-validation.md
                    ↓
NEW PROJECT:
  bootstrap → constitution.md → TASK_000_setup → Execute setup
                    ↓
PRODUCT RESEARCH (optional):
  /faion-product-research → market, competitors, personas, validation, pricing
                    ↓
GTM MANIFEST (optional):
  /faion-gtm-manifest → go-to-market strategy from research data
                    ↓
FEATURE DEVELOPMENT (with quality gates):
  backlog/ → [confidence-check] → grooming → todo/ → [parallelize] → in-progress/ → done/
     ↓                               ↓         ↓                          ↓            ↓
  spec.md                      + design    ready                    executing    [reflexion]
                               + tasks                                            archived
                    ↓
MLP PLANNING (optional):
  /faion-mlp-planning → gap analysis → update specs → WOW moments → impl order
```

## Phase 1-2: Select Project

```bash
ls -d aidocs/sdd/*/ 2>/dev/null | xargs -I{} basename {}
```

AskUserQuestion: "З яким проектом працюємо?" + "+ Новий проект"

## Phase 3: New Project

If new project:
1. Ask project name (kebab-case)
2. Ask if codebase exists:
   - **No codebase** → Call `faion-project-bootstrap` skill (full brainstorm + constitution + TASK_000)
   - **Has codebase** → Call `faion-writing-constitutions` skill (analysis mode)

**After bootstrap completes:**
- Constitution created: `aidocs/sdd/{project}/constitution.md`
- Roadmap created: `aidocs/sdd/{project}/roadmap.md`
- Setup task created: `aidocs/sdd/{project}/features/todo/00-setup/tasks/todo/TASK_000_project_setup.md`
- Offer: "Виконати TASK_000 зараз?" → `/faion-execute-task {project}/00-setup TASK_000`

## Phase 4: Select Feature

```bash
# List features by status
ls -d aidocs/sdd/{project}/features/in-progress/*/ 2>/dev/null | xargs -I{} basename {}
ls -d aidocs/sdd/{project}/features/todo/*/ 2>/dev/null | xargs -I{} basename {}
ls -d aidocs/sdd/{project}/features/backlog/*/ 2>/dev/null | xargs -I{} basename {}
ls -d aidocs/sdd/{project}/features/done/*/ 2>/dev/null | xargs -I{} basename {}
```

AskUserQuestion: "Що хочеш зробити?" options:
- 🚧 In-progress features (continue work)
- 📋 Todo features (start execution)
- 📝 Backlog features (needs grooming)
- ✅ Done features (review)
- "+ Нова фіча" (add to backlog)
- "📊 Backlog grooming" → Call `faion-backlog-grooming` skill
- "🔬 Product research" → Call `faion-product-research` skill
- "📊 GTM Manifest" → Call `faion-gtm-manifest` skill
- "💡 Idea discovery" → Call `faion-idea-discovery` skill
- "💖 MLP Planning" → Call `faion-mlp-planning` skill
- "🔧 Standalone tasks" (technical/one-off tasks)
- "📄 Product docs" (PRD, personas, etc.)

**If Backlog grooming:**
→ Call `faion-backlog-grooming` skill
→ Interactive session: prioritize, refine specs, create designs, generate tasks

**If Product research:**
→ Call `faion-product-research` skill
→ Options: market research, competitor analysis, user personas, problem validation, pricing
→ Writes to `product_docs/`

**If GTM Manifest:**
→ Requires: product research complete (market, competitors, personas, pricing)
→ Call `faion-gtm-manifest` skill
→ Writes to `product_docs/gtm-manifest/`

**If Idea discovery:**
→ Call `faion-idea-discovery` skill
→ Brainstorm ideas, research pain points, evaluate niches
→ Creates: `idea-validation.md`

**If MLP Planning:**
→ Call `faion-mlp-planning` skill
→ Analyzes MVP specs, identifies MLP gaps, adds WOW moments
→ Creates: `mlp-analysis-report.md`, `mlp-implementation-order.md`

**If feature from backlog:**
→ Needs grooming first (spec, design, tasks)
→ Redirect to `faion-backlog-grooming` skill

**If feature from todo:**
→ Ready for execution
→ Offer: `/faion-execute-task` or `/faion-do-all-tasks`

**If feature from in-progress:**
→ Show task status, continue execution

**If new feature:**
1. Get next number from existing features
2. Call `faion-writing-specifications` skill
3. Create `features/backlog/{NN}-{feature}/spec.md`

**If Standalone tasks:**
1. List tasks from `tasks/{backlog,todo,in-progress,done}/`
2. Options:
   - Execute task from todo/
   - Create new standalone task
   - Move task between statuses

**If Product docs:**
1. List docs from `product_docs/`
2. Options:
   - View/edit existing doc
   - Create new doc (PRD, personas, competitive analysis, etc.)

## Phase 5: Feature Grooming (via skill)

When feature needs grooming:
1. Call `faion-backlog-grooming` skill with feature
2. Skill handles: spec refinement → design → tasks
3. Moves feature from backlog/ to todo/

## Phase 6: Feature Execution

When feature is in todo/ and ready:
1. Move to in-progress/
2. Execute tasks: `/faion-execute-task {project}/{feature} TASK_NNN`
3. Or batch: `/faion-do-all-tasks {project}/{feature}`

## Phase 7: Feature Completion

When all tasks done:
1. Move feature from in-progress/ to done/
2. Update roadmap.md status
3. Offer next feature

## Directory Structure

```
aidocs/sdd/{project}/
├── constitution.md
├── roadmap.md                       # Milestones, progress, risks
│
├── product_docs/                    # Product documentation
│   ├── idea-validation.md           # Idea validation & niche evaluation
│   ├── prd.md                       # Product Requirements Document
│   ├── market-research.md           # TAM/SAM/SOM, trends
│   ├── competitive-analysis.md      # Competitors analysis
│   ├── user-personas.md             # User personas
│   ├── problem-validation.md        # Problem validation evidence
│   ├── pricing-research.md          # Pricing benchmarks
│   ├── executive-summary.md         # Research synthesis
│   ├── mlp-analysis-report.md       # MLP gap analysis
│   ├── mlp-implementation-order.md  # MLP phases & WOW moments
│   └── gtm-manifest/                # Go-to-market strategy
│       └── gtm-manifest-full.md
│
├── tasks/                           # Standalone tasks (no feature)
│   ├── backlog/                     # Task ideas
│   ├── todo/                        # Ready to execute
│   ├── in-progress/                 # Being executed
│   └── done/                        # Completed
│
└── features/
    ├── backlog/                     # Features waiting for grooming
    │   └── {NN}-{feature}/
    │       ├── spec.md              # Draft or needs refinement
    │       └── tasks/
    │           └── backlog/         # Task ideas (optional)
    │
    ├── todo/                        # Features ready for execution
    │   └── {NN}-{feature}/
    │       ├── spec.md              # Approved
    │       ├── design.md            # Approved
    │       ├── implementation-plan.md
    │       └── tasks/
    │           ├── backlog/         # Task ideas
    │           ├── todo/            # Ready to execute
    │           ├── in-progress/     # Being executed
    │           └── done/            # Completed
    │
    ├── in-progress/                 # Features being worked on
    │   └── {NN}-{feature}/
    │       └── ... (same structure as todo)
    │
    └── done/                        # Completed features
        └── {NN}-{feature}/
            └── ... (archived)
```

## Standalone Tasks vs Feature Tasks

**Standalone tasks** (`tasks/`):
- One-off technical tasks (refactoring, upgrades, infra)
- Quick fixes without full spec/design
- Research spikes
- Don't belong to any feature

**Feature tasks** (`features/{status}/{NN}-{feature}/tasks/`):
- Part of feature implementation
- Have spec.md and design.md as context
- Follow implementation-plan.md

## Feature Lifecycle

```
backlog/  →  todo/  →  in-progress/  →  done/
   ↓           ↓            ↓             ↓
 draft      groomed     executing     archived
 spec       spec+       tasks
            design+
            tasks
```

## Task Lifecycle (within feature)

```
tasks/backlog/  →  tasks/todo/  →  tasks/in-progress/  →  tasks/done/
      ↓               ↓                  ↓                    ↓
  task ideas      refined &         being executed        completed
                  ready
```

## Numbering Convention

- Feature directories: `{NN}-{name}` (00, 01, 02, ...)
- Tasks: `TASK_{NNN}_*` (000, 001, 002, ...)
- Requirements: `FR-{NN}.{N}` (FR-01.1, FR-01.2, ...)
- Acceptance Criteria: `AC-{NN}.{N}` (AC-01.1, AC-01.2, ...)

## Quality Assurance

### Confidence Check (before each phase)
```
Pre-Spec:     Problem validated? Market gap? Target audience?
Pre-Design:   Requirements clear? AC testable? No contradictions?
Pre-Task:     Architecture decided? No duplicates? Dependencies mapped?
Pre-Impl:     Task clear? Approach decided? No blockers?
```
**Threshold:** ≥90% proceed, 70-89% clarify, <70% stop

### Hallucination Prevention (before marking done)
1. Tests passing? → Show actual output
2. Requirements met? → List each with evidence
3. No assumptions? → Show documentation
4. Evidence exists? → Provide test results, code changes

### Reflexion Learning (after completion)
- Success → Store pattern in `~/.sdd/memory/patterns_learned.jsonl`
- Failure → Store error + solution in `~/.sdd/memory/mistakes_learned.jsonl`
- Metrics → Track in `~/.sdd/memory/workflow_metrics.jsonl`

## Memory System

```
~/.sdd/memory/
├── patterns_learned.jsonl    # Successful patterns (PAT-NNN)
├── mistakes_learned.jsonl    # Errors + solutions (ERR-NNN)
├── workflow_metrics.jsonl    # Task execution metrics
└── session_context.md        # Current session state
```

Use `/faion-reflexion` to record and learn.

## Skills & Agents

| Type | Name | Purpose |
|------|------|---------|
| Skill | **faion-project-bootstrap** | Full project bootstrap (brainstorm → constitution → backlog → TASK_000) |
| Skill | **faion-idea-discovery** | **Brainstorm ideas, research pain points, evaluate niches** |
| Skill | **faion-backlog-grooming** | **Interactive grooming: prioritize, refine specs, create designs & tasks** |
| Skill | **faion-product-research** | Market research, competitor analysis, personas, problem validation, pricing |
| Skill | **faion-gtm-manifest** | Go-to-market strategy from research data (12 sections) |
| Skill | **faion-mlp-planning** | Transform MVP to MLP - gap analysis, WOW moments, implementation order |
| Skill | **faion-project-naming** | Generate & validate project names, check domains, write to constitution |
| Skill | **faion-roadmap** | Review progress, reprioritize, add new features |
| Skill | **faion-confidence-check** | Pre-execution validation (≥90% to proceed, prevents wrong-direction work) |
| Skill | **faion-reflexion** | Learn from mistakes, store patterns in ~/.sdd/memory/ |
| Skill | **faion-task-parallelizer** | Analyze dependencies, create parallel execution waves (3.5x speedup) |
| Skill | **faion-dev-ui-design** | UI brainstorming, prototyping, Storybook-driven development |
| Skill | **faion-landing-page** | Create high-converting landing pages (copy + design + implementation) |
| Skill | **faion-execute-task** | Execute single task via faion-task-executor agent |
| Skill | **faion-do-all-tasks** | Execute all tasks for feature sequentially |
| Skill | **faion-make-tasks** | Create tasks from SDD documents (spec + design + impl-plan) |
| Skill | **faion-review** | Code review or SDD document review |
| Skill | faion-writing-constitutions | Create constitution (for existing codebase) |
| Skill | faion-writing-specifications | Create/refine spec |
| Skill | faion-writing-design-docs | Create design |
| Skill | faion-writing-implementation-plan | Create implementation plan |
| Agent | faion-task-creator | Create individual tasks |
| Agent | faion-task-executor | Execute tasks autonomously |
| Agent | faion-tasks-reviewer | Review tasks quality |
| Agent | faion-spec-reviewer | Review spec quality before approval |
| Agent | faion-design-reviewer | Review design for architecture decisions |
| Agent | faion-impl-plan-reviewer | Review impl-plan for 100k token compliance |
| Agent | faion-market-researcher | TAM/SAM/SOM, trends, growth drivers |
| Agent | faion-competitor-analyzer | Competitor features, pricing, positioning |
| Agent | faion-persona-builder | User personas from real feedback |
| Agent | faion-problem-validator | Problem validation with evidence |
| Agent | faion-pricing-researcher | Pricing benchmarks and strategies |
| Agent | faion-mvp-scope-analyzer | Define MVP via competitor feature analysis |
| Agent | faion-mlp-spec-analyzer | Analyze specs for MLP gaps |
| Agent | faion-mlp-gap-finder | Compare MVP vs MLP |
| Agent | faion-mlp-spec-updater | Add MLP requirements to specs |
| Agent | faion-mlp-feature-proposer | Propose new MLP features |
| Agent | faion-mlp-impl-planner | Create MLP implementation order |
| Agent | faion-name-generator | Creative project name brainstorming |
| Agent | faion-domain-checker | Verify domains, handles, trademarks |
| Agent | faion-idea-generator | Generate startup/product ideas using frameworks |
| Agent | faion-pain-point-researcher | Research pain points via Reddit/forums |
| Agent | faion-niche-evaluator | Evaluate niche viability (market, competition, barriers) |
| Agent | faion-hallucination-checker | Verify task completion with evidence (94% accuracy protocol) |
| Agent | faion-dev-design-brainstormer | Generate multiple UI design variants (HTML/React) |
| Agent | faion-dev-storybook-manager | Setup and maintain Storybook |
| Agent | faion-landing-copywriter | Landing page copy using AIDA/PAS frameworks |
| Agent | faion-landing-designer | Landing page design and HTML/Tailwind implementation |
| Agent | faion-landing-analyzer | Landing page conversion analysis and A/B test suggestions |
| Agent | faion-dev-component-developer | Develop components with stories and tests |

## Commands (User Entry Points)

| Command | Purpose |
|---------|---------|
| `/sdd` | **Single entry point** - all SDD workflow starts here |
| `/faion-net {project}` | Work with specific project |
| `/faion-net {project}/{feature}` | Work with specific feature |

**All operations are accessed through `/sdd`:**
- Task execution → `/sdd` → select feature → execute task
- Task creation → `/sdd` → select feature → create tasks
- Reviews → `/sdd` → select feature → review
- Grooming → `/sdd` → backlog grooming
- Research → `/sdd` → product research

**Skills are internal** (user-invocable: false) - orchestrated by `/sdd`.
