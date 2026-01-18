# M-LLM-007: LLM Evaluation

## Overview

LLM evaluation measures model performance across various dimensions: accuracy, relevance, safety, and task-specific metrics. Methods include automated benchmarks, human evaluation, and A/B testing. Essential for model selection and continuous improvement.

**When to use:** Choosing models, validating prompts, measuring improvements, and ensuring quality in production.

## Core Concepts

### 1. Evaluation Dimensions

| Dimension | Description | Metrics |
|-----------|-------------|---------|
| **Accuracy** | Correctness of outputs | Precision, Recall, F1 |
| **Relevance** | Match to user intent | BLEU, ROUGE, BERTScore |
| **Fluency** | Natural language quality | Perplexity, human rating |
| **Safety** | Harmful content avoidance | Toxicity score, refusal rate |
| **Consistency** | Same input = similar output | Semantic similarity |
| **Latency** | Response time | TTFT, total time |
| **Cost** | Token efficiency | $/request, tokens/answer |

### 2. Evaluation Types

| Type | Speed | Cost | Best For |
|------|-------|------|----------|
| **Automated metrics** | Fast | Low | Initial screening |
| **LLM-as-judge** | Medium | Medium | Quality assessment |
| **Human evaluation** | Slow | High | Final validation |
| **A/B testing** | Slow | Medium | Production decisions |

### 3. Common Benchmarks

| Benchmark | Measures | Use Case |
|-----------|----------|----------|
| MMLU | Knowledge breadth | General capability |
| HumanEval | Code generation | Coding tasks |
| GSM8K | Math reasoning | Quantitative tasks |
| TruthfulQA | Truthfulness | Factual accuracy |
| MT-Bench | Multi-turn chat | Conversation quality |
| AlpacaEval | Instruction following | Assistant quality |

## Best Practices

### 1. Define Clear Criteria

```python
evaluation_criteria = {
    "factual_accuracy": {
        "description": "Response is factually correct",
        "scoring": "1-5 scale",
        "guidelines": """
        5: All facts verified and correct
        4: Minor factual issues
        3: Some facts incorrect but core message right
        2: Major factual errors
        1: Mostly or entirely incorrect
        """
    },
    "helpfulness": {
        "description": "Response addresses user's need",
        "scoring": "1-5 scale",
        "guidelines": """
        5: Fully addresses query with actionable info
        4: Mostly helpful, minor gaps
        3: Partially helpful
        2: Mostly unhelpful
        1: Completely misses the point
        """
    },
    "safety": {
        "description": "Response is safe and appropriate",
        "scoring": "pass/fail",
        "guidelines": """
        Pass: No harmful, biased, or inappropriate content
        Fail: Contains problematic content
        """
    }
}
```

### 2. Create Diverse Test Sets

```python
test_set = {
    "categories": {
        "easy": [
            {"input": "What is 2+2?", "expected": "4"},
            {"input": "Capital of France?", "expected": "Paris"}
        ],
        "medium": [
            {"input": "Explain quantum entanglement simply",
             "criteria": ["accurate", "accessible"]},
            {"input": "Write a haiku about coding",
             "criteria": ["5-7-5 syllables", "relevant theme"]}
        ],
        "hard": [
            {"input": "Analyze the economic implications of AI on labor markets",
             "criteria": ["balanced", "cited sources", "nuanced"]},
            {"input": "Debug this code: [complex code snippet]",
             "criteria": ["correct fix", "explanation", "prevention tips"]}
        ],
        "edge_cases": [
            {"input": "", "expected": "Appropriate handling of empty input"},
            {"input": "[very long input]", "expected": "Handles gracefully"},
            {"input": "[adversarial prompt]", "expected": "Refuses appropriately"}
        ]
    }
}
```

### 3. Use LLM-as-Judge

```python
def llm_judge(response: str, criteria: dict) -> dict:
    """Use GPT-4 to evaluate response quality."""

    judge_prompt = """
    Evaluate this AI response against the given criteria.

    Response to evaluate:
    {response}

    Evaluation criteria:
    {criteria}

    For each criterion, provide:
    1. Score (1-5)
    2. Justification (1-2 sentences)

    Respond in JSON format:
    {{
        "scores": {{
            "criterion_name": {{
                "score": <1-5>,
                "justification": "..."
            }}
        }},
        "overall_score": <1-5>,
        "summary": "..."
    }}
    """

    result = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert AI evaluator."},
            {"role": "user", "content": judge_prompt.format(
                response=response,
                criteria=json.dumps(criteria)
            )}
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(result.choices[0].message.content)
```

## Common Patterns

### Pattern 1: Automated Metrics

```python
from evaluate import load
from bert_score import score as bert_score

def compute_metrics(predictions: list, references: list) -> dict:
    """Compute automated text quality metrics."""

    # BLEU - n-gram overlap
    bleu = load("bleu")
    bleu_score = bleu.compute(predictions=predictions, references=references)

    # ROUGE - recall-oriented
    rouge = load("rouge")
    rouge_score = rouge.compute(predictions=predictions, references=references)

    # BERTScore - semantic similarity
    P, R, F1 = bert_score(predictions, references, lang="en")

    return {
        "bleu": bleu_score["bleu"],
        "rouge1": rouge_score["rouge1"],
        "rouge2": rouge_score["rouge2"],
        "rougeL": rouge_score["rougeL"],
        "bertscore_precision": P.mean().item(),
        "bertscore_recall": R.mean().item(),
        "bertscore_f1": F1.mean().item()
    }
```

### Pattern 2: Pairwise Comparison

```python
def pairwise_compare(model_a: str, model_b: str, test_cases: list) -> dict:
    """Compare two models using pairwise evaluation."""

    results = {"model_a_wins": 0, "model_b_wins": 0, "ties": 0}

    for case in test_cases:
        response_a = call_model(model_a, case["input"])
        response_b = call_model(model_b, case["input"])

        # Randomize order to avoid position bias
        if random.random() > 0.5:
            first, second = response_a, response_b
            first_label, second_label = "A", "B"
        else:
            first, second = response_b, response_a
            first_label, second_label = "B", "A"

        # Judge comparison
        judgment = llm.invoke(f"""
        Compare these two responses to the query: "{case['input']}"

        Response 1: {first}

        Response 2: {second}

        Which response is better? Answer: "1", "2", or "tie"
        Explain briefly.
        """)

        winner = parse_winner(judgment)
        if winner == "1":
            results[f"model_{first_label.lower()}_wins"] += 1
        elif winner == "2":
            results[f"model_{second_label.lower()}_wins"] += 1
        else:
            results["ties"] += 1

    return results
```

### Pattern 3: A/B Testing Framework

```python
class ABTestFramework:
    def __init__(self, variants: dict, traffic_split: dict = None):
        self.variants = variants  # {"control": model_a, "treatment": model_b}
        self.traffic_split = traffic_split or {"control": 0.5, "treatment": 0.5}
        self.results = {v: {"requests": 0, "scores": []} for v in variants}

    def route_request(self, request_id: str) -> str:
        """Deterministically route request to variant."""
        hash_val = hash(request_id) % 100
        cumulative = 0
        for variant, split in self.traffic_split.items():
            cumulative += split * 100
            if hash_val < cumulative:
                return variant
        return list(self.variants.keys())[-1]

    def record_result(self, variant: str, score: float, metadata: dict = None):
        self.results[variant]["requests"] += 1
        self.results[variant]["scores"].append(score)

    def analyze(self) -> dict:
        """Analyze A/B test results with statistical significance."""
        from scipy import stats

        control_scores = self.results["control"]["scores"]
        treatment_scores = self.results["treatment"]["scores"]

        # T-test for significance
        t_stat, p_value = stats.ttest_ind(control_scores, treatment_scores)

        return {
            "control_mean": np.mean(control_scores),
            "treatment_mean": np.mean(treatment_scores),
            "lift": (np.mean(treatment_scores) - np.mean(control_scores)) / np.mean(control_scores),
            "p_value": p_value,
            "significant": p_value < 0.05,
            "control_n": len(control_scores),
            "treatment_n": len(treatment_scores)
        }
```

### Pattern 4: Regression Testing

```python
class LLMRegressionSuite:
    def __init__(self, golden_set_path: str):
        self.golden_set = load_golden_set(golden_set_path)
        self.thresholds = {
            "accuracy": 0.95,
            "similarity": 0.85,
            "latency_p99": 5000  # ms
        }

    def run_regression(self, model: str) -> dict:
        """Run regression tests against golden set."""

        results = {
            "passed": 0,
            "failed": 0,
            "failures": []
        }

        for case in self.golden_set:
            response = call_model(model, case["input"])

            # Check against expected output
            similarity = compute_similarity(response, case["expected"])
            latency = get_latency()

            passed = (
                similarity >= self.thresholds["similarity"] and
                latency <= self.thresholds["latency_p99"]
            )

            if passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
                results["failures"].append({
                    "case_id": case["id"],
                    "input": case["input"],
                    "expected": case["expected"],
                    "actual": response,
                    "similarity": similarity,
                    "latency": latency
                })

        results["pass_rate"] = results["passed"] / len(self.golden_set)
        results["regression_detected"] = results["pass_rate"] < self.thresholds["accuracy"]

        return results
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Single metric | Incomplete picture | Use multiple metrics |
| No human baseline | Can't interpret scores | Include human eval |
| Static test set | Overfitting | Refresh regularly |
| Ignoring edge cases | Production failures | Include adversarial tests |
| No statistical significance | False conclusions | Calculate p-values |

## Tools & References

### Related Skills
- faion-openai-api-skill
- faion-claude-api-skill

### Related Agents
- faion-prompt-engineer-agent

### External Resources
- [Hugging Face Evaluate](https://huggingface.co/docs/evaluate)
- [LangSmith Evaluation](https://docs.smith.langchain.com/evaluation)
- [OpenAI Evals](https://github.com/openai/evals)
- [LMSYS Chatbot Arena](https://chat.lmsys.org/)

## Checklist

- [ ] Defined evaluation criteria
- [ ] Created diverse test set
- [ ] Included edge cases
- [ ] Set up automated metrics
- [ ] Implemented LLM-as-judge
- [ ] Added human evaluation option
- [ ] Created regression suite
- [ ] Calculated statistical significance
- [ ] Set up continuous monitoring
- [ ] Documented baselines

---

*Methodology: M-LLM-007 | Category: LLM/Orchestration*
*Related: faion-prompt-engineer-agent, faion-openai-api-skill*
