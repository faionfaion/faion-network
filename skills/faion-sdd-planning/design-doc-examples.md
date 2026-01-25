# Design Document Examples

## Example: User Authentication System

### Spec Coverage

| FR | Requirement Summary | Implemented By |
|----|---------------------|----------------|
| FR-001 | User registration with email/password | AD-001, AD-002, AD-003 |
| FR-002 | Email validation required | AD-001 |
| FR-003 | Password strength requirements (8+ chars, 1 uppercase, 1 number) | AD-002 |
| FR-004 | User login with JWT token | AD-004 |
| FR-005 | User logout | AD-004 |
| FR-006 | Protected routes middleware | AD-004 |
| NFR-001 | Response time < 500ms p95 | AD-005 |
| NFR-002 | bcrypt password hashing | AD-002 |
| NFR-003 | HTTP-only cookies for tokens | AD-003 |

### Architectural Decisions

#### AD-001: Email Validation Strategy

**Context:** Users must provide valid email addresses for account recovery and notifications.

**Decision:** Use Zod schema validation with RFC 5322 format check at API level.

**Rationale:**
- Immediate feedback to user on invalid format
- Prevents invalid data from reaching database
- Zod provides TypeScript type safety

**Alternatives Considered:**
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Database constraint only | Simple | No user feedback until commit | Poor UX |
| External email verification service | Catches typos | Adds latency, cost | Over-engineering for MVP |

**Consequences:**
- **Positive:** Fast validation, good UX, no external dependencies
- **Negative:** Won't catch typos in valid format emails
- **Risks:** Some valid emails might be rejected by strict RFC 5322

**Traces to:** FR-001, FR-002

#### AD-002: Password Hashing

**Context:** Passwords must be stored securely to prevent breaches.

**Decision:** Use bcrypt with cost factor 12.

**Rationale:**
- Industry standard for password hashing
- Adaptive work factor (can increase as hardware improves)
- Built-in salt generation
- Cost 12 balances security and performance (~300ms hash time)

**Alternatives Considered:**
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| SHA-256 | Fast | No salt, vulnerable to rainbow tables | Insecure |
| Argon2 | More secure | Less battle-tested, harder to configure | Over-engineering |
| Cost 10 | Faster | Weaker security | NFR-002 requires strong hashing |

**Consequences:**
- **Positive:** Strong security, proven algorithm
- **Negative:** ~300ms latency on registration/login
- **Risks:** Future hardware may require cost increase

**Traces to:** FR-001, FR-003, NFR-002

#### AD-003: Token Storage

**Context:** JWT tokens need storage mechanism that balances security and UX.

**Decision:** Store JWT in HTTP-only, SameSite=Strict cookies.

**Rationale:**
- HTTP-only prevents XSS attacks
- SameSite=Strict prevents CSRF attacks
- Cookies sent automatically with requests (better UX)

**Alternatives Considered:**
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| localStorage | Simple, works with CORS | Vulnerable to XSS | Security risk |
| sessionStorage | Simple | Lost on tab close | Poor UX |
| In-memory only | Most secure | Lost on refresh | Poor UX |

**Consequences:**
- **Positive:** Strong security, automatic handling
- **Negative:** Slightly more complex CORS setup
- **Risks:** Requires HTTPS in production

**Traces to:** FR-001, FR-004, NFR-003

#### AD-004: JWT vs Session-Based Auth

**Context:** Need authentication mechanism for protected routes.

**Decision:** Use JWT with 7-day expiration, no refresh tokens for MVP.

**Rationale:**
- Stateless authentication (no server-side session store)
- Scales horizontally (no shared state)
- Simpler implementation for MVP

**Alternatives Considered:**
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Session-based with Redis | Can revoke instantly | Requires Redis, stateful | More infrastructure |
| JWT with refresh tokens | Better security | Complex flow | Over-engineering for MVP |

**Consequences:**
- **Positive:** Simple, scalable, no external dependencies
- **Negative:** Cannot revoke tokens before expiration
- **Risks:** Compromised token valid for 7 days

**Traces to:** FR-004, FR-005, FR-006

#### AD-005: Connection Pooling

**Context:** Database queries must meet NFR-001 (< 500ms p95).

**Decision:** Use connection pooling with min=2, max=10 connections.

**Rationale:**
- Reduces connection overhead (~50ms per connection)
- Handles burst traffic efficiently
- Max 10 prevents database overload

**Alternatives Considered:**
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| No pooling | Simple | High latency | Fails NFR-001 |
| Higher max (20+) | More concurrency | Risk of DB overload | Over-provisioning |

**Consequences:**
- **Positive:** Consistent low latency, efficient resource use
- **Negative:** Slightly more memory usage
- **Risks:** Must monitor pool exhaustion

**Traces to:** NFR-001

---

## Example: File Structure for Auth Feature

```
src/
├── auth/
│   ├── handlers/
│   │   ├── register.ts       # CREATE - FR-001
│   │   ├── login.ts          # CREATE - FR-004
│   │   └── logout.ts         # CREATE - FR-005
│   ├── services/
│   │   ├── password.ts       # CREATE - FR-003 (bcrypt wrapper)
│   │   ├── jwt.ts            # CREATE - FR-002 (JWT utils)
│   │   └── email.ts          # CREATE - FR-002 (validation)
│   ├── middleware/
│   │   └── protect.ts        # CREATE - FR-006 (JWT verification)
│   ├── types.ts              # CREATE - Type definitions
│   └── index.ts              # CREATE - Router setup
├── database/
│   └── migrations/
│       ├── 001_users.sql     # CREATE - User table
│       └── 002_sessions.sql  # CREATE - Session tracking
└── tests/
    └── auth/
        ├── register.test.ts  # CREATE - Registration tests
        ├── login.test.ts     # CREATE - Login tests
        └── middleware.test.ts # CREATE - Middleware tests
```

### File Changes Table

| Action | File | Description | FR | AD |
|--------|------|-------------|----|----|
| CREATE | `src/auth/handlers/register.ts` | User registration endpoint | FR-001 | AD-001, AD-002 |
| CREATE | `src/auth/handlers/login.ts` | User login endpoint | FR-004 | AD-002, AD-004 |
| CREATE | `src/auth/handlers/logout.ts` | User logout endpoint | FR-005 | AD-004 |
| CREATE | `src/auth/services/password.ts` | Password hashing/verification | FR-003 | AD-002 |
| CREATE | `src/auth/services/jwt.ts` | JWT generation/verification | FR-004 | AD-003, AD-004 |
| CREATE | `src/auth/services/email.ts` | Email validation | FR-002 | AD-001 |
| CREATE | `src/auth/middleware/protect.ts` | JWT auth middleware | FR-006 | AD-004 |
| CREATE | `src/auth/types.ts` | TypeScript interfaces | FR-001 | - |
| CREATE | `src/auth/index.ts` | Router configuration | FR-001 | - |
| CREATE | `database/migrations/001_users.sql` | User table schema | FR-001 | - |
| CREATE | `database/migrations/002_sessions.sql` | Session tracking | FR-004 | - |
| CREATE | `tests/auth/register.test.ts` | Registration tests | FR-001 | - |
| CREATE | `tests/auth/login.test.ts` | Login tests | FR-004 | - |
| CREATE | `tests/auth/middleware.test.ts` | Middleware tests | FR-006 | - |

---

## Example: Component Hierarchy (Frontend)

```
<AuthLayout>
├── <RegisterForm>
│   ├── <EmailInput />
│   │   └── <ValidationMessage />
│   ├── <PasswordInput />
│   │   ├── <PasswordStrengthMeter />
│   │   └── <ShowPasswordToggle />
│   ├── <SubmitButton />
│   └── <FormError />
└── <AuthFooter>
    └── <LoginLink />
```

### Component Props

```typescript
// src/components/auth/RegisterForm.tsx
interface RegisterFormProps {
  onSuccess: (user: User) => void;
  onError?: (error: Error) => void;
  redirectPath?: string;
}

// src/components/auth/EmailInput.tsx
interface EmailInputProps {
  value: string;
  onChange: (value: string) => void;
  onBlur?: () => void;
  error?: string;
}

// src/components/auth/PasswordInput.tsx
interface PasswordInputProps {
  value: string;
  onChange: (value: string) => void;
  showStrengthMeter?: boolean;
  minLength?: number;
}
```

---

## Sources

- [Software Architecture Patterns](https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/) - O'Reilly architecture guide
- [Microsoft Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/) - Real-world patterns
- [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/) - Cloud architecture examples
- [System Design Primer](https://github.com/donnemartin/system-design-primer) - Comprehensive design patterns
- [The Twelve-Factor App](https://12factor.net/) - Modern application architecture
