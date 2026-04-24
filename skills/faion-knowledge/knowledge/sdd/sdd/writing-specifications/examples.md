# Specification Examples

Good vs bad spec examples with analysis. Learn from real patterns.

---

## Example 1: Authentication Feature

### Bad Spec

```markdown
# Authentication

We need to add user authentication to the app. Users should be able to
register and login. The system should be secure and fast. Handle errors
gracefully. Make it mobile-friendly.

Features:
- Registration
- Login
- Password reset
- Profile page

The design should look good and be easy to use.
```

**Problems:**

| Issue | Line | Problem |
|-------|------|---------|
| No structure | All | Missing sections, unorganized |
| Vague requirements | "secure and fast" | Not measurable |
| No acceptance criteria | Missing | No way to verify completion |
| Subjective language | "look good", "easy to use" | Not testable |
| No personas | Missing | Who are the users? |
| No priorities | Missing | What's MVP vs nice-to-have? |
| No constraints | Missing | What framework? What patterns? |

---

### Good Spec

```markdown
# Feature: User Authentication

**Version:** 1.0
**Status:** Approved
**Project:** cashflow-planner

---

## Reference Documents

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Tech stack, auth patterns |
| Design System | `.aidocs/design-system.md` | Form components |

---

## Problem Statement

**Who:** New users of the cashflow planning app
**Problem:** Cannot access personal financial data because there's no authentication
**Impact:** Users cannot save projections (0 retention, 0 revenue potential)
**Solution:** Email-based authentication with JWT
**Success Metric:** 1000 registered users in first month, 40% day-7 retention

---

## User Personas

### Persona 1: Financial Planner "Alex"
- **Role:** Freelance developer tracking client projects
- **Goal:** Save and access cashflow projections across devices
- **Pain Points:** Loses data when closing browser
- **Context:** Works from laptop and phone, uses Chrome

---

## User Stories

### US-001: Email Registration (MVP)
**As a** financial planner
**I want to** create an account with my email
**So that** I can save and access my cashflow projections

**Priority:** Must
**Acceptance Criteria:** AC-001, AC-002, AC-003
**Complexity:** Medium

### US-002: Email Login (MVP)
**As a** registered user
**I want to** login with my email and password
**So that** I can access my saved data

**Priority:** Must
**Acceptance Criteria:** AC-004, AC-005
**Complexity:** Low

### US-003: Password Reset (Should)
**As a** user who forgot my password
**I want to** reset my password via email
**So that** I can regain access to my account

**Priority:** Should
**Acceptance Criteria:** AC-006
**Complexity:** Medium

---

## Functional Requirements

| ID | Requirement | Traces To | Priority |
|----|-------------|-----------|----------|
| FR-001 | System SHALL allow registration with email + password | US-001 | Must |
| FR-002 | System SHALL validate email format per RFC 5322 | US-001 | Must |
| FR-003 | System SHALL require password: min 8 chars, 1 upper, 1 digit | US-001 | Must |
| FR-004 | System SHALL check email uniqueness before registration | US-001 | Must |
| FR-005 | System SHALL send verification email within 30 seconds | US-001 | Must |
| FR-006 | System SHALL authenticate users with email + password | US-002 | Must |
| FR-007 | System SHALL issue JWT with 15-minute expiry | US-002 | Must |
| FR-008 | System SHALL issue refresh token with 7-day expiry | US-002 | Must |
| FR-009 | System SHALL allow password reset via email link | US-003 | Should |
| FR-010 | System SHALL expire reset links after 1 hour | US-003 | Should |

### FR-001: Email Registration

**Requirement:** System SHALL allow users to register with email and password.

**Rationale:** Enables user identification for data persistence.

**Traces to:** US-001

**Validation Rules:**
- Email: valid RFC 5322 format, unique in system
- Password: minimum 8 characters, at least 1 uppercase letter, at least 1 digit

**Technical Notes:**
- Use existing `UserModel` from constitution
- Password hashing: bcrypt with 12 rounds
- Store in PostgreSQL `users` table

---

## Non-Functional Requirements

| ID | Category | Requirement | Target | Priority |
|----|----------|-------------|--------|----------|
| NFR-001 | Performance | Login response time | < 500ms p95 | Must |
| NFR-002 | Performance | Registration response time | < 1000ms p95 | Must |
| NFR-003 | Security | Password storage | bcrypt 12 rounds | Must |
| NFR-004 | Security | Transport | HTTPS only | Must |
| NFR-005 | Security | Rate limiting | 5 attempts/minute | Must |
| NFR-006 | Scalability | Concurrent users | 10,000 | Should |
| NFR-007 | Accessibility | Form inputs | WCAG 2.1 AA | Should |

---

## Acceptance Criteria

### AC-001: Successful Registration

**Scenario:** User registers with valid credentials

**Given:** User is on `/register` page
**And:** Email "newuser@example.com" does not exist in system
**When:** User enters email "newuser@example.com"
**And:** User enters password "SecurePass1"
**And:** User clicks "Create Account" button
**Then:** Account is created in `users` table
**And:** Verification email is sent within 30 seconds
**And:** User is redirected to `/verify-email` page
**And:** Success message "Check your email to verify your account" is displayed

### AC-002: Registration with Existing Email

**Scenario:** User tries to register with existing email

**Given:** Email "existing@example.com" exists in system
**When:** User enters email "existing@example.com"
**And:** User enters password "AnyPass123"
**And:** User clicks "Create Account" button
**Then:** Error message "An account with this email already exists" is displayed
**And:** No duplicate account is created
**And:** User remains on `/register` page

### AC-003: Registration with Invalid Password

**Scenario:** User enters weak password

**Given:** User is on `/register` page
**When:** User enters email "test@example.com"
**And:** User enters password "weak" (less than 8 chars, no uppercase, no digit)
**And:** User clicks "Create Account" button
**Then:** Error message "Password must be at least 8 characters with 1 uppercase letter and 1 number" is displayed
**And:** No account is created

### AC-004: Successful Login

**Scenario:** User logs in with correct credentials

**Given:** User "verified@example.com" exists and is verified
**And:** User is on `/login` page
**When:** User enters email "verified@example.com"
**And:** User enters password "CorrectPass1"
**And:** User clicks "Login" button
**Then:** JWT is issued and stored in httpOnly cookie
**And:** User is redirected to `/dashboard`

### AC-005: Login with Wrong Password

**Scenario:** User enters incorrect password

**Given:** User "test@example.com" exists
**When:** User enters email "test@example.com"
**And:** User enters password "WrongPassword1"
**And:** User clicks "Login" button
**Then:** Error message "Invalid email or password" is displayed
**And:** No JWT is issued
**And:** Failed attempt is logged

### AC-006: Password Reset Flow

**Scenario:** User successfully resets password

**Given:** User "forgot@example.com" exists
**When:** User clicks "Forgot Password" on login page
**And:** User enters email "forgot@example.com"
**And:** User clicks "Send Reset Link"
**Then:** Reset email is sent within 30 seconds
**And:** Email contains link with token valid for 1 hour

**Given:** User clicks valid reset link
**When:** User enters new password "NewSecure1"
**And:** User confirms password "NewSecure1"
**And:** User clicks "Reset Password"
**Then:** Password is updated in database
**And:** All existing sessions are invalidated
**And:** User is redirected to `/login`
**And:** Success message "Password reset successfully. Please login." is displayed

---

## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| Social login (Google, GitHub) | Not MVP priority | Phase 2 |
| Two-factor authentication | Complexity | Phase 3 |
| SSO/SAML | Enterprise feature | Not planned |
| Biometric authentication | Mobile only | v2.0 |
| Username-based login | Email preferred | Never |

---

## Assumptions & Constraints

### Assumptions
- Users have access to email for verification
- Users accept cookies for session management
- Email delivery service (SendGrid) is configured

### Constraints
- Must use existing tech stack from constitution (Next.js, PostgreSQL)
- Must follow existing component patterns in `src/components/`
- JWT implementation must use `jose` library (already in deps)

---

## Dependencies

### Internal
- Database schema (users table) - defined in constitution
- Email service configuration - already set up

### External
- SendGrid API for transactional emails
- PostgreSQL database

---

## Boundaries

### Always (Agent Can Do)
- Follow existing code patterns in `src/auth/`
- Run `npm test` before completing tasks
- Use TypeScript strict mode
- Add JSDoc comments to public functions

### Ask First (Requires Review)
- Changes to existing database schema
- New npm dependencies
- Changes to API response format

### Never
- Store passwords in plain text
- Log passwords or tokens
- Skip input validation
- Commit `.env` files
```

**Why This Works:**

| Aspect | Benefit |
|--------|---------|
| Clear structure | Agent knows where to find information |
| Specific values | "bcrypt 12 rounds" not "secure hashing" |
| Testable AC | Given-When-Then with concrete values |
| Explicit boundaries | Agent knows autonomy limits |
| Traceability | Requirements link to stories and AC |
| Out of scope | Prevents scope creep |

---

## Example 2: API Endpoint

### Bad Spec

```markdown
Add an API endpoint to get user data. It should return the user's
profile information. Make sure it's authenticated and handles errors.
```

**Problems:** No URL, no response format, no error codes, no auth method.

---

### Good Spec

```markdown
## FR-015: Get User Profile Endpoint

**Requirement:** System SHALL provide REST endpoint to retrieve authenticated user's profile.

**Traces to:** US-010

### Endpoint Specification

| Field | Value |
|-------|-------|
| Method | GET |
| Path | `/api/v1/users/me` |
| Auth | Bearer JWT in Authorization header |
| Rate Limit | 100 requests/minute |

### Request

```http
GET /api/v1/users/me
Authorization: Bearer <jwt_token>
```

### Response: Success (200)

```json
{
  "id": "usr_abc123",
  "email": "user@example.com",
  "name": "John Doe",
  "avatar_url": "https://cdn.example.com/avatars/abc123.jpg",
  "created_at": "2024-01-15T10:30:00Z",
  "email_verified": true
}
```

### Response: Unauthorized (401)

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired token"
  }
}
```

### Response: Not Found (404)

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User account no longer exists"
  }
}
```

### Acceptance Criteria

**AC-015-1: Successful Profile Retrieval**
Given: Valid JWT for user "usr_abc123"
When: GET request to `/api/v1/users/me`
Then: Response status is 200
And: Response body contains user id, email, name, avatar_url, created_at, email_verified

**AC-015-2: Missing Authorization Header**
Given: No Authorization header
When: GET request to `/api/v1/users/me`
Then: Response status is 401
And: Error code is "UNAUTHORIZED"

**AC-015-3: Expired Token**
Given: JWT that expired 1 hour ago
When: GET request to `/api/v1/users/me`
Then: Response status is 401
And: Error code is "UNAUTHORIZED"
```

---

## Example 3: UI Component

### Bad Spec

```markdown
Create a button component. It should have different variants and sizes.
Make it accessible.
```

---

### Good Spec

```markdown
## FR-020: Button Component

**Requirement:** System SHALL provide reusable Button component with variants and sizes.

**Traces to:** US-015

### Props Interface

```typescript
interface ButtonProps {
  /** Button visual style */
  variant: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive';
  /** Button size */
  size: 'sm' | 'md' | 'lg';
  /** Loading state shows spinner and disables interaction */
  loading?: boolean;
  /** Disabled state */
  disabled?: boolean;
  /** Full width button */
  fullWidth?: boolean;
  /** Click handler */
  onClick?: () => void;
  /** Button content */
  children: React.ReactNode;
}
```

### Visual Specifications

| Variant | Background | Text | Border | Hover |
|---------|------------|------|--------|-------|
| primary | `#2563EB` | `#FFFFFF` | none | `#1D4ED8` |
| secondary | `#F3F4F6` | `#374151` | none | `#E5E7EB` |
| outline | transparent | `#2563EB` | `1px #2563EB` | `#EFF6FF` |
| ghost | transparent | `#374151` | none | `#F3F4F6` |
| destructive | `#DC2626` | `#FFFFFF` | none | `#B91C1C` |

| Size | Height | Padding | Font Size |
|------|--------|---------|-----------|
| sm | 32px | 12px 16px | 14px |
| md | 40px | 16px 24px | 16px |
| lg | 48px | 20px 32px | 18px |

### Accessibility Requirements

- [ ] `role="button"` on non-button elements
- [ ] `aria-disabled="true"` when disabled
- [ ] `aria-busy="true"` when loading
- [ ] Focus visible ring: `2px solid #2563EB` with `2px offset`
- [ ] Keyboard activation: Enter and Space keys
- [ ] Minimum touch target: 44x44px

### Acceptance Criteria

**AC-020-1: Primary Button Renders**
Given: Button with `variant="primary"` and `size="md"`
When: Component renders
Then: Background color is `#2563EB`
And: Text color is `#FFFFFF`
And: Height is 40px

**AC-020-2: Loading State**
Given: Button with `loading={true}`
When: Component renders
Then: Spinner icon is visible
And: Button text is hidden but maintains width
And: `aria-busy="true"` is set
And: Click events are prevented

**AC-020-3: Keyboard Navigation**
Given: Button is focused
When: User presses Enter or Space
Then: onClick handler is called
And: Focus ring is visible (`2px solid #2563EB`)
```

---

## Anti-Patterns to Avoid

### 1. The Kitchen Sink Spec

**Problem:** Including every possible detail upfront.

```markdown
# Bad: 50 pages of requirements before any design

## User Stories (47 stories)
## Requirements (156 requirements)
## Acceptance Criteria (312 scenarios)
```

**Fix:** Start with MVP scope. Add detail iteratively.

### 2. The Copy-Paste Spec

**Problem:** Duplicating spec sections across features.

**Fix:** Reference shared components and patterns.

```markdown
## Reference
- Auth patterns: See `feature-001-auth/spec.md`
- Form validation: See `.aidocs/patterns/form-validation.md`
```

### 3. The Vague Spec

**Problem:** Requirements that can't be tested.

```markdown
# Bad
- System should be user-friendly
- Performance should be acceptable
- Security should be adequate
```

**Fix:** Quantify everything.

```markdown
# Good
- Task completion in < 3 clicks (usability)
- Response time < 500ms p95 (performance)
- bcrypt 12 rounds, JWT 15min expiry (security)
```

### 4. The Implementation-Coupled Spec

**Problem:** Dictating implementation instead of behavior.

```markdown
# Bad
- Use Redis for caching
- Create a useAuth hook
- Add middleware in auth.ts
```

**Fix:** Describe WHAT, let design describe HOW.

```markdown
# Good
- Session data SHALL be cached for performance
- Auth state SHALL be accessible throughout app
- API routes SHALL verify authentication
```

---

*Specification Examples | v1.0.0*
