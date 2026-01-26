# LLM Prompts for Tool Use

Prompts for designing, debugging, and optimizing tool use with LLMs.

---

## Tool Design Prompts

### Generate Tool Definition

```
I need to create a tool definition for an LLM function calling system.

**Tool Purpose:** {describe what the tool should do}

**Context:**
- Target LLM provider: {OpenAI/Claude/Gemini}
- Use case: {describe the use case}
- Expected inputs: {list expected inputs}
- Expected outputs: {describe expected output}

**Requirements:**
1. Generate a complete tool definition in JSON format
2. Include detailed descriptions for the tool and each parameter
3. Use appropriate JSON Schema types and constraints
4. Mark only truly required parameters as required
5. Include sensible defaults for optional parameters
6. Add enum constraints where applicable

**Output format:**
```json
{
  "name": "...",
  "description": "...",
  "parameters": {...}
}
```

Please generate the tool definition.
```

### Improve Tool Description

```
Improve this tool description for better LLM understanding:

**Current tool:**
```json
{tool_definition}
```

**Issues to address:**
1. Make the description clearer about when to use this tool
2. Add examples of queries that should trigger this tool
3. Improve parameter descriptions with examples
4. Ensure descriptions are concise but informative

**Guidelines:**
- First sentence should clearly state what the tool does
- Include 2-3 example use cases in the description
- Each parameter description should include an example value
- Keep total description under 200 characters for token efficiency

Provide the improved tool definition.
```

### Design Tool Set for Domain

```
Design a comprehensive tool set for the following domain:

**Domain:** {e.g., e-commerce, customer support, data analysis}

**Requirements:**
- Users need to: {list key user actions}
- System integrations: {list systems to integrate with}
- Data sources: {list data sources}

**Constraints:**
- Maximum 15 tools (to avoid LLM confusion)
- Tools should not overlap in functionality
- Each tool should have a single responsibility

**Output format:**
For each tool, provide:
1. Name and description
2. Parameters with types
3. Example use cases
4. Dependencies on other tools (if any)

Design the tool set with clear naming conventions and consistent patterns.
```

### Convert API Endpoint to Tool

```
Convert this API endpoint into an LLM tool definition:

**API Documentation:**
```
Endpoint: {endpoint}
Method: {method}
Description: {description}

Request Parameters:
{parameters}

Response:
{response_format}
```

**Requirements:**
1. Map API parameters to tool parameters
2. Simplify complex nested structures where possible
3. Add user-friendly descriptions
4. Handle authentication separately (not as a parameter)
5. Include error response handling guidance in description

Generate the tool definition and a sample implementation function.
```

---

## Debugging Prompts

### Diagnose Tool Selection Issues

```
The LLM is not selecting the correct tool. Help me diagnose the issue.

**Available tools:**
```json
{list_of_tools}
```

**User query:** "{user_query}"

**Expected tool:** {expected_tool}
**Actual tool selected:** {actual_tool} (or none)

**Analysis needed:**
1. Why might the LLM have chosen the wrong tool?
2. Is there ambiguity between tool descriptions?
3. Are the tool descriptions clear enough?
4. Should the user query trigger tool use at all?

**Provide:**
1. Root cause analysis
2. Specific improvements to tool definitions
3. Alternative query phrasings that would work
4. System prompt improvements if needed
```

### Debug Tool Execution Errors

```
A tool is failing during execution. Help me debug.

**Tool definition:**
```json
{tool_definition}
```

**LLM-generated arguments:**
```json
{arguments}
```

**Error:**
```
{error_message}
```

**Tool implementation:**
```python
{implementation}
```

**Analysis needed:**
1. Is the error in the arguments or implementation?
2. Are the arguments valid according to the schema?
3. Should the tool handle this case differently?
4. How can we make the error recoverable?

Provide a diagnosis and fix.
```

### Analyze Tool Loop Issues

```
The agent is stuck in a tool calling loop. Help me diagnose.

**Conversation history:**
```
{conversation_history_with_tool_calls}
```

**Tools available:**
```json
{tools}
```

**Observations:**
- Number of iterations: {count}
- Pattern observed: {describe pattern}

**Questions:**
1. Why is the agent not reaching a final answer?
2. Is there missing information the agent needs?
3. Are the tool results insufficient?
4. Is the system prompt causing this behavior?

Provide analysis and solutions.
```

### Fix Malformed Tool Arguments

```
The LLM is generating malformed tool arguments. Help me fix this.

**Tool definition:**
```json
{tool_definition}
```

**Examples of malformed arguments:**
```json
// Example 1
{malformed_args_1}

// Example 2
{malformed_args_2}
```

**Expected format:**
```json
{expected_format}
```

**Questions:**
1. What's causing the malformation?
2. Should the tool definition be clearer?
3. Should we add examples to the description?
4. Is the schema too complex?

Provide fixes for the tool definition and any system prompt changes needed.
```

---

## Optimization Prompts

### Optimize Tool Definitions for Tokens

```
Optimize these tool definitions to reduce token usage while maintaining clarity.

**Current tools:**
```json
{tools}
```

**Current token count:** {count} tokens

**Target:** Reduce by at least 30% without losing essential information

**Optimization strategies to consider:**
1. Shorten descriptions while keeping clarity
2. Remove redundant information
3. Use shorter parameter names
4. Simplify nested structures
5. Consolidate similar tools if appropriate

Provide optimized definitions with token count comparison.
```

### Improve Tool Selection Accuracy

```
Improve tool selection accuracy for this system.

**Current tools:**
```json
{tools}
```

**Problematic queries:**
| Query | Expected Tool | Actual Tool | Issue |
|-------|---------------|-------------|-------|
{problem_cases}

**Analysis needed:**
1. Identify patterns in misclassification
2. Find overlapping tool responsibilities
3. Detect ambiguous descriptions

**Provide:**
1. Root cause analysis for each issue
2. Improved tool definitions
3. System prompt additions if needed
4. Test queries to verify improvements
```

### Reduce Tool Call Latency

```
Help me reduce latency in this tool-calling system.

**Current architecture:**
{describe_architecture}

**Metrics:**
- Average tool execution time: {time}ms
- Average LLM response time: {time}ms
- Average total time: {time}ms
- Tool calls per request: {count}

**Bottlenecks identified:**
{list_bottlenecks}

**Optimization options to consider:**
1. Parallel tool execution
2. Tool result caching
3. Reducing number of tool calls
4. Streaming responses
5. Batching similar operations

Provide optimization recommendations with expected impact.
```

### Design Tool Caching Strategy

```
Design a caching strategy for these tools.

**Tools:**
```json
{tools}
```

**Usage patterns:**
- Most frequently called: {tool_names}
- Average arguments per tool: {data}
- Result change frequency: {data}

**Requirements:**
1. Identify which tools benefit from caching
2. Determine appropriate TTLs for each tool
3. Define cache key strategies
4. Handle cache invalidation

**Considerations:**
- Some data is time-sensitive (weather, stock prices)
- Some data rarely changes (user profiles, product details)
- Some operations should never be cached (writes, payments)

Provide a complete caching strategy with implementation guidance.
```

---

## Agent Design Prompts

### Design Agent System Prompt

```
Design a system prompt for an agent with these tools.

**Agent purpose:** {describe agent purpose}

**Available tools:**
```json
{tools}
```

**Behavioral requirements:**
1. {requirement_1}
2. {requirement_2}
3. {requirement_3}

**Tone and style:** {describe desired tone}

**Constraints:**
- {constraint_1}
- {constraint_2}

**The system prompt should:**
1. Clearly define the agent's role
2. Explain when to use each tool
3. Define the reasoning approach (ReAct, CoT, etc.)
4. Set boundaries for behavior
5. Handle edge cases gracefully

Generate a complete system prompt.
```

### Design Multi-Agent Workflow

```
Design a multi-agent workflow for this task.

**Task:** {describe task}

**Available capabilities:**
- Research and information gathering
- Data analysis and processing
- Content creation and writing
- Code generation and execution

**Requirements:**
1. Define specialized agents needed
2. Specify tools for each agent
3. Design handoff protocols between agents
4. Handle error cases and retries

**Output:**
1. Agent definitions (name, role, tools)
2. Workflow diagram
3. System prompts for each agent
4. Handoff message templates
```

### Design Tool Router

```
Design a tool router for a large tool set.

**Problem:** We have {count} tools, which is too many for reliable selection.

**Tools by category:**
```
{categorized_tools}
```

**Requirements:**
1. Design a routing strategy to select relevant tools per query
2. Keep active tools under 10 per request
3. Maintain high accuracy in tool selection
4. Minimize latency impact

**Options to consider:**
1. Category-based routing (pre-classify query)
2. RAG-based tool selection (embed tool descriptions)
3. Two-stage selection (router LLM + executor LLM)
4. Hybrid approach

Design the router with implementation details.
```

---

## Testing and Evaluation Prompts

### Generate Tool Test Cases

```
Generate comprehensive test cases for this tool.

**Tool definition:**
```json
{tool_definition}
```

**Tool implementation:**
```python
{implementation}
```

**Generate test cases for:**
1. Happy path - valid inputs, expected outputs
2. Edge cases - boundary values, empty inputs
3. Error cases - invalid inputs, missing required params
4. Security cases - injection attempts, oversized inputs
5. Performance cases - large inputs, concurrent calls

**Format:**
| Test Name | Input | Expected Output | Category |
|-----------|-------|-----------------|----------|
...
```

### Evaluate Tool Selection Accuracy

```
Create an evaluation dataset for tool selection accuracy.

**Tools:**
```json
{tools}
```

**Generate 50 test queries covering:**
1. Clear single-tool cases (20 queries)
2. Ambiguous cases that could match multiple tools (10 queries)
3. Cases that should NOT trigger tool use (10 queries)
4. Multi-tool cases requiring sequential calls (10 queries)

**Format:**
| Query | Expected Tool(s) | Reasoning | Difficulty |
|-------|------------------|-----------|------------|
...

Include diverse phrasings, edge cases, and potential confusion points.
```

### Benchmark Agent Performance

```
Design a benchmark suite for this agent system.

**Agent configuration:**
{agent_config}

**Benchmark dimensions:**
1. Task completion rate
2. Tool selection accuracy
3. Number of tool calls per task
4. Total latency
5. Error recovery rate

**Generate benchmark tasks:**
1. Simple tasks (1-2 tool calls)
2. Medium tasks (3-5 tool calls)
3. Complex tasks (6+ tool calls)
4. Error recovery tasks (require retries)
5. Edge case tasks (unusual inputs)

Provide the complete benchmark suite with expected baselines.
```

---

## Security Prompts

### Security Review Tool Definitions

```
Perform a security review of these tool definitions.

**Tools:**
```json
{tools}
```

**Review for:**
1. **Input validation gaps:** Parameters that could accept dangerous input
2. **Authorization issues:** Operations that should require auth
3. **Data exposure:** Parameters that could leak sensitive data
4. **Injection risks:** String parameters used in queries/commands
5. **Resource abuse:** Unbounded operations

**For each issue found, provide:**
1. Risk level (Critical/High/Medium/Low)
2. Specific vulnerability
3. Remediation steps
4. Improved tool definition

Generate a complete security report.
```

### Design Input Validation

```
Design input validation for this tool.

**Tool definition:**
```json
{tool_definition}
```

**Threats to consider:**
1. SQL injection
2. Command injection
3. Path traversal
4. SSRF (if URLs are accepted)
5. Oversized inputs
6. Unicode attacks

**Provide:**
1. Validation rules for each parameter
2. Sanitization functions
3. Error messages for validation failures
4. Implementation code

Generate complete validation implementation.
```

### Design Human-in-the-Loop Workflow

```
Design a human approval workflow for sensitive tools.

**Sensitive tools:**
```json
{tools}
```

**Sensitivity levels:**
- Low: Log only (data reads)
- Medium: Notify user (data writes)
- High: Require approval (payments, deletions)
- Critical: Multi-factor approval (security operations)

**Requirements:**
1. Define approval workflow for each level
2. Design approval UI/API
3. Handle approval timeouts
4. Implement audit logging

Provide complete workflow design with implementation guidance.
```

---

## Migration and Integration Prompts

### Migrate Tools Between Providers

```
Migrate these tools from {source_provider} to {target_provider}.

**Source tools ({source_provider} format):**
```json
{source_tools}
```

**Migration requirements:**
1. Convert tool definitions to target format
2. Handle format differences (parameters vs input_schema)
3. Adapt to provider-specific features
4. Update response handling code

**Provide:**
1. Converted tool definitions
2. Mapping of differences
3. Code changes needed
4. Testing checklist for migration
```

### Integrate Existing API as Tools

```
Convert this existing API into LLM tools.

**API specification:**
```yaml
{openapi_spec}
```

**Conversion requirements:**
1. Create tool for each endpoint
2. Simplify complex request bodies
3. Add user-friendly descriptions
4. Group related endpoints logically

**Constraints:**
- Max 15 tools total
- Avoid exposing internal implementation details
- Make parameters intuitive for natural language

Generate tool definitions and implementation wrappers.
```

---

## Quick Reference Prompts

### Tool Naming

```
Suggest a name for a tool that: {description}

Requirements:
- Snake_case format
- Action verb prefix (get_, create_, update_, delete_, search_, calculate_)
- Clear and descriptive
- Max 30 characters
```

### Tool Description

```
Write a tool description for: {tool_name}

Requirements:
- First sentence: what the tool does
- Second sentence: when to use it
- Under 200 characters total
- No jargon or technical terms
```

### Parameter Description

```
Write a parameter description for:
- Parameter: {param_name}
- Type: {type}
- Purpose: {purpose}

Requirements:
- Explain what the parameter is for
- Include an example value
- Under 100 characters
```

---

## Related Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts |
| [checklist.md](checklist.md) | Implementation checklists |
| [examples.md](examples.md) | Code examples |
| [templates.md](templates.md) | Reusable templates |
