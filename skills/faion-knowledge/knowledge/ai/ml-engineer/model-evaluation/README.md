---
id: model-evaluation
name: "Model Evaluation"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Model Evaluation

## Overview

Model evaluation systematically assesses LLM performance across various dimensions including accuracy, latency, cost, safety, and task-specific metrics. Proper evaluation is essential for model selection, prompt optimization, and production monitoring.

## When to Use

- Selecting between different models
- Comparing prompt strategies
- Before deploying to production
- After fine-tuning
- Continuous monitoring
- A/B testing changes

## Evaluation Dimensions

| Dimension | Metrics | Priority |
|-----------|---------|----------|
| Quality | Accuracy, F1, BLEU, ROUGE | High |
| Latency | p50, p95, p99 | Medium-High |
| Cost | $/1K tokens, $/request | Medium |
| Safety | Toxicity, bias, refusal rate | High |
| Reliability | Success rate, error rate | High |

## Evaluation Types

**Offline Evaluation:**
- Test datasets with ground truth
- Automated metrics
- Reproducible benchmarks

**Online Evaluation:**
- A/B testing in production
- User feedback collection
- Real-time monitoring

## Key Benchmarks (2025-2026)

### Knowledge & Reasoning

| Benchmark | Focus | Notes |
|-----------|-------|-------|
| MMLU | 57 subjects (math, history, law) | Saturating for top models |
| MMLU-Pro | 10 choices, harder reasoning | Expert-reviewed, reduced noise |
| GPQA | Domain expert questions | Validated difficulty |
| ARC | Science reasoning | Challenge + Easy sets |
| HellaSwag | Commonsense reasoning | Sentence completion |
| WinoGrande | Coreference resolution | Pronoun disambiguation |
| BoolQ | Boolean QA | Yes/no questions |
| TruthfulQA | Truthfulness | GPT-Judge evaluator |

### Code Generation

| Benchmark | Focus | Notes |
|-----------|-------|-------|
| HumanEval | Python coding | 164 problems, pass@k metric |
| HumanEval+ | Extended tests | More rigorous validation |
| MBPP | Basic Python | 1000 crowd-sourced problems |
| LiveCodeBench | Live contests | Contamination-free (LeetCode, AtCoder) |
| SWE-bench | Real GitHub issues | End-to-end software engineering |
| BigCodeBench | Complex coding | Multi-function, library usage |

### Mathematical Reasoning

| Benchmark | Focus | Notes |
|-----------|-------|-------|
| GSM8K | Grade school math | 8.5K word problems |
| MATH | Competition math | High school competitions |
| MathVista | Visual math | Diagrams, charts |

### Instruction Following

| Benchmark | Focus | Notes |
|-----------|-------|-------|
| IFEval | Instruction following | Verifiable constraints |
| MT-Bench | Multi-turn chat | LLM-as-judge scoring |
| AlpacaEval | Instruction quality | GPT-4 as evaluator |

### Safety & Alignment

| Benchmark | Focus | Notes |
|-----------|-------|-------|
| ToxiGen | Toxicity detection | Implicit toxic language |
| RealToxicityPrompts | Toxicity generation | Prompt continuation |
| BBQ | Bias evaluation | 9 social categories |
| BOLD | Fairness | Demographic bias |

## Evaluation Methods

### Automated Metrics

| Metric | Use Case | Formula/Tool |
|--------|----------|--------------|
| Exact Match | Classification | `actual == expected` |
| Contains Match | Factual QA | `expected in actual` |
| BLEU | Translation | n-gram precision |
| ROUGE | Summarization | Recall-oriented |
| BERTScore | Semantic similarity | Contextual embeddings |
| pass@k | Code generation | k samples, any passes |

### LLM-as-Judge

Use a powerful LLM to evaluate outputs on criteria like:
- Relevance
- Helpfulness
- Accuracy
- Coherence
- Safety

**Best Practices:**
- Use GPT-4 or Claude as judge
- Provide clear rubrics
- Include reference answers when available
- Run multiple evaluations for consistency

### Human Evaluation

| Method | When to Use |
|--------|-------------|
| A/B preference | Comparing outputs |
| Likert scale | Rating quality dimensions |
| Error annotation | Finding failure modes |
| Expert review | Domain-specific evaluation |

## Production Monitoring

### Key Metrics

| Metric | Threshold |
|--------|-----------|
| Success rate | > 99% |
| p95 latency | < 3s |
| Error rate | < 1% |
| Quality score | > 4.0/5.0 |

### Sampling Strategy

- Sample 1-10% of production traffic
- Use stratified sampling across user segments
- Store samples for offline analysis
- Run LLM-as-judge on smaller sample (0.1-1%)

## Current Challenges (2025-2026)

1. **Benchmark Saturation** - Top models approaching ceiling on MMLU, HumanEval
2. **Data Contamination** - Training on benchmark data inflates scores
3. **Evaluation Crisis** - Unclear which metrics matter most
4. **Benchmark Gaming** - Models optimized for specific tests
5. **Multi-dimensional Trade-offs** - Quality vs latency vs cost

## Files in This Directory

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts |
| [checklist.md](checklist.md) | Evaluation checklist |
| [examples.md](examples.md) | Code examples |
| [templates.md](templates.md) | Evaluation templates |
| [llm-prompts.md](llm-prompts.md) | LLM-as-judge prompts |

## References

- [HELM Benchmark](https://crfm.stanford.edu/helm/)
- [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness)
- [OpenAI Evals](https://github.com/openai/evals)
- [RAGAS](https://docs.ragas.io/)
- [DeepEval](https://deepeval.com/)
- [Evidently AI Benchmarks Guide](https://www.evidentlyai.com/llm-guide/llm-benchmarks)
- [Hugging Face Evaluation Guidebook](https://huggingface.co/spaces/OpenEvals/evaluation-guidebook)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Benchmark selection | sonnet | Evaluation framework |
| Metric interpretation | sonnet | Analysis |
| Model comparison | sonnet | Evaluation |
