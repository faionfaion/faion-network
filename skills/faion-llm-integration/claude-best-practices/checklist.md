# Claude Best Practices - Checklist

## Model Selection

- [ ] Evaluate Sonnet 4 for balanced use cases (chat, general)
- [ ] Consider Opus 4.5 for complex analysis and reasoning
- [ ] Select Haiku 3.5 for cost-sensitive high-volume tasks
- [ ] Choose model based on task complexity and budget
- [ ] Document model selection rationale
- [ ] Test different models for output quality

## Prompt Engineering

- [ ] Write specific, detailed prompts (not vague)
- [ ] Include requirements in prompt text
- [ ] Specify output format (markdown, JSON, etc.)
- [ ] Add examples for better results
- [ ] Structure prompts with clear sections
- [ ] Iterate and refine prompts based on results

## System Prompt Design

- [ ] Define clear role for the model
- [ ] Specify behavior expectations
- [ ] Document output format requirements
- [ ] Include content guidelines
- [ ] Add resource links when relevant
- [ ] Test system prompt effectiveness

## Tool Definition Best Practices

- [ ] Write clear, descriptive tool names
- [ ] Provide detailed tool descriptions
- [ ] Define input schema with required fields
- [ ] Use enum for restricted choices
- [ ] Test tool invocation scenarios
- [ ] Document tool error handling

## Cost Optimization

- [ ] Implement prompt caching for repeated context
- [ ] Select appropriate model for task type
- [ ] Use Batch API for non-urgent work (50% savings)
- [ ] Set max_tokens appropriately (not too high)
- [ ] Pre-count tokens for large inputs
- [ ] Monitor and analyze costs regularly

## Prompt Caching Implementation

- [ ] Mark cacheable content with cache_control
- [ ] Structure static content for efficiency
- [ ] Test first call (cache creation) performance
- [ ] Verify subsequent calls use cache
- [ ] Track cache hit rates
- [ ] Achieve 90% token cost savings on cached context

## Batch Processing Strategy

- [ ] Prepare batch requests with custom_ids
- [ ] Group non-urgent tasks for batch processing
- [ ] Submit batch with 24-hour completion window
- [ ] Monitor batch job status
- [ ] Process results file (JSONL format)
- [ ] Calculate savings (typically 50% discount)

## Quality Assurance

- [ ] Test prompts with diverse inputs
- [ ] Evaluate output quality metrics
- [ ] Verify output format compliance
- [ ] Test edge cases and error scenarios
- [ ] Benchmark against previous approaches
- [ ] Document optimization results
