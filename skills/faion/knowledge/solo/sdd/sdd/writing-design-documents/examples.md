# Design Document Examples

Real-world examples of design documents for different scenarios.

---

## Example 1: User Authentication Feature

A complete design document for adding user authentication to a web application.

```markdown
# Design: User Authentication System

**Version:** 1.0
**Spec:** `features/todo/01-auth/spec.md`
**Status:** Approved
**Author:** Engineering Team
**Date:** 2026-01-15

---

## Reference Documents

| Document | Path |
|----------|------|
| Constitution | `.aidocs/constitution.md` |
| Specification | `features/todo/01-auth/spec.md` |
| API Patterns | `src/api/CLAUDE.md` |

---

## Overview

Implement JWT-based authentication with email/password login. Uses HTTP-only cookies for token storage, bcrypt for password hashing, and Zod for validation.

---

## Spec Coverage

| FR/NFR | Requirement | Implemented By |
|--------|-------------|----------------|
| FR-001 | User registration | AD-001, AD-002 |
| FR-002 | Email validation | AD-001 |
| FR-003 | Password requirements | AD-002, AD-003 |
| FR-004 | Login with email/password | AD-001, AD-004 |
| FR-005 | Logout functionality | AD-004 |
| NFR-001 | Response < 500ms | AD-005 |
| NFR-002 | Password hashing (bcrypt) | AD-003 |

---

## Architectural Decisions

### AD-001: Use Zod for Request Validation

**Status:** Accepted

**Context:** Need type-safe validation for auth endpoints. Options include Joi, Yup, Zod.

**Decision:** Use Zod for request validation.

**Rationale:**
- TypeScript-first with automatic type inference
- Smaller bundle size than Joi
- Already used in project for other validations

**Alternatives Considered:**

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Joi | Mature, feature-rich | Large bundle, JS-first | Size, TS support |
| Yup | Popular, good TS | Less performant | Performance |
| Manual validation | No dependencies | Error-prone, verbose | Maintainability |

**Consequences:**
- **Positive:** Type-safe, consistent validation across API
- **Negative:** Team needs to learn Zod syntax
- **Risks:** None significant

**Traces to:** FR-001, FR-002, FR-003

---

### AD-002: Email Uniqueness Check Before Insert

**Status:** Accepted

**Context:** Need to ensure email uniqueness. Can check before insert or rely on DB constraint.

**Decision:** Check email existence before insert, with DB unique constraint as backup.

**Rationale:**
- Provides better error messages to user
- Faster feedback than waiting for DB error
- DB constraint catches race conditions

**Alternatives Considered:**

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| DB constraint only | Simpler | Generic error message | Poor UX |
| App check only | Good UX | Race condition possible | Data integrity |

**Consequences:**
- **Positive:** Good UX with specific error messages
- **Negative:** Extra DB query per registration

**Traces to:** FR-001, FR-002

---

### AD-003: bcrypt with Cost Factor 12

**Status:** Accepted

**Context:** Need secure password hashing. Options: bcrypt, argon2, scrypt.

**Decision:** Use bcrypt with cost factor 12.

**Rationale:**
- Industry standard, battle-tested
- Cost 12 balances security and performance (~250ms hash time)
- Well-supported in Node.js

**Alternatives Considered:**

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Argon2 | More secure, newer | Less mature ecosystem | Ecosystem |
| scrypt | Memory-hard | More complex config | Complexity |
| PBKDF2 | Standard | Slower for same security | Performance |

**Consequences:**
- **Positive:** Secure password storage
- **Negative:** ~250ms per hash operation
- **Risks:** None with proper implementation

**Traces to:** FR-003, NFR-002

---

### AD-004: JWT in HTTP-Only Cookie

**Status:** Accepted

**Context:** Need to store authentication token. Options: localStorage, sessionStorage, cookies.

**Decision:** Store JWT in HTTP-only, secure, SameSite=Strict cookie.

**Rationale:**
- HTTP-only prevents XSS access to token
- SameSite=Strict prevents CSRF
- Automatic inclusion in requests

**Alternatives Considered:**

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| localStorage | Easy JS access | XSS vulnerable | Security |
| sessionStorage | Tab-scoped | XSS vulnerable, no persistence | Security, UX |
| Authorization header | Standard | Requires JS storage | Security |

**Consequences:**
- **Positive:** Secure token storage
- **Negative:** CORS config needed for cross-origin
- **Risks:** Cookie size limits (4KB)

**Traces to:** FR-004, FR-005

---

### AD-005: Connection Pooling with pg-pool

**Status:** Accepted

**Context:** Need fast DB queries for auth. Single connections are slow.

**Decision:** Use pg-pool with pool size 10, idle timeout 30s.

**Rationale:**
- Reuses connections, reduces latency
- Handles connection lifecycle automatically
- Default settings suitable for our load

**Traces to:** NFR-001

---

## File Structure

```
src/
├── auth/
│   ├── handlers/
│   │   ├── register.ts    # CREATE - FR-001
│   │   ├── login.ts       # CREATE - FR-004
│   │   └── logout.ts      # CREATE - FR-005
│   ├── services/
│   │   ├── password.ts    # CREATE - FR-003
│   │   └── jwt.ts         # CREATE - AD-004
│   ├── middleware/
│   │   └── protect.ts     # CREATE - FR-004
│   ├── schemas/
│   │   └── auth.ts        # CREATE - AD-001
│   └── index.ts           # CREATE - router
└── tests/
    └── auth/
        ├── register.test.ts
        └── login.test.ts
```

### File Changes

| Action | File | Description | FR | AD |
|--------|------|-------------|----|----|
| CREATE | `src/auth/handlers/register.ts` | Registration endpoint | FR-001 | AD-001, AD-002 |
| CREATE | `src/auth/handlers/login.ts` | Login endpoint | FR-004 | AD-001, AD-004 |
| CREATE | `src/auth/handlers/logout.ts` | Logout endpoint | FR-005 | AD-004 |
| CREATE | `src/auth/services/password.ts` | Password hashing | FR-003 | AD-003 |
| CREATE | `src/auth/services/jwt.ts` | JWT utilities | FR-004 | AD-004 |
| CREATE | `src/auth/middleware/protect.ts` | Auth middleware | FR-004 | AD-004 |
| CREATE | `src/auth/schemas/auth.ts` | Zod schemas | FR-001-003 | AD-001 |
| CREATE | `src/auth/index.ts` | Router setup | All | - |
| MODIFY | `src/app.ts` | Mount auth routes | All | - |

---

## Data Models

### User

```typescript
// src/auth/types.ts

interface User {
  id: string;           // UUID v4
  email: string;        // Unique, RFC 5322 format
  passwordHash: string; // bcrypt hash
  createdAt: Date;
  verifiedAt: Date | null;
}
```

### Database Schema

```sql
-- migrations/001_create_users.sql

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  verified_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

---

## API Contracts

### POST /api/auth/register

**Summary:** Register a new user account

**Authentication:** None

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass1"
}
```

**Validation Rules:**
| Field | Rules |
|-------|-------|
| email | Required, RFC 5322 format, max 255 chars |
| password | Required, min 8 chars, 1 uppercase, 1 number |

**Response (201 Created):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "createdAt": "2026-01-19T10:00:00Z"
  }
}
```
*Sets HTTP-only cookie: access_token*

**Error Responses:**
| Code | Condition | Response |
|------|-----------|----------|
| 400 | Invalid email format | `{"error": "Invalid email format"}` |
| 400 | Password too weak | `{"error": "Password requires 8+ chars, 1 uppercase, 1 number"}` |
| 409 | Email exists | `{"error": "Email already registered"}` |
| 500 | Server error | `{"error": "Internal server error"}` |

---

### POST /api/auth/login

**Summary:** Authenticate user and create session

**Authentication:** None

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass1"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com"
  }
}
```
*Sets HTTP-only cookie: access_token*

**Error Responses:**
| Code | Condition | Response |
|------|-----------|----------|
| 400 | Missing fields | `{"error": "Email and password required"}` |
| 401 | Invalid credentials | `{"error": "Invalid email or password"}` |
| 500 | Server error | `{"error": "Internal server error"}` |

---

### POST /api/auth/logout

**Summary:** End user session

**Authentication:** Required

**Request:** No body required

**Response (200 OK):**
```json
{
  "message": "Logged out successfully"
}
```
*Clears access_token cookie*

---

## Dependencies

### Packages

| Package | Version | Purpose | License |
|---------|---------|---------|---------|
| bcrypt | ^5.1.0 | Password hashing | MIT |
| jsonwebtoken | ^9.0.0 | JWT tokens | MIT |
| zod | ^3.22.0 | Request validation | MIT |

### External Services

| Service | Purpose | Required | Fallback |
|---------|---------|----------|----------|
| PostgreSQL | User storage | Yes | SQLite (dev) |

---

## Security Considerations

| Concern | Mitigation | AD |
|---------|------------|-----|
| Password storage | bcrypt with cost 12 | AD-003 |
| XSS prevention | HTTP-only cookies | AD-004 |
| CSRF protection | SameSite=Strict | AD-004 |
| SQL injection | Parameterized queries | - |
| Rate limiting | 5 attempts/minute/IP | - |
| Timing attacks | Constant-time comparison | AD-003 |

---

## Performance Considerations

| Concern | Strategy | Target | AD |
|---------|----------|--------|-----|
| DB latency | Connection pooling | < 500ms p95 | AD-005 |
| Hash time | bcrypt cost 12 | < 300ms | AD-003 |
| Token validation | Stateless JWT | < 10ms | AD-004 |

---

## Testing Strategy

### Unit Tests
- Password hashing/verification
- JWT sign/verify functions
- Zod schema validation

### Integration Tests
- Register with valid/invalid data
- Login with correct/wrong credentials
- Logout clears cookie

### E2E Tests
- Full registration flow
- Login and access protected route
- Logout and verify access revoked

---

## Migration Strategy

### Data Migration
- No existing user data (greenfield)

### Rollback Plan
1. Disable feature flag
2. Routes return 503
3. No data rollback needed

---

**Status:** APPROVED - Ready for Implementation Plan
```

---

## Example 2: API Endpoint Addition (Simple)

A minimal design for adding a single endpoint.

```markdown
# Design: Get User Profile Endpoint

**Version:** 1.0
**Status:** Approved

---

## Overview

Add GET /api/users/me endpoint to return current user's profile.

---

## Spec Coverage

| FR | Requirement | Implemented By |
|----|-------------|----------------|
| FR-007 | View own profile | AD-001 |

---

## Architectural Decisions

### AD-001: Return Limited User Fields

**Decision:** Only return non-sensitive fields (id, email, createdAt).

**Rationale:** Never expose passwordHash or internal fields.

**Traces to:** FR-007

---

## File Changes

| Action | File | Description |
|--------|------|-------------|
| CREATE | `src/users/handlers/me.ts` | Profile endpoint |
| MODIFY | `src/users/index.ts` | Add route |
| CREATE | `tests/users/me.test.ts` | Tests |

---

## API Contract

### GET /api/users/me

**Authentication:** Required

**Response (200):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "createdAt": "2026-01-19T10:00:00Z"
  }
}
```

**Errors:** 401 (not authenticated)

---

**Status:** APPROVED
```

---

## Example 3: Database Migration Design

Design for a schema change.

```markdown
# Design: Add User Roles

**Version:** 1.0
**Status:** Approved

---

## Overview

Add role-based access control (RBAC) with predefined roles.

---

## Architectural Decisions

### AD-001: Enum for Role Values

**Decision:** Use PostgreSQL ENUM type for roles.

**Rationale:**
- Type safety at database level
- Smaller storage than VARCHAR
- Clear documentation of valid values

**Alternatives:**
| Alternative | Why Rejected |
|-------------|--------------|
| Roles table | Overkill for fixed roles |
| VARCHAR | No type safety |

---

## Data Models

### Role Enum

```sql
CREATE TYPE user_role AS ENUM ('user', 'admin', 'moderator');
```

### User Table Change

```sql
ALTER TABLE users ADD COLUMN role user_role DEFAULT 'user' NOT NULL;
```

### Migration

```sql
-- migrations/002_add_user_roles.sql

-- Up
CREATE TYPE user_role AS ENUM ('user', 'admin', 'moderator');
ALTER TABLE users ADD COLUMN role user_role DEFAULT 'user' NOT NULL;

-- Down
ALTER TABLE users DROP COLUMN role;
DROP TYPE user_role;
```

---

## Backwards Compatibility

- Default role is 'user' - existing users automatically get this
- API responses include role field
- Existing tokens remain valid

---

## Rollback Plan

1. Run down migration
2. Deploy previous API version
3. Role checks will be no-ops

---

**Status:** APPROVED
```

---

## Example 4: Frontend Component Design

Design for a React component.

```markdown
# Design: Registration Form Component

**Version:** 1.0
**Status:** Approved

---

## Overview

Create reusable registration form with validation and error handling.

---

## Component Hierarchy

```
<RegisterPage>
└── <AuthLayout>
    └── <RegisterForm>
        ├── <Input name="email" />
        ├── <Input name="password" type="password" />
        ├── <PasswordStrengthMeter />
        ├── <Button type="submit" />
        └── <FormError />
```

---

## Component Specifications

### RegisterForm

**Location:** `src/components/auth/RegisterForm.tsx`

**Props:**
```typescript
interface RegisterFormProps {
  onSuccess: (user: User) => void;
  onError?: (error: Error) => void;
}
```

**State:**
```typescript
interface FormState {
  email: string;
  password: string;
  isLoading: boolean;
  errors: Record<string, string>;
}
```

**Behavior:**
1. Validates email on blur
2. Shows password strength on input
3. Disables submit while loading
4. Shows field-level errors
5. Calls API and handles response

---

### PasswordStrengthMeter

**Location:** `src/components/auth/PasswordStrengthMeter.tsx`

**Props:**
```typescript
interface PasswordStrengthMeterProps {
  password: string;
}
```

**Visual:**
- Empty: Gray bar
- Weak: Red bar (25%)
- Fair: Orange bar (50%)
- Good: Yellow bar (75%)
- Strong: Green bar (100%)

---

## File Changes

| Action | File |
|--------|------|
| CREATE | `src/components/auth/RegisterForm.tsx` |
| CREATE | `src/components/auth/PasswordStrengthMeter.tsx` |
| CREATE | `src/components/auth/RegisterForm.test.tsx` |
| MODIFY | `src/components/auth/index.ts` |

---

## Accessibility

- Form has proper labels
- Error messages linked with aria-describedby
- Focus management on error
- Submit disabled state announced
- Password strength announced to screen readers

---

**Status:** APPROVED
```

---

## Quick Reference: What to Include

| Scenario | Sections Needed |
|----------|-----------------|
| New API endpoint | Overview, AD, File Changes, API Contract |
| Database change | Overview, AD, Data Models, Migration, Rollback |
| Frontend component | Overview, Component Hierarchy, Props/State, Accessibility |
| Full feature | All sections |

---

*Examples | SDD Documentation | Version 3.0.0*
