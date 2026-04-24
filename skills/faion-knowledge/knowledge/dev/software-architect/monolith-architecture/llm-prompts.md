# LLM Prompts for Monolith Architecture

Effective prompts for AI-assisted monolith design, development, and optimization.

## Architecture Decision Prompts

### Should I Use a Monolith?

```
I'm starting a new project with these characteristics:
- Team size: [X] developers
- Budget: [tight/moderate/flexible]
- Timeline: [MVP in X months / long-term product]
- Domain complexity: [simple CRUD / moderate / complex domain logic]
- Expected scale: [X users, Y requests/second]
- DevOps expertise: [none / basic / experienced]

Questions:
1. Should I start with a monolith or microservices?
2. If monolith, what type? (traditional / modular / vertical slices)
3. What are the key risks with this choice?
4. At what point should I reconsider this architecture?
```

### Architecture Pattern Selection

```
I'm building a [type of application] with these requirements:
- [List main features]
- [Data consistency requirements]
- [Performance requirements]
- [Team structure]

My tech stack is [Python/Django | Node.js/Express | Go | etc.].

Compare these monolith patterns for my use case:
1. Layered architecture
2. Vertical slice architecture
3. Modular monolith with DDD
4. Clean/Hexagonal architecture

For each, explain:
- Pros and cons for my specific case
- Code organization
- Testing strategy
- Learning curve for my team
```

### Technology Stack Selection

```
I'm building a monolith for [describe application].

Requirements:
- Expected traffic: [X req/s]
- Data model: [relational / document / mixed]
- Real-time features: [yes/no, describe]
- Background processing: [yes/no, describe]
- Team expertise: [languages/frameworks team knows]

Recommend a complete tech stack including:
- Web framework
- Database
- Caching
- Background jobs
- Search (if needed)
- API approach (REST vs GraphQL)

For each choice, explain why it's suitable for a monolith at this scale.
```

---

## Code Organization Prompts

### Module Structure Design

```
I'm building a [describe application] monolith using [framework].

My domain includes these main concepts:
- [Entity 1]: [description]
- [Entity 2]: [description]
- [Entity 3]: [description]

Relationships:
- [Entity 1] has many [Entity 2]
- [Entity 2] belongs to [Entity 3]
- etc.

Design a module structure that:
1. Groups related functionality
2. Minimizes coupling between modules
3. Allows future extraction to microservices
4. Follows [chosen pattern] principles

Include:
- Directory structure
- Module public APIs
- Inter-module communication approach
- Database schema organization
```

### Dependency Management

```
My monolith has these modules:
- users: authentication, profiles, permissions
- orders: order management, fulfillment
- payments: payment processing, invoicing
- inventory: stock management, warehouses
- notifications: email, SMS, push

Currently, modules import each other directly:
```python
# orders/services.py
from users.models import User
from inventory.services import reserve_stock
from payments.services import charge_payment
```

Help me:
1. Identify problematic dependencies
2. Design public APIs for each module
3. Implement event-driven communication where appropriate
4. Create dependency rules to prevent coupling
5. Suggest linting/tooling to enforce these rules
```

### Refactoring Big Ball of Mud

```
I inherited a Django/Rails/Express monolith that has become a "big ball of mud":

Current problems:
- [Describe specific issues: circular imports, god classes, etc.]
- [Files/classes that are too large]
- [Missing boundaries between features]

Codebase stats:
- [X] files
- [Y] lines of code
- [Z] models/entities

Help me create a refactoring plan:
1. How to identify module boundaries in existing code
2. Step-by-step migration approach (without breaking production)
3. Which areas to tackle first
4. How to prevent regression during refactoring
5. How long this might take for a team of [X]
```

---

## Database Design Prompts

### Schema Design for Monolith

```
I'm designing a database schema for a [type] monolith.

Entities and relationships:
- [List entities with their key attributes]
- [List relationships between entities]

Requirements:
- Expected data volume: [X rows per table per year]
- Read/write ratio: [e.g., 90% reads, 10% writes]
- Query patterns: [describe main queries]
- Data retention: [how long to keep data]

Design a PostgreSQL schema that:
1. Supports the query patterns efficiently
2. Uses appropriate indexes
3. Organizes tables by module (schemas or naming conventions)
4. Handles the expected scale
5. Supports future horizontal scaling if needed

Include:
- CREATE TABLE statements
- Index definitions
- Explanation of normalization choices
- Schema diagram (text-based)
```

### Database Optimization

```
My monolith's database is becoming slow. Here's the situation:

Database: PostgreSQL [version]
Tables: [list main tables with row counts]
Current issues:
- [Specific slow queries with execution times]
- [Lock contention issues]
- [Connection pool exhaustion]

Current indexes: [list existing indexes]

Queries that need optimization:
```sql
-- Query 1 (takes X seconds)
[SQL query]

-- Query 2 (takes Y seconds)
[SQL query]
```

Please:
1. Analyze these queries and suggest optimizations
2. Recommend additional indexes
3. Suggest schema changes if beneficial
4. Identify potential N+1 query issues
5. Recommend connection pool settings
```

### Migration Strategy

```
I need to make this database change to my production monolith:

Current schema:
```sql
[current table definition]
```

Desired schema:
```sql
[new table definition]
```

Constraints:
- Zero downtime required
- [X] million rows in affected table
- Peak traffic: [Y] req/s
- Database: [PostgreSQL/MySQL version]

Create a migration plan that:
1. Achieves zero downtime
2. Is reversible if issues arise
3. Minimizes lock time
4. Can be done in phases if needed
5. Includes rollback procedure
```

---

## Scaling Prompts

### Scaling Analysis

```
My monolith is experiencing performance issues. Here's the setup:

Current infrastructure:
- Server: [specs - CPU, RAM, storage]
- Database: [type, specs, configuration]
- Traffic: [current req/s, growth rate]
- Response times: [p50, p95, p99]

Architecture:
- Framework: [Django/Rails/etc.]
- Cache: [Redis/Memcached/none]
- Background jobs: [Celery/Sidekiq/none]
- File storage: [local/S3/etc.]

Symptoms:
- [Describe performance issues]
- [Error patterns]
- [Resource utilization patterns]

Analyze and recommend:
1. Root cause analysis - what's likely the bottleneck?
2. Quick wins - what can be fixed immediately?
3. Medium-term improvements
4. Scaling strategy (vertical vs horizontal)
5. Estimated infrastructure needs for [target traffic]
```

### Horizontal Scaling Setup

```
I need to horizontally scale my [framework] monolith.

Current state:
- Single server deployment
- Local session storage
- Local file uploads
- Background jobs run on same server
- Database on same server

Target state:
- [X] application servers behind load balancer
- Support for auto-scaling

Help me:
1. Identify all state that needs to be externalized
2. Choose appropriate services (Redis, S3, etc.)
3. Update application configuration
4. Set up load balancer configuration (nginx/HAProxy/ALB)
5. Configure health checks
6. Handle database connection pooling
7. Set up deployment strategy (blue-green/rolling)
```

### Caching Strategy

```
My monolith serves [type of content/data] with these characteristics:
- Read/write ratio: [e.g., 95/5]
- Data freshness requirements: [real-time / minutes / hours]
- Hot data percentage: [% of data accessed frequently]
- Current response times: [p50, p95]
- Target response times: [p50, p95]

Data types:
- [Type 1]: [access pattern, size, freshness requirement]
- [Type 2]: [access pattern, size, freshness requirement]

Design a multi-level caching strategy:
1. What to cache at each level (CDN, Redis, application, database)
2. Cache key design
3. TTL strategy for each type
4. Cache invalidation approach
5. Estimated hit rates and performance improvement
6. Implementation code examples for [framework]
```

---

## Deployment and Operations Prompts

### Deployment Strategy Design

```
I'm deploying a [framework] monolith to [AWS/GCP/bare metal/etc.].

Current deployment:
- [Describe current process]
- Deployment frequency: [X per week/day]
- Downtime acceptable: [yes/no]
- Rollback frequency: [how often needed]

Requirements:
- Zero downtime deployments
- Quick rollback capability
- Database migrations without downtime
- Feature flags support

Design a deployment strategy including:
1. Recommended approach (blue-green/canary/rolling)
2. Infrastructure setup (load balancer, app servers)
3. Database migration strategy
4. Health check implementation
5. Rollback procedure
6. CI/CD pipeline configuration
7. Monitoring and alerting for deployments
```

### Monitoring Setup

```
I need to set up monitoring for my [framework] monolith.

Current situation:
- Infrastructure: [describe]
- No monitoring currently / basic monitoring only
- Budget: [self-hosted only / can use paid services]

Business requirements:
- Know when site is down within [X] minutes
- Track performance degradation
- Debug production issues
- Capacity planning data

Design a monitoring strategy with:
1. Infrastructure metrics to collect
2. Application metrics to track (RED method)
3. Log aggregation setup
4. Alerting rules and thresholds
5. Dashboard design
6. Tool recommendations ([Prometheus/Grafana | Datadog | etc.])
7. Implementation steps
```

### Incident Response

```
My monolith is experiencing [describe incident]:
- Symptoms: [error messages, slow responses, etc.]
- Started: [when]
- Impact: [% of users affected]
- Recent changes: [deployments, config changes]

Current metrics:
- Error rate: [%]
- Response time: [ms]
- CPU: [%]
- Memory: [%]
- Database connections: [X/Y]

Help me:
1. Prioritized list of things to check
2. Diagnostic commands/queries to run
3. Quick mitigation options
4. Root cause analysis approach
5. Post-incident improvements to prevent recurrence
```

---

## Migration Prompts

### Modular Monolith Conversion

```
I want to convert my traditional monolith to a modular monolith.

Current structure:
```
[show current directory structure]
```

Current issues:
- [describe coupling problems]
- [describe testing difficulties]
- [describe team coordination issues]

My goals:
1. Clear module boundaries
2. Independent module testing
3. Potential future microservices extraction
4. Improved team autonomy

Create a migration plan:
1. How to identify module boundaries from existing code
2. Step-by-step refactoring approach
3. Public API design for each module
4. Database schema reorganization
5. Testing strategy during migration
6. How to enforce boundaries (tooling)
```

### Microservices Extraction

```
I've decided to extract [specific functionality] from my monolith into a microservice.

Current state:
- [Describe the functionality in the monolith]
- [Dependencies on other parts of the system]
- [Database tables involved]
- [External API contracts]

Reasons for extraction:
- [Why this functionality specifically]
- [Expected benefits]

Plan the extraction using the strangler fig pattern:
1. Define the service boundary
2. Design the API between monolith and new service
3. Data migration strategy (if needed)
4. Traffic routing approach
5. Rollback strategy
6. Testing approach
7. Monitoring during migration
8. Timeline and milestones
```

---

## Code Generation Prompts

### Generate Module Boilerplate

```
Generate a complete [Python/TypeScript/Go] module for [module name] in my monolith.

Module responsibilities:
- [List main features]

Framework: [Django/FastAPI/Express/etc.]

Include:
1. Directory structure
2. Models/entities with fields
3. Repository/data access layer
4. Service layer with business logic
5. API endpoints (REST)
6. DTOs/serializers
7. Unit tests for service layer
8. Integration tests for API
9. Public API exports

Follow these conventions:
- [Any naming conventions]
- [Testing patterns]
- [Error handling approach]
```

### Generate Database Migration

```
Generate an Alembic/Django migration for:

Change: [describe schema change]

Current schema:
```sql
[current table]
```

Requirements:
- Zero downtime (online migration)
- Reversible
- Handle [X] rows

Include:
1. Migration code
2. Reverse migration
3. Any required index changes
4. Data migration if needed
5. Testing queries to verify
```

### Generate API Endpoint

```
Generate a complete REST API endpoint for [operation].

Details:
- Framework: [FastAPI/Django REST/Express]
- HTTP method: [GET/POST/PUT/DELETE]
- URL: [path]
- Authentication: [JWT/session/none]
- Authorization: [describe rules]

Request:
```json
[request body if applicable]
```

Response:
```json
[expected response]
```

Include:
1. Route/view/handler code
2. Request validation
3. Error responses
4. Unit tests
5. OpenAPI documentation
```

---

## Review and Analysis Prompts

### Architecture Review

```
Review my monolith architecture for potential issues.

[Include: directory structure, key configuration, sample code showing patterns]

Specifically evaluate:
1. Module coupling - are there problematic dependencies?
2. Database design - any scaling concerns?
3. Error handling - is it consistent?
4. Testing - are there gaps?
5. Security - any obvious vulnerabilities?
6. Performance - any anti-patterns?
7. Maintainability - will this scale with team growth?

For each issue found:
- Severity (critical/high/medium/low)
- Specific location in code
- Recommended fix
- Migration path if significant change needed
```

### Performance Review

```
Review this code for performance issues:

```[language]
[code to review]
```

Context:
- Called [X] times per [second/minute/request]
- Typical data size: [describe]
- Current response time: [ms]
- Database: [type]

Identify:
1. N+1 query issues
2. Missing indexes
3. Unnecessary database calls
4. Caching opportunities
5. Algorithm inefficiencies
6. Memory issues

For each issue, provide:
- Explanation of the problem
- Performance impact estimate
- Corrected code
```

### Security Review

```
Review this monolith code for security vulnerabilities:

[Include relevant code: authentication, authorization, input handling, etc.]

Check for:
1. SQL injection vulnerabilities
2. XSS vulnerabilities
3. CSRF issues
4. Authentication weaknesses
5. Authorization bypasses
6. Sensitive data exposure
7. Insecure direct object references
8. Missing input validation
9. Insecure dependencies

For each issue:
- Severity and CVSS estimate
- Exploitation scenario
- Recommended fix
- Code example of the fix
```

---

## Troubleshooting Prompts

### Debug Production Issue

```
I'm seeing this error in production:

Error:
```
[error message and stack trace]
```

Context:
- When it happens: [always / intermittent / under load]
- Affected endpoint: [URL]
- Recent changes: [any deployments]
- Environment: [production / staging]

Relevant code:
```[language]
[code around the error]
```

Help me:
1. Interpret the error
2. Identify likely root causes
3. Suggest debugging steps
4. Provide potential fixes
5. Recommend preventive measures
```

### Memory Leak Investigation

```
My monolith's memory usage keeps growing:
- Starting memory: [X GB]
- After 24 hours: [Y GB]
- Restart frequency: [how often we restart]
- Framework: [Django/Rails/etc.]

Relevant patterns in our code:
- [Describe caching usage]
- [Describe background jobs]
- [Describe long-running processes]

Help me:
1. Common causes of memory leaks in [framework]
2. How to profile memory usage
3. Tools to identify the leak
4. Common fixes for each potential cause
5. Monitoring to set up for future detection
```
