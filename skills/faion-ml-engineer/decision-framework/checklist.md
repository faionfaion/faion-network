# Decision Checklist

> Systematic checklist for ML approach and model selection.

## Approach Selection Checklist

### Step 1: Define Requirements

- [ ] **Task type**: Generation / Classification / Extraction / Reasoning / Multimodal
- [ ] **Quality threshold**: What accuracy/quality level is acceptable?
- [ ] **Latency requirement**: Real-time (<2s) / Interactive (<10s) / Batch (>10s)
- [ ] **Volume**: Requests per day/month
- [ ] **Budget constraint**: Monthly budget for AI costs

### Step 2: Data Assessment

- [ ] **Need external data?** (documents, databases, APIs)
  - YES: Consider RAG
  - NO: Continue
- [ ] **Data is private/sensitive?**
  - YES: Self-hosted or RAG with local data
  - NO: Any provider
- [ ] **Data changes frequently?**
  - YES: RAG preferred (no retraining)
  - NO: Fine-tuning viable

### Step 3: Behavior Requirements

- [ ] **Standard task with good prompting?**
  - YES: Prompt engineering only
  - NO: Continue
- [ ] **Need specific output format?**
  - YES: Structured output (JSON mode)
  - NO: Continue
- [ ] **Need domain-specific behavior?**
  - YES: Fine-tuning
  - NO: Prompt engineering or RAG
- [ ] **Need consistent style/tone?**
  - YES: Fine-tuning or few-shot prompts
  - NO: Standard prompting

### Step 4: Cost-Performance Tradeoff

- [ ] **High volume + simple tasks?**
  - YES: Smaller model (DeepSeek, Llama)
  - NO: Continue
- [ ] **Critical decisions, high error cost?**
  - YES: Premium model (Claude Opus, GPT-5.2)
  - NO: Mid-tier model
- [ ] **User-facing with latency sensitivity?**
  - YES: Fast model (GPT-4o, Sonnet)
  - NO: Any model

## Model Selection Checklist

### Step 1: Task Requirements

| Requirement | Best Models |
|-------------|-------------|
| General purpose | GPT-4o, Claude Sonnet |
| Complex reasoning | Claude Opus 4.5, o3 |
| Code generation | Claude Sonnet/Opus, GPT-5.2 |
| Long context (>100K) | Gemini 2 Pro, Claude |
| Multimodal | Gemini, GPT-4o |
| High volume/low cost | DeepSeek, Llama |
| Privacy/self-hosted | Llama, Mistral |

### Step 2: Calculate Total Cost

```
Total Cost = API Costs + Developer Time + Infrastructure

API Costs:
  Input tokens/month x price per 1M input
+ Output tokens/month x price per 1M output
= Monthly API cost

Developer Time:
  Error correction hours x hourly rate
+ Prompt engineering hours x hourly rate
= Development cost

Infrastructure (if RAG/self-hosted):
  Vector DB cost
+ Compute cost
+ Storage cost
= Infrastructure cost
```

### Step 3: Multi-Model Routing Decision

- [ ] **Different task types with different complexity?**
  - YES: Implement routing
  - NO: Single model
- [ ] **Volume > 100K requests/month?**
  - YES: Routing saves significant cost
  - NO: Simpler architecture may be better
- [ ] **Can tolerate routing complexity?**
  - YES: Implement smart routing
  - NO: Use single mid-tier model

### Routing Strategy

| Task Complexity | Route To | Example |
|-----------------|----------|---------|
| Simple extraction | DeepSeek | Extract name from text |
| Standard generation | GPT-4o | Write email |
| Complex reasoning | Claude Opus | Analyze contract |
| Code generation | Claude Sonnet | Write function |

## Quick Decision Tree

```
START
  |
  v
Need external data? --YES--> RAG
  |NO
  v
Need specialized behavior? --YES--> Fine-tuning
  |NO
  v
High volume + simple? --YES--> Small model (DeepSeek)
  |NO
  v
Critical decisions? --YES--> Premium model (Opus, GPT-5.2)
  |NO
  v
User-facing? --YES--> Fast model (GPT-4o, Sonnet)
  |NO
  v
Default: Mid-tier model (GPT-4o, Sonnet)
```

## Pre-Launch Checklist

- [ ] Model selection documented with rationale
- [ ] Cost projections calculated for 1x, 5x, 10x volume
- [ ] Fallback model identified
- [ ] Rate limits understood
- [ ] Error handling implemented
- [ ] Monitoring/observability set up
- [ ] A/B testing plan for optimization
