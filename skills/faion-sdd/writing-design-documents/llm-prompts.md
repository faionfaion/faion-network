# LLM Prompts for Design Documents

Prompts for using LLMs to create, review, and improve design documents.

---

## Design Document Creation

### Generate Design from Spec

```
I have a specification with these requirements:

[Paste FR-X and NFR-X requirements]

Project context:
- Tech stack: [stack]
- Existing patterns: [patterns]
- Constraints: [constraints]

Generate a design document that:
1. Creates AD-X for each requirement
2. Specifies file structure
3. Defines data models
4. Documents API contracts
5. Addresses security and performance

Use the SDD design template format.
```

### Generate Architectural Decisions

```
I need to make a decision about [topic].

Context:
- [Background information]
- [Constraints]
- [Requirements: FR-X, NFR-X]

Generate 3 alternatives with:
- Pros and cons for each
- Trade-off analysis
- Recommendation with rationale

Format as AD-XXX following ADR style.
```

### Generate API Contract

```
Design an API endpoint for [purpose].

Requirements:
- [FR-X requirements]
- Authentication: [required/none]
- Rate limiting: [requirements]

Follow existing patterns from:
[Paste example endpoint]

Include:
- Request/response JSON examples
- Validation rules
- Error responses
- OpenAPI-style documentation
```

---

## Design Document Review

### Completeness Review

```
Review this design document for completeness:

[Paste design document]

Check:
1. Are all FR-X from the spec covered by AD-X?
2. Are all NFR-X addressed?
3. Is every file change traced to requirements?
4. Are all API endpoints documented with examples?
5. Are security considerations complete?
6. Is there a testing strategy?

Provide a checklist with pass/fail for each item.
```

### Technical Review

```
Review this design document for technical correctness:

[Paste design document]

Context:
- Tech stack: [stack]
- Existing patterns: [paste examples]

Check:
1. Are the chosen technologies appropriate?
2. Are there any architectural anti-patterns?
3. Will the design scale for [expected load]?
4. Are there security vulnerabilities?
5. Is error handling adequate?

Provide specific, actionable feedback.
```

### Traceability Review

```
Verify traceability in this design:

Spec requirements:
[Paste FR-X and NFR-X list]

Design decisions:
[Paste AD-X list]

File changes:
[Paste file list]

Verify:
1. Every FR-X has at least one AD-X
2. Every AD-X traces to FR-X
3. Every file change traces to AD-X
4. No orphan decisions or files

Report any gaps.
```

### LLM-Readiness Review

```
Review this design for LLM code generation readiness:

[Paste design document]

Check:
1. Are type definitions complete and explicit?
2. Do API contracts have example JSON?
3. Are error responses documented?
4. Are validation rules specified?
5. Are pattern references clear?
6. Can an LLM implement this without asking questions?

Suggest improvements for LLM-friendly documentation.
```

---

## Design Improvement

### Suggest Alternatives

```
For this architectural decision:

[Paste AD-X]

Suggest 2-3 alternative approaches I may have missed.
For each alternative:
- Describe the approach
- List pros and cons
- Explain when it would be better

Consider: performance, maintainability, simplicity, security.
```

### Identify Edge Cases

```
For this feature design:

[Paste design overview and API contracts]

Identify edge cases and failure scenarios:
1. What inputs could break this?
2. What concurrent operations could conflict?
3. What happens if dependencies fail?
4. What data integrity issues are possible?

For each, suggest how to handle it.
```

### Security Analysis

```
Analyze security for this design:

[Paste design document]

Identify:
1. Authentication vulnerabilities
2. Authorization gaps
3. Input validation issues
4. Data exposure risks
5. Injection possibilities

For each issue:
- Severity: High/Medium/Low
- Mitigation recommendation
- Reference to OWASP if applicable
```

### Performance Analysis

```
Analyze performance for this design:

[Paste design document]

Expected load: [requests/second, users, data volume]

Identify:
1. Potential bottlenecks
2. N+1 query risks
3. Missing caching opportunities
4. Scalability limits

Suggest optimizations for each issue.
```

---

## Design Discussion

### Explore Trade-offs

```
I'm designing [feature] and facing this trade-off:

Option A: [description]
- Pros: [list]
- Cons: [list]

Option B: [description]
- Pros: [list]
- Cons: [list]

Context:
- Priority: [speed/quality/flexibility]
- Team size: [small/medium/large]
- Expected lifespan: [months/years]

Help me think through this decision.
What questions should I ask?
What factors am I missing?
```

### Challenge Assumptions

```
I've made these assumptions in my design:

[List assumptions]

Challenge each assumption:
1. What if this assumption is wrong?
2. What evidence supports/contradicts it?
3. How would the design change if false?

Help me identify blind spots.
```

### Validate Approach

```
I'm planning to implement [feature] using [approach].

My reasoning:
[Explain why you chose this approach]

Context:
- [Project constraints]
- [Team experience]
- [Time constraints]

Is this the right approach?
What am I missing?
What would you do differently?
```

---

## Spec-First Design (from Addy Osmani's Workflow)

### Requirements Discovery

```
I want to build [project/feature].

Ask me questions one at a time until you understand:
1. The core functionality
2. User workflows
3. Edge cases
4. Non-functional requirements
5. Constraints

After each answer, ask the next most important question.
When complete, summarize as a spec.md.
```

### Comprehensive Spec Generation

```
Based on our discussion, generate a comprehensive spec.md containing:

1. Requirements (FR-X format)
   - Functional requirements
   - Non-functional requirements

2. Acceptance Criteria (Given-When-Then)
   - For each requirement

3. Assumptions
   - What we're assuming is true

4. Out of Scope
   - What we're explicitly not doing

5. Open Questions
   - What still needs to be decided
```

### Design from Spec

```
Here is the specification:

[Paste spec.md]

Generate a design document that:
1. Covers all FR-X and NFR-X
2. Uses appropriate patterns for [tech stack]
3. Follows existing conventions from [paste examples]
4. Is optimized for LLM code generation

Include:
- Architecture overview
- Data models with TypeScript types
- API contracts with JSON examples
- File structure with CREATE/MODIFY actions
- Testing strategy
```

---

## Context Packing

### Load Context for Design

```
I'm designing a feature for this project.

Constitution (tech stack & standards):
[Paste constitution.md]

Existing pattern examples:
[Paste relevant code files]

Similar completed feature:
[Paste related design.md]

Specification for new feature:
[Paste spec.md]

With this context, generate a design document that:
1. Follows existing patterns
2. Uses established conventions
3. Integrates with current architecture
4. Covers all requirements from spec
```

---

## Output Formatting

### Request Specific Format

```
Generate the design in this exact format:

[Paste template structure]

Use markdown with:
- Tables for structured data
- Code blocks with language tags
- Proper heading hierarchy
- No emojis
```

### Request Concise Output

```
Keep the design document concise:
- Each AD-X should be < 200 words
- API contracts: just request/response examples
- No verbose explanations
- Focus on what LLMs need to generate code
```

---

## Multi-Model Strategy

### Cross-Check Design

```
Review this design document critically:

[Paste design]

You are an adversarial reviewer. Find:
1. Logical inconsistencies
2. Missing requirements
3. Technical risks
4. Implementation ambiguities

Be specific and constructive.
```

### Synthesize Multiple Perspectives

```
I received these two design proposals:

Proposal A:
[Paste proposal A]

Proposal B:
[Paste proposal B]

Analyze both and recommend:
1. Which is better overall and why
2. What to take from each
3. A synthesized approach combining the best of both
```

---

## Tips for Effective Prompts

### Do

- Provide full context (spec, constitution, examples)
- Ask for specific outputs (AD-X format, JSON examples)
- Request actionable feedback
- Use iterative refinement

### Don't

- Ask vague questions ("Is this good?")
- Skip context ("Review this design")
- Request too much at once
- Ignore the LLM's questions

### Iteration Pattern

1. Start broad: "Generate a design for X"
2. Refine specific sections: "Improve the API contracts"
3. Add missing pieces: "What about error handling?"
4. Final review: "Check completeness and readiness"

---

*Prompts | LLM-Assisted Design | Version 3.0.0*
