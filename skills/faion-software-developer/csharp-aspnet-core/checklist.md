# Checklist

## Project Setup Phase

- [ ] Create ASP.NET Core project
- [ ] Choose project template (Web API, Mvc)
- [ ] Set up solution structure
- [ ] Configure appsettings.json
- [ ] Set up environment configurations
- [ ] Create dockerfile if containerizing

## Middleware Configuration Phase

- [ ] Configure routing
- [ ] Add HTTPS redirection
- [ ] Add CORS if needed
- [ ] Add authentication middleware
- [ ] Add authorization middleware
- [ ] Add custom middleware
- [ ] Order middleware correctly
- [ ] Test middleware execution order

## Dependency Injection Phase

- [ ] Register services in ConfigureServices
- [ ] Use DI for controllers and services
- [ ] Register database context
- [ ] Register repositories
- [ ] Register custom services
- [ ] Use dependency injection properly in tests

## Database Configuration Phase

- [ ] Create DbContext
- [ ] Configure connection string
- [ ] Set up migrations
- [ ] Create initial migration
- [ ] Test database connectivity
- [ ] Seed initial data if needed

## Controller Implementation Phase

- [ ] Create API controllers
- [ ] Implement HTTP methods
- [ ] Add input validation
- [ ] Return proper status codes
- [ ] Add error handling
- [ ] Document endpoints

## Model Binding Phase

- [ ] Create DTOs for requests/responses
- [ ] Set up model validation attributes
- [ ] Test model binding works
- [ ] Handle validation errors
- [ ] Return validation error response

## Routing Configuration Phase

- [ ] Configure route templates
- [ ] Use attribute routing
- [ ] Set up API versioning routes
- [ ] Test all routes work
- [ ] Document route patterns

## Authentication Phase

- [ ] Set up JWT authentication
- [ ] Configure authentication in middleware
- [ ] Create token generation service
- [ ] Implement login endpoint
- [ ] Test authentication flow

## Authorization Phase

- [ ] Implement authorization policies
- [ ] Add policy-based authorization
- [ ] Implement role-based access
- [ ] Add [Authorize] attributes
- [ ] Test authorization

## Exception Handling Phase

- [ ] Create custom exception classes
- [ ] Implement global exception handler
- [ ] Return consistent error responses
- [ ] Log exceptions appropriately
- [ ] Test exception handling

## Logging Phase

- [ ] Configure logging provider
- [ ] Add logging throughout app
- [ ] Configure log levels per class
- [ ] Implement structured logging
- [ ] Test logging output

## Health Checks Phase

- [ ] Implement health check endpoints
- [ ] Check critical dependencies
- [ ] Test health checks
- [ ] Implement in orchestration if containerized

## Testing Phase

- [ ] Create unit tests
- [ ] Create integration tests
- [ ] Test controllers
- [ ] Test services
- [ ] Aim for 80%+ coverage

## Performance Phase

- [ ] Implement caching
- [ ] Optimize database queries
- [ ] Use async/await properly
- [ ] Implement response compression
- [ ] Load test application

## Security Phase

- [ ] Implement input validation
- [ ] Implement HTTPS
- [ ] Implement CSRF protection if needed
- [ ] Secure sensitive configuration
- [ ] Implement rate limiting
- [ ] Test security controls

## Deployment Phase

- [ ] Create Docker image if needed
- [ ] Set up CI/CD pipeline
- [ ] Configure health checks
- [ ] Set up monitoring
- [ ] Document deployment process