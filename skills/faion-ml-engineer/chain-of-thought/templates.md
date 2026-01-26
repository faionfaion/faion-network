# Chain-of-Thought Templates

Copy-paste templates for implementing CoT techniques.

## Table of Contents

1. [Zero-Shot CoT Templates](#zero-shot-cot-templates)
2. [Few-Shot CoT Templates](#few-shot-cot-templates)
3. [Self-Consistency Templates](#self-consistency-templates)
4. [Tree-of-Thoughts Templates](#tree-of-thoughts-templates)
5. [Least-to-Most Templates](#least-to-most-templates)
6. [Domain-Specific Templates](#domain-specific-templates)
7. [Python Code Templates](#python-code-templates)

---

## Zero-Shot CoT Templates

### Basic Zero-Shot CoT

```
{TASK_DESCRIPTION}

Problem:
<problem>
{PROBLEM}
</problem>

Let's think step by step.

<thinking>
[Work through the problem systematically]
</thinking>

<answer>
[Final answer only]
</answer>
```

### Zero-Shot CoT with Format

```
{TASK_DESCRIPTION}

Problem:
<problem>
{PROBLEM}
</problem>

Think through this step by step, then provide the answer.

<thinking>
Step 1: [First observation or calculation]
Step 2: [Next step]
Step 3: [Continue as needed]
...
Final Step: [Verification or conclusion]
</thinking>

<answer>
{OUTPUT_FORMAT}
</answer>
```

### Zero-Shot CoT for Claude

```xml
<task>
{TASK_DESCRIPTION}
</task>

<problem>
{PROBLEM}
</problem>

<instructions>
Please solve this step by step. Show your reasoning in the thinking section, then provide your final answer.
</instructions>

<thinking>
[Your systematic reasoning here]
</thinking>

<answer>
[Your final answer]
</answer>
```

### Zero-Shot CoT - Verification Variant

```
{TASK_DESCRIPTION}

Problem:
<problem>
{PROBLEM}
</problem>

Solve step by step, then verify your answer.

<thinking>
[Solution steps]
</thinking>

<verification>
[Check your answer by working backwards or using an alternative method]
</verification>

<answer>
[Final answer with confidence: high/medium/low]
</answer>
```

---

## Few-Shot CoT Templates

### Basic Few-Shot CoT

```
{TASK_DESCRIPTION}

Here are some examples:

<example>
Problem: {EXAMPLE_1_PROBLEM}
<thinking>
{EXAMPLE_1_REASONING}
</thinking>
<answer>{EXAMPLE_1_ANSWER}</answer>
</example>

<example>
Problem: {EXAMPLE_2_PROBLEM}
<thinking>
{EXAMPLE_2_REASONING}
</thinking>
<answer>{EXAMPLE_2_ANSWER}</answer>
</example>

Now solve this:

Problem: {ACTUAL_PROBLEM}
<thinking>
</thinking>
<answer></answer>
```

### Few-Shot CoT - Math

```
Solve math word problems step by step.

Example 1:
Problem: A store has 45 apples. They sell 12 and receive a shipment of 30. How many apples now?
<thinking>
1. Start with: 45 apples
2. Sold: 45 - 12 = 33 apples
3. Received shipment: 33 + 30 = 63 apples
</thinking>
<answer>63 apples</answer>

Example 2:
Problem: If 4 workers take 6 hours to paint a room, how long for 8 workers?
<thinking>
1. Total work: 4 workers * 6 hours = 24 worker-hours
2. With 8 workers: 24 worker-hours / 8 workers = 3 hours
</thinking>
<answer>3 hours</answer>

Now solve:
Problem: {PROBLEM}
<thinking>
</thinking>
<answer></answer>
```

### Few-Shot CoT - Classification

```
Classify the text and explain your reasoning.

Example 1:
Text: "The new restaurant exceeded expectations - fantastic food and great service!"
<thinking>
- "exceeded expectations" = positive
- "fantastic food" = strong positive
- "great service" = positive
- Overall: Multiple strong positive indicators
</thinking>
<answer>positive</answer>

Example 2:
Text: "The product works but has some annoying quirks I wish they'd fix."
<thinking>
- "works" = neutral/mildly positive
- "annoying quirks" = negative
- "wish they'd fix" = criticism
- Overall: Mixed but leans negative due to frustration
</thinking>
<answer>negative</answer>

Example 3:
Text: "Received the package yesterday. Standard shipping took 5 days."
<thinking>
- No emotional language
- Pure factual statement
- No positive or negative indicators
</thinking>
<answer>neutral</answer>

Now classify:
Text: "{TEXT}"
<thinking>
</thinking>
<answer></answer>
```

---

## Self-Consistency Templates

### Self-Consistency Prompt

```
{TASK_DESCRIPTION}

Problem:
<problem>
{PROBLEM}
</problem>

Solve this problem. Show your reasoning step by step.

<thinking>
[Your reasoning here - be thorough]
</thinking>

<answer>
[Final answer - keep it concise for comparison]
</answer>
```

### Self-Consistency with Explicit Alternatives

```
{TASK_DESCRIPTION}

Problem:
<problem>
{PROBLEM}
</problem>

Solve using THREE different approaches, then determine the most likely correct answer.

<approach_1>
Method: [Description of approach]
Steps:
[Working]
Result: [Answer from this approach]
</approach_1>

<approach_2>
Method: [Different approach]
Steps:
[Working]
Result: [Answer from this approach]
</approach_2>

<approach_3>
Method: [Third approach]
Steps:
[Working]
Result: [Answer from this approach]
</approach_3>

<consensus>
Answers obtained: [List of answers]
Agreement: [X/3 approaches agree]
Most reliable answer: [Chosen answer]
Confidence: [high/medium/low]
Reasoning: [Why this answer is most likely correct]
</consensus>
```

### Self-Consistency Configuration

```python
SELF_CONSISTENCY_CONFIG = {
    "num_samples": 5,           # Number of reasoning paths
    "temperature": 0.7,         # Diversity of paths (0.5-1.0)
    "aggregation": "majority",  # majority | weighted | unanimous
    "min_agreement": 0.6,       # Minimum consensus threshold
    "answer_extraction": "xml", # How to parse answer: xml | last_line | json
}
```

---

## Tree-of-Thoughts Templates

### Thought Generation Prompt

```
Problem: {PROBLEM}

Generate {NUM_THOUGHTS} different approaches to start solving this problem.

Each approach should be:
- A distinct first step or strategy
- Concrete enough to evaluate
- Different from other approaches

Return as JSON:
{
  "approaches": [
    "Approach 1: [description]",
    "Approach 2: [description]",
    "Approach 3: [description]"
  ]
}
```

### Thought Evaluation Prompt

```
Problem: {PROBLEM}

Proposed approach: {THOUGHT}

Evaluate this approach on a scale of 1-10:

Criteria:
1. Relevance: Does it address the core problem?
2. Feasibility: Can it lead to a solution?
3. Efficiency: Is it a good use of effort?
4. Correctness: Is the reasoning sound?

Return JSON:
{
  "score": 7,
  "relevance": 8,
  "feasibility": 7,
  "efficiency": 6,
  "correctness": 8,
  "strengths": "...",
  "weaknesses": "...",
  "should_continue": true
}
```

### Thought Expansion Prompt

```
Problem: {PROBLEM}

Current reasoning path:
{CURRENT_PATH}

Current thought: {CURRENT_THOUGHT}

Continue reasoning from this point. Generate {NUM_THOUGHTS} possible next steps.

Return JSON:
{
  "next_steps": [
    "Step option 1: [description]",
    "Step option 2: [description]"
  ]
}
```

### Simplified Single-Prompt ToT

```
Imagine three different experts are answering this question.
All experts will write down 1 step of their thinking, then share it with the group.
Then all experts will go on to the next step, etc.
If any expert realizes they're wrong at any point, they leave.

Question: {QUESTION}

Expert 1 (Analytical):
Expert 2 (Creative):
Expert 3 (Systematic):

Round 1:
[Each expert's first step]

Round 2:
[Remaining experts' second step]

Round 3:
[Continue until conclusion]

Final Answer: [Consensus from remaining experts]
```

---

## Least-to-Most Templates

### Decomposition Prompt

```
Problem: {PROBLEM}

Break this into simpler subproblems.
Order them from simplest to most complex.
Later subproblems may depend on solutions to earlier ones.

Return JSON:
{
  "subproblems": [
    {
      "id": 1,
      "description": "Simplest subproblem",
      "depends_on": []
    },
    {
      "id": 2,
      "description": "Next subproblem",
      "depends_on": [1]
    },
    {
      "id": 3,
      "description": "Most complex subproblem",
      "depends_on": [1, 2]
    }
  ]
}
```

### Subproblem Solution Prompt

```
Original problem: {ORIGINAL_PROBLEM}

Previous solutions:
<context>
{ACCUMULATED_SOLUTIONS}
</context>

Current subproblem: {CURRENT_SUBPROBLEM}

Solve this subproblem, using previous solutions as needed.

<thinking>
[Your reasoning]
</thinking>

<solution>
[Solution to this subproblem]
</solution>
```

### Synthesis Prompt

```
Original problem: {ORIGINAL_PROBLEM}

All subproblem solutions:
<solutions>
{ALL_SOLUTIONS}
</solutions>

Using all the solutions above, provide the final answer to the original problem.

<synthesis>
[How the solutions combine]
</synthesis>

<answer>
[Final comprehensive answer]
</answer>
```

---

## Domain-Specific Templates

### Code Debugging CoT

```
Debug this code that produces an error.

Code:
```{LANGUAGE}
{CODE}
```

Error:
```
{ERROR_MESSAGE}
```

Analyze step by step:

<thinking>
1. **Intent**: What should this code do?
2. **Error Location**: Where does the error occur?
3. **Root Cause**: Why does this error happen?
4. **Fix Strategy**: How should we fix it?
</thinking>

<diagnosis>
Error type: {error_type}
Location: {line/function}
Root cause: {explanation}
</diagnosis>

<fix>
```{LANGUAGE}
{FIXED_CODE}
```
</fix>

<explanation>
[What was changed and why]
</explanation>
```

### Decision Analysis CoT

```
Help make this decision.

Decision: {DECISION_QUESTION}

Options:
{OPTIONS_LIST}

Criteria:
{CRITERIA_LIST}

<thinking>
1. **Clarify Decision**: What exactly are we choosing?
2. **Understand Options**: Key characteristics of each
3. **Apply Criteria**: Evaluate each option
4. **Assess Risks**: What could go wrong?
5. **Consider Trade-offs**: What do we give up?
</thinking>

<analysis>
| Option | {CRITERION_1} | {CRITERION_2} | {CRITERION_3} | Overall |
|--------|--------------|--------------|--------------|---------|
| Option A | score | score | score | X/10 |
| Option B | score | score | score | X/10 |
</analysis>

<recommendation>
Best Option: [Choice]
Key Reasons:
1. [Reason 1]
2. [Reason 2]
Risks to Mitigate: [Main concerns]
</recommendation>
```

### Mathematical Problem CoT

```
Solve this math problem with detailed reasoning.

Problem: {PROBLEM}

<thinking>
**Given**: [Extract known information]
**Find**: [What we need to solve for]
**Approach**: [Method to use]
**Solution**:
Step 1: [First step with calculation]
Step 2: [Next step]
...
**Verification**: [Check the answer]
</thinking>

<answer>
{ANSWER_WITH_UNITS}
</answer>
```

### Research Analysis CoT

```
Analyze this research finding/claim.

Claim: {CLAIM}

Source: {SOURCE_INFO}

<thinking>
1. **Understand the Claim**: What exactly is being asserted?
2. **Evidence Quality**: How strong is the supporting evidence?
3. **Methodology**: How was this determined?
4. **Limitations**: What caveats exist?
5. **Alternative Explanations**: Other possible interpretations?
6. **Implications**: If true, what does this mean?
</thinking>

<analysis>
Claim validity: [Strong/Moderate/Weak/Insufficient]
Evidence quality: [High/Medium/Low]
Key strengths: [List]
Key limitations: [List]
</analysis>

<conclusion>
[Summary assessment with confidence level]
</conclusion>
```

---

## Python Code Templates

### Basic CoT Function

```python
def chain_of_thought(
    client,
    problem: str,
    model: str = "gpt-4o",
    trigger: str = "Let's think step by step."
) -> dict:
    """Basic zero-shot chain-of-thought."""

    prompt = f"""{problem}

{trigger}

<thinking>
[Your reasoning]
</thinking>

<answer>
[Final answer]
</answer>"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    # Extract thinking and answer
    import re
    thinking = re.search(r'<thinking>(.*?)</thinking>', content, re.DOTALL)
    answer = re.search(r'<answer>(.*?)</answer>', content, re.DOTALL)

    return {
        "full_response": content,
        "thinking": thinking.group(1).strip() if thinking else None,
        "answer": answer.group(1).strip() if answer else None
    }
```

### Self-Consistency Function

```python
from collections import Counter
from typing import List, Dict, Any

def self_consistency(
    client,
    problem: str,
    num_samples: int = 5,
    temperature: float = 0.7,
    model: str = "gpt-4o"
) -> Dict[str, Any]:
    """Self-consistency with majority voting."""

    prompt = f"""{problem}

Solve step by step.

<thinking>
[Your reasoning]
</thinking>

<answer>
[Concise final answer]
</answer>"""

    answers = []
    responses = []

    for _ in range(num_samples):
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        content = response.choices[0].message.content
        responses.append(content)

        # Extract answer
        import re
        match = re.search(r'<answer>(.*?)</answer>', content, re.DOTALL)
        answer = match.group(1).strip() if match else content.split('\n')[-1]
        answers.append(answer)

    # Majority vote
    counts = Counter(answers)
    winner, count = counts.most_common(1)[0]

    return {
        "answer": winner,
        "confidence": count / num_samples,
        "agreement": f"{count}/{num_samples}",
        "all_answers": dict(counts),
        "responses": responses
    }
```

### Tree-of-Thoughts Class

```python
from typing import List, Dict, Any
import json

class TreeOfThoughts:
    """Tree-of-Thoughts reasoning."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def solve(
        self,
        problem: str,
        num_thoughts: int = 3,
        prune_threshold: float = 5.0
    ) -> Dict[str, Any]:
        """Solve using tree exploration."""

        # Generate initial thoughts
        thoughts = self._generate_thoughts(problem, num_thoughts)

        # Evaluate thoughts
        evaluated = []
        for thought in thoughts:
            score = self._evaluate_thought(problem, thought)
            evaluated.append({"thought": thought, **score})

        # Select best
        viable = [t for t in evaluated if t["score"] >= prune_threshold]
        if not viable:
            viable = [max(evaluated, key=lambda x: x["score"])]

        best = max(viable, key=lambda x: x["score"])

        # Complete from best
        final = self._complete(problem, best["thought"])

        return {
            "thoughts": evaluated,
            "selected": best,
            "answer": final
        }

    def _generate_thoughts(self, problem: str, num: int) -> List[str]:
        prompt = f"""Problem: {problem}

Generate {num} different approaches. Return JSON:
{{"approaches": ["approach 1", "approach 2", ...]}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content).get("approaches", [])

    def _evaluate_thought(self, problem: str, thought: str) -> dict:
        prompt = f"""Problem: {problem}
Approach: {thought}

Rate 1-10. Return JSON: {{"score": N, "reason": "..."}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    def _complete(self, problem: str, thought: str) -> str:
        prompt = f"""Problem: {problem}
Approach: {thought}

Continue to final answer.

<thinking>[Continue reasoning]</thinking>
<answer>[Final answer]</answer>"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

### Least-to-Most Function

```python
def least_to_most(
    client,
    problem: str,
    model: str = "gpt-4o"
) -> Dict[str, Any]:
    """Least-to-most decomposition and solving."""

    # Decompose
    decompose_prompt = f"""Problem: {problem}

Break into subproblems, simplest to most complex.
Return JSON: {{"subproblems": ["sub1", "sub2", ...]}}"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": decompose_prompt}],
        response_format={"type": "json_object"}
    )
    subproblems = json.loads(response.choices[0].message.content).get("subproblems", [])

    # Solve each
    context = ""
    solutions = []

    for sub in subproblems:
        solve_prompt = f"""Original: {problem}
Previous solutions: {context or "(none)"}
Subproblem: {sub}

Solve this subproblem.
<solution>[Your solution]</solution>"""

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": solve_prompt}]
        )
        solution = response.choices[0].message.content
        solutions.append({"subproblem": sub, "solution": solution})
        context += f"\n- {sub}: {solution}\n"

    # Synthesize
    synth_prompt = f"""Original: {problem}
Solutions: {context}

Synthesize final answer.
<answer>[Final answer]</answer>"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": synth_prompt}]
    )

    return {
        "subproblems": subproblems,
        "solutions": solutions,
        "final": response.choices[0].message.content
    }
```

---

## Quick Reference: Template Selection

| Task | Template |
|------|----------|
| Simple reasoning | Basic Zero-Shot CoT |
| Format-critical | Few-Shot CoT |
| High accuracy needed | Self-Consistency |
| Complex exploration | Tree-of-Thoughts |
| Sequential problems | Least-to-Most |
| Code debugging | Code Debugging CoT |
| Business decisions | Decision Analysis CoT |
| Math problems | Mathematical Problem CoT |
