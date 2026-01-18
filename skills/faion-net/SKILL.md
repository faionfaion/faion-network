---
name: faion-net
description: "SDD Workflow Orchestrator - manage projects, features, specs, designs, implementation plans, tasks"
user-invocable: true
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
- Offer: "Виконати TASK_000 зараз?"

## Phase 4: Select Feature

```bash
# List features by status
ls -d aidocs/sdd/{project}/features/in-progress/*/ 2>/dev/null | xargs -I{} basename {}
ls -d aidocs/sdd/{project}/features/todo/*/ 2>/dev/null | xargs -I{} basename {}
ls -d aidocs/sdd/{project}/features/backlog/*/ 2>/dev/null | xargs -I{} basename {}
ls -d aidocs/sdd/{project}/features/done/*/ 2>/dev/null | xargs -I{} basename {}
```

AskUserQuestion: "Що хочеш зробити?" options:
- In-progress features (continue work)
- Todo features (start execution)
- Backlog features (needs grooming)
- Done features (review)
- "+ Нова фіча" (add to backlog)
- "Backlog grooming" → Call `faion-backlog-grooming` skill
- "Product research" → Call `faion-product-research` skill
- "GTM Manifest" → Call `faion-gtm-manifest` skill
- "Idea discovery" → Call `faion-idea-discovery` skill
- "MLP Planning" → Call `faion-mlp-planning` skill
- "Standalone tasks" (technical/one-off tasks)
- "Product docs" (PRD, personas, etc.)

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
→ Offer task execution

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
2. Execute tasks using faion-task-executor agent
3. Or batch execution

## Phase 7: Feature Completion

When all tasks done:
1. Move feature from in-progress/ to done/
2. Update roadmap.md status
3. Offer next feature

---

## Directory Structure

```
aidocs/sdd/{project}/
├── constitution.md
├── roadmap.md
│
├── product_docs/
│   ├── idea-validation.md
│   ├── prd.md
│   ├── market-research.md
│   ├── competitive-analysis.md
│   ├── user-personas.md
│   ├── problem-validation.md
│   ├── pricing-research.md
│   ├── executive-summary.md
│   ├── mlp-analysis-report.md
│   ├── mlp-implementation-order.md
│   └── gtm-manifest/
│
├── tasks/
│   ├── backlog/
│   ├── todo/
│   ├── in-progress/
│   └── done/
│
└── features/
    ├── backlog/{NN}-{feature}/
    │   └── spec.md
    ├── todo/{NN}-{feature}/
    │   ├── spec.md
    │   ├── design.md
    │   ├── implementation-plan.md
    │   └── tasks/{backlog,todo,in-progress,done}/
    ├── in-progress/{NN}-{feature}/
    └── done/{NN}-{feature}/
```

---

## Domain Skills

| Skill | When to Use |
|-------|-------------|
| `faion-sdd-domain-skill` | Writing specs, designs, implementation plans. Task creation and execution. Quality gates, confidence checks, reflexion learning. |
| `faion-research-domain-skill` | Brainstorming ideas, validating problems, researching markets. Competitor analysis, persona building, pricing research. |
| `faion-product-domain-skill` | MVP/MLP planning, feature prioritization (RICE/MoSCoW), roadmapping. Gap analysis between current state and target. |
| `faion-development-domain-skill` | Writing code (Python, JS, Go, etc.), code review, refactoring. CI/CD, testing, API design, DevOps. |
| `faion-marketing-domain-skill` | GTM strategy, landing pages, content marketing. Ads (Meta/Google), email campaigns, social media, SEO. |
| `faion-pmbok-domain-skill` | Project management using PMBOK 7/8. Stakeholder management, risk management, EVM, change control. |
| `faion-babok-domain-skill` | Business analysis using BABOK v3. Requirements elicitation, traceability, solution assessment. |
| `faion-ux-domain-skill` | UX research, usability testing, heuristic evaluation (Nielsen Norman 10). Personas, journey mapping, wireframing. |

---

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
