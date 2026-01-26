# Structured Output Checklists

Comprehensive checklists for designing, implementing, and validating structured output schemas.

## Schema Design Checklist

### Requirements Analysis

- [ ] **Identify output consumers**: Who/what will use this data?
- [ ] **Define required fields**: What data MUST be present?
- [ ] **Define optional fields**: What data MAY be present?
- [ ] **Determine field types**: String, number, boolean, array, object?
- [ ] **Establish value constraints**: Min/max, patterns, enums?
- [ ] **Plan nested structures**: What objects contain other objects?
- [ ] **Consider edge cases**: Empty values, missing data, errors?
- [ ] **Version strategy**: How will schema evolve?

### Field Design

- [ ] **Use descriptive names**: `customer_email` not `ce`
- [ ] **Add Field descriptions**: Helps LLM understand intent
- [ ] **Set appropriate types**: Use most specific type possible
- [ ] **Define enums for categories**: Avoid free-form where possible
- [ ] **Use Optional for nullable**: `Optional[str] = None`
- [ ] **Set sensible defaults**: Reduce required LLM output
- [ ] **Add validation rules**: `ge`, `le`, `pattern`, `min_length`
- [ ] **Document examples**: Show expected values in descriptions

### Structure Design

- [ ] **Prefer flat structures**: Nesting adds complexity
- [ ] **Group related fields**: Use nested models logically
- [ ] **Limit nesting depth**: Max 3-4 levels recommended
- [ ] **Use lists appropriately**: For variable-length collections
- [ ] **Consider field order**: Place important fields first
- [ ] **Avoid circular references**: They break JSON Schema
- [ ] **Keep schemas focused**: One schema per task type

### Type Selection Guide

| Data Type | Python Type | When to Use |
|-----------|-------------|-------------|
| Text | `str` | Names, descriptions, free text |
| Integer | `int` | Counts, IDs, whole numbers |
| Decimal | `float` | Prices, scores, percentages |
| Boolean | `bool` | Yes/no, true/false flags |
| Date/Time | `str` | ISO format strings |
| Enum | `Enum` | Fixed set of options |
| List | `List[T]` | Multiple items of same type |
| Object | `BaseModel` | Grouped related fields |
| Union | `Union[A, B]` | Multiple possible types |
| Optional | `Optional[T]` | May be null/missing |

## Implementation Checklist

### Environment Setup

- [ ] **Install dependencies**:
  ```bash
  pip install pydantic openai anthropic google-generativeai
  ```
- [ ] **Configure API keys**: Set environment variables
- [ ] **Choose provider**: Match provider to requirements
- [ ] **Select model**: Consider capabilities and cost
- [ ] **Set up logging**: Track requests and responses

### Pydantic Model Creation

- [ ] **Import required modules**:
  ```python
  from pydantic import BaseModel, Field
  from typing import List, Optional
  from enum import Enum
  ```
- [ ] **Define enums first**: For type references
- [ ] **Define nested models**: Before parent models
- [ ] **Add field metadata**: Descriptions, constraints
- [ ] **Set class docstring**: Describes model purpose
- [ ] **Add model_config**: For JSON Schema customization
- [ ] **Test model locally**: Validate with sample data

### Provider Integration

#### OpenAI

- [ ] **Use correct method**: `beta.chat.completions.parse()`
- [ ] **Pass model to response_format**: Not JSON Schema directly
- [ ] **Handle refusals**: Check `message.refusal`
- [ ] **Access parsed result**: `message.parsed`
- [ ] **Set appropriate max_tokens**: Schema affects output length

#### Claude (Anthropic)

- [ ] **Use tool use pattern**: For structured output
- [ ] **Define tool schema**: From Pydantic model
- [ ] **Force tool use**: Set `tool_choice`
- [ ] **Parse tool response**: Extract from `tool_use` block
- [ ] **Handle no-tool cases**: When model doesn't use tool

#### Gemini

- [ ] **Set response_mime_type**: `"application/json"`
- [ ] **Provide response_schema**: JSON Schema dict
- [ ] **Configure generation_config**: All settings together
- [ ] **Parse JSON response**: `json.loads(response.text)`

#### Local Models (Outlines)

- [ ] **Install outlines**: `pip install outlines`
- [ ] **Load model**: `outlines.models.transformers()`
- [ ] **Create generator**: `outlines.generate.json()`
- [ ] **Generate output**: Pass prompt to generator

### Error Handling

- [ ] **Wrap in try/except**: Catch all failure modes
- [ ] **Handle JSON parse errors**: `json.JSONDecodeError`
- [ ] **Handle validation errors**: `pydantic.ValidationError`
- [ ] **Handle API errors**: Rate limits, timeouts
- [ ] **Implement retries**: With exponential backoff
- [ ] **Log failures**: For debugging and monitoring
- [ ] **Return meaningful errors**: To calling code

### Testing

- [ ] **Unit test models**: Validate with sample data
- [ ] **Test happy path**: Normal expected inputs
- [ ] **Test edge cases**: Empty, null, extreme values
- [ ] **Test error handling**: Invalid inputs
- [ ] **Integration test**: With actual LLM calls
- [ ] **Load test**: Under production conditions
- [ ] **Monitor in production**: Track success rates

## Validation Checklist

### Schema Validation

- [ ] **Required fields present**: All required fields have values
- [ ] **Types correct**: Values match expected types
- [ ] **Constraints satisfied**: Min/max, patterns, enums
- [ ] **Nested objects valid**: Recursively validate
- [ ] **Arrays not empty**: If minimum length required
- [ ] **No extra fields**: Unless explicitly allowed

### Business Logic Validation

- [ ] **Cross-field consistency**: Related fields agree
- [ ] **Date ranges valid**: Start before end
- [ ] **Totals correct**: Sums match line items
- [ ] **References exist**: Foreign keys are valid
- [ ] **State transitions valid**: Status changes make sense
- [ ] **Format correct**: Phone numbers, emails, URLs

### Data Quality Validation

- [ ] **No placeholder values**: "N/A", "Unknown", etc.
- [ ] **Confidence reasonable**: Not always 1.0
- [ ] **Completeness acceptable**: Enough fields extracted
- [ ] **Consistency check**: Similar inputs similar outputs
- [ ] **No hallucinations**: Values exist in source text
- [ ] **Language correct**: Expected language in text fields

## Pre-Production Checklist

### Code Quality

- [ ] **Type hints complete**: All functions typed
- [ ] **Docstrings present**: All public functions documented
- [ ] **Error messages clear**: Help debugging
- [ ] **Logging appropriate**: Not too verbose, not too sparse
- [ ] **Secrets secured**: No hardcoded API keys
- [ ] **Dependencies pinned**: Lock file up to date

### Performance

- [ ] **Timeouts configured**: Prevent hanging requests
- [ ] **Rate limiting implemented**: Respect provider limits
- [ ] **Caching considered**: For repeated extractions
- [ ] **Batch processing**: Where applicable
- [ ] **Async where beneficial**: For concurrent requests
- [ ] **Memory efficient**: Handle large documents

### Monitoring

- [ ] **Success rate tracked**: Percentage of valid outputs
- [ ] **Latency tracked**: P50, P95, P99
- [ ] **Costs tracked**: Tokens and API calls
- [ ] **Errors alerted**: On failure spikes
- [ ] **Schema violations logged**: For refinement
- [ ] **Model comparison**: If using multiple providers

### Documentation

- [ ] **Schema documented**: All fields explained
- [ ] **Examples provided**: Sample inputs and outputs
- [ ] **Error codes documented**: What each error means
- [ ] **Integration guide**: How to use the API
- [ ] **Changelog maintained**: Track schema changes
- [ ] **Runbook created**: For operational issues

## Migration Checklist

### Schema Migration

When changing schemas in production:

- [ ] **Assess impact**: What downstream systems affected?
- [ ] **Plan versioning**: How to handle both versions?
- [ ] **Add new fields as optional**: Don't break existing
- [ ] **Deprecate old fields**: Mark, don't remove
- [ ] **Test migration**: With production-like data
- [ ] **Communicate changes**: To all consumers
- [ ] **Monitor rollout**: Watch for increased errors
- [ ] **Rollback plan**: If issues arise

### Provider Migration

When switching LLM providers:

- [ ] **Compare capabilities**: Schema support differences
- [ ] **Test with same prompts**: Compare output quality
- [ ] **Adjust prompts if needed**: Provider-specific tuning
- [ ] **Update error handling**: Different error formats
- [ ] **Validate output parity**: Same schema, same results
- [ ] **Cost analysis**: Compare token costs
- [ ] **Gradual rollout**: A/B test before full switch

## Troubleshooting Checklist

### Invalid JSON Output

- [ ] Check: Is JSON mode enabled?
- [ ] Check: Is prompt asking for JSON?
- [ ] Check: Is model capable of JSON mode?
- [ ] Try: Increase max_tokens
- [ ] Try: Simplify schema
- [ ] Try: Add "return only JSON" to prompt

### Missing Required Fields

- [ ] Check: Is field in schema with description?
- [ ] Check: Is source data sufficient?
- [ ] Try: Add field description with examples
- [ ] Try: Make field optional with default
- [ ] Try: Reduce total number of fields

### Wrong Field Types

- [ ] Check: Is type constraint clear?
- [ ] Check: Are examples showing correct type?
- [ ] Try: Add type hint in description
- [ ] Try: Use enum instead of string
- [ ] Try: Add format hint (e.g., "ISO date")

### Validation Errors

- [ ] Check: Are constraints too strict?
- [ ] Check: Is input data clean enough?
- [ ] Try: Relax validation rules
- [ ] Try: Add preprocessing step
- [ ] Try: Use coercion instead of strict

### Inconsistent Results

- [ ] Check: Is temperature too high?
- [ ] Check: Is prompt deterministic?
- [ ] Try: Set temperature to 0
- [ ] Try: Add examples to prompt
- [ ] Try: Use more constrained schema

## Quality Gates

### Before Schema Approval

| Gate | Criteria |
|------|----------|
| Completeness | All required data captured |
| Simplicity | No unnecessary complexity |
| Clarity | Field names self-explanatory |
| Constraints | Appropriate validation rules |
| Documentation | All fields documented |
| Testing | Unit tests pass |

### Before Production Deploy

| Gate | Criteria |
|------|----------|
| Accuracy | >95% correct extractions on test set |
| Reliability | <1% JSON parse failures |
| Performance | P95 latency < SLA |
| Cost | Within budget projections |
| Monitoring | Alerts configured |
| Rollback | Plan documented and tested |

### Ongoing Quality

| Metric | Target | Action if Below |
|--------|--------|-----------------|
| Success Rate | >98% | Review schema complexity |
| Parse Errors | <0.5% | Check model and prompt |
| Validation Errors | <2% | Refine schema or preprocessing |
| Latency P95 | <5s | Consider model or batch |
| Cost per Extract | <$0.01 | Optimize tokens or model |
