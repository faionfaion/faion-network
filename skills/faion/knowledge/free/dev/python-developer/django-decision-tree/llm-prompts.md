# LLM Prompts for Django Decisions

Effective prompts for using LLMs (Claude, GPT, etc.) to assist with Django architecture decisions.

---

## Prompt Patterns

### Context-Rich Decision Prompt

Always provide context for better recommendations:

```
I need help deciding {DECISION_TYPE} for my Django project.

**Project Context:**
- Type: {e-commerce | SaaS | CMS | API | internal tool}
- Team: {size} developers with {experience level} Django experience
- Timeline: {X months} to {MVP | production}
- Scale: {expected users/requests}
- Budget: {constraints}

**Requirements:**
- {Requirement 1}
- {Requirement 2}
- {Requirement 3}

**Constraints:**
- {Constraint 1}
- {Constraint 2}

**Trade-off priority (rank 1-4):**
- [ ] Developer experience
- [ ] Performance
- [ ] Maintainability
- [ ] Cost

What do you recommend and why?
```

---

## Framework Selection Prompts

### Django vs FastAPI Decision

```
Help me decide between Django and FastAPI for my project.

**Project Requirements:**
- {Describe what you're building}
- Need admin interface: {Yes/No}
- Server-side templates: {Yes/No}
- API-only: {Yes/No}
- Real-time features: {Yes/No}
- Expected concurrent connections: {number}

**Team:**
- Django experience: {None | Basic | Expert}
- FastAPI experience: {None | Basic | Expert}
- Async Python experience: {None | Basic | Expert}

**Non-negotiables:**
- {List must-have features}

Please recommend the framework with specific reasoning for my context.
```

### Django API Framework Decision

```
I'm building a Django project and need to choose an API framework.

**API Characteristics:**
- Number of endpoints: {approximate}
- Complexity: {simple CRUD | complex business logic | mixed}
- Nested resources: {Yes/No}
- Need OpenAPI docs: {Yes/No}
- Performance critical: {Yes/No}

**Team:**
- DRF experience: {None | Basic | Expert}
- Type hints usage: {Rarely | Sometimes | Always}

Compare Django REST Framework vs Django Ninja vs raw views for my use case.
Include code examples for a typical endpoint.
```

---

## Architecture Decision Prompts

### Architecture Pattern Selection

```
Help me choose an architecture pattern for my Django project.

**Project Scale:**
- Number of Django apps: {current or expected}
- Number of models: {current or expected}
- Team size: {number}
- Project lifespan: {short-term | long-term}

**Complexity Indicators:**
- Business logic complexity: {Low | Medium | High}
- Multiple entry points (API, CLI, admin): {Yes/No}
- Integration with external services: {count}
- Domain concepts that need isolation: {list}

**Testing Requirements:**
- Unit test coverage target: {percentage}
- Need to test business logic without HTTP: {Yes/No}

Compare:
1. Simple (Fat Models)
2. Service Layer
3. Clean Architecture / DDD

For my context, which is appropriate and why?
Show example file structure for chosen pattern.
```

### Code Placement Decision

```
I have this function in my Django project and I'm not sure where to place it:

```python
{paste your function}
```

**Context:**
- App: {app name}
- Called from: {view | other service | task | CLI}
- Dependencies: {what it uses}

Based on these characteristics:
- Does it write to database?
- Does it call external APIs?
- Is it a pure function?
- Does it handle HTTP?

Where should this code live? Explain the reasoning.
```

---

## Database Decision Prompts

### Database Selection

```
Help me choose a database for my Django project.

**Data Characteristics:**
- Expected data size: {GB}
- Query patterns: {read-heavy | write-heavy | balanced}
- Need transactions: {Yes/No}
- Concurrent users: {number}

**Special Requirements:**
- Full-text search: {Yes/No}
- JSON/document storage: {Yes/No}
- Geographic queries: {Yes/No}
- Array fields: {Yes/No}

**Operational:**
- Deployment: {managed | self-hosted}
- Backup requirements: {frequency}
- Team database expertise: {PostgreSQL | MySQL | SQLite | None}

Compare PostgreSQL, MySQL, and SQLite for my needs.
Include migration considerations if starting with SQLite.
```

### Query Optimization

```
I have a slow Django query that I need to optimize:

```python
{paste your query}
```

**Context:**
- Model definitions:
```python
{paste relevant models}
```
- Table sizes: {approximate row counts}
- Current execution time: {time}
- Database: {PostgreSQL | MySQL | SQLite}

Analyze this query and suggest optimizations:
1. Index recommendations
2. Query rewriting
3. select_related/prefetch_related usage
4. Raw SQL if beneficial
```

---

## Deployment Decision Prompts

### Deployment Platform Selection

```
Help me choose a deployment platform for my Django project.

**Application:**
- Traffic pattern: {steady | spiky | unpredictable}
- Uptime requirement: {percentage}
- Background tasks: {Yes/No}
- WebSockets: {Yes/No}

**Team:**
- DevOps expertise: {None | Basic | Advanced}
- Time for infrastructure: {limited | moderate | flexible}

**Budget:**
- Monthly budget: ${range}
- Cost optimization priority: {High | Medium | Low}

**Compliance:**
- Requirements: {None | SOC2 | HIPAA | GDPR}
- Data residency: {any | specific regions}

Compare:
1. PaaS (Render, Fly.io, Railway)
2. VPS (DigitalOcean, Hetzner)
3. Kubernetes
4. Serverless (Cloud Run, Lambda)

For my situation, recommend the best option with cost estimates.
```

### Container Configuration

```
I need a Docker configuration for my Django project.

**Project Setup:**
- Python version: {version}
- Database: {PostgreSQL | MySQL | SQLite}
- Cache: {Redis | Memcached | None}
- Task queue: {Celery | Django-Q | None}

**Requirements:**
- Development and production configs
- Multi-stage build for smaller images
- Proper handling of static files
- Health check endpoints

Generate:
1. Dockerfile (multi-stage)
2. docker-compose.yml (development)
3. docker-compose.prod.yml (production)
4. .dockerignore
```

---

## Package Evaluation Prompts

### Package Comparison

```
I need to choose a Django package for {functionality}.

**Requirements:**
- {Specific requirement 1}
- {Specific requirement 2}
- Must support Django {version}
- Must support Python {version}

**Candidates:**
1. {package1}
2. {package2}
3. {package3}

Compare these packages on:
- Features
- Maintenance status
- Documentation quality
- Community size
- Performance
- Learning curve

Recommend the best choice for my needs.
```

### Package Security Check

```
I'm evaluating {package_name} for my Django project.

Check:
1. Recent maintenance activity
2. Known security vulnerabilities
3. Dependency health
4. License compatibility with {MIT | Apache | GPL}

Also provide:
- Installation instructions
- Basic configuration example
- Common pitfalls to avoid
```

---

## Code Review Prompts

### Architecture Review

```
Review my Django project structure for architectural issues:

```
{paste directory tree}
```

**Key files:**
```python
# models.py
{paste models}

# views.py or api.py
{paste views/api code}

# services.py (if exists)
{paste services}
```

Identify:
1. Code placement issues
2. Circular dependency risks
3. Layer violations
4. Testing challenges
5. Scalability concerns

Provide specific recommendations with code examples.
```

### Code Smell Detection

```
Review this Django code for anti-patterns:

```python
{paste code}
```

Check for:
- Fat views (business logic in views)
- N+1 queries
- Improper transaction handling
- Missing error handling
- Security issues
- Testing difficulties

For each issue found, show the improved version.
```

---

## Migration & Refactoring Prompts

### Architecture Migration

```
I need to refactor my Django project from {current pattern} to {target pattern}.

**Current State:**
- Pattern: {Fat Models | Spaghetti | Mixed}
- Pain points: {list specific issues}
- Code example:
```python
{paste problematic code}
```

**Target State:**
- Pattern: {Service Layer | Clean Architecture}
- Goals: {testability | maintainability | etc}

Create a step-by-step migration plan:
1. Identify what to extract
2. Order of operations
3. Testing strategy during migration
4. Rollback approach

Include before/after code examples.
```

### Database Migration

```
I need to migrate my Django project from {SQLite | MySQL} to {PostgreSQL}.

**Current Setup:**
- Models count: {number}
- Data size: {GB}
- Active users: {Yes/No - can we have downtime?}

**Concerns:**
- {Specific concern 1}
- {Specific concern 2}

Provide:
1. Pre-migration checklist
2. Migration script/commands
3. Data validation approach
4. Rollback plan
5. Post-migration verification
```

---

## Testing Decision Prompts

### Testing Strategy

```
Help me design a testing strategy for my Django project.

**Project Type:** {API | Full-stack | Internal tool}

**Current State:**
- Test coverage: {percentage or "none"}
- Existing tests: {describe}

**Constraints:**
- CI/CD: {Yes/No - pipeline time limits}
- Database: {PostgreSQL | SQLite for tests}
- External services: {list services to mock}

Design a testing strategy including:
1. Test pyramid allocation (unit/integration/e2e ratio)
2. What to test at each level
3. Mocking strategy
4. Fixtures approach
5. CI configuration

Include example tests for a typical service function.
```

---

## Quick Decision Prompts

### Rapid Framework Decision

```
Quick decision needed: {DRF or Django Ninja}?
- Project: {one-line description}
- Team DRF experience: {Yes/No}
- Performance critical: {Yes/No}
- Need ViewSets: {Yes/No}
```

### Rapid Architecture Decision

```
Quick: What architecture for {X} apps, {Y} developers, {complexity} complexity?
```

### Rapid Database Decision

```
Quick: PostgreSQL vs SQLite?
- Production: {Yes/No}
- Full-text search: {Yes/No}
- JSON fields: {Yes/No}
- Solo developer: {Yes/No}
```

---

## Prompt Best Practices

### Do

- Provide specific project context
- State your constraints clearly
- Rank your trade-off priorities
- Include relevant code snippets
- Ask for examples in the response

### Don't

- Ask "what's the best" without context
- Omit team experience level
- Forget to mention scale requirements
- Ask multiple unrelated questions
- Ignore framework recommendations based on hype

### Example of Bad vs Good Prompt

**Bad:**
```
What database should I use for Django?
```

**Good:**
```
I'm building a content management system with Django.
- 50k articles with full-text search
- 3 content editors, 100k monthly readers
- Need JSON fields for flexible metadata
- Team has PostgreSQL experience
- Deployed on Railway (managed PostgreSQL available)

Should I use PostgreSQL or stick with SQLite for development?
What about MySQL since it's cheaper on our hosting?
```

---

## Follow-up Prompts

After getting initial recommendation:

```
Thanks for the recommendation. Can you:
1. Show a minimal working example?
2. What are the common pitfalls with this approach?
3. How would I migrate away from this if needed?
4. What monitoring/observability should I add?
```

For deeper exploration:

```
I want to understand the trade-offs better.
- What would I lose by choosing {alternative}?
- What's the complexity cost of {recommended option}?
- Are there hybrid approaches?
```

---

*These prompts are designed to get actionable, context-aware recommendations from LLMs.*
