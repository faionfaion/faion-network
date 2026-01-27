# Writing Design Documents

## Metadata

| Field | Value |
|-------|-------|
| **ID** | writing-design-documents |
| **Version** | 3.0.0 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #design, #architecture, #llm |
| **Domain Skill** | faion-sdd |

---

## What is a Design Document?

A design document answers: **"HOW are we building this?"**

It bridges the gap between specification (WHAT) and implementation (CODE). Design docs are informal documents created before coding to document the high-level implementation strategy and key design decisions with emphasis on trade-offs.

> "As software engineers, our job is not to produce code per se, but rather to solve problems. Unstructured text may be the better tool for solving problems early in a project lifecycle."
> — [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)

---

## When to Write a Design Doc

| Situation | Write Design Doc? |
|-----------|-------------------|
| Small bug fix | No |
| Refactoring existing code | Maybe (if architecture changes) |
| New feature with 1-2 files | No |
| New feature touching 5+ files | Yes |
| API changes affecting consumers | Yes |
| Database schema changes | Yes |
| Cross-team dependencies | Yes |
| Security-sensitive changes | Yes |
| Performance-critical systems | Yes |

**Rule of thumb:** If the change is non-trivial and has dependencies, write a design doc. The effort should be proportionate to complexity.

---

## Document Hierarchy

```
CONSTITUTION (project-wide)
    |
    v informs
SPEC (feature) --> DESIGN (feature) --> IMPL-PLAN --> TASKS
    FR-X            AD-X                 Waves         TASK-XXX
    requirements    decisions            breakdown     executable
```

### Design vs Spec vs Implementation Plan

| Aspect | Specification | Design | Implementation Plan |
|--------|---------------|--------|---------------------|
| Question | What to build? | How to build it? | In what order? |
| Audience | Stakeholders, PMs | Developers, AI | Developers, AI agents |
| Content | Requirements, AC | Architecture, APIs | Tasks, estimates |
| Output | FR-X, NFR-X | AD-X, file list | TASK-XXX list |

---

## Design Document Structure

### Google-Style Structure

Based on [Google's approach](https://www.industrialempathy.com/posts/design-docs-at-google/):

```markdown
# Design: [Feature Name]

## Context and Scope
[What is and isn't covered]

## Goals and Non-Goals
[Explicit about what we're NOT doing]

## Overview
[High-level summary of technical approach]

## Detailed Design
[The actual design with diagrams]

## Alternatives Considered
[Other options and why rejected]

## Cross-cutting Concerns
[Security, privacy, observability]
```

### SDD Structure (LLM-Optimized)

Optimized for LLM code generation and review:

```markdown
# Design: [Feature Name]

## Reference Documents
[Links to spec, constitution, related designs]

## Spec Coverage
[FR-X to AD-X traceability matrix]

## Architectural Decisions
[AD-X with rationale, alternatives, consequences]

## File Structure
[What files to create/modify with patterns]

## Data Models
[Database schemas, TypeScript types]

## API Contracts
[Endpoints with OpenAPI-style documentation]

## Dependencies
[Libraries, services, infrastructure]

## Security Considerations
[Auth, validation, encryption]

## Performance Considerations
[Caching, optimization, scaling]

## Testing Strategy
[Unit, integration, E2E approach]
```

---

## Using LLMs for Design Documents

### Design Phase with LLMs

From [Addy Osmani's LLM workflow](https://addyosmani.com/blog/ai-coding-workflow/):

> "For a new project, describe the idea and ask the LLM to iteratively ask you questions until you've fleshed out requirements and edge cases."

### LLM-Assisted Design Process

1. **Context Packing**: Feed the LLM all relevant information
   - Existing codebase patterns
   - Tech stack constraints
   - Project constitution
   - Related designs

2. **Iterative Refinement**: Ask LLM to:
   - Challenge assumptions
   - Identify edge cases
   - Suggest alternatives
   - Find potential issues

3. **Review and Validation**: Use LLM to:
   - Check for completeness
   - Verify traceability
   - Identify missing sections
   - Suggest improvements

### Prompts for Design Discussions

See [llm-prompts.md](llm-prompts.md) for specific prompts.

---

## Architectural Decisions (ADR-Style)

Based on [ADR best practices](https://adr.github.io/):

### Decision Format

```markdown
### AD-001: [Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded

**Context:** [Background, constraints, why decision needed]

**Decision:** [What was decided]

**Rationale:**
- [Reason 1]
- [Reason 2]

**Alternatives Considered:**
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| [Option A] | [+] | [-] | [Reason] |

**Consequences:**
- **Positive:** [Benefits]
- **Negative:** [Trade-offs]
- **Risks:** [What could go wrong]

**Traces to:** FR-001, NFR-002
```

### Y-Statement Format (Concise)

> "In the context of [use case], facing [concern], we decided for [option] to achieve [quality], accepting [downside]."

---

## Trade-off Documentation

Always document trade-offs explicitly:

| Dimension | Option A | Option B | Decision |
|-----------|----------|----------|----------|
| Performance | High | Medium | A |
| Complexity | High | Low | B |
| Time to implement | Slow | Fast | B |
| Maintainability | Medium | High | B |
| **Choice** | | | **Option B** |

### Common Trade-off Categories

- **Build vs Buy**: Custom code vs third-party solution
- **Consistency vs Availability**: CAP theorem trade-offs
- **Performance vs Readability**: Optimization vs clean code
- **Flexibility vs Simplicity**: Generic vs specific solution
- **Speed vs Quality**: MVP vs production-ready

---

## Structuring for LLM Code Generation

Design docs should enable LLMs to generate code efficiently:

### 1. Be Explicit About Patterns

```markdown
## File Patterns

Follow existing pattern from `src/auth/handlers/login.ts`:
- Export single async handler function
- Use Zod for validation
- Return standardized response
- Log with context object
```

### 2. Provide Type Definitions

```typescript
// src/feature/types.ts

interface CreateUserRequest {
  email: string;     // RFC 5322 format
  password: string;  // Min 8 chars, 1 uppercase, 1 number
}

interface CreateUserResponse {
  user: {
    id: string;      // UUID v4
    email: string;
    createdAt: Date;
  };
}
```

### 3. Include API Contracts

```markdown
### POST /api/users

**Request:**
```json
{"email": "user@example.com", "password": "SecurePass1"}
```

**Response (201):**
```json
{"user": {"id": "uuid", "email": "user@example.com"}}
```

**Errors:** 400 (validation), 409 (exists), 500 (server)
```

### 4. Reference Existing Code

```markdown
## Implementation Reference

| Component | Pattern Source | What to Copy |
|-----------|----------------|--------------|
| Handler | `src/auth/handlers/login.ts` | Error handling, response format |
| Service | `src/auth/services/user.ts` | Dependency injection pattern |
| Tests | `tests/auth/login.test.ts` | Setup, mocking strategy |
```

---

## Document Types Comparison

### RFC (Request for Comments)

**Use when:** Proposing changes that need team consensus

**Structure:**
- Summary
- Motivation/Problem
- Proposed Solution
- Drawbacks
- Alternatives
- Implementation

**Companies using:** [Stripe, HashiCorp, Uber](https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design)

### TDD (Technical Design Document)

**Use when:** Detailed technical specification needed

**Structure:**
- System Overview
- Architecture
- Data Model
- API Specification
- Security
- Performance

**Companies using:** Many enterprise organizations

### ADR (Architecture Decision Record)

**Use when:** Recording a single architectural decision

**Structure:**
- Context
- Decision
- Consequences

**Best for:** Lightweight, decision-focused documentation

See [templates.md](templates.md) for full templates.

---

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Quality gate checklist |
| [examples.md](examples.md) | Real design doc examples |
| [templates.md](templates.md) | RFC, TDD, ADR templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for design |

---

## External Resources

### Company Design Doc Guides

- [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/) - Original post on Google's approach
- [RFC and Design Doc Examples](https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design) - Pragmatic Engineer
- [HashiCorp RFC Template](https://works.hashicorp.com/articles/rfc-template) - Detailed RFC structure

### ADR Resources

- [ADR GitHub](https://adr.github.io/) - Official ADR resources
- [ADR Templates](https://adr.github.io/adr-templates/) - Various template formats
- [AWS ADR Guide](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/) - AWS best practices

### LLM-Assisted Design

- [Addy Osmani's LLM Workflow](https://addyosmani.com/blog/ai-coding-workflow/) - Spec-first approach
- [Software Engineering with LLMs](https://newsletter.pragmaticengineer.com/p/software-engineering-with-llms-in-2025) - Reality check

---

*Methodology | SDD Foundation | Version 3.0.0*
*LLM-optimized design documentation*
