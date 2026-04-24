# Examples

> Real-world model selection scenarios and decisions.

## Example 1: Customer Support Chatbot

### Requirements
- 50,000 conversations/month
- Response time < 5s
- Mix of simple FAQ and complex troubleshooting
- Budget: $2,000/month

### Analysis
| Factor | Value |
|--------|-------|
| Volume | High (50K/month) |
| Latency | Medium (< 5s) |
| Task mix | 70% simple, 30% complex |
| Error cost | Medium (customer satisfaction) |

### Decision: Multi-Model Routing

```
User query
    |
    v
Intent classifier (local/DeepSeek)
    |
    +--> Simple FAQ --> DeepSeek V3 ($0.14/1M in)
    |
    +--> Product question --> GPT-4o ($2.50/1M in)
    |
    +--> Complex issue --> Claude Sonnet ($3/1M in)
```

### Cost Calculation

| Model | Requests | Avg Tokens | Monthly Cost |
|-------|----------|------------|--------------|
| DeepSeek (70%) | 35,000 | 2,000 | ~$30 |
| GPT-4o (20%) | 10,000 | 2,500 | ~$90 |
| Claude Sonnet (10%) | 5,000 | 3,000 | ~$70 |
| **Total** | 50,000 | - | **~$190** |

**Savings vs single GPT-4o:** ~60%

---

## Example 2: Legal Document Analysis

### Requirements
- 500 contracts/month
- High accuracy critical (legal liability)
- Documents 10-50 pages each
- Budget: $5,000/month

### Analysis
| Factor | Value |
|--------|-------|
| Volume | Low (500/month) |
| Latency | Not critical (batch) |
| Complexity | High (legal reasoning) |
| Error cost | Very high (legal risk) |

### Decision: Premium Model + RAG

```
Contract --> Document chunking --> RAG retrieval
                                        |
                                        v
                        Claude Opus 4.5 (200K context)
                                        |
                                        v
                        Structured analysis output
                                        |
                                        v
                        Human review workflow
```

### Rationale
- **Claude Opus 4.5** for complex legal reasoning
- **Long context** handles full contracts
- **RAG** retrieves relevant precedents/clauses
- **Human review** catches edge cases (given high error cost)

### Cost Calculation
- 500 contracts x 30 pages avg x 3,000 tokens/page = 45M tokens/month
- Opus input: 45M x $15/1M = $675
- Opus output: ~15M x $75/1M = $1,125
- Vector DB: ~$100/month
- **Total: ~$1,900/month** (well under budget)

---

## Example 3: Content Generation Platform

### Requirements
- 10,000 blog posts/month
- SEO-optimized, brand voice
- 2,000 words average
- Budget: $1,000/month

### Analysis
| Factor | Value |
|--------|-------|
| Volume | Very high (10K/month) |
| Latency | Not critical (batch) |
| Complexity | Medium (structured writing) |
| Error cost | Low (editable) |

### Decision: Fine-tuned Smaller Model

**Phase 1: Baseline**
```
GPT-4o --> Generate 1,000 high-quality examples
                    |
                    v
        Human editing for brand voice
                    |
                    v
        Training dataset ready
```

**Phase 2: Fine-tuning**
```
Training data --> Fine-tune GPT-4o-mini
                        |
                        v
        Fine-tuned model (brand voice)
                        |
                        v
        Production deployment
```

### Cost Comparison

| Approach | Per Article | Monthly Cost |
|----------|-------------|--------------|
| GPT-4o (baseline) | $0.08 | $800 |
| GPT-4o-mini (base) | $0.02 | $200 |
| GPT-4o-mini (fine-tuned) | $0.03 | $300 |

**Savings:** 62% with better brand consistency

---

## Example 4: Code Review Assistant

### Requirements
- 200 PRs/day
- Catch bugs, suggest improvements
- Response time < 30s
- Integration with GitHub

### Analysis
| Factor | Value |
|--------|-------|
| Volume | High (6,000/month) |
| Latency | Medium (< 30s) |
| Complexity | High (code reasoning) |
| Error cost | Medium (developer time) |

### Decision: Claude Sonnet 4

```
PR Diff --> Extract changed files
                    |
                    v
        Context gathering (related files)
                    |
                    v
        Claude Sonnet 4 (code expertise)
                    |
                    v
        Structured review comments
                    |
                    v
        Post to GitHub PR
```

### Rationale
- **Claude Sonnet 4** best for code understanding
- **Not Opus** - Sonnet sufficient for reviews, 3x faster
- **Not GPT** - Claude better at nuanced code feedback

### Cost Calculation
- 6,000 PRs x 5,000 tokens avg = 30M tokens/month
- Input: 30M x $3/1M = $90
- Output: 10M x $15/1M = $150
- **Total: ~$240/month**

---

## Example 5: Multimodal Product Catalog

### Requirements
- Process 50,000 product images/month
- Extract: title, description, attributes
- Support multiple languages
- Real-time API for uploads

### Analysis
| Factor | Value |
|--------|-------|
| Volume | Very high (50K/month) |
| Latency | Real-time (< 5s) |
| Task | Vision + text generation |
| Error cost | Low (human verification) |

### Decision: Gemini 2 Flash + GPT-4o Vision

```
Product Image
    |
    +--> High-res detail needed?
    |         |
    |         YES --> GPT-4o Vision (better detail)
    |         |
    |         NO --> Gemini 2 Flash (faster, cheaper)
    |
    v
Structured output (JSON)
    |
    v
Translation layer (if needed)
```

### Cost Calculation

| Model | % Traffic | Images | Cost |
|-------|-----------|--------|------|
| Gemini Flash (80%) | Simple products | 40,000 | ~$120 |
| GPT-4o Vision (20%) | Complex products | 10,000 | ~$150 |
| **Total** | - | 50,000 | **~$270/month** |

---

## Anti-Pattern Examples

### Anti-Pattern 1: Over-Engineering Simple Tasks

**Bad:**
```
Simple FAQ --> Claude Opus 4.5 --> $75/1M output
```

**Good:**
```
Simple FAQ --> GPT-4o-mini or DeepSeek --> $0.60/1M output
```

**Waste:** 100x cost increase for no quality benefit

### Anti-Pattern 2: Under-Powering Critical Decisions

**Bad:**
```
Medical symptom analysis --> DeepSeek --> Potential misdiagnosis
```

**Good:**
```
Medical symptom analysis --> Claude Opus + Human review --> Safe output
```

**Risk:** Liability from cheap model errors

### Anti-Pattern 3: Ignoring Total Cost

**Appears Cheaper:**
```
Small model: $0.10/call x 100,000 calls = $10,000
+ Developer fixing errors: 100 hrs x $50 = $5,000
Total: $15,000
```

**Actually Cheaper:**
```
Better model: $0.30/call x 100,000 calls = $30,000
+ Developer fixing errors: 10 hrs x $50 = $500
Total: $30,500 (but less developer frustration)
```

**Rule:** If error rate > 5%, consider upgrading model
