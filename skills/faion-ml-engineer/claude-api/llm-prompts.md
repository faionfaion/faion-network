# Claude API LLM Prompts

Prompts for Claude to help with Claude API integration tasks.

## API Integration

### Generate Tool Definition

```
Create a Claude API tool definition for the following function:

Function: {function_name}
Purpose: {description}
Parameters:
- {param1}: {type} - {description}
- {param2}: {type} - {description}

Requirements:
1. Use JSON Schema for input_schema
2. Mark required parameters
3. Add clear descriptions for each parameter
4. Include enum constraints where applicable

Output format: JSON tool definition
```

### Design Tool Set

```
Design a set of Claude API tools for the following use case:

Use Case: {description}
Available Data Sources: {data_sources}
Required Operations: {operations}

Requirements:
1. Create minimal set of tools (prefer fewer, more powerful tools)
2. Each tool should have clear, non-overlapping purpose
3. Tool descriptions should explain WHEN to use them
4. Handle errors gracefully

Output: Tool definitions with example usage
```

### Optimize System Prompt

```
Optimize this system prompt for Claude API:

Current prompt:
{prompt}

Goals:
- {goal1}
- {goal2}

Requirements:
1. Be concise (minimize tokens)
2. Use clear structure (Role, Behavior, Format)
3. Include examples only if essential
4. Avoid redundancy

Output: Optimized system prompt with token count estimate
```

## Troubleshooting

### Debug Tool Loop

```
Help debug this Claude API tool use loop:

Code:
{code}

Error/Issue:
{error_description}

Current behavior:
{current_behavior}

Expected behavior:
{expected_behavior}

Diagnose the issue and provide corrected code.
```

### Fix Streaming Issue

```
Debug this Claude API streaming implementation:

Code:
{code}

Issue:
{issue_description}

Provide:
1. Root cause analysis
2. Corrected code
3. Best practices to prevent similar issues
```

### Resolve Rate Limiting

```
Our Claude API integration is hitting rate limits:

Current usage pattern:
- Requests per minute: {rpm}
- Tokens per minute: {tpm}
- Model: {model}
- Tier: {tier}

Symptoms:
{symptoms}

Provide:
1. Analysis of the issue
2. Retry strategy with exponential backoff
3. Request batching recommendations
4. Caching opportunities
```

## Architecture

### Design Claude Integration

```
Design a Claude API integration for:

Application: {app_description}
Use Cases:
- {use_case_1}
- {use_case_2}

Requirements:
- Model selection rationale
- Tool architecture
- Error handling strategy
- Cost optimization approach
- Caching strategy

Constraints:
- Budget: ${monthly_budget}/month
- Latency: <{latency}ms p95
- Volume: {requests_per_day} requests/day

Output: Architecture document with diagrams
```

### Design Agentic System

```
Design an agentic system using Claude API:

Agent Purpose: {purpose}
Available Tools:
- {tool_1}
- {tool_2}

Required Capabilities:
- {capability_1}
- {capability_2}

Constraints:
- Max iterations: {max_iterations}
- Budget per request: {budget_tokens} tokens

Provide:
1. Agent loop architecture
2. Tool orchestration strategy
3. State management approach
4. Guardrails and safety measures
5. Example implementation
```

### Migrate from OpenAI

```
Help migrate from OpenAI API to Claude API:

Current OpenAI Implementation:
{code_or_description}

OpenAI Features Used:
- {feature_1}
- {feature_2}

Provide:
1. Feature mapping (OpenAI to Claude)
2. Code migration guide
3. Prompt adjustments needed
4. Tool definition conversion
5. Testing strategy
```

## Prompt Engineering

### Improve Prompt Quality

```
Improve this Claude API prompt:

Current Prompt:
{prompt}

Issues:
- {issue_1}
- {issue_2}

Goals:
- Better {metric_1}
- Reduce {metric_2}

Provide:
1. Analysis of current prompt weaknesses
2. Improved prompt
3. A/B testing suggestions
4. Metrics to track
```

### Create Chain-of-Thought Prompt

```
Create a chain-of-thought prompt for:

Task: {task_description}
Input Type: {input_type}
Output Requirements: {output_requirements}

Requirements:
1. Break down reasoning steps
2. Include validation checkpoints
3. Handle edge cases
4. Produce structured output

Output: Complete prompt with examples
```

### Design Multi-Turn Conversation

```
Design a multi-turn conversation flow for:

Use Case: {use_case}
User Goals: {user_goals}
System Behavior: {behavior}

Provide:
1. System prompt
2. Conversation state management
3. Turn-by-turn example dialogue
4. Error recovery strategies
5. Implementation code
```

## Extended Thinking

### Configure Thinking Budget

```
Help configure extended thinking for:

Task Type: {task_type}
Complexity: {low|medium|high|very_high}
Latency Requirements: {requirements}
Cost Constraints: {constraints}

Provide:
1. Recommended budget_tokens
2. When to enable/disable thinking
3. Streaming considerations
4. Cost/quality tradeoff analysis
```

### Design Thinking + Tools Flow

```
Design a flow combining extended thinking with tool use:

Task: {task_description}
Available Tools: {tools}
Reasoning Requirements: {requirements}

Provide:
1. When to use thinking vs tools
2. Interleaved thinking implementation
3. Token budget allocation
4. Example implementation
```

## Cost Optimization

### Analyze API Costs

```
Analyze Claude API costs for our usage:

Current Usage:
- Model: {model}
- Requests/day: {count}
- Avg input tokens: {input}
- Avg output tokens: {output}
- Current monthly cost: ${cost}

Target: Reduce costs by {percentage}%

Provide:
1. Cost breakdown analysis
2. Optimization recommendations
3. Model switching suggestions
4. Caching opportunities
5. Batch API applicability
6. Projected savings
```

### Design Caching Strategy

```
Design a prompt caching strategy for:

Application: {description}
Usage Patterns:
- {pattern_1}
- {pattern_2}

Current costs: ${monthly_cost}
Cacheable content: {content_types}

Provide:
1. What to cache (system prompts, documents, tools)
2. Cache key strategy
3. TTL considerations
4. Implementation code
5. Expected savings
```

## Testing

### Create Test Suite

```
Create a test suite for Claude API integration:

Integration Points:
- {point_1}
- {point_2}

Test Requirements:
- Unit tests for {components}
- Integration tests for {flows}
- Error handling tests
- Rate limit simulation

Provide:
1. Test structure
2. Mock strategies
3. Test cases with expected outputs
4. CI/CD integration
```

### Evaluate Response Quality

```
Create an evaluation framework for Claude API responses:

Use Case: {use_case}
Quality Dimensions:
- {dimension_1}
- {dimension_2}

Provide:
1. Evaluation criteria
2. Scoring rubric
3. LLM-as-judge prompts
4. Human evaluation guidelines
5. Automated metrics
```

## Security

### Audit API Integration

```
Audit this Claude API integration for security:

Code:
{code}

Concerns:
- API key handling
- Input validation
- Output sanitization
- Rate limiting
- Logging

Provide:
1. Security issues found
2. Risk assessment
3. Remediation steps
4. Best practices checklist
```

### Design Guardrails

```
Design guardrails for Claude API usage:

Application: {description}
Risk Profile: {risk_level}
User Base: {user_types}

Requirements:
- Content filtering
- Output validation
- Cost controls
- Abuse prevention

Provide:
1. Input validation strategy
2. Output filtering approach
3. Rate limiting per user
4. Monitoring and alerting
5. Implementation code
```

## Quick Reference Prompts

### Model Selection

```
Recommend Claude model for:
Task: {task}
Volume: {requests}/day
Latency: {requirement}
Budget: ${budget}/month

Consider: accuracy, speed, cost tradeoffs.
```

### Error Resolution

```
Claude API error: {error_message}
Request: {request_summary}
Context: {additional_context}

Diagnose and provide fix.
```

### Performance Optimization

```
Optimize Claude API call:
Current latency: {latency}ms
Current cost: ${cost}/request
Target: {improvement_goal}

Current implementation: {code_snippet}

Suggest optimizations.
```
