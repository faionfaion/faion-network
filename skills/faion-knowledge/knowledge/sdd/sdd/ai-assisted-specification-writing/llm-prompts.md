# LLM Prompts for Specification Writing

> Effective prompts for AI-assisted specification creation, validation, and refinement.

## Prompt Categories

1. [Initial Specification Generation](#1-initial-specification-generation)
2. [Clarification and Discovery](#2-clarification-and-discovery)
3. [Requirements Extraction](#3-requirements-extraction)
4. [Acceptance Criteria Writing](#4-acceptance-criteria-writing)
5. [Edge Case Identification](#5-edge-case-identification)
6. [Specification Review](#6-specification-review)
7. [Technical Design](#7-technical-design)
8. [Implementation Planning](#8-implementation-planning)
9. [Refinement and Iteration](#9-refinement-and-iteration)

---

## 1. Initial Specification Generation

### Basic Feature Spec

```markdown
Generate a specification for [FEATURE_NAME].

**Context:**
- Product: [product description]
- Target users: [user personas]
- Existing system: [relevant existing features/constraints]
- Technical stack: [languages, frameworks, databases]

**Requirements:**
1. Generate functional requirements (FR-X format)
2. Identify edge cases and error scenarios
3. Write acceptance criteria (Given-When-Then)
4. List dependencies and assumptions
5. Flag potential risks

**Format:** Use the standard spec.md template with sections:
- Overview (problem, goals, non-goals)
- User stories
- Functional requirements
- Non-functional requirements
- Edge cases
- Dependencies
- Risks
```

### Detailed Spec with Questions First

```markdown
I need a specification for [FEATURE_NAME].

Before generating the spec, please:
1. Ask clarifying questions about unclear aspects
2. Identify any missing information you need
3. Suggest scope boundaries if not defined

**Initial context:**
[Provide what you know about the feature]

Once I've answered your questions, generate a comprehensive specification.
```

### Spec from Rough Notes

```markdown
Convert these rough notes into a formal specification:

---
[Paste rough notes, meeting minutes, or informal description]
---

**Instructions:**
1. Extract and structure all requirements mentioned
2. Identify implicit requirements not explicitly stated
3. Flag any contradictions or ambiguities
4. Organize into standard spec.md format
5. List questions that need clarification
```

---

## 2. Clarification and Discovery

### Discovery Questions

```markdown
I'm planning to build [FEATURE_NAME].

Act as a senior product manager and ask me the most important
clarifying questions to understand:
1. The core problem being solved
2. Target users and their needs
3. Success criteria and metrics
4. Technical constraints
5. Scope boundaries
6. Edge cases I might not have considered

Ask questions in batches of 5-7, prioritized by importance.
```

### Stakeholder Perspective

```markdown
For [FEATURE_NAME], help me think through different stakeholder perspectives:

1. **End User:** What would they expect? What frustrates them?
2. **Developer:** What technical challenges exist?
3. **QA:** What's hard to test? What breaks often?
4. **Security:** What vulnerabilities might exist?
5. **Support:** What questions will users ask?
6. **Business:** What metrics matter?

For each perspective, list:
- Key concerns
- Must-have requirements
- Potential risks
```

### Assumption Surfacing

```markdown
Review this feature description and list all implicit assumptions:

[Feature description]

For each assumption:
1. State the assumption explicitly
2. Rate its risk if wrong (High/Medium/Low)
3. Suggest how to validate it
4. Propose what to do if it's false
```

---

## 3. Requirements Extraction

### From User Stories to FRs

```markdown
Convert these user stories into formal functional requirements:

[User stories]

For each requirement:
1. Use FR-X numbering
2. Write in "The system shall..." format
3. Make it specific and testable
4. Link back to the originating user story
5. Identify any missing requirements implied by the stories
```

### NFR Generation

```markdown
For [FEATURE_NAME] with context:
- Expected users: [number]
- Data volume: [amount]
- Criticality: [high/medium/low]
- Industry: [industry]

Generate non-functional requirements covering:
1. Performance (latency, throughput)
2. Scalability (growth expectations)
3. Reliability (uptime, recovery)
4. Security (auth, data protection)
5. Compliance (GDPR, HIPAA, etc.)
6. Maintainability (logging, monitoring)

Use NFR-X format with measurable criteria.
```

### Requirement Decomposition

```markdown
This requirement is too large:

[Large requirement]

Break it down into smaller, implementable requirements:
1. Each sub-requirement should be independently testable
2. Identify dependencies between sub-requirements
3. Estimate relative complexity (Low/Medium/High)
4. Suggest implementation order
```

---

## 4. Acceptance Criteria Writing

### Given-When-Then Format

```markdown
Write acceptance criteria for:

**Requirement:** [requirement text]

**Instructions:**
1. Use Given-When-Then (Gherkin) format
2. Cover the happy path first
3. Include at least 2 error/edge case scenarios
4. Use concrete data examples, not placeholders
5. Make criteria independently verifiable

**Example format:**
Given [initial context/state]
When [action/trigger]
Then [expected outcome]
And [additional outcome]
```

### Comprehensive AC Set

```markdown
Generate complete acceptance criteria for [FEATURE_NAME].

For each user story/requirement, include:
1. **Happy path:** Normal successful flow
2. **Validation errors:** Invalid input handling
3. **Authorization:** Permission checks
4. **Edge cases:** Boundary conditions
5. **Error recovery:** System failure handling

Use concrete values:
- Instead of "valid email" → "user@example.com"
- Instead of "large file" → "file of 100MB"
- Instead of "many items" → "list of 1000 items"
```

### AC Review and Improvement

```markdown
Review these acceptance criteria for completeness and testability:

[Acceptance criteria]

Check for:
1. **Ambiguity:** Are there vague terms? (quickly, properly, correctly)
2. **Completeness:** Are all scenarios covered?
3. **Testability:** Can each criterion be verified?
4. **Independence:** Can each be tested in isolation?
5. **Data:** Are concrete examples provided?

Suggest improvements for any issues found.
```

---

## 5. Edge Case Identification

### Systematic Edge Cases

```markdown
Identify edge cases for [FEATURE_NAME]:

**Categories to explore:**
1. **Input boundaries:** Min, max, empty, null
2. **State transitions:** First use, expired, locked
3. **Concurrency:** Race conditions, conflicts
4. **Network:** Timeout, disconnect, slow connection
5. **Data:** Unicode, special characters, injection
6. **Permissions:** Unauthorized, role changes mid-session
7. **Time:** Timezones, DST, leap years
8. **Resources:** Quota exceeded, storage full

For each edge case:
- Describe the scenario
- State expected behavior
- Rate likelihood (Common/Rare)
- Rate impact (High/Medium/Low)
```

### Security-Focused Edge Cases

```markdown
Generate security-focused edge cases for [FEATURE_NAME]:

Consider:
1. **Authentication bypass:** Token manipulation, session hijacking
2. **Authorization escalation:** Accessing others' data
3. **Injection attacks:** SQL, XSS, command injection
4. **Data exposure:** Error messages revealing info
5. **Rate abuse:** Brute force, DoS
6. **Business logic:** Exploiting flow assumptions

Format:
| Threat | Attack Vector | Expected Defense | Test Method |
```

### Failure Mode Analysis

```markdown
For [FEATURE_NAME], analyze failure modes:

**Dependencies:**
[List services, APIs, databases this feature depends on]

For each dependency, describe:
1. What happens if it's unavailable?
2. What happens if it's slow (>5s response)?
3. What happens if it returns invalid data?
4. How should the system degrade gracefully?
5. What should users see?
6. How should it recover when dependency returns?
```

---

## 6. Specification Review

### Completeness Review

```markdown
Review this specification for completeness:

[Specification]

Check against this criteria:
- [ ] Problem statement is clear
- [ ] Goals and non-goals defined
- [ ] All user types identified
- [ ] Functional requirements complete (no implicit features)
- [ ] Non-functional requirements specified
- [ ] Edge cases documented
- [ ] All requirements have acceptance criteria
- [ ] Dependencies listed
- [ ] Assumptions stated
- [ ] Risks identified

Report:
1. Missing elements
2. Incomplete sections
3. Ambiguous requirements
4. Suggestions for improvement
```

### Conflict Detection

```markdown
Analyze this specification for conflicts and inconsistencies:

[Specification]

Look for:
1. Requirements that contradict each other
2. Requirements that conflict with stated constraints
3. Acceptance criteria that don't match requirements
4. Edge cases with undefined behavior
5. Assumptions that contradict requirements

For each conflict:
- Identify the conflicting items
- Explain the conflict
- Suggest resolution options
```

### Testability Review

```markdown
Review this specification for testability:

[Specification]

For each requirement/AC, assess:
1. Can it be verified automatically?
2. Can it be verified manually?
3. What test data is needed?
4. What test environment is needed?
5. What's the effort to test? (Low/Medium/High)

Flag any untestable requirements with suggestions to make them testable.
```

### Six-Area Checklist (for AI Agents)

```markdown
Review this specification against the AI agent checklist:

[Specification]

**Six Areas:**
1. **Commands:** Are build/test/run commands specified?
2. **Testing:** Are testing requirements clear?
3. **Project Structure:** Is file organization defined?
4. **Code Style:** Are conventions documented?
5. **Git Workflow:** Is branching/commit strategy clear?
6. **Boundaries:** Are non-goals explicitly stated?

For each area, rate coverage (Full/Partial/Missing) and suggest additions.
```

---

## 7. Technical Design

### Architecture from Spec

```markdown
Based on this specification, generate a technical design:

[Specification]

Include:
1. **System architecture:** Components and their relationships
2. **Data models:** Entities, fields, relationships
3. **API design:** Endpoints, request/response formats
4. **Integration points:** How this connects to existing systems
5. **Technology choices:** With rationale

Use existing stack: [your tech stack]
Follow patterns in: [link to existing code/patterns]
```

### ADR Generation

```markdown
Generate Architecture Decision Records for key decisions in this design:

[Design document]

For each significant decision:
1. **Title:** Short description
2. **Status:** Proposed/Accepted/Deprecated
3. **Context:** Why this decision is needed
4. **Decision:** What we decided
5. **Consequences:** Pros, cons, trade-offs
6. **Alternatives:** What else was considered, why rejected
```

### API Contract Design

```markdown
Design API contracts for [FEATURE_NAME]:

**Requirements:**
[Relevant requirements]

**Constraints:**
- RESTful / GraphQL
- Auth method: [JWT/API key/OAuth]
- Existing patterns: [link to existing API docs]

Generate:
1. Endpoint definitions (method, path, description)
2. Request schemas (with validation rules)
3. Response schemas (success and error)
4. Error codes and messages
5. Example requests/responses
```

---

## 8. Implementation Planning

### Task Breakdown

```markdown
Create an implementation plan for this specification:

[Specification + Design]

**Requirements:**
1. Break into tasks that fit in ~100k tokens of context
2. Identify dependencies between tasks
3. Group into parallelization waves
4. Estimate complexity (Low/Medium/High)
5. Identify what tests each task needs

**Format:**
- Task ID, title, description
- Files to create/modify
- Dependencies (task IDs)
- Acceptance criteria
- Complexity
```

### Dependency Graph

```markdown
Analyze these tasks and create a dependency graph:

[Task list]

Output:
1. Visual dependency graph (ASCII or Mermaid)
2. Parallelization waves (tasks that can run simultaneously)
3. Critical path (longest dependency chain)
4. Bottlenecks (tasks blocking many others)
5. Suggested order of execution
```

### Task File Generation

```markdown
Generate a TASK file for:

**Task:** [Task ID and title]
**From:** [Link to impl-plan]
**Spec:** [Link to spec]
**Design:** [Link to design]

Include:
1. SDD references table
2. Dependencies completed (what this task can use)
3. What this task provides (for dependent tasks)
4. Requirements covered
5. Acceptance criteria (from spec)
6. Files to change (CREATE/MODIFY/DELETE)
7. Implementation notes
8. Testing requirements
9. Complexity estimate
```

---

## 9. Refinement and Iteration

### Spec Improvement

```markdown
Improve this specification:

[Current specification]

Focus on:
1. Making requirements more specific
2. Adding missing edge cases
3. Clarifying ambiguous language
4. Strengthening acceptance criteria
5. Adding concrete examples

Keep the same structure, enhance the content.
```

### Scope Reduction

```markdown
This specification is too large. Help me reduce scope while maintaining value:

[Specification]

**Constraints:**
- Must fit in [X] tasks
- Phase 1 should deliver [core value]

Suggest:
1. What to keep in Phase 1 (MVP)
2. What to defer to Phase 2
3. What to remove entirely
4. Risks of each deferral
```

### Feedback Integration

```markdown
Update this specification based on feedback:

**Current spec:**
[Specification]

**Feedback received:**
[Feedback from stakeholders/review]

Instructions:
1. Address each feedback point
2. Document what changed and why
3. Flag any feedback that conflicts with constraints
4. Suggest alternatives for rejected feedback
```

### Version Comparison

```markdown
Compare these two versions of the specification:

**Version 1:**
[Old spec]

**Version 2:**
[New spec]

Generate:
1. Summary of changes
2. New requirements added
3. Requirements removed
4. Requirements modified
5. Impact assessment of changes
```

---

## Model-Specific Tips

### Claude (Sonnet/Opus)

```markdown
<!-- Claude excels at: long documents, nuanced reasoning, clean structure -->

When generating specifications with Claude:
- Provide full context upfront (200k window)
- Ask for reasoning before conclusions
- Request markdown with clear hierarchy
- Use "think step by step" for complex requirements
```

### GPT-4/5

```markdown
<!-- GPT excels at: versatility, wide language support, consistent format -->

When generating specifications with GPT:
- Be explicit about output format
- Provide examples of desired output
- Use system prompts for consistent style
- Break very large specs into sections
```

### Gemini

```markdown
<!-- Gemini excels at: massive context, codebase analysis, multimodal -->

When generating specifications with Gemini:
- Leverage large context for full codebase analysis
- Include visual mockups/diagrams when relevant
- Use for understanding existing large codebases
- Good for generating specs from existing code
```

---

## Prompt Engineering Best Practices

### Do

- Provide rich context (project, constraints, examples)
- Use specific formats (FR-X, Given-When-Then)
- Ask for reasoning and trade-offs
- Request concrete examples, not placeholders
- Iterate through multiple rounds

### Avoid

- Vague requests ("make a spec for login")
- Assuming AI knows your domain
- Accepting first output without review
- Ignoring AI's clarifying questions
- Skipping validation prompts

---

## Quick Reference

### Start a Spec Session
```
I need to create a specification for [feature].
Before generating anything, ask me clarifying questions.
```

### Generate Requirements
```
Generate functional requirements (FR-X format) for [feature].
Include acceptance criteria for each.
```

### Find Edge Cases
```
What edge cases should I consider for [feature]?
Focus on [security/performance/data/user experience].
```

### Review Spec
```
Review this spec for completeness, conflicts, and testability.
Suggest specific improvements.
```

### Create Tasks
```
Break this spec into implementation tasks.
Each task should fit in ~100k token context.
```

---

*Part of the [ai-assisted-specification-writing](README.md) methodology.*
