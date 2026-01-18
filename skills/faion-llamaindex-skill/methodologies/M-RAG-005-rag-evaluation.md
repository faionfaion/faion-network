# M-RAG-005: RAG Evaluation

## Overview

RAG evaluation measures system quality across retrieval accuracy, answer correctness, and generation quality. Metrics include faithfulness, relevance, and groundedness. Both automated and human evaluation methods are essential.

**When to use:** Validating RAG systems, comparing configurations, continuous monitoring, and debugging retrieval/generation issues.

## Core Concepts

### 1. Evaluation Dimensions

| Dimension | Question | Metrics |
|-----------|----------|---------|
| **Retrieval Quality** | Did we find the right documents? | Recall, Precision, MRR, NDCG |
| **Context Relevance** | Is retrieved context useful? | Context Precision/Recall |
| **Faithfulness** | Is answer grounded in context? | Groundedness score |
| **Answer Relevance** | Does answer address query? | Semantic similarity |
| **Answer Correctness** | Is answer factually correct? | Human eval, fact-check |

### 2. Evaluation Flow

```
Query + Ground Truth
        ↓
    Retrieval → Retrieved Docs → Retrieval Metrics
        ↓
    Generation → Answer → Generation Metrics
        ↓
    Comparison → Final Scores
```

### 3. Common Frameworks

| Framework | Type | Best For |
|-----------|------|----------|
| **RAGAS** | Automated | Comprehensive RAG eval |
| **TruLens** | Automated | LLM-based scoring |
| **DeepEval** | Automated | Unit testing RAG |
| **LangSmith** | Platform | Production monitoring |
| **Human Eval** | Manual | Ground truth |

## Best Practices

### 1. Use Multiple Metrics

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

def evaluate_rag_system(test_cases: list) -> dict:
    """Comprehensive RAG evaluation."""

    results = evaluate(
        dataset=test_cases,
        metrics=[
            faithfulness,        # Is answer grounded in context?
            answer_relevancy,    # Does answer address the query?
            context_precision,   # Are retrieved docs relevant?
            context_recall       # Did we retrieve all relevant docs?
        ]
    )

    return {
        "faithfulness": results["faithfulness"],
        "answer_relevancy": results["answer_relevancy"],
        "context_precision": results["context_precision"],
        "context_recall": results["context_recall"],
        "overall": sum(results.values()) / len(results)
    }
```

### 2. Create Quality Test Sets

```python
def create_evaluation_dataset(documents: list, llm) -> list:
    """Generate test cases from documents."""

    test_cases = []

    for doc in documents:
        # Generate questions from document
        questions = llm.invoke(f"""
        Generate 3 questions that can be answered using this document:

        Document: {doc.text}

        For each question, also provide:
        1. The expected answer
        2. The relevant passage that contains the answer

        Format as JSON array.
        """)

        for q in json.loads(questions):
            test_cases.append({
                "question": q["question"],
                "ground_truth": q["answer"],
                "ground_truth_context": q["relevant_passage"],
                "source_doc_id": doc.id
            })

    return test_cases

# Example test case structure
test_case = {
    "question": "What is the maximum context length for GPT-4?",
    "ground_truth": "128,000 tokens",
    "ground_truth_context": "GPT-4 supports a context window of 128K tokens",
    "source_doc_id": "openai_docs_123"
}
```

### 3. Evaluate Component by Component

```python
class RAGEvaluator:
    def __init__(self, retriever, generator, evaluator_llm):
        self.retriever = retriever
        self.generator = generator
        self.llm = evaluator_llm

    def evaluate_retrieval(self, query: str, expected_docs: list) -> dict:
        """Evaluate retrieval independently."""

        retrieved = self.retriever.retrieve(query)
        retrieved_ids = set(doc.id for doc in retrieved)
        expected_ids = set(expected_docs)

        precision = len(retrieved_ids & expected_ids) / len(retrieved_ids)
        recall = len(retrieved_ids & expected_ids) / len(expected_ids)

        return {
            "precision": precision,
            "recall": recall,
            "f1": 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
        }

    def evaluate_generation(
        self,
        query: str,
        context: str,
        answer: str,
        ground_truth: str
    ) -> dict:
        """Evaluate generation independently."""

        # Faithfulness: Is answer grounded in context?
        faithfulness = self._check_faithfulness(answer, context)

        # Relevance: Does answer address query?
        relevance = self._check_relevance(answer, query)

        # Correctness: Does answer match ground truth?
        correctness = self._check_correctness(answer, ground_truth)

        return {
            "faithfulness": faithfulness,
            "relevance": relevance,
            "correctness": correctness
        }

    def _check_faithfulness(self, answer: str, context: str) -> float:
        """Check if answer is supported by context."""

        prompt = f"""
        Given the following context and answer, evaluate if the answer
        is fully supported by the context.

        Context: {context}

        Answer: {answer}

        Score from 0 to 1, where:
        - 1.0: Fully supported by context
        - 0.5: Partially supported
        - 0.0: Not supported / contradicts context

        Return only the numeric score.
        """

        score = float(self.llm.invoke(prompt))
        return score
```

## Common Patterns

### Pattern 1: RAGAS Evaluation

```python
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_correctness
)

def ragas_evaluate(rag_system, test_cases: list) -> dict:
    """Evaluate using RAGAS framework."""

    # Run RAG system on test cases
    results = []
    for case in test_cases:
        retrieved = rag_system.retrieve(case["question"])
        answer = rag_system.generate(case["question"], retrieved)

        results.append({
            "question": case["question"],
            "answer": answer,
            "contexts": [doc.text for doc in retrieved],
            "ground_truth": case["ground_truth"]
        })

    # Create dataset
    dataset = Dataset.from_list(results)

    # Evaluate
    scores = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
            answer_correctness
        ]
    )

    return scores.to_pandas()
```

### Pattern 2: Custom Faithfulness Check

```python
def check_faithfulness_detailed(
    answer: str,
    context: str,
    llm
) -> dict:
    """Detailed faithfulness evaluation."""

    # Extract claims from answer
    claims_prompt = f"""
    Extract all factual claims from this answer as a JSON array:

    Answer: {answer}

    Return format: ["claim 1", "claim 2", ...]
    """
    claims = json.loads(llm.invoke(claims_prompt))

    # Check each claim against context
    supported_claims = []
    unsupported_claims = []

    for claim in claims:
        check_prompt = f"""
        Is this claim supported by the context?

        Claim: {claim}

        Context: {context}

        Answer: "supported" or "not_supported" with brief reason.
        Return as JSON: {{"verdict": "...", "reason": "..."}}
        """

        result = json.loads(llm.invoke(check_prompt))

        if result["verdict"] == "supported":
            supported_claims.append({"claim": claim, "reason": result["reason"]})
        else:
            unsupported_claims.append({"claim": claim, "reason": result["reason"]})

    return {
        "faithfulness_score": len(supported_claims) / len(claims) if claims else 1.0,
        "total_claims": len(claims),
        "supported_claims": supported_claims,
        "unsupported_claims": unsupported_claims
    }
```

### Pattern 3: Retrieval Quality Metrics

```python
import numpy as np

def calculate_retrieval_metrics(
    retrieved_docs: list,
    relevant_docs: set,
    k_values: list = [1, 3, 5, 10]
) -> dict:
    """Calculate comprehensive retrieval metrics."""

    metrics = {}
    retrieved_ids = [doc.id for doc in retrieved_docs]

    # Precision@k and Recall@k
    for k in k_values:
        top_k_ids = set(retrieved_ids[:k])
        precision_k = len(top_k_ids & relevant_docs) / k
        recall_k = len(top_k_ids & relevant_docs) / len(relevant_docs)

        metrics[f"precision@{k}"] = precision_k
        metrics[f"recall@{k}"] = recall_k

    # Mean Reciprocal Rank
    mrr = 0
    for rank, doc_id in enumerate(retrieved_ids, 1):
        if doc_id in relevant_docs:
            mrr = 1 / rank
            break
    metrics["mrr"] = mrr

    # NDCG@k
    for k in k_values:
        dcg = sum(
            1 / np.log2(i + 2)  # i+2 because log2(1) = 0
            for i, doc_id in enumerate(retrieved_ids[:k])
            if doc_id in relevant_docs
        )
        ideal_dcg = sum(1 / np.log2(i + 2) for i in range(min(k, len(relevant_docs))))
        ndcg = dcg / ideal_dcg if ideal_dcg > 0 else 0
        metrics[f"ndcg@{k}"] = ndcg

    return metrics
```

### Pattern 4: End-to-End Evaluation

```python
class E2EEvaluator:
    def __init__(self, rag_system, test_set_path: str):
        self.rag = rag_system
        self.test_set = load_test_set(test_set_path)

    def run_evaluation(self) -> dict:
        """Run full evaluation suite."""

        all_results = []

        for case in self.test_set:
            # Run RAG pipeline
            start_time = time.time()
            response = self.rag.query(case["question"])
            latency = time.time() - start_time

            # Collect metrics
            result = {
                "question": case["question"],
                "answer": response.answer,
                "latency_ms": latency * 1000,
                "num_docs_retrieved": len(response.retrieved_docs),
                "retrieval_scores": [d.score for d in response.retrieved_docs]
            }

            # Quality metrics
            if "ground_truth" in case:
                result["correctness"] = self._score_correctness(
                    response.answer, case["ground_truth"]
                )

            if "relevant_doc_ids" in case:
                result["retrieval_metrics"] = calculate_retrieval_metrics(
                    response.retrieved_docs,
                    set(case["relevant_doc_ids"])
                )

            all_results.append(result)

        return self._aggregate_results(all_results)

    def _aggregate_results(self, results: list) -> dict:
        """Aggregate individual results into summary."""

        return {
            "num_evaluated": len(results),
            "avg_latency_ms": np.mean([r["latency_ms"] for r in results]),
            "avg_correctness": np.mean([r.get("correctness", 0) for r in results]),
            "avg_precision@5": np.mean([
                r["retrieval_metrics"]["precision@5"]
                for r in results if "retrieval_metrics" in r
            ]),
            "avg_mrr": np.mean([
                r["retrieval_metrics"]["mrr"]
                for r in results if "retrieval_metrics" in r
            ])
        }
```

### Pattern 5: Human Evaluation Framework

```python
class HumanEvalTask:
    """Generate human evaluation tasks."""

    def __init__(self, rag_system, sample_size: int = 100):
        self.rag = rag_system
        self.sample_size = sample_size

    def generate_eval_tasks(self, queries: list) -> list:
        """Create tasks for human evaluators."""

        tasks = []

        for query in random.sample(queries, self.sample_size):
            response = self.rag.query(query)

            task = {
                "task_id": generate_id(),
                "query": query,
                "answer": response.answer,
                "context_shown": response.retrieved_docs[:3],
                "questions": [
                    {
                        "id": "relevance",
                        "text": "Does the answer address the question?",
                        "scale": "1-5"
                    },
                    {
                        "id": "accuracy",
                        "text": "Is the information in the answer correct?",
                        "scale": "1-5"
                    },
                    {
                        "id": "grounded",
                        "text": "Is the answer supported by the provided context?",
                        "scale": "yes/no/partial"
                    },
                    {
                        "id": "helpfulness",
                        "text": "Would this answer be helpful to the user?",
                        "scale": "1-5"
                    }
                ]
            }
            tasks.append(task)

        return tasks

    def analyze_human_results(self, completed_tasks: list) -> dict:
        """Analyze human evaluation results."""

        scores = {
            "relevance": [],
            "accuracy": [],
            "grounded": {"yes": 0, "no": 0, "partial": 0},
            "helpfulness": []
        }

        for task in completed_tasks:
            for response in task["responses"]:
                scores["relevance"].append(response["relevance"])
                scores["accuracy"].append(response["accuracy"])
                scores["grounded"][response["grounded"]] += 1
                scores["helpfulness"].append(response["helpfulness"])

        return {
            "avg_relevance": np.mean(scores["relevance"]),
            "avg_accuracy": np.mean(scores["accuracy"]),
            "grounded_pct": scores["grounded"]["yes"] / len(completed_tasks),
            "avg_helpfulness": np.mean(scores["helpfulness"])
        }
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Single metric | Incomplete picture | Use multiple dimensions |
| No ground truth | Can't measure correctness | Create evaluation dataset |
| Ignoring retrieval | Hidden issues | Evaluate components separately |
| Only automated | Misses nuance | Add human evaluation |
| Static test set | Overfitting | Refresh periodically |

## Tools & References

### Related Skills
- faion-llamaindex-skill
- faion-langchain-skill

### Related Agents
- faion-rag-agent

### External Resources
- [RAGAS](https://docs.ragas.io/)
- [TruLens](https://www.trulens.org/)
- [DeepEval](https://github.com/confident-ai/deepeval)
- [LangSmith Evaluation](https://docs.smith.langchain.com/evaluation)

## Checklist

- [ ] Created evaluation dataset with ground truth
- [ ] Implemented retrieval metrics (MRR, NDCG)
- [ ] Added faithfulness evaluation
- [ ] Set up answer relevance scoring
- [ ] Configured correctness checking
- [ ] Established human evaluation process
- [ ] Created continuous monitoring
- [ ] Documented baseline metrics
- [ ] Set up regression testing
- [ ] Defined quality thresholds

---

*Methodology: M-RAG-005 | Category: RAG/Vector DB*
*Related: faion-rag-agent, faion-llamaindex-skill*
