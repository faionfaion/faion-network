# Templates

> Decision document templates for ML approach and model selection.

## Template 1: Model Selection Decision Record

```markdown
# Model Selection Decision: [Application Name]

**Date:** YYYY-MM-DD
**Author:** [Name]
**Status:** Draft | Approved | Implemented

## Context

[Brief description of the application and what it needs to accomplish]

## Requirements

| Requirement | Value | Priority |
|-------------|-------|----------|
| Task type | [Generation/Classification/Extraction/etc.] | Required |
| Quality threshold | [Accuracy/quality level needed] | Required |
| Latency | [Real-time/Interactive/Batch] | Required |
| Volume | [Requests per month] | Required |
| Budget | [Monthly budget] | Required |
| Privacy | [Public API OK / Self-hosted required] | Required |
| Context length | [Max tokens needed] | If applicable |
| Multimodal | [Yes/No] | If applicable |

## Options Considered

### Option 1: [Model Name]

| Aspect | Details |
|--------|---------|
| Provider | [OpenAI/Anthropic/Google/etc.] |
| Model | [Exact model ID] |
| Pricing | Input: $X/1M, Output: $Y/1M |
| Projected cost | $Z/month |
| Latency | ~X tokens/sec |
| Pros | [List benefits] |
| Cons | [List drawbacks] |

### Option 2: [Model Name]

[Same structure as Option 1]

### Option 3: Multi-Model Routing

| Task Type | Model | % Traffic | Cost |
|-----------|-------|-----------|------|
| Simple | [Model] | X% | $Y |
| Complex | [Model] | X% | $Y |
| **Total** | - | 100% | $Z |

## Decision

**Selected:** [Option N - Model Name / Multi-Model Routing]

**Rationale:**
- [Reason 1]
- [Reason 2]
- [Reason 3]

## Cost Projection

| Scenario | Volume | Monthly Cost |
|----------|--------|--------------|
| Current | X requests | $Y |
| 5x growth | 5X requests | $Z |
| 10x growth | 10X requests | $W |

## Implementation Plan

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Accuracy | >X% | [How to measure] |
| Latency p95 | <Xs | [How to measure] |
| Cost per request | <$X | [How to measure] |

## Review Schedule

- [ ] 1 week post-launch: Initial metrics review
- [ ] 1 month post-launch: Cost optimization review
- [ ] Quarterly: Model upgrade assessment
```

---

## Template 2: Approach Decision Matrix

```markdown
# Approach Decision: [Use Case]

## Current State

[Description of current implementation or starting point]

## Decision Criteria

| Criterion | Weight | Prompting | RAG | Fine-tuning |
|-----------|--------|-----------|-----|-------------|
| Setup time | X% | [Score] | [Score] | [Score] |
| Ongoing cost | X% | [Score] | [Score] | [Score] |
| Quality | X% | [Score] | [Score] | [Score] |
| Maintainability | X% | [Score] | [Score] | [Score] |
| **Weighted Total** | 100% | [Total] | [Total] | [Total] |

### Scoring Guide
- 5: Excellent fit
- 4: Good fit
- 3: Acceptable
- 2: Suboptimal
- 1: Poor fit

## Analysis

### Prompt Engineering

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Estimated Cost:** $X/month
**Time to Deploy:** X hours/days

### RAG

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Estimated Cost:** $X/month (infra) + $Y/month (API)
**Time to Deploy:** X days/weeks

### Fine-tuning

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Estimated Cost:** $X (training) + $Y/month (inference)
**Time to Deploy:** X weeks/months

## Recommendation

**Selected Approach:** [Approach]

**Rationale:** [Why this approach best fits the requirements]

## Next Steps

1. [Action item 1]
2. [Action item 2]
3. [Action item 3]
```

---

## Template 3: Cost Analysis Worksheet

```markdown
# Cost Analysis: [Application Name]

## Token Usage Estimation

### Input Tokens

| Component | Tokens | Frequency | Monthly Total |
|-----------|--------|-----------|---------------|
| System prompt | X | Per request | Y |
| User input (avg) | X | Per request | Y |
| Context/RAG | X | Per request | Y |
| **Total Input** | - | - | Z |

### Output Tokens

| Component | Tokens | Frequency | Monthly Total |
|-----------|--------|-----------|---------------|
| Response (avg) | X | Per request | Y |
| **Total Output** | - | - | Z |

## API Cost Calculation

### Single Model

| Model | Input Cost | Output Cost | Total |
|-------|------------|-------------|-------|
| [Model 1] | $X | $Y | $Z |
| [Model 2] | $X | $Y | $Z |
| [Model 3] | $X | $Y | $Z |

### Multi-Model Routing

| Task Type | Model | % Traffic | Tokens | Cost |
|-----------|-------|-----------|--------|------|
| [Type 1] | [Model] | X% | Y | $Z |
| [Type 2] | [Model] | X% | Y | $Z |
| [Type 3] | [Model] | X% | Y | $Z |
| **Total** | - | 100% | - | $W |

## Infrastructure Costs (if RAG)

| Component | Service | Monthly Cost |
|-----------|---------|--------------|
| Vector DB | [Service] | $X |
| Embeddings | [Model] | $X |
| Compute | [Service] | $X |
| **Total Infra** | - | $Y |

## Total Cost of Ownership

| Category | Monthly Cost |
|----------|--------------|
| API costs | $X |
| Infrastructure | $X |
| Development/maintenance (est.) | $X |
| **Total** | $Y |

## Cost per Unit

| Metric | Value |
|--------|-------|
| Cost per request | $X |
| Cost per user (monthly) | $X |
| Cost per output word | $X |

## Scaling Projections

| Scale | Requests/mo | Est. Cost | Cost/Request |
|-------|-------------|-----------|--------------|
| 1x | X | $Y | $Z |
| 5x | X | $Y | $Z |
| 10x | X | $Y | $Z |
| 100x | X | $Y | $Z |

**Note:** Bulk pricing may apply at higher volumes.
```

---

## Template 4: Model Comparison Table

```markdown
# Model Comparison: [Use Case]

## Candidates

| Model | Provider | Context | Input $/1M | Output $/1M |
|-------|----------|---------|------------|-------------|
| [Model 1] | [Provider] | [Tokens] | $X | $Y |
| [Model 2] | [Provider] | [Tokens] | $X | $Y |
| [Model 3] | [Provider] | [Tokens] | $X | $Y |

## Benchmark Results

| Test | [Model 1] | [Model 2] | [Model 3] |
|------|-----------|-----------|-----------|
| [Task-specific test 1] | X% | X% | X% |
| [Task-specific test 2] | X% | X% | X% |
| [Task-specific test 3] | X% | X% | X% |
| Latency (tok/s) | X | X | X |
| **Average Score** | X | X | X |

## Qualitative Assessment

| Factor | [Model 1] | [Model 2] | [Model 3] |
|--------|-----------|-----------|-----------|
| Output quality | [1-5] | [1-5] | [1-5] |
| Instruction following | [1-5] | [1-5] | [1-5] |
| Consistency | [1-5] | [1-5] | [1-5] |
| Edge case handling | [1-5] | [1-5] | [1-5] |

## Cost Simulation (10,000 requests)

| Model | Estimated Cost | Quality Score | Cost/Quality |
|-------|----------------|---------------|--------------|
| [Model 1] | $X | Y | Z |
| [Model 2] | $X | Y | Z |
| [Model 3] | $X | Y | Z |

## Recommendation

**Best Overall:** [Model] - [Brief rationale]

**Best Value:** [Model] - [Brief rationale]

**Best Quality:** [Model] - [Brief rationale]
```

---

## Template 5: Routing Configuration

```markdown
# Model Routing Configuration: [Application Name]

## Routing Strategy

```yaml
routing:
  default_model: "gpt-4o"

  rules:
    - name: "simple_queries"
      condition:
        - token_count: "<500"
        - complexity: "low"
      model: "deepseek-v3"

    - name: "code_tasks"
      condition:
        - task_type: ["code_generation", "code_review"]
      model: "claude-sonnet-4"

    - name: "complex_reasoning"
      condition:
        - complexity: "high"
        - requires_reasoning: true
      model: "claude-opus-4.5"

    - name: "multimodal"
      condition:
        - has_images: true
      model: "gpt-4o"

  fallback:
    model: "gpt-4o"
    on_error: true
    on_rate_limit: true
```

## Complexity Classification

| Complexity | Indicators | Route To |
|------------|------------|----------|
| Low | <500 tokens, single intent, FAQ-like | DeepSeek |
| Medium | 500-2000 tokens, standard task | GPT-4o |
| High | >2000 tokens, multi-step, reasoning | Claude Opus |

## Expected Distribution

| Route | Model | Expected % | Avg Cost |
|-------|-------|------------|----------|
| Simple | DeepSeek | 40% | $0.01 |
| Standard | GPT-4o | 40% | $0.05 |
| Complex | Claude Opus | 15% | $0.50 |
| Code | Claude Sonnet | 5% | $0.10 |

**Weighted Average Cost per Request:** $X

## Monitoring

| Metric | Alert Threshold |
|--------|-----------------|
| Routing accuracy | <90% |
| Fallback rate | >10% |
| Cost per request | >$X |
| p95 latency | >Xs |
```
