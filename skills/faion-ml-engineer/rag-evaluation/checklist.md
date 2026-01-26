# RAG Evaluation Checklist

## Pre-Evaluation Setup

### Test Set Preparation

- [ ] Create diverse question types
  - [ ] Factual questions (simple lookup)
  - [ ] Comparative questions (compare A vs B)
  - [ ] Reasoning questions (require inference)
  - [ ] Summarization questions (aggregate info)
  - [ ] Multi-hop questions (require multiple docs)

- [ ] Establish ground truth
  - [ ] Manually verify correct answers
  - [ ] Document source passages for each answer
  - [ ] Mark relevant document IDs
  - [ ] Create relevance grades (0-3 scale)

- [ ] Sample size planning
  - [ ] Minimum 50 questions for statistical significance
  - [ ] Cover all document topics/domains
  - [ ] Include edge cases and failure modes

### Infrastructure Setup

- [ ] Evaluation framework selected
  - [ ] RAGAS for reference-free evaluation
  - [ ] Custom metrics for domain-specific needs
  - [ ] LLM evaluator configured (GPT-4o recommended)

- [ ] Logging and tracking
  - [ ] Evaluation results database
  - [ ] Version control for test sets
  - [ ] Metrics dashboard

## Retrieval Evaluation

### Core Metrics Checklist

| Metric | Target | Status |
|--------|--------|--------|
| Hit Rate | > 0.9 | [ ] |
| MRR | > 0.6 | [ ] |
| Precision@5 | > 0.7 | [ ] |
| Recall@5 | > 0.8 | [ ] |
| NDCG@10 | > 0.8 | [ ] |

### Retrieval Analysis

- [ ] Analyze failure cases
  - [ ] Zero results returned
  - [ ] Relevant docs ranked low
  - [ ] Wrong document retrieved

- [ ] Check for biases
  - [ ] Recency bias
  - [ ] Popularity bias
  - [ ] Length bias

- [ ] Test retrieval configurations
  - [ ] Different k values (3, 5, 10, 20)
  - [ ] Similarity thresholds
  - [ ] Hybrid search ratios (dense vs sparse)

## Generation Evaluation

### Core Metrics Checklist

| Metric | Target | Status |
|--------|--------|--------|
| Faithfulness | > 0.85 | [ ] |
| Answer Relevance | > 0.9 | [ ] |
| Context Relevance | > 0.7 | [ ] |
| Hallucination Rate | < 0.1 | [ ] |

### Generation Analysis

- [ ] Analyze failure modes
  - [ ] Hallucinations (fabricated facts)
  - [ ] Incomplete answers
  - [ ] Irrelevant information
  - [ ] Missing citations

- [ ] Check edge cases
  - [ ] Unanswerable questions
  - [ ] Conflicting context
  - [ ] Insufficient context

## End-to-End Evaluation

### System Metrics

- [ ] Latency (P50, P95, P99)
  - [ ] Retrieval latency
  - [ ] Generation latency
  - [ ] Total response time

- [ ] Cost metrics
  - [ ] Cost per query
  - [ ] Token usage per query
  - [ ] Embedding API costs

### Quality Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Answer Correctness | > 0.8 | [ ] |
| User Satisfaction | > 4/5 | [ ] |
| Task Completion | > 0.85 | [ ] |

## A/B Testing Checklist

- [ ] Define hypothesis
- [ ] Select control and treatment configs
- [ ] Determine sample size
- [ ] Run parallel evaluation
- [ ] Statistical significance test
- [ ] Document findings

## Production Monitoring

### Real-Time Metrics

- [ ] Response latency alerts
- [ ] Error rate monitoring
- [ ] Token usage tracking
- [ ] Cost monitoring

### Periodic Reviews

- [ ] Weekly: Sample review (10-20 queries)
- [ ] Monthly: Full evaluation on test set
- [ ] Quarterly: Ground truth refresh

## Post-Evaluation Actions

### Documentation

- [ ] Record all metric scores
- [ ] Document failure analysis
- [ ] Note configuration details
- [ ] Capture improvement recommendations

### Iteration

- [ ] Prioritize issues by impact
- [ ] Plan improvements
- [ ] Re-evaluate after changes
- [ ] Track metric trends over time

## Quick Reference: Metric Targets

| Metric | Minimum | Good | Excellent |
|--------|---------|------|-----------|
| Hit Rate | 0.8 | 0.9 | 0.95 |
| MRR | 0.4 | 0.6 | 0.8 |
| Precision@5 | 0.5 | 0.7 | 0.85 |
| NDCG@10 | 0.6 | 0.8 | 0.9 |
| Faithfulness | 0.7 | 0.85 | 0.95 |
| Answer Relevance | 0.8 | 0.9 | 0.95 |
| Latency P95 | < 5s | < 2s | < 1s |
