# RAG Evaluation Examples

## Retrieval Metrics Implementation

### Precision and Recall

```python
from typing import List, Set

def precision_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """
    Precision@K: How many retrieved docs are relevant?

    Args:
        retrieved: List of retrieved document IDs (ordered by rank)
        relevant: Set of relevant document IDs
        k: Number of top results to consider

    Returns:
        Precision score between 0 and 1
    """
    retrieved_at_k = set(retrieved[:k])
    relevant_retrieved = retrieved_at_k.intersection(relevant)
    return len(relevant_retrieved) / k


def recall_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """
    Recall@K: How many relevant docs were retrieved?
    """
    if not relevant:
        return 0.0
    retrieved_at_k = set(retrieved[:k])
    relevant_retrieved = retrieved_at_k.intersection(relevant)
    return len(relevant_retrieved) / len(relevant)


# Example usage
retrieved_docs = ["doc_1", "doc_3", "doc_5", "doc_2", "doc_7"]
relevant_docs = {"doc_1", "doc_2", "doc_4"}

print(f"Precision@3: {precision_at_k(retrieved_docs, relevant_docs, 3)}")  # 0.33
print(f"Recall@3: {recall_at_k(retrieved_docs, relevant_docs, 3)}")        # 0.33
print(f"Precision@5: {precision_at_k(retrieved_docs, relevant_docs, 5)}")  # 0.40
print(f"Recall@5: {recall_at_k(retrieved_docs, relevant_docs, 5)}")        # 0.67
```

### Mean Reciprocal Rank (MRR)

```python
def mean_reciprocal_rank(retrieved: List[str], relevant: Set[str]) -> float:
    """
    MRR: How highly is the first relevant doc ranked?

    Score interpretation:
        1.0  = First result is relevant
        0.5  = Second result is relevant
        0.33 = Third result is relevant
        0.0  = No relevant results
    """
    for i, doc_id in enumerate(retrieved):
        if doc_id in relevant:
            return 1.0 / (i + 1)
    return 0.0


def mrr_batch(queries: List[dict]) -> float:
    """Calculate MRR across multiple queries."""
    scores = []
    for query in queries:
        score = mean_reciprocal_rank(query["retrieved"], query["relevant"])
        scores.append(score)
    return sum(scores) / len(scores) if scores else 0.0


# Example
print(f"MRR: {mean_reciprocal_rank(retrieved_docs, relevant_docs)}")  # 1.0 (doc_1 is first)
```

### NDCG (Normalized Discounted Cumulative Gain)

```python
import numpy as np
from typing import Dict

def ndcg_at_k(retrieved: List[str], relevance_scores: Dict[str, float], k: int) -> float:
    """
    NDCG@K: Normalized Discounted Cumulative Gain.

    Considers graded relevance (not just binary).
    Relevance scores: 0=not relevant, 1=marginally, 2=relevant, 3=highly relevant

    Args:
        retrieved: List of retrieved document IDs (ordered by rank)
        relevance_scores: Dict mapping doc_id to relevance score (0-3)
        k: Number of top results to consider

    Returns:
        NDCG score between 0 and 1
    """
    def dcg(scores: List[float]) -> float:
        return sum(
            (2**score - 1) / np.log2(i + 2)
            for i, score in enumerate(scores)
        )

    # Actual DCG from retrieved order
    actual_scores = [relevance_scores.get(doc_id, 0) for doc_id in retrieved[:k]]
    actual_dcg = dcg(actual_scores)

    # Ideal DCG (best possible ranking)
    ideal_scores = sorted(relevance_scores.values(), reverse=True)[:k]
    ideal_dcg = dcg(ideal_scores)

    return actual_dcg / ideal_dcg if ideal_dcg > 0 else 0.0


# Example with graded relevance
relevance = {
    "doc_1": 3,  # Highly relevant
    "doc_2": 2,  # Relevant
    "doc_3": 1,  # Marginally relevant
    "doc_4": 3,  # Highly relevant (but not retrieved!)
    "doc_5": 0,  # Not relevant
}

print(f"NDCG@3: {ndcg_at_k(retrieved_docs, relevance, 3):.3f}")  # 0.766
print(f"NDCG@5: {ndcg_at_k(retrieved_docs, relevance, 5):.3f}")  # 0.793
```

### Hit Rate

```python
def hit_rate(retrieved: List[str], relevant: Set[str]) -> float:
    """
    Hit Rate: Was at least one relevant doc retrieved?

    Simple but important baseline metric.
    """
    return 1.0 if any(doc_id in relevant for doc_id in retrieved) else 0.0


def hit_rate_batch(queries: List[dict]) -> float:
    """Calculate hit rate across multiple queries."""
    hits = sum(
        hit_rate(q["retrieved"], q["relevant"])
        for q in queries
    )
    return hits / len(queries) if queries else 0.0
```

## Generation Quality Metrics (LLM-as-Judge)

### Faithfulness Evaluation

```python
from openai import OpenAI
import json

client = OpenAI()

def evaluate_faithfulness(
    answer: str,
    context: str,
    model: str = "gpt-4o"
) -> dict:
    """
    Faithfulness: Is the answer supported by the context?

    Returns:
        dict with: score, supported_claims, unsupported_claims, explanation
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

    return json.loads(response.choices[0].message.content)


# Example
context = """
Machine learning is a branch of artificial intelligence that
focuses on building systems that learn from data. It was coined
by Arthur Samuel in 1959.
"""

answer = """
Machine learning is a type of AI where computers learn from data.
It was invented by Arthur Samuel in 1959 and uses neural networks
exclusively.
"""

result = evaluate_faithfulness(answer, context)
# Expected: score ~0.7 (claim about neural networks is unsupported)
```

### Answer Relevance Evaluation

```python
def evaluate_relevance(
    answer: str,
    question: str,
    model: str = "gpt-4o"
) -> dict:
    """
    Answer Relevance: Does the answer address the question?

    Returns:
        dict with: score, addresses_question, completeness, explanation
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

    return json.loads(response.choices[0].message.content)
```

### Context Relevance Evaluation

```python
def evaluate_context_relevance(
    context: str,
    question: str,
    model: str = "gpt-4o"
) -> dict:
    """
    Context Relevance: Is the retrieved context relevant to the question?

    Returns:
        dict with: score, relevant_sentences, irrelevant_sentences, missing_info
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

    return json.loads(response.choices[0].message.content)
```

## RAGAS Integration

### Basic RAGAS Evaluation

```python
# pip install ragas datasets

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_correctness
)
from datasets import Dataset

def evaluate_with_ragas(
    questions: list[str],
    answers: list[str],
    contexts: list[list[str]],
    ground_truths: list[str]
) -> dict:
    """
    Comprehensive RAG evaluation using RAGAS framework.

    Args:
        questions: List of user questions
        answers: List of RAG-generated answers
        contexts: List of retrieved contexts (list of chunks per question)
        ground_truths: List of expected correct answers

    Returns:
        Dictionary with metric scores
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
questions = [
    "What is machine learning?",
    "Who invented machine learning?"
]
answers = [
    "Machine learning is a subset of AI that enables systems to learn from data.",
    "Arthur Samuel coined the term machine learning in 1959."
]
contexts = [
    ["Machine learning is a branch of artificial intelligence focused on building systems that learn from data."],
    ["The term 'machine learning' was coined by Arthur Samuel in 1959 while at IBM."]
]
ground_truths = [
    "Machine learning is a type of AI where computers learn from data without being explicitly programmed.",
    "Arthur Samuel invented machine learning in 1959."
]

scores = evaluate_with_ragas(questions, answers, contexts, ground_truths)
print(scores)
```

### RAGAS with Custom LLM

```python
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI

# Use GPT-4o for evaluation
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))

result = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy],
    llm=evaluator_llm
)
```

## Complete Evaluation Pipeline

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import json

@dataclass
class EvaluationResult:
    question: str
    answer: str
    context: list[str]
    ground_truth: Optional[str]
    retrieval_metrics: dict
    generation_metrics: dict
    timestamp: str


class RAGEvaluator:
    """Complete RAG evaluation pipeline."""

    def __init__(self, rag_pipeline, model: str = "gpt-4o"):
        self.rag = rag_pipeline
        self.model = model
        self.results: list[EvaluationResult] = []

    def evaluate_single(
        self,
        question: str,
        ground_truth: Optional[str] = None,
        relevant_doc_ids: Optional[set] = None
    ) -> EvaluationResult:
        """Evaluate single question."""
        # Get RAG response
        response = self.rag.query(question)

        # Extract components
        answer = response["answer"]
        contexts = [s["content"] for s in response["sources"]]
        retrieved_ids = [s["metadata"].get("id") for s in response["sources"]]

        # Retrieval metrics
        retrieval_metrics = {}
        if relevant_doc_ids:
            retrieval_metrics["precision@5"] = precision_at_k(retrieved_ids, relevant_doc_ids, 5)
            retrieval_metrics["recall@5"] = recall_at_k(retrieved_ids, relevant_doc_ids, 5)
            retrieval_metrics["mrr"] = mean_reciprocal_rank(retrieved_ids, relevant_doc_ids)
            retrieval_metrics["hit_rate"] = hit_rate(retrieved_ids, relevant_doc_ids)

        # Generation metrics
        context_combined = "\n\n".join(contexts)

        faithfulness_result = evaluate_faithfulness(answer, context_combined, self.model)
        relevance_result = evaluate_relevance(answer, question, self.model)
        context_result = evaluate_context_relevance(context_combined, question, self.model)

        generation_metrics = {
            "faithfulness": faithfulness_result.get("score", 0),
            "answer_relevance": relevance_result.get("score", 0),
            "context_relevance": context_result.get("score", 0)
        }

        result = EvaluationResult(
            question=question,
            answer=answer,
            context=contexts,
            ground_truth=ground_truth,
            retrieval_metrics=retrieval_metrics,
            generation_metrics=generation_metrics,
            timestamp=datetime.now().isoformat()
        )

        self.results.append(result)
        return result

    def evaluate_batch(self, test_set: list[dict]) -> dict:
        """Evaluate batch of questions and compute aggregate metrics."""
        for item in test_set:
            self.evaluate_single(
                question=item["question"],
                ground_truth=item.get("answer"),
                relevant_doc_ids=item.get("relevant_docs")
            )

        return self.aggregate_metrics()

    def aggregate_metrics(self) -> dict:
        """Compute aggregate metrics across all evaluations."""
        if not self.results:
            return {}

        metrics = {
            "avg_faithfulness": 0,
            "avg_answer_relevance": 0,
            "avg_context_relevance": 0,
            "avg_precision@5": 0,
            "avg_recall@5": 0,
            "avg_mrr": 0,
            "total_evaluated": len(self.results)
        }

        for result in self.results:
            metrics["avg_faithfulness"] += result.generation_metrics.get("faithfulness", 0)
            metrics["avg_answer_relevance"] += result.generation_metrics.get("answer_relevance", 0)
            metrics["avg_context_relevance"] += result.generation_metrics.get("context_relevance", 0)
            metrics["avg_precision@5"] += result.retrieval_metrics.get("precision@5", 0)
            metrics["avg_recall@5"] += result.retrieval_metrics.get("recall@5", 0)
            metrics["avg_mrr"] += result.retrieval_metrics.get("mrr", 0)

        n = len(self.results)
        for key in metrics:
            if key.startswith("avg_"):
                metrics[key] /= n

        return metrics

    def export_results(self, filepath: str):
        """Export results to JSON."""
        data = [
            {
                "question": r.question,
                "answer": r.answer,
                "ground_truth": r.ground_truth,
                "retrieval_metrics": r.retrieval_metrics,
                "generation_metrics": r.generation_metrics,
                "timestamp": r.timestamp
            }
            for r in self.results
        ]

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
```

## Test Set Generation

```python
def generate_test_questions(
    documents: list[str],
    num_questions: int = 10,
    model: str = "gpt-4o"
) -> list[dict]:
    """
    Generate test questions from documents.
    """
    test_set = []

    for doc in random.sample(documents, min(num_questions, len(documents))):
        prompt = f"""Based on this document, generate a question and its answer.

Document:
{doc[:2000]}

Generate a factual question that can be answered from this document.
Return JSON with: question, answer, source_quote"""

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        qa = json.loads(response.choices[0].message.content)
        qa["document"] = doc
        test_set.append(qa)

    return test_set


def generate_diverse_questions(
    documents: list[str],
    question_types: list[str] = ["factual", "comparative", "reasoning", "summarization"]
) -> list[dict]:
    """
    Generate diverse question types for comprehensive testing.
    """
    test_set = []

    type_descriptions = {
        "factual": "Simple fact lookup (who, what, when, where)",
        "comparative": "Compare two concepts, features, or entities",
        "reasoning": "Requires inference or logical deduction",
        "summarization": "Summarize or synthesize information"
    }

    for q_type in question_types:
        prompt = f"""Generate a {q_type} question based on these documents.

Documents:
{chr(10).join(documents[:3])}

Question type: {q_type}
Description: {type_descriptions[q_type]}

Return JSON with: question, expected_answer, type, difficulty (easy/medium/hard)"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        test_set.append(json.loads(response.choices[0].message.content))

    return test_set
```

## A/B Testing Framework

```python
class RAGABTest:
    """A/B testing for RAG configurations."""

    def __init__(self, config_a: dict, config_b: dict):
        self.config_a = config_a
        self.config_b = config_b
        self.results_a = []
        self.results_b = []

    def run_test(
        self,
        test_questions: list[str],
        rag_a,  # RAG pipeline with config A
        rag_b   # RAG pipeline with config B
    ):
        """Run A/B test on both configurations."""
        import time

        for question in test_questions:
            # Test config A
            start = time.time()
            response_a = rag_a.query(question)
            latency_a = time.time() - start

            self.results_a.append({
                "question": question,
                "answer": response_a["answer"],
                "latency": latency_a,
                "num_sources": len(response_a.get("sources", []))
            })

            # Test config B
            start = time.time()
            response_b = rag_b.query(question)
            latency_b = time.time() - start

            self.results_b.append({
                "question": question,
                "answer": response_b["answer"],
                "latency": latency_b,
                "num_sources": len(response_b.get("sources", []))
            })

    def compare_results(self) -> dict:
        """Compare results between configurations."""
        def avg(results: list[dict], key: str) -> float:
            values = [r.get(key, 0) for r in results]
            return sum(values) / len(values) if values else 0

        return {
            "config_a": {
                "name": self.config_a.get("name", "Config A"),
                "avg_latency": avg(self.results_a, "latency"),
                "avg_sources": avg(self.results_a, "num_sources"),
                "total_questions": len(self.results_a)
            },
            "config_b": {
                "name": self.config_b.get("name", "Config B"),
                "avg_latency": avg(self.results_b, "latency"),
                "avg_sources": avg(self.results_b, "num_sources"),
                "total_questions": len(self.results_b)
            }
        }

    def statistical_significance(self, metric: str = "latency") -> dict:
        """Calculate statistical significance using t-test."""
        from scipy import stats

        values_a = [r.get(metric, 0) for r in self.results_a]
        values_b = [r.get(metric, 0) for r in self.results_b]

        t_stat, p_value = stats.ttest_ind(values_a, values_b)

        return {
            "metric": metric,
            "t_statistic": t_stat,
            "p_value": p_value,
            "significant": p_value < 0.05,
            "better_config": "A" if np.mean(values_a) < np.mean(values_b) else "B"
        }
```
