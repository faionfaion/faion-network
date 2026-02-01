# Specification Examples: Basic

## Example: Authentication Spec (Condensed)

This is a minimal, condensed specification example showing the core sections needed for a simple feature.

```markdown
# Feature: User Authentication

**Version:** 1.0
**Status:** Approved
**Project:** cashflow-planner

---

## Reference Documents

| Document | Path |
|----------|------|
| Constitution | `.aidocs/constitution.md` |

---

## Problem Statement

**Who:** New users of the cashflow planning app
**Problem:** Cannot access personal financial data because there's no authentication
**Impact:** Users cannot save cashflow projections, blocking core value proposition
**Solution:** Email-based authentication with JWT
**Success Metric:** 1000 registered users in first month

---

## User Stories

### US-001: Email Registration (MVP)
**As a** financial planner
**I want to** create an account with my email
**So that** I can save and access my cashflow projections

**Priority:** Must
**Acceptance Criteria:** AC-001, AC-002

---

## Functional Requirements

| ID | Requirement | Traces To | Priority |
|----|-------------|-----------|----------|
| FR-001 | System SHALL allow registration with email + password | US-001 | Must |
| FR-002 | System SHALL validate email format (RFC 5322) | US-001 | Must |
| FR-003 | System SHALL require password min 8 chars, 1 upper, 1 number | US-001 | Must |

---

## Acceptance Criteria

### AC-001: Successful Registration
**Given:** User is on registration page
**When:** User enters valid email and valid password
**Then:** Account is created
**And:** User receives verification email within 30 seconds
**And:** User is redirected to dashboard

### AC-002: Registration with Existing Email
**Given:** Email "test@example.com" exists in system
**When:** User tries to register with "test@example.com"
**Then:** Error message "Email already registered" is displayed
**And:** No duplicate account is created

---

## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| Social login | Not MVP | Phase 2 |
| 2FA | Complexity | Phase 3 |
```

---

## Key Characteristics of Condensed Specs

### When to Use

- MVP features with clear requirements
- Simple CRUD operations
- Well-understood patterns (auth, registration)
- Small team, fast iteration
- Proof of concept

### What to Include

**Minimum viable sections:**
1. Problem Statement
2. User Stories (1-3)
3. Functional Requirements
4. Acceptance Criteria (happy path + 1 error case)
5. Out of Scope

**Optional sections:**
- Non-functional requirements (add if critical)
- Dependencies (add if blocking)
- Assumptions (add if non-obvious)

### What to Skip

- Detailed personas (use simple "As a {role}")
- Extensive wireframes
- Multiple NFR categories
- Deep technical appendices
- Open questions section

### Token Estimation

| Section | Approx Tokens |
|---------|---------------|
| Problem Statement | 100-200 |
| User Stories (3) | 300-400 |
| Functional Req (5) | 200-300 |
| Acceptance Criteria (3) | 400-600 |
| Out of Scope | 100-150 |
| **Total** | **1100-1650** |

---

## Tips for Writing Condensed Specs

### Be Concise

```
❌ "The system shall provide users with the ability to create a new
   account using their email address and a secure password that meets
   our security requirements"

✅ "System SHALL allow registration with email + password"
```

### Focus on MUST requirements

```
❌ Include every possible requirement
✅ Only include MVP requirements (Must priority)
```

### Use Traceability

```
✅ FR-001 traces to US-001
✅ AC-001 validates US-001
```

### One Happy Path, One Error Case

```
✅ AC-001: Happy path (successful registration)
✅ AC-002: Error case (duplicate email)
❌ AC-003, AC-004, AC-005... (save for full spec)
```

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Planning task breakdown | haiku | Task decomposition from checklist |
| Estimating task complexity | sonnet | Comparative complexity assessment |
| Creating strategic roadmaps | opus | Long-term planning, dependency chains |

## Sources

- [OAuth 2.0 Framework](https://oauth.net/2/) - Authentication standard
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725) - JWT security guidelines
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) - Security practices
- [Passport.js Strategies](http://www.passportjs.org/packages/) - Authentication patterns
- [Auth0 Documentation](https://auth0.com/docs) - Modern auth implementation
