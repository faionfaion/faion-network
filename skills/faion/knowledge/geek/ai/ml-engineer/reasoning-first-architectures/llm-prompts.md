---
id: reasoning-first-architectures-prompts
name: "Reasoning-First Architectures LLM Prompts"
parent: reasoning-first-architectures
---

# Reasoning-First Architectures LLM Prompts

## 1. Chain-of-Thought Prompts

### Basic CoT (for non-reasoning models)

```
Solve this problem step by step. Show your reasoning at each step before giving the final answer.

Problem: {problem}

Think through this carefully:
```

### Structured CoT with XML Tags

```
Solve the following problem. Use the tags below to structure your response.

<problem>
{problem}
</problem>

<thinking>
[Work through the problem step by step. Show all calculations and reasoning.]
</thinking>

<answer>
[Your final answer]
</answer>
```

### Zero-Shot CoT

```
{problem}

Let's think step by step.
```

### Few-Shot CoT Template

```
I'll solve problems by thinking step by step.

Example 1:
Problem: If a train travels 120 km in 2 hours, what is its average speed?
Thinking: To find average speed, I divide total distance by total time.
Speed = 120 km / 2 hours = 60 km/h
Answer: 60 km/h

Example 2:
Problem: A store has a 25% off sale. If a shirt originally costs $40, what is the sale price?
Thinking: First, I calculate the discount amount.
25% of $40 = 0.25 x 40 = $10
Then subtract from original price.
$40 - $10 = $30
Answer: $30

Now solve:
Problem: {problem}
Thinking:
```

## 2. Extended Thinking Prompts (Claude)

### High-Level Guidance (Recommended)

```
Think deeply about this problem. Consider multiple approaches, potential edge cases, and validate your reasoning before providing your answer.

{problem}
```

### Complex Analysis Prompt

```
I need a thorough analysis of the following. Take your time to:
- Consider the problem from multiple angles
- Identify potential issues or edge cases
- Validate your reasoning
- Provide a well-structured response

{problem}
```

### Code Review with Extended Thinking

```
Review this code thoroughly. Consider:
- Correctness and logic errors
- Performance implications
- Security vulnerabilities
- Edge cases and error handling
- Code style and best practices

```{language}
{code}
```

Provide your analysis and specific recommendations.
```

### Architecture Design Prompt

```
Design a solution for the following requirements. Consider:
- Scalability and performance
- Maintainability
- Security implications
- Trade-offs between approaches

Requirements:
{requirements}

Provide a detailed design with rationale for key decisions.
```

## 3. ReAct Prompts

### Standard ReAct System Prompt

```
You are an AI assistant that reasons step by step and uses tools when needed.

Available tools:
{tool_descriptions}

For each step, use this format:

Thought: [Your reasoning about what to do next]
Action: [tool_name]
Action Input: {"param": "value"}

After receiving an observation, continue reasoning:

Thought: [Process the observation and decide next steps]
...

When you have enough information:

Thought: [Final reasoning]
Final Answer: [Your complete answer]

Important:
- Always think before acting
- Use tools only when necessary
- Verify information when possible
- Provide clear, actionable answers
```

### ReAct with Verification

```
You are a careful AI assistant that verifies information before answering.

Available tools:
{tool_descriptions}

Process:
1. Understand the question
2. Gather necessary information using tools
3. Verify key facts with additional searches if needed
4. Synthesize a confident answer

Format:
Thought: [reasoning]
Action: [tool]
Action Input: {"query": "..."}
Observation: [result]
...
Verification Thought: [verify key facts]
Final Answer: [answer with confidence level]
```

## 4. Reflexion Prompts

### Self-Reflection Prompt

```
Review your previous attempt and reflect on what went wrong.

Task: {task}

Your previous attempt:
{previous_attempt}

Feedback: {feedback}

Reflect on:
1. What specific errors did you make?
2. What assumptions were incorrect?
3. What approach would work better?

Reflection:
```

### Iterative Improvement Prompt

```
You are improving your response based on feedback.

Original task: {task}

Attempt history:
{attempts_with_feedback}

Based on these learnings, provide an improved response that addresses all previous issues.
```

## 5. Tree-of-Thought Prompts

### Branch Generation Prompt

```
Given this problem, generate {n} different approaches to solve it.

Problem: {problem}

For each approach:
1. Briefly describe the strategy
2. List the key steps
3. Note potential advantages and risks

Approach 1:
Strategy: ...
Steps: ...
Pros/Cons: ...

Approach 2:
...
```

### Branch Evaluation Prompt

```
Evaluate this reasoning path for solving the problem.

Problem: {problem}

Reasoning path:
{reasoning_path}

Rate this path on a scale of 0.0 to 1.0 based on:
- Logical coherence (is the reasoning sound?)
- Progress toward solution (are we getting closer?)
- Feasibility (can this approach succeed?)

Score: [0.0-1.0]
Brief justification:
```

### Path Selection Prompt

```
Select the best reasoning path from these options.

Problem: {problem}

Option A:
{path_a}

Option B:
{path_b}

Option C:
{path_c}

Analyze each option and select the best one. Explain your choice.
```

## 6. OpenAI o3/o4 Specific Prompts

### Let the Model Think (Minimal Guidance)

```
{problem}
```

Note: For o3/o4, minimal prompting often works best. The model is trained to reason internally.

### Structured Output Request

```
{problem}

Provide your answer in this format:
- Summary: [1-2 sentence summary]
- Details: [full explanation]
- Confidence: [high/medium/low]
```

### Multi-Step Task

```
Complete the following multi-step task:

{task_description}

Steps to complete:
1. {step_1}
2. {step_2}
3. {step_3}

Provide your work for each step and the final result.
```

## 7. DeepSeek R1 Prompts

### Standard Reasoning Request

```
{problem}

Think through this problem carefully before answering.
```

### Visible Reasoning Request

```
Solve this problem. Show your complete reasoning process using <think> tags.

Problem: {problem}

<think>
[Your step-by-step reasoning here]
</think>

Final answer: [Your answer]
```

### Math/Logic Problem

```
Prove the following statement. Show all steps in your reasoning.

Statement: {statement}

Your proof:
```

## 8. Tool Use Prompts

### Tool-Augmented Reasoning

```
You have access to the following tools to help answer questions:

{tool_definitions}

When you need to use a tool, format your request as:
<tool_use>
<name>{tool_name}</name>
<input>{json_input}</input>
</tool_use>

Wait for the tool result before continuing your reasoning.

Question: {question}
```

### Code Execution Tool

```
You can execute Python code to help solve problems.

To run code, use:
```python
# Your code here
```

I will execute the code and show you the output.

Problem: {problem}

Think about what calculations or data processing would help, then write and run the necessary code.
```

## 9. Verification Prompts

### Self-Verification

```
{problem}

After solving, verify your answer by:
1. Checking your calculations
2. Testing edge cases
3. Confirming the answer makes sense

Solution:
[Your solution]

Verification:
[Your verification steps]

Final confirmed answer:
```

### Cross-Check Prompt

```
Verify this solution is correct:

Problem: {problem}
Proposed solution: {solution}

Check for:
- Logical errors
- Calculation mistakes
- Missing edge cases
- Incorrect assumptions

Is this solution correct? If not, what needs to be fixed?
```

## 10. System Prompts for Reasoning Agents

### General Reasoning Agent

```
You are an advanced AI reasoning assistant. Your approach:

1. UNDERSTAND: Carefully read and comprehend the request
2. PLAN: Outline your approach before executing
3. EXECUTE: Work through the problem methodically
4. VERIFY: Check your work for errors
5. RESPOND: Provide a clear, well-structured answer

For complex problems, break them into smaller parts. Show your reasoning when it adds clarity.
```

### Code Generation Agent

```
You are an expert programmer who writes high-quality code.

Process:
1. Understand requirements fully before coding
2. Consider edge cases and error handling
3. Write clean, documented code
4. Explain key design decisions

When solving coding problems:
- Start with the approach
- Implement step by step
- Test with examples
- Optimize if needed
```

### Research Agent

```
You are a thorough research assistant. Your process:

1. Identify what information is needed
2. Search for relevant sources
3. Verify information from multiple sources when possible
4. Synthesize findings into a coherent response
5. Note uncertainties and limitations

Always cite sources and indicate confidence levels.
```

## 11. Domain-Specific Prompts

### Mathematical Proof

```
Prove the following mathematical statement rigorously.

Statement: {statement}

Requirements:
- State all assumptions clearly
- Use formal logical steps
- Justify each step
- Address edge cases
- Conclude with QED

Proof:
```

### Code Debugging

```
Debug this code. The expected behavior is: {expected}
The actual behavior is: {actual}

```{language}
{code}
```

Process:
1. Understand what the code should do
2. Trace through the logic to find the bug
3. Explain why the bug occurs
4. Provide the corrected code

Debug analysis:
```

### Architecture Decision

```
Make an architecture decision for the following scenario.

Context: {context}
Requirements: {requirements}
Constraints: {constraints}

Consider at least 3 options. For each:
- Describe the approach
- List pros and cons
- Estimate complexity

Then recommend the best option with justification.
```

## 12. Few-Shot Reasoning Examples

### Math Problem Solving

```
Solve math problems by showing clear reasoning.

Example:
Problem: A rectangle has a perimeter of 36 cm. If its length is 3 times its width, find its dimensions.

Solution:
Let width = w, then length = 3w
Perimeter = 2(length + width) = 2(3w + w) = 2(4w) = 8w
8w = 36
w = 4.5 cm
length = 3(4.5) = 13.5 cm
Answer: Width = 4.5 cm, Length = 13.5 cm

---

Now solve:
Problem: {problem}

Solution:
```

### Code Analysis

```
Analyze code for potential issues.

Example:
Code:
```python
def divide(a, b):
    return a / b
```

Analysis:
- Issue: No handling for division by zero
- Issue: No type checking for inputs
- Severity: High - will crash on b=0
- Fix: Add validation and try/except

---

Now analyze:
```{language}
{code}
```

Analysis:
```

## Usage Guidelines

### For OpenAI o3/o4

1. Keep prompts simple - the model reasons internally
2. Don't over-specify reasoning steps
3. Use `reasoning_effort` parameter instead of prompt engineering
4. Structured output requests work well

### For Claude Extended Thinking

1. Give high-level guidance, not step-by-step instructions
2. Trust the model's creative problem-solving
3. Use multishot examples with `<thinking>` patterns
4. Adjust `budget_tokens` based on complexity

### For DeepSeek R1

1. Explicitly request reasoning with `<think>` tags
2. The model naturally produces verbose reasoning
3. Be aware of potential language mixing in reasoning
4. Parsing `<think>` blocks gives insight into the process

### For Standard Models with CoT

1. Use explicit "think step by step" instructions
2. Provide few-shot examples of reasoning
3. Use XML tags to structure output
4. Verify results when accuracy is critical
