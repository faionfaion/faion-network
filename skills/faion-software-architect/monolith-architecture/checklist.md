# Monolith Architecture Checklist

Step-by-step checklist for designing, building, and scaling monolithic applications.

## Phase 1: Decision Validation

Confirm monolith is the right choice for your context.

### Team and Organization

- [ ] Team size is under 10-15 developers
- [ ] Single team or closely collaborating teams
- [ ] Limited DevOps/SRE expertise available
- [ ] No requirement for independent team deployments

### Technical Requirements

- [ ] Domain boundaries are unclear or still evolving
- [ ] Strong data consistency (ACID) required
- [ ] No need for polyglot architecture (multiple languages)
- [ ] No extreme fault isolation requirements
- [ ] Performance requirements achievable with vertical/horizontal scaling

### Business Context

- [ ] MVP or early-stage product
- [ ] Speed to market prioritized over scalability
- [ ] Budget constraints favor simpler infrastructure
- [ ] Single deployment environment (no multi-region complexity)

**Decision:** If majority checked, proceed with monolith.

---

## Phase 2: Architecture Pattern Selection

Choose the internal organization pattern.

### Pattern Options

| Pattern | Best For | Check If Applies |
|---------|----------|------------------|
| Layered | CRUD apps, simple domains | [ ] Simple domain model |
| Vertical Slices | Feature teams, clear features | [ ] Feature-based development |
| Modular Monolith | Growth potential, microservices path | [ ] Future extraction likely |
| Clean Architecture | Complex domains, long-lived apps | [ ] Rich business logic |

### Selected Pattern Validation

- [ ] Pattern aligns with team structure
- [ ] Pattern supports expected growth
- [ ] Team understands the pattern
- [ ] Pattern has good tooling for your stack

---

## Phase 3: Code Organization

Structure the codebase properly.

### Directory Structure

- [ ] Root level organized by feature or layer (based on pattern)
- [ ] Clear separation between modules/features
- [ ] Shared code in dedicated location
- [ ] Configuration separated from code
- [ ] Tests co-located with code or in parallel structure

### Module Boundaries

- [ ] Each module has explicit public interface
- [ ] Module internals are private/protected
- [ ] No circular dependencies between modules
- [ ] Dependencies flow in one direction
- [ ] Dependency rules documented

### Dependency Management

- [ ] Dependency injection configured
- [ ] No hardcoded external service references
- [ ] Interfaces defined for external dependencies
- [ ] Mock/fake implementations for testing

### Enforcement

- [ ] Linting rules for import restrictions
- [ ] CI checks for dependency violations
- [ ] Architecture decision records (ADRs) for structure decisions
- [ ] Documentation of module responsibilities

---

## Phase 4: Database Design

Design database schema and access patterns.

### Schema Organization

- [ ] Schema separation strategy chosen (single schema / schema-per-module)
- [ ] Tables grouped by domain/module
- [ ] Naming conventions documented
- [ ] Foreign key strategy defined

### Data Access

- [ ] ORM configured properly
- [ ] Repository pattern implemented (if applicable)
- [ ] No direct SQL in business logic
- [ ] Query optimization guidelines documented

### Migrations

- [ ] Migration tool selected and configured
- [ ] Migrations are reversible
- [ ] Migration naming convention established
- [ ] Migration testing process defined
- [ ] Zero-downtime migration strategy documented

### Performance

- [ ] Primary indexes on all primary keys
- [ ] Secondary indexes on frequently queried columns
- [ ] Composite indexes for complex queries
- [ ] Query execution plans reviewed for critical paths
- [ ] Connection pooling configured

### Scaling Preparation

- [ ] Read replica support possible (stateless queries)
- [ ] Sharding strategy considered (if needed)
- [ ] Archival strategy for old data
- [ ] Backup and restore tested

---

## Phase 5: API Design

Design external and internal interfaces.

### External API

- [ ] REST or GraphQL chosen with rationale
- [ ] API versioning strategy defined
- [ ] Authentication mechanism selected
- [ ] Authorization model designed
- [ ] Rate limiting configured
- [ ] API documentation generated (OpenAPI/Swagger)

### Internal Module APIs

- [ ] Each module has defined public interface
- [ ] DTOs for cross-module communication
- [ ] No leaking of internal types
- [ ] Async communication patterns identified (if needed)

### Error Handling

- [ ] Consistent error response format
- [ ] Error codes documented
- [ ] Appropriate HTTP status codes
- [ ] Error logging configured
- [ ] User-friendly error messages

---

## Phase 6: Scaling Strategy

Prepare for growth from day one.

### Statelessness

- [ ] No local session storage
- [ ] No local file storage for user data
- [ ] All state externalized (Redis, S3, etc.)
- [ ] Sticky sessions not required (or explicitly handled)

### Horizontal Scaling

- [ ] Application can run multiple instances
- [ ] Session storage externalized (Redis)
- [ ] File storage externalized (S3, MinIO)
- [ ] Background jobs support distributed execution
- [ ] Database connection pooling configured

### Caching

- [ ] Caching strategy documented
- [ ] Cache invalidation strategy defined
- [ ] HTTP caching headers configured
- [ ] Application-level caching implemented
- [ ] CDN configured for static assets

### Load Balancing

- [ ] Load balancer configured
- [ ] Health check endpoint implemented
- [ ] Graceful shutdown handling
- [ ] Connection draining configured

---

## Phase 7: Deployment Pipeline

Set up reliable deployment.

### CI/CD Basics

- [ ] Automated build on every commit
- [ ] Automated test execution
- [ ] Code quality checks (linting, formatting)
- [ ] Security scanning (dependencies, SAST)
- [ ] Artifact versioning

### Deployment Strategy

Choose one:

- [ ] **Blue-Green:** Two identical environments, instant switch
- [ ] **Canary:** Gradual rollout to percentage of users
- [ ] **Rolling:** Gradual instance replacement
- [ ] **Feature Flags:** Deploy disabled, enable gradually

### Deployment Checklist

- [ ] Database migrations run before deployment
- [ ] Health checks verify new deployment
- [ ] Rollback procedure documented and tested
- [ ] Deployment notifications configured
- [ ] Post-deployment smoke tests automated

### Environment Management

- [ ] Environment parity (dev = staging = prod)
- [ ] Secrets management configured
- [ ] Configuration externalized (env vars, config files)
- [ ] Feature flags for risky changes

---

## Phase 8: Observability

Implement monitoring and logging.

### Logging

- [ ] Structured logging implemented (JSON format)
- [ ] Request ID propagation for tracing
- [ ] Log levels properly used (DEBUG, INFO, WARN, ERROR)
- [ ] Sensitive data excluded from logs
- [ ] Log aggregation configured (ELK, Loki, CloudWatch)
- [ ] Log retention policy defined

### Metrics

- [ ] Application metrics exported (Prometheus format)
- [ ] Key metrics identified:
  - [ ] Request rate
  - [ ] Error rate
  - [ ] Response time (p50, p95, p99)
  - [ ] Active users/sessions
  - [ ] Business metrics
- [ ] Infrastructure metrics collected
- [ ] Dashboards created

### Alerting

- [ ] Critical alerts defined (errors, downtime)
- [ ] Warning alerts defined (degradation)
- [ ] Alert routing configured (PagerDuty, Slack)
- [ ] Runbooks for common alerts
- [ ] Alert noise reduction (grouping, deduplication)

### Health Checks

- [ ] Liveness endpoint (is app running?)
- [ ] Readiness endpoint (can app serve traffic?)
- [ ] Dependency health checks (DB, Redis, external APIs)
- [ ] Deep health check for detailed diagnostics

---

## Phase 9: Security

Implement security best practices.

### Authentication

- [ ] Authentication mechanism implemented
- [ ] Password hashing with modern algorithm (Argon2, bcrypt)
- [ ] Session management secure
- [ ] Token expiration configured
- [ ] Multi-factor authentication available (if required)

### Authorization

- [ ] Role-based or permission-based access control
- [ ] Authorization checks on all endpoints
- [ ] Resource-level authorization (users can only access their data)
- [ ] Admin functionality protected

### Input Validation

- [ ] All input validated and sanitized
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] CSRF protection configured
- [ ] File upload validation

### Infrastructure Security

- [ ] HTTPS enforced
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] Secrets not in code or version control
- [ ] Dependency vulnerabilities scanned
- [ ] Network security groups configured

---

## Phase 10: Performance Optimization

Optimize for production workloads.

### Profiling

- [ ] Application profiling done
- [ ] Hot paths identified
- [ ] Memory usage analyzed
- [ ] Database query analysis done

### Database Optimization

- [ ] N+1 queries eliminated
- [ ] Slow queries optimized
- [ ] Indexes cover critical queries
- [ ] Connection pool sized correctly
- [ ] Query result caching for expensive queries

### Application Optimization

- [ ] Expensive computations cached
- [ ] Async processing for non-critical operations
- [ ] Background jobs for long-running tasks
- [ ] Response compression enabled
- [ ] Static asset optimization (minification, bundling)

### Load Testing

- [ ] Load testing performed
- [ ] Performance baselines established
- [ ] Bottlenecks identified and addressed
- [ ] Auto-scaling thresholds determined

---

## Phase 11: Documentation

Document architecture and operations.

### Technical Documentation

- [ ] Architecture overview documented
- [ ] Module responsibilities documented
- [ ] API documentation generated
- [ ] Database schema documented
- [ ] Deployment procedures documented

### Operations Documentation

- [ ] Runbooks for common issues
- [ ] Incident response procedures
- [ ] On-call procedures
- [ ] Disaster recovery plan
- [ ] Backup and restore procedures

### Developer Documentation

- [ ] Local development setup guide
- [ ] Coding standards documented
- [ ] Pull request guidelines
- [ ] Testing guidelines
- [ ] Debugging guide

---

## Phase 12: Migration Preparation

Prepare for future evolution (optional but recommended).

### Module Independence

- [ ] Modules can be tested independently
- [ ] Modules have clear ownership
- [ ] Module interfaces are stable
- [ ] Breaking changes have migration paths

### Data Isolation

- [ ] Each module owns its data
- [ ] Cross-module data access through APIs only
- [ ] Schema separation allows future database split
- [ ] No direct foreign keys across module boundaries

### Service Extraction Path

- [ ] Candidate modules for extraction identified
- [ ] Strangler fig pattern understood
- [ ] API gateway can route to both monolith and services
- [ ] Feature flags can toggle between implementations

---

## Review Checklist

### Before Production Launch

- [ ] All critical path tests passing
- [ ] Security review completed
- [ ] Performance testing passed
- [ ] Monitoring and alerting configured
- [ ] Runbooks available
- [ ] Rollback procedure tested
- [ ] On-call rotation established

### Quarterly Review

- [ ] Architecture still fits requirements
- [ ] No major scaling issues
- [ ] Technical debt manageable
- [ ] Team productivity maintained
- [ ] Incident count acceptable
- [ ] Documentation up to date

### Annual Review

- [ ] Evaluate if microservices needed
- [ ] Review technology stack currency
- [ ] Assess team growth impact
- [ ] Plan major refactoring if needed
- [ ] Update disaster recovery plan

---

## Quick Reference

### Minimum Viable Checklist (MVP)

For rapid deployment:

- [ ] Basic layered or vertical slice structure
- [ ] Database with migrations
- [ ] Authentication
- [ ] Logging
- [ ] Health check endpoint
- [ ] CI/CD with tests
- [ ] Basic monitoring

### Production-Ready Checklist

Add to MVP:

- [ ] Horizontal scaling support
- [ ] Caching layer
- [ ] Full observability (logs, metrics, alerts)
- [ ] Security hardening
- [ ] Deployment strategy (blue-green or canary)
- [ ] Documentation

### Enterprise-Ready Checklist

Add to Production-Ready:

- [ ] Modular monolith structure
- [ ] Comprehensive testing (unit, integration, e2e)
- [ ] Disaster recovery plan
- [ ] Compliance requirements met
- [ ] Multi-environment support
- [ ] Advanced observability (tracing, profiling)
