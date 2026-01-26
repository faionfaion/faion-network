# MCP LLM Prompts

Prompts for AI-assisted MCP development.

## Server Development

### Create MCP Server

```
Create an MCP server in [TypeScript/Python] with the following requirements:

**Server Name:** [name]
**Purpose:** [description]

**Tools:**
1. [tool_name] - [description] - Params: [params]
2. [tool_name] - [description] - Params: [params]

**Resources:**
1. [uri_scheme] - [description]
2. [uri_scheme] - [description]

**Prompts:**
1. [prompt_name] - [description] - Args: [args]

Requirements:
- Use official MCP SDK
- Include proper error handling
- Add input validation
- Follow MCP 2025-11-25 specification
- Use stdio transport
```

### Add Tool to Existing Server

```
Add a new tool to my MCP server:

**Tool Name:** [name]
**Description:** [what it does]

**Input Schema:**
- [param1]: [type] - [description] (required/optional)
- [param2]: [type] - [description] (required/optional)

**Output:**
- [describe expected output format]

**Error Cases:**
- [error case 1]
- [error case 2]

Existing server code:
```[language]
[paste existing code]
```

Generate the tool implementation following MCP best practices.
```

### Design Resource Schema

```
Design MCP resources for a [type] system:

**Domain:** [description]

**Data to expose:**
1. [data type 1]
2. [data type 2]
3. [data type 3]

Requirements:
- Define appropriate URI schemes
- Support both static and dynamic resources
- Include resource templates where appropriate
- Add proper MIME types
- Consider subscriptions for real-time updates

Provide:
1. Resource list with URIs
2. Resource templates
3. Sample resource contents
4. Implementation code
```

### Create Prompt Templates

```
Create MCP prompts for [use case]:

**Prompts needed:**
1. [prompt_name] - [purpose]
2. [prompt_name] - [purpose]

For each prompt:
- Define clear arguments
- Structure the prompt message effectively
- Support multi-turn conversations if needed
- Include embedded resources where helpful

Target LLM: [Claude/GPT-4/etc.]
Output format: MCP prompt definitions with implementation
```

## Debugging & Troubleshooting

### Debug Connection Issues

```
Help me debug MCP connection issues.

**Server:** [language/framework]
**Client:** [Claude Desktop/Claude Code/custom]
**Transport:** [stdio/HTTP+SSE/WebSocket]

**Error message:**
```
[paste error]
```

**Server code:**
```[language]
[paste relevant code]
```

**Configuration:**
```json
[paste config]
```

What I've tried:
- [attempt 1]
- [attempt 2]

Diagnose the issue and provide solutions.
```

### Fix Tool Execution Error

```
My MCP tool is returning errors. Help me fix it.

**Tool name:** [name]
**Expected behavior:** [description]
**Actual behavior:** [what's happening]

**Tool implementation:**
```[language]
[paste code]
```

**Error response:**
```json
[paste error response]
```

**Test input:**
```json
[paste test input]
```

Analyze the issue and provide fixed implementation.
```

### Validate MCP Messages

```
Validate these MCP JSON-RPC messages for correctness:

**Request:**
```json
[paste request]
```

**Response:**
```json
[paste response]
```

Check:
1. JSON-RPC 2.0 compliance
2. MCP 2025-11-25 specification compliance
3. Schema correctness
4. Error handling
5. Best practices

Identify issues and provide corrected versions.
```

## Architecture & Design

### Design MCP Architecture

```
Design an MCP server architecture for:

**System:** [description]
**Integrations:** [list of systems to integrate]
**Users:** [who will use it]

Requirements:
- [requirement 1]
- [requirement 2]
- [requirement 3]

Consider:
1. Tool organization and naming
2. Resource structure and URIs
3. Prompt templates for common workflows
4. Security constraints
5. Performance requirements
6. Scalability needs

Provide:
1. Architecture diagram (text-based)
2. Component breakdown
3. Tool/resource/prompt catalog
4. Security model
5. Implementation roadmap
```

### Migrate to MCP

```
Help me migrate from [current approach] to MCP:

**Current implementation:**
```[language]
[paste current code/API definitions]
```

**Current capabilities:**
1. [capability 1]
2. [capability 2]
3. [capability 3]

Requirements:
- Maintain backward compatibility where possible
- Follow MCP best practices
- Optimize for LLM consumption
- Include proper error handling

Provide:
1. Migration plan
2. MCP server implementation
3. Configuration for Claude Code/Desktop
4. Testing strategy
```

### Multi-Server Architecture

```
Design a multi-server MCP architecture:

**Servers needed:**
1. [server 1] - [responsibility]
2. [server 2] - [responsibility]
3. [server 3] - [responsibility]

**Shared resources:** [list]
**Cross-server workflows:** [describe]

Requirements:
- Clear separation of concerns
- Minimal duplication
- Efficient resource sharing
- Coordinated error handling

Provide:
1. Server responsibility matrix
2. Inter-server communication patterns
3. Client configuration
4. Deployment strategy
```

## Security & Best Practices

### Security Review

```
Review this MCP server for security issues:

```[language]
[paste server code]
```

Check for:
1. Input validation vulnerabilities
2. Path traversal risks
3. Injection attacks (SQL, command, etc.)
4. Information disclosure
5. Access control issues
6. Rate limiting needs
7. Credential handling

Provide:
1. Security findings (severity, description, location)
2. Remediation recommendations
3. Fixed code snippets
4. Security best practices to add
```

### Performance Optimization

```
Optimize this MCP server for performance:

**Current implementation:**
```[language]
[paste code]
```

**Performance issues:**
- [issue 1]
- [issue 2]

**Metrics:**
- Current latency: [value]
- Expected latency: [value]
- Request volume: [value]

Analyze and provide:
1. Performance bottlenecks
2. Optimization strategies
3. Optimized code
4. Caching recommendations
5. Monitoring suggestions
```

## Testing

### Generate Test Suite

```
Generate a comprehensive test suite for this MCP server:

```[language]
[paste server code]
```

Include tests for:
1. Tool invocation (success and error cases)
2. Resource reading
3. Prompt retrieval
4. Input validation
5. Error handling
6. Edge cases

Testing framework: [pytest/jest/etc.]
Coverage target: [percentage]

Provide:
1. Unit tests
2. Integration tests
3. Mock implementations
4. Test utilities
```

### Test MCP Integration

```
Create integration tests for MCP server-client communication:

**Server:** [language/framework]
**Transport:** [stdio/HTTP]

**Scenarios to test:**
1. [scenario 1]
2. [scenario 2]
3. [scenario 3]

Provide:
1. Test client setup
2. Test cases for each scenario
3. Assertions and validations
4. CI/CD integration
```

## Documentation

### Generate Documentation

```
Generate comprehensive documentation for this MCP server:

```[language]
[paste server code]
```

Include:
1. Overview and purpose
2. Installation instructions
3. Configuration guide
4. Tool reference (with examples)
5. Resource reference (with URI examples)
6. Prompt reference (with argument examples)
7. Error handling guide
8. Security considerations
9. Troubleshooting

Format: Markdown
```

### Generate OpenAPI Spec

```
Generate OpenAPI specification for this MCP server's HTTP endpoints:

```[language]
[paste server code]
```

Include:
1. All endpoints (SSE, message handling)
2. Request/response schemas
3. Authentication requirements
4. Error responses
5. Examples

OpenAPI version: 3.1.0
```

## Quick Reference Prompts

### Convert API to MCP Tool

```
Convert this REST API endpoint to an MCP tool:

Endpoint: [METHOD] [path]
Request body: [schema]
Response: [schema]
Authentication: [type]

Provide MCP tool definition and implementation.
```

### Create MCP Client

```
Create an MCP client in [language] that connects to servers via [transport].

Required operations:
1. List and call tools
2. Read resources
3. Get prompts
4. Handle notifications

Include proper error handling and reconnection logic.
```

### Debug Tool Not Working

```
My MCP tool "[name]" isn't working in [Claude Desktop/Claude Code].

Server logs: [paste]
Client behavior: [describe]
Expected: [describe]
Actual: [describe]

Config: [paste]

What's wrong and how to fix?
```

---

*MCP LLM Prompts v2025-11-25*
