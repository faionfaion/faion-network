# LLM Prompts for SDD Trend Analysis

Effective prompts for leveraging LLMs in Specification-Driven Development workflows.

**Version:** 1.0

---

## Table of Contents

1. [Specification Writing](#1-specification-writing)
2. [Architecture Decision Records](#2-architecture-decision-records)
3. [Design Documents](#3-design-documents)
4. [Implementation Planning](#4-implementation-planning)
5. [Code Generation](#5-code-generation)
6. [Documentation](#6-documentation)
7. [Trend Analysis](#7-trend-analysis)
8. [Quality Review](#8-quality-review)

---

## 1. Specification Writing

### 1.1 Generate Spec from User Request

```
I need to write a specification for a new feature. Here's the user request:

"[Paste user request or ticket description]"

Please help me create a comprehensive specification that includes:
1. Problem statement (2-3 sentences with metrics if possible)
2. Goals (3-5 measurable outcomes)
3. User stories with acceptance criteria (Given-When-Then format)
4. Non-functional requirements (performance, security, scalability)
5. Out of scope items
6. Success metrics with targets

Context about our system:
- Tech stack: [list technologies]
- Current relevant features: [describe related features]
- User types: [list user personas]
```

### 1.2 Identify Missing Requirements

```
Review this specification and identify potential gaps:

[Paste specification]

Please analyze for:
1. Missing edge cases
2. Ambiguous requirements that need clarification
3. Implicit assumptions that should be explicit
4. Security considerations not addressed
5. Performance requirements not specified
6. Error scenarios not covered
7. Integration points not documented

For each gap found, suggest specific language to add.
```

### 1.3 Generate Acceptance Criteria

```
Convert these user stories into detailed acceptance criteria using Given-When-Then format:

User Story: [Paste user story]

Requirements:
1. Cover the happy path
2. Include at least 2 error scenarios
3. Consider edge cases (empty data, maximum limits, concurrent access)
4. Include validation rules
5. Specify observable outcomes (what the user sees, what the system records)
```

### 1.4 Spec Critique and Improvement

```
Act as a critical reviewer for this specification. You are reviewing it before
it goes to the development team.

[Paste specification]

Evaluate against these criteria:
1. Clarity: Can a developer implement this without asking questions?
2. Completeness: Are all scenarios covered?
3. Testability: Can each requirement be verified?
4. Feasibility: Are there any technically impossible requirements?
5. Consistency: Do any requirements contradict each other?
6. Scope: Is the scope appropriate (not too large, not too small)?

Provide specific, actionable feedback with suggested improvements.
```

---

## 2. Architecture Decision Records

### 2.1 Generate ADR from Discussion

```
Help me create an ADR from this discussion/decision:

Context: [Describe the situation, problem, constraints]

Decision made: [What was decided]

Alternatives discussed: [List alternatives]

Key factors: [What influenced the decision]

Please generate an ADR with:
1. Clear status (Proposed/Accepted)
2. Detailed context explaining the forces at play
3. Specific decision statement
4. Rationale with key factors
5. Consequences (positive, negative, neutral)
6. Analysis of rejected alternatives
7. Related decisions to reference
```

### 2.2 ADR Alternative Analysis

```
We're considering this architectural decision:

Decision: [Describe proposed decision]

Context:
- System: [Describe system]
- Constraints: [List constraints]
- Current state: [Describe current architecture]

Please analyze these alternatives:
1. [Alternative 1]
2. [Alternative 2]
3. [Alternative 3]

For each alternative, provide:
- Pros (benefits, advantages)
- Cons (drawbacks, risks)
- Implementation complexity
- Long-term maintenance implications
- Team expertise requirements
- Migration path from current state

Conclude with a recommendation and justification.
```

### 2.3 ADR Impact Assessment

```
Review this ADR and analyze its impact:

[Paste ADR]

Please assess:
1. Impact on existing architecture
2. Required changes to other systems
3. Migration effort required
4. Risk assessment (likelihood and impact)
5. Monitoring/observability implications
6. Security implications
7. Cost implications (infrastructure, licensing, engineering time)
8. Reversibility - how easy to undo if needed?

Provide a summary matrix of impacts: High/Medium/Low for each area.
```

---

## 3. Design Documents

### 3.1 Generate Technical Design

```
Create a technical design document for this feature:

Specification: [Link or paste spec]

Technical constraints:
- Stack: [List technologies]
- Existing patterns: [Describe patterns used in codebase]
- Performance requirements: [List requirements]
- Security requirements: [List requirements]

Please include:
1. Architecture overview with component diagram
2. Data model changes (new tables, schema changes)
3. API design (endpoints, request/response)
4. Component design (responsibilities, interfaces)
5. Security considerations
6. Error handling strategy
7. Testing strategy
8. Observability (metrics, logs, traces)
9. Rollout plan with feature flags
10. Open questions that need resolution
```

### 3.2 Design Review Checklist

```
Review this technical design document:

[Paste design document]

Evaluate against these dimensions:

**Architecture:**
- Does it follow existing patterns?
- Is it appropriately decoupled?
- Are responsibilities clearly defined?

**Security:**
- Authentication and authorization addressed?
- Data protection considered?
- Input validation specified?

**Performance:**
- Will it meet performance requirements?
- Are there potential bottlenecks?
- Is caching strategy appropriate?

**Reliability:**
- Error handling comprehensive?
- Failure scenarios covered?
- Rollback plan defined?

**Maintainability:**
- Is it testable?
- Is complexity manageable?
- Are dependencies appropriate?

Provide specific feedback with suggested improvements.
```

---

## 4. Implementation Planning

### 4.1 Generate Task Breakdown

```
Create an implementation plan from this design:

[Paste design document]

Requirements:
1. Break into tasks that fit in ~100k token context
2. Identify dependencies between tasks
3. Group into parallelizable waves
4. Estimate complexity (Low/Medium/High) for each task
5. List files to create/modify for each task
6. Include testing tasks
7. Include documentation tasks

Output format:
- Wave 1: [Tasks that can run in parallel]
- Wave 2: [Tasks dependent on Wave 1]
- Wave 3: [Tasks dependent on Wave 2]
- etc.

For each task, provide: ID, description, files, complexity, dependencies.
```

### 4.2 Dependency Analysis

```
Analyze the dependencies in this implementation plan:

[Paste implementation plan]

Please identify:
1. Critical path (longest chain of dependent tasks)
2. Parallelization opportunities
3. Potential bottlenecks
4. Tasks that could be done earlier to unblock others
5. Hidden dependencies not explicitly stated
6. Risks of circular or complex dependencies

Suggest optimizations to reduce overall implementation time.
```

### 4.3 Risk Identification

```
Review this implementation plan and identify risks:

[Paste implementation plan]

For each risk found:
1. Description of the risk
2. Likelihood (High/Medium/Low)
3. Impact if realized (High/Medium/Low)
4. Early warning signs
5. Mitigation strategy
6. Contingency plan

Also identify:
- Technical risks (complexity, unfamiliar technology)
- Integration risks (dependencies on other teams/systems)
- Timeline risks (underestimated effort)
- Quality risks (insufficient testing)
```

---

## 5. Code Generation

### 5.1 Context-Packed Code Request

```
I need to implement [feature/component].

## Project Context
- Language: [language and version]
- Framework: [framework and version]
- Patterns used: [list patterns]
- Relevant existing code: [paste or describe]

## Requirements
[Paste from spec or task file]

## Constraints
- Must follow existing patterns for [X]
- Error handling should use [approach]
- Testing: [testing requirements]

## Files to Generate
- [File 1]: [purpose]
- [File 2]: [purpose]

## Examples of Similar Code
[Paste example from codebase]

## Do NOT
- [Anti-pattern to avoid]
- [Thing to not do]

Generate the implementation with:
1. Clear comments explaining key decisions
2. Error handling for all failure cases
3. Input validation
4. Type safety (no 'any' types)
```

### 5.2 Test Generation

```
Generate tests for this code:

[Paste code to test]

Testing requirements:
- Framework: [Jest/pytest/etc.]
- Style: [describe preferred style]
- Coverage target: [percentage]

Generate:
1. Unit tests for each public function/method
2. Edge case tests (empty input, maximum values, null/undefined)
3. Error scenario tests
4. Integration test skeleton (if applicable)

For each test:
- Clear test name describing what it tests
- Arrange-Act-Assert structure
- Meaningful assertions
- Comments for complex test setups
```

### 5.3 Code Review Prompt

```
Review this code for quality:

[Paste code]

Context:
- This implements: [feature/task]
- Spec requirements: [list key requirements]
- Coding standards: [paste or describe]

Check for:
1. Correctness: Does it implement the requirements?
2. Security: Any vulnerabilities?
3. Performance: Any inefficiencies?
4. Readability: Is it clear and well-named?
5. Maintainability: Is it easy to modify?
6. Testing: Are there test coverage gaps?
7. Error handling: Is it robust?
8. Edge cases: Are they handled?

For each issue found, provide:
- Location (line number or section)
- Issue description
- Severity (Critical/Major/Minor/Suggestion)
- Suggested fix with code example
```

---

## 6. Documentation

### 6.1 Generate API Documentation

```
Generate API documentation for these endpoints:

[Paste code or OpenAPI spec]

Documentation should include:
1. Endpoint summary (one line)
2. Detailed description
3. Authentication requirements
4. Request parameters (path, query, body)
5. Request body example
6. Response schema with all fields explained
7. Response examples (success and error cases)
8. Error codes and their meanings
9. Rate limiting information
10. Usage examples with curl/fetch
```

### 6.2 Update CLAUDE.md

```
Update the project CLAUDE.md based on these recent changes:

Current CLAUDE.md:
[Paste current content]

Recent changes:
1. [Change 1]
2. [Change 2]
3. [Change 3]

New patterns introduced:
[Describe new patterns]

Decisions made:
[List relevant ADRs or decisions]

Please update CLAUDE.md to:
1. Reflect new patterns in the "Patterns to Follow" section
2. Add any new anti-patterns discovered
3. Update directory structure if changed
4. Add new ADR references
5. Update current focus section
6. Maintain existing style and format
```

### 6.3 Generate README

```
Generate a README.md for this project/component:

[Paste code structure or describe project]

Include:
1. Project name and one-line description
2. Problem it solves
3. Key features (bullet points)
4. Prerequisites
5. Installation instructions
6. Quick start (3-5 steps to get running)
7. Configuration options
8. Usage examples
9. API reference (brief)
10. Contributing guidelines
11. License

Style:
- Concise but complete
- Code examples for all non-obvious steps
- No emojis
- Tables for configuration options
```

---

## 7. Trend Analysis

### 7.1 Technology Trend Research

```
Research the current state of [technology/practice] for software development.

Focus on:
1. Current adoption rates and trends
2. Major players and tools
3. Best practices as of 2025-2026
4. Common pitfalls to avoid
5. Comparison with alternatives
6. Implementation considerations
7. Future trajectory

For each point, cite sources where possible.

Output format:
- Executive summary (2-3 paragraphs)
- Detailed analysis by category
- Recommendations for adoption
- Resources for further learning
```

### 7.2 Compare Approaches

```
Compare these approaches for [problem/goal]:

1. [Approach 1]
2. [Approach 2]
3. [Approach 3]

Evaluation criteria:
- Adoption/maturity in 2025-2026
- Learning curve
- Team skill requirements
- Tooling ecosystem
- Integration with existing stack: [describe stack]
- Long-term maintenance
- Cost (licensing, infrastructure, engineering)
- Community and support

Output:
- Comparison matrix
- Detailed analysis of each
- Recommended approach with justification
- Migration path if switching from current approach
```

### 7.3 Assess Trend Relevance

```
Assess whether [trend/technology] is relevant for our project:

Our context:
- Project type: [type]
- Team size: [size]
- Current stack: [stack]
- Business domain: [domain]
- Current pain points: [list]

For the trend, evaluate:
1. Does it address our pain points?
2. Is our team positioned to adopt it?
3. What's the ROI vs. effort?
4. What are the risks of adopting?
5. What are the risks of NOT adopting?
6. When is the right time to adopt?

Provide a recommendation: Adopt now / Plan for future / Monitor / Ignore
```

---

## 8. Quality Review

### 8.1 Spec Quality Score

```
Score this specification on quality:

[Paste specification]

Criteria (1-5 scale):
1. Clarity: How clear and unambiguous is it?
2. Completeness: Are all scenarios covered?
3. Testability: Can requirements be verified?
4. Feasibility: Are requirements achievable?
5. Prioritization: Is scope appropriate?
6. User focus: Are user needs addressed?
7. Technical accuracy: Are technical aspects correct?

For each criterion:
- Score (1-5)
- Justification
- Specific improvements needed

Overall score and readiness assessment:
- Ready for implementation
- Needs minor revisions
- Needs significant revision
- Needs complete rewrite
```

### 8.2 Design Consistency Check

```
Check this design document for consistency with our codebase:

Design document:
[Paste design]

Our patterns and standards:
[Paste CLAUDE.md or describe]

Check for:
1. Pattern consistency (does it follow our patterns?)
2. Naming consistency (follows our conventions?)
3. API consistency (matches our API style?)
4. Error handling consistency
5. Testing approach consistency
6. Documentation consistency

For each inconsistency:
- Description
- Impact
- Suggested correction
```

### 8.3 Implementation Verification

```
Verify this implementation against its specification:

Specification:
[Paste spec or key requirements]

Implementation:
[Paste code]

For each requirement in the spec:
1. Is it implemented? (Yes/No/Partial)
2. Where is it implemented? (file/function)
3. Does it meet acceptance criteria?
4. Are there gaps or issues?

Summary:
- Requirements fully met: X/Y
- Requirements partially met: X/Y
- Requirements not met: X/Y
- Additional work needed: [list]
```

---

## Prompt Engineering Tips

### 1. Context Packing Best Practices

- **Be specific**: Include file paths, function names, exact requirements
- **Provide examples**: Show what good looks like from your codebase
- **State constraints**: Explicitly list what NOT to do
- **Include relevant code**: Paste existing patterns to follow

### 2. Multi-Turn Strategy

For complex tasks, break into steps:
1. First prompt: Gather information and plan
2. Second prompt: Generate with plan review
3. Third prompt: Refine based on feedback

### 3. Output Format Control

```
Respond in this exact format:
[Specify format with example]

Do NOT include:
- [Things to exclude]
- [Other things to exclude]
```

### 4. Chain of Thought

For complex analysis:
```
Think through this step by step:
1. First, analyze [aspect 1]
2. Then, consider [aspect 2]
3. Finally, synthesize into [output]

Show your reasoning for each step.
```

### 5. Role Assignment

```
Act as a [senior architect / security expert / performance engineer]
reviewing this [artifact] for [specific concern].
```

---

## Resources

- [README.md](README.md) - Overview and context
- [checklist.md](checklist.md) - Adoption checklist
- [examples.md](examples.md) - Real-world examples
- [templates.md](templates.md) - Copy-paste templates

---

*Prompts Document | LLM-Assisted SDD | Version 1.0*
