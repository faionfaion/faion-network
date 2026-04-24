# Specification Requirements

## Methodology Reference

**Primary:** writing-specifications (Writing Specifications v2.0)

**Integrated:**
| Domain | Methodology | Principle Applied |
|--------|-------------|-------------------|
| BA | smart-requirements | SMART requirements criteria |
| BA | requirements-traceability | Requirements traceability (FR-X → US-X) |
| BA | use-case-modeling | Use Case diagrams and flows |
| BA | user-story-mapping | User Story Mapping |
| BA | acceptance-criteria | Acceptance criteria (Given-When-Then) |
| PdM | mvp-scoping | MVP scoping (MoSCoW prioritization) |
| PdM | user-story-mapping | User Story Mapping |
| PdM | spec-writing | PRD writing best practices |
| PM | scope-management | Scope Management |
| UX | user-research | User Research synthesis |
| UX | persona-development | Persona development |

---

## Problem Analysis (SMART)

### Define the Problem

| Criterion | Question | Bad Example | Good Example |
|-----------|----------|-------------|--------------|
| **S**pecific | Exactly who and what? | "Users need auth" | "New users cannot register" |
| **M**easurable | How to measure success? | "Should be fast" | "Registration < 3 seconds" |
| **A**chievable | Technically feasible? | "AI that reads minds" | "OAuth 2.0 integration" |
| **R**elevant | Ties to business goal? | "Nice to have" | "Blocks monetization" |
| **T**ime-bound | When needed? | "Eventually" | "Required for Q1 launch" |

### Business Value Statement

Format:
```
[WHO] currently cannot [WHAT] because [WHY].
This results in [IMPACT].
By implementing [SOLUTION], we will [BENEFIT].
```

Example:
```
New users currently cannot access premium content because there's no
login system. This results in $0 revenue from premium features.
By implementing email authentication, we will enable premium subscriptions.
```

---

## User Personas

| Field | Description |
|-------|-------------|
| **Name** | Archetype name |
| **Role** | What they do |
| **Goal** | What they want to achieve |
| **Pain Points** | Current frustrations |
| **Context** | When/where they use the product |

Example:
```markdown
### Persona 1: Freelance Developer "Alex"
- **Role:** Solo developer building SaaS products
- **Goal:** Ship MVPs quickly without server management
- **Pain Points:** Too much time on auth, payments, infra
- **Context:** Works from home, uses macOS, deploys to Vercel
```

---

## User Story Mapping

### Story Mapping Structure

```
                    ┌─────────────────────────────────────────┐
                    │             USER ACTIVITIES             │
                    │  (High-level goals: "Manage Account")   │
                    └─────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ↓                   ↓                   ↓
            ┌───────────┐       ┌───────────┐       ┌───────────┐
            │  BACKBONE │       │  BACKBONE │       │  BACKBONE │
            │ (Actions) │       │ (Actions) │       │ (Actions) │
            │ "Register"│       │  "Login"  │       │ "Logout"  │
            └───────────┘       └───────────┘       └───────────┘
                    │                   │                   │
        ┌───────────┼───────┐   ┌───────┼───────┐          │
        ↓           ↓       ↓   ↓       ↓       ↓          ↓
    ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
    │ MVP   │ │ MVP   │ │ v1.1  │ │ MVP   │ │ v1.1  │ │ MVP   │
    │US-001 │ │US-002 │ │US-005 │ │US-003 │ │US-006 │ │US-004 │
    └───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘

    ─────────── MVP (Walking Skeleton) ───────────────────────
    ─────────── v1.1 (Release 2) ─────────────────────────────
```

### Write User Stories

Format: As a [PERSONA], I want [ACTION], so that [BENEFIT].

**INVEST Criteria:**
| Criterion | Question |
|-----------|----------|
| **I**ndependent | Can be delivered separately? |
| **N**egotiable | Details can be discussed? |
| **V**aluable | Delivers user/business value? |
| **E**stimable | Can estimate effort? |
| **S**mall | Fits in one sprint/iteration? |
| **T**estable | Can write acceptance tests? |

Example:
```markdown
### US-001: Email Registration (MVP)
**As a** freelance developer (Alex)
**I want to** create an account with my email
**So that** I can save my API keys and project settings

**Acceptance Criteria:** (see AC-001)
**Priority:** Must (MVP)
**Estimate:** 3 story points
```

---

## Use Cases (For Complex Features)

When to use: Multi-step workflows, multiple actors, complex validations.

```markdown
### UC-001: User Registration

**Primary Actor:** Unregistered User
**Preconditions:** User is not logged in, has valid email

**Main Flow:**
1. User navigates to registration page
2. User enters email and password
3. System validates email format
4. System checks email uniqueness
5. System creates account
6. System sends verification email
7. User is redirected to dashboard

**Alternative Flows:**
- 3a. Invalid email format → Show error, return to step 2
- 4a. Email exists → Show "already registered" error

**Postconditions:** Account created, verification email sent
```

---

## Functional Requirements

### SMART Requirements

| Criterion | How to Apply |
|-----------|--------------|
| **Specific** | One interpretation only |
| **Measurable** | Testable with pass/fail |
| **Achievable** | Technically possible |
| **Relevant** | Traces to user story |
| **Time-bound** | Has priority (MoSCoW) |

### Requirements Format

```markdown
### FR-001: Email Registration

**Requirement:** System SHALL allow users to register with email and password.

**Rationale:** Enables user identification for premium features.

**Traces to:** US-001

**Acceptance Criteria:** AC-001, AC-002

**Priority:** Must

**Validation Rules:**
- Email: valid format, unique in system
- Password: min 8 chars, 1 uppercase, 1 number
```

### MoSCoW Prioritization

| Priority | Meaning | Example |
|----------|---------|---------|
| **Must** | MVP requirement, cannot launch without | Login, Core feature |
| **Should** | Important but not critical | Password reset |
| **Could** | Nice to have if time allows | Social login |
| **Won't** | Explicitly not in this release | SSO, 2FA |

---

## Non-Functional Requirements

### NFR Categories

| Category | What to Specify | Example |
|----------|-----------------|---------|
| **Performance** | Response times, throughput | < 500ms p95 latency |
| **Scalability** | Load capacity | 10k concurrent users |
| **Security** | Auth, encryption, compliance | bcrypt, HTTPS, GDPR |
| **Availability** | Uptime, recovery | 99.9% uptime, 4h RTO |
| **Accessibility** | WCAG level | WCAG 2.1 AA |
| **Usability** | UX metrics | < 3 clicks to complete |

### NFR Format

```markdown
### NFR-001: Login Performance

**Requirement:** Login response time SHALL be < 500ms for p95.

**Measurement:** Server-side response time, excluding network.

**Priority:** Must

**Validation:** Load test with 1000 concurrent users.
```

---

## Acceptance Criteria (BDD)

### Given-When-Then Format

```markdown
### AC-001: Successful Registration

**Scenario:** User registers with valid credentials

**Given:** User is on registration page
**And:** User has valid email not in system
**When:** User enters email "test@example.com" and password "SecurePass1"
**And:** User clicks "Register" button
**Then:** Account is created in database
**And:** User receives verification email within 30 seconds
**And:** User is redirected to dashboard
**And:** Success message "Check your email" is displayed
```

### Coverage Checklist

- [x] Happy path (main success scenario)
- [x] Error handling (validation failures)
- [ ] Boundary conditions (min/max values)
- [ ] Security scenarios (injection, auth bypass)
- [ ] Performance scenarios (load, timeout)
- [ ] Accessibility (screen reader, keyboard)

---

## Scope Definition

### In Scope

```markdown
## In Scope

- Email/password registration
- Email/password login
- Session management (7-day cookie)
- Password reset via email
- Basic profile (name, avatar)
```

### Out of Scope

```markdown
## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| Social login (Google, GitHub) | Not MVP | Phase 2 |
| Two-factor authentication | Complexity | Phase 3 |
| SSO/SAML | Enterprise only | Not planned |
| Biometric auth | Mobile-only | v2.0 |
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "System should be fast" | SMART: "Response time < 500ms p95" |
| No user personas | Define at least 2 personas |
| User stories without benefits | Always include "so that [benefit]" |
| Requirements without IDs | Always use FR-X, NFR-X format |
| No traceability | Every FR must trace to a user story |
| AC not testable | Use Given-When-Then with specific values |
| Missing out-of-scope | Explicitly list what you're NOT building |
| No related features | Check features/done/ for patterns |

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Planning task breakdown | haiku | Task decomposition from checklist |
| Estimating task complexity | sonnet | Comparative complexity assessment |
| Creating strategic roadmaps | opus | Long-term planning, dependency chains |

## Sources

- [SMART Goals Framework](https://www.projectsmart.co.uk/brief-history-of-smart-goals.php) - Goal-setting methodology
- [BABOK Guide](https://www.iiba.org/business-analysis-certifications/babok/) - Business Analysis Body of Knowledge
- [Behavior-Driven Development](https://cucumber.io/docs/bdd/) - BDD and Given-When-Then
- [MoSCoW Method](https://www.agilebusiness.org/page/ProjectFramework_10_MoSCoWPrioritisation) - Prioritization technique
- [Requirements Engineering Book](https://www.amazon.com/Requirements-Engineering-Fundamentals-Principles-Techniques/dp/3662622718) - RE fundamentals
