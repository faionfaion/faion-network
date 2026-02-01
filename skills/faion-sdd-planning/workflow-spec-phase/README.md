# SDD Workflow: Specification Phase

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Analyze codebase for constitution | sonnet | Medium-complexity codebase analysis |
| Facilitate requirements brainstorming | sonnet | Medium-complexity dialogue and questioning |
| Research existing codebase patterns | haiku | Mechanical pattern search and listing |
| Write specification documents | sonnet | Medium-complexity document composition |
| Create roadmap and plan releases | opus | Complex strategic planning and prioritization |

Detailed workflows for creating specification documents (constitution, spec, contracts, roadmap).

---

## Table of Contents

1. [Writing Constitutions](#1-writing-constitutions)
2. [Writing Specifications](#2-writing-specifications)
3. [Backlog Grooming](#3-backlog-grooming)
4. [Roadmapping](#4-roadmapping)

---

## 1. Writing Constitutions

### Philosophy

Constitution.md defines immutable project principles for ALL features. Two modes:
1. **Existing Project** - codebase analysis
2. **New Project** - Socratic dialogue

### MODE 1: Existing Project Workflow

```
Detect -> Analyze Structure -> Tech Stack -> Patterns -> Draft -> Review
```

**Step 1: Analyze Codebase**
- Directory layout, CLAUDE.md, README.md
- Config files (pyproject.toml, package.json)
- Architecture patterns, naming conventions
- Linter configs, testing setup

**Step 2: Present Findings**
```markdown
**Analysis:**
1. Tech: Python 3.11, Django 4.2, PostgreSQL
2. Architecture: Layered (views -> services -> models)
3. Standards: black + isort + flake8
Does this match? What to change?
```

**Step 3: Draft and Review**

### MODE 2: New Project Workflow

```
Vision -> Tech Choices -> Architecture -> Standards -> Draft -> Review
```

**Step 1: Vision (Socratic)**
"Tell me about the project. What problem does it solve?"
Apply Five Whys to get to real need.

**Step 2: Tech Choices (Alternatives)**
For each decision, present A/B/C with pros/cons:
- Backend: Django vs FastAPI vs NestJS
- Database: PostgreSQL vs MongoDB vs SQLite

**Step 3: Architecture Trade-offs**
- Monolith vs Microservices
- REST vs GraphQL
- ORM vs Raw SQL

**Step 4: Standards**
- Linter, formatter, type hints
- Testing coverage, CI/CD
- Git conventions

### Save Location

```bash
mkdir -p .aidocs/{backlog,todo,in-progress,done}
# Write constitution.md to .aidocs/
```

Create CLAUDE.md navigation hub in project folder.

### Anti-patterns

- Copying without understanding
- Over-engineering at start
- Ignoring team expertise

---

## 2. Writing Specifications

### Philosophy

- **Intent is source of truth** - spec is main artifact
- **Socratic dialogue** - user formulates requirements through questions
- **Brainstorming** - iterative refinement via alternatives

### Workflow

```
BRAINSTORM -> RESEARCH -> CLARIFY -> DRAFT -> REVIEW -> SAVE
```

### Phase 1: Brainstorming

Start: "Tell me about the problem. Who suffers and how?"

**Five Whys** - for each answer ask "Why?":
```
"Need export" -> Why? -> "Managers ask" -> Why? -> "No access" -> Real problem: UX
```

**Alternatives** - for each idea:
```markdown
**A:** {approach 1}
- Pros: {benefits}
- Cons: {drawbacks}

**B:** {approach 2}
- Pros: {benefits}
- Cons: {drawbacks}

Which is closer?
```

**Challenge assumptions:**
- "Is this needed for v1?"
- "What if we DON'T do this?"
- "What exists in codebase?"

### Phase 2: Research Codebase

Search: `Glob **/models.py`, `Grep class.*Model`, `Glob **/.aidocs/**/spec.md`

Share findings: "Found existing export in services.py. Does this affect approach?"

### Phase 3: Clarify Details

**User stories workshop:**
```markdown
As {role}, I want {goal}, so that {benefit}.
- How often?
- What happens if can't do this?
```

**Edge cases through questions** (not assumptions):
- "What if data invalid?"
- "What if 1000+ records?"
- "What if service unavailable?"

### Phase 4: Draft Section by Section

Each section -> show -> validate -> next:

1. Problem Statement -> "Correct?"
2. User Stories with AC -> "Complete?"
3. Functional Requirements -> "Anything redundant?"
4. Out of Scope -> "Agree with boundaries?"

### Phase 5: Review

**Checklist:**
- [ ] Problem clear (SMART)
- [ ] User Stories specific (INVEST)
- [ ] Requirements testable
- [ ] Out of Scope defined

Call `faion-sdd-reviewer-agent (mode: spec)` before save.

### Phase 6: Save

**New feature:** `.aidocs/features/backlog/{NN}-{feature}/spec.md`
**Active feature:** update existing spec.md

### Anti-patterns

- Assumptions instead of questions
- Solution before problem
- Large blocks without validation
- Ignoring "I don't know"

---

## 3. Backlog Grooming

### Workflow

```
READ BACKLOG -> PRIORITIZE -> SELECT FEATURE -> REFINE SPEC -> CREATE DESIGN -> GENERATE TASKS -> MOVE TO TODO
```

### Phase 1: Load Context

Read: `roadmap.md`, `constitution.md`
List features by status: backlog, todo, in-progress, done

### Phase 2: Display Status

```markdown
## Feature Status

### In Progress ({n})
- {feature} - {summary}

### Todo ({n})
- {feature} - {summary}

### Backlog ({n})
- {feature} - {summary} [P0/P1/P2]
```

### Phase 3: Action Selection

AskUserQuestion: "What do you want to do?"
1. Review priorities
2. Take feature to work
3. Add new feature
4. Remove feature
5. Finish grooming

### Phase 4: Feature Selection

Show backlog with: Name, Spec status, Design status, Dependencies

### Phase 5-7: Refine Documents

- If no spec: Use Writing Specifications workflow
- If spec approved: Use Writing Design Documents workflow
- If design approved: Use Writing Implementation Plans workflow

### Phase 8: Move to Todo

If all artifacts complete:
```bash
mv features/backlog/{feature}/ features/todo/{feature}/
```

### Definition of Ready

- [ ] Problem/need clear
- [ ] Acceptance criteria defined
- [ ] Dependencies identified
- [ ] Small enough for one sprint
- [ ] No blockers
- [ ] Spec approved
- [ ] Design approved
- [ ] Tasks created

---

## 4. Roadmapping

### When to Use

- After completing features -> progress review
- New ideas -> add to backlog
- Priorities changed -> reprioritize
- Weekly/sprint -> roadmap sync

### Workflow

```
ANALYZE -> REVIEW PRIORITIES -> ADD FEATURES -> UPDATE ROADMAP
```

### Phase 1: Analyze Progress

```bash
# Count features by status
ls .aidocs/features/done/
ls .aidocs/features/backlog/
```

### Phase 2: Review Priorities

AskUserQuestion: "Are priorities current?"

### Phase 3: Add New Features

For each new idea:
1. Discuss scope via Socratic dialogue
2. Create `backlog/{NN}-{name}/spec.md`
3. Add to roadmap.md

### Roadmap Principles

| Timeframe | Confidence | Detail Level |
|-----------|------------|--------------|
| Now | 90% | Detailed, committed |
| Next | 70% | Planned, flexible |
| Later | 50% | Thematic, vision |

Include 20% buffer for unknowns.

---

*SDD Spec Phase Workflows v1.0*
*Use with faion-sdd skill*
