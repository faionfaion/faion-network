# ASP.NET Core LLM Prompts

Prompts for AI-assisted ASP.NET Core development.

## Initial Setup Prompts

### Project Architecture

```
I'm building a {type} application with ASP.NET Core. Help me set up:

Context:
- Application type: {Web API / MVC / Blazor / Minimal API}
- Database: {PostgreSQL / SQL Server / MySQL / MongoDB}
- Authentication: {JWT / Identity / OAuth}
- Expected scale: {Small / Medium / Enterprise}
- Team size: {1-5 / 5-20 / 20+}

Generate:
1. Solution structure with projects
2. NuGet packages list
3. Program.cs configuration
4. appsettings.json template
5. Recommended architecture pattern (layered / clean / vertical slice)

Provide:
- Project creation commands
- Folder structure
- Key dependencies with versions
- Reasoning for architecture choices
```

### Database Schema Design

```
Design an Entity Framework Core data model for {domain}:

Requirements:
- Entities: {list main entities}
- Relationships: {describe key relationships}
- Business rules: {constraints, validations}
- Performance needs: {read-heavy / write-heavy / balanced}
- Soft delete: {yes / no}
- Audit fields: {yes / no}
- Multi-tenancy: {yes / no}

Generate:
1. Entity classes with annotations
2. IEntityTypeConfiguration classes
3. DbContext setup
4. Initial migration
5. Index recommendations
6. Sample seed data

Include:
- Navigation properties
- Value objects where appropriate
- Conventions vs explicit configuration
```

## Code Generation Prompts

### Controller + Service + Repository

```
Create a complete CRUD implementation for {Entity}:

Entity details:
- Name: {EntityName}
- Key properties: {list properties with types}
- Relationships: {related entities}
- Business logic: {describe any special logic}

Generate:
1. Entity class with EF Core configuration
2. Repository interface and implementation
3. Service interface and implementation
4. DTOs (Create, Update, Response)
5. AutoMapper profile
6. Controller with all CRUD endpoints
7. xUnit tests

Requirements:
- Async/await throughout
- Pagination for list endpoints
- Validation with FluentValidation
- Error handling
- XML documentation comments
- Following repository pattern
```

### Authentication & Authorization

```
Implement JWT authentication for ASP.NET Core API:

Requirements:
- User registration with email verification
- Login with JWT token + refresh token
- Role-based authorization: {list roles}
- Claims-based policies: {list policies}
- Password requirements: {specify}
- Token expiration: {access: 1h, refresh: 7d}
- Multi-tenant: {yes / no}

Generate:
1. User and RefreshToken entities
2. Authentication service
3. Token generation logic
4. Login/Register/Refresh endpoints
5. Authorization policies
6. Middleware configuration
7. Integration tests

Include:
- Password hashing with Identity
- Secure token generation
- Refresh token rotation
- Claims setup
```

### Background Service

```
Create a background service for {task description}:

Requirements:
- Task type: {periodic / queue-based / event-driven}
- Frequency: {every X minutes/hours / on-demand}
- Dependencies: {services needed}
- Error handling: {retry logic, dead-letter queue}
- Cancellation: {graceful shutdown}
- Monitoring: {logging, metrics}

Generate:
1. BackgroundService implementation
2. Hosted service registration
3. Queue/Channel setup (if applicable)
4. Error handling with retry logic
5. Unit tests
6. Configuration in appsettings.json

Include:
- Scoped service resolution
- Cancellation token handling
- Structured logging
```

## Refactoring Prompts

### Clean Architecture Migration

```
Refactor this {monolithic / poorly structured} code to Clean Architecture:

Current code:
{paste code}

Requirements:
- Separate into layers: Domain, Application, Infrastructure, API
- Implement repository pattern
- Use dependency injection properly
- Add DTOs instead of exposing entities
- Implement CQRS if appropriate

Provide:
1. Refactored code with layers
2. Interfaces in correct locations
3. Dependency registration
4. Migration steps
5. Benefits of each change
```

### Performance Optimization

```
Optimize this ASP.NET Core code for performance:

Current code:
{paste code}

Issues observed:
- {N+1 queries / slow response time / high memory}
- {specific metrics if available}

Analyze and provide:
1. Performance bottlenecks
2. Optimized code
3. EF Core query improvements (AsNoTracking, Include, projection)
4. Caching strategy (memory / distributed)
5. Async improvements
6. Before/after performance comparison
7. Benchmarking code with BenchmarkDotNet
```

## Testing Prompts

### Unit Tests

```
Generate comprehensive unit tests for this service:

Service code:
{paste service code}

Generate:
1. xUnit test class with setup
2. Happy path tests for all methods
3. Edge case tests (null, empty, invalid)
4. Exception handling tests
5. Mock setup with Moq
6. FluentAssertions usage
7. Test data builders/fixtures

Coverage goal: >80%
Include AAA pattern (Arrange-Act-Assert)
```

### Integration Tests

```
Create integration tests for this API controller:

Controller code:
{paste controller code}

Generate:
1. WebApplicationFactory setup
2. Test database configuration (in-memory)
3. Tests for all endpoints
4. Authentication tests
5. Validation tests
6. Error response tests
7. Test data seeding

Include:
- HTTP client setup
- JSON serialization
- Status code assertions
- Response content validation
```

## Debugging & Troubleshooting Prompts

### EF Core Query Issues

```
Debug this EF Core query issue:

Error/Problem:
{describe error or performance issue}

Query code:
{paste LINQ query}

Entity relationships:
{describe entities and navigation properties}

Help me:
1. Identify the problem
2. Show generated SQL
3. Provide optimized query
4. Explain why original query was problematic
5. Add appropriate indexes if needed
```

### Dependency Injection Errors

```
Resolve this dependency injection error:

Error message:
{paste error}

Service registration code:
{paste Program.cs / Startup.cs relevant code}

Class constructor:
{paste constructor}

Help me:
1. Identify the DI issue
2. Fix service registration
3. Explain service lifetimes (Transient/Scoped/Singleton)
4. Suggest best practices
```

## Architecture Decision Prompts

### Repository vs Direct DbContext

```
Should I use Repository pattern or access DbContext directly?

Context:
- Application type: {type}
- Team size: {size}
- Complexity: {simple CRUD / complex business logic}
- Testing approach: {unit / integration focused}

Provide:
1. Recommendation with reasoning
2. Pros/cons of each approach
3. Example implementation for both
4. When to switch from one to another
5. Hybrid approaches
```

### Monolith vs Microservices

```
Should this feature be a separate microservice?

Feature: {describe feature}

Current architecture: {monolith / modular monolith / microservices}

Considerations:
- Team ownership: {shared / dedicated team}
- Deployment frequency: {rarely / frequently}
- Scalability needs: {same as main app / different}
- Data requirements: {shared DB / separate DB}
- Communication: {sync / async}

Provide:
1. Recommendation
2. Decision tree/criteria
3. If microservice: API contract design
4. If monolith: module boundaries
5. Migration strategy if needed
```

## Security Review Prompts

### Security Audit

```
Review this code for security vulnerabilities:

Code:
{paste code}

Check for:
- SQL injection
- XSS vulnerabilities
- CSRF protection
- Authentication/Authorization flaws
- Sensitive data exposure
- Input validation issues
- Secure communication (HTTPS)
- Password handling
- Token security

Provide:
1. List of vulnerabilities found
2. Severity rating (Critical/High/Medium/Low)
3. Fixed code
4. Security best practices
5. Additional security headers/middleware needed
```

## API Documentation Prompts

### OpenAPI/Swagger Enhancement

```
Enhance Swagger documentation for this controller:

Controller code:
{paste controller}

Generate:
1. XML documentation comments
2. ProducesResponseType attributes
3. Example request/response objects
4. Operation descriptions
5. Parameter descriptions
6. Security requirements documentation
7. SwaggerGen configuration

Make it:
- Clear and comprehensive
- Include all response codes
- Show example payloads
- Group by tags appropriately
```

## Migration Prompts

### .NET Version Upgrade

```
Migrate this ASP.NET Core app from .NET {old version} to .NET {new version}:

Current code:
{paste relevant code}

Provide:
1. Breaking changes that affect this code
2. Updated code for new version
3. New features to leverage
4. Performance improvements available
5. Migration checklist
6. Testing strategy
```

### Database Migration

```
Create an EF Core migration for this change:

Current schema:
{describe current}

Desired changes:
{describe changes}

Generate:
1. Migration code (Up and Down methods)
2. Data migration if needed
3. Index changes
4. Potential issues (data loss, downtime)
5. Rollback strategy
6. Testing approach
```

## Performance Analysis Prompts

### Profiling Request

```
Help me profile and optimize this API endpoint:

Endpoint:
{paste controller action}

Services involved:
{list services}

Current performance:
- Response time: {Xms}
- Throughput: {Y req/s}
- Issues: {describe}

Provide:
1. Profiling checklist
2. Tools to use (MiniProfiler, Application Insights)
3. Key metrics to monitor
4. Optimization opportunities
5. Caching strategy
6. Database query optimization
7. Expected performance improvement
```

## Deployment Prompts

### Docker Containerization

```
Create Docker setup for this ASP.NET Core app:

Application details:
- .NET version: {version}
- Database: {type}
- External dependencies: {list}
- Environment configs: {list}
- Multi-stage build: {yes / no}

Generate:
1. Dockerfile (optimized, multi-stage)
2. .dockerignore
3. docker-compose.yml (with DB)
4. Docker commands for build/run
5. Environment variable configuration
6. Health check setup
7. Volume mounts for development
```

### CI/CD Pipeline

```
Create a CI/CD pipeline for ASP.NET Core:

Environment:
- CI/CD platform: {GitHub Actions / Azure DevOps / GitLab}
- Deployment target: {Azure App Service / Kubernetes / IIS}
- Stages: {Build / Test / Deploy}
- Environments: {Dev / Staging / Prod}

Generate:
1. Pipeline configuration file
2. Build steps
3. Test execution
4. Docker image build/push
5. Deployment steps
6. Environment-specific configuration
7. Rollback strategy
```

## Code Review Prompts

### Best Practices Review

```
Review this ASP.NET Core code for best practices:

Code:
{paste code}

Check for:
- Naming conventions
- Async/await usage
- Error handling
- Logging
- Dependency injection
- SOLID principles
- Code duplication
- Performance issues
- Security concerns
- Testability

Provide:
1. Issues found with severity
2. Refactored code
3. Explanation of each improvement
4. Best practice references
```

## Prompt Template

```
{Task description}

Context:
- {Key context item 1}
- {Key context item 2}
- {Constraints or requirements}

Generate/Provide:
1. {Specific output 1}
2. {Specific output 2}
3. {Additional deliverable}

Include:
- {Quality requirement}
- {Documentation requirement}
- {Best practice requirement}

Expected format: {code / explanation / comparison}
```

## Tips for Effective Prompts

### Be Specific

- Provide versions (.NET 8, EF Core 8, etc.)
- Include actual error messages
- Describe exact requirements
- Share relevant code context

### Provide Context

- Application type and scale
- Team size and structure
- Existing architecture
- Performance requirements
- Security requirements

### Ask for Explanation

- Request reasoning behind decisions
- Ask for trade-offs
- Request best practices
- Ask for alternative approaches

### Iterate

- Start with high-level design
- Drill into specific components
- Refine based on feedback
- Ask follow-up questions

## Sources

- [ASP.NET Core Documentation](https://docs.microsoft.com/en-us/aspnet/core/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
