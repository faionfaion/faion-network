# LLM Prompts for OpenAI API Integration

Prompts for using LLMs to assist with OpenAI API implementation, debugging, and optimization.

## Table of Contents

1. [Code Generation](#code-generation)
2. [Debugging and Troubleshooting](#debugging-and-troubleshooting)
3. [Optimization](#optimization)
4. [Schema Design](#schema-design)
5. [Prompt Engineering](#prompt-engineering)
6. [Migration and Updates](#migration-and-updates)
7. [Security Review](#security-review)

---

## Code Generation

### Generate Chat Completion Code

```
Generate Python code for OpenAI chat completion with these requirements:

Task: {TASK_DESCRIPTION}
Model: {MODEL_NAME}
Features needed:
- {FEATURE_1}
- {FEATURE_2}
- {FEATURE_3}

Output format: {OUTPUT_FORMAT}
Error handling: {ERROR_HANDLING_REQUIREMENTS}

Generate production-ready code with:
1. Proper error handling with retry logic
2. Type hints
3. Docstrings
4. Usage tracking
5. Example usage

Use OpenAI Python SDK v1.x syntax.
```

### Generate Streaming Implementation

```
Generate streaming implementation for OpenAI API.

Use case: {USE_CASE}
Framework: {FRAMEWORK} (e.g., FastAPI, Flask, vanilla Python)
Requirements:
- {REQUIREMENT_1}
- {REQUIREMENT_2}

Include:
1. Server-side streaming code
2. Client-side consumption example
3. Error handling during stream
4. Connection recovery
5. Progress indication

Ensure the code handles:
- Partial chunk accumulation
- Network interruptions
- Proper cleanup on completion/error
```

### Generate Structured Output Schema

```
Create a Pydantic schema for structured output from OpenAI API.

Data to extract/generate: {DATA_DESCRIPTION}

Fields needed:
1. {FIELD_1}: {DESCRIPTION_1}
2. {FIELD_2}: {DESCRIPTION_2}
3. {FIELD_3}: {DESCRIPTION_3}

Constraints:
- {CONSTRAINT_1}
- {CONSTRAINT_2}

Generate:
1. Pydantic BaseModel with proper field types
2. Field descriptions for LLM guidance
3. Validators where needed
4. Example of using with client.beta.chat.completions.parse()
5. Refusal handling
```

### Generate Tool Definition

```
Create OpenAI tool definition for the following function.

Function purpose: {FUNCTION_PURPOSE}
Parameters:
- {PARAM_1}: {TYPE_1} - {DESCRIPTION_1} (required/optional)
- {PARAM_2}: {TYPE_2} - {DESCRIPTION_2} (required/optional)
- {PARAM_3}: {TYPE_3} - {DESCRIPTION_3} (required/optional)

Return type: {RETURN_TYPE}

Generate:
1. Tool definition JSON schema
2. Python function signature with type hints
3. Complete tool use loop implementation
4. Example usage
5. Error handling for tool execution
```

---

## Debugging and Troubleshooting

### Debug API Error

```
Help debug this OpenAI API error.

Error message:
<error>
{ERROR_MESSAGE}
</error>

Code that caused the error:
<code>
{CODE}
</code>

Request parameters:
{REQUEST_PARAMS}

Analyze:
1. What is the root cause of this error?
2. What are the possible fixes?
3. How to prevent this error in the future?

Provide:
- Explanation of the error
- Fixed code
- Recommendations for error handling
```

### Debug Unexpected Output

```
The OpenAI API is returning unexpected output. Help diagnose the issue.

Prompt/messages sent:
<messages>
{MESSAGES}
</messages>

Model: {MODEL}
Parameters: {PARAMETERS}

Expected output:
<expected>
{EXPECTED}
</expected>

Actual output:
<actual>
{ACTUAL}
</actual>

Analyze:
1. Why might the model produce this output?
2. What in the prompt could be causing this?
3. What parameters might affect the output?

Provide:
- Root cause analysis
- Modified prompt/messages
- Parameter adjustments
- Test cases to verify fix
```

### Debug Streaming Issues

```
Debug streaming issues with OpenAI API.

Issue description: {ISSUE_DESCRIPTION}

Code:
<code>
{STREAMING_CODE}
</code>

Symptoms:
- {SYMPTOM_1}
- {SYMPTOM_2}

Environment:
- Python version: {PYTHON_VERSION}
- OpenAI SDK version: {SDK_VERSION}
- Framework: {FRAMEWORK}

Diagnose:
1. Common streaming issues to check
2. Specific issue in this code
3. Framework-specific considerations

Provide:
- Issue diagnosis
- Fixed code
- Testing approach
```

### Debug Tool Use Loop

```
Debug issues with OpenAI function calling / tool use.

Issue: {ISSUE_DESCRIPTION}

Tool definitions:
<tools>
{TOOL_DEFINITIONS}
</tools>

Code:
<code>
{TOOL_LOOP_CODE}
</code>

Problem behavior:
{PROBLEM_BEHAVIOR}

Analyze:
1. Is the tool definition correct?
2. Is the tool use loop implemented correctly?
3. Are tool results being passed back properly?
4. Is there an infinite loop risk?

Provide:
- Issue diagnosis
- Fixed code
- Best practices for this scenario
```

---

## Optimization

### Optimize for Latency

```
Optimize this OpenAI API integration for lower latency.

Current code:
<code>
{CODE}
</code>

Current latency: {CURRENT_LATENCY}
Target latency: {TARGET_LATENCY}
Use case: {USE_CASE}

Constraints:
- {CONSTRAINT_1}
- {CONSTRAINT_2}

Suggest optimizations for:
1. Model selection
2. Streaming vs non-streaming
3. Prompt length
4. max_tokens setting
5. Concurrency
6. Caching opportunities

Provide:
- Optimized code
- Expected improvement
- Trade-offs
```

### Optimize for Cost

```
Optimize this OpenAI API usage for lower cost.

Current implementation:
<code>
{CODE}
</code>

Current monthly cost: {CURRENT_COST}
Target cost: {TARGET_COST}

Usage pattern:
- Requests per day: {REQUESTS}
- Average prompt tokens: {PROMPT_TOKENS}
- Average completion tokens: {COMPLETION_TOKENS}
- Model: {MODEL}

Suggest optimizations for:
1. Model tiering (when to use mini vs full)
2. Prompt optimization
3. Caching identical requests
4. Batch API usage
5. Token reduction techniques

Provide:
- Cost analysis by optimization
- Implementation changes
- Quality trade-offs
```

### Optimize Prompt for Reliability

```
Optimize this prompt for more reliable outputs.

Current prompt:
<prompt>
{PROMPT}
</prompt>

Issues observed:
- {ISSUE_1}
- {ISSUE_2}

Output requirements:
{OUTPUT_REQUIREMENTS}

Improve:
1. Clarity of instructions
2. Output format specification
3. Edge case handling
4. Consistency across runs

Provide:
- Optimized prompt
- Explanation of changes
- Test cases
```

### Optimize Token Usage

```
Optimize token usage for this OpenAI API call.

Current messages:
<messages>
{MESSAGES}
</messages>

Token count: {TOKEN_COUNT}
Target reduction: {TARGET_REDUCTION}%

The response must still contain: {REQUIRED_INFORMATION}

Optimize:
1. System prompt length
2. Context relevance
3. Few-shot examples
4. Message history trimming

Provide:
- Optimized messages
- Token count comparison
- Quality impact assessment
```

---

## Schema Design

### Design Extraction Schema

```
Design a Pydantic schema for extracting data from {DOCUMENT_TYPE}.

Sample document:
<document>
{SAMPLE_DOCUMENT}
</document>

Data to extract:
1. {DATA_1}
2. {DATA_2}
3. {DATA_3}

Considerations:
- Missing data handling
- Data validation
- Nested structures
- Lists vs single values

Provide:
1. Pydantic models with Field descriptions
2. JSON Schema for reference
3. Example prompt for extraction
4. Handling for edge cases
```

### Design Classification Schema

```
Design a schema for classification task.

Classification task: {TASK_DESCRIPTION}

Categories:
1. {CATEGORY_1}: {DESCRIPTION_1}
2. {CATEGORY_2}: {DESCRIPTION_2}
3. {CATEGORY_3}: {DESCRIPTION_3}

Additional outputs needed:
- Confidence score
- Reasoning
- Alternative categories

Provide:
1. Pydantic model with Literal types for categories
2. Prompt template for classification
3. Handling for ambiguous cases
4. Multi-label support if needed
```

### Design Agent Response Schema

```
Design a schema for an AI agent's responses.

Agent capabilities:
1. {CAPABILITY_1}
2. {CAPABILITY_2}
3. {CAPABILITY_3}

Response must include:
- Action type
- Parameters for action
- Reasoning
- Confidence
- Fallback suggestions

Constraints:
- {CONSTRAINT_1}
- {CONSTRAINT_2}

Provide:
1. Response schema with union types for different actions
2. Validation for action-specific parameters
3. Example responses
4. Error response schema
```

---

## Prompt Engineering

### Create System Prompt

```
Create a system prompt for {USE_CASE}.

Requirements:
- Persona: {PERSONA}
- Tone: {TONE}
- Capabilities: {CAPABILITIES}
- Constraints: {CONSTRAINTS}
- Output format: {OUTPUT_FORMAT}

Include:
1. Clear role definition
2. Behavioral guidelines
3. Output specifications
4. Safety guardrails
5. Error handling instructions

Generate a complete system prompt following OpenAI best practices.
```

### Improve Existing Prompt

```
Improve this prompt for better results with OpenAI API.

Current prompt:
<prompt>
{PROMPT}
</prompt>

Issues:
- {ISSUE_1}
- {ISSUE_2}

Goals:
- {GOAL_1}
- {GOAL_2}

Analyze and improve:
1. Clarity and specificity
2. Structure and formatting
3. Example inclusion
4. Edge case handling
5. Output format specification

Provide:
- Improved prompt
- Explanation of changes
- Before/after comparison
```

### Create Few-Shot Examples

```
Create few-shot examples for this task.

Task: {TASK_DESCRIPTION}

Input format: {INPUT_FORMAT}
Output format: {OUTPUT_FORMAT}

Generate 3-5 diverse examples covering:
1. Typical case
2. Edge case
3. Challenging case
4. Error/invalid input case

Format each example as:
<example>
Input: [example input]
Output: [example output]
Note: [why this example is useful]
</example>

Ensure examples are realistic and representative.
```

### Create Chain-of-Thought Prompt

```
Convert this task to a chain-of-thought prompt.

Task: {TASK_DESCRIPTION}

Current direct prompt:
<prompt>
{CURRENT_PROMPT}
</prompt>

The task requires reasoning because: {REASONING_NEEDS}

Create:
1. CoT prompt with thinking/answer structure
2. Example reasoning path
3. Verification step
4. Output extraction method

Consider:
- Step clarity
- Intermediate validation
- Final answer format
```

---

## Migration and Updates

### Migrate to Responses API

```
Help migrate this code from Chat Completions API to Responses API.

Current code:
<code>
{CURRENT_CODE}
</code>

Features used:
- {FEATURE_1}
- {FEATURE_2}

Provide:
1. Equivalent Responses API code
2. Differences in behavior
3. New features to consider
4. Deprecation timeline notes
5. Testing approach
```

### Update SDK Version

```
Help update this code to latest OpenAI Python SDK (v1.x).

Current code (old SDK):
<code>
{OLD_CODE}
</code>

Changes needed:
1. Client initialization
2. Method names and signatures
3. Response object structure
4. Error handling classes
5. Async patterns

Provide:
- Updated code
- Breaking changes summary
- New features available
- Deprecation warnings to address
```

### Migrate Prompt to New Model

```
Help migrate this prompt from {OLD_MODEL} to {NEW_MODEL}.

Current prompt:
<prompt>
{PROMPT}
</prompt>

Known differences between models:
{KNOWN_DIFFERENCES}

Analyze:
1. Compatibility issues
2. Feature differences
3. Prompt adjustments needed
4. Expected output changes

Provide:
- Adjusted prompt for new model
- Testing recommendations
- Fallback strategy
```

---

## Security Review

### Review for Prompt Injection

```
Review this OpenAI API implementation for prompt injection vulnerabilities.

Code:
<code>
{CODE}
</code>

User input handling:
{USER_INPUT_FLOW}

Check for:
1. Direct user input in prompts
2. Missing input sanitization
3. System prompt exposure risks
4. Instruction override attempts
5. Data exfiltration vectors

Provide:
- Vulnerabilities found
- Risk assessment (high/medium/low)
- Recommended fixes
- Secure code example
```

### Review for Data Leakage

```
Review this implementation for potential data leakage.

Code:
<code>
{CODE}
</code>

Sensitive data involved:
- {DATA_TYPE_1}
- {DATA_TYPE_2}

Check for:
1. PII in prompts
2. Credentials in context
3. Logging sensitive data
4. API response exposure
5. Error message leakage

Provide:
- Leakage risks found
- Severity assessment
- Mitigation recommendations
- Secure patterns to follow
```

### Review Rate Limiting and Abuse Prevention

```
Review this implementation for rate limiting and abuse prevention.

Code:
<code>
{CODE}
</code>

Exposure:
- Public API: {YES/NO}
- User authentication: {AUTH_METHOD}
- Usage tracking: {YES/NO}

Check for:
1. Request rate limiting
2. Token usage limits per user
3. Cost runaway prevention
4. Abuse pattern detection
5. User identification for tracking

Provide:
- Gaps identified
- Risk assessment
- Implementation recommendations
- Monitoring suggestions
```

---

## Quick Reference

### Prompt Selection Guide

| Task | Recommended Prompt |
|------|-------------------|
| Generate new API code | Generate Chat Completion Code |
| API errors | Debug API Error |
| Wrong outputs | Debug Unexpected Output |
| Slow responses | Optimize for Latency |
| High costs | Optimize for Cost |
| Design JSON output | Design Extraction Schema |
| Write system prompt | Create System Prompt |
| Improve prompt | Improve Existing Prompt |
| SDK upgrade | Update SDK Version |
| Security check | Review for Prompt Injection |

### Tips for Best Results

1. **Be specific** - Include actual code, errors, and requirements
2. **Provide context** - Use case, constraints, environment details
3. **Show examples** - Sample inputs/outputs when relevant
4. **State constraints** - Model, cost limits, latency requirements
5. **Request format** - Specify how you want the response structured
