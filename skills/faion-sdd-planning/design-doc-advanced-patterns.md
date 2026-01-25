# Design Document Advanced Patterns

## Advanced Patterns

### Phase 8: Component Design (if frontend)

#### 8.1 Component Hierarchy

```
<AuthLayout>
├── <RegisterForm>
│   ├── <EmailInput />
│   ├── <PasswordInput />
│   ├── <PasswordStrengthMeter />
│   └── <SubmitButton />
└── <AuthFooter>
    └── <LoginLink />
```

#### 8.2 Component Specification

```markdown
### RegisterForm Component

**Location:** `src/components/auth/RegisterForm.tsx`

**Props:**
```typescript
interface RegisterFormProps {
  onSuccess: (user: User) => void;
  onError?: (error: Error) => void;
}
```

**State:**
- email: string
- password: string
- isLoading: boolean
- errors: ValidationErrors

**Behavior:**
1. Validates email format on blur
2. Shows password strength meter on input
3. Disables submit while loading
4. Calls onSuccess with user data
```

### Phase 9: Dependencies

#### 9.1 New Packages

| Package | Version | Purpose | License |
|---------|---------|---------|---------|
| bcrypt | ^5.1.0 | Password hashing | MIT |
| jsonwebtoken | ^9.0.0 | JWT tokens | MIT |
| zod | ^3.22.0 | Request validation | MIT |

#### 9.2 External Services

| Service | Purpose | Required | Fallback |
|---------|---------|----------|----------|
| SendGrid | Email delivery | Yes | Log to console (dev) |
| Redis | Session blacklist | No | In-memory (dev) |

### Phase 10: Security Considerations

| Concern | Mitigation | AD Reference |
|---------|------------|--------------|
| Password storage | bcrypt with cost 12 | AD-003 |
| XSS prevention | HTTP-only cookies | AD-002 |
| CSRF protection | SameSite=Strict cookie | AD-002 |
| SQL injection | Parameterized queries | AD-001 |
| Rate limiting | 5 attempts/minute/IP | AD-005 |
| Input validation | Zod schema validation | AD-001 |

### Phase 11: Performance Considerations

| Concern | Strategy | Target | AD Reference |
|---------|----------|--------|--------------|
| Login latency | Connection pooling | < 500ms p95 | AD-004 |
| Token validation | JWT (stateless) | < 10ms | AD-002 |
| Database queries | Indexed email lookup | < 50ms | AD-001 |
| Password hashing | bcrypt cost 12 | < 300ms | AD-003 |

### Phase 12: Testing Strategy

#### 12.1 Test Pyramid

```
         E2E Tests
        (Playwright)
       ┌───────────┐
       │  Critical │
       │  Flows    │
       └─────┬─────┘
             │
    Integration Tests
       (Supertest)
    ┌─────────────────┐
    │ API endpoints   │
    │ Service layers  │
    └───────┬─────────┘
            │
      Unit Tests
       (Vitest)
   ┌───────────────────┐
   │ Pure functions    │
   │ Utilities         │
   │ Validators        │
   └───────────────────┘
```

#### 12.2 Test Coverage Requirements

| Layer | Coverage Target | What to Test |
|-------|-----------------|--------------|
| Unit | 80%+ | Password hashing, JWT utils, validators |
| Integration | 100% endpoints | All API routes with happy/error paths |
| E2E | Critical flows | Registration, Login, Logout |

### Phase 13: Migration Strategy (if applicable)

```markdown
## Migration Strategy

### Data Migration
- No existing user data (greenfield)

### Backwards Compatibility
- N/A (new feature)

### Rollout Plan
1. Deploy database migrations
2. Deploy API changes (behind feature flag)
3. Enable feature flag for 10% users
4. Monitor error rates
5. Gradual rollout to 100%

### Rollback Plan
1. Disable feature flag
2. No data migration needed (new tables)
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No rationale for decisions | Always explain WHY, not just what |
| Missing file list | Every file touched must be listed |
| Vague API contracts | Specify exact request/response JSON |
| No traceability | Every AD must trace to FR-X |
| Forgetting security | Add security section for all features |
| No testing strategy | Define what tests you'll write |
| Missing alternatives | Document at least 2 alternatives per AD |
| No related designs | Check features/done/ for patterns |

---

## Sources

- [Google Engineering Practices](https://google.github.io/eng-practices/review/) - Google's design doc review process
- [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/) - Real-world practices
- [Amazon Architecture Principles](https://aws.amazon.com/architecture/well-architected/) - AWS Well-Architected Framework
- [Stripe API Design](https://stripe.com/docs/api) - API design patterns
- [Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications) - Testing strategy patterns
