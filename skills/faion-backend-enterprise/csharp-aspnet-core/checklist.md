# ASP.NET Core Development Checklist

Step-by-step checklist for building production-ready ASP.NET Core applications.

## Phase 1: Project Setup

### 1.1 Initialize Project

- [ ] Create solution with `dotnet new sln -n MyApp`
- [ ] Create Web API project with `dotnet new webapi -n MyApp.Api`
- [ ] Create class library for domain with `dotnet new classlib -n MyApp.Domain`
- [ ] Create class library for infrastructure with `dotnet new classlib -n MyApp.Infrastructure`
- [ ] Create test project with `dotnet new xunit -n MyApp.Tests`
- [ ] Add projects to solution
- [ ] Configure project references
- [ ] Set up .gitignore for .NET

### 1.2 Configure Dependencies

- [ ] Install EntityFramework Core packages
- [ ] Install AutoMapper for DTO mapping
- [ ] Install FluentValidation for validation
- [ ] Install Serilog for logging
- [ ] Install Swashbuckle for Swagger/OpenAPI
- [ ] Install authentication packages (JWT, Identity)
- [ ] Install testing packages (Moq, FluentAssertions)
- [ ] Configure package versions consistently

### 1.3 Project Structure

- [ ] Create Controllers folder
- [ ] Create Services folder
- [ ] Create Repositories folder
- [ ] Create DTOs folder
- [ ] Create Entities folder
- [ ] Create Configurations folder
- [ ] Create Middleware folder
- [ ] Create Filters folder

## Phase 2: Architecture Setup

### 2.1 Dependency Injection

- [ ] Register services in Program.cs
- [ ] Configure service lifetimes (Transient, Scoped, Singleton)
- [ ] Set up AutoMapper profiles
- [ ] Register repositories
- [ ] Configure database context
- [ ] Set up health checks
- [ ] Configure CORS policies

### 2.2 Database Configuration

- [ ] Install database provider (SQL Server, PostgreSQL, MySQL)
- [ ] Configure connection string in appsettings.json
- [ ] Create DbContext class
- [ ] Configure entity type configurations
- [ ] Set up migrations folder
- [ ] Create initial migration
- [ ] Apply migration to database
- [ ] Seed initial data if needed

### 2.3 API Configuration

- [ ] Configure routing conventions
- [ ] Set up API versioning
- [ ] Configure JSON serialization options
- [ ] Set up model binding
- [ ] Configure ProblemDetails for error responses
- [ ] Enable HTTPS redirection
- [ ] Configure request/response compression

## Phase 3: Domain Layer

### 3.1 Entities

- [ ] Define entity classes with properties
- [ ] Add validation attributes
- [ ] Configure navigation properties
- [ ] Implement IEquatable if needed
- [ ] Add domain events if using DDD
- [ ] Document entities with XML comments
- [ ] Add value objects where appropriate

### 3.2 Entity Framework Configuration

- [ ] Create IEntityTypeConfiguration classes
- [ ] Configure table names and schemas
- [ ] Set up primary keys
- [ ] Configure indexes (unique, composite)
- [ ] Set up foreign key relationships
- [ ] Configure cascade delete behavior
- [ ] Add query filters for soft delete
- [ ] Configure value conversions if needed

### 3.3 Repository Pattern

- [ ] Define repository interfaces
- [ ] Implement generic repository if needed
- [ ] Create specific repositories for entities
- [ ] Implement async query methods
- [ ] Add pagination support
- [ ] Implement search/filter methods
- [ ] Add unit of work pattern if needed
- [ ] Include eager loading options

## Phase 4: Application Layer

### 4.1 DTOs

- [ ] Create request DTOs (Create, Update)
- [ ] Create response DTOs
- [ ] Add validation attributes to DTOs
- [ ] Create PagedResult DTO for pagination
- [ ] Implement AutoMapper profiles for mapping
- [ ] Add FluentValidation validators
- [ ] Document DTOs with XML comments
- [ ] Use records for immutable DTOs where appropriate

### 4.2 Service Layer

- [ ] Define service interfaces
- [ ] Implement service classes
- [ ] Add business logic validation
- [ ] Implement transaction management
- [ ] Add error handling
- [ ] Implement logging
- [ ] Add caching where appropriate
- [ ] Document public methods

### 4.3 AutoMapper Configuration

- [ ] Create mapping profiles
- [ ] Configure entity to DTO mappings
- [ ] Set up reverse mappings
- [ ] Handle nested objects
- [ ] Configure value converters
- [ ] Add custom type converters if needed
- [ ] Test mappings with unit tests

## Phase 5: API Controllers

### 5.1 Controller Setup

- [ ] Create controller classes inheriting ControllerBase
- [ ] Add [ApiController] attribute
- [ ] Configure route templates
- [ ] Inject required services
- [ ] Add authorization attributes
- [ ] Add XML documentation
- [ ] Configure API versioning attributes

### 5.2 Action Methods

- [ ] Implement GET endpoints (list, single)
- [ ] Implement POST endpoints (create)
- [ ] Implement PUT/PATCH endpoints (update)
- [ ] Implement DELETE endpoints
- [ ] Add proper HTTP status codes
- [ ] Implement pagination for list endpoints
- [ ] Add filtering and sorting
- [ ] Use ActionResult<T> for return types

### 5.3 Validation and Error Handling

- [ ] Enable automatic model validation
- [ ] Add custom validation logic where needed
- [ ] Implement global exception handler
- [ ] Configure ProblemDetails responses
- [ ] Add validation error messages
- [ ] Log errors appropriately
- [ ] Return consistent error format

## Phase 6: Authentication & Authorization

### 6.1 JWT Authentication

- [ ] Install Microsoft.AspNetCore.Authentication.JwtBearer
- [ ] Configure JWT settings in appsettings.json
- [ ] Add authentication middleware
- [ ] Implement token generation service
- [ ] Create login endpoint
- [ ] Add refresh token support
- [ ] Configure token validation parameters
- [ ] Set up claims-based authorization

### 6.2 Authorization Policies

- [ ] Define authorization policies
- [ ] Create role-based policies
- [ ] Implement claim-based policies
- [ ] Add policy-based authorization to endpoints
- [ ] Create custom authorization requirements
- [ ] Implement authorization handlers
- [ ] Test authorization rules

### 6.3 Identity Setup (if needed)

- [ ] Install Microsoft.AspNetCore.Identity packages
- [ ] Configure Identity services
- [ ] Create ApplicationUser class
- [ ] Set up password requirements
- [ ] Configure user lockout settings
- [ ] Add email confirmation
- [ ] Implement password reset

## Phase 7: Middleware & Filters

### 7.1 Custom Middleware

- [ ] Create exception handling middleware
- [ ] Add request logging middleware
- [ ] Implement correlation ID middleware
- [ ] Add response time middleware
- [ ] Configure middleware pipeline order
- [ ] Test middleware behavior

### 7.2 Action Filters

- [ ] Create validation filter
- [ ] Implement caching filter
- [ ] Add audit logging filter
- [ ] Create rate limiting filter
- [ ] Configure filter ordering
- [ ] Register filters globally or per controller

## Phase 8: Background Services

### 8.1 Hosted Services

- [ ] Create IHostedService implementations
- [ ] Implement BackgroundService for long-running tasks
- [ ] Configure service dependencies
- [ ] Add graceful shutdown handling
- [ ] Implement error handling and retries
- [ ] Add logging
- [ ] Configure service timing

### 8.2 Message Queues (if needed)

- [ ] Choose queue provider (RabbitMQ, Azure Service Bus)
- [ ] Install required packages
- [ ] Configure queue connection
- [ ] Create message producers
- [ ] Implement message consumers
- [ ] Add message serialization
- [ ] Implement retry and dead letter handling

## Phase 9: Testing

### 9.1 Unit Tests

- [ ] Create test projects
- [ ] Write service layer tests
- [ ] Test repository methods
- [ ] Mock dependencies with Moq
- [ ] Test validation logic
- [ ] Use FluentAssertions for assertions
- [ ] Aim for >80% code coverage
- [ ] Test edge cases and error scenarios

### 9.2 Integration Tests

- [ ] Set up WebApplicationFactory
- [ ] Create test database
- [ ] Write controller integration tests
- [ ] Test authentication flows
- [ ] Test database operations
- [ ] Verify API contracts
- [ ] Test error responses
- [ ] Clean up test data

### 9.3 Test Data

- [ ] Create test fixtures
- [ ] Use builder pattern for test data
- [ ] Implement database seeding for tests
- [ ] Use in-memory database for fast tests
- [ ] Set up test data factories
- [ ] Create shared test utilities

## Phase 10: API Documentation

### 10.1 Swagger/OpenAPI

- [ ] Configure Swashbuckle
- [ ] Enable XML documentation
- [ ] Add API descriptions
- [ ] Document request/response examples
- [ ] Configure security definitions
- [ ] Add operation IDs
- [ ] Group endpoints by tags
- [ ] Test Swagger UI

### 10.2 Code Documentation

- [ ] Add XML comments to controllers
- [ ] Document service interfaces
- [ ] Add summary for DTOs
- [ ] Document complex methods
- [ ] Include parameter descriptions
- [ ] Add code examples where helpful
- [ ] Generate documentation with DocFX (optional)

## Phase 11: Performance & Optimization

### 11.1 Database Optimization

- [ ] Use AsNoTracking for read-only queries
- [ ] Implement query projection
- [ ] Add appropriate indexes
- [ ] Use Include for eager loading
- [ ] Avoid N+1 query problems
- [ ] Use compiled queries where appropriate
- [ ] Monitor slow queries
- [ ] Implement database connection pooling

### 11.2 Caching

- [ ] Add IMemoryCache for in-memory caching
- [ ] Implement distributed cache (Redis)
- [ ] Cache expensive query results
- [ ] Set appropriate cache expiration
- [ ] Implement cache invalidation
- [ ] Add response caching
- [ ] Monitor cache hit rates

### 11.3 API Performance

- [ ] Enable response compression
- [ ] Implement pagination
- [ ] Add API rate limiting
- [ ] Use async/await properly
- [ ] Minimize DTO size
- [ ] Implement ETags for conditional requests
- [ ] Profile API performance

## Phase 12: Logging & Monitoring

### 12.1 Structured Logging

- [ ] Configure Serilog
- [ ] Set up log sinks (Console, File, Seq)
- [ ] Add structured log properties
- [ ] Log request/response details
- [ ] Log exceptions with context
- [ ] Configure log levels
- [ ] Implement correlation IDs
- [ ] Sanitize sensitive data from logs

### 12.2 Health Checks

- [ ] Add health check endpoints
- [ ] Implement database health check
- [ ] Add external dependency checks
- [ ] Configure health check UI
- [ ] Set up liveness and readiness probes
- [ ] Add custom health checks
- [ ] Monitor health check results

### 12.3 Application Insights (optional)

- [ ] Install Application Insights SDK
- [ ] Configure instrumentation key
- [ ] Track custom events
- [ ] Log custom metrics
- [ ] Monitor API performance
- [ ] Set up alerts
- [ ] Create dashboards

## Phase 13: Security

### 13.1 Security Hardening

- [ ] Enable HTTPS redirection
- [ ] Configure HSTS
- [ ] Add security headers
- [ ] Implement CSRF protection
- [ ] Validate all inputs
- [ ] Sanitize outputs
- [ ] Use parameterized queries
- [ ] Implement rate limiting

### 13.2 Data Protection

- [ ] Configure data protection API
- [ ] Encrypt sensitive data
- [ ] Hash passwords with Identity
- [ ] Protect connection strings
- [ ] Use user secrets in development
- [ ] Implement secret management in production
- [ ] Add audit logging

### 13.3 Security Testing

- [ ] Run OWASP dependency check
- [ ] Perform security scanning
- [ ] Test authentication bypass
- [ ] Verify authorization rules
- [ ] Test input validation
- [ ] Check for SQL injection vulnerabilities
- [ ] Verify CORS configuration

## Phase 14: Deployment

### 14.1 Configuration Management

- [ ] Set up environment-specific configs
- [ ] Use appsettings.{Environment}.json
- [ ] Configure environment variables
- [ ] Implement feature flags
- [ ] Externalize secrets
- [ ] Configure logging per environment
- [ ] Test configuration loading

### 14.2 Containerization (Docker)

- [ ] Create Dockerfile
- [ ] Create .dockerignore
- [ ] Build Docker image
- [ ] Test container locally
- [ ] Optimize image size
- [ ] Configure docker-compose for local dev
- [ ] Set up multi-stage builds

### 14.3 CI/CD Pipeline

- [ ] Set up GitHub Actions / Azure DevOps
- [ ] Configure build pipeline
- [ ] Run tests in pipeline
- [ ] Run code analysis
- [ ] Build Docker image
- [ ] Push to container registry
- [ ] Deploy to staging
- [ ] Deploy to production

## Quick Reference Checklist

### Minimal API (5 Steps)

- [ ] Create project, install packages
- [ ] Set up EF Core with entities
- [ ] Create controller with CRUD endpoints
- [ ] Add authentication
- [ ] Write tests

### Standard API (10 Steps)

- [ ] Project setup with layered architecture
- [ ] Database + EF Core configuration
- [ ] Implement repository pattern
- [ ] Create service layer
- [ ] Build controllers with DTOs
- [ ] Add authentication & authorization
- [ ] Implement validation
- [ ] Set up logging
- [ ] Write unit + integration tests
- [ ] Configure Swagger

### Production-Ready API (20+ Steps)

- [ ] Complete standard API setup
- [ ] Add caching layer
- [ ] Implement background services
- [ ] Set up health checks
- [ ] Add monitoring (Application Insights)
- [ ] Implement rate limiting
- [ ] Security hardening
- [ ] Performance optimization
- [ ] API documentation
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Load testing

## Checklist Summary

| Phase | Items | Priority |
|-------|-------|----------|
| Project Setup | 20 | High |
| Architecture | 15 | High |
| Domain Layer | 15 | High |
| Application Layer | 18 | High |
| Controllers | 15 | High |
| Auth & Authorization | 15 | High |
| Middleware | 8 | Medium |
| Background Services | 10 | Medium |
| Testing | 18 | High |
| Documentation | 12 | Medium |
| Performance | 15 | Medium |
| Logging & Monitoring | 15 | High |
| Security | 15 | High |
| Deployment | 18 | High |
| **Total** | **209** | - |
