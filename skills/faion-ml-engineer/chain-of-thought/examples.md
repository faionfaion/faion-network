# Chain-of-Thought Examples

Real-world examples, patterns, and code implementations for CoT techniques.

## Table of Contents

1. [Zero-Shot CoT Examples](#zero-shot-cot-examples)
2. [Few-Shot CoT Examples](#few-shot-cot-examples)
3. [Self-Consistency Examples](#self-consistency-examples)
4. [Tree-of-Thoughts Examples](#tree-of-thoughts-examples)
5. [Least-to-Most Examples](#least-to-most-examples)
6. [Domain-Specific CoT](#domain-specific-cot)
7. [Production Patterns](#production-patterns)
8. [Anti-Patterns](#anti-patterns)

---

## Zero-Shot CoT Examples

### Basic Math Problem

**Prompt:**
```
A store sells notebooks for $3.50 each. If you buy 5 or more, you get 20% off.
You need to buy 7 notebooks. How much will you pay?

Let's think step by step.

<thinking>
[Work through the problem]
</thinking>

<answer>
[Final answer with units]
</answer>
```

**Expected Output:**
```xml
<thinking>
1. Base price per notebook: $3.50
2. Quantity needed: 7 notebooks
3. Check discount eligibility: 7 >= 5, so 20% discount applies
4. Calculate subtotal without discount: 7 * $3.50 = $24.50
5. Calculate discount amount: $24.50 * 0.20 = $4.90
6. Calculate final price: $24.50 - $4.90 = $19.60
</thinking>

<answer>
$19.60
</answer>
```

### Logical Reasoning

**Prompt:**
```
All roses are flowers. Some flowers fade quickly. Can we conclude that some roses fade quickly?

Think through this step by step, analyzing the logical structure.

<thinking>
[Analyze the logic]
</thinking>

<answer>
[Yes/No with brief explanation]
</answer>
```

**Expected Output:**
```xml
<thinking>
1. Premise 1: All roses are flowers (Roses ⊆ Flowers)
2. Premise 2: Some flowers fade quickly (∃ flowers that fade quickly)
3. Question: Do some roses fade quickly?
4. Analysis: The "some flowers" that fade quickly might be non-rose flowers
5. We cannot determine if the quick-fading flowers include any roses
6. This is a logical fallacy: affirming the consequent with "some"
</thinking>

<answer>
No. We cannot conclude this. While all roses are flowers, the flowers that fade quickly might be entirely non-rose flowers (like daisies or tulips). The premises don't guarantee any overlap between roses and quick-fading flowers.
</answer>
```

### Code Debugging

**Prompt:**
```python
Debug this code that should find the second largest number:

def second_largest(numbers):
    largest = numbers[0]
    second = numbers[0]
    for n in numbers:
        if n > largest:
            largest = n
        elif n > second:
            second = n
    return second

# Test: second_largest([5, 2, 8, 1, 9]) should return 8, but returns 5

Let's analyze step by step to find the bug.
```

**Expected Output:**
```xml
<thinking>
1. Trace through with [5, 2, 8, 1, 9]:
   - Initial: largest=5, second=5
   - n=5: neither condition true, skip
   - n=2: 2<5, 2<5, skip
   - n=8: 8>5, so largest=8, second still 5
   - n=1: 1<8, 1<5, skip
   - n=9: 9>8, so largest=9, second still 5

2. The bug: When we find a new largest, we don't update second to the old largest

3. Fix: Before updating largest, save its value to second
</thinking>

<answer>
Bug: When finding a new largest, the old largest should become second, but it's not being updated.

Fixed code:
```python
def second_largest(numbers):
    largest = numbers[0]
    second = float('-inf')  # Handle case where all numbers are same
    for n in numbers:
        if n > largest:
            second = largest  # Save old largest
            largest = n
        elif n > second and n != largest:  # Also handle duplicates
            second = n
    return second
```
</answer>
```

---

## Few-Shot CoT Examples

### Sentiment Analysis with Reasoning

**Prompt:**
```
Analyze the sentiment and explain your reasoning.

Example 1:
Text: "The product arrived on time but the quality was disappointing."
<thinking>
- Positive aspect: arrived on time (delivery was good)
- Negative aspect: quality was disappointing (core product issue)
- Weight: Quality issues outweigh delivery success for product satisfaction
</thinking>
<answer>negative</answer>

Example 2:
Text: "Not bad for the price, exceeded my low expectations."
<thinking>
- "Not bad" = mild positive
- "exceeded expectations" = positive
- "low expectations" = customer wasn't expecting much
- Overall: Pleasantly surprised, positive experience
</thinking>
<answer>positive</answer>

Example 3:
Text: "It works. Nothing special, nothing wrong."
<thinking>
- "It works" = functional, neutral
- "Nothing special" = no positive standouts
- "Nothing wrong" = no negatives either
- Perfectly balanced, pure utility statement
</thinking>
<answer>neutral</answer>

Now analyze:
Text: "{user_text}"
```

### Math Word Problems

**Prompt:**
```
Solve the math problem showing your work.

Example 1:
Problem: A train travels 120 miles in 2 hours. How long to travel 300 miles at the same speed?
<thinking>
1. Find speed: 120 miles / 2 hours = 60 mph
2. Time for 300 miles: 300 miles / 60 mph = 5 hours
</thinking>
<answer>5 hours</answer>

Example 2:
Problem: If 3 workers can paint a house in 6 days, how many days for 9 workers?
<thinking>
1. Total work: 3 workers * 6 days = 18 worker-days
2. With 9 workers: 18 worker-days / 9 workers = 2 days
</thinking>
<answer>2 days</answer>

Now solve:
Problem: {problem}
```

---

## Self-Consistency Examples

### Python Implementation

```python
from typing import List, Dict, Any
from collections import Counter
import json

class SelfConsistencyReasoner:
    """Self-consistency CoT with majority voting."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def solve(
        self,
        problem: str,
        num_samples: int = 5,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Solve with self-consistency."""

        prompt = f"""Solve this problem step by step.

Problem: {problem}

<thinking>
[Your reasoning steps]
</thinking>

<answer>
[Final answer only - be concise]
</answer>"""

        # Generate multiple reasoning paths
        responses = []
        for _ in range(num_samples):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            responses.append(response.choices[0].message.content)

        # Extract answers
        answers = []
        reasoning_paths = []
        for resp in responses:
            answer = self._extract_answer(resp)
            reasoning = self._extract_thinking(resp)
            answers.append(answer)
            reasoning_paths.append(reasoning)

        # Majority vote
        answer_counts = Counter(answers)
        most_common = answer_counts.most_common(1)[0]
        final_answer = most_common[0]
        confidence = most_common[1] / num_samples

        # Find best reasoning for the winning answer
        winning_idx = answers.index(final_answer)
        best_reasoning = reasoning_paths[winning_idx]

        return {
            "answer": final_answer,
            "confidence": confidence,
            "agreement": f"{most_common[1]}/{num_samples}",
            "all_answers": dict(answer_counts),
            "reasoning": best_reasoning
        }

    def _extract_answer(self, text: str) -> str:
        """Extract answer from response."""
        import re
        match = re.search(r'<answer>(.*?)</answer>', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.split('\n')[-1].strip()

    def _extract_thinking(self, text: str) -> str:
        """Extract thinking from response."""
        import re
        match = re.search(r'<thinking>(.*?)</thinking>', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""


# Usage
client = OpenAI()
reasoner = SelfConsistencyReasoner(client)

result = reasoner.solve(
    problem="If a shirt costs $25 after a 20% discount, what was the original price?",
    num_samples=5
)

print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']:.0%}")
print(f"Agreement: {result['agreement']}")
```

### Example Output

```json
{
  "answer": "$31.25",
  "confidence": 0.8,
  "agreement": "4/5",
  "all_answers": {
    "$31.25": 4,
    "$30": 1
  },
  "reasoning": "1. Let x = original price\n2. After 20% discount: x - 0.20x = 0.80x\n3. 0.80x = $25\n4. x = $25 / 0.80 = $31.25"
}
```

---

## Tree-of-Thoughts Examples

### Python Implementation

```python
from typing import List, Dict, Any
import json

class TreeOfThoughts:
    """Tree of Thoughts for deliberate reasoning."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def solve(
        self,
        problem: str,
        num_thoughts: int = 3,
        max_depth: int = 3,
        prune_threshold: float = 5.0
    ) -> Dict[str, Any]:
        """Solve using tree exploration."""

        # Generate initial thoughts
        thoughts = self._generate_thoughts(problem, num_thoughts)

        # Evaluate thoughts
        evaluated = self._evaluate_thoughts(problem, thoughts)

        # Prune low-scoring thoughts
        viable = [t for t in evaluated if t['score'] >= prune_threshold]

        if not viable:
            # Fallback to best available
            viable = [max(evaluated, key=lambda x: x['score'])]

        # Expand best thought
        best = max(viable, key=lambda x: x['score'])

        # Continue reasoning from best thought
        final = self._complete_reasoning(problem, best['thought'])

        return {
            "problem": problem,
            "initial_thoughts": evaluated,
            "selected_thought": best,
            "final_answer": final,
            "exploration_path": [best['thought']]
        }

    def _generate_thoughts(self, problem: str, num: int) -> List[str]:
        """Generate diverse initial thoughts."""

        prompt = f"""Problem: {problem}

Generate {num} different approaches to start solving this problem.
Each approach should be a distinct first step or strategy.

Return as JSON:
{{"approaches": ["approach 1", "approach 2", ...]}}"""

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
    ) -> List[Dict[str, Any]]:
        """Evaluate how promising each thought is."""

        evaluated = []
        for thought in thoughts:
            prompt = f"""Problem: {problem}

Proposed approach: {thought}

Evaluate this approach (1-10):
- Relevance: Does it address the problem?
- Feasibility: Can it lead to a solution?
- Efficiency: Is it a good use of effort?

Return JSON: {{"score": N, "strengths": "...", "weaknesses": "..."}}"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            evaluated.append({
                "thought": thought,
                "score": result.get("score", 5),
                "strengths": result.get("strengths", ""),
                "weaknesses": result.get("weaknesses", "")
            })

        return evaluated

    def _complete_reasoning(self, problem: str, starting_thought: str) -> str:
        """Complete reasoning from a starting point."""

        prompt = f"""Problem: {problem}

Starting with this approach: {starting_thought}

Continue the reasoning to reach the final answer.
Show each step clearly.

<thinking>
[Continue from the starting approach]
</thinking>

<answer>
[Final answer]
</answer>"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content


# Usage
tot = TreeOfThoughts(client)
result = tot.solve(
    problem="Game of 24: Use 4, 7, 8, 8 to make 24 using +, -, *, /",
    num_thoughts=4
)

print("Initial thoughts evaluated:")
for t in result['initial_thoughts']:
    print(f"  [{t['score']}/10] {t['thought']}")
print(f"\nSelected: {result['selected_thought']['thought']}")
print(f"\nFinal answer:\n{result['final_answer']}")
```

### Simplified Single-Prompt ToT (Hulbert 2023)

```
Imagine three different experts are answering this question.
All experts will write down 1 step of their thinking, then share it with the group.
Then all experts will go on to the next step, etc.
If any expert realizes they're wrong at any point, they leave.

Question: {question}

Expert deliberation:
```

---

## Least-to-Most Examples

### Python Implementation

```python
from typing import List, Dict, Any
import json

def least_to_most_solve(
    client,
    problem: str,
    model: str = "gpt-4o"
) -> Dict[str, Any]:
    """Solve using least-to-most decomposition."""

    # Step 1: Decompose problem
    decompose_prompt = f"""Problem: {problem}

Break this into simpler subproblems, ordered from simplest to most complex.
Each subproblem should be solvable, and later ones may depend on earlier solutions.

Return JSON: {{"subproblems": ["simplest first", "more complex", "most complex"]}}"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": decompose_prompt}],
        response_format={"type": "json_object"}
    )

    subproblems = json.loads(response.choices[0].message.content).get("subproblems", [])

    # Step 2: Solve each subproblem
    solutions = []
    context = ""

    for subproblem in subproblems:
        solve_prompt = f"""Original problem: {problem}

Previous solutions:
{context if context else "(none yet)"}

Current subproblem: {subproblem}

Solve this subproblem step by step, using any previous solutions as needed.

<solution>
[Your solution]
</solution>"""

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": solve_prompt}]
        )

        solution = response.choices[0].message.content
        solutions.append({
            "subproblem": subproblem,
            "solution": solution
        })

        # Build context for next iteration
        context += f"\nSubproblem: {subproblem}\nSolution: {solution}\n---"

    # Step 3: Synthesize final answer
    synthesis_prompt = f"""Original problem: {problem}

All subproblem solutions:
{context}

Using all the above solutions, provide the final answer to the original problem.

<answer>
[Final comprehensive answer]
</answer>"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": synthesis_prompt}]
    )

    return {
        "problem": problem,
        "subproblems": subproblems,
        "solutions": solutions,
        "final_answer": response.choices[0].message.content
    }


# Example usage
result = least_to_most_solve(
    client,
    problem="Calculate the compound interest on $10,000 at 5% annual rate, compounded monthly, for 3 years"
)

print("Decomposition:")
for i, sp in enumerate(result['subproblems'], 1):
    print(f"  {i}. {sp}")
```

---

## Domain-Specific CoT

### Code Review CoT

```python
CODE_REVIEW_COT = """Review this code for issues.

Code:
```{language}
{code}
```

Analyze step by step:

<thinking>
1. **Purpose Analysis**: What does this code intend to do?
2. **Logic Check**: Are there any logical errors?
3. **Edge Cases**: What inputs could cause problems?
4. **Security**: Any vulnerabilities (injection, overflow, etc.)?
5. **Performance**: Any inefficiencies?
6. **Best Practices**: Does it follow conventions?
</thinking>

<issues>
## Critical (must fix)
[List any bugs or security issues]

## Improvements (should fix)
[List performance or code quality issues]

## Suggestions (nice to have)
[List style or minor improvements]
</issues>

<fixed_code>
[Provide corrected version if critical issues found]
</fixed_code>
"""
```

### Decision Making CoT

```python
DECISION_COT = """Help make this decision using structured analysis.

Decision: {decision}

Options:
{options}

Criteria:
{criteria}

<thinking>
1. **Clarify Decision**: What exactly are we deciding?
2. **Understand Options**: Brief summary of each option
3. **Apply Criteria**: Evaluate each option against each criterion
4. **Risk Assessment**: What could go wrong with each?
5. **Weigh Trade-offs**: What are we gaining/losing?
6. **Consider Context**: Any situational factors?
</thinking>

<analysis>
| Option | {criteria[0]} | {criteria[1]} | {criteria[2]} | Overall |
|--------|--------------|--------------|--------------|---------|
| {option 1} | ... | ... | ... | X/10 |
| {option 2} | ... | ... | ... | X/10 |
</analysis>

<recommendation>
**Recommended Option**: [Choice]
**Key Reasons**: [Top 2-3 reasons]
**Risks to Mitigate**: [Main concerns with this choice]
**Implementation Notes**: [How to proceed]
</recommendation>
"""
```

### Mathematical Proof CoT

```python
MATH_PROOF_COT = """Prove or disprove the following statement.

Statement: {statement}

<thinking>
1. **Understand the Statement**: What exactly needs to be proven?
2. **Identify Approach**: Direct proof, contradiction, induction, counterexample?
3. **Set Up**: Define variables, state assumptions
4. **Develop Argument**: Build the logical chain
5. **Verify**: Check each step is valid
</thinking>

<proof>
**Claim**: {statement}

**Approach**: [Method chosen]

**Proof**:
[Step-by-step logical argument]

**QED** / **Counterexample**: [Conclusion]
</proof>
"""
```

---

## Production Patterns

### CoT Service with Fallback

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any
import logging

class CoTStrategy(Enum):
    ZERO_SHOT = "zero_shot"
    FEW_SHOT = "few_shot"
    SELF_CONSISTENCY = "self_consistency"
    TREE_OF_THOUGHTS = "tree_of_thoughts"

@dataclass
class CoTConfig:
    strategy: CoTStrategy = CoTStrategy.ZERO_SHOT
    num_samples: int = 5
    temperature: float = 0.7
    max_retries: int = 3
    fallback_strategy: Optional[CoTStrategy] = None

class ChainOfThoughtService:
    """Production-ready CoT service with fallbacks."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model
        self.logger = logging.getLogger(__name__)

    def reason(
        self,
        problem: str,
        config: Optional[CoTConfig] = None
    ) -> Dict[str, Any]:
        """Apply CoT with automatic fallback."""
        config = config or CoTConfig()

        for attempt in range(config.max_retries):
            try:
                result = self._execute_strategy(problem, config.strategy, config)

                if self._validate_result(result):
                    return {
                        "success": True,
                        "strategy": config.strategy.value,
                        "result": result,
                        "attempts": attempt + 1
                    }

            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")

        # Try fallback strategy
        if config.fallback_strategy:
            self.logger.info(f"Trying fallback: {config.fallback_strategy}")
            try:
                result = self._execute_strategy(
                    problem,
                    config.fallback_strategy,
                    config
                )
                return {
                    "success": True,
                    "strategy": config.fallback_strategy.value,
                    "result": result,
                    "fallback_used": True
                }
            except Exception as e:
                self.logger.error(f"Fallback failed: {e}")

        return {
            "success": False,
            "error": "All strategies failed",
            "attempts": config.max_retries
        }

    def _execute_strategy(
        self,
        problem: str,
        strategy: CoTStrategy,
        config: CoTConfig
    ) -> Dict[str, Any]:
        """Execute specific CoT strategy."""
        if strategy == CoTStrategy.ZERO_SHOT:
            return self._zero_shot(problem)
        elif strategy == CoTStrategy.SELF_CONSISTENCY:
            return self._self_consistency(
                problem,
                config.num_samples,
                config.temperature
            )
        # ... other strategies

        return self._zero_shot(problem)

    def _validate_result(self, result: Dict) -> bool:
        """Validate CoT result."""
        return bool(result.get("answer"))


# Usage
service = ChainOfThoughtService(client)

result = service.reason(
    problem="Complex problem here",
    config=CoTConfig(
        strategy=CoTStrategy.SELF_CONSISTENCY,
        num_samples=5,
        fallback_strategy=CoTStrategy.ZERO_SHOT
    )
)
```

---

## Anti-Patterns

### Anti-Pattern 1: CoT for Simple Tasks

**Bad:**
```
What is the capital of France?

Let's think step by step:
1. France is a country in Europe
2. Countries have capitals
3. I need to recall France's capital
4. The capital of France is Paris

Answer: Paris
```

**Problem:** Wastes tokens on trivial lookup. Just ask directly.

**Good:**
```
What is the capital of France?

Answer: Paris
```

### Anti-Pattern 2: Vague Trigger

**Bad:**
```
Solve this problem.
{complex problem}
Think about it.
```

**Problem:** "Think about it" doesn't trigger step-by-step reasoning.

**Good:**
```
Solve this problem step by step.

{complex problem}

<thinking>
[Show your work]
</thinking>

<answer>
[Final answer]
</answer>
```

### Anti-Pattern 3: No Structure

**Bad:**
```
Calculate compound interest. Think through it.

Principal: $1000, Rate: 5%, Time: 2 years, Compound: monthly
```

**Problem:** Output format unclear, hard to parse answer.

**Good:**
```
Calculate compound interest.

Given:
- Principal: $1000
- Annual Rate: 5%
- Time: 2 years
- Compounding: monthly

Think through step by step:

<thinking>
[Show calculations]
</thinking>

<answer>
Final Amount: $___
Interest Earned: $___
</answer>
```

### Anti-Pattern 4: Inconsistent Examples

**Bad (conflicting examples):**
```
Example 1: 2 + 2 = ?
Thinking: Add the numbers
Answer: 4

Example 2: 3 + 3 = ?
Answer: 6
(no thinking shown)
```

**Problem:** Format inconsistency confuses the model.

### Anti-Pattern 5: Unbounded ToT

**Bad:**
```python
def solve(problem):
    thoughts = generate_all_thoughts(problem)  # Could be infinite
    for thought in thoughts:
        expand_forever(thought)  # No depth limit
```

**Problem:** Resource exhaustion, timeouts.

**Good:**
```python
def solve(problem, max_thoughts=5, max_depth=3, timeout=30):
    # Bounded exploration
    ...
```

---

## Quick Reference: Pattern Selection

| Problem Type | Recommended Pattern | Example |
|--------------|--------------------| --------|
| Simple math | Zero-Shot CoT | Arithmetic, percentages |
| Complex math | Self-Consistency | Multi-step word problems |
| Logic puzzles | Zero-Shot CoT | Syllogisms, deductions |
| Code debugging | Domain-Specific CoT | Bug finding, fixes |
| Planning | Tree-of-Thoughts | Game playing, scheduling |
| Multi-part problems | Least-to-Most | Complex calculations |
| High-stakes decisions | Self-Consistency | Medical, legal, financial |
