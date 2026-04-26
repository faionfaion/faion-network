# Structured Output Basics - Checklist

## Output Format Options

- [ ] Evaluate JSON Mode (valid JSON, not schema-validated)
- [ ] Evaluate Structured Outputs (valid JSON + schema compliance)
- [ ] Evaluate Prompt Engineering (maximum flexibility)
- [ ] Evaluate Output Parsers (LangChain integration)
- [ ] Document trade-offs between reliability and flexibility
- [ ] Choose approach based on requirements

## JSON Mode Implementation (OpenAI)

- [ ] Set response_format to {"type": "json_object"}
- [ ] Include JSON structure in system prompt
- [ ] Test with json.loads() parsing
- [ ] Handle parsing errors gracefully
- [ ] Validate returned JSON structure
- [ ] Document JSON schema expectations
- [ ] Test edge cases for JSON compliance

## Structured Outputs (OpenAI)

- [ ] Install pydantic for model definition
- [ ] Create BaseModel classes with fields
- [ ] Add Field descriptions for each property
- [ ] Use type hints (str, int, float, bool, etc.)
- [ ] Define enums for restricted choices
- [ ] Use client.beta.chat.completions.parse()
- [ ] Access parsed response via message.parsed
- [ ] Guarantee both JSON validity and schema compliance

## Claude JSON Output

- [ ] Build schema as Python dict or JSON
- [ ] Create schema with type, properties, required fields
- [ ] Implement markdown code block extraction
- [ ] Parse extracted JSON with json.loads()
- [ ] Handle schema validation manually
- [ ] Test schema compliance verification
- [ ] Provide fallback for parsing failures

## Pydantic Models

- [ ] Define model with Field descriptions
- [ ] Use validators for custom validation
- [ ] Support nested models (composition)
- [ ] Define enums for categorical data
- [ ] Test model_json_schema() output
- [ ] Implement model serialization
- [ ] Handle optional fields with Optional[]

## Function-Based Structured Output

- [ ] Define function schema for tool calling
- [ ] Use function parameters as schema
- [ ] Parse tool_calls and function arguments
- [ ] Extract JSON from function arguments
- [ ] Validate against function schema
- [ ] Test parallel function calls
- [ ] Handle function execution errors

## Complex Schema Definition

- [ ] Design task extraction schema with subtasks
- [ ] Create nested models (Task with Subtasks)
- [ ] Support array of complex objects
- [ ] Define validators for validation rules
- [ ] Test schema with real data
- [ ] Document field constraints and rules
- [ ] Handle optional nested structures

## Form and Document Extraction

- [ ] Define schema for invoice extraction
- [ ] Handle address and contact information
- [ ] Extract line items with calculations
- [ ] Support optional fields (nullable)
- [ ] Validate extracted data completeness
- [ ] Test with real documents
- [ ] Handle OCR-generated content

## Validation & Error Handling

- [ ] Implement schema validation
- [ ] Handle validation errors gracefully
- [ ] Provide helpful error messages
- [ ] Retry with clarification if needed
- [ ] Log failed extractions
- [ ] Document edge cases
- [ ] Test with malformed inputs

## Testing & Quality Assurance

- [ ] Test schema compliance
- [ ] Test data type conversions
- [ ] Test nested structure parsing
- [ ] Test validation rules
- [ ] Benchmark reliability vs flexibility
- [ ] Compare different implementations
- [ ] Monitor extraction quality metrics
