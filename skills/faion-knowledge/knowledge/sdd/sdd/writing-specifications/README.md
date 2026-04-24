# Writing Specifications

> **Entry point:** `/faion-net` - invoke for automatic routing.

A practical guide to writing specifications that LLM coding agents can execute without clarification.

---

## What is a Specification?

A specification answers: **"WHAT are we building and WHY?"**

| Document | Question | Output |
|----------|----------|--------|
| **Specification** | WHAT and WHY? | Requirements, user stories, acceptance criteria |
| Design | HOW? | Architecture, API contracts, data models |
| Implementation Plan | IN WHAT ORDER? | Tasks, dependencies, token estimates |

The spec is the "intent" - the single source of truth for what gets built.

---

## Why Specs Matter for LLM Agents

Traditional specs were alignment artifacts between humans. LLM agents require specs that function as **programming interfaces**:

| Human Specs | LLM Agent Specs |
|-------------|-----------------|
| Narrative context | Structured data |
| Implied constraints | Explicit boundaries |
| Negotiable details | Precise requirements |
| Subjective success | Testable criteria |

**The specification becomes the source code for intent.**

---

## Spec Structure

### Minimal Viable Spec (MVS)

For simple tasks, use this minimal structure:

```markdown
# Feature: [Name]

## Problem
[Who cannot do what, and why it matters]

## Solution
[What to build - high level]

## Requirements
- FR-001: System SHALL [specific, testable requirement]
- FR-002: System SHALL [specific, testable requirement]

## Acceptance Criteria
### AC-001: [Happy Path]
Given [context]
When [action]
Then [expected result]

## Out of Scope
- [What we're NOT building]
```

### Full Spec Structure

For complex features, use the complete structure:

```markdown
# Feature: [Name]

## Reference Documents
[Links to constitution, related specs]

## Overview
[2-3 sentences describing feature and purpose]

## Problem Statement
- **Who:** [User persona]
- **Problem:** [What they cannot do]
- **Impact:** [Business/user impact]
- **Solution:** [High-level approach]
- **Success Metric:** [How we measure success]

## User Personas
[Brief persona descriptions with goals and pain points]

## User Stories
[As a X, I want Y, so that Z - with INVEST criteria]

## Functional Requirements
[FR-XXX with SMART criteria, MoSCoW priority, traceability]

## Non-Functional Requirements
[NFR-XXX for performance, security, scalability]

## Acceptance Criteria
[Given-When-Then format for all scenarios]

## Out of Scope
[Explicit exclusions with reasoning]

## Assumptions & Constraints
[Technical and business constraints]

## Dependencies
[Internal features, external services]
```

---

## Writing for LLM Execution

### The 6 Core Areas

Research across 2,500+ agent configurations identified six essential areas:

| Area | Purpose | Example |
|------|---------|---------|
| **Commands** | Executable commands with flags | `npm test`, `pytest -v` |
| **Testing** | Framework, location, coverage | "Tests in `__tests__/`, 80% coverage" |
| **Project Structure** | Directory layout with paths | `src/components/Button.tsx` |
| **Code Style** | Real code snippets > descriptions | Show actual pattern, not prose |
| **Git Workflow** | Branch naming, commit format | `feature/XXX-description` |
| **Boundaries** | What agents must never touch | "Never modify `.env`" |

### Three-Tier Boundary System

Define clear boundaries for agent autonomy:

```markdown
## Boundaries

### Always (Safe Actions)
- Run tests before committing
- Follow existing code patterns
- Add type annotations

### Ask First (High Impact)
- Database schema changes
- API contract modifications
- Dependency version upgrades

### Never (Hard Stops)
- Commit secrets or credentials
- Delete production data
- Bypass security checks
```

### Avoiding Ambiguity

| Ambiguous | Precise |
|-----------|---------|
| "Should be fast" | "Response time < 500ms p95" |
| "Handle errors gracefully" | "Display error message, log to Sentry, no stack traces to user" |
| "Support many users" | "10,000 concurrent connections" |
| "Good user experience" | "< 3 clicks to complete task" |
| "Secure authentication" | "bcrypt with 12 rounds, JWT with 15min expiry" |
| "Mobile friendly" | "Responsive breakpoints: 320px, 768px, 1024px" |

### Context Window Management

LLM context fills fast. Optimize your specs:

**Do:**
- Divide large specs into phases (backend/frontend sections)
- Use table format for dense information
- Reference external files instead of inlining
- Include only relevant code snippets

**Don't:**
- Dump 50 pages of documentation
- Repeat information across sections
- Include full file contents when excerpts suffice
- Add "nice to know" background

**The "Curse of Instructions":** As requirements pile up, model adherence drops. Aim for 150-200 focused instructions maximum.

---

## Requirements Engineering

### SMART Criteria

Every requirement must be:

| Criterion | Question | Bad | Good |
|-----------|----------|-----|------|
| **S**pecific | Exactly who and what? | "Users need auth" | "Unregistered users cannot create accounts" |
| **M**easurable | How to measure success? | "Should be fast" | "Login < 500ms p95" |
| **A**chievable | Technically feasible? | "AI reads minds" | "OAuth 2.0 with Google" |
| **R**elevant | Ties to business goal? | "Nice to have" | "Blocks monetization" |
| **T**ime-bound | Priority assigned? | "Eventually" | "Must have for MVP" |

### Requirement Format

```markdown
### FR-001: Email Registration

**Requirement:** System SHALL allow users to register with email and password.

**Rationale:** Enables user identification for premium features.

**Traces to:** US-001

**Priority:** Must

**Validation Rules:**
- Email: RFC 5322 format, unique in system
- Password: min 8 chars, 1 uppercase, 1 digit
```

### MoSCoW Prioritization

| Priority | Meaning | Decision |
|----------|---------|----------|
| **Must** | MVP requirement | Cannot launch without |
| **Should** | Important feature | Include if possible |
| **Could** | Nice to have | Only if time allows |
| **Won't** | Explicit exclusion | Not in this release |

---

## Acceptance Criteria

### Given-When-Then (BDD)

```markdown
### AC-001: Successful Registration

**Scenario:** User registers with valid credentials

**Given:** User is on registration page
**And:** Email "test@example.com" does not exist in system
**When:** User enters email "test@example.com" and password "SecurePass1"
**And:** User clicks "Register" button
**Then:** Account is created in database
**And:** User receives verification email within 30 seconds
**And:** User is redirected to dashboard
**And:** Success message "Check your email" is displayed
```

### Coverage Checklist

Every feature needs acceptance criteria for:

- [ ] **Happy path** - Main success scenario
- [ ] **Error handling** - Validation failures, edge cases
- [ ] **Boundary conditions** - Min/max values, empty states
- [ ] **Security scenarios** - Auth bypass, injection attempts
- [ ] **Performance scenarios** - Load, timeout handling
- [ ] **Accessibility** - Screen reader, keyboard navigation

### Specific Values

Always use concrete values in acceptance criteria:

| Vague | Specific |
|-------|----------|
| "valid email" | "test@example.com" |
| "wrong password" | "incorrect123" |
| "many items" | "1000 items" |
| "recent time" | "within 30 seconds" |

---

## User Stories

### INVEST Criteria

| Criterion | Question |
|-----------|----------|
| **I**ndependent | Can be delivered separately? |
| **N**egotiable | Details can be discussed? |
| **V**aluable | Delivers user/business value? |
| **E**stimable | Can estimate complexity? |
| **S**mall | Fits in one iteration? |
| **T**estable | Can write acceptance tests? |

### Story Format

```markdown
### US-001: Email Registration (MVP)

**As a** freelance developer
**I want to** create an account with my email
**So that** I can save my API keys and project settings

**Acceptance Criteria:** AC-001, AC-002
**Priority:** Must
**Complexity:** Medium
```

---

## External References

### Amazon 6-Pager
- [How to Write an Amazon 6-Pager](https://maestra.ai/blogs/how-to-write-an-amazon-6-pager)
- [Amazon 6-Pager Template](https://www.sixpagermemo.com/blog/amazon-six-pager-template)

Six sections: Introduction, Goals, Tenets, State of Business, Lessons Learned, Strategic Priorities.

### PRD Templates
- [AI PRD Template by OpenAI Product Lead](https://www.productcompass.pm/p/ai-prd-template)
- [ChatPRD Resources](https://www.chatprd.ai/resources/using-ai-to-write-prd)

### LLM-Specific Guides
- [How to Write a Good Spec for AI Agents](https://addyosmani.com/blog/good-spec/) - Addy Osmani
- [Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) - HumanLayer
- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices) - Anthropic

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Writing specification templates | haiku | Form completion, mechanical setup |
| Reviewing specifications for clarity | sonnet | Language analysis, logical consistency |
| Architecting complex system specs | opus | Holistic design, novel combinations |

## Related Methodologies

| Methodology | File | Purpose |
|-------------|------|---------|
| SMART Requirements | `faion-ba-core/smart-requirements.md` | Requirement criteria |
| Use Case Modeling | `faion-ba-core/use-case-modeling.md` | Complex workflows |
| User Story Mapping | `faion-ba-core/user-story-mapping.md` | Story organization |
| Acceptance Criteria | `faion-ba-core/acceptance-criteria.md` | BDD patterns |
| MVP Scoping | `faion-product-planning/mvp-scoping.md` | Prioritization |

---

## Files in This Directory

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Spec quality checklist |
| [examples.md](examples.md) | Good vs bad spec examples |
| [templates.md](templates.md) | Spec templates by type |
| [llm-prompts.md](llm-prompts.md) | Prompts for spec writing |

---

*Writing Specifications | SDD Foundation | v2.1.0*
