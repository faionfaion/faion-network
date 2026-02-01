---
id: chain-of-thought-basics
name: "Chain-of-Thought Basics"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
parent: chain-of-thought
---

# Chain-of-Thought Basics

## Overview

Chain-of-Thought (CoT) prompting enables LLMs to break down complex problems into intermediate reasoning steps. This technique dramatically improves performance on tasks requiring multi-step reasoning, math, logic, and complex analysis.

## When to Use

- Mathematical calculations
- Multi-step reasoning problems
- Logic puzzles
- Code debugging
- Complex analysis tasks
- Decision making with multiple factors

## Key Concepts

### CoT Techniques

| Technique | Description | Trigger |
|-----------|-------------|---------|
| Zero-shot CoT | Add "think step by step" | Single phrase |
| Few-shot CoT | Examples with reasoning | Demonstrated steps |
| Self-consistency | Multiple paths, vote | Sample + aggregate |
| Tree of Thoughts | Explore multiple branches | Structured exploration |
| Least-to-Most | Break into subproblems | Decomposition |

### How CoT Works

```
Without CoT:
Q: If John has 5 apples and gives 2 to Mary, then buys 3 more, how many does he have?
A: 6 ← (May be wrong, no reasoning shown)

With CoT:
Q: If John has 5 apples and gives 2 to Mary, then buys 3 more, how many does he have?
A: Let me think step by step:
   1. John starts with 5 apples
   2. He gives 2 to Mary: 5 - 2 = 3 apples
   3. He buys 3 more: 3 + 3 = 6 apples
   Therefore, John has 6 apples.
```

## Implementation

### Zero-Shot Chain-of-Thought

```python
def zero_shot_cot(
    client,
    problem: str,
    model: str = "gpt-4o"
) -> str:
    """Simple zero-shot CoT with magic phrase."""
    messages = [
        {
            "role": "user",
            "content": f"{problem}\n\nLet's think step by step."
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content

# Variations of the magic phrase
COT_TRIGGERS = [
    "Let's think step by step.",
    "Let's work through this systematically.",
    "Let me break this down:",
    "Let's analyze this carefully:",
    "Let's solve this step by step:",
    "First, let me understand the problem, then solve it methodically."
]
```

### Few-Shot Chain-of-Thought

```python
def few_shot_cot(
    client,
    problem: str,
    examples: list[dict],
    model: str = "gpt-4o"
) -> str:
    """Few-shot CoT with reasoning examples."""
    messages = []

    # Add examples with reasoning
    for ex in examples:
        messages.append({"role": "user", "content": ex["question"]})
        messages.append({"role": "assistant", "content": ex["reasoning"]})

    # Add the actual problem
    messages.append({"role": "user", "content": problem})

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content

# Example reasoning chains
MATH_COT_EXAMPLES = [
    {
        "question": "Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?",
        "reasoning": """Let me solve this step by step:
1. Roger starts with 5 tennis balls
2. He buys 2 cans, each with 3 balls
3. New balls from cans: 2 × 3 = 6 balls
4. Total balls: 5 + 6 = 11 balls

Therefore, Roger has 11 tennis balls."""
    },
    {
        "question": "A store had 40 apples. If they sold 15 in the morning and 18 in the afternoon, how many are left?",
        "reasoning": """Let me work through this:
1. Starting apples: 40
2. Sold in morning: 15
3. After morning: 40 - 15 = 25 apples
4. Sold in afternoon: 18
5. After afternoon: 25 - 18 = 7 apples

Therefore, 7 apples are left."""
    }
]
```

### Self-Consistency

```python
import random
from collections import Counter
from typing import List, Tuple

def self_consistency_cot(
    client,
    problem: str,
    num_samples: int = 5,
    temperature: float = 0.7,
    model: str = "gpt-4o"
) -> Tuple[str, float]:
    """
    Generate multiple reasoning paths and vote on the answer.
    Returns most common answer and confidence.
    """
    answers = []

    for _ in range(num_samples):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"{problem}\n\nLet's think step by step. End with 'The answer is: [answer]'"
                }
            ],
            temperature=temperature
        )

        # Extract answer
        text = response.choices[0].message.content
        if "The answer is:" in text:
            answer = text.split("The answer is:")[-1].strip().rstrip(".")
            answers.append(answer)

    if not answers:
        return None, 0.0

    # Vote on most common answer
    counter = Counter(answers)
    most_common = counter.most_common(1)[0]

    return most_common[0], most_common[1] / len(answers)

# Usage
problem = "If a shirt costs $25 and is 20% off, what is the final price?"
answer, confidence = self_consistency_cot(client, problem, num_samples=5)
print(f"Answer: {answer} (confidence: {confidence:.0%})")
```

## Best Practices

1. **Choose Right Strategy**
   - Zero-shot for simple problems
   - Few-shot for pattern-dependent tasks
   - Self-consistency for critical decisions

2. **Provide Clear Examples**
   - Show complete reasoning
   - Cover different problem types
   - Include edge cases

3. **Structure the Output**
   - Request step-by-step format
   - Ask for explicit answer marker
   - Use structured formats when possible

4. **Verify Reasoning**
   - Check intermediate steps
   - Use self-consistency for validation
   - Ask for verification step

## Common Pitfalls

1. **Expecting Perfection** - CoT improves but doesn't guarantee correctness
2. **Wrong Problem Type** - CoT helps with reasoning, not all tasks
3. **Weak Examples** - Poor few-shot examples lead to poor reasoning
4. **Ignoring Confidence** - Not using self-consistency when accuracy matters
5. **No Verification** - Not checking reasoning steps

## References

- [Chain-of-Thought Paper](https://arxiv.org/abs/2201.11903)
- [Self-Consistency Paper](https://arxiv.org/abs/2203.11171)

## See Also

- [cot-techniques.md](cot-techniques.md) - Advanced CoT techniques (ToT, Least-to-Most, domain-specific)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Step-by-step reasoning | haiku | Format application |
| Thinking process extraction | sonnet | Analysis pattern |
