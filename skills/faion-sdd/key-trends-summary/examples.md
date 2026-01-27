# Real Examples of Modern SDD Practices

Practical examples demonstrating Specification-Driven Development trends in action.

**Version:** 1.0

---

## 1. Specification-Driven Development Examples

### Example 1.1: Feature Specification (E-Commerce Cart)

**Before SDD (vague prompt):**
```
Add a shopping cart to the e-commerce site
```

**After SDD (structured specification):**

```markdown
# SPEC: Shopping Cart Feature

## Problem Statement
Users cannot save items for later purchase, leading to abandoned sessions
and lost sales (current bounce rate: 67%).

## User Stories

### US-1: Add Item to Cart
As a logged-in user, I want to add products to my cart so I can purchase
multiple items in one transaction.

**Acceptance Criteria:**
- Given I am on a product page
- When I click "Add to Cart"
- Then the item appears in my cart with quantity 1
- And the cart icon shows updated item count
- And I see a confirmation toast

### US-2: Persistent Cart
As a user, I want my cart to persist across sessions so I don't lose
my selections.

**Acceptance Criteria:**
- Given I have items in cart
- When I close browser and return later
- Then my cart contains the same items
- And quantities are preserved

## Non-Functional Requirements
- NFR-1: Cart operations < 200ms response time
- NFR-2: Support 10,000 concurrent cart updates
- NFR-3: Cart data encrypted at rest

## Out of Scope
- Wishlist functionality (separate feature)
- Guest checkout cart merging (Phase 2)
- Multi-currency support

## Success Metrics
- Cart abandonment rate < 45% (from 67%)
- Add-to-cart conversion > 25%
- Page load with cart < 1.5s
```

### Example 1.2: SDD Workflow in Practice

**Real workflow from Anthropic (Claude Code):**

```
Step 1: User provides intent
"Add rate limiting to the API endpoints"

Step 2: LLM drafts spec
- Identifies affected endpoints
- Proposes rate limits (100/min authenticated, 20/min anonymous)
- Lists edge cases (burst handling, distributed systems)
- Suggests Redis for distributed counting

Step 3: Human reviews spec
- Adjusts limits based on business needs
- Adds requirement for graceful degradation
- Specifies header format for rate limit info

Step 4: LLM creates implementation plan
- Task 1: Add Redis dependency
- Task 2: Create rate limiter middleware
- Task 3: Apply to routes
- Task 4: Add tests
- Task 5: Update API docs

Step 5: Human approves plan
- Confirms task ordering
- Validates file list
- Approves estimated scope

Step 6: LLM executes tasks
- Generates code for each task
- Runs tests after each step
- Commits atomically

Step 7: Human reviews output
- Code review
- Integration testing
- Merge decision
```

---

## 2. Architecture Decision Record Examples

### Example 2.1: Database Selection ADR

```markdown
# ADR-0042: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need to select a primary database for the new inventory management
system. The system will handle:
- 500K products
- 10M daily transactions
- Complex queries with joins
- Need for ACID compliance
- Full-text search requirements

Current options considered:
1. PostgreSQL
2. MySQL
3. MongoDB
4. CockroachDB

## Decision
We will use PostgreSQL 16 as our primary database.

## Rationale
- **JSONB support**: Flexible schema for product attributes
- **Full-text search**: Built-in FTS eliminates need for Elasticsearch
- **Mature ecosystem**: pg_stat_statements, pg_repack, robust tooling
- **Team expertise**: 4/5 backend engineers have PostgreSQL experience
- **Cost**: Open source, no licensing fees
- **Performance**: Benchmarks show 15% faster for our query patterns vs MySQL

## Consequences

### Positive
- Reduced infrastructure complexity (no separate search service)
- Team can be productive immediately
- Strong community support for issues
- Built-in partitioning for large tables

### Negative
- Horizontal scaling requires careful planning (pg_shard or Citus)
- Some NoSQL patterns need workarounds
- Need to train one engineer on advanced PostgreSQL

### Risks
- If we exceed 10TB, may need distributed PostgreSQL solution
- Mitigation: Design schema for future partitioning

## Alternatives Rejected

### MongoDB
- Team lacks expertise
- ACID transactions only at document level
- Would need separate search solution

### MySQL
- Weaker JSONB support
- Full-text search less capable
- No significant advantages for our use case

### CockroachDB
- Overkill for current scale
- Higher operational complexity
- More expensive (cloud managed)

## Related Decisions
- ADR-0038: Use Docker for all services
- ADR-0041: Adopt event sourcing for audit trail

## References
- Benchmark results: /docs/benchmarks/db-comparison.md
- PostgreSQL 16 release notes: [link]
```

### Example 2.2: ADR for Adopting SDD

```markdown
# ADR-0001: Adopt Specification-Driven Development

## Status
Accepted

## Context
Our team is experiencing:
- Inconsistent code quality from AI assistants
- Lack of documentation for new features
- Difficulty onboarding new team members
- Repeated discussions about "why we did X"

AI coding assistants (Claude Code, Cursor) are capable of generating
code but produce better results with structured input.

## Decision
We will adopt Specification-Driven Development (SDD) for all new
features and significant changes.

This means:
1. Every feature starts with a specification document
2. Specifications are reviewed before implementation
3. AI assistants receive specs as context
4. Implementation plans break work into reviewable chunks

## Workflow
```
Spec → Review → Design → Plan → Execute → Review → Merge
```

## Consequences

### Positive
- Better AI-generated code quality
- Built-in documentation
- Clearer requirements before coding
- Easier code reviews (compare output to spec)
- Historical record of decisions

### Negative
- Initial slowdown for spec writing
- Learning curve for team
- Need to maintain spec discipline

### Neutral
- Requires process change
- New tooling (templates, linting)

## Implementation
- Week 1-2: Create templates, train team
- Week 3-4: Pilot on 2-3 features
- Week 5+: Full adoption

## Success Metrics
- Spec exists for 100% of new features (after Week 5)
- AI code acceptance rate > 70%
- Documentation always matches implementation

## References
- Thoughtworks SDD article: [link]
- Martin Fowler SDD tools analysis: [link]
```

---

## 3. Living Documentation Examples

### Example 3.1: Auto-Generated API Docs

**OpenAPI Spec (source of truth):**

```yaml
openapi: 3.1.0
info:
  title: Inventory API
  version: 2.1.0
  description: |
    API for managing product inventory.

    ## Authentication
    All endpoints require Bearer token in Authorization header.

    ## Rate Limits
    - Authenticated: 1000 requests/minute
    - Per-endpoint limits in endpoint descriptions

paths:
  /products:
    get:
      summary: List products
      description: |
        Returns paginated list of products.
        Supports filtering, sorting, and full-text search.
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: search
          in: query
          description: Full-text search across name and description
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProductList'
```

**Generated Documentation Pipeline:**

```yaml
# .github/workflows/docs.yml
name: Generate API Docs

on:
  push:
    paths:
      - 'api/openapi.yaml'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate HTML docs
        run: |
          npx redocly build-docs api/openapi.yaml -o docs/api/index.html

      - name: Generate SDK
        run: |
          npx openapi-generator-cli generate \
            -i api/openapi.yaml \
            -g typescript-axios \
            -o sdk/typescript

      - name: Run contract tests
        run: |
          npx dredd api/openapi.yaml http://localhost:3000

      - name: Deploy to portal
        run: |
          aws s3 sync docs/ s3://developer-portal/api/
```

### Example 3.2: CLAUDE.md for Project Context

```markdown
# CLAUDE.md - Project Context for LLM Assistants

## Project Overview
E-commerce platform built with:
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: Node.js, Express, PostgreSQL
- **Infrastructure**: AWS ECS, RDS, ElastiCache

## Code Standards

### TypeScript
- Strict mode enabled
- No `any` types (use `unknown` if needed)
- Prefer interfaces over types for objects
- Use Zod for runtime validation

### Naming Conventions
- Components: PascalCase (`ProductCard.tsx`)
- Hooks: camelCase with `use` prefix (`useCart.ts`)
- Utils: camelCase (`formatPrice.ts`)
- Constants: SCREAMING_SNAKE_CASE

### File Structure
```
src/
├── components/     # React components
│   ├── ui/         # Generic UI (Button, Input)
│   └── features/   # Feature-specific (Cart, Product)
├── hooks/          # Custom React hooks
├── lib/            # Utilities and helpers
├── services/       # API clients
└── types/          # TypeScript types
```

## Patterns to Follow

### API Calls
```typescript
// Always use the api client
import { api } from '@/services/api';

// Good
const products = await api.products.list({ page: 1 });

// Bad - direct fetch
const response = await fetch('/api/products');
```

### Error Handling
```typescript
// Use Result pattern
type Result<T> = { ok: true; data: T } | { ok: false; error: string };

// Good
async function getProduct(id: string): Promise<Result<Product>> {
  try {
    const product = await api.products.get(id);
    return { ok: true, data: product };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}
```

## Anti-Patterns to Avoid

- No inline styles (use Tailwind classes)
- No `console.log` in production code (use logger)
- No hardcoded API URLs (use environment variables)
- No mutation of props or state directly
- No synchronous file operations in API routes

## Testing Requirements

- Unit tests for all utils (100% coverage target)
- Component tests for user interactions
- Integration tests for API routes
- E2E tests for critical paths (checkout, auth)

## Recent Decisions

- ADR-0042: PostgreSQL for primary database
- ADR-0045: Redis for session storage
- ADR-0048: Feature flags via LaunchDarkly

## Current Focus

Working on: Shopping Cart Feature (SPEC-024)
Blocked by: Nothing
Next up: Checkout Flow (SPEC-025)
```

---

## 4. LLM-First Workflow Examples

### Example 4.1: Context Packing

**Ineffective context:**
```
Add user authentication to the app
```

**Effective context packing:**
```markdown
# Task: Add User Authentication

## Project Context
- Next.js 14 with App Router
- PostgreSQL database with Prisma ORM
- Currently no auth, all routes public
- Using Tailwind CSS and shadcn/ui components

## Requirements
1. Email/password authentication
2. OAuth with Google and GitHub
3. JWT tokens stored in HTTP-only cookies
4. Protected routes with middleware
5. User profile page

## Constraints
- Must use existing User table schema
- No third-party auth services (self-hosted)
- Session timeout: 7 days
- Password: min 8 chars, 1 number, 1 special

## Examples of Good Implementation
See `/src/lib/auth.example.ts` for our auth pattern.
Password hashing uses bcrypt with 12 rounds.

## Avoid
- Do NOT use localStorage for tokens
- Do NOT store plaintext passwords
- Do NOT use deprecated crypto functions

## Files to Modify
- prisma/schema.prisma (add Session model)
- src/middleware.ts (create, add auth check)
- src/app/api/auth/* (create routes)
- src/components/auth/* (create forms)

## Acceptance Criteria
- [ ] User can register with email/password
- [ ] User can login/logout
- [ ] Protected routes redirect to login
- [ ] OAuth providers work
- [ ] Tests pass
```

### Example 4.2: Agentic Workflow with MCP

```markdown
# Multi-Agent Development Session

## Agent Configuration

### Primary Agent (Claude Code)
Role: Code generation and implementation
Tools:
- File read/write
- Terminal (git, npm, test runners)
- Web search for documentation

### Review Agent
Role: Code review and quality checks
Tools:
- Static analysis (ESLint, TypeScript)
- Security scanning (Semgrep)
- Test coverage analysis

### Documentation Agent
Role: Documentation updates
Tools:
- Markdown linting
- Link checking
- API doc generation

## Workflow

```
User Intent
    ↓
Primary Agent: Generate Spec
    ↓
Human: Review/Approve Spec
    ↓
Primary Agent: Generate Code
    ↓
Review Agent: Automated Review
    ↓
Primary Agent: Fix Issues
    ↓
Documentation Agent: Update Docs
    ↓
Human: Final Review
    ↓
Merge
```

## MCP Server Configuration

```json
{
  "servers": {
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["--root", "/project"]
    },
    "github": {
      "command": "mcp-server-github",
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "mcp-server-postgres",
      "args": ["--connection-string", "${DATABASE_URL}"]
    }
  }
}
```
```

---

## 5. Platform Engineering Examples

### Example 5.1: Backstage Service Catalog Entry

```yaml
# catalog-info.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: inventory-service
  description: Manages product inventory and stock levels
  annotations:
    github.com/project-slug: 'company/inventory-service'
    backstage.io/techdocs-ref: dir:.
    pagerduty.com/service-id: 'P123ABC'
  tags:
    - python
    - fastapi
    - postgresql
  links:
    - url: https://inventory.internal.company.com/docs
      title: API Documentation
    - url: https://grafana.company.com/d/inventory
      title: Grafana Dashboard
spec:
  type: service
  lifecycle: production
  owner: team-platform
  system: e-commerce
  dependsOn:
    - component:default/postgresql
    - component:default/redis
  providesApis:
    - inventory-api
---
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: inventory-api
  description: REST API for inventory operations
spec:
  type: openapi
  lifecycle: production
  owner: team-platform
  definition:
    $text: ./openapi.yaml
```

### Example 5.2: Golden Path Template

```yaml
# template.yaml - New Service Template
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: python-fastapi-service
  title: Python FastAPI Service
  description: Create a new Python microservice with FastAPI
  tags:
    - python
    - fastapi
    - recommended
spec:
  owner: platform-team
  type: service

  parameters:
    - title: Service Details
      required:
        - name
        - owner
      properties:
        name:
          title: Service Name
          type: string
          pattern: '^[a-z0-9-]+$'
        owner:
          title: Owner Team
          type: string
          ui:field: OwnerPicker
        description:
          title: Description
          type: string

    - title: Infrastructure
      properties:
        database:
          title: Database
          type: string
          enum: ['postgresql', 'none']
          default: 'postgresql'
        redis:
          title: Redis Cache
          type: boolean
          default: false

  steps:
    - id: fetch-base
      name: Fetch Base Template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          name: ${{ parameters.name }}
          owner: ${{ parameters.owner }}
          database: ${{ parameters.database }}

    - id: create-repo
      name: Create GitHub Repository
      action: github:repo:create
      input:
        repoUrl: github.com?owner=company&repo=${{ parameters.name }}

    - id: setup-cicd
      name: Configure CI/CD
      action: github:actions:workflow
      input:
        repoUrl: ${{ steps.create-repo.output.repoUrl }}
        workflow: .github/workflows/ci.yml

    - id: register-catalog
      name: Register in Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.create-repo.output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'

  output:
    links:
      - title: Repository
        url: ${{ steps.create-repo.output.remoteUrl }}
      - title: Open in Catalog
        icon: catalog
        entityRef: ${{ steps.register-catalog.output.entityRef }}
```

---

## 6. Observability Examples

### Example 6.1: OpenTelemetry Integration

```python
# Python FastAPI with OpenTelemetry

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

# Configure resource
resource = Resource.create({
    "service.name": "inventory-service",
    "service.version": "1.2.3",
    "deployment.environment": os.getenv("ENVIRONMENT", "development"),
})

# Configure tracer
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_ENDPOINT", "localhost:4317")
))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Auto-instrument
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)

# Custom span example
tracer = trace.get_tracer(__name__)

@app.post("/orders")
async def create_order(order: OrderCreate):
    with tracer.start_as_current_span("create_order") as span:
        span.set_attribute("order.items_count", len(order.items))
        span.set_attribute("order.customer_id", order.customer_id)

        # Validate inventory
        with tracer.start_as_current_span("validate_inventory"):
            available = await check_inventory(order.items)
            span.set_attribute("inventory.all_available", available)

        if not available:
            span.set_status(Status(StatusCode.ERROR))
            raise HTTPException(400, "Items not available")

        # Process order
        with tracer.start_as_current_span("process_order"):
            result = await process_order(order)
            span.set_attribute("order.id", result.id)

        return result
```

### Example 6.2: Structured Logging

```typescript
// TypeScript structured logging with correlation

import pino from 'pino';
import { trace, context } from '@opentelemetry/api';

const logger = pino({
  formatters: {
    log(object) {
      // Add trace context to every log
      const span = trace.getSpan(context.active());
      if (span) {
        const spanContext = span.spanContext();
        return {
          ...object,
          trace_id: spanContext.traceId,
          span_id: spanContext.spanId,
        };
      }
      return object;
    },
  },
});

// Usage in service
async function processPayment(orderId: string, amount: number) {
  const log = logger.child({
    operation: 'processPayment',
    orderId,
    amount,
  });

  log.info('Starting payment processing');

  try {
    const result = await paymentGateway.charge(amount);
    log.info({
      transactionId: result.id,
      status: result.status,
    }, 'Payment processed successfully');
    return result;
  } catch (error) {
    log.error({
      error: error.message,
      code: error.code,
    }, 'Payment processing failed');
    throw error;
  }
}
```

---

## Summary

These examples demonstrate:

1. **SDD**: Transform vague requirements into structured specifications
2. **ADRs**: Document decisions with context, rationale, and consequences
3. **Living Docs**: Keep documentation in sync with code automatically
4. **LLM-First**: Pack context effectively for better AI assistance
5. **Platform Engineering**: Self-service developer experience
6. **Observability**: Instrument from day one with OTel

---

## Resources

- [README.md](README.md) - Overview and context
- [checklist.md](checklist.md) - Adoption checklist
- [templates.md](templates.md) - Copy-paste templates
- [llm-prompts.md](llm-prompts.md) - Effective prompts

---

*Examples Document | Modern SDD Practices | Version 1.0*
