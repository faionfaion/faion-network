# LLM Prompts for Structured Output

Prompts for schema design, debugging, optimization, and validation assistance.

## Schema Design Prompts

### Generate Pydantic Model from Description

```
You are an expert Python developer specializing in Pydantic models for LLM structured output.

Given the following requirements, create a Pydantic model that:
1. Uses appropriate field types (str, int, float, bool, List, Optional, Enum)
2. Includes Field() with descriptions for all fields
3. Uses Enum for fields with fixed options
4. Sets sensible defaults for optional fields
5. Adds validators where appropriate
6. Is compatible with OpenAI's structured output feature

Requirements:
{requirements}

Provide the complete Python code including all imports. Include example usage showing how to use the model with OpenAI's API.
```

### Generate JSON Schema from Description

```
Create a JSON Schema for structured output based on these requirements:

Requirements:
{requirements}

The schema must:
1. Follow JSON Schema draft 2020-12
2. Include descriptions for all properties
3. Specify required fields appropriately
4. Use enums for categorical fields
5. Include appropriate constraints (minimum, maximum, pattern, etc.)
6. Be compatible with LLM structured output APIs

Return only the JSON Schema, properly formatted.
```

### Convert Existing Data to Schema

```
Analyze the following example data and generate a Pydantic model that would validate it:

Example Data:
```json
{data}
```

Requirements:
1. Infer the most appropriate types for each field
2. Determine which fields should be required vs optional
3. Identify fields that could be enums (limited values)
4. Add appropriate validation constraints
5. Create nested models for complex objects
6. Add docstrings and field descriptions

Provide the complete Pydantic model code with all imports.
```

### Design Schema for Specific Use Case

```
Design a Pydantic schema for the following use case:

Use Case: {use_case}

Input Type: {input_type} (e.g., text, document, form, conversation)

Consider:
1. What data must always be extracted (required fields)?
2. What data might sometimes be present (optional fields)?
3. What values should be from a fixed set (enums)?
4. What validation rules apply?
5. What nested structures are needed?
6. How will the output be used downstream?

Provide:
1. The Pydantic model with full annotations
2. An explanation of design decisions
3. Example input and expected output
4. Potential edge cases to handle
```

## Debugging Prompts

### Diagnose Extraction Failures

```
Analyze this structured output failure and suggest fixes:

Schema (Pydantic model):
```python
{schema}
```

Input Text:
{input_text}

LLM Response:
{llm_response}

Error:
{error_message}

Diagnose:
1. What caused the extraction to fail?
2. Is the schema too complex or restrictive?
3. Is the input text sufficient for extraction?
4. Did the LLM misunderstand the task?

Provide:
1. Root cause analysis
2. Specific fixes for the schema
3. Improved prompt if needed
4. Alternative approaches to try
```

### Fix Validation Errors

```
Fix this Pydantic validation error:

Model:
```python
{model}
```

Data that failed:
```json
{data}
```

Validation Error:
{error}

Provide:
1. Explanation of why validation failed
2. Two solutions:
   a. Fix the data to match the model
   b. Fix the model to accept this data type
3. Recommendation on which approach is better
4. Updated code for the recommended solution
```

### Improve Extraction Accuracy

```
The following extraction is producing inconsistent or inaccurate results:

Schema:
```python
{schema}
```

System Prompt:
{system_prompt}

Sample Input 1:
{input_1}

Expected Output 1:
{expected_1}

Actual Output 1:
{actual_1}

[Additional samples if available]

Analyze and improve:
1. What patterns of errors are occurring?
2. Is the schema design causing issues?
3. Is the prompt unclear or ambiguous?
4. Are there edge cases not being handled?

Provide:
1. Root cause analysis
2. Improved schema (if needed)
3. Improved prompt
4. Additional validation to add
5. Test cases to verify the fix
```

### Debug JSON Parse Errors

```
The LLM output cannot be parsed as JSON:

Prompt Used:
{prompt}

Raw LLM Response:
{response}

Parse Error:
{error}

Diagnose and fix:
1. What is wrong with the output format?
2. Why did the model produce non-JSON text?
3. How can this be prevented?

Provide:
1. Explanation of the issue
2. Cleaned/fixed JSON if recoverable
3. Improved prompt to prevent this
4. Code to handle this edge case gracefully
```

## Optimization Prompts

### Optimize Schema for Tokens

```
Optimize this Pydantic schema to reduce token usage while maintaining data quality:

Current Schema:
```python
{schema}
```

Current average output tokens: {token_count}
Target reduction: {target_percentage}%

Optimization strategies to consider:
1. Shorter field names (with descriptions preserved)
2. Removing unnecessary fields
3. Using enums instead of free text
4. Flattening nested structures
5. Combining related fields
6. Using more efficient types

Provide:
1. Optimized schema
2. Mapping from old to new field names
3. Estimated token reduction
4. Any trade-offs or data loss
```

### Optimize for Latency

```
Optimize this extraction pipeline for lower latency:

Current Implementation:
```python
{implementation}
```

Current average latency: {latency}ms
Target latency: {target}ms

Consider:
1. Can the schema be simplified?
2. Can any fields be extracted in parallel?
3. Is the prompt efficiently written?
4. Can responses be streamed?
5. Is caching applicable?
6. Would a smaller/faster model work?

Provide:
1. Optimized implementation
2. Explanation of changes
3. Expected latency improvement
4. Any accuracy trade-offs
```

### Improve Schema Reliability

```
Improve the reliability of this schema (reduce failed extractions):

Current Schema:
```python
{schema}
```

Current success rate: {success_rate}%
Target success rate: {target}%

Common failure patterns:
{failure_patterns}

Improve by:
1. Making strict fields more lenient
2. Adding better defaults
3. Using coercion instead of strict validation
4. Improving field descriptions
5. Adding fallback values
6. Improving prompt instructions

Provide:
1. More robust schema
2. Updated prompt if needed
3. Fallback handling code
4. Expected improvement in success rate
```

### Compare Schema Approaches

```
Compare these two schema designs for the same extraction task:

Approach A:
```python
{schema_a}
```

Approach B:
```python
{schema_b}
```

Use Case: {use_case}

Compare on:
1. Extraction accuracy
2. Token efficiency
3. Schema maintainability
4. Validation strictness
5. Downstream usability
6. Error handling

Provide:
1. Comparison table
2. Recommendation with rationale
3. Hybrid approach if beneficial
4. Test cases to validate
```

## Prompt Engineering for Extraction

### Create System Prompt

```
Create an optimized system prompt for structured extraction:

Task: {task_description}

Schema:
```python
{schema}
```

The prompt should:
1. Clearly explain the extraction task
2. Provide guidance for ambiguous cases
3. Specify how to handle missing data
4. Set appropriate defaults
5. Be concise to minimize tokens
6. Improve extraction accuracy

Provide:
1. Complete system prompt
2. Example user message format
3. Expected output format
4. Edge cases handled by the prompt
```

### Create Few-Shot Examples

```
Create few-shot examples to improve extraction accuracy:

Task: {task}

Schema:
```python
{schema}
```

Current system prompt:
{system_prompt}

Provide 3-5 few-shot examples that:
1. Cover common cases
2. Handle edge cases
3. Demonstrate proper field population
4. Show handling of missing data
5. Are concise to minimize tokens

Format examples as:
- User: [input text]
- Assistant: [JSON output]

Include brief explanation of why each example is included.
```

### Design Retry Prompt

```
Create a retry prompt for when extraction fails validation:

Original prompt:
{original_prompt}

Schema:
```python
{schema}
```

Common validation errors:
{errors}

The retry prompt should:
1. Reference the original task
2. Explain what was wrong
3. Provide specific guidance to fix
4. Not repeat the full schema
5. Be concise

Provide:
1. Retry prompt template (with placeholders for error details)
2. Logic for constructing the retry message
3. Maximum retries recommendation
4. When to give up and return partial results
```

### Multi-Step Extraction Prompt

```
Design prompts for multi-step extraction:

Task: {complex_task}

The task is too complex for single-pass extraction. Break it into steps:

1. Identify logical extraction phases
2. Design schema for each phase
3. Create prompt for each phase
4. Define how phases connect

Provide:
1. Phase breakdown with rationale
2. Schema for each phase
3. Prompt for each phase
4. Code to orchestrate multi-step extraction
5. How to handle phase failures
```

## Validation and Testing Prompts

### Generate Test Cases

```
Generate comprehensive test cases for this extraction schema:

Schema:
```python
{schema}
```

Use case: {use_case}

Generate test cases covering:
1. Happy path (normal expected inputs)
2. Edge cases (minimal valid inputs)
3. Error cases (should fail validation)
4. Boundary values (limits of constraints)
5. Missing optional fields
6. Malformed inputs

For each test case provide:
- Test name
- Input text
- Expected output (or expected error)
- What this tests

Aim for 80%+ code coverage of validators.
```

### Validate Schema Design

```
Review this schema design for potential issues:

Schema:
```python
{schema}
```

Intended use: {use_case}

Check for:
1. Overly strict constraints
2. Missing field descriptions
3. Inadequate type safety
4. Missing validators
5. Inefficient structure
6. Unclear field purposes
7. Missing required fields
8. Unnecessary optional fields
9. Enum completeness
10. Nested model issues

Provide:
1. Issues found (severity: high/medium/low)
2. Specific recommendations for each
3. Improved schema if significant changes needed
4. Best practices being violated
```

### Create Validation Rules

```
Create comprehensive validation rules for this extraction task:

Schema:
```python
{schema}
```

Domain: {domain}

For each field, define:
1. Type validation (built-in Pydantic)
2. Format validation (regex patterns)
3. Business logic validation (custom validators)
4. Cross-field validation (model validators)
5. Semantic validation (makes sense in context)

Provide:
1. Complete schema with all validators
2. Helper functions for complex validation
3. Error messages for each validation rule
4. Validation priority order
```

## Schema Evolution Prompts

### Migrate Schema Version

```
Help migrate from schema v1 to v2:

Schema v1:
```python
{schema_v1}
```

Schema v2:
```python
{schema_v2}
```

Provide:
1. Field mapping (old to new)
2. Migration function to convert v1 data to v2
3. Backward compatibility function (v2 to v1 if needed)
4. Handling of new required fields
5. Deprecation warnings for removed fields
6. Test cases for migration
```

### Extend Schema Safely

```
Extend this schema with new requirements while maintaining backward compatibility:

Current Schema:
```python
{current_schema}
```

New Requirements:
{new_requirements}

Constraints:
- Existing clients must continue working
- New fields should be optional with defaults
- No breaking changes to field types

Provide:
1. Extended schema
2. Migration notes for existing data
3. Version indicator approach
4. Documentation of changes
```

### Merge Multiple Schemas

```
Merge these schemas into a unified model:

Schema A (from system 1):
```python
{schema_a}
```

Schema B (from system 2):
```python
{schema_b}
```

Requirements:
- Preserve all data from both schemas
- Resolve naming conflicts sensibly
- Create unified field types where possible
- Document source of each field

Provide:
1. Unified schema
2. Mapping from each source schema
3. Conversion functions
4. Handling of conflicting fields
5. Test cases for conversion
```

## Code Generation Prompts

### Generate Extraction Pipeline

```
Generate a complete extraction pipeline:

Requirements:
{requirements}

Provider: {provider} (OpenAI/Anthropic/Google/Local)

Include:
1. Pydantic models with full validation
2. Extraction function with error handling
3. Retry logic with exponential backoff
4. Response caching
5. Logging and monitoring hooks
6. Type hints throughout
7. Unit tests
8. Usage examples

The code should be production-ready with:
- Proper error handling
- Configurable parameters
- Documentation
- Type safety
```

### Generate API Endpoint

```
Generate a FastAPI endpoint for structured extraction:

Schema:
```python
{schema}
```

Requirements:
- POST endpoint accepting text input
- Return structured extraction result
- Include proper error responses
- Add request validation
- Include OpenAPI documentation
- Rate limiting consideration
- Async implementation

Provide:
1. Complete FastAPI router code
2. Request/Response models
3. Error handling
4. Tests for the endpoint
5. Example requests/responses
```

### Generate Batch Processor

```
Generate a batch processing system for structured extraction:

Schema:
```python
{schema}
```

Requirements:
- Process multiple documents efficiently
- Respect rate limits
- Handle individual failures gracefully
- Report progress
- Support resumption after failure
- Configurable concurrency

Provide:
1. Batch processor class
2. Progress tracking
3. Error aggregation
4. Retry logic
5. Result storage
6. CLI interface option
```

## Troubleshooting Reference Prompts

### Common Issues Checklist

```
I'm having issues with structured output extraction. Help me diagnose:

Issue: {issue_description}

Provider: {provider}
Model: {model}

Schema:
```python
{schema}
```

Prompt:
{prompt}

Error/Symptom:
{error}

Walk through this checklist:
1. Is JSON mode properly enabled?
2. Is the schema valid JSON Schema?
3. Are required fields achievable from input?
4. Is the prompt clear about output format?
5. Are field descriptions helpful?
6. Is temperature set appropriately?
7. Is max_tokens sufficient?
8. Are there constraint conflicts?
9. Is the model capable of this task?
10. Is input text suitable for extraction?

For each applicable issue, provide:
- Specific diagnosis
- Code fix
- Verification test
```

### Provider-Specific Debugging

```
Debug this {provider}-specific extraction issue:

Code:
```python
{code}
```

Error:
{error}

Check {provider}-specific issues:
- API version compatibility
- SDK version compatibility
- Feature availability
- Parameter names/formats
- Response structure
- Error handling patterns

Provide:
1. Root cause
2. Fixed code
3. Provider-specific best practices
4. Alternative approaches
```
