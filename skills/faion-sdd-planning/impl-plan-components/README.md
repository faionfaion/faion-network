# Implementation Plan Components

## Document Structure v2.0

### Full Structure

```markdown
# Implementation Plan: [Feature Name]

## Reference Documents
[Links to design, spec, constitution]

## Overview
[Summary of implementation approach]

## Prerequisites
[What must exist before starting]

## Dependency Graph
[Visual dependency tree]

## Wave Analysis
[Tasks grouped by execution waves]

## Phase Breakdown
[Logical grouping of tasks]

## Task List
[TASK-XXX entries with INVEST validation]

## Critical Path
[Longest dependency chain]

## Risk Assessment
[Risks and mitigations]

## Testing Plan
[What to test at each phase]

## Rollout Strategy
[How to deploy safely]

## Recommended Skills & Methodologies
[For task execution]
```

---

## Prerequisites

What must exist before starting.

### Structure

```markdown
## Prerequisites

### Infrastructure
- [ ] PostgreSQL database running
- [ ] Redis instance configured
- [ ] SendGrid API key obtained

### Environment
- [ ] Development environment set up
- [ ] Environment variables configured
- [ ] Access permissions granted

### Code Dependencies
- [ ] Base service class exists
- [ ] Auth middleware exists
- [ ] Test framework configured

### Documentation
- [ ] Spec approved (status: Approved)
- [ ] Design approved (status: Approved)
```

---

## Dependency Graph

Visual representation of task dependencies.

### Dependency Types (PM: dependency-management)

| Type | Meaning | Example |
|------|---------|---------|
| **FS** | Finish-to-Start | TASK-002 starts when TASK-001 finishes |
| **SS** | Start-to-Start | TASK-002 can start when TASK-001 starts |
| **FF** | Finish-to-Finish | TASK-002 finishes when TASK-001 finishes |
| **SF** | Start-to-Finish | TASK-002 finishes when TASK-001 starts (rare) |

### Example

```markdown
## Dependency Graph

```
TASK-001 (Users table)
    │
    ├──[FS]──→ TASK-003 (Registration handler)
    │              │
    │              └──[FS]──→ TASK-005 (Registration tests)
    │
    └──[FS]──→ TASK-004 (Login handler)
                   │
                   └──[FS]──→ TASK-006 (Login tests)

TASK-002 (Password utils) ──[SS]──→ TASK-003 (Registration handler)
                          ──[SS]──→ TASK-004 (Login handler)
```
```

---

## Wave Analysis

Group tasks by dependency level for parallel execution.

### Structure

```markdown
## Wave Analysis

| Wave | Tasks | Can Run In Parallel | Dependencies |
|------|-------|---------------------|--------------|
| Wave 1 | TASK-001, TASK-002 | Yes | None |
| Wave 2 | TASK-003, TASK-004 | Yes | Wave 1 |
| Wave 3 | TASK-005, TASK-006 | Yes | Wave 2 |
| Wave 4 | TASK-007 | No | Wave 3 |
```

### Wave Visualization

```
Wave 1 (parallel)    Wave 2 (parallel)    Wave 3 (parallel)    Wave 4
┌──────────┐         ┌──────────┐         ┌──────────┐         ┌──────────┐
│ TASK-001 │─────────│ TASK-003 │─────────│ TASK-005 │─────────│ TASK-007 │
│ Users DB │         │ Register │         │ Reg Tests│         │ E2E Tests│
└──────────┘    ┌────│          │────┐    └──────────┘         └──────────┘
                │    └──────────┘    │
┌──────────┐    │                    │    ┌──────────┐
│ TASK-002 │────┤                    └────│ TASK-006 │
│ Password │    │    ┌──────────┐         │ Login Tst│
└──────────┘    └────│ TASK-004 │────────└──────────┘
                     │  Login   │
                     └──────────┘
```

---

## Phase Breakdown

Logical grouping of tasks.

### Structure

```markdown
## Phases

| Phase | Description | Tasks | Complexity | Dependencies |
|-------|-------------|-------|------------|--------------|
| 1 | Infrastructure | TASK-001, TASK-002 | Medium | None |
| 2 | Core Logic | TASK-003, TASK-004 | High | Phase 1 |
| 3 | Testing | TASK-005, TASK-006, TASK-007 | Medium | Phase 2 |
| 4 | Integration | TASK-008 | Low | Phase 3 |

**Total Token Estimate:** ~150k tokens
```

---

## Risk Assessment

### Structure

```markdown
## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| External API unavailable | Medium | High | Mock API for development |
| Database schema changes | Low | High | Run migrations in staging first |
| Performance issues | Medium | Medium | Load test before production |
| Security vulnerability | Low | High | Security review before launch |

### Contingency Buffer
- Add 20% buffer to complexity estimates
- Medium complexity → High complexity consideration
```

---

## Testing Plan

### Structure

```markdown
## Testing Plan

### Per-Phase Testing

| Phase | Tests | Pass Criteria |
|-------|-------|---------------|
| Phase 1 | DB migrations | Tables created, rollback works |
| Phase 2 | Unit tests | 80%+ coverage, all pass |
| Phase 3 | Integration tests | All API endpoints tested |
| Phase 4 | E2E tests | Critical flows pass |

### Test Coverage Targets

| Layer | Target | Actual |
|-------|--------|--------|
| Unit | 80% | TBD |
| Integration | 100% endpoints | TBD |
| E2E | Critical flows | TBD |
```

---

## Rollout Strategy

### Structure

```markdown
## Rollout Strategy

### Pre-deployment
- [ ] All tests pass in staging
- [ ] Database backup created
- [ ] Feature flag configured (disabled)
- [ ] Monitoring alerts set up

### Deployment Steps
1. Apply database migrations
2. Deploy code changes
3. Verify health checks
4. Enable feature flag (10% users)
5. Monitor error rates (30 minutes)
6. Gradual rollout (25% → 50% → 100%)

### Rollback Plan
1. Disable feature flag (immediate)
2. Revert code deployment (if needed)
3. Rollback migrations (if needed)

### Success Criteria
- Error rate < 0.1%
- Response time < 500ms p95
- No critical bugs in 24 hours
```

---

## Full Template

```markdown
# Implementation Plan: [Feature Name]

**Version:** 1.0
**Design:** `{FEATURE_DIR}/design.md`
**Status:** Draft | In Progress | Complete
**Author:** [Name]
**Date:** YYYY-MM-DD
**Project:** [project-name]

---

## Reference Documents

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Standards |
| Spec | `{FEATURE_DIR}/spec.md` | FR-X requirements |
| Design | `{FEATURE_DIR}/design.md` | AD-X decisions |
| Contracts | `.aidocs/contracts.md` | API patterns |

---

## Overview

[1-2 paragraphs summarizing implementation approach and key decisions]

**Token Estimate:** ~Xk tokens
**Critical Path:** High/Medium/Low complexity
**Waves:** [N waves]
**Total Tasks:** [M tasks]

---

## Prerequisites

### Infrastructure
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

### Environment
- [ ] [Prerequisite 1]

### Code Dependencies
- [ ] [Prerequisite 1]

---

## Dependency Graph

```
[Visual representation of task dependencies]
```

---

## Wave Analysis

| Wave | Tasks | Parallel | Dependencies | Tokens |
|------|-------|----------|--------------|--------|
| 1 | TASK-001, TASK-002 | Yes | None | ~Xk |
| 2 | TASK-003, TASK-004 | Yes | Wave 1 | ~Xk |
| 3 | TASK-005 | No | Wave 2 | ~Xk |

**Wave Diagram:**
```
[Visual wave diagram]
```

---

## Phases

| Phase | Description | Tasks | Complexity |
|-------|-------------|-------|------------|
| 1 | [Phase name] | TASK-001, TASK-002 | Medium |
| 2 | [Phase name] | TASK-003, TASK-004 | High |

---

## Phase 1: [Phase Name]

### TASK-001: [Task Title]

**Wave:** 1
**Complexity:** simple | normal | complex
**Context:** ~Xk tokens

**Description:**
[2-3 sentences]

**Traces to:** AD-001, FR-001

**Depends on:** None
**Blocks:** TASK-003, TASK-004

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Files:**
| Action | File | Description |
|--------|------|-------------|
| CREATE | `path/file.ts` | Description |

**Tests:**
- [ ] Unit: [description]
- [ ] Integration: [description]

---

## Critical Path

```
[Critical path visualization]
```

**Complexity:** High/Medium/Low
**Tasks on Critical Path:** TASK-001 → TASK-003 → TASK-005

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Strategy] |

**Contingency Buffer:** 20% added to estimates

---

## Testing Plan

### Per-Phase Testing
| Phase | Tests | Pass Criteria |
|-------|-------|---------------|
| 1 | [Tests] | [Criteria] |

### Coverage Targets
| Layer | Target |
|-------|--------|
| Unit | 80%+ |
| Integration | 100% endpoints |
| E2E | Critical flows |

---

## Rollout Strategy

### Pre-deployment
- [ ] [Checklist item]

### Deployment Steps
1. [Step 1]
2. [Step 2]

### Rollback Plan
1. [Rollback step]

### Success Criteria
- [Metric 1]
- [Metric 2]

---

## Recommended Skills & Methodologies

### Skills
| Skill | Tasks | Purpose |
|-------|-------|---------|
| faion-software-developer | TASK-001 to TASK-005 | Core implementation |
| faion-devops-engineer | TASK-006 | Deployment |

### Methodologies
| ID | Name | Relevant Tasks |
|----|------|----------------|
| M-DEV-XXX | [Name] | TASK-001, TASK-002 |

---

## Open Questions

- [ ] [Question to resolve]

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| YYYY-MM-DD | 1.0 | Initial plan |
```

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Planning task breakdown | haiku | Task decomposition from checklist |
| Estimating task complexity | sonnet | Comparative complexity assessment |
| Creating strategic roadmaps | opus | Long-term planning, dependency chains |

## Sources

- [Critical Path Method](https://www.projectmanager.com/guides/critical-path-method) - CPM in project management
- [PERT Charts](https://www.smartsheet.com/pert-charts) - Program Evaluation Review Technique
- [Risk Management Guide](https://www.pmi.org/learning/library/risk-analysis-project-management-7070) - PMI risk assessment
- [Dependency Types in PM](https://www.projectmanager.com/blog/task-dependencies) - FS, SS, FF, SF explained
- [Testing Pyramid](https://martinfowler.com/bliki/TestPyramid.html) - Martin Fowler's testing strategy
