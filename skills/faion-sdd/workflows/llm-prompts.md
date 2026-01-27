# LLM Prompts for SDD Workflows

Ready-to-use prompts for each workflow phase. Copy, adapt, and use with your preferred LLM.

---

## Prompt Design Principles

### 1. Context First

Always provide relevant context before the request:

```
CONTEXT:
- Project: [name]
- Tech stack: [stack]
- Current phase: [phase]

REQUEST:
[What you need]
```

### 2. Epistemic Humility

Include uncertainty handling:

```
If you are unsure about any context or making assumptions,
ask for clarification rather than guessing.
```

### 3. Structured Output

Request structured output for consistency:

```
OUTPUT FORMAT:
- Use markdown headers
- Include tables for lists
- Provide code in fenced blocks
```

### 4. Examples

Provide examples when possible:

```
EXAMPLE:
Input: [example input]
Output: [example output]
```

---

## Specification Workflow Prompts

### Brainstorming: Five Whys

```markdown
# Five Whys Analysis

CONTEXT:
User described: "[user's initial request]"

TASK:
Apply the Five Whys technique to uncover the root problem.

PROCESS:
1. State the surface-level problem
2. Ask "Why?" and provide the answer
3. Repeat 4 more times
4. Identify the root cause
5. Suggest how this changes our approach

OUTPUT FORMAT:
## Surface Problem
[Initial problem statement]

## Why Analysis
1. Why? → [Answer]
2. Why? → [Answer]
3. Why? → [Answer]
4. Why? → [Answer]
5. Why? → [Answer]

## Root Cause
[Underlying issue]

## Implication
[How this changes what we should build]
```

### Brainstorming: Alternatives

```markdown
# Alternative Approaches

CONTEXT:
Problem: [problem statement]
Constraints: [known constraints]

TASK:
Generate 3 alternative approaches to solve this problem.

OUTPUT FORMAT:
## Approach A: [Name]
- **Description:** [Brief description]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Effort:** [Low/Medium/High]
- **Risk:** [Low/Medium/High]

## Approach B: [Name]
...

## Approach C: [Name]
...

## Recommendation
[Which approach and why]
```

### Research: Codebase Analysis

```markdown
# Codebase Research

CONTEXT:
Feature: [feature name]
Problem: [problem to solve]
Codebase: [relevant directories/files to search]

TASK:
1. Search for similar implementations
2. Identify patterns to follow
3. Find reusable components
4. List integration points

SEARCH QUERIES:
- Glob("[pattern]") for file structure
- Grep("[pattern]") for code patterns

OUTPUT FORMAT:
## Similar Implementations
| File | Relevance | What to Reuse |
|------|-----------|---------------|

## Patterns Found
1. [Pattern 1]: Found in [location]
2. [Pattern 2]: Found in [location]

## Reusable Components
- [Component]: [How to reuse]

## Integration Points
- [Point 1]: [Description]
```

### Clarify: Edge Cases

```markdown
# Edge Case Exploration

CONTEXT:
Feature: [feature name]
Happy path: [main success scenario]

TASK:
Identify edge cases through questions (not assumptions).

CATEGORIES:
1. Data validation failures
2. Volume/scale limits
3. Timing/concurrency
4. Permission/auth issues
5. External dependencies
6. State transitions

OUTPUT FORMAT:
## Edge Cases to Explore

### Data Validation
- What if [input] is empty?
- What if [input] exceeds [limit]?
- What if [format] is invalid?

### Volume
- What if there are 0 items?
- What if there are 10,000 items?
- What if there are 1 million items?

### Timing
- What if two users do this simultaneously?
- What if the operation times out?
- What if it's retried?

### Permissions
- What if user lacks permission?
- What if token expires mid-operation?

### External
- What if [service] is unavailable?
- What if [API] returns unexpected response?

### State
- What if item already exists?
- What if item was deleted?
- What if item is in [intermediate state]?

Please answer these questions to complete the specification.
```

### Draft: Requirement Writing

```markdown
# Write Functional Requirement

CONTEXT:
User story: [As a X, I want Y, so that Z]
Acceptance criteria: [Given/When/Then]

TASK:
Write a formal functional requirement following SMART criteria.

OUTPUT FORMAT:
### FR-XXX: [Title]

**Requirement:** System SHALL [specific, testable action].

**Rationale:** [Why this is needed - traces to user value]

**Traces to:** US-XXX

**Priority:** Must | Should | Could

**Validation Rules:**
- [Rule 1 with specific values]
- [Rule 2 with specific values]

**Test Criteria:**
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
```

### Review: Spec Validation

```markdown
# Specification Review

SPEC CONTENT:
[Paste spec.md content]

TASK:
Review this specification for completeness, consistency, and LLM-readiness.

CHECKLIST:
1. Completeness
   - [ ] Problem statement with SMART criteria
   - [ ] User personas defined
   - [ ] User stories with INVEST criteria
   - [ ] Functional requirements (FR-XXX)
   - [ ] Non-functional requirements (NFR-XXX)
   - [ ] Acceptance criteria (Given-When-Then)
   - [ ] Out of scope documented
   - [ ] Assumptions listed

2. Consistency
   - [ ] No contradicting requirements
   - [ ] Priorities consistent with MVP scope
   - [ ] Terminology used consistently

3. Testability
   - [ ] Every requirement has measurable criterion
   - [ ] Acceptance criteria use specific values
   - [ ] Edge cases have defined behavior

4. LLM-Readiness
   - [ ] Specific examples included
   - [ ] Patterns referenced from codebase
   - [ ] Boundaries defined
   - [ ] No ambiguous language

OUTPUT FORMAT:
## Review Results

### Passed
- [x] [Item that passed]

### Failed
- [ ] [Item that failed]: [Reason]

### Recommendations
1. [Specific fix for issue 1]
2. [Specific fix for issue 2]

### Confidence Score
[X]% - [Ready to proceed | Needs revision]
```

---

## Design Workflow Prompts

### Architecture Decision

```markdown
# Architecture Decision

CONTEXT:
Feature: [feature name]
Requirement: [FR-XXX that needs decision]
Constraints: [from constitution.md]

TASK:
Make an architecture decision following ADR format.

OUTPUT FORMAT:
### AD-XXX: [Decision Title]

**Status:** Proposed

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

**Traces to:** FR-XXX
```

### File Structure Planning

```markdown
# File Structure Design

CONTEXT:
Feature: [feature name]
Architecture: [layered/hexagonal/clean]
Existing patterns: [from codebase research]

TASK:
Define files to create and modify.

OUTPUT FORMAT:
## Files to Change

### CREATE
| File | Purpose | Pattern Source |
|------|---------|----------------|
| `src/[path]` | [What it does] | `src/[similar]` |

### MODIFY
| File | Scope | Changes |
|------|-------|---------|
| `src/[path]` | [Affected area] | [What changes] |

### Dependencies
- [Library]: [Purpose]

### Integration Points
- [File/Service]: [How it connects]
```

### API Contract Definition

```markdown
# API Contract Design

CONTEXT:
Feature: [feature name]
Requirements: [FR-XXX list]
Existing API style: [from constitution]

TASK:
Define API contract for this feature.

OUTPUT FORMAT:
## API Contracts

### [METHOD] /api/v1/[resource]

**Description:** [What this endpoint does]

**Authentication:** Required | Optional | None

**Request:**
```json
{
  "field1": "string",
  "field2": 123
}
```

**Validation:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| field1 | string | Yes | max 255 chars |
| field2 | integer | No | min 0 |

**Response (2XX):**
```json
{
  "id": "uuid",
  "field1": "string",
  "createdAt": "ISO8601"
}
```

**Errors:**
| Code | Reason | Response Body |
|------|--------|---------------|
| 400 | Validation failed | `{"error": "field1 required"}` |
| 401 | Unauthorized | `{"error": "token expired"}` |
| 404 | Not found | `{"error": "resource not found"}` |
| 409 | Conflict | `{"error": "already exists"}` |
| 500 | Server error | `{"error": "internal error"}` |

**Traces to:** FR-XXX
```

### Design Review

```markdown
# Design Document Review

DESIGN CONTENT:
[Paste design.md content]

SPEC SUMMARY:
- FR-XXX list: [list]
- NFR-XXX list: [list]

TASK:
Review this design for spec coverage, consistency, and implementability.

CHECKLIST:
1. Coverage
   - [ ] All FR-XXX addressed by AD-XXX
   - [ ] All NFR-XXX have technical approach
   - [ ] API contracts for all endpoints
   - [ ] Data models complete

2. Consistency
   - [ ] Follows constitution patterns
   - [ ] No contradicting decisions
   - [ ] Terminology consistent with spec

3. Implementability
   - [ ] File structure clear
   - [ ] Patterns referenced exist
   - [ ] Dependencies available
   - [ ] Tests can be written

OUTPUT FORMAT:
## Review Results

### Coverage Matrix
| Requirement | Decision | Status |
|-------------|----------|--------|
| FR-001 | AD-001 | Covered |
| FR-002 | ??? | Missing |

### Issues Found
1. [Issue]: [Details]

### Recommendations
1. [Fix suggestion]

### Confidence
[X]% - [Proceed | Revise]
```

---

## Implementation Workflow Prompts

### Task Breakdown

```markdown
# Implementation Planning

CONTEXT:
Design: [design.md summary]
Files: [CREATE/MODIFY list]
100k token rule: Each task must fit within 100k context

TASK:
Break down implementation into tasks with dependencies.

OUTPUT FORMAT:
## Work Units

### Unit 1: [Name]
**Description:** [What this accomplishes]
**Files:**
| File | Action | Tokens Est. |
|------|--------|-------------|

**Total Tokens:** ~Xk
**Covers:** FR-XXX, AD-XXX
**Dependencies:** None | Unit X

### Unit 2: [Name]
...

## Dependency Graph
```
Unit 1 ──┐
         ├──> Unit 3
Unit 2 ──┘
```

## Waves
- Wave 1: Unit 1, Unit 2 (parallel)
- Wave 2: Unit 3 (depends on Wave 1)
```

### Task Creation

```markdown
# Create Task File

CONTEXT:
Work Unit: [description]
Feature: [feature-XXX]
Wave: [N]
Dependencies: [TASK-XXX list]

SPEC COVERAGE:
- FR-XXX: [requirement text]
- AC-XXX: [acceptance criteria]

DESIGN COVERAGE:
- AD-XXX: [decision text]

TASK:
Create a comprehensive task file.

OUTPUT FORMAT:
---
id: TASK-XXX
feature: feature-XXX
wave: N
status: todo
depends_on: []
tokens_estimate: ~Xk
complexity: Low | Medium | High
---

# TASK-XXX: [Title]

## SDD References
| Document | Path |
|----------|------|
| Spec | .aidocs/[path]/spec.md |
| Design | .aidocs/[path]/design.md |

## Objective
[Clear statement of what this task accomplishes]

## Requirements Coverage
### FR-XXX: [Title]
[Full requirement text]

## Acceptance Criteria
### AC-XXX.1: [Scenario]
**Given:** [Context]
**When:** [Action]
**Then:** [Result]

## Files to Change
| Action | File | Scope |
|--------|------|-------|
| CREATE | [path] | [description] |

## Technical Approach
### Step 1: [Title]
[Details]

## Testing Requirements
- [ ] Unit tests for [X]
- [ ] Integration test for [Y]

## Dependencies
### Before This Task
- [What must be done first]

### Needed By
- [What depends on this]
```

### Code Generation

```markdown
# Implement Feature

CONTEXT:
Task: [TASK-XXX description]
Files to create/modify: [list]
Patterns to follow: [from codebase]

CONSTITUTION:
- Language: [language]
- Framework: [framework]
- Code style: [style guide]

SPEC REQUIREMENTS:
[Relevant FR-XXX]

DESIGN DECISIONS:
[Relevant AD-XXX]

TASK:
Implement the code following existing patterns.

CONSTRAINTS:
- Follow pattern from [reference file]
- Use [specific library] for [purpose]
- Include error handling for [cases]

OUTPUT FORMAT:
## Implementation

### [filename]
```[language]
[code]
```

### [test filename]
```[language]
[test code]
```

### Changes Summary
- [What was implemented]
- [Patterns followed]
- [Decisions made during implementation]
```

### Fix from Error

```markdown
# Fix Error

ERROR MESSAGE:
```
[paste error output]
```

CONTEXT:
File: [file with error]
Recent change: [what was changed]
Expected behavior: [what should happen]

TASK:
1. Analyze the error
2. Identify root cause
3. Provide fix

OUTPUT FORMAT:
## Error Analysis

### Type
[Syntax | Type | Runtime | Logic]

### Root Cause
[Why this error occurred]

### Fix
```[language]
[corrected code]
```

### Explanation
[Why this fix works]

### Prevention
[How to avoid this in future]
```

---

## Review Workflow Prompts

### Code Review

```markdown
# Code Review

CODE:
```[language]
[code to review]
```

CONTEXT:
Purpose: [what this code does]
Requirements: [FR-XXX it implements]
Patterns: [expected patterns]

TASK:
Review for correctness, security, performance, and maintainability.

OUTPUT FORMAT:
## Code Review

### Correctness
- [x] [What's correct]
- [ ] [Issue]: [Details]

### Security
- [x] [What's secure]
- [ ] [Issue]: [Details]

### Performance
- [x] [What's efficient]
- [ ] [Issue]: [Details]

### Maintainability
- [x] [What's maintainable]
- [ ] [Issue]: [Details]

### Suggestions
1. [Improvement suggestion]

### Overall
[Approve | Request Changes]
```

### Acceptance Testing

```markdown
# Acceptance Test

SCENARIO:
AC-XXX: [scenario name]

Given: [precondition]
When: [action]
Then: [expected result]

IMPLEMENTATION:
[Summary of what was built]

TASK:
Generate test steps to verify this acceptance criterion.

OUTPUT FORMAT:
## Acceptance Test: AC-XXX

### Prerequisites
1. [Setup step]

### Test Steps
1. [Step 1]
   - Expected: [result]
2. [Step 2]
   - Expected: [result]
3. [Step 3]
   - Expected: [result]

### Verification
- [ ] [Check 1]
- [ ] [Check 2]

### Evidence Required
- Screenshot of [what]
- Log showing [what]
```

### Pattern Extraction

```markdown
# Extract Pattern

COMPLETED WORK:
Task: [TASK-XXX]
Feature: [feature description]
Outcome: [success/failure]

TASK:
Analyze and extract reusable patterns.

OUTPUT FORMAT:
## Pattern Learned

### Pattern: [Name]

**ID:** PAT-XXX

**Context:**
[When to use this pattern]

**Problem:**
[What problem it solves]

**Solution:**
[The approach that worked]

**Example:**
```[language]
[Example code]
```

**Benefits:**
- [Benefit 1]
- [Benefit 2]

**Trade-offs:**
- [Trade-off 1]

**Evidence:**
- Used in: [task/feature]
- Result: [outcome]
- Metrics: [if applicable]
```

### Mistake Analysis

```markdown
# Analyze Mistake

ERROR:
[What went wrong]

CONTEXT:
Task: [TASK-XXX]
Expected: [what should have happened]
Actual: [what happened]

TASK:
Perform root cause analysis and prevention planning.

OUTPUT FORMAT:
## Mistake Record

### Error
[What went wrong]

### Timeline
1. [Event 1]
2. [Event 2]
3. [Error occurred]

### Root Cause Analysis (5 Whys)
1. Why? → [Answer]
2. Why? → [Answer]
3. Why? → [Answer]
4. Why? → [Answer]
5. Why? → [Root cause]

### Impact
- [What was affected]
- [Severity]

### Prevention
- [Process change]
- [Check to add]
- [Tool to use]

### Recovery
[How to fix if it happens again]

### Checklist Addition
- [ ] [New item to add to checklist]
```

---

## Multi-Model Prompts

### Cross-Model Validation

```markdown
# Cross-Model Validation Request

CODE/DECISION:
[Content to validate]

CONTEXT:
[Relevant background]

PREVIOUS REVIEWS:
Model A said: [summary]
Model B said: [summary]

TASK:
Provide independent review and highlight:
1. Points of agreement
2. Points of disagreement
3. New issues not previously identified

OUTPUT FORMAT:
## Independent Review

### My Assessment
[Your analysis]

### Agreement with Previous Reviews
- [Point of agreement]

### Disagreement
- [Point of disagreement]: [My reasoning]

### New Findings
- [Issue not previously identified]

### Synthesis Recommendation
[What to do with conflicting opinions]
```

---

## Context Templates

### Session Context

```markdown
# Session Context

## Project
- Name: [project]
- Repository: [path]
- Tech stack: [stack]

## Current Work
- Feature: [feature-XXX]
- Phase: [spec/design/implement/review]
- Task: [TASK-XXX if applicable]

## SDD Documents
- Constitution: [path]
- Spec: [path]
- Design: [path]

## Session State
- Last action: [what was done]
- Next action: [what to do]
- Blockers: [any blockers]

## Memory Reference
- Relevant patterns: [PAT-XXX]
- Known mistakes: [ERR-XXX]
```

### Full Task Context

```markdown
# Task Execution Context

## Task
[Paste TASK-XXX.md content]

## Spec Extract
[Relevant FR-XXX and AC-XXX from spec.md]

## Design Extract
[Relevant AD-XXX and file structure from design.md]

## Constitution Extract
[Relevant standards from constitution.md]

## Existing Patterns
[Code patterns from codebase to follow]

## Previous Learnings
- Pattern: [PAT-XXX summary if relevant]
- Avoid: [ERR-XXX summary if relevant]

## Instructions
1. Read all context carefully
2. Follow existing patterns
3. If unsure, ask for clarification
4. Implement step by step
5. Include tests
6. Run quality checks
```

---

## Prompt Customization

### Adding Project-Specific Context

Replace placeholders with your project specifics:

```markdown
CONSTITUTION SNIPPET:
- Language: Python 3.11
- Framework: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Testing: pytest
- Linting: ruff
- Types: mypy strict

CODE STYLE:
- Follow PEP 8
- Use type hints everywhere
- Docstrings for public functions
- 100 char line limit
```

### Creating Reusable Prompt Libraries

Save commonly used prompts in `.claude/prompts/`:

```
.claude/prompts/
├── spec/
│   ├── five-whys.md
│   ├── alternatives.md
│   └── edge-cases.md
├── design/
│   ├── adr.md
│   └── api-contract.md
├── implement/
│   ├── task-creation.md
│   └── code-gen.md
└── review/
    ├── code-review.md
    └── pattern-extraction.md
```

---

*LLM Prompts | SDD Workflows | v1.0.0*
