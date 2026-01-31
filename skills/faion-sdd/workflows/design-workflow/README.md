# Design Workflow

Step-by-step workflow for writing design documents with LLM assistance.

---

## Overview

The design workflow transforms an approved spec.md into a technical design.md that defines HOW to build the feature.

```
READ-SPEC -> READ-CONSTITUTION -> RESEARCH -> DECISIONS -> APPROACH -> TESTING -> RISKS -> REVIEW -> SAVE
    |              |                 |            |            |          |         |        |        |
 Load FR-X     Load stack        Codebase     AD-X with    Files,     Test      Risk    Quality  design.md
               patterns           search      rationale    APIs      strategy   matrix    gate
```

---

## Prerequisites

| Requirement | Status Check |
|-------------|--------------|
| spec.md exists | `.aidocs/{status}/feature-XXX/spec.md` |
| spec.md approved | `status: approved` in frontmatter |
| constitution.md exists | `.aidocs/constitution.md` |
| contracts.md exists (API features) | `.aidocs/contracts.md` |

---

## Phase 1: Read Specification

### Purpose

Extract all requirements and acceptance criteria that the design must address.

### Entry State

```
INPUT: Approved spec.md path
STATE: read-spec
CONFIDENCE: 0%
```

### Workflow Steps

```
1. Load spec.md
   |
   v
2. Extract key elements:
   |
   +---> Problem Statement
   +---> User Stories (US-XXX)
   +---> Functional Requirements (FR-XXX)
   +---> Non-Functional Requirements (NFR-XXX)
   +---> Acceptance Criteria (AC-XXX)
   +---> Out of Scope
   +---> Assumptions
   |
   v
3. Create traceability placeholder
   |
   +---> FR-XXX -> AD-??? (to be filled)
   |
   v
4. Identify API requirements (if any)
```

### Extraction Template

```markdown
## Spec Summary

### Problem
[Extracted problem statement]

### Requirements to Address
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | [Summary] | Must |
| FR-002 | [Summary] | Should |

### Performance Constraints
| NFR | Constraint |
|-----|------------|
| NFR-001 | [Extracted constraint] |

### Key Acceptance Criteria
- AC-001: [Summary]
- AC-002: [Summary]
```

### Exit Criteria

- [ ] All FR-XXX extracted
- [ ] All NFR-XXX extracted
- [ ] API requirements identified
- [ ] Scope boundaries understood

### Exit State

```
OUTPUT: Extracted spec summary
STATE: read-constitution
CONFIDENCE: 20%
```

---

## Phase 2: Read Constitution

### Purpose

Load project standards and constraints that design must follow.

### Entry State

```
INPUT: Spec summary
STATE: read-constitution
CONFIDENCE: 20%
```

### Workflow Steps

```
1. Load constitution.md
   |
   v
2. Extract constraints:
   |
   +---> Tech Stack (languages, frameworks)
   +---> Architecture Patterns (layered, hexagonal, etc.)
   +---> Code Standards (naming, structure)
   +---> Testing Requirements (coverage, types)
   +---> API Conventions (REST, versioning)
   |
   v
3. Note any conflicts with spec
   |
   +---> If conflict: Raise to user for resolution
```

### Constitution Checklist

```markdown
## Constitution Constraints

### Tech Stack
- Backend: [language, framework]
- Frontend: [language, framework]
- Database: [type, version]

### Architecture
- Pattern: [layered/hexagonal/clean]
- API Style: [REST/GraphQL]
- Auth: [JWT/OAuth/etc.]

### Standards
- Naming: [conventions]
- Testing: [coverage %, types required]
- Commits: [format]
```

### Exit Criteria

- [ ] Tech stack constraints loaded
- [ ] Architecture patterns identified
- [ ] Code standards understood
- [ ] No unresolved conflicts

### Exit State

```
OUTPUT: Constitution constraints
STATE: research
CONFIDENCE: 35%
```

---

## Phase 3: Research Codebase

### Purpose

Find existing patterns, similar implementations, and integration points.

### Entry State

```
INPUT: Spec summary, constitution constraints
STATE: research
CONFIDENCE: 35%
```

### Workflow Steps

```
1. Search for similar implementations
   |
   +---> Glob("**/services/{domain}*.py")
   +---> Grep("class.*{concept}")
   |
   v
2. Search for related models
   |
   +---> Glob("**/models.py")
   +---> Grep("class.*Model.*{entity}")
   |
   v
3. Search for similar API endpoints
   |
   +---> Grep("@router\.(get|post)")
   +---> Find existing patterns
   |
   v
4. Search for test patterns
   |
   +---> Glob("**/test_*.py")
   +---> Find setup/teardown patterns
   |
   v
5. Identify reusable components
   |
   v
6. Determine integration points
```

### Research Queries by Type

| Finding | Search Strategy |
|---------|-----------------|
| Similar service | `Grep("class.*Service")` in services/ |
| Model patterns | Read existing models in domain |
| API patterns | Find similar endpoints |
| Error handling | Search for exception patterns |
| Validation | Find Pydantic/Zod schemas |
| Testing | Read similar test files |

### Findings Report

```markdown
## Codebase Research

### Similar Implementations
| File | Relevance | Pattern to Copy |
|------|-----------|-----------------|
| [path] | [High/Medium] | [What to reuse] |

### Integration Points
| Component | File | Purpose |
|-----------|------|---------|
| [Component] | [path] | [How it connects] |

### Patterns to Follow
- [Pattern 1] from [source]
- [Pattern 2] from [source]

### Dependencies
- [Existing module] - can be reused
- [External service] - needs integration

### Gaps
- No existing pattern for [X]
- Will need new approach for [Y]
```

### Exit Criteria

- [ ] Similar implementations found
- [ ] Patterns to follow identified
- [ ] Integration points mapped
- [ ] Dependencies documented

### Exit State

```
OUTPUT: Research findings
STATE: decisions
CONFIDENCE: 50%
```

---

## Phase 4: Architecture Decisions

### Purpose

Make and document key technical decisions with rationale.

### Entry State

```
INPUT: Spec, constitution, research findings
STATE: decisions
CONFIDENCE: 50%
```

### Workflow Steps

```
1. Identify decisions needed
   |
   +---> For each FR, what technical choice?
   +---> For each NFR, what approach?
   |
   v
2. For each decision:
   |
   +---> Define context (problem/constraint)
   +---> List alternatives (minimum 2)
   +---> Evaluate trade-offs
   +---> Choose option with rationale
   +---> Document consequences
   |
   v
3. Create traceability
   |
   +---> AD-XXX traces to FR-XXX
   |
   v
4. Review decisions with user
   |
   +---> Present key decisions
   +---> Get alignment
```

### Decision Template (ADR-Style)

```markdown
### AD-001: [Decision Title]

**Status:** Proposed | Accepted | Deprecated

**Context:**
[Background, constraints, why decision needed]

**Decision:**
[What was decided]

**Rationale:**
- [Reason 1]
- [Reason 2]

**Alternatives Considered:**

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| [Option A] | [+] | [-] | [Reason] |
| [Option B] | [+] | [-] | [Reason] |

**Consequences:**
- **Positive:** [Benefits]
- **Negative:** [Trade-offs]
- **Risks:** [What could go wrong]

**Traces to:** FR-XXX, NFR-XXX
```

### Y-Statement Format (Concise)

```
In the context of [use case],
facing [concern],
we decided for [option]
to achieve [quality],
accepting [downside].
```

### Common Decision Types

| Category | Decision Examples |
|----------|-------------------|
| Data | SQL vs NoSQL, ORM vs Raw |
| API | REST vs GraphQL, sync vs async |
| Auth | Session vs JWT, OAuth provider |
| Cache | Redis vs in-memory, TTL strategy |
| Queue | Celery vs RQ, sync vs async |
| Storage | S3 vs local, CDN strategy |

### Exit Criteria

- [ ] All key decisions documented as AD-XXX
- [ ] Each AD has alternatives considered
- [ ] Trade-offs explicitly stated
- [ ] User alignment on decisions

### Exit State

```
OUTPUT: Architecture decisions (AD-XXX)
STATE: approach
CONFIDENCE: 65%
```

---

## Phase 5: Define Technical Approach

### Purpose

Define components, data flow, file structure, and API contracts.

### Entry State

```
INPUT: Architecture decisions
STATE: approach
CONFIDENCE: 65%
```

### Workflow Steps

```
1. Define Components
   |
   +---> New components needed
   +---> Existing components to modify
   +---> Component interactions
   |
   v
2. Define Data Flow
   |
   +---> Request path
   +---> Data transformations
   +---> Validation points
   +---> Error handling points
   |
   v
3. Define File Structure
   |
   +---> CREATE: [new files with purpose]
   +---> MODIFY: [existing files with scope]
   |
   v
4. Define API Contracts (if applicable)
   |
   +---> Reference contracts.md OR
   +---> Define OpenAPI-style endpoints
   |
   v
5. Define Data Models
   |
   +---> Database schemas
   +---> TypeScript/Pydantic types
   +---> Migrations needed
```

### Component Diagram (Text)

```markdown
## Component Architecture

```
[External Client]
       |
       v
[API Gateway/Router]
       |
       v
[Handler/Controller]
       |
       +---> [Validator]
       |
       v
[Service Layer]
       |
       +---> [External Service]
       |
       v
[Repository/DAO]
       |
       v
[Database]
```
```

### File Structure Template

```markdown
## Files to Change

### CREATE
| File | Purpose | Pattern Source |
|------|---------|----------------|
| `src/features/{name}/service.py` | Business logic | `src/auth/service.py` |
| `src/features/{name}/models.py` | Data models | `src/auth/models.py` |
| `tests/test_{name}.py` | Unit tests | `tests/test_auth.py` |

### MODIFY
| File | Scope | Changes |
|------|-------|---------|
| `src/routes.py` | Add routes | Register new endpoints |
| `src/config.py` | Add config | Add feature flag |
```

### API Contract Template

```markdown
## API Contracts

> References: [contracts.md](../../contracts.md)

### POST /api/v1/{resource}

**Request:**
```json
{
  "field1": "string",
  "field2": 123
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "field1": "string",
  "createdAt": "ISO8601"
}
```

**Errors:**
| Code | Reason | Body |
|------|--------|------|
| 400 | Validation failed | `{"error": "field1 required"}` |
| 409 | Already exists | `{"error": "duplicate"}` |
| 500 | Server error | `{"error": "internal"}` |
```

### Exit Criteria

- [ ] Components and interactions defined
- [ ] File structure documented
- [ ] API contracts specified (if applicable)
- [ ] Data models defined

### Exit State

```
OUTPUT: Technical approach
STATE: testing
CONFIDENCE: 75%
```

---

## Phase 6: Define Testing Strategy

### Purpose

Plan test coverage based on constitution requirements.

### Entry State

```
INPUT: Technical approach
STATE: testing
CONFIDENCE: 75%
```

### Workflow Steps

```
1. Review constitution testing requirements
   |
   +---> Coverage threshold
   +---> Required test types
   |
   v
2. Define unit tests
   |
   +---> What to test in isolation
   +---> Mocking strategy
   |
   v
3. Define integration tests
   |
   +---> What flows to cover
   +---> Test data needed
   |
   v
4. Define E2E tests (if applicable)
   |
   +---> Critical user paths
   |
   v
5. Define test fixtures
   |
   +---> Data factories
   +---> Mocks/stubs
```

### Testing Strategy Template

```markdown
## Testing Strategy

### Unit Tests
| Component | Test Focus | Coverage Target |
|-----------|------------|-----------------|
| `{service}` | Business logic | 90% |
| `{validator}` | Validation rules | 100% |

### Integration Tests
| Flow | Description | Priority |
|------|-------------|----------|
| Happy path | [Description] | P0 |
| Error handling | [Description] | P1 |

### Test Data
- Factory: `{entity}Factory` for generating test data
- Fixtures: `conftest.py` for shared setup

### Mocking Strategy
| Dependency | Mock Type | Purpose |
|------------|-----------|---------|
| [External API] | Response mock | Avoid external calls |
| [Database] | In-memory | Speed |
```

### Exit Criteria

- [ ] Unit test scope defined
- [ ] Integration test flows identified
- [ ] Test data approach documented
- [ ] Mocking strategy clear

### Exit State

```
OUTPUT: Testing strategy
STATE: risks
CONFIDENCE: 80%
```

---

## Phase 7: Identify Risks

### Purpose

Document risks with impact assessment and mitigation strategies.

### Entry State

```
INPUT: Complete technical approach
STATE: risks
CONFIDENCE: 80%
```

### Workflow Steps

```
1. Brainstorm risks
   |
   +---> Technical risks
   +---> Integration risks
   +---> Performance risks
   +---> Security risks
   |
   v
2. Assess each risk
   |
   +---> Probability: High/Medium/Low
   +---> Impact: High/Medium/Low
   +---> Priority = Probability x Impact
   |
   v
3. Define mitigations
   |
   +---> Prevention strategy
   +---> Detection method
   +---> Recovery plan
```

### Risk Matrix Template

```markdown
## Risk Analysis

| ID | Risk | Probability | Impact | Priority | Mitigation |
|----|------|-------------|--------|----------|------------|
| R1 | [Description] | High | High | P0 | [Strategy] |
| R2 | [Description] | Medium | Medium | P1 | [Strategy] |

### Detailed Mitigations

#### R1: [Risk Title]
- **Prevention:** [How to prevent]
- **Detection:** [How to detect early]
- **Recovery:** [How to recover]
```

### Common Risk Categories

| Category | Examples |
|----------|----------|
| Technical | Wrong architecture, performance issues |
| Integration | External API changes, version conflicts |
| Security | Auth bypass, data exposure |
| Data | Migration failures, data loss |
| Dependencies | Library vulnerabilities, deprecation |

### Exit Criteria

- [ ] All significant risks identified
- [ ] Impact/probability assessed
- [ ] Mitigation strategies defined

### Exit State

```
OUTPUT: Risk analysis
STATE: review
CONFIDENCE: 85%
```

---

## Phase 8: Review

### Purpose

Quality gate validation before saving the design document.

### Entry State

```
INPUT: Complete design.md draft
STATE: review
CONFIDENCE: 85%
```

### Workflow Steps

```
1. Self-Review Checklist
   |
   +---> All FR-X covered by AD-X?
   +---> Constitution compliance?
   +---> File structure complete?
   +---> API contracts specified?
   |
   v
2. Traceability Verification
   |
   +---> FR -> AD mapping complete?
   +---> No orphan decisions?
   |
   v
3. LLM-Readiness Check
   |
   +---> Patterns explicitly referenced?
   +---> Type definitions included?
   +---> Examples provided?
   |
   v
4. Agent Review (optional)
   |
   +---> Call faion-sdd-reviewer-agent (mode: design)
   |
   v
5. User Review
   |
   +---> Present key decisions
   +---> Get approval
```

### Review Checklist

```markdown
## Design Review Checklist

### Coverage
- [ ] All FR-XXX addressed by AD-XXX
- [ ] All NFR-XXX have technical approach
- [ ] API contracts for all endpoints
- [ ] Data models complete

### Consistency
- [ ] Follows constitution patterns
- [ ] No contradicting decisions
- [ ] Terminology consistent with spec

### Implementability
- [ ] File structure clear
- [ ] Patterns referenced exist
- [ ] Dependencies available
- [ ] Tests can be written

### LLM-Readiness
- [ ] Code examples included
- [ ] Type definitions provided
- [ ] Pattern sources referenced
- [ ] No ambiguous instructions
```

### Exit Criteria

- [ ] All checklist items passed
- [ ] Confidence >= 90%
- [ ] User approval received

### Exit State

```
OUTPUT: Approved design.md
STATE: save
CONFIDENCE: 90%+
```

---

## Phase 9: Save

### Purpose

Persist the design document and update project state.

### Entry State

```
INPUT: Approved design.md
STATE: save
CONFIDENCE: 90%+
```

### Workflow Steps

```
1. Add metadata header
   |
   +---> Frontmatter with status, version
   |
   v
2. Write to feature folder
   |
   +---> Same folder as spec.md
   |
   v
3. Update session memory
   |
   +---> Record decisions
   |
   v
4. Notify user
   |
   +---> "Design saved to: [path]"
   +---> "Next step: Implementation Plan"
```

### Frontmatter Template

```yaml
---
id: design-{feature-NNN}
spec: feature-{NNN}
status: draft | approved
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: [human | AI-assisted]
---
```

### Exit State

```
OUTPUT: Saved design.md
STATE: complete
NEXT: implementation-workflow (impl-plan phase)
```

---

## Decision Points

### Decision Tree

```
START
  |
  v
Is spec.md approved?
  |
  +--NO--> Return to spec-workflow
  |
  YES
  |
  v
Is constitution loaded?
  |
  +--NO--> Create/load constitution
  |
  YES
  |
  v
Are all FR covered by AD?
  |
  +--NO--> Add missing decisions
  |
  YES
  |
  v
Is file structure complete?
  |
  +--NO--> Complete file list
  |
  YES
  |
  v
Does design pass review?
  |
  +--NO--> Address gaps
  |
  YES
  |
  v
SAVE AND PROCEED
```

### Conflict Resolution

| Conflict | Resolution |
|----------|------------|
| Spec vs Constitution | Constitution wins, update spec if needed |
| Pattern vs Requirement | Discuss with user, document deviation |
| Performance vs Simplicity | Refer to NFRs, use decision matrix |

---

## Related Workflows

| Workflow | Relationship |
|----------|--------------|
| [spec-workflow.md](spec-workflow.md) | Input to this workflow |
| [implementation-workflow.md](implementation-workflow.md) | Next phase |
| [review-workflow.md](review-workflow.md) | Quality gate process |
| [llm-prompts.md](llm-prompts.md) | Prompts for each phase |

---

*Design Workflow | SDD Workflows | v1.0.0*
