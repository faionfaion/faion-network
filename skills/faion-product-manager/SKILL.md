---
name: faion-product-manager
description: "Product Manager orchestrator: coordinates 2 sub-skills (Planning + Operations). 33 total methodologies. MVP/MLP planning, prioritization, roadmaps, backlog, analytics."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Bash(ls:*), Bash(mkdir:*), Task, AskUserQuestion, TodoWrite
---

# Product Manager Skill

**Communication: User's language. Docs: English.**

## Purpose

Orchestrates product management activities: planning, operations, discovery, launch.

**Architecture:** Orchestrator → 2 sub-skills (17 + 16 methodologies)

---

## Sub-Skills

| Sub-Skill | Focus | Methodologies |
|-----------|-------|---------------|
| [faion-product-manager:planning](../faion-product-manager:planning/SKILL.md) | MVP/MLP, roadmaps, discovery, launch | 17 |
| [faion-product-manager:operations](../faion-product-manager:operations/SKILL.md) | Prioritization, backlog, analytics, lifecycle | 16 |

**Total:** 33 methodologies | 2 agents

---

## Decision Tree

### Planning Activities
Use [faion-product-manager:planning](../faion-product-manager:planning/SKILL.md):
- Define MVP/MLP scope
- Create roadmaps (Now-Next-Later, outcome-based)
- User story mapping
- Product discovery and validation
- Launch planning
- OKR setting

### Operations Activities
Use [faion-product-manager:operations](../faion-product-manager:operations/SKILL.md):
- Feature prioritization (RICE, MoSCoW)
- Backlog management and grooming
- Product analytics and metrics
- Feedback management
- Technical debt tracking
- Stakeholder management

---

## Quick Reference

| Resource | Location | Content |
|----------|----------|---------|
| **Workflows** | [workflows.md](workflows.md) | Bootstrap, MLP transformation flows |
| **Agents** | [agents.md](agents.md) | MVP analyzer, MLP orchestrator |
| **Methodologies** | [methodologies-summary.md](methodologies-summary.md) | Full 33-methodology catalog |

---

## Common Workflows

**New Product:**
```
mvp-scoping → feature-prioritization-rice → user-story-mapping → roadmap-design → product-launch
```

**Quarterly Planning:**
```
okr-setting → backlog-management → feature-prioritization-rice → release-planning
```

**Discovery Sprint:**
```
product-discovery → continuous-discovery → feedback-management → backlog-management
```

---

## Agents

| Agent | Purpose | Location |
|-------|---------|----------|
| faion-mvp-scope-analyzer-agent | MVP scope via competitor analysis | [agents.md](agents.md) |
| faion-mlp-agent | MLP orchestrator (5 modes) | [agents.md](agents.md) |

---

## Cross-Skill Routing

<<<<<<< HEAD
| Reference | Content | Lines |
|-----------|---------|-------|
| ref-minimum-product-frameworks.md | 9 Product Frameworks: MVP, MLP, MMP, MAC, RAT, MDP, MVA, MFP, SLC |
| ref-micro-mvps.md | Micro-MVPs: Landing page, concierge, Wizard of Oz, video demo |
| ref-ai-native-product-development.md | AI-Native Product Development |
| ref-continuous-discovery.md | Continuous Discovery Habits |

---

## Workflows

### Workflow 1: Project Bootstrap

Full pipeline from idea to first task.

```
IDEA → CONCEPT → TECH STACK → MVP SCOPE → CONFIRMATION → BACKLOG → CONSTITUTION → TASK_000
```

**Output:**
```
.aidocs/
├── constitution.md
├── roadmap.md
└── features/
    ├── backlog/{NN}-{feature}/spec.md
    └── 00-setup/tasks/todo/TASK_000_project_setup.md
```

**Phases:**
1. Vision Brainstorm - Apply Five Whys to get to real need
2. Tech Stack Selection - Frontend, backend, database
3. MVP Definition - Max 3-5 features, cut 50% nice-to-haves
4. User Confirmation - Present summary, get approval
5. Backlog Creation - Create feature specs
6. Constitution - Write project constitution
7. TASK_000 - Setup task with project goals

### Workflow 2: MLP Planning

Transform MVP to Most Lovable Product.

```
1. Analyze MVP scope (competitors)
2. Extract current state from specs
3. Find MLP gaps
4. Propose WOW features
5. Update specs with MLP reqs
6. Create implementation order
```

**Output:**
```
product_docs/
├── mvp-scope-analysis.md
├── mlp-analysis-report.md
└── mlp-implementation-order.md
```

---

## Methodologies (18)

### mvp-scoping

**Problem:** Teams build too much before validation.

**Framework:**
1. Define core problem (one sentence)
2. Identify minimum features to solve it
3. Cut 50% of nice-to-haves
4. Set 4-week development constraint

**Agent:** faion-mvp-scope-analyzer-agent

### mlp-planning

**Problem:** MVP works but users don't love it.

**Framework:**
1. Analyze MVP for friction points
2. Identify WOW moments opportunities
3. Plan delight features
4. Create implementation phases

**MLP Dimensions:**
- **Delight**: Micro-interactions, animations, polish
- **Ease**: Intuitive UX, zero friction
- **Speed**: Instant feedback, fast performance
- **Trust**: Security signals, reliability
- **Personality**: Brand voice, memorable moments

**Agent:** faion-mlp-agent (mode: find-gaps)

### feature-prioritization-rice

**Problem:** Too many features, limited resources.

**Framework:**
| Factor | Question | Score |
|--------|----------|-------|
| Reach | How many users affected per quarter? | 0-10 |
| Impact | How much will it move the needle? | 0.25, 0.5, 1, 2, 3 |
| Confidence | How sure are we? | 0-100% |
| Effort | How many person-weeks? | 0.5-10 |

**Formula:** `RICE = (Reach * Impact * Confidence) / Effort`

**Agent:** faion-pm-agent

### feature-prioritization-moscow

**Problem:** Stakeholders disagree on priorities.

**Framework:**
| Category | Description | Rule |
|----------|-------------|------|
| **Must** | Non-negotiable for launch | 60% of effort |
| **Should** | Important but not critical | 20% of effort |
| **Could** | Nice to have | 10% of effort |
| **Won't** | Explicitly out of scope | 0% |

**Agent:** faion-pm-agent

### roadmap-design

**Problem:** No clear development direction.

**Framework:**
1. Define time horizons (Now, Next, Later)
2. Align with business goals
3. Map features to milestones
4. Include buffer (20%)

**Template:**
```
## Q1 - Now (commit)
- Feature A: description
- Feature B: description

## Q2 - Next (plan)
- Feature C: description

## Q3+ - Later (vision)
- Theme: description
```

**Agent:** faion-pm-agent

### user-story-mapping

**Problem:** Features lack user context.

**Framework:**
1. Define user activities (horizontal)
2. List tasks under activities
3. Prioritize vertically (top = MVP)
4. Draw release lines

**Format:**
```
Activity 1    Activity 2    Activity 3
---------     ---------     ---------
Task 1.1      Task 2.1      Task 3.1   ← MVP
Task 1.2      Task 2.2      Task 3.2   ← Release 2
Task 1.3                    Task 3.3   ← Release 3
```

**Agent:** faion-pm-agent

### okr-setting

**Problem:** Goals are vague or unmeasurable.

**Framework:**
| Component | Rule |
|-----------|------|
| Objective | Qualitative, inspiring, time-bound |
| Key Results | 3-5 per objective, measurable, ambitious |
| Initiatives | Actions to achieve key results |

**Template:**
```
## Objective: [What we want to achieve]

### KR1: [Metric] from X to Y
- Initiative: [Action]
- Initiative: [Action]

### KR2: [Metric] from X to Y
- Initiative: [Action]
```

**Agent:** faion-pm-agent

### problem-validation (see faion-researcher)

**Problem:** Building solutions for non-problems.

**Framework:**
1. State the problem
2. Who has this problem?
3. How do they solve it today?
4. How much does it cost them?
5. Would they pay for a solution?

**Evidence Required:**
- 5+ user interviews
- Competitor analysis
- Search volume data

**Agent:** faion-market-researcher-agent

### risk-assessment

**Problem:** Unknown risks in product decisions.

**Framework:**
```
               High Impact
                   │
    High Risk ─────┼───── Low Risk
    (test first)   │      (monitor)
                   │
               Low Impact
```

**Steps:**
1. List all assumptions
2. Rate impact (1-5)
3. Rate uncertainty (1-5)
4. Plot on matrix
5. Test high-impact, high-uncertainty first

**Agent:** faion-pm-agent

### business-model-research (see faion-researcher)

**Problem:** Business model not structured.

**Framework:**
```
┌─────────────┬──────────────┬─────────────┐
│ Problem     │ Solution     │ UVP         │
├─────────────┼──────────────┼─────────────┤
│ Key Metrics │ Unfair Adv.  │ Channels    │
├─────────────┴──────────────┴─────────────┤
│ Cost Structure      │ Revenue Streams    │
└─────────────────────┴────────────────────┘
```

**Agent:** faion-pm-agent

### jobs-to-be-done (see faion-researcher)

**Problem:** Features don't match user needs.

**Framework:**
```
When I [situation],
I want to [motivation],
So I can [expected outcome].
```

**Example:**
```
When I receive a payment notification,
I want to verify it's legitimate,
So I can confirm to my customer without worry.
```

**Agent:** faion-persona-builder-agent

### niche-evaluation (see faion-researcher)

**Problem:** Too many opportunities, no prioritization.

**Framework:**
| Factor | Weight | Score (1-10) |
|--------|--------|--------------|
| Market Size | 30% | |
| Competition | 20% | |
| Fit with skills | 25% | |
| Monetization | 25% | |

**Formula:** Weighted average = final score

**Agent:** faion-market-researcher-agent

### value-proposition-design (see faion-researcher)

**Problem:** Product-market fit unclear.

**Framework:**
```
Customer Segment:
├── Jobs (what they try to do)
├── Pains (obstacles, risks)
└── Gains (desired outcomes)

Value Map:
├── Products/Services
├── Pain Relievers (how we reduce pains)
└── Gain Creators (how we create gains)

FIT = Pain Relievers match Pains + Gain Creators match Gains
```

**Agent:** faion-market-researcher-agent

### release-planning

**Problem:** Unclear work for upcoming sprint.

**Framework:**
1. Review sprint goal
2. Select items from backlog
3. Break into tasks (< 8 hours each)
4. Estimate total capacity
5. Commit to sprint backlog

**Velocity:** Average story points from last 3 sprints

**Agent:** faion-pm-agent

### product-launch

**Problem:** No clear release timeline.

**Framework:**
1. Define release goal
2. Identify required features
3. Estimate total effort
4. Divide by velocity = sprints needed
5. Add 20% buffer
6. Set release date

**Agent:** faion-pm-agent

### backlog-management

**Problem:** Backlog items unclear or oversized.

**Framework:**
1. Review items for next 2-3 sprints
2. Add acceptance criteria
3. Estimate complexity
4. Split large items (> 13 points)
5. Prioritize

**Definition of Ready:**
- [ ] Clear description
- [ ] Acceptance criteria defined
- [ ] Estimated
- [ ] Dependencies identified
- [ ] Small enough for one sprint

**Agent:** faion-pm-agent

### product-discovery

**Problem:** Root cause not understood.

**Framework:**
```
Problem: [State the problem]

Why 1: [First level answer]
Why 2: [Go deeper]
Why 3: [Go deeper]
Why 4: [Go deeper]
Why 5: [Root cause]

Action: [Fix the root cause]
```

**Agent:** faion-pm-agent

### stakeholder-management

**Problem:** Features disconnected from goals.

**Framework:**
```
Goal → Actor → Impact → Deliverable
  │       │       │         │
  │       │       │         └─ What we build
  │       │       └─ How actor behavior changes
  │       └─ Who can help/hinder goal
  └─ Business objective
```

**Example:**
```
Goal: Increase revenue 20%
├─ Actor: Premium users
│  └─ Impact: Use more features
│     └─ Deliverable: Feature X
└─ Actor: Free users
   └─ Impact: Upgrade
      └─ Deliverable: Upgrade prompts
```

**Agent:** faion-pm-agent


> **Note:** Full methodology details available in skill root (files: mvp-scoping.md, mlp-planning.md, etc.).

---

## Execution

### Bootstrap Flow

```python
# Phase 1: Vision
AskUserQuestion(questions=[
    {"question": "Tell me about the project"},
])

# Phase 2: Tech Stack
AskUserQuestion([
    {"question": "Frontend?", "options": [
        {"label": "React + TypeScript"},
        {"label": "Next.js"},
        {"label": "None (API only)"}
    ]},
    {"question": "Backend?", "options": [
        {"label": "Python + Django"},
        {"label": "Python + FastAPI"},
        {"label": "Go"},
        {"label": "Node.js"}
    ]},
    {"question": "Database?", "options": [
        {"label": "PostgreSQL"},
        {"label": "SQLite"},
        {"label": "MongoDB"}
    ]}
])

# Phase 3: MVP Definition
Task(subagent_type="faion-mvp-scope-analyzer-agent",
     prompt=f"Analyze {product_type} competitors for MVP scope")

# Phase 4: Confirmation (MANDATORY)
# Present summary, get approval

# Phase 5: Create backlog and constitution
```

### MLP Flow

```python
# MVP analysis first
Task(subagent_type="faion-mvp-scope-analyzer-agent",
     prompt=f"Analyze {product_type} competitors for MVP scope")

# MLP orchestrator handles all phases
Task(subagent_type="faion-mlp-agent",
     prompt=f"""
     mode: analyze
     project_path: {project_path}
     """)

Task(subagent_type="faion-mlp-agent",
     prompt=f"""
     mode: find-gaps
     project_path: {project_path}
     """)

Task(subagent_type="faion-mlp-agent",
     prompt=f"""
     mode: propose
     project_path: {project_path}
     product_type: {product_type}
     """)

Task(subagent_type="faion-mlp-agent",
     prompt=f"""
     mode: update
     project_path: {project_path}
     """)

Task(subagent_type="faion-mlp-agent",
     prompt=f"""
     mode: plan
     project_path: {project_path}
     """)
```

---

## Numbering Convention

| Type | Pattern | Example |
|------|---------|---------|
| Features | `{NN}-{name}` | `01-auth`, `02-payments` |
| Tasks | `TASK_{NNN}_*` | `TASK_001_setup` |
| Requirements | `FR-{NN}.{N}` | `FR-01.1` |
| Acceptance | `AC-{NN}.{N}` | `AC-01.1` |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-researcher | Provides market data for product decisions |
| faion-project-manager | Provides PM standards |
| faion-business-analyst | Provides BA standards |
| faion-sdd | Uses product decisions for specs |

---

*Domain Skill v1.1 - Product Planning*
*18 Methodologies | 2 Agents*
*Merged from: faion-mlp-planning, faion-project-bootstrap*
=======
| Need | Route To |
|------|----------|
| Market research, competitors | [faion-researcher](../faion-researcher/SKILL.md) |
| Technical architecture | [faion-software-architect](../faion-software-architect/SKILL.md) |
| Specs to implementation | [faion-sdd](../faion-sdd/SKILL.md) |
| Execution tracking | [faion-project-manager](../faion-project-manager/SKILL.md) |
| Requirements analysis | [faion-business-analyst](../faion-business-analyst/SKILL.md) |

---

*Product Manager Orchestrator v2.0*
*33 Methodologies | 2 Sub-Skills | 2 Agents*
>>>>>>> claude
