---
id: rag-eval-metrics
name: "RAG Evaluation Metrics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# RAG Evaluation Metrics

## Overview

RAG evaluation metrics measure retrieval quality, generation quality, and end-to-end performance. This document covers all core metrics with implementations.

## Evaluation Dimensions

| Dimension | Measures | Key Metrics |
|-----------|----------|-------------|
| Retrieval | Finding relevant docs | Precision, Recall, MRR, NDCG |
| Generation | Response quality | Faithfulness, Relevance, Coherence |
| End-to-End | Full pipeline | Answer accuracy, User satisfaction |

## RAG Triad (RAGAS Framework)

```
┌─────────────────────────────────────────┐
│           CONTEXT RELEVANCE             │
│   (Is retrieved context relevant?)       │
└────────────────────┬────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   FAITHFULNESS  │    │ ANSWER RELEVANCE│
│ (Is answer true │    │ (Does answer    │
│  to context?)   │    │  address query?)│
└─────────────────┘    └─────────────────┘
```

## Retrieval Metrics

### Implementation

```python
from typing import List, Set, Dict
import numpy as np

def precision_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """
    Precision@K: How many retrieved docs are relevant?

    Args:
        retrieved: List of retrieved document IDs (ordered by rank)
        relevant: Set of relevant document IDs
        k: Number of top results to consider
    """
    retrieved_at_k = set(retrieved[:k])
    relevant_retrieved = retrieved_at_k.intersection(relevant)
    return len(relevant_retrieved) / k

def recall_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """
    Recall@K: How many relevant docs were retrieved?
    """
    retrieved_at_k = set(retrieved[:k])
    relevant_retrieved = retrieved_at_k.intersection(relevant)
    return len(relevant_retrieved) / len(relevant) if relevant else 0

def mean_reciprocal_rank(retrieved: List[str], relevant: Set[str]) -> float:
    """
    MRR: How highly is the first relevant doc ranked?
    """
    for i, doc_id in enumerate(retrieved):
        if doc_id in relevant:
            return 1.0 / (i + 1)
    return 0.0

def ndcg_at_k(retrieved: List[str], relevance_scores: Dict[str, float], k: int) -> float:
    """
    NDCG@K: Normalized Discounted Cumulative Gain.
    Considers graded relevance (not just binary).
    """
    def dcg(scores: List[float]) -> float:
        return sum(
            (2**score - 1) / np.log2(i + 2)
            for i, score in enumerate(scores)
        )

    # Actual DCG
    actual_scores = [relevance_scores.get(doc_id, 0) for doc_id in retrieved[:k]]
    actual_dcg = dcg(actual_scores)

    # Ideal DCG (best possible ranking)
    ideal_scores = sorted(relevance_scores.values(), reverse=True)[:k]
    ideal_dcg = dcg(ideal_scores)

    return actual_dcg / ideal_dcg if ideal_dcg > 0 else 0

def hit_rate(retrieved: List[str], relevant: Set[str]) -> float:
    """
    Hit Rate: Was at least one relevant doc retrieved?
    """
    return 1.0 if any(doc_id in relevant for doc_id in retrieved) else 0.0
```

### Metric Selection Guide

| Metric | When to Use | Range | Interpretation |
|--------|-------------|-------|----------------|
| Precision@K | Care about accuracy in top-K | 0-1 | Higher = fewer irrelevant docs |
| Recall@K | Need to find all relevant docs | 0-1 | Higher = fewer missed docs |
| MRR | First relevant result matters | 0-1 | Higher = relevant docs ranked higher |
| NDCG@K | Graded relevance (not binary) | 0-1 | Higher = better ranking quality |
| Hit Rate | Only need one relevant doc | 0-1 | Binary: found relevant or not |

## Generation Quality Metrics

### LLM-Based Evaluation

```python
from openai import OpenAI

client = OpenAI()

def evaluate_faithfulness(
    answer: str,
    context: str,
    model: str = "gpt-4o"
) -> Dict[str, any]:
    """
    Faithfulness: Is the answer supported by the context?
    """
    prompt = f"""Evaluate if the answer is faithful to the given context.

Context:
{context}

Answer:
{answer}

Analyze the answer and determine:
1. What claims does the answer make?
2. Is each claim supported by the context?
3. Are there any hallucinations (claims not in context)?

Provide a score from 0 to 1 where:
- 1.0: Completely faithful, all claims supported
- 0.5: Partially faithful, some unsupported claims
- 0.0: Unfaithful, major hallucinations

Return JSON with: score, supported_claims, unsupported_claims, explanation"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    import json
    return json.loads(response.choices[0].message.content)

def evaluate_relevance(
    answer: str,
    question: str,
    model: str = "gpt-4o"
) -> Dict[str, any]:
    """
    Answer Relevance: Does the answer address the question?
    """
    prompt = f"""Evaluate if the answer addresses the question.

Question:
{question}

Answer:
{answer}

Analyze:
1. Does the answer directly address the question?
2. Is the answer complete or partial?
3. Is there irrelevant information?

Score from 0 to 1 where:
- 1.0: Completely answers the question
- 0.5: Partially answers or includes irrelevant info
- 0.0: Does not answer the question

Return JSON with: score, addresses_question, completeness, explanation"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    import json
    return json.loads(response.choices[0].message.content)

def evaluate_context_relevance(
    context: str,
    question: str,
    model: str = "gpt-4o"
) -> Dict[str, any]:
    """
    Context Relevance: Is the retrieved context relevant to the question?
    """
    prompt = f"""Evaluate if the context is relevant to answering the question.

Question:
{question}

Context:
{context}

Analyze:
1. Does the context contain information to answer the question?
2. How much of the context is relevant?
3. What relevant information is missing?

Score from 0 to 1 where:
- 1.0: Context fully relevant and sufficient
- 0.5: Partially relevant or incomplete
- 0.0: Irrelevant context

Return JSON with: score, relevant_sentences, irrelevant_sentences, missing_info"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    import json
    return json.loads(response.choices[0].message.content)
```

## RAGAS Integration

```python
# pip install ragas

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    context_entity_recall,
    answer_similarity,
    answer_correctness
)
from datasets import Dataset

def evaluate_with_ragas(
    questions: List[str],
    answers: List[str],
    contexts: List[List[str]],
    ground_truths: List[str]
) -> Dict[str, float]:
    """
    Comprehensive RAG evaluation using RAGAS framework.
    """
    # Prepare dataset
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    dataset = Dataset.from_dict(data)

    # Run evaluation
    result = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
            answer_correctness
        ]
    )

    return result

# Example usage
questions = ["What is machine learning?"]
answers = ["Machine learning is a subset of AI that enables systems to learn from data."]
contexts = [["Machine learning is a branch of artificial intelligence focused on building systems that learn from data."]]
ground_truths = ["Machine learning is a type of AI where computers learn from data without being explicitly programmed."]

scores = evaluate_with_ragas(questions, answers, contexts, ground_truths)
print(scores)
```

## Metric Selection Best Practices

### By Evaluation Stage

| Stage | Recommended Metrics |
|-------|-------------------|
| **Development** | Precision@5, Recall@5, Faithfulness |
| **Pre-production** | Full RAGAS suite + NDCG |
| **Production Monitoring** | Hit Rate, Faithfulness, Latency |
| **A/B Testing** | End-to-end accuracy, User satisfaction |

### By Use Case

| Use Case | Key Metrics |
|----------|-------------|
| **Question Answering** | Faithfulness, Answer Relevance, Precision@3 |
| **Document Search** | NDCG@10, Recall@20, MRR |
| **Chatbot** | Context Relevance, Coherence, User satisfaction |
| **Summarization** | Faithfulness, Completeness, Conciseness |

## Cost Optimization

### Metric Tiers by Cost

| Tier | Metrics | Cost | When to Use |
|------|---------|------|-------------|
| **Free** | Precision, Recall, MRR, NDCG | None | Always include |
| **Low** | RAGAS with small model | $ | Regular testing |
| **Medium** | LLM-based with GPT-4o-mini | $$ | Important evals |
| **High** | Full suite with GPT-4o | $$$ | Critical decisions |

### Sampling Strategy

```python
def smart_sampling(
    test_set: List[dict],
    budget: int,
    strategy: str = "diverse"
) -> List[dict]:
    """
    Sample test cases based on budget and strategy.

    Strategies:
    - diverse: Cover different question types
    - difficult: Focus on hard cases
    - random: Random sampling
    """
    if strategy == "diverse":
        # Group by question type, sample evenly
        pass
    elif strategy == "difficult":
        # Prioritize cases where model previously failed
        pass
    else:
        # Random sampling
        import random
        return random.sample(test_set, min(budget, len(test_set)))
```

## Common Pitfalls

1. **Single Metric Trap** - Don't rely on one metric only
2. **No Baseline** - Always compare against a baseline
3. **Evaluator Bias** - LLM evaluators have their own biases
4. **Non-representative Test Set** - Ensure test matches production
5. **Ignoring Edge Cases** - Test on difficult/ambiguous queries
6. **Static Ground Truth** - Update ground truth as system evolves

## References

- [RAGAS Paper](https://arxiv.org/abs/2309.15217)
- [RAGAS Documentation](https://docs.ragas.io/)
- [Information Retrieval Metrics](https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval))

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## Sources

- [RAGAS Paper](https://arxiv.org/abs/2309.15217)
- [RAGAS Docs](https://docs.ragas.io/)
- [IR Metrics](https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval))
- [TruLens RAG Triad](https://www.trulens.org/trulens_eval/tracking/instrumentation/rag_triad/)
