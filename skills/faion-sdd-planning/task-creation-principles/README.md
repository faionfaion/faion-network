# Task Creation Principles

## Problem

Implementation plans fail when:
- Task granularity is wrong (too big or too small)
- Tasks lack context for AI/human execution
- No traceability to requirements or design decisions
- Progress is hard to track
- Acceptance criteria are vague

**The root cause:** Poor task decomposition and missing context.

---

## Integrated Best Practices

| Domain | Methodology | Key Principle |
|--------|-------------|---------------|
| **BA** | smart-requirements | SMART criteria for requirements |
| **BA** | acceptance-criteria | Given-When-Then acceptance criteria |
| **BA** | requirements-traceability | Requirements traceability (FR-X, AD-X links) |
| **PM** | wbs-decomposition | WBS decomposition (8-80 rule, 100% rule) |
| **PdM** | backlog-management | INVEST principle for task quality |
| **SDD** | writing-specifications | Spec → Task traceability |
| **SDD** | design-doc-structure | Design → Task traceability |

---

## Task Decomposition Principles

### 1. Right Size (PM Framework 8-80 Rule Adapted)

| Complexity | Effort | Tokens | Description |
|------------|--------|--------|-------------|
| **simple** | 1-2h | <30k | Single file, clear pattern |
| **normal** | 2-3h | 30-60k | Multiple files, some decisions |
| **complex** | 3-4h | 60-100k | Architecture decisions, research needed |

**Maximum:** 4 hours / 100k tokens per task (single work session)

**Too big:** "Implement authentication" (multiple days)
**Too small:** "Add import statement" (minutes)
**Right size:** "Create password hashing utilities" (2-3 hours)

### 2. INVEST Principle (from backlog-management)

Each task must be:

| Criterion | Question | Example |
|-----------|----------|---------|
| **Independent** | Can be done without other tasks? | ✅ Password utils (no deps) |
| **Negotiable** | Details can be refined? | ✅ Algorithm choice negotiable |
| **Valuable** | Clear user/business value? | ✅ "Enables secure login" |
| **Estimable** | Can estimate effort? | ✅ "2-3 hours" |
| **Small** | Fits in 1-4 hours? | ✅ Not "build auth system" |
| **Testable** | Clear acceptance criteria? | ✅ Given-When-Then defined |

### 3. Clear Boundaries

Each task must define:
- **Input:** What exists before (files, data, dependencies)
- **Output:** What exists after (files created/modified, features)
- **Success criteria:** How to verify completion (tests, AC)

### 4. SMART Criteria (from smart-requirements)

| Criterion | Application |
|-----------|-------------|
| **Specific** | Only one interpretation of task |
| **Measurable** | Can verify completion objectively |
| **Achievable** | Technically feasible with given context |
| **Relevant** | Traces to business need (FR-X) |
| **Time-bound** | Effort estimate provided |

---

## Traceability (from requirements-traceability)

Every task must link to:

```
TASK → FR-X (spec.md) → AD-X (design.md)
```

| Link Type | What It Answers |
|-----------|-----------------|
| **FR-X** | WHY this task exists (user need) |
| **AD-X** | HOW to implement (architecture decision) |
| **NFR-X** | Constraints (performance, security) |

**Template:**
```markdown
## Requirements Coverage
### FR-2: User can log in with email/password
Full text of requirement from spec.md

## Architecture Decisions
### AD-1: JWT for authentication
Full text of decision from design.md
```

---

## Acceptance Criteria (from acceptance-criteria)

Use Given-When-Then (BDD) format:

```markdown
## Acceptance Criteria

**AC-1: Successful login**
- Given: registered user with valid credentials
- When: user submits login form
- Then: JWT token returned, user redirected to dashboard

**AC-2: Invalid password**
- Given: registered user with wrong password
- When: user submits login form
- Then: error message "Invalid credentials" displayed
```

**Coverage checklist:**
- [ ] Happy path (success scenario)
- [ ] Alternative paths (valid variations)
- [ ] Boundary conditions (limits, edge cases)
- [ ] Error handling (invalid inputs, failures)
- [ ] Security (unauthorized access)
- [ ] Performance (if NFR applies)

---

## Task States

```
BACKLOG → TODO → IN_PROGRESS → DONE
                      ↓
                  BLOCKED
```

| State | Meaning | Action |
|-------|---------|--------|
| BACKLOG | Future work, not prioritized | Grooming needed |
| TODO | Ready to start, deps met | Can pick up |
| IN_PROGRESS | Being worked on | Single assignee |
| BLOCKED | Cannot proceed | Document blocker |
| DONE | Completed, verified | Move to done/ |

---

## Quality Checklist

### Before Creating Task
- [ ] Implementation plan reviewed (writing-implementation-plans)
- [ ] Design decisions (AD-X) understood
- [ ] Requirements (FR-X) mapped

### Task Definition
- [ ] INVEST criteria met
- [ ] SMART criteria met
- [ ] Complexity/effort assigned
- [ ] SDD references included
- [ ] Recommended skills listed

### Acceptance Criteria
- [ ] Given-When-Then format
- [ ] Happy path covered
- [ ] Error cases covered
- [ ] Boundary conditions covered
- [ ] Testable (not vague)

### Context
- [ ] Related files identified
- [ ] Code patterns documented
- [ ] Token estimate <100k
- [ ] Risks pre-identified

### Traceability
- [ ] Links to FR-X (spec)
- [ ] Links to AD-X (design)
- [ ] Links to NFR-X (if applicable)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Tasks too large | Break down until < 4 hours |
| No traceability | Add FR-X, AD-X links |
| Vague acceptance criteria | Use Given-When-Then |
| No context for AI | Add SDD References section |
| Missing skills recommendation | Add Recommended Skills |
| No risk assessment | Add Risks & Mitigations |
| Forgetting tests | Include testing in AC |

---

## Sources

- [INVEST User Stories](https://agileforall.com/new-to-agile-invest-in-good-user-stories/) - User story quality criteria
- [SMART Tasks](https://www.mindtools.com/pages/article/smart-goals.htm) - Task goal-setting
- [WBS Practice Standard](https://www.pmi.org/pmbok-guide-standards/framework/practice-standard-wbs) - PMI WBS guide
- [Task Dependencies Guide](https://www.smartsheet.com/understanding-task-dependencies-project-management) - Dependency types
- [Behavior-Driven Development](https://cucumber.io/docs/bdd/) - Acceptance criteria format
