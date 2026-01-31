# Bun Runtime: LLM Prompts

Prompts for AI-assisted Bun development.

## Project Setup Prompts

### Initial Setup

```
I want to create a new TypeScript project using Bun runtime.

Requirements:
- HTTP server with routing
- PostgreSQL database
- JWT authentication
- Input validation with Zod
- Docker deployment

Please provide:
1. Complete project structure
2. Configuration files (bunfig.toml, tsconfig.json, package.json)
3. Example routes with validation
4. Dockerfile for production
```

### Migration Assessment

```
I have an existing Node.js + Express application that I want to migrate to Bun.

Current stack:
- Node.js 20
- Express 4.x
- PostgreSQL with node-postgres
- Jest for testing
- Docker deployment

Please analyze:
1. Which dependencies need replacement?
2. What code patterns need updating?
3. Potential compatibility issues?
4. Step-by-step migration plan with risks
```

## Development Prompts

### API Development

```
Create a RESTful API endpoint using Bun + Hono for [resource name].

Requirements:
- CRUD operations (GET, POST, PUT, DELETE)
- Input validation with Zod schemas
- JWT authentication middleware
- PostgreSQL database queries
- Error handling with proper HTTP status codes
- TypeScript types for all entities

Include:
1. Route handlers
2. Validation schemas
3. Database queries
4. Authentication middleware
5. Unit tests
```

### WebSocket Implementation

```
Implement a WebSocket server in Bun for [feature description].

Requirements:
- Real-time bidirectional communication
- Room/channel support
- Message broadcasting
- Connection management (join, leave, disconnect)
- Error handling

Provide:
1. WebSocket server setup
2. Message protocol (TypeScript types)
3. Client management logic
4. Example client-side code (TypeScript)
```

### File Upload System

```
Create a file upload system using Bun's native APIs.

Requirements:
- Support multiple file types: [list types]
- Max file size: [size]
- File validation (type, size)
- Store files in [storage location]
- Generate unique filenames
- Serve files via HTTP endpoint

Include:
1. Upload endpoint with multipart/form-data handling
2. File validation logic
3. Storage implementation using Bun.file/Bun.write
4. File serving endpoint
5. Error handling
```

## Testing Prompts

### Unit Test Generation

```
Generate comprehensive unit tests for this Bun code:

[paste code here]

Requirements:
- Use bun:test framework
- Cover happy path and error cases
- Mock external dependencies
- Test edge cases
- Include TypeScript types

Provide:
- Test file structure
- Mock setup
- Test cases with descriptions
- Assertions for expected behavior
```

### Integration Test Setup

```
Create integration tests for a Bun API with PostgreSQL.

Setup:
- Bun HTTP server with Hono
- PostgreSQL database
- Test database setup/teardown
- API endpoints: [list endpoints]

Provide:
1. Test database configuration
2. Setup/teardown hooks
3. Example integration tests
4. Test data fixtures
```

## Migration Prompts

### Node.js to Bun

```
Convert this Node.js code to use Bun-native APIs:

[paste Node.js code]

Replace:
- fs/promises → Bun.file / Bun.write
- node-fetch → native fetch
- bcrypt → Bun.password
- dotenv → Bun.env

Maintain the same functionality while leveraging Bun's performance advantages.
```

### Express to Hono

```
Migrate this Express.js application to Hono framework for Bun:

[paste Express code]

Requirements:
- Keep the same API routes
- Convert middleware to Hono equivalents
- Use Zod for validation instead of express-validator
- Maintain error handling
- Preserve authentication logic

Provide:
1. Converted Hono code
2. Middleware equivalents
3. Any breaking changes noted
```

## Optimization Prompts

### Performance Analysis

```
Analyze this Bun application for performance improvements:

[paste code or describe architecture]

Focus areas:
- Database query optimization
- Caching opportunities
- Connection pooling
- Memory usage
- Response time

Provide:
1. Performance bottlenecks identified
2. Specific optimization recommendations
3. Code examples for improvements
4. Expected performance gains
```

### Bundle Optimization

```
Optimize the build configuration for this Bun application:

Project details:
- Target: [bun/node/browser]
- Entry points: [list]
- Dependencies: [list key dependencies]
- Deployment: [environment]

Provide:
1. Optimized build command
2. bunfig.toml configuration
3. Code splitting strategy
4. Tree shaking opportunities
5. Source map configuration for production
```

## Troubleshooting Prompts

### Debug Compatibility Issues

```
I'm getting this error when running my code in Bun:

[paste error message]

Code that causes the error:
[paste code]

This worked in Node.js. Help me:
1. Understand why it fails in Bun
2. Find the Bun-compatible alternative
3. Refactor the code to work with Bun
4. Prevent similar issues in the future
```

### Database Connection Issues

```
My Bun application fails to connect to PostgreSQL with this error:

[paste error]

Configuration:
- Bun version: [version]
- PostgreSQL version: [version]
- Connection library: [pg/postgres/etc]
- Environment: [Docker/local/cloud]

Provide:
1. Diagnosis of the issue
2. Correct connection configuration
3. Environment variable setup
4. Testing approach to verify connection
```

## Best Practices Prompts

### Project Structure Review

```
Review this Bun project structure and suggest improvements:

[paste directory tree]

Evaluate:
- File organization
- Separation of concerns
- Module boundaries
- Testing structure
- Configuration management

Provide specific recommendations following Bun best practices.
```

### Security Audit

```
Perform a security audit of this Bun application:

[paste relevant code or describe architecture]

Check for:
- Authentication/authorization vulnerabilities
- Input validation gaps
- Dependency security issues
- Environment variable exposure
- SQL injection risks
- XSS vulnerabilities

Provide:
1. Identified security issues
2. Severity ratings
3. Remediation recommendations
4. Secure code examples
```

## Documentation Prompts

### API Documentation

```
Generate API documentation for these Bun + Hono routes:

[paste routes code]

Include:
- Endpoint descriptions
- HTTP methods
- Request/response schemas
- Authentication requirements
- Error responses
- Example requests (curl)

Format: OpenAPI 3.0 or Markdown
```

### README Generation

```
Create a comprehensive README for this Bun project:

Project details:
- Name: [name]
- Description: [description]
- Tech stack: Bun, [other technologies]
- Key features: [list features]

Include:
1. Project overview
2. Prerequisites (Bun version, etc.)
3. Installation instructions
4. Environment variables
5. Running locally
6. Running tests
7. Docker deployment
8. API documentation link
9. Contributing guidelines
10. License
```

## Learning Prompts

### Concept Explanation

```
Explain how [Bun concept] works and when to use it.

Concepts:
- Bun.serve vs framework (Express/Hono)
- Bun.file vs fs/promises
- Bun.password vs bcrypt
- bun test vs Jest/Vitest
- bun build vs webpack/vite

Provide:
- Explanation with examples
- Advantages/disadvantages
- Use cases
- Migration guide from traditional approach
```

### Code Example Request

```
Show me a complete example of [feature] in Bun.

Feature: [describe feature]

Requirements:
- Production-ready code
- TypeScript with strict types
- Error handling
- Tests included
- Comments explaining key concepts

Focus on Bun-specific APIs and best practices.
```

## Advanced Prompts

### Microservices Architecture

```
Design a microservices architecture using Bun for:

[describe system]

Requirements:
- [number] microservices
- Service communication: [REST/gRPC/events]
- Data storage: [databases]
- Authentication: JWT
- Deployment: Docker + Kubernetes

Provide:
1. System architecture diagram
2. Service boundaries and responsibilities
3. Communication patterns
4. Data management strategy
5. Deployment configuration
6. Example implementation for one service
```

### Real-Time Features

```
Implement real-time features using Bun WebSocket:

[describe feature]

Requirements:
- WebSocket connection management
- Real-time data synchronization
- Conflict resolution
- Offline support strategy
- Scalability (multiple server instances)

Provide:
1. Server-side implementation (Bun WebSocket)
2. Client-side implementation (TypeScript)
3. Message protocol design
4. State management approach
5. Scaling considerations (Redis pub/sub?)
```
