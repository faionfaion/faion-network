# Tool Use Checklists

Comprehensive checklists for designing, implementing, and securing tool use in LLM applications.

---

## Tool Design Checklist

### Naming and Structure

- [ ] **Descriptive name:** Uses action verbs (`get_`, `create_`, `update_`, `delete_`, `search_`)
- [ ] **Consistent naming:** Follows project naming conventions
- [ ] **No abbreviations:** Full words for clarity (`get_user_profile`, not `get_usr_prof`)
- [ ] **Unique names:** No conflicts with other tools in the system
- [ ] **Lowercase with underscores:** Snake_case for all tool names

### Description Quality

- [ ] **Clear purpose:** First sentence explains what the tool does
- [ ] **Use cases:** Describes when to use this tool
- [ ] **Limitations:** Notes what the tool cannot do
- [ ] **Examples:** Includes example queries that should trigger this tool
- [ ] **Output format:** Describes what the tool returns
- [ ] **Concise:** Under 200 characters to minimize token usage

### Parameter Design

- [ ] **JSON Schema compliant:** Valid JSON Schema for parameters
- [ ] **Type definitions:** All parameters have explicit types
- [ ] **Required fields:** Only truly required parameters marked as required
- [ ] **Default values:** Sensible defaults for optional parameters
- [ ] **Enums for choices:** Use enums for limited value sets
- [ ] **Descriptions:** Each parameter has a clear description
- [ ] **Examples:** Include example values in descriptions
- [ ] **Validation rules:** Min/max, patterns, formats specified

### Scope and Responsibility

- [ ] **Single responsibility:** Tool does one thing well
- [ ] **Appropriate granularity:** Not too broad, not too narrow
- [ ] **Minimal side effects:** Clear about what changes state
- [ ] **Idempotent when possible:** Repeated calls produce same result
- [ ] **Composable:** Can be combined with other tools

### Tool Set Design

- [ ] **Reasonable count:** Fewer than 20 tools per context
- [ ] **No overlap:** Tools have distinct responsibilities
- [ ] **Complete coverage:** All needed operations are covered
- [ ] **Consistent patterns:** Similar tools have similar interfaces
- [ ] **Grouped logically:** Related tools follow similar naming

---

## Implementation Checklist

### Core Implementation

- [ ] **Input validation:** Validate all parameters before execution
- [ ] **Type checking:** Verify parameter types match schema
- [ ] **Null handling:** Handle missing optional parameters
- [ ] **Error handling:** Catch and handle all exceptions
- [ ] **Structured responses:** Return consistent JSON structure
- [ ] **Error messages:** Provide actionable error descriptions

### External API Integration

- [ ] **Timeout configuration:** Set reasonable request timeouts
- [ ] **Retry logic:** Implement exponential backoff for transient errors
- [ ] **Rate limiting:** Respect API rate limits
- [ ] **Circuit breaker:** Prevent cascading failures
- [ ] **Connection pooling:** Reuse HTTP connections efficiently
- [ ] **API key rotation:** Support credential rotation

### Execution Management

- [ ] **Parallel execution:** Execute independent tools concurrently
- [ ] **Dependency handling:** Sequential execution for dependent tools
- [ ] **Max iterations:** Limit agentic loop iterations
- [ ] **Max tool calls:** Limit total tool calls per request
- [ ] **Timeout per tool:** Individual tool execution limits
- [ ] **Cancellation support:** Allow cancelling long-running operations

### Response Handling

- [ ] **Consistent structure:** All tools return same response format
- [ ] **Success indicator:** Clear success/failure status
- [ ] **Error details:** Structured error information
- [ ] **Partial results:** Handle partial successes appropriately
- [ ] **Large responses:** Truncate or paginate large outputs
- [ ] **Serialization:** Properly serialize all response types

### Tool Result Processing

```python
# Standard response structure
{
    "success": True,
    "data": {...},      # Actual result
    "error": None,      # Error message if failed
    "metadata": {       # Optional metadata
        "execution_time_ms": 123,
        "cached": False
    }
}
```

### Testing

- [ ] **Unit tests:** Test each tool in isolation
- [ ] **Input validation tests:** Test with invalid inputs
- [ ] **Error scenario tests:** Test error handling paths
- [ ] **Integration tests:** Test with actual LLM calls
- [ ] **Load tests:** Verify performance under load
- [ ] **Regression tests:** Catch breaking changes

### Monitoring and Logging

- [ ] **Request logging:** Log all tool call requests
- [ ] **Response logging:** Log all tool responses (sanitized)
- [ ] **Error logging:** Log all errors with stack traces
- [ ] **Metrics collection:** Track latency, success rate, usage
- [ ] **Alerting:** Alert on error spikes or latency degradation
- [ ] **Cost tracking:** Monitor token usage per tool

---

## Security Checklist

### Input Validation

- [ ] **Schema validation:** Validate against JSON Schema
- [ ] **Type coercion:** Strictly check types, don't auto-convert
- [ ] **Length limits:** Enforce max lengths for strings
- [ ] **Range checks:** Validate numeric ranges
- [ ] **Pattern matching:** Validate formats (emails, URLs, etc.)
- [ ] **Sanitization:** Clean inputs before use
- [ ] **Injection prevention:** Escape special characters

### Authentication and Authorization

- [ ] **User context:** Pass user identity to tools
- [ ] **Permission checks:** Verify user can perform action
- [ ] **Resource ownership:** Verify user owns requested resources
- [ ] **Role-based access:** Respect role permissions
- [ ] **Scope limitations:** Limit tool capabilities per context
- [ ] **Session validation:** Verify session is valid

### Secrets Management

- [ ] **No hardcoded secrets:** No credentials in code
- [ ] **Environment variables:** Use env vars or secret managers
- [ ] **Secret rotation:** Support credential rotation
- [ ] **No logging secrets:** Never log credentials
- [ ] **No exposure:** Never include secrets in tool definitions
- [ ] **Secure storage:** Use encrypted secret storage

### Data Protection

- [ ] **PII handling:** Identify and protect personal data
- [ ] **Data minimization:** Only request necessary data
- [ ] **Encryption in transit:** Use HTTPS for all API calls
- [ ] **Encryption at rest:** Encrypt stored sensitive data
- [ ] **Audit trail:** Log data access for compliance
- [ ] **Retention policies:** Delete data per retention rules

### Dangerous Operations

- [ ] **Human approval:** Require confirmation for destructive actions
- [ ] **Dry run mode:** Support preview of changes
- [ ] **Reversibility:** Provide undo capabilities where possible
- [ ] **Soft delete:** Prefer soft delete over hard delete
- [ ] **Batch limits:** Limit bulk operations
- [ ] **Confirmation tokens:** Require confirmation for sensitive ops

### Sandboxing and Isolation

- [ ] **Execution isolation:** Run tools in sandboxed environment
- [ ] **Resource limits:** CPU, memory, time limits
- [ ] **Network restrictions:** Limit network access
- [ ] **File system restrictions:** Limit file system access
- [ ] **Process isolation:** Separate processes for untrusted code
- [ ] **Container isolation:** Use containers for execution

### API Security

- [ ] **API key security:** Secure API key storage and usage
- [ ] **Request signing:** Sign requests where supported
- [ ] **CORS configuration:** Proper CORS settings
- [ ] **IP allowlisting:** Restrict API access by IP
- [ ] **Rate limiting:** Prevent abuse with rate limits
- [ ] **DDoS protection:** Protect against denial of service

---

## Production Readiness Checklist

### Configuration

- [ ] **Environment-based config:** Different configs per environment
- [ ] **Feature flags:** Toggle tools on/off without deploy
- [ ] **Dynamic configuration:** Update configs without restart
- [ ] **Validation:** Validate configuration at startup
- [ ] **Defaults:** Sensible defaults for all settings

### Reliability

- [ ] **Health checks:** Endpoint to verify tool availability
- [ ] **Graceful degradation:** Continue working if tool fails
- [ ] **Fallback strategies:** Alternative paths when tools fail
- [ ] **Recovery procedures:** Documented recovery steps
- [ ] **Backup tools:** Redundant implementations for critical tools

### Scalability

- [ ] **Horizontal scaling:** Tools can scale horizontally
- [ ] **Caching:** Cache frequent tool results
- [ ] **Connection pooling:** Efficient connection management
- [ ] **Async execution:** Non-blocking tool execution
- [ ] **Queue-based:** Use queues for heavy processing

### Documentation

- [ ] **API documentation:** Complete tool API docs
- [ ] **Usage examples:** Examples for each tool
- [ ] **Error codes:** Documented error codes and meanings
- [ ] **Troubleshooting:** Common issues and solutions
- [ ] **Runbooks:** Operational procedures

### Observability

- [ ] **Structured logging:** JSON logs with correlation IDs
- [ ] **Distributed tracing:** Trace requests across services
- [ ] **Metrics dashboards:** Visualize key metrics
- [ ] **Alerting rules:** Alerts for critical conditions
- [ ] **SLO monitoring:** Track service level objectives

---

## Pre-Deployment Checklist

### Code Review

- [ ] **Security review:** Security team approval
- [ ] **Architecture review:** Design reviewed and approved
- [ ] **Code quality:** Passes linting and static analysis
- [ ] **Test coverage:** Adequate test coverage (>80%)
- [ ] **Documentation:** All tools documented

### Testing

- [ ] **Unit tests pass:** All unit tests green
- [ ] **Integration tests pass:** All integration tests green
- [ ] **Performance tests pass:** Meets performance requirements
- [ ] **Security scan:** No critical vulnerabilities
- [ ] **LLM testing:** Tested with actual LLM calls

### Deployment

- [ ] **Rollback plan:** Documented rollback procedure
- [ ] **Canary deployment:** Gradual rollout plan
- [ ] **Monitoring ready:** Dashboards and alerts configured
- [ ] **Runbook ready:** Operational procedures documented
- [ ] **On-call prepared:** Team briefed on new tools

---

## Quick Reference: Tool Quality Rubric

| Aspect | Poor | Good | Excellent |
|--------|------|------|-----------|
| **Name** | `do_thing` | `get_weather` | `get_current_weather_by_location` |
| **Description** | "Gets weather" | "Get weather for location" | "Get current weather conditions including temperature, humidity, and forecast for a specific location" |
| **Parameters** | No types | Types defined | Types + descriptions + examples |
| **Error handling** | Crashes | Returns error string | Structured error with code and details |
| **Security** | No validation | Basic validation | Full validation + sanitization + auth |
| **Testing** | None | Unit tests | Unit + integration + load tests |
| **Monitoring** | Logs only | Logs + metrics | Full observability stack |
