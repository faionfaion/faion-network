# M-SDD-003: Writing Design Documents

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-SDD-003 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #design |
| **Domain Skill** | faion-sdd-domain-skill |
| **Agents** | faion-design-reviewer-agent |

---

## Problem

Developers jump from requirements to coding without planning architecture. This causes:
- Inconsistent code patterns across the codebase
- Wrong technology choices discovered too late
- Rewrites when architecture doesn't scale
- Onboarding struggles - new devs can't understand the system

**The root cause:** No documented decisions about HOW to build.

---

## Framework

### What is a Design Document?

A design document answers: **"HOW are we building this?"**

It bridges the gap between specification (what) and implementation (code).

### Design vs Spec

| Aspect | Specification | Design |
|--------|---------------|--------|
| Question | What to build? | How to build it? |
| Audience | Stakeholders, PMs | Developers |
| Content | Requirements, acceptance criteria | Architecture, file structure |
| Changes | Needs approval | Technical decision |

### Design Document Structure

```markdown
# Design: [Feature Name]

## Overview
[Brief summary of technical approach]

## Architectural Decisions
[AD-1, AD-2, etc. with rationale]

## File Structure
[What files to create/modify]

## Data Models
[Database schemas, types]

## API Contracts
[Endpoints, request/response]

## Dependencies
[Libraries, services]

## Testing Strategy
[What and how to test]
```

### Writing Process

#### Step 1: Review the Specification
Read spec.md thoroughly. Understand:
- All functional requirements
- Non-functional requirements (performance, security)
- Acceptance criteria
- Scope boundaries

#### Step 2: Make Architectural Decisions
For each major technical choice, document:
- **Decision:** What you chose
- **Rationale:** Why you chose it
- **Alternatives:** What you considered
- **Consequences:** Trade-offs

Use AD-X format (Architectural Decision):

```markdown
### AD-1: Database Choice

**Decision:** Use PostgreSQL

**Rationale:**
- Need relational data (users, subscriptions, content)
- Complex queries for analytics
- Team has PostgreSQL experience

**Alternatives Considered:**
- MongoDB: Rejected - relational data fits better
- SQLite: Rejected - need concurrent writes

**Consequences:**
- Need to manage PostgreSQL server
- Get ACID compliance
- Complex queries are efficient
```

#### Step 3: Define File Structure
List every file to CREATE or MODIFY:

```markdown
## File Changes

| Action | File | Description |
|--------|------|-------------|
| CREATE | `src/auth/login.ts` | Login handler |
| CREATE | `src/auth/register.ts` | Registration handler |
| MODIFY | `src/middleware/auth.ts` | Add session validation |
| CREATE | `tests/auth.test.ts` | Auth unit tests |
```

#### Step 4: Specify Data Models
Define database schemas:

```markdown
## Data Models

### User
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  verified_at TIMESTAMP
);
```

### Session
```sql
CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  expires_at TIMESTAMP NOT NULL
);
```
```

#### Step 5: Document API Contracts
For each endpoint:

```markdown
## API Endpoints

### POST /api/auth/register

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "created_at": "2026-01-17T10:00:00Z"
}
```

**Errors:**
- 400: Invalid email format
- 409: Email already exists
```

#### Step 6: List Dependencies
Document external libraries and services:

```markdown
## Dependencies

### New Packages
| Package | Version | Purpose |
|---------|---------|---------|
| bcrypt | ^5.1.0 | Password hashing |
| jsonwebtoken | ^9.0.0 | JWT tokens |
| nodemailer | ^6.9.0 | Email sending |

### External Services
- SendGrid: Email delivery
- Redis: Session storage
```

---

## Templates

### Full Design Template

```markdown
# Design: [Feature Name]

**Version:** 1.0
**Spec:** [link to spec.md]
**Status:** Draft | Review | Approved
**Author:** [Name]
**Date:** YYYY-MM-DD

---

## Overview

[2-3 sentences summarizing technical approach]

---

## Architectural Decisions

### AD-1: [Decision Title]

**Decision:** [What you chose]

**Rationale:** [Why]

**Alternatives Considered:**
- [Option A]: [Why rejected]
- [Option B]: [Why rejected]

**Consequences:**
- [Trade-off 1]
- [Trade-off 2]

### AD-2: [Decision Title]
...

---

## File Structure

```
src/
├── feature/
│   ├── handlers/
│   │   ├── create.ts    # CREATE
│   │   └── update.ts    # CREATE
│   ├── models/
│   │   └── schema.ts    # CREATE
│   └── index.ts         # MODIFY
└── tests/
    └── feature.test.ts  # CREATE
```

### File Changes

| Action | File | Description | FR |
|--------|------|-------------|-----|
| CREATE | `src/feature/handlers/create.ts` | Create handler | FR-1 |
| CREATE | `src/feature/handlers/update.ts` | Update handler | FR-2 |
| MODIFY | `src/middleware/auth.ts` | Add permission check | FR-3 |

---

## Data Models

### [Model Name]

```typescript
interface ModelName {
  id: string;
  field1: string;
  field2: number;
  createdAt: Date;
}
```

**Database:**
```sql
CREATE TABLE model_name (
  id UUID PRIMARY KEY,
  field1 VARCHAR(255) NOT NULL,
  field2 INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Contracts

### [METHOD] /api/[endpoint]

**Description:** [What this endpoint does]

**Authentication:** Required | Optional | None

**Request:**
```json
{
  "field1": "value",
  "field2": 123
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "field1": "value",
  "createdAt": "2026-01-17T10:00:00Z"
}
```

**Errors:**
| Code | Reason |
|------|--------|
| 400 | Invalid input |
| 401 | Not authenticated |
| 404 | Not found |

---

## Dependencies

### Packages

| Package | Version | Purpose |
|---------|---------|---------|
| package-name | ^1.0.0 | Description |

### External Services

| Service | Purpose | Required |
|---------|---------|----------|
| Service Name | Description | Yes/No |

---

## Testing Strategy

### Unit Tests
- [ ] [Test case 1]
- [ ] [Test case 2]

### Integration Tests
- [ ] [Test case 1]

### E2E Tests
- [ ] [Test case 1]

---

## Security Considerations

- [Security measure 1]
- [Security measure 2]

---

## Performance Considerations

- [Performance optimization 1]
- [Performance optimization 2]

---

## Open Questions

- [ ] [Question to resolve]

---

## References

- [Link to related design]
- [External documentation]
```

---

## Examples

### Example: Authentication Design

```markdown
# Design: User Authentication

**Spec:** features/04-auth-system/spec.md
**Status:** Approved

---

## Overview

Implement JWT-based authentication with HTTP-only cookies.
Use PostgreSQL for user storage and Redis for session blacklist.

---

## Architectural Decisions

### AD-1: JWT in HTTP-only Cookies

**Decision:** Store JWT in HTTP-only cookies, not localStorage.

**Rationale:**
- Prevents XSS attacks (JavaScript can't read cookie)
- Automatic inclusion in requests
- Can set SameSite for CSRF protection

**Alternatives Considered:**
- localStorage: Rejected - vulnerable to XSS
- Session IDs: Rejected - requires server state

### AD-2: Access + Refresh Token Pattern

**Decision:** Use short-lived access tokens (15min) +
long-lived refresh tokens (7 days).

**Rationale:**
- Limits damage from token theft
- Good UX (not logging out constantly)
- Industry standard

---

## File Structure

```
src/
├── auth/
│   ├── handlers/
│   │   ├── register.ts   # CREATE
│   │   ├── login.ts      # CREATE
│   │   ├── logout.ts     # CREATE
│   │   └── refresh.ts    # CREATE
│   ├── middleware/
│   │   └── protect.ts    # CREATE
│   ├── utils/
│   │   ├── jwt.ts        # CREATE
│   │   └── password.ts   # CREATE
│   └── index.ts          # CREATE
└── tests/
    └── auth/
        ├── register.test.ts
        ├── login.test.ts
        └── jwt.test.ts
```

---

## API Contracts

### POST /api/auth/register

**Request:**
```json
{
  "email": "user@example.com",
  "password": "min8chars"
}
```

**Response (201):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com"
  }
}
```
*Sets HTTP-only cookie with access token*

### POST /api/auth/login

**Request:**
```json
{
  "email": "user@example.com",
  "password": "min8chars"
}
```

**Response (200):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com"
  }
}
```
*Sets HTTP-only cookies: access_token, refresh_token*
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No rationale for decisions | Always explain WHY, not just what |
| Missing file list | Every file touched must be listed |
| Vague API contracts | Specify exact request/response JSON |
| Forgetting security | Add security section for sensitive features |
| No testing strategy | Define what tests you'll write |

---

## Related Methodologies

- **M-SDD-002:** Writing Specifications
- **M-SDD-004:** Writing Implementation Plans
- **M-API-001:** REST API Design
- **M-API-004:** OpenAPI Specification

---

## Agent

**faion-design-reviewer-agent** reviews design documents. Invoke with:
- "Review this design for completeness"
- "Suggest architectural decisions for [feature]"
- "Generate API contracts from spec"

---

*Methodology M-SDD-003 | SDD Foundation | Version 1.0*
