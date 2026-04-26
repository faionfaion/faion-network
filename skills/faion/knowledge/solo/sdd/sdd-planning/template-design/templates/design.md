# Design: {Feature Name}

**Version:** 1.0
**Status:** Draft | Review | Approved
**Author:** {Name}
**Date:** YYYY-MM-DD
**Spec:** {link to spec.md}

---

## Reference Documents

| Document | Path |
|----------|------|
| Specification | `spec.md` |
| Constitution | `.aidocs/constitution.md` |
| Contracts | `.aidocs/contracts.md` |

---

## Overview

{2-3 sentences: technical approach summary — write LAST after all other sections}

---

## Architecture Decisions

### AD-1: {Decision Name}

**Context:**
{Problem being solved and relevant context}

**Options:**
- **A: {Option}** — Pros: {benefits}. Cons: {drawbacks}.
- **B: {Option}** — Pros: {benefits}. Cons: {drawbacks}.

**Decision:** {Chosen solution}

**Rationale:** {Why this solution; which constraints drove the choice}

**Consequences:**
- Positive: {benefits}
- Negative: {trade-offs}
- Risks: {what could go wrong}

**Traces to:** FR-001, NFR-002

### AD-2: {Decision Name}
...

---

## Components

### Component 1: {Name}
- **Purpose:** {what it does}
- **Location:** {path}
- **Dependencies:** {what it uses}

---

## Data Flow

{Component A} → validate → {Component B} → process → {Component C} → persist

Error path: {Component A} → validation failure → return 400

---

## Data Models

### {Model Name}

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Primary key |
| {field} | {type} | {NOT NULL / UNIQUE / FK} | {description} |

---

## API Endpoints

Reference: `contracts.md` section {X}

| Method | Path | Description | FR |
|--------|------|-------------|-----|
| POST | /api/v1/{resource} | Create | FR-001 |
| GET | /api/v1/{resource}/{id} | Read | FR-002 |

---

## Files

| Action | File | Description | FR | AD |
|--------|------|-------------|----|----|
| CREATE | {path/to/file.py} | {what to create} | FR-001 | AD-1 |
| MODIFY | {path/to/file.py} | {what to modify} | FR-002 | AD-2 |
| CREATE | {path/to/test_file.py} | {tests for above} | FR-001 | - |

---

## Testing Strategy

### Unit Tests

| Component | Test File | Coverage Target |
|-----------|-----------|----------------|
| {component} | test_{component}.py | {target}% |

### Integration Tests

| Flow | Test File | Description |
|------|-----------|-------------|
| {flow} | test_{flow}_integration.py | {description} |

---

## Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| {risk} | High/Med/Low | High/Med/Low | {mitigation} |

---

## FR Coverage

| FR | AD | Files | Status |
|----|-----|-------|--------|
| FR-001 | AD-1 | models.py, services.py | Covered |
| FR-002 | AD-2 | views.py | Covered |
