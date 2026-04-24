---
id: chain-of-thought-techniques
name: "Chain-of-Thought Advanced Techniques"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
parent: chain-of-thought
---

# Chain-of-Thought Advanced Techniques

## Overview

Advanced Chain-of-Thought techniques for complex reasoning: Tree of Thoughts (ToT), Least-to-Most decomposition, domain-specific CoT patterns, and production services.

## Tree of Thoughts

```python
from typing import List, Dict
import json

class TreeOfThoughts:
    """
    Explore multiple reasoning paths and evaluate them.
    """

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def solve(
        self,
        problem: str,
        num_branches: int = 3,
        max_depth: int = 3
    ) -> Dict:
        """Solve problem using tree of thoughts."""
        # Generate initial thoughts
        initial_thoughts = self._generate_thoughts(problem, num_branches)

        # Evaluate and select best thoughts
        evaluated = self._evaluate_thoughts(problem, initial_thoughts)

        # Expand best thought
        best_thought = max(evaluated, key=lambda x: x["score"])

        # Continue reasoning from best thought
        final_answer = self._complete_reasoning(problem, best_thought["thought"])

        return {
            "problem": problem,
            "explored_thoughts": evaluated,
            "selected_path": best_thought,
            "final_answer": final_answer
        }

    def _generate_thoughts(self, problem: str, num_thoughts: int) -> List[str]:
        """Generate initial reasoning approaches."""
        prompt = f"""Problem: {problem}

Generate {num_thoughts} different approaches to solve this problem.
Each approach should be a first step in the reasoning process.
Format: Return JSON array of strings."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result.get("approaches", [])

    def _evaluate_thoughts(
        self,
        problem: str,
        thoughts: List[str]
    ) -> List[Dict]:
        """Evaluate how promising each thought is."""
        evaluated = []

        for thought in thoughts:
            prompt = f"""Problem: {problem}

Proposed first step: {thought}

Evaluate this approach on a scale of 1-10:
- Is it relevant to the problem?
- Does it lead toward a solution?
- Is it logically sound?

Return JSON: {{"score": N, "reason": "..."}}"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            evaluated.append({
                "thought": thought,
                "score": result.get("score", 0),
                "reason": result.get("reason", "")
            })

        return evaluated

    def _complete_reasoning(self, problem: str, starting_thought: str) -> str:
        """Complete the reasoning from a starting point."""
        prompt = f"""Problem: {problem}

Starting approach: {starting_thought}

Continue this reasoning to reach the final answer.
Show each step clearly and end with the final answer."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
```

## Least-to-Most Prompting

```python
def least_to_most(
    client,
    problem: str,
    model: str = "gpt-4o"
) -> Dict:
    """
    Decompose into subproblems and solve from simplest to most complex.
    """
    # Step 1: Decompose the problem
    decompose_prompt = f"""Problem: {problem}

Break this problem down into simpler subproblems.
List them from simplest to most complex.
Return JSON: {{"subproblems": ["...", "..."]}}"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": decompose_prompt}],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    subproblems = result.get("subproblems", [])

    # Step 2: Solve each subproblem
    solutions = []
    context = ""

    for subproblem in subproblems:
        solve_prompt = f"""Original problem: {problem}

Previous solutions:
{context}

Current subproblem: {subproblem}

Solve this subproblem step by step."""

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": solve_prompt}]
        )

        solution = response.choices[0].message.content
        solutions.append({
            "subproblem": subproblem,
            "solution": solution
        })

        context += f"\nSubproblem: {subproblem}\nSolution: {solution}\n"

    # Step 3: Synthesize final answer
    synthesize_prompt = f"""Original problem: {problem}

Subproblem solutions:
{context}

Using all the above solutions, provide the final answer to the original problem."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": synthesize_prompt}]
    )

    return {
        "problem": problem,
        "subproblems": solutions,
        "final_answer": response.choices[0].message.content
    }
```

## Domain-Specific CoT

### Code Debugging

```python
def code_debugging_cot(
    client,
    code: str,
    error: str,
    model: str = "gpt-4o"
) -> str:
    """Chain-of-thought for debugging code."""
    prompt = f"""Debug this code that produces an error.

Code:
```
{code}
```

Error:
```
{error}
```

Analyze step by step:
1. What does the code intend to do?
2. Where exactly does the error occur?
3. What is the root cause?
4. What is the fix?

Then provide the corrected code."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
```

### Decision Making

```python
def decision_making_cot(
    client,
    decision: str,
    options: List[str],
    criteria: List[str],
    model: str = "gpt-4o"
) -> str:
    """Chain-of-thought for decision making."""
    options_text = "\n".join([f"- {opt}" for opt in options])
    criteria_text = "\n".join([f"- {crit}" for crit in criteria])

    prompt = f"""Help make this decision:

Decision: {decision}

Options:
{options_text}

Evaluation criteria:
{criteria_text}

Analyze step by step:
1. List pros and cons for each option
2. Evaluate each option against each criterion
3. Identify potential risks and mitigations
4. Consider trade-offs
5. Make a recommendation with reasoning

Provide a structured analysis and final recommendation."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
```

### Math Problems

```python
def math_problem_cot(
    client,
    problem: str,
    model: str = "gpt-4o"
) -> Dict:
    """Structured math problem solving."""
    prompt = f"""Solve this math problem with detailed steps:

{problem}

Follow this structure:
1. **Given**: What information is provided?
2. **Find**: What are we solving for?
3. **Approach**: What method will we use?
4. **Solution**: Step-by-step calculation
5. **Verification**: Check the answer
6. **Answer**: Final answer with units

Return your analysis in JSON format with these sections."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
```

## Production CoT Service

```python
from dataclasses import dataclass
from typing import Optional, Callable
from enum import Enum
import logging

class CoTStrategy(Enum):
    ZERO_SHOT = "zero_shot"
    FEW_SHOT = "few_shot"
    SELF_CONSISTENCY = "self_consistency"
    TREE_OF_THOUGHTS = "tree_of_thoughts"
    LEAST_TO_MOST = "least_to_most"

@dataclass
class CoTConfig:
    strategy: CoTStrategy = CoTStrategy.ZERO_SHOT
    num_samples: int = 5  # For self-consistency
    temperature: float = 0.7
    examples: list = None  # For few-shot

class ChainOfThoughtService:
    """Production CoT reasoning service."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model
        self.logger = logging.getLogger(__name__)

    def reason(
        self,
        problem: str,
        config: Optional[CoTConfig] = None
    ) -> Dict:
        """Apply chain-of-thought reasoning to a problem."""
        config = config or CoTConfig()

        try:
            if config.strategy == CoTStrategy.ZERO_SHOT:
                result = self._zero_shot(problem)
            elif config.strategy == CoTStrategy.FEW_SHOT:
                result = self._few_shot(problem, config.examples or [])
            elif config.strategy == CoTStrategy.SELF_CONSISTENCY:
                result = self._self_consistency(problem, config.num_samples, config.temperature)
            elif config.strategy == CoTStrategy.TREE_OF_THOUGHTS:
                tot = TreeOfThoughts(self.client, self.model)
                result = tot.solve(problem)
            elif config.strategy == CoTStrategy.LEAST_TO_MOST:
                result = least_to_most(self.client, problem, self.model)
            else:
                result = self._zero_shot(problem)

            return {
                "success": True,
                "strategy": config.strategy.value,
                "result": result
            }

        except Exception as e:
            self.logger.error(f"CoT reasoning failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _zero_shot(self, problem: str) -> str:
        """Zero-shot CoT."""
        # Import from cot-basics.md implementation
        pass

    def _few_shot(self, problem: str, examples: list) -> str:
        """Few-shot CoT."""
        # Import from cot-basics.md implementation
        pass

    def _self_consistency(
        self,
        problem: str,
        num_samples: int,
        temperature: float
    ) -> Dict:
        """Self-consistency CoT."""
        # Import from cot-basics.md implementation
        pass
```

## Best Practices

1. **Handle Complexity**
   - Decompose complex problems
   - Use tree of thoughts for branching logic
   - Apply least-to-most for sequential dependencies

2. **Optimize Performance**
   - Cache intermediate results
   - Parallelize independent paths (ToT)
   - Set depth limits to prevent infinite exploration

3. **Error Handling**
   - Validate generated thoughts
   - Handle malformed JSON responses
   - Fallback to simpler strategies on failure

## Common Pitfalls

1. **Overly Complex** - Using ToT when zero-shot suffices
2. **No Depth Limits** - ToT exploration without bounds
3. **Ignoring Context** - Not using previous solutions in decomposition
4. **Poor Evaluation** - Weak thought evaluation criteria

## References

- [Tree of Thoughts Paper](https://arxiv.org/abs/2305.10601)
- [Least-to-Most Paper](https://arxiv.org/abs/2205.10625)

## See Also

- [cot-basics.md](cot-basics.md) - Basic CoT techniques (zero-shot, few-shot, self-consistency)
- [prompt-engineering.md](prompt-engineering.md) - General prompt engineering patterns

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Self-consistency prompting | sonnet | Advanced technique |
| Tree-of-thought implementation | opus | Novel pattern |
