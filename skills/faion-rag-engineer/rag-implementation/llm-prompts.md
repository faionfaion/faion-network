# Rag Implementation - LLM Prompts

## AI-Assisted Development

Use these prompts with Claude, GPT-4, or other LLMs for implementation guidance.

## Architecture Prompts

### Design Pattern
```
Prompt: Design a rag-implementation system that:
1. Handles {use_case}
2. Implements {requirements}
3. Meets performance target: {target}

Consider:
- Scalability
- Error handling
- Monitoring/logging
```

### Code Generation
```
Prompt: Generate Python code for {specific_task} using rag-implementation.

Requirements:
- Handle {edge_cases}
- Include error handling
- Add docstrings
- Follow best practices from README.md
```

## Implementation Prompts

### Debugging
```
Prompt: Debug this {language} code that {problem}:

```{code}```

Using rag-implementation, what's the issue and how to fix it?
```

### Optimization
```
Prompt: Optimize this {language} implementation for {metric} (latency/throughput/memory).

Current performance: {current_metrics}
Target performance: {target_metrics}

{language}:
```{code}```
```

## Testing Prompts

### Test Generation
```
Prompt: Generate comprehensive tests for {function_name} that handles rag-implementation.

Consider:
- Normal cases
- Edge cases
- Error conditions
- Performance benchmarks
```

### Test Review
```
Prompt: Review these {language} tests for {module}:

```{test_code}```

Are they comprehensive? What's missing?
```

## Documentation Prompts

### API Documentation
```
Prompt: Generate API documentation for this {language} module:

```{code}```

Include:
- Function signatures
- Parameters with types
- Return values
- Example usage
- Common use cases
```

### Tutorial Generation
```
Prompt: Create a tutorial for implementing rag-implementation from scratch.

Target audience: {audience_level}
Use case: {specific_use_case}
Code examples: {language}
```

## Optimization Prompts

### Performance
```
Prompt: How can I improve the performance of {metric} in {language} for rag-implementation?

Current approach:
```{code}```

Bottlenecks:
- {bottleneck_1}
- {bottleneck_2}
```

### Cost Optimization
```
Prompt: How to reduce API costs while maintaining quality for rag-implementation?

Current setup:
- {api_call_pattern}
- {data_volume}
- {frequency}

Budget constraint: {budget}
```

---

## More Resources

- **README.md** - Full documentation with concepts and examples
- **templates.md** - Reusable code templates
- **examples.md** - Real-world implementation examples
