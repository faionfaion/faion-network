# AI-Assisted Specification Writing Checklist

> Step-by-step checklist for creating high-quality specifications with LLM assistance.

## Pre-Specification Checklist

### Context Preparation

- [ ] **Define the problem statement** - What problem are we solving? Why does it matter?
- [ ] **Identify target users** - Who will use this? What are their personas?
- [ ] **List known constraints** - Technical, business, regulatory, timeline
- [ ] **Gather existing context** - Related specs, codebase patterns, past decisions
- [ ] **Prepare domain terminology** - Key terms the AI needs to understand
- [ ] **Set scope boundaries** - What is explicitly NOT in scope

### LLM Setup

- [ ] **Choose appropriate model** - Claude for complexity, GPT for versatility, Gemini for scale
- [ ] **Prepare context documents** - Constitution, existing specs, codebase structure
- [ ] **Set appropriate temperature** - Lower (0.2-0.5) for specs, higher for brainstorming
- [ ] **Establish output format** - Markdown, YAML, JSON, or BDD format

---

## Phase 1: Intent Capture

### Initial Brainstorming with AI

- [ ] **Describe the feature/system** in natural language
- [ ] **Let AI ask clarifying questions** - Answer all questions thoroughly
- [ ] **Identify stakeholders** - Who cares about this? Who approves?
- [ ] **Define success criteria** - How do we know when it's done?
- [ ] **Document assumptions** - What are we taking for granted?

### Intent Validation

- [ ] **Review AI's understanding** - Does it match your mental model?
- [ ] **Correct any misunderstandings** - Be explicit about what's wrong
- [ ] **Add missing context** - What did AI miss that you know?
- [ ] **Confirm scope** - Is AI's interpretation of scope correct?

---

## Phase 2: Requirements Extraction

### Functional Requirements

- [ ] **Generate FR list** - Use AI to enumerate all functional requirements
- [ ] **Format consistently** - FR-1, FR-2, etc. with clear descriptions
- [ ] **Verify completeness** - Ask AI: "What functionality might I have missed?"
- [ ] **Prioritize requirements** - Must-have vs. nice-to-have (MoSCoW)
- [ ] **Check for conflicts** - Ask AI to identify conflicting requirements

### Non-Functional Requirements

- [ ] **Performance requirements** - Response times, throughput, capacity
- [ ] **Security requirements** - Authentication, authorization, data protection
- [ ] **Scalability requirements** - Growth expectations, scaling patterns
- [ ] **Reliability requirements** - Uptime, failover, recovery
- [ ] **Compliance requirements** - GDPR, HIPAA, industry standards

### Edge Cases

- [ ] **Ask AI to enumerate edge cases** - "What could go wrong?"
- [ ] **Document error scenarios** - Invalid input, network failures, timeouts
- [ ] **Handle boundary conditions** - Empty states, maximum limits, unicode
- [ ] **Consider concurrent scenarios** - Race conditions, deadlocks
- [ ] **Plan degraded modes** - What happens when dependencies fail?

---

## Phase 3: Acceptance Criteria

### Given-When-Then Format

- [ ] **Write AC for each requirement** - At least one AC per FR
- [ ] **Use consistent format** - Given [context], When [action], Then [outcome]
- [ ] **Make criteria testable** - Can QA verify this without ambiguity?
- [ ] **Include positive and negative cases** - Happy path + error paths
- [ ] **Add data examples** - Concrete values, not just "valid input"

### AC Quality Check

- [ ] **Specific** - No vague terms like "quickly" or "efficiently"
- [ ] **Measurable** - Quantifiable outcomes where possible
- [ ] **Achievable** - Technically feasible within constraints
- [ ] **Relevant** - Directly tied to a requirement
- [ ] **Testable** - Can be verified through automated or manual testing

---

## Phase 4: Technical Design

### Architecture Elements

- [ ] **Data models** - Entities, relationships, schemas
- [ ] **API contracts** - Endpoints, request/response formats
- [ ] **Component interfaces** - How modules communicate
- [ ] **Dependencies** - External services, libraries, APIs
- [ ] **Integration points** - Where this connects to existing systems

### Design Validation with AI

- [ ] **Ask AI to review design** - "What problems do you see with this design?"
- [ ] **Check for scalability issues** - "How would this handle 10x traffic?"
- [ ] **Verify security** - "What security vulnerabilities might exist?"
- [ ] **Assess maintainability** - "What would make this hard to change later?"

---

## Phase 5: Implementation Planning

### Task Breakdown

- [ ] **Generate task list** - Discrete, implementable units
- [ ] **Sequence by dependencies** - What must come first?
- [ ] **Estimate complexity** - Low/Medium/High (NOT time estimates)
- [ ] **Identify parallelization** - What can be done simultaneously?
- [ ] **Plan testing strategy** - Unit, integration, E2E for each phase

### Quality Gates

- [ ] **Define phase boundaries** - When is Phase 1 "done"?
- [ ] **Set review checkpoints** - Human review after each phase
- [ ] **Plan rollback points** - Where can we safely revert?
- [ ] **Document dependencies** - External dependencies and their status

---

## Phase 6: AI Validation Review

### Completeness Check

- [ ] **All requirements have acceptance criteria**
- [ ] **All edge cases documented and handled**
- [ ] **Dependencies explicitly listed**
- [ ] **Non-goals clearly stated** (what we're NOT building)
- [ ] **Assumptions documented**

### Consistency Check

- [ ] **No conflicting requirements**
- [ ] **Terminology used consistently**
- [ ] **Format follows template**
- [ ] **Traceability maintained** (AC → FR → User Story)

### AI Review Prompts

```
"Review this specification for:
1. Missing requirements
2. Conflicting requirements
3. Ambiguous acceptance criteria
4. Missing edge cases
5. Security concerns
6. Scalability issues"
```

---

## Phase 7: Human Review

### Domain Validation

- [ ] **Business logic correct** - Does this match how the business actually works?
- [ ] **User needs addressed** - Will users actually want this?
- [ ] **Edge cases realistic** - Are we over-engineering or missing real scenarios?
- [ ] **Constraints accurate** - Are technical/business constraints correctly stated?

### Stakeholder Sign-off

- [ ] **Product owner approval** - Requirements match vision
- [ ] **Tech lead approval** - Design is feasible
- [ ] **QA approval** - Criteria are testable
- [ ] **Security review** (if applicable) - No obvious vulnerabilities

---

## Post-Specification Checklist

### Documentation

- [ ] **Spec is version-controlled** - In git with the codebase
- [ ] **Links to related docs** - Design docs, ADRs, previous specs
- [ ] **Glossary updated** - New terms defined
- [ ] **Decision log updated** - Key decisions documented

### Handoff

- [ ] **Implementation team briefed** - Walkthrough completed
- [ ] **Questions answered** - Ambiguities resolved
- [ ] **Change process defined** - How to request spec changes
- [ ] **Success metrics agreed** - How we measure success

---

## Quick Reference: AI Review Commands

```markdown
## Completeness Review
"List any requirements that are missing acceptance criteria."

## Conflict Detection
"Identify any requirements that conflict with each other."

## Edge Case Generation
"What edge cases should we consider for [feature]?"

## Security Review
"What security vulnerabilities might exist in this specification?"

## Testability Check
"Which acceptance criteria are not testable? How can we make them testable?"

## Scope Validation
"Based on these requirements, what is implicitly in scope that should be explicit?"
```

---

## Checklist Summary

| Phase | Key Deliverable |
|-------|-----------------|
| Pre-Spec | Context document, constraints list |
| Intent Capture | Problem statement, success criteria |
| Requirements | FR list, NFR list, edge cases |
| Acceptance Criteria | Given-When-Then for all FRs |
| Technical Design | Data models, APIs, architecture |
| Implementation Plan | Task list, dependencies, phases |
| AI Validation | Completeness/consistency report |
| Human Review | Stakeholder sign-offs |

---

*Part of the [ai-assisted-specification-writing](README.md) methodology.*
