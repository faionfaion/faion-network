# LLM Prompts for SDD Workflow

## Purpose

Copy-paste prompts for each SDD phase. These prompts help guide LLMs to produce spec-first outputs and reduce hallucinations.

---

## General Guidelines

### Before Any Prompt

Add this preamble to reduce hallucinations:

```
IMPORTANT: If you are unsure about something or the codebase context is missing,
ask for clarification rather than making up an answer. Do not fabricate
file names, API endpoints, or implementation details.
```

### Context Loading

Always provide:
1. Relevant spec/design sections
2. Existing code patterns (if any)
3. Constitution constraints
4. Previous related work

---

## Phase 0: Constitution Creation

### Prompt: Generate Constitution

```
I'm starting a new project. Help me create a constitution.md that defines
technical standards and constraints.

PROJECT CONTEXT:
- Project type: [Web app / API / CLI / Library]
- Team size: [Solo / Small team / Large team]
- Domain: [Description]
- Key constraints: [Budget, timeline, regulations]

REQUIREMENTS:
1. Recommend a technology stack appropriate for the context
2. Define coding standards (style, testing, commits)
3. Establish architecture principles
4. Set quality thresholds

OUTPUT FORMAT:
Use the standard constitution.md template structure with:
- Tech stack tables
- Coding standards checklist
- Architecture principles (numbered)
- Quality thresholds table

Do not include technologies you are unsure about - ask if clarification needed.
```

---

## Phase 1: Specification Writing

### Prompt: Write Spec from Idea

```
Help me write a specification for this feature/product.

IDEA:
[Describe the idea in 2-3 sentences]

CONTEXT:
- Target users: [Who will use this?]
- Existing system: [What already exists, if anything?]
- Constraints: [Any known limitations]

TASK:
1. Write a problem statement (who has this problem, what is it, why it matters)
2. Define 3-5 functional requirements (FR-X) with acceptance criteria (AC-X.X)
3. Identify non-functional requirements (performance, security, accessibility)
4. Define clear MVP scope
5. List what is explicitly OUT of scope

FORMAT:
Use Given-When-Then format for acceptance criteria.
Number all requirements (FR-1, FR-2, etc.).
Be specific - avoid vague terms like "fast" or "user-friendly" without metrics.

IMPORTANT: If any requirement is ambiguous or could be interpreted multiple ways,
ask for clarification before proceeding.
```

### Prompt: Review Spec for Completeness

```
Review this specification for completeness and clarity.

SPECIFICATION:
[Paste spec.md content]

CHECK FOR:
1. Ambiguous requirements - flag any that could be interpreted multiple ways
2. Missing acceptance criteria - every FR should have testable AC
3. Conflicting requirements - identify any contradictions
4. Scope gaps - requirements mentioned but not fully defined
5. Implicit assumptions - surface any assumptions being made
6. Testability - can each AC be verified?

OUTPUT:
- List of issues found (numbered)
- Suggested fixes for each issue
- Questions that need answering before design phase
- Confidence score (0-100%) that spec is ready for design
```

### Prompt: Convert User Stories to Requirements

```
Convert these user stories into formal functional requirements.

USER STORIES:
[Paste user stories]

FOR EACH STORY:
1. Extract the core requirement (FR-X format)
2. Write acceptance criteria (Given-When-Then)
3. Identify edge cases
4. Note any ambiguities that need clarification

OUTPUT FORMAT:
### FR-X: [Requirement Title]
[Description]

**Acceptance Criteria:**
- AC-X.1: Given [context], when [action], then [result]
- AC-X.2: Given [context], when [action], then [result]

**Edge Cases:**
- [Edge case 1]
- [Edge case 2]
```

---

## Phase 2: Design Document Creation

### Prompt: Generate Design from Spec

```
Create a design document based on this specification.

SPECIFICATION:
[Paste spec.md content]

CONSTITUTION CONSTRAINTS:
[Paste relevant sections from constitution.md]

EXISTING CODEBASE PATTERNS:
[Describe existing patterns, or "greenfield project"]

TASK:
1. Make architecture decisions (AD-X) for each major component
2. For each decision, explain context, decision, rationale, and alternatives considered
3. Define file/folder structure
4. Design data models with types
5. Specify API contracts (endpoints, request/response schemas)
6. Map requirements to design components (traceability)

FORMAT:
- Use AD-X numbering for decisions
- Include code blocks for schemas and structure
- Use tables for traceability mapping

IMPORTANT:
- Ensure every FR from spec maps to at least one design component
- Do not introduce features not in the spec
- If the spec is missing information needed for design, ask before proceeding
```

### Prompt: Design API Contract

```
Design an API contract for this requirement.

REQUIREMENT:
[Paste FR-X with acceptance criteria]

CONTEXT:
- API style: [REST / GraphQL / gRPC]
- Authentication: [How users authenticate]
- Existing patterns: [Describe existing API patterns in codebase]

DESIGN:
1. Endpoint path and method
2. Request schema (with types and validation)
3. Response schema (success and error cases)
4. Error codes with meanings
5. Example request/response

FORMAT:
```
[METHOD] /api/[path]

Request:
{json schema}

Response (200):
{json schema}

Errors:
| Code | Meaning |
|------|---------|
```

Ensure the contract supports all acceptance criteria for this requirement.
```

### Prompt: Review Design Document

```
Review this design document against the specification.

SPECIFICATION:
[Paste spec.md]

DESIGN:
[Paste design.md]

CHECK FOR:
1. Coverage - does design address all requirements?
2. Consistency - are architecture decisions coherent?
3. Feasibility - can this actually be built?
4. Completeness - are all interfaces defined?
5. Security - are there obvious security gaps?
6. Traceability - can we trace each FR to design components?

OUTPUT:
- Coverage matrix (FR-X → AD-X mapping)
- Issues found (numbered)
- Missing elements
- Suggested improvements
- Confidence score (0-100%) that design is ready for implementation planning
```

---

## Phase 3: Implementation Planning

### Prompt: Create Implementation Plan

```
Create an implementation plan from this design document.

DESIGN:
[Paste design.md]

CONSTRAINTS:
- Max task complexity: Each task must fit in ~100k token context
- Testing: [Testing requirements from constitution]
- Parallelization goal: Maximize independent tasks

TASK:
1. Decompose design into discrete tasks
2. Identify dependencies between tasks
3. Group into execution waves (independent tasks in same wave)
4. Assign complexity (Low/Medium/High)
5. Map tasks to requirements and design decisions
6. Define quality gates between waves

FORMAT:
Use task naming: TASK-XXX
Create dependency graph visualization
Use tables for wave organization

IMPORTANT:
- Every design component should have implementing tasks
- No task should require context beyond 100k tokens
- Identify critical path through dependencies
```

### Prompt: Optimize Task Parallelization

```
Optimize this implementation plan for maximum parallelization.

CURRENT PLAN:
[Paste implementation-plan.md]

ANALYZE:
1. Are there false dependencies? (tasks marked dependent that could be parallel)
2. Can any sequential tasks be restructured for parallelism?
3. Is the critical path as short as possible?
4. Are waves balanced? (similar effort across parallel tasks)

OUTPUT:
- Revised wave structure
- Removed false dependencies (with justification)
- New parallelization opportunities
- Expected speedup factor (1.X - 3.X)
```

---

## Phase 4: Task Execution

### Prompt: Execute Single Task

```
Execute this task following the specification and design.

TASK:
[Paste TASK-XXX.md content]

SPECIFICATION CONTEXT:
[Paste relevant FR-X and AC from spec]

DESIGN CONTEXT:
[Paste relevant AD-X and file structure from design]

EXISTING CODE PATTERNS:
[Paste similar existing code for pattern reference]

INSTRUCTIONS:
1. Follow existing code patterns exactly
2. Implement all acceptance criteria
3. Add appropriate tests
4. Update documentation if needed

QUALITY GATES:
- [ ] Code syntax valid
- [ ] Matches existing patterns
- [ ] All AC implemented
- [ ] Tests written
- [ ] No hardcoded secrets

OUTPUT:
For each file: specify CREATE or MODIFY, show complete code.
At the end: list which AC are satisfied.

IMPORTANT:
- Do not add features beyond what's specified
- If unclear about anything, ask before implementing
- Use exact file paths from design document
```

### Prompt: Self-Verification

```
Verify this implementation against the specification.

SPECIFICATION:
[Paste relevant FR-X and AC]

IMPLEMENTATION:
[Paste implemented code]

VERIFY:
1. For each acceptance criterion, confirm it is satisfied
2. Identify any AC that are NOT satisfied
3. Check for features added beyond spec (scope creep)
4. Verify error handling covers edge cases

OUTPUT FORMAT:
## Verification Results

### AC-X.1: [Criterion text]
- Status: [PASS / FAIL / PARTIAL]
- Evidence: [How it's satisfied or why it fails]

### AC-X.2: ...

## Summary
- Passing: X/Y criteria
- Issues found: [List]
- Recommendations: [If any fixes needed]
```

### Prompt: Fix Failed Quality Gate

```
The quality gate failed. Help fix the issue.

FAILURE:
[Paste error message, test failure, or lint error]

CONTEXT:
- Task: [TASK-XXX]
- Relevant code: [Paste relevant code]
- Spec requirement: [Paste AC being implemented]

INSTRUCTIONS:
1. Analyze the failure
2. Identify root cause
3. Propose fix
4. Verify fix satisfies the original requirement

IMPORTANT:
- Fix should be minimal - address the failure, don't refactor unrelated code
- Ensure fix doesn't break other functionality
- If fix requires changing the design, flag this before proceeding
```

---

## Phase 5: Validation & Learning

### Prompt: Feature Completion Review

```
Review this completed feature for final validation.

SPECIFICATION:
[Paste spec.md]

DESIGN:
[Paste design.md]

IMPLEMENTATION:
[List of completed tasks and their outputs]

TEST RESULTS:
[Paste test output]

VALIDATE:
1. All functional requirements implemented
2. All acceptance criteria passing
3. Non-functional requirements met
4. No scope creep (features beyond spec)
5. Documentation complete
6. Tests adequate

OUTPUT:
## Validation Report

### Requirements Coverage
| FR | Status | Evidence |
|----|--------|----------|

### Quality Assessment
- Test coverage: X%
- Code quality: [Assessment]
- Documentation: [Complete/Partial/Missing]

### Issues
[Any issues found]

### Recommendation
[APPROVE / APPROVE WITH NOTES / REJECT with reasons]
```

### Prompt: Extract Lessons Learned

```
Analyze this completed feature for patterns and lessons.

FEATURE CONTEXT:
[Brief description]

WHAT WENT WELL:
[List successes]

WHAT WENT WRONG:
[List issues encountered]

EXTRACT:
1. Reusable patterns discovered
2. Mistakes to avoid in future
3. Process improvements suggested
4. Documentation updates needed

OUTPUT FORMAT:
## Patterns Learned
- [Pattern 1]: [When to apply, how it helps]
- [Pattern 2]: ...

## Mistakes to Avoid
- [Mistake 1]: [What happened, how to prevent]
- [Mistake 2]: ...

## Process Improvements
- [Improvement 1]
- [Improvement 2]
```

---

## Utility Prompts

### Prompt: Hallucination Check

```
Before proceeding, verify your understanding.

WHAT YOU THINK YOU KNOW:
[State your assumptions about the codebase, requirements, or implementation]

PLEASE CONFIRM:
1. Which of these assumptions are you confident about (have evidence)?
2. Which are you uncertain about (need verification)?
3. What information would help clarify uncertainties?

I will provide clarification before you continue.
```

### Prompt: Context Dump

```
Here is context for the upcoming task.

PROJECT CONSTITUTION:
[Paste constitution.md]

CURRENT FEATURE SPEC:
[Paste spec.md]

CURRENT FEATURE DESIGN:
[Paste design.md]

EXISTING CODE PATTERNS:
[Paste relevant code examples]

RULES:
- Follow patterns exactly
- Do not add undocumented features
- Ask if anything is unclear
- Reference FR-X/AD-X in your responses

Confirm you have loaded this context before proceeding.
```

### Prompt: Break Down Large Request

```
This request seems too large for a single task. Help me decompose it.

REQUEST:
[Paste the large request]

ANALYZE:
1. What are the distinct components?
2. What are the dependencies between components?
3. How should this be sequenced?
4. What's the MVP subset if we need to reduce scope?

OUTPUT:
Suggested task breakdown with dependencies and wave assignment.
```

---

## Quick Reference: Prompt Principles

| Principle | Example |
|-----------|---------|
| Be specific | "Create REST API endpoint" not "make the backend work" |
| Provide context | Include spec, design, patterns |
| Request format | Specify output structure |
| Enable escape | "Ask if unclear" |
| Verify coverage | "Map to requirements" |
| Limit scope | "Only this task, no extras" |

---

*LLM Prompts | SDD Foundation | Version 1.0*
