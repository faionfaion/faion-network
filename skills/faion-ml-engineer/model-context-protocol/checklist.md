# MCP Implementation Checklist

## Server Implementation

### Setup

- [ ] Choose SDK (TypeScript, Python, C#, Go)
- [ ] Install dependencies
  - TypeScript: `npm install @modelcontextprotocol/sdk zod`
  - Python: `pip install mcp`
- [ ] Choose transport (stdio, HTTP+SSE, WebSocket)
- [ ] Define server metadata (name, version, description)

### Capabilities Declaration

- [ ] Declare `tools` capability (if providing tools)
  - [ ] Set `listChanged: true` if tool list can change
- [ ] Declare `resources` capability (if providing resources)
  - [ ] Set `subscribe: true` if supporting subscriptions
  - [ ] Set `listChanged: true` if resource list can change
- [ ] Declare `prompts` capability (if providing prompts)
  - [ ] Set `listChanged: true` if prompt list can change

### Tools Implementation

- [ ] Define tool schemas with JSON Schema
  - [ ] Unique `name` (1-128 chars, alphanumeric + `_-.)
  - [ ] Clear `description` for LLM understanding
  - [ ] Valid `inputSchema` (type: object)
  - [ ] Optional `outputSchema` for structured responses
- [ ] Implement `tools/list` handler
- [ ] Implement `tools/call` handler
  - [ ] Validate input against schema
  - [ ] Return content array (text, image, audio, resources)
  - [ ] Set `isError: true` for execution errors
- [ ] Implement `notifications/tools/list_changed` (if listChanged)

### Resources Implementation

- [ ] Define resource URIs (file://, https://, custom://)
- [ ] Implement `resources/list` handler with pagination
- [ ] Implement `resources/read` handler
  - [ ] Return text content (with `text` field)
  - [ ] Return binary content (with `blob` field, base64)
- [ ] Implement `resources/templates/list` for dynamic resources
- [ ] Implement `resources/subscribe` (if subscribe capability)
- [ ] Implement `notifications/resources/updated` for subscriptions
- [ ] Implement `notifications/resources/list_changed` (if listChanged)

### Prompts Implementation

- [ ] Define prompt templates
  - [ ] Unique `name`
  - [ ] Clear `description`
  - [ ] Define `arguments` with required flag
- [ ] Implement `prompts/list` handler with pagination
- [ ] Implement `prompts/get` handler
  - [ ] Validate arguments
  - [ ] Return messages array with role and content
- [ ] Implement `notifications/prompts/list_changed` (if listChanged)

### Error Handling

- [ ] Return JSON-RPC errors for protocol issues
  - [ ] `-32600` Invalid Request
  - [ ] `-32601` Method not found
  - [ ] `-32602` Invalid params
  - [ ] `-32603` Internal error
  - [ ] `-32002` Resource not found
- [ ] Return tool execution errors with `isError: true`
- [ ] Include actionable error messages for LLM self-correction

### Security

- [ ] Validate all input URIs and parameters
- [ ] Implement access controls for sensitive resources
- [ ] Rate limit tool invocations
- [ ] Sanitize all outputs
- [ ] Log operations for audit purposes
- [ ] Never expose credentials in tool descriptions

## Client Implementation

### Setup

- [ ] Choose SDK matching your application
- [ ] Configure transport to match server
- [ ] Implement connection lifecycle

### Connection

- [ ] Send `initialize` request with client capabilities
- [ ] Handle server capability response
- [ ] Store negotiated capabilities
- [ ] Implement reconnection logic

### Tool Consumption

- [ ] Call `tools/list` to discover tools
- [ ] Parse tool schemas for LLM tool definitions
- [ ] Implement `tools/call` invocation
- [ ] Handle tool results (content array)
- [ ] Handle tool errors (isError: true)
- [ ] Implement user confirmation for sensitive operations
- [ ] Subscribe to `notifications/tools/list_changed`

### Resource Consumption

- [ ] Call `resources/list` with pagination
- [ ] Call `resources/templates/list` for dynamic resources
- [ ] Implement `resources/read` for content retrieval
- [ ] Handle text and binary content
- [ ] Implement `resources/subscribe` for updates
- [ ] Handle `notifications/resources/updated`
- [ ] Handle `notifications/resources/list_changed`

### Prompt Consumption

- [ ] Call `prompts/list` with pagination
- [ ] Implement `prompts/get` with arguments
- [ ] Parse prompt messages for LLM consumption
- [ ] Handle `notifications/prompts/list_changed`

### Sampling (if supported)

- [ ] Declare sampling capability
- [ ] Handle `sampling/createMessage` requests from server
- [ ] Implement user approval flow
- [ ] Return sampling results to server

### Security

- [ ] Obtain user consent before tool invocations
- [ ] Show tool inputs before sending to server
- [ ] Validate tool results before passing to LLM
- [ ] Implement timeouts for all requests
- [ ] Log all operations for audit

## Testing

### Unit Tests

- [ ] Test tool schema validation
- [ ] Test resource URI parsing
- [ ] Test prompt argument handling
- [ ] Test error response generation

### Integration Tests

- [ ] Test full initialization flow
- [ ] Test tool invocation end-to-end
- [ ] Test resource reading
- [ ] Test prompt retrieval
- [ ] Test notification handling

### Security Tests

- [ ] Test input validation (SQL injection, path traversal)
- [ ] Test rate limiting
- [ ] Test access control enforcement
- [ ] Test error message safety (no credential leaks)

## Deployment

### Documentation

- [ ] Document all tools with examples
- [ ] Document all resources with URI schemes
- [ ] Document all prompts with argument descriptions
- [ ] Provide usage examples

### Configuration

- [ ] Environment variable handling
- [ ] Transport configuration
- [ ] Logging configuration
- [ ] Error reporting setup

### Monitoring

- [ ] Tool invocation metrics
- [ ] Error rate tracking
- [ ] Latency monitoring
- [ ] Resource usage tracking

---

*MCP Implementation Checklist v2025-11-25*
