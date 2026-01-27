# SDD Workflow Checklist

## Purpose

Use this checklist to ensure completeness at each SDD phase. Check items sequentially; do not proceed to next phase until current phase is complete.

---

## Phase 0: Constitution

### Project Setup

- [ ] Repository initialized with version control
- [ ] `.aidocs/` folder structure created
- [ ] CLAUDE.md or rules file established

### Technology Decisions

- [ ] Frontend stack chosen and documented
- [ ] Backend stack chosen and documented
- [ ] Database technology selected
- [ ] Hosting/deployment target identified

### Standards Defined

- [ ] Coding style guide referenced or created
- [ ] Test coverage threshold set (e.g., 80%)
- [ ] Commit message format specified
- [ ] PR/review process documented

### Architecture Principles

- [ ] Key architectural patterns identified
- [ ] Quality attributes prioritized (performance, security, etc.)
- [ ] Constraints documented (budget, timeline, regulations)

**Output:** `constitution.md` committed

---

## Phase 1: Specification

### Problem Definition

- [ ] Problem statement written (who, what, why)
- [ ] Target users/personas identified
- [ ] Current alternatives analyzed
- [ ] Success criteria defined

### Functional Requirements

- [ ] All FR-X requirements listed
- [ ] Each FR has acceptance criteria
- [ ] Requirements use domain language (not tech jargon)
- [ ] Given-When-Then format for complex scenarios

### Non-Functional Requirements

- [ ] Performance requirements (response time, throughput)
- [ ] Security requirements (authentication, authorization)
- [ ] Scalability requirements (users, data volume)
- [ ] Accessibility requirements (WCAG level)

### Scope

- [ ] MVP scope clearly bounded
- [ ] Out-of-scope items explicitly listed
- [ ] MLP features identified for post-MVP
- [ ] Dependencies on external systems noted

### Validation

- [ ] Stakeholder review completed
- [ ] Ambiguous requirements clarified
- [ ] Conflicts resolved
- [ ] Confidence: 90%+ ready for design

**Output:** `spec.md` committed

---

## Phase 2: Design

### Architecture Decisions

- [ ] All major decisions documented as AD-X
- [ ] Each AD includes context, decision, rationale
- [ ] Alternatives considered are listed
- [ ] Consequences acknowledged

### System Structure

- [ ] Component/module boundaries defined
- [ ] File/folder structure planned
- [ ] Naming conventions established
- [ ] Dependency graph clear

### API Contracts

- [ ] All endpoints/operations listed
- [ ] Request/response schemas defined
- [ ] Error responses documented
- [ ] Authentication/authorization specified

### Data Models

- [ ] Entity relationships mapped
- [ ] Database schema designed
- [ ] Migrations strategy defined
- [ ] Data validation rules specified

### Integration Points

- [ ] External APIs identified
- [ ] Integration contracts documented
- [ ] Error handling for integrations planned
- [ ] Rate limits and quotas noted

### Validation

- [ ] Design covers all spec requirements
- [ ] Traceability: FR-X → AD-X mapping exists
- [ ] Technical feasibility confirmed
- [ ] Confidence: 90%+ ready for planning

**Output:** `design.md` committed

---

## Phase 3: Implementation Plan

### Task Decomposition

- [ ] All work broken into tasks
- [ ] Each task has clear definition of done
- [ ] Tasks reference FR-X and AD-X
- [ ] Token estimates assigned (Low/Medium/High or ~Xk)

### Dependencies

- [ ] Inter-task dependencies identified
- [ ] Dependency types noted (FS, SS, FF, SF)
- [ ] No circular dependencies
- [ ] Critical path identified

### Parallelization

- [ ] Independent tasks grouped into waves
- [ ] Wave execution order documented
- [ ] Parallel execution opportunities maximized
- [ ] Sequential bottlenecks minimized

### Quality Gates

- [ ] Gate checkpoints placed at wave boundaries
- [ ] L1-L6 gates assigned appropriately
- [ ] Test requirements per task specified
- [ ] Review points scheduled

### Validation

- [ ] All spec requirements have tasks
- [ ] All design decisions are implementable
- [ ] Confidence: 95%+ ready to execute

**Output:** `implementation-plan.md` committed

---

## Phase 4: Task Execution

### Per-Task Checklist

- [ ] Task moved to `in-progress/`
- [ ] Context loaded (spec, design, dependencies)
- [ ] Existing patterns consulted
- [ ] Implementation follows standards

### Quality Verification

- [ ] L1: Code syntax valid
- [ ] L2: Linting passes
- [ ] L3: Type checking passes
- [ ] L4: Unit tests written and pass
- [ ] L5: Integration tests pass (if applicable)
- [ ] L6: Acceptance criteria verified

### Documentation

- [ ] Code comments where needed
- [ ] API documentation updated
- [ ] README updated if necessary
- [ ] CHANGELOG entry added

### Completion

- [ ] Task moved to `done/`
- [ ] Summary written in task file
- [ ] Patterns learned documented
- [ ] Mistakes captured for future reference

---

## Phase 5: Validation & Delivery

### Final Verification

- [ ] All tasks completed
- [ ] All acceptance criteria met
- [ ] Full test suite passes
- [ ] No known critical bugs

### Deployment Readiness

- [ ] Build succeeds
- [ ] Environment configuration ready
- [ ] Deployment scripts tested
- [ ] Rollback plan exists

### Documentation Complete

- [ ] User documentation updated
- [ ] API documentation complete
- [ ] CHANGELOG updated
- [ ] Release notes drafted

### Post-Delivery

- [ ] Feature moved to `done/`
- [ ] Retrospective notes captured
- [ ] Metrics collection configured
- [ ] Feedback loop established

---

## Quick Reference: Confidence Thresholds

| Transition | Minimum Confidence |
|------------|-------------------|
| Idea → Spec | 70% |
| Spec → Design | 90% |
| Design → Plan | 90% |
| Plan → Execute | 95% |

---

## Quick Reference: Quality Gates

| Level | What It Validates |
|-------|------------------|
| L1 | Syntax validity |
| L2 | Linting compliance |
| L3 | Type correctness |
| L4 | Unit test passage |
| L5 | Integration test passage |
| L6 | Acceptance criteria met |

---

*Checklist | SDD Foundation | Version 1.0*
