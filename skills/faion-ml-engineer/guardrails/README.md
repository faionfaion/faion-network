# LLM Guardrails

Comprehensive guide to implementing safety guardrails for LLM-based applications. Guardrails are essential components that transform unpredictable generative models into reliable, safe, and compliant systems.

## Overview

Guardrails (or "rails") are specific mechanisms for controlling LLM behavior:
- Preventing harmful or inappropriate content
- Enforcing topic boundaries
- Validating output format and structure
- Detecting and blocking prompt injection attacks
- Filtering PII and sensitive data
- Reducing hallucinations

## Key Concepts

### Input vs Output Guardrails

| Type | Purpose | Examples |
|------|---------|----------|
| **Input Rails** | Filter/validate user input before LLM | PII masking, injection detection, length limits |
| **Output Rails** | Validate/filter LLM responses | Content moderation, format validation, hallucination check |
| **Dialog Rails** | Control conversation flow | Topic boundaries, persona enforcement |
| **Retrieval Rails** | Filter RAG chunks | Relevance filtering, sensitive data removal |
| **Execution Rails** | Validate tool/action calls | Permission checks, parameter validation |

### Embedded vs Programmable Guardrails

**Embedded Guardrails:**
- Built into model through training (RLHF, Constitutional AI)
- Part of model's base behavior
- Examples: Claude's safety training, Llama Guard classification

**Programmable Guardrails:**
- External rule-based systems
- Runtime monitoring and filtering
- Examples: NeMo Guardrails, Guardrails AI, custom validators

### Guardrail Strategies

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **Block** | Reject input/output entirely | Dangerous content, injection attacks |
| **Filter** | Remove problematic parts | PII, URLs, code blocks |
| **Transform** | Modify to acceptable form | Rephrase, summarize, mask |
| **Warn** | Flag for review | Borderline content, low confidence |
| **Log** | Record without blocking | Analytics, audit trails |

## Framework Comparison

### NeMo Guardrails (NVIDIA)

**Best for:** Complex conversational flows, multi-turn dialogs, enterprise deployments

| Feature | Details |
|---------|---------|
| Architecture | Colang DSL for dialog flow definition |
| Input Rails | Jailbreak detection, topic control, content safety |
| Output Rails | Fact-checking, hallucination detection, moderation |
| Integration | LangChain, LangGraph, LlamaIndex |
| Models | Works with any LLM; optimized for NVIDIA NIM |
| Latency | GPU-accelerated for low latency |

**Strengths:**
- Declarative dialog flow control
- State machine approach for complex conversations
- Built-in jailbreak detection
- Fact-checking against knowledge base
- Multi-agent support

**Limitations:**
- Learning curve for Colang DSL
- Heavier setup compared to simple validators
- Best performance with NVIDIA infrastructure

### Guardrails AI

**Best for:** Output validation, structured data extraction, schema enforcement

| Feature | Details |
|---------|---------|
| Architecture | Validator-based pipeline |
| Spec Format | RAIL (XML) or Pydantic schemas |
| Validators | 50+ pre-built on Guardrails Hub |
| Languages | Python, JavaScript |
| Integration | OpenAI, Anthropic, local models |

**Strengths:**
- Simple, code-first approach
- Rich validator ecosystem
- Strong typing and schema validation
- Easy to extend with custom validators
- Good for structured output extraction

**Limitations:**
- Less sophisticated dialog control
- Primarily output-focused
- No built-in conversation state management

### Llama Guard (Meta)

**Best for:** Content classification, safety filtering

| Feature | Details |
|---------|---------|
| Type | Fine-tuned Llama model |
| Task | Binary/multi-class safety classification |
| Categories | Customizable safety taxonomy |
| Usage | Input/output classification |

**Strengths:**
- High accuracy on safety classification
- Customizable categories
- Can run locally

**Limitations:**
- Classification only (no transformation)
- Requires additional logic for filtering
- Model inference overhead

### Custom Implementation

**Best for:** Specific requirements, maximum control, lightweight deployments

| Approach | Pros | Cons |
|----------|------|------|
| Regex/Rules | Fast, deterministic | Brittle, limited |
| LLM-as-judge | Flexible, semantic | Latency, cost |
| Classifier | Accurate, fast | Training data needed |
| Hybrid | Best of both | Complex setup |

## Architecture Patterns

### Basic Pipeline

```
User Input → Input Rails → LLM → Output Rails → Response
                ↓                      ↓
           Blocked/Modified      Blocked/Modified
```

### RAG with Guardrails

```
User Input → Input Rails → Query → Retrieval Rails → Chunks
                                          ↓
                                    Filtered Chunks
                                          ↓
                               LLM (with context)
                                          ↓
                                    Output Rails
                                          ↓
                                      Response
```

### Multi-Agent with Guardrails

```
User Input → Input Rails → Router Agent
                                ↓
                    ┌──────────┼──────────┐
                    ↓          ↓          ↓
                Agent A    Agent B    Agent C
                    ↓          ↓          ↓
              Execution Rails (each agent)
                    ↓          ↓          ↓
                    └──────────┼──────────┘
                               ↓
                         Output Rails
                               ↓
                           Response
```

## Decision Framework

### When to Use Which Framework

```
START
  │
  ├─ Need complex dialog control?
  │   YES → NeMo Guardrails
  │   NO  ↓
  │
  ├─ Need structured output validation?
  │   YES → Guardrails AI
  │   NO  ↓
  │
  ├─ Need safety classification?
  │   YES → Llama Guard + Custom logic
  │   NO  ↓
  │
  ├─ Simple validation needs?
  │   YES → Custom implementation
  │   NO  ↓
  │
  └─ Complex requirements?
      → Combine frameworks
```

### Guardrail Selection by Use Case

| Use Case | Recommended Approach |
|----------|---------------------|
| Customer support bot | NeMo Guardrails (dialog control) |
| Data extraction | Guardrails AI (schema validation) |
| Content moderation | Llama Guard + rules |
| Code generation | Custom validators + sandboxing |
| Medical/Legal | All layers + human review |
| Internal tools | Lighter validation, logging |

## Performance Considerations

### Latency Impact

| Guardrail Type | Typical Latency | Optimization |
|----------------|-----------------|--------------|
| Regex/Rules | <1ms | Compile patterns |
| Classifier | 10-50ms | Batch, cache |
| LLM-as-judge | 500ms-2s | Async, cache |
| Full pipeline | 1-3s | Parallel checks |

### Cost Optimization

| Strategy | Description |
|----------|-------------|
| Tiered checking | Simple rules first, LLM checks for edge cases |
| Caching | Cache common input/output validations |
| Sampling | Check subset in production, full in development |
| Async logging | Non-blocking audit logging |

## Security Considerations

### Prompt Injection Defense

1. **Input sanitization** - Remove/escape special characters
2. **Instruction hierarchy** - System prompts take precedence
3. **Output validation** - Check for instruction echoing
4. **Isolation** - Separate user content from instructions

### PII Protection

1. **Detection** - Identify PII in input/output
2. **Masking** - Replace with placeholders
3. **Logging** - Never log raw PII
4. **Encryption** - Encrypt sensitive data at rest

## Monitoring and Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Block rate | % of blocked requests | >10% (investigate) |
| False positive rate | Legitimate content blocked | >1% (tune) |
| Latency p99 | 99th percentile latency | >3s (optimize) |
| Violation types | Distribution of violations | Sudden changes |

### Logging Requirements

```
Required fields:
- timestamp
- request_id
- guardrail_type
- result (pass/fail/warn)
- latency_ms
- violation_details (if failed)
- user_id (hashed)

Never log:
- Raw user input (may contain PII)
- Full LLM output (may contain sensitive data)
- API keys or credentials
```

## Files in This Directory

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Design, implementation, testing checklists |
| [examples.md](examples.md) | Code examples for all frameworks |
| [templates.md](templates.md) | Configuration and policy templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for guardrail design and testing |

## External Resources

### Official Documentation

- [NeMo Guardrails Documentation](https://docs.nvidia.com/nemo/guardrails/latest/index.html)
- [NeMo Guardrails GitHub](https://github.com/NVIDIA-NeMo/Guardrails)
- [Guardrails AI Documentation](https://www.guardrailsai.com/docs)
- [Guardrails Hub](https://hub.guardrailsai.com/)

### Research Papers

- [NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications](https://arxiv.org/abs/2310.10501)
- [Llama Guard: LLM-based Input-Output Safeguard](https://arxiv.org/abs/2312.06674)

### Tutorials and Guides

- [NVIDIA Developer - NeMo Guardrails](https://developer.nvidia.com/nemo-guardrails)
- [Guardrails AI + NeMo Integration](https://www.guardrailsai.com/blog/nemoguardrails-integration)
- [Essential Guide to LLM Guardrails](https://medium.com/data-science-collective/essential-guide-to-llm-guardrails-llama-guard-nemo-d16ebb7cbe82)

### Related Methodologies

- [prompt-engineering.md](../methodologies/prompt-engineering.md) - Prompt design patterns
- [llm-apis.md](../methodologies/llm-apis.md) - LLM API integration
- [rag-pipeline.md](../methodologies/rag-pipeline.md) - RAG implementation

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-01 | Reorganized into folder structure |
| 1.0.0 | 2024-11 | Initial guardrails methodology |
