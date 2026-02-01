---
id: rag-eval-methods
name: "RAG Evaluation Methods"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# RAG Evaluation Methods

## Overview

Comprehensive evaluation methods for RAG systems, including test set generation, evaluation pipelines, A/B testing, and production monitoring.

## When to Use

- Building comprehensive evaluation framework
- Setting up continuous evaluation
- Comparing different RAG configurations
- Generating test datasets
- Running A/B tests

## Test Set Generation

### Automatic Question Generation

```python
from typing import List, Dict
import random
from openai import OpenAI

client = OpenAI()

def generate_test_questions(
    documents: List[str],
    num_questions: int = 10,
    model: str = "gpt-4o"
) -> List[Dict[str, str]]:
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

        import json
        qa = json.loads(response.choices[0].message.content)
        qa["document"] = doc
        test_set.append(qa)

    return test_set

def generate_diverse_questions(
    documents: List[str],
    question_types: List[str] = ["factual", "comparative", "reasoning", "summarization"]
) -> List[Dict[str, str]]:
    """
    Generate diverse question types for comprehensive testing.
    """
    test_set = []

    for q_type in question_types:
        prompt = f"""Generate a {q_type} question based on the documents.

Documents:
{chr(10).join(documents[:3])}

Question type: {q_type}
- factual: Simple fact lookup
- comparative: Compare two things
- reasoning: Requires inference
- summarization: Summarize information

Return JSON with: question, expected_answer, type, difficulty"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        import json
        test_set.append(json.loads(response.choices[0].message.content))

    return test_set
```

### Manual Test Set Creation

```python
# Structure for manual test cases
test_cases = [
    {
        "id": "test_001",
        "question": "What is retrieval augmented generation?",
        "expected_answer": "RAG combines information retrieval with language generation...",
        "relevant_doc_ids": ["doc_42", "doc_103"],
        "difficulty": "easy",
        "category": "factual"
    },
    {
        "id": "test_002",
        "question": "Compare semantic search and keyword search",
        "expected_answer": "Semantic search understands meaning...",
        "relevant_doc_ids": ["doc_15", "doc_89"],
        "difficulty": "medium",
        "category": "comparative"
    }
]
```

## Evaluation Pipeline

### Complete Pipeline

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

@dataclass
class EvaluationResult:
    question: str
    answer: str
    context: List[str]
    ground_truth: Optional[str]
    retrieval_metrics: Dict[str, float]
    generation_metrics: Dict[str, float]
    timestamp: str

class RAGEvaluator:
    """Complete RAG evaluation pipeline."""

    def __init__(self, rag_pipeline, model: str = "gpt-4o"):
        self.rag = rag_pipeline
        self.model = model
        self.results: List[EvaluationResult] = []

    def evaluate_single(
        self,
        question: str,
        ground_truth: Optional[str] = None,
        relevant_doc_ids: Optional[Set[str]] = None
    ) -> EvaluationResult:
        """Evaluate single question."""
        # Get RAG response
        response = self.rag.query(question)

        # Extract components
        answer = response["answer"]
        contexts = [s["content"] for s in response["sources"]]
        retrieved_ids = [s["metadata"].get("id") for s in response["sources"]]

        # Retrieval metrics (from rag-eval-metrics.md)
        from rag_eval_metrics import precision_at_k, recall_at_k, mean_reciprocal_rank, hit_rate

        retrieval_metrics = {}
        if relevant_doc_ids:
            retrieval_metrics["precision@5"] = precision_at_k(retrieved_ids, relevant_doc_ids, 5)
            retrieval_metrics["recall@5"] = recall_at_k(retrieved_ids, relevant_doc_ids, 5)
            retrieval_metrics["mrr"] = mean_reciprocal_rank(retrieved_ids, relevant_doc_ids)
            retrieval_metrics["hit_rate"] = hit_rate(retrieved_ids, relevant_doc_ids)

        # Generation metrics
        from rag_eval_metrics import evaluate_faithfulness, evaluate_relevance, evaluate_context_relevance

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

    def evaluate_batch(
        self,
        test_set: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Evaluate batch of questions and compute aggregate metrics."""
        for item in test_set:
            self.evaluate_single(
                question=item["question"],
                ground_truth=item.get("answer"),
                relevant_doc_ids=item.get("relevant_docs")
            )

        return self.aggregate_metrics()

    def aggregate_metrics(self) -> Dict[str, float]:
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

# Usage
evaluator = RAGEvaluator(rag_pipeline)
results = evaluator.evaluate_batch(test_set)
evaluator.export_results("evaluation_results.json")
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
        test_questions: List[str],
        rag_a,  # RAG pipeline with config A
        rag_b   # RAG pipeline with config B
    ):
        """Run A/B test on both configurations."""
        for question in test_questions:
            # Test config A
            response_a = rag_a.query(question)
            eval_a = self._evaluate(question, response_a)
            self.results_a.append(eval_a)

            # Test config B
            response_b = rag_b.query(question)
            eval_b = self._evaluate(question, response_b)
            self.results_b.append(eval_b)

    def _evaluate(self, question: str, response: dict) -> dict:
        """Quick evaluation of single response."""
        return {
            "question": question,
            "answer": response["answer"],
            "latency": response.get("latency", 0),
            "num_sources": len(response.get("sources", []))
        }

    def compare_results(self) -> dict:
        """Compare results between configurations."""
        def avg_metric(results: List[dict], key: str) -> float:
            values = [r.get(key, 0) for r in results]
            return sum(values) / len(values) if values else 0

        return {
            "config_a": {
                "name": self.config_a.get("name", "Config A"),
                "avg_latency": avg_metric(self.results_a, "latency"),
                "total_questions": len(self.results_a)
            },
            "config_b": {
                "name": self.config_b.get("name", "Config B"),
                "avg_latency": avg_metric(self.results_b, "latency"),
                "total_questions": len(self.results_b)
            }
        }

# Example: Compare chunk sizes
config_a = {"name": "Chunk 500", "chunk_size": 500}
config_b = {"name": "Chunk 1000", "chunk_size": 1000}

ab_test = RAGABTest(config_a, config_b)
ab_test.run_test(test_questions, rag_pipeline_500, rag_pipeline_1000)
comparison = ab_test.compare_results()
```

## Production Monitoring

```python
class RAGMonitor:
    """Monitor RAG system in production."""

    def __init__(self):
        self.metrics = []

    def log_query(
        self,
        question: str,
        answer: str,
        latency: float,
        num_sources: int,
        user_feedback: Optional[str] = None
    ):
        """Log individual query metrics."""
        self.metrics.append({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "latency": latency,
            "num_sources": num_sources,
            "user_feedback": user_feedback
        })

    def get_summary(self, hours: int = 24) -> dict:
        """Get summary metrics for last N hours."""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = [
            m for m in self.metrics
            if datetime.fromisoformat(m["timestamp"]) > cutoff
        ]

        if not recent:
            return {}

        return {
            "total_queries": len(recent),
            "avg_latency": sum(m["latency"] for m in recent) / len(recent),
            "avg_sources": sum(m["num_sources"] for m in recent) / len(recent),
            "positive_feedback": sum(1 for m in recent if m["user_feedback"] == "positive"),
            "negative_feedback": sum(1 for m in recent if m["user_feedback"] == "negative")
        }

    def detect_anomalies(self) -> List[str]:
        """Detect anomalies in metrics."""
        anomalies = []
        recent = self.get_summary(hours=24)

        if recent.get("avg_latency", 0) > 5.0:
            anomalies.append("High latency detected")

        if recent.get("negative_feedback", 0) > 10:
            anomalies.append("Increased negative feedback")

        return anomalies
```

## Best Practices

### 1. Ground Truth Creation

- Manually verify ground truth answers
- Include diverse question types (factual, comparative, reasoning)
- Cover edge cases and ambiguous queries
- Update ground truth as system evolves

### 2. Evaluation Frequency

| Stage | Frequency | Metrics |
|-------|-----------|---------|
| **Development** | Every change | Precision@5, Faithfulness |
| **Pre-deployment** | Full test suite | All RAGAS metrics |
| **Production** | Real-time | Latency, Hit Rate, User feedback |
| **Weekly** | Batch evaluation | Full metrics on sample |

### 3. Human Evaluation

```python
def human_evaluation_interface(
    questions: List[str],
    answers: List[str],
    contexts: List[List[str]]
):
    """
    Interface for human evaluation.

    Guidelines:
    1. Is the answer factually correct? (Yes/No)
    2. Is the answer relevant to the question? (1-5 scale)
    3. Is the answer supported by context? (Yes/No/Partial)
    4. Overall quality (1-5 scale)
    """
    results = []
    for q, a, c in zip(questions, answers, contexts):
        print(f"\nQuestion: {q}")
        print(f"Answer: {a}")
        print(f"Context: {c[:200]}...")

        rating = {
            "factually_correct": input("Factually correct? (y/n): "),
            "relevance": int(input("Relevance (1-5): ")),
            "supported": input("Supported by context? (y/n/p): "),
            "overall": int(input("Overall quality (1-5): "))
        }
        results.append(rating)

    return results
```

### 4. Cost Management

```python
def cost_efficient_evaluation(
    test_set: List[dict],
    budget_dollars: float,
    cost_per_eval: float = 0.01
):
    """
    Evaluate within budget using smart sampling.
    """
    max_evals = int(budget_dollars / cost_per_eval)

    if len(test_set) <= max_evals:
        # Evaluate all
        return test_set

    # Sample strategically
    # 1. All high-priority cases
    high_priority = [t for t in test_set if t.get("priority") == "high"]

    # 2. Representative sample of others
    remaining = max_evals - len(high_priority)
    others = [t for t in test_set if t.get("priority") != "high"]
    import random
    sampled = random.sample(others, min(remaining, len(others)))

    return high_priority + sampled
```

## Common Pitfalls

1. **No Ground Truth** - Evaluating without knowing correct answers
2. **Non-representative Test Set** - Test questions don't match production
3. **Static Evaluation** - Not re-evaluating after changes
4. **Ignoring Latency** - Only measuring quality, not speed
5. **Evaluator Bias** - LLM evaluator may have biases
6. **No Human Validation** - Relying only on automated metrics

## References

- [RAGAS Documentation](https://docs.ragas.io/)
- [Evaluating RAG (LlamaIndex)](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/)
- [RAG Evaluation Best Practices](https://www.pinecone.io/learn/rag-evaluation/)

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

- [RAGAS Documentation](https://docs.ragas.io/)
- [LlamaIndex Evaluation](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/)
- [RAG Evaluation - Pinecone](https://www.pinecone.io/learn/rag-evaluation/)
- [LangChain Evaluation](https://python.langchain.com/docs/guides/evaluation/)
