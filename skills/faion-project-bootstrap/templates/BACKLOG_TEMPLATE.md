# Backlog: {project_name}

## Metadata

- **Version:** 1.0.0
- **Created:** {YYYY-MM-DD}
- **Status:** Draft
- **MVP Target:** {N} features

---

## MVP Overview

**Problem:** {problem statement - what pain point are we solving}

**Solution:** {solution summary - how the product solves it}

**Target User:** {user persona - who benefits from this}

**MVP Success Criteria:**
- [ ] {criterion 1 - specific, measurable}
- [ ] {criterion 2 - specific, measurable}
- [ ] {criterion 3 - specific, measurable}

---

## Feature Priority Matrix

| # | Feature | Directory | Priority | Complexity | Dependencies | Status |
|---|---------|-----------|----------|------------|--------------|--------|
| 00 | setup | `00-setup/` | P0-must | normal | none | todo |
| 01 | {feature-1} | `01-{name}/` | P0-must | {complexity} | 00-setup | todo |
| 02 | {feature-2} | `02-{name}/` | P0-must | {complexity} | {deps} | todo |
| 03 | {feature-3} | `03-{name}/` | P1-should | {complexity} | {deps} | todo |
| 04 | {feature-4} | `04-{name}/` | P2-could | {complexity} | {deps} | todo |

**Directory Structure:**
```
features/
├── 00-setup/           # TASK_000_*
├── 01-{feature-1}/     # TASK_001_*
├── 02-{feature-2}/     # TASK_002_*, TASK_003_* (if multiple tasks)
├── 03-{feature-3}/     # TASK_004_*
└── 04-{feature-4}/     # TASK_005_*
```

**Priority Legend:**
- **P0-must:** MVP не працює без цього
- **P1-should:** Значно покращує MVP
- **P2-could:** Nice to have

**Complexity Legend:**
- **simple:** 1-2 tasks, straightforward
- **normal:** 2-5 tasks, some decisions
- **complex:** > 5 tasks, significant architecture

---

## Feature Details

### 00. setup

**Directory:** `features/todo/00-setup/`
**Summary:** Initialize project with development infrastructure

**User Story:**
> As a developer,
> I want the project properly set up with linting, testing, and CI,
> So that I can focus on features without setup overhead.

**Requirements:**
- FR-00.1: Package manager initialized
- FR-00.2: Directory structure created
- FR-00.3: Linting and formatting configured
- FR-00.4: Test framework set up
- FR-00.5: CI pipeline created

**Acceptance Criteria:**
- [ ] `make lint` passes
- [ ] `make test` runs
- [ ] CI pipeline is green

**Dependencies:** none
**Complexity:** normal
**Priority:** P0-must

---

### 01. {feature-1-name}

**Directory:** `features/01-{feature-1-name}/`
**Summary:** {one sentence description}

**User Story:**
> As a {user type},
> I want {goal/desire},
> So that {benefit/value}.

**Requirements:**
- FR-01.1: {functional requirement}
- FR-01.2: {functional requirement}
- FR-01.3: {functional requirement}
- FR-01.4: {functional requirement}

**Acceptance Criteria:**
- [ ] AC-01.1: {testable criterion}
- [ ] AC-01.2: {testable criterion}
- [ ] AC-01.3: {testable criterion}

**Dependencies:** 00-setup
**Complexity:** {simple/normal/complex}
**Priority:** P0-must

---

### 02. {feature-2-name}

**Directory:** `features/02-{feature-2-name}/`
**Summary:** {one sentence description}

**User Story:**
> As a {user type},
> I want {goal/desire},
> So that {benefit/value}.

**Requirements:**
- FR-02.1: {functional requirement}
- FR-02.2: {functional requirement}
- FR-02.3: {functional requirement}

**Acceptance Criteria:**
- [ ] AC-02.1: {testable criterion}
- [ ] AC-02.2: {testable criterion}

**Dependencies:** {01-feature-1, or none}
**Complexity:** {simple/normal/complex}
**Priority:** P0-must

---

### 03. {feature-3-name}

**Directory:** `features/03-{feature-3-name}/`
**Summary:** {one sentence description}

**User Story:**
> As a {user type},
> I want {goal/desire},
> So that {benefit/value}.

**Requirements:**
- FR-03.1: {functional requirement}
- FR-03.2: {functional requirement}

**Acceptance Criteria:**
- [ ] AC-03.1: {testable criterion}
- [ ] AC-03.2: {testable criterion}

**Dependencies:** {deps with NN- prefix}
**Complexity:** {simple/normal/complex}
**Priority:** P1-should

---

{...add more features as needed, incrementing NN...}

---

## Recommended Implementation Order

Based on dependencies and priorities:

### Phase 1: Foundation
1. **00-setup** - Project infrastructure (TASK_000)

### Phase 2: Core MVP
2. **01-{feature-1}** - {why first after setup}
3. **02-{feature-2}** - {depends on 01 or parallel}

### Phase 3: Complete MVP
4. **03-{feature-3}** - {why this order}
5. **04-{feature-4}** - {final touches}

---

## Dependency Graph

```
00-setup ──────────────────────────────────────┐
    │                                          │
    ▼                                          │
01-feature-1 ───────────┐                      │
    │                   │                      │
    ▼                   ▼                      │
02-feature-2      03-feature-3                 │
    │                   │                      │
    └────────┬──────────┘                      │
             ▼                                 │
        04-feature-4 ──────────────────────────┘
```

---

## Out of Scope (Future)

These features are explicitly excluded from MVP:

| Feature | Why Later | When to Consider |
|---------|-----------|------------------|
| {future-feature-1} | {reason - MVP validation first} | After MVP launch |
| {future-feature-2} | {reason - complexity} | v2.0 |
| {future-feature-3} | {reason - not core} | Based on user feedback |

---

## Risks & Assumptions

### Assumptions
- {assumption 1}
- {assumption 2}
- {assumption 3}

### Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| {risk 1} | {high/medium/low} | {mitigation strategy} |
| {risk 2} | {high/medium/low} | {mitigation strategy} |

---

## Notes

- {important context}
- {technical constraints}
- {business constraints}

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| {YYYY-MM-DD} | 1.0.0 | Initial backlog created |
