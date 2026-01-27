# Specification Workflow

Step-by-step workflow for writing specifications with LLM assistance.

---

## Overview

The specification workflow transforms a vague idea into a structured, testable spec.md that LLM agents can execute without clarification.

```
IDEA -> BRAINSTORM -> RESEARCH -> CLARIFY -> DRAFT -> REVIEW -> SAVE
  |         |            |           |          |        |        |
 Input   Socratic    Codebase    Edge      Section   Quality   spec.md
         dialogue     search     cases    by section   gate
```

---

## Prerequisites

| Requirement | Status Check |
|-------------|--------------|
| Problem statement exists | "What problem are we solving?" |
| Stakeholder identified | "Who has this problem?" |
| Constitution exists | `.aidocs/constitution.md` present |
| Feature folder created | `.aidocs/backlog/feature-XXX-name/` |

---

## Phase 1: Brainstorming

### Purpose

Surface the real problem through Socratic dialogue. Users often describe solutions, not problems.

### Entry State

```
INPUT: Vague idea or feature request
STATE: brainstorming
CONFIDENCE: 0-30%
```

### Workflow Steps

```
1. Ask "What problem are you trying to solve?"
   |
   v
2. Apply Five Whys
   |
   +---> "Why is this a problem?"
   +---> "Why does this happen?"
   +---> "Why does that matter?"
   |
   v
3. Identify real need (often different from stated request)
   |
   v
4. Generate alternatives
   |
   +---> Option A (approach 1)
   +---> Option B (approach 2)
   +---> Option C (approach 3)
   |
   v
5. User selects direction
   |
   v
6. Challenge assumptions
   |
   +---> "Is this needed for v1?"
   +---> "What if we DON'T do this?"
   +---> "What exists already?"
```

### Five Whys Example

```
User: "We need an export feature"
    |
    v
Why? "Managers ask for reports"
    |
    v
Why? "They can't access the dashboard"
    |
    v
Why? "They don't have accounts"
    |
    v
Why? "Account creation is complex"
    |
    v
REAL PROBLEM: Access/permissions UX, not export feature
```

### Alternatives Template

```markdown
**Approach A:** [Description]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Effort: [Low/Medium/High]

**Approach B:** [Description]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Effort: [Low/Medium/High]

Which direction feels right?
```

### Exit Criteria

- [ ] Real problem identified (not just stated problem)
- [ ] At least 2 alternatives considered
- [ ] Direction chosen
- [ ] Assumptions challenged

### Exit State

```
OUTPUT: Problem statement, chosen direction
STATE: research
CONFIDENCE: 30-50%
```

---

## Phase 2: Research

### Purpose

Understand existing codebase patterns and constraints before defining requirements.

### Entry State

```
INPUT: Problem statement, chosen direction
STATE: research
CONFIDENCE: 30-50%
```

### Workflow Steps

```
1. Search for similar features
   |
   +---> Glob("**/spec.md")
   +---> Grep("feature.*similar")
   |
   v
2. Search for related code
   |
   +---> Glob("**/{domain}/**")
   +---> Grep("class.*{concept}")
   |
   v
3. Read constitution constraints
   |
   +---> Read(.aidocs/constitution.md)
   |
   v
4. Identify reusable patterns
   |
   v
5. Present findings to user
   |
   +---> "Found existing X in Y. Does this affect approach?"
   +---> "Pattern Z is used for similar features. Follow it?"
```

### Research Queries

| What to Find | How to Search |
|--------------|---------------|
| Similar specs | `Glob("**/.aidocs/**/spec.md")` |
| Related models | `Grep("class.*Model")` in domain folder |
| Existing services | `Glob("**/services/*.py")` |
| API patterns | `Grep("@router.*{endpoint}")` |
| Test patterns | `Glob("**/test_*.py")` |

### Findings Report Template

```markdown
## Codebase Research Findings

### Existing Similar Features
- [Feature X] in [location]: [relevance]

### Patterns to Follow
- [Pattern description] from [source file]

### Constraints Found
- [Constraint from constitution]

### Reusable Components
- [Component] - can be extended for this feature

### Questions Raised
- Does [finding] change our approach?
```

### Exit Criteria

- [ ] Codebase searched for similar implementations
- [ ] Constitution constraints identified
- [ ] Patterns to follow documented
- [ ] User informed of findings

### Exit State

```
OUTPUT: Research findings, patterns
STATE: clarify
CONFIDENCE: 50-70%
```

---

## Phase 3: Clarify

### Purpose

Define detailed requirements through user story workshops and edge case exploration.

### Entry State

```
INPUT: Problem statement, research findings
STATE: clarify
CONFIDENCE: 50-70%
```

### Workflow Steps

```
1. User Story Workshop
   |
   +---> "As [role], I want [goal], so that [benefit]"
   |     |
   |     +---> "How often will this happen?"
   |     +---> "What happens if you CAN'T do this?"
   |     +---> "What's the minimum viable version?"
   |
   v
2. Edge Cases through Questions (NOT assumptions)
   |
   +---> "What if data is invalid?"
   +---> "What if there are 10,000 records?"
   +---> "What if the service is unavailable?"
   +---> "What if the user cancels mid-process?"
   |
   v
3. Acceptance Criteria Definition
   |
   +---> Happy path scenarios
   +---> Error scenarios
   +---> Boundary conditions
   |
   v
4. Scope Boundaries
   |
   +---> "What is explicitly OUT of scope?"
   +---> "What can wait for v2?"
```

### User Story Format

```markdown
### US-XXX: [Title] (MVP/POST-MVP)

**As a** [specific persona]
**I want to** [specific action]
**So that** [specific benefit]

**Frequency:** [How often?]
**Priority:** Must/Should/Could
**Complexity:** Low/Medium/High

**Acceptance Criteria:** AC-XXX
```

### Edge Cases Checklist

| Category | Questions to Ask |
|----------|------------------|
| Data validation | What if empty? Invalid format? Too long? |
| Volumes | 1 item? 1000 items? 1 million items? |
| Timing | Simultaneous requests? Timeout? Retry? |
| Permissions | Unauthorized? Wrong role? Expired token? |
| State | Already exists? Deleted? Archived? |
| External | API down? Rate limited? Changed? |

### Acceptance Criteria Format

```markdown
### AC-XXX: [Scenario Name]

**Scenario:** [Brief description]

**Given:** [Initial context]
**And:** [Additional context]
**When:** [Action taken]
**And:** [Additional action]
**Then:** [Expected outcome]
**And:** [Additional outcome]
```

### Exit Criteria

- [ ] All user stories defined with INVEST criteria
- [ ] Edge cases explored through questions
- [ ] Acceptance criteria for happy path
- [ ] Acceptance criteria for error cases
- [ ] Out of scope explicitly defined

### Exit State

```
OUTPUT: User stories, acceptance criteria, scope
STATE: draft
CONFIDENCE: 70-85%
```

---

## Phase 4: Draft

### Purpose

Write spec.md section by section with validation after each section.

### Entry State

```
INPUT: User stories, acceptance criteria, scope
STATE: draft
CONFIDENCE: 70-85%
```

### Workflow Steps

```
1. Draft Problem Statement
   |
   +---> Write section
   +---> Ask: "Is this problem statement accurate?"
   +---> Iterate if needed
   |
   v
2. Draft User Stories with AC
   |
   +---> Write section
   +---> Ask: "Are these stories complete?"
   +---> Iterate if needed
   |
   v
3. Draft Functional Requirements
   |
   +---> Write FR-XXX list
   +---> Ask: "Anything redundant or missing?"
   +---> Iterate if needed
   |
   v
4. Draft Non-Functional Requirements
   |
   +---> Write NFR-XXX list
   +---> Ask: "Performance/security/scalability covered?"
   +---> Iterate if needed
   |
   v
5. Draft Out of Scope
   |
   +---> Write exclusions
   +---> Ask: "Agree with these boundaries?"
   +---> Iterate if needed
   |
   v
6. Compile complete spec.md
```

### Section Templates

#### Problem Statement

```markdown
## Problem Statement

| Field | Value |
|-------|-------|
| **Who** | [Specific persona] |
| **Problem** | [What they cannot do] |
| **Impact** | [Business/user impact] |
| **Solution** | [High-level approach] |
| **Success Metric** | [How we measure] |
```

#### Functional Requirements

```markdown
## Functional Requirements

### FR-001: [Title]

**Requirement:** System SHALL [specific, testable action].

**Rationale:** [Why this is needed]

**Traces to:** US-XXX

**Priority:** Must/Should/Could

**Validation:**
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
```

### Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Large blocks without validation | User loses context | Show section, validate, proceed |
| Assumptions instead of questions | Wrong requirements | Always ask, never assume |
| Solution before problem | Building wrong thing | Define problem fully first |
| Ignoring "I don't know" | Gaps in spec | Document unknowns, plan spikes |

### Exit Criteria

- [ ] All sections drafted
- [ ] Each section validated with user
- [ ] No assumptions made without confirmation
- [ ] Spec compiles to valid markdown

### Exit State

```
OUTPUT: Complete spec.md draft
STATE: review
CONFIDENCE: 85-95%
```

---

## Phase 5: Review

### Purpose

Quality gate validation before saving the specification.

### Entry State

```
INPUT: Complete spec.md draft
STATE: review
CONFIDENCE: 85-95%
```

### Workflow Steps

```
1. Self-Review Checklist
   |
   +---> Problem clear (SMART)?
   +---> User stories specific (INVEST)?
   +---> Requirements testable?
   +---> Out of scope defined?
   +---> No contradictions?
   |
   v
2. Traceability Check
   |
   +---> Every FR traces to US?
   +---> Every AC traces to FR?
   +---> All priorities assigned?
   |
   v
3. LLM-Readiness Check
   |
   +---> Specific values in examples?
   +---> Boundaries explicitly defined?
   +---> No ambiguous terms?
   +---> Patterns referenced?
   |
   v
4. Agent Review (optional)
   |
   +---> Call faion-sdd-reviewer-agent (mode: spec)
   |
   v
5. User Final Approval
   |
   +---> Present complete spec
   +---> Ask: "Ready to approve?"
```

### Review Checklist

```markdown
## Spec Review Checklist

### Completeness
- [ ] Problem statement with SMART criteria
- [ ] User personas defined
- [ ] User stories with INVEST criteria
- [ ] Functional requirements (FR-XXX)
- [ ] Non-functional requirements (NFR-XXX)
- [ ] Acceptance criteria (Given-When-Then)
- [ ] Out of scope documented
- [ ] Assumptions listed

### Consistency
- [ ] No contradicting requirements
- [ ] Priorities consistent with MVP scope
- [ ] Terminology used consistently

### Testability
- [ ] Every requirement has measurable criterion
- [ ] Acceptance criteria use specific values
- [ ] Edge cases have defined behavior

### LLM-Readiness
- [ ] Specific examples included
- [ ] Patterns referenced from codebase
- [ ] Boundaries (Always/Ask First/Never) defined
- [ ] No ambiguous language
```

### Confidence Score Calculation

| Criterion | Weight | Score |
|-----------|--------|-------|
| Problem validated | 25% | 0-100 |
| Requirements complete | 25% | 0-100 |
| Acceptance criteria specific | 20% | 0-100 |
| No contradictions | 15% | 0-100 |
| Dependencies identified | 15% | 0-100 |

**Pass threshold:** 90%+

### Exit Criteria

- [ ] All checklist items passed
- [ ] Confidence score >= 90%
- [ ] User approval received

### Exit State

```
OUTPUT: Approved spec.md
STATE: save
CONFIDENCE: 90%+
```

---

## Phase 6: Save

### Purpose

Persist the specification and update project state.

### Entry State

```
INPUT: Approved spec.md
STATE: save
CONFIDENCE: 90%+
```

### Workflow Steps

```
1. Determine save location
   |
   +---> New feature: .aidocs/backlog/{NN}-{feature}/spec.md
   +---> Existing feature: Update existing spec.md
   |
   v
2. Add metadata header
   |
   +---> Add frontmatter (status, version, date)
   |
   v
3. Write file
   |
   v
4. Update session memory
   |
   +---> Record decisions made
   +---> Record patterns learned
   |
   v
5. Notify user
   |
   +---> "Specification saved to: [path]"
   +---> "Next step: Design workflow"
```

### File Location Rules

| Scenario | Location |
|----------|----------|
| New feature | `.aidocs/backlog/feature-{NNN}-{name}/spec.md` |
| Existing feature (update) | Same path, increment version |
| Standalone task | `.aidocs/backlog/TASK-{NNNN}-{name}.md` |

### Frontmatter Template

```yaml
---
id: feature-{NNN}
name: "{Feature Name}"
status: draft | approved
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: [human | AI-assisted]
---
```

### Exit State

```
OUTPUT: Saved spec.md with metadata
STATE: complete
NEXT: design-workflow
```

---

## Decision Points

### Decision Tree

```
START
  |
  v
Is problem clearly defined?
  |
  +--NO--> Return to Brainstorming
  |
  YES
  |
  v
Is codebase researched?
  |
  +--NO--> Return to Research
  |
  YES
  |
  v
Are edge cases explored?
  |
  +--NO--> Return to Clarify
  |
  YES
  |
  v
Is each section validated?
  |
  +--NO--> Return to Draft
  |
  YES
  |
  v
Does spec pass review checklist?
  |
  +--NO--> Return to relevant phase
  |
  YES
  |
  v
SAVE AND PROCEED
```

### Escalation Points

| Situation | Action |
|-----------|--------|
| User says "I don't know" | Document unknown, plan discovery spike |
| Conflicting requirements | Surface conflict, require resolution |
| Scope creep detected | Reference MVP, push to v2 |
| Technical constraint found | Add to assumptions, may need design input |

---

## Mode Variations

### Mode 1: Existing Project

```
1. Analyze existing codebase first
2. Present findings
3. Adapt spec to existing patterns
4. Reference constitution constraints
```

### Mode 2: New Project

```
1. Start with vision and mission
2. Technology choices through alternatives
3. Create constitution alongside spec
4. Define standards from scratch
```

### Mode 3: Quick Spec (15-Minute Waterfall)

```
1. 5 min: Problem + requirements (minimal)
2. 5 min: Key acceptance criteria
3. 5 min: Out of scope + assumptions
4. Skip detailed user personas/stories
```

---

## Related Workflows

| Workflow | Relationship |
|----------|--------------|
| [design-workflow.md](design-workflow.md) | Next phase after spec approval |
| [review-workflow.md](review-workflow.md) | Quality gate process |
| [llm-prompts.md](llm-prompts.md) | Prompts for each phase |

---

*Specification Workflow | SDD Workflows | v1.0.0*
