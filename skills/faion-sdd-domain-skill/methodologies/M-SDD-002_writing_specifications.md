# M-SDD-002: Writing Specifications

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-SDD-002 |
| **Category** | SDD Foundation |
| **Difficulty** | Beginner |
| **Tags** | #methodology, #sdd, #specification |
| **Domain Skill** | faion-sdd-domain-skill |
| **Agents** | faion-spec-reviewer |

---

## Problem

Projects fail when teams build the wrong thing. This happens because:
- Requirements are vague or missing
- Stakeholders have different expectations
- Scope keeps changing during development
- No single source of truth for "what are we building?"

**The root cause:** No written specification that everyone agrees on.

---

## Framework

### What is a Specification?

A specification (spec) answers: **"WHAT are we building?"**

It does NOT answer "how" - that's for the design document.

### Spec Structure

```markdown
# Feature: [Name]

## Overview
[1-2 paragraphs explaining what this feature does]

## User Stories
[Who wants what, and why]

## Functional Requirements
[Specific, testable requirements]

## Non-Functional Requirements
[Performance, security, scalability]

## Acceptance Criteria
[How we know it's done]

## Out of Scope
[What we're explicitly NOT building]
```

### Writing Process

#### Step 1: Define the Problem
Write one paragraph explaining:
- Who has this problem?
- What is the problem?
- Why does it matter?

**Bad:** "Users need authentication"
**Good:** "New users cannot access premium content because there's no login system. This blocks monetization."

#### Step 2: Write User Stories
Format: As a [persona], I want [action], so that [benefit].

**Examples:**
- As a free user, I want to create an account, so that I can save my progress
- As a subscriber, I want to login with email, so that I can access paid content
- As an admin, I want to see user analytics, so that I can understand usage

#### Step 3: List Functional Requirements
Each requirement:
- Has unique ID (FR-1, FR-2, etc.)
- Is specific and testable
- Uses "shall" language

**Bad:** "The system should handle users"
**Good:** "FR-1: System shall allow users to register with email and password"

#### Step 4: Add Non-Functional Requirements
Cover:
- Performance (response times, throughput)
- Security (authentication, encryption)
- Scalability (expected load)
- Accessibility (WCAG level)

**Example:**
- NFR-1: Login shall complete in < 500ms
- NFR-2: Passwords shall be hashed with bcrypt
- NFR-3: System shall support 1000 concurrent users

#### Step 5: Define Acceptance Criteria
Use Given-When-Then format:

```
Given: [initial state]
When: [action]
Then: [expected result]
```

**Example:**
```
Given: User is on login page
When: User enters valid email and password
Then: User is redirected to dashboard
And: Session cookie is set
```

#### Step 6: Scope It Out
List what you're NOT building:
- Features for later phases
- Edge cases you'll ignore for now
- Integrations that aren't needed yet

---

## Templates

### Full Spec Template

```markdown
# Feature: [Feature Name]

**Version:** 1.0
**Status:** Draft | Review | Approved
**Author:** [Name]
**Date:** YYYY-MM-DD

---

## Overview

[2-3 sentences describing the feature]

---

## Problem Statement

[Who has this problem? What is the problem? Why does it matter?]

---

## User Stories

### US-01: [Story Title]
**As a** [persona]
**I want to** [action]
**So that** [benefit]

### US-02: [Story Title]
...

---

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | [Requirement] | Must |
| FR-2 | [Requirement] | Must |
| FR-3 | [Requirement] | Should |
| FR-4 | [Requirement] | Could |

---

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Response time | < 500ms |
| NFR-2 | Uptime | 99.9% |
| NFR-3 | Concurrent users | 1000 |

---

## Acceptance Criteria

### AC-01: [Criteria Title]
**Given:** [initial state]
**When:** [action]
**Then:** [expected result]

### AC-02: [Criteria Title]
...

---

## Out of Scope

- [Feature not included]
- [Integration not needed]
- [Edge case ignored]

---

## Dependencies

- [Other feature or external system]

---

## Open Questions

- [ ] [Question to resolve before design]

---

## Appendix

### Wireframes
[Link or embed]

### Data Models
[If known at spec stage]
```

### Requirement Checklist

```markdown
## Spec Quality Checklist

### Completeness
- [ ] Problem statement is clear
- [ ] All user personas covered
- [ ] All core features have requirements
- [ ] NFRs address performance, security, scalability

### Clarity
- [ ] Each requirement is specific
- [ ] No ambiguous words (good, fast, easy)
- [ ] Technical terms are defined
- [ ] Acceptance criteria are testable

### Consistency
- [ ] Requirement IDs are unique
- [ ] No conflicting requirements
- [ ] Scope is clearly defined

### Traceability
- [ ] Requirements link to user stories
- [ ] Acceptance criteria link to requirements
- [ ] Dependencies are documented
```

---

## Examples

### Example: Authentication Spec

```markdown
# Feature: User Authentication

**Version:** 1.0
**Status:** Approved

---

## Overview

Implement email-based authentication so users can register, login,
and access protected content.

---

## Problem Statement

Currently, all content is publicly accessible. We cannot:
- Track individual users
- Offer premium content
- Personalize experience

This blocks our monetization strategy.

---

## User Stories

### US-01: Registration
**As a** visitor
**I want to** create an account with my email
**So that** I can access member features

### US-02: Login
**As a** registered user
**I want to** login with my email and password
**So that** I can access my account

### US-03: Logout
**As a** logged-in user
**I want to** logout
**So that** I can secure my account on shared devices

---

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | System shall allow registration with email + password | Must |
| FR-2 | System shall validate email format | Must |
| FR-3 | System shall require password min 8 characters | Must |
| FR-4 | System shall send email verification | Should |
| FR-5 | System shall allow password reset via email | Must |

---

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Login response time | < 500ms |
| NFR-2 | Password storage | bcrypt, 12 rounds |
| NFR-3 | Session duration | 7 days |
| NFR-4 | Rate limiting | 5 attempts/minute |

---

## Acceptance Criteria

### AC-01: Successful Registration
**Given:** User is on registration page
**When:** User enters valid email and password (8+ chars)
**Then:** Account is created
**And:** User receives verification email
**And:** User is redirected to dashboard

### AC-02: Login with Valid Credentials
**Given:** User has verified account
**When:** User enters correct email and password
**Then:** User is logged in
**And:** Session is created for 7 days

---

## Out of Scope

- Social login (Google, GitHub) - Phase 2
- Two-factor authentication - Phase 3
- SSO/SAML - Not planned
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "System should be fast" | Specify: "Response time < 500ms" |
| Missing out-of-scope | Explicitly list what you're NOT building |
| Requirements without IDs | Always use FR-1, FR-2 format |
| Mixing what and how | Spec = what, Design = how |
| No acceptance criteria | Every requirement needs testable criteria |

---

## Related Methodologies

- **M-SDD-001:** SDD Workflow Overview
- **M-SDD-003:** Writing Design Documents
- **M-PRD-001:** MVP Scoping
- **M-PRD-006:** User Story Mapping

---

## Agent

**faion-spec-reviewer** reviews and improves specifications. Invoke with:
- "Review this spec for completeness"
- "Help me write user stories for [feature]"
- "Generate acceptance criteria for FR-1"

---

*Methodology M-SDD-002 | SDD Foundation | Version 1.0*
