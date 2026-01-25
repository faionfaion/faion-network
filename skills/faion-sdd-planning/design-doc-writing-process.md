# Design Document Writing Process

## Writing Process

### Phase 1: Load Full SDD Context

Before writing, read and understand:

```
1. .aidocs/constitution.md - project principles, tech stack
2. .aidocs/contracts.md - existing API contracts
3. {FEATURE_DIR}/spec.md - requirements to implement (FR-X)
4. features/done/ - completed designs for patterns
```

Extract:
- Tech stack constraints (from constitution)
- Existing patterns (from done features)
- API naming conventions (from contracts)
- All FR-X and NFR-X to implement

### Phase 2: Codebase Research

**This phase is critical. Invest tokens here.**

#### 2.1 Find Existing Patterns

```bash
# Find similar implementations
Grep: pattern from spec keyword
Glob: **/similar_feature/**

# Find existing architecture patterns
Grep: class.*Service
Grep: class.*Controller
Grep: export.*Router

# Read project CLAUDE.md files
Read: app/CLAUDE.md
Read: app/components/CLAUDE.md
```

#### 2.2 Map Patterns for Each Component

| Component Type | Pattern Source | What to Extract |
|----------------|----------------|-----------------|
| API endpoints | existing routes | URL structure, middleware |
| Services | existing services | Base class, error handling |
| Models | existing models | Field naming, relationships |
| Components | existing UI | Props interface, styling |
| Tests | existing tests | Setup, mocking strategy |

### Phase 3: Create Traceability Matrix

**Every FR-X must map to at least one AD-X.**

```markdown
## Spec Coverage

| FR | Requirement Summary | Implemented By |
|----|---------------------|----------------|
| FR-001 | User registration | AD-001, AD-002 |
| FR-002 | Email validation | AD-001 |
| FR-003 | Password requirements | AD-002, AD-003 |
| NFR-001 | Response < 500ms | AD-004 |
| NFR-002 | bcrypt hashing | AD-003 |
```

### Phase 4: Architecture Decisions

#### 4.1 Decision Format (ADR-Style)

```markdown
### AD-001: [Decision Title]

**Context:** [Background, constraints, why decision needed]

**Decision:** [What was decided]

**Rationale:**
- [Reason 1]
- [Reason 2]
- [Reason 3]

**Alternatives Considered:**
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| [Option A] | [+] | [-] | [Reason] |
| [Option B] | [+] | [-] | [Reason] |

**Consequences:**
- **Positive:** [Benefits]
- **Negative:** [Trade-offs]
- **Risks:** [What could go wrong]

**Traces to:** FR-001, NFR-002
```

#### 4.2 Decision Categories

| Category | Examples |
|----------|----------|
| **Data** | Database choice, schema design, caching |
| **API** | REST vs GraphQL, authentication, versioning |
| **Architecture** | Monolith vs microservice, module structure |
| **Libraries** | Framework choice, utility libraries |
| **Security** | Auth mechanism, encryption, validation |
| **Performance** | Indexing, caching strategy, CDN |

### Phase 5: File Structure

#### 5.1 List All File Changes

```markdown
## File Changes

| Action | File | Description | FR | AD |
|--------|------|-------------|----|----|
| CREATE | `src/auth/handlers/register.ts` | Registration endpoint | FR-001 | AD-001 |
| CREATE | `src/auth/services/password.ts` | Password hashing | FR-003 | AD-003 |
| MODIFY | `src/middleware/auth.ts` | Add JWT validation | FR-004 | AD-002 |
| CREATE | `tests/auth/register.test.ts` | Registration tests | FR-001 | AD-001 |
```

#### 5.2 Directory Tree

```
src/
├── auth/
│   ├── handlers/
│   │   ├── register.ts    # CREATE - FR-001
│   │   ├── login.ts       # CREATE - FR-004
│   │   └── logout.ts      # CREATE - FR-005
│   ├── services/
│   │   ├── password.ts    # CREATE - FR-003
│   │   └── jwt.ts         # CREATE - FR-002
│   ├── middleware/
│   │   └── protect.ts     # CREATE - FR-006
│   └── index.ts           # CREATE - router
└── tests/
    └── auth/
        ├── register.test.ts
        └── login.test.ts
```

### Phase 6: Data Models

#### 6.1 TypeScript Types

```typescript
// src/auth/types.ts

interface User {
  id: string;           // UUID v4
  email: string;        // Unique, RFC 5322 format
  passwordHash: string; // bcrypt hash
  createdAt: Date;
  verifiedAt: Date | null;
}

interface Session {
  id: string;           // UUID v4
  userId: string;       // FK → User.id
  expiresAt: Date;      // 7 days from creation
}
```

#### 6.2 Database Schema

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

-- migrations/002_create_sessions.sql

CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
```

### Phase 7: API Contracts

#### 7.1 OpenAPI-Style Documentation

```markdown
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

**Request Validation:**
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
| 400 | Password too weak | `{"error": "Password must be 8+ chars with 1 uppercase and 1 number"}` |
| 409 | Email exists | `{"error": "Email already registered"}` |
| 500 | Server error | `{"error": "Internal server error"}` |
```

---

## Sources

- [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/) - API design practices
- [Thoughtworks Technology Radar](https://www.thoughtworks.com/radar) - Architecture trends
- [Martin Fowler's Refactoring Catalog](https://refactoring.com/catalog/) - Code patterns
- [Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/) - Enterprise patterns
- [Database Design Patterns](https://www.postgresql.org/docs/current/tutorial.html) - PostgreSQL best practices
