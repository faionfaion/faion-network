# LLM Prompts for Chain-of-Thought

Effective prompts for using LLMs to assist with CoT implementation, debugging, and optimization.

## Table of Contents

1. [CoT Design Assistance](#cot-design-assistance)
2. [Technique Selection](#technique-selection)
3. [Debugging CoT Issues](#debugging-cot-issues)
4. [Optimization](#optimization)
5. [Evaluation and Testing](#evaluation-and-testing)
6. [Learning and Analysis](#learning-and-analysis)

---

## CoT Design Assistance

### Design CoT Prompt for Task

```
Help me design a chain-of-thought prompt for this task.

Task: {TASK_DESCRIPTION}

Input type: {INPUT_TYPE}
Output type: {OUTPUT_TYPE}
Complexity: {LOW/MEDIUM/HIGH}

Requirements:
- {REQUIREMENT_1}
- {REQUIREMENT_2}

Constraints:
- Model: {MODEL_NAME}
- Token budget: {MAX_TOKENS}
- Latency requirement: {MAX_LATENCY}

Design a CoT prompt that:
1. Encourages step-by-step reasoning
2. Produces consistent, parseable outputs
3. Handles edge cases gracefully
4. Stays within constraints

Provide:
- Complete prompt template
- Recommended CoT variant (zero-shot, few-shot, etc.)
- Example of expected reasoning
- Potential issues to watch for
```

### Generate Few-Shot CoT Examples

```
Generate few-shot examples with chain-of-thought reasoning for this task.

Task: {TASK_DESCRIPTION}

Input format: {INPUT_FORMAT}
Output format: {OUTPUT_FORMAT}

Generate 3 diverse examples that:
1. Show clear step-by-step reasoning
2. Cover different scenarios (typical, edge case, tricky)
3. Use consistent formatting
4. Demonstrate correct reasoning patterns

For each example:
<example>
Problem: [Input]
<thinking>
Step 1: [First reasoning step]
Step 2: [Next step]
...
</thinking>
<answer>[Output]</answer>
Difficulty: [easy/medium/hard]
What this example teaches: [Why it's useful]
</example>
```

### Convert Direct Prompt to CoT

```
Convert this direct prompt to use chain-of-thought reasoning.

Original prompt:
<prompt>
{ORIGINAL_PROMPT}
</prompt>

The prompt currently works but could benefit from explicit reasoning.

Create a CoT version that:
1. Adds appropriate trigger phrase
2. Structures thinking section
3. Separates reasoning from answer
4. Maintains original functionality

Provide:
- CoT version of the prompt
- Comparison of expected behavior
- When to use original vs CoT version
```

---

## Technique Selection

### Recommend CoT Technique

```
Help me choose the right chain-of-thought technique for my use case.

Use case: {USE_CASE_DESCRIPTION}

Task characteristics:
- Reasoning complexity: {LOW/MEDIUM/HIGH}
- Answer type: {SINGLE/MULTIPLE/OPEN_ENDED}
- Accuracy requirement: {STANDARD/HIGH/CRITICAL}
- Latency tolerance: {LOW/MEDIUM/HIGH}
- Budget: {LIMITED/MODERATE/FLEXIBLE}

Available techniques:
1. Zero-shot CoT ("Let's think step by step")
2. Few-shot CoT (with examples)
3. Self-consistency (multiple samples + voting)
4. Tree-of-Thoughts (exploration + evaluation)
5. Least-to-Most (decomposition)

Recommend:
- Primary technique with reasoning
- Alternative if primary doesn't work
- Configuration parameters
- Implementation considerations
- Expected accuracy vs cost trade-off
```

### Compare CoT Approaches

```
Compare these CoT approaches for my specific task.

Task: {TASK_DESCRIPTION}

Current approach: {CURRENT_APPROACH}

Alternative to consider: {ALTERNATIVE_APPROACH}

Compare on:
1. Expected accuracy improvement
2. Token cost per request
3. Latency impact
4. Implementation complexity
5. Failure modes

Provide:
- Side-by-side comparison table
- Recommendation with reasoning
- Scenarios where each excels
- Migration strategy if switching
```

### Determine If CoT Is Needed

```
Help me determine if chain-of-thought is beneficial for this task.

Task: {TASK_DESCRIPTION}

Current approach: {CURRENT_APPROACH}
Current accuracy: {ACCURACY}%
Current issues: {ISSUES}

Questions to answer:
1. Does this task require multi-step reasoning?
2. Would explicit reasoning improve accuracy?
3. Is the additional latency/cost justified?
4. Are there simpler alternatives?

Analysis:
- CoT benefit likelihood: [high/medium/low]
- Expected improvement: [quantitative if possible]
- Recommended action: [use CoT / don't use CoT / test both]
- Alternative solutions to consider
```

---

## Debugging CoT Issues

### Debug Poor Reasoning Quality

```
Help me debug this CoT prompt that produces poor reasoning.

Prompt:
<prompt>
{PROMPT}
</prompt>

Example input: {INPUT}

Expected reasoning:
<expected>
{EXPECTED_REASONING}
</expected>

Actual reasoning:
<actual>
{ACTUAL_REASONING}
</actual>

Problems observed:
- {PROBLEM_1}
- {PROBLEM_2}

Diagnose:
1. What's wrong with the current reasoning?
2. Why is the model producing this output?
3. What in the prompt is causing this?

Provide:
- Root cause analysis
- Specific fixes to the prompt
- Improved prompt version
- Test cases to verify fix
```

### Fix Inconsistent CoT Outputs

```
My CoT prompt produces inconsistent reasoning. Help me stabilize it.

Prompt:
<prompt>
{PROMPT}
</prompt>

Same input, different runs:
Output 1: {OUTPUT_1}
Output 2: {OUTPUT_2}
Output 3: {OUTPUT_3}

Desired behavior: {DESIRED_BEHAVIOR}

Analyze:
1. What varies between outputs?
2. What in the prompt allows this variation?
3. Is the variation in reasoning or just answer?

Fix by:
- Making instructions more specific
- Adding structural constraints
- Providing clearer examples
- Adjusting temperature (currently: {TEMPERATURE})

Provide improved prompt that produces consistent reasoning.
```

### Debug Self-Consistency Failures

```
Self-consistency isn't improving my results. Help me diagnose.

Base prompt:
<prompt>
{PROMPT}
</prompt>

Configuration:
- Samples: {NUM_SAMPLES}
- Temperature: {TEMPERATURE}

Results:
- Agreement rate: {AGREEMENT}%
- Accuracy: {ACCURACY}%
- Expected improvement: {EXPECTED}%

Sample outputs:
{SAMPLE_OUTPUTS}

Analyze:
1. Are the reasoning paths diverse enough?
2. Is the answer format consistent for comparison?
3. Is the task appropriate for self-consistency?
4. Are there systematic errors across paths?

Provide:
- Diagnosis of the issue
- Recommended parameter adjustments
- Prompt modifications if needed
- Alternative approach if self-consistency isn't suitable
```

### Fix Answer Extraction Issues

```
I'm having trouble extracting answers from CoT responses.

Prompt:
<prompt>
{PROMPT}
</prompt>

Example responses that fail parsing:
{RESPONSE_1}
---
{RESPONSE_2}

Current extraction method: {EXTRACTION_METHOD}

Problems:
- {PARSING_ISSUE_1}
- {PARSING_ISSUE_2}

Help me:
1. Understand why extraction is failing
2. Modify prompt for more consistent format
3. Improve extraction logic
4. Handle edge cases gracefully

Provide:
- Improved prompt with stricter format
- Regex/parsing code for extraction
- Fallback handling for edge cases
```

---

## Optimization

### Optimize CoT Token Usage

```
Help me reduce token usage in this CoT prompt while maintaining quality.

Current prompt:
<prompt>
{PROMPT}
</prompt>

Current token usage: ~{TOKENS} per request
Target: {TARGET_TOKENS} tokens

Constraints:
- Must maintain reasoning quality
- Must keep answer accuracy at {ACCURACY}%+
- Cannot change: {UNCHANGEABLE_PARTS}

Optimize by:
1. Reducing verbosity in instructions
2. Shortening examples if present
3. Compressing reasoning structure
4. Using more efficient phrasing

Provide:
- Optimized prompt
- Token count comparison
- Trade-offs made
- Quality verification approach
```

### Optimize Self-Consistency Configuration

```
Help me optimize self-consistency parameters for my use case.

Task: {TASK_DESCRIPTION}
Current config:
- Samples: {NUM_SAMPLES}
- Temperature: {TEMPERATURE}
- Aggregation: {METHOD}

Current results:
- Accuracy: {ACCURACY}%
- Cost: ${COST} per query
- Latency: {LATENCY}ms

Goals:
- Maintain accuracy at {TARGET_ACCURACY}%+
- Reduce cost to ${TARGET_COST}
- OR reduce latency to {TARGET_LATENCY}ms

Optimize:
1. Is sample count optimal?
2. Is temperature appropriate for diversity?
3. Is aggregation method best for this task?

Provide:
- Recommended configuration
- Expected accuracy/cost trade-off
- Testing strategy to validate
```

### Simplify Complex CoT Flow

```
My CoT implementation has become complex. Help simplify.

Current flow:
{FLOW_DESCRIPTION}

Components:
1. {COMPONENT_1}
2. {COMPONENT_2}
3. {COMPONENT_3}

Pain points:
- {PAIN_POINT_1}
- {PAIN_POINT_2}

Goals:
- Reduce complexity
- Maintain accuracy
- Improve maintainability

Analyze:
1. Which components are essential?
2. What can be combined or eliminated?
3. Is a simpler technique sufficient?

Provide:
- Simplified architecture
- Migration path from current
- Trade-offs of simplification
```

---

## Evaluation and Testing

### Generate CoT Test Cases

```
Generate comprehensive test cases for evaluating this CoT prompt.

Prompt:
<prompt>
{PROMPT}
</prompt>

Expected behavior: {EXPECTED_BEHAVIOR}

Generate test cases for:

1. **Normal Cases** (5 cases)
   - Typical inputs that should work well
   - Varying complexity levels

2. **Edge Cases** (5 cases)
   - Boundary conditions
   - Unusual but valid inputs

3. **Failure Cases** (3 cases)
   - Inputs that might break reasoning
   - Ambiguous situations

4. **Adversarial Cases** (2 cases)
   - Inputs designed to confuse
   - Common failure modes

For each case provide:
{
  "id": "TC-001",
  "category": "normal|edge|failure|adversarial",
  "input": "...",
  "expected_reasoning": "Key steps that should appear",
  "expected_answer": "...",
  "what_it_tests": "..."
}
```

### Create CoT Evaluation Rubric

```
Create an evaluation rubric for assessing CoT outputs.

Task: {TASK_DESCRIPTION}

Evaluate reasoning quality on these dimensions:

1. **Logical Coherence** (weight: X%)
   - Steps follow logically
   - No contradictions
   - Valid inferences

2. **Completeness** (weight: X%)
   - All necessary steps present
   - No gaps in reasoning
   - Assumptions stated

3. **Relevance** (weight: X%)
   - Steps address the problem
   - No tangential reasoning
   - Efficient path to answer

4. **Correctness** (weight: X%)
   - Calculations are accurate
   - Facts are correct
   - Conclusion matches reasoning

5. **Clarity** (weight: X%)
   - Easy to follow
   - Well-organized
   - Appropriate detail level

For each dimension, define:
| Score | Description | Example |
|-------|-------------|---------|
| 5 | Excellent | ... |
| 4 | Good | ... |
| 3 | Acceptable | ... |
| 2 | Below average | ... |
| 1 | Poor | ... |
```

### Analyze CoT Failure Patterns

```
Analyze failures in my CoT implementation to identify patterns.

Prompt:
<prompt>
{PROMPT}
</prompt>

Failed cases:
Case 1:
Input: {INPUT_1}
Expected: {EXPECTED_1}
Actual: {ACTUAL_1}

Case 2:
Input: {INPUT_2}
Expected: {EXPECTED_2}
Actual: {ACTUAL_2}

Case 3:
Input: {INPUT_3}
Expected: {EXPECTED_3}
Actual: {ACTUAL_3}

Analyze:
1. Common patterns across failures
2. Root causes (prompt, model, task)
3. Categories of failure types
4. Severity of each pattern

Provide:
- Failure pattern taxonomy
- Priority ranking (by frequency/impact)
- Specific fixes for top patterns
- Prevention strategies
```

---

## Learning and Analysis

### Explain CoT Technique

```
Explain the {TECHNIQUE_NAME} chain-of-thought technique.

Cover:
1. **Concept**: What is it and how does it work?
2. **When to use**: What tasks benefit most?
3. **When NOT to use**: Contraindications
4. **Implementation**: Step-by-step guide
5. **Simple example**: Basic demonstration
6. **Advanced example**: Complex application
7. **Common mistakes**: What to avoid
8. **Best practices**: Key success factors
9. **Comparison**: How it differs from other CoT variants
10. **Recent developments**: 2025 research insights

Include code examples where helpful.
```

### Analyze Research Paper on CoT

```
Summarize and analyze this CoT research for practical application.

Paper: {PAPER_TITLE_OR_CONTENT}

Extract:
1. **Key contribution**: Main innovation or finding
2. **How it works**: Technical approach
3. **Results**: Performance improvements shown
4. **Limitations**: Acknowledged or observed
5. **Practical applicability**: Can I use this today?
6. **Implementation requirements**: What's needed
7. **Trade-offs**: Costs vs benefits

Provide:
- Executive summary (3-5 sentences)
- Actionable takeaways
- Implementation recommendations
- Questions to investigate further
```

### Compare CoT Evolution (2022-2026)

```
Compare how chain-of-thought prompting has evolved from 2022 to 2026.

Cover:
1. **Original CoT (2022)**: Wei et al.'s introduction
2. **Self-Consistency (2022)**: Wang et al.'s improvement
3. **Zero-Shot CoT (2022)**: Kojima et al.'s simplification
4. **Tree-of-Thoughts (2023)**: Yao et al.'s expansion
5. **Recent advances (2024-2026)**: Latest developments

For each:
- Core innovation
- Performance gains
- When it's most useful
- Current relevance

Key trends:
- What's becoming more/less important
- How model capabilities affect CoT value
- Future directions
```

### Understand CoT Reasoning Process

```
Help me understand how {MODEL_NAME} processes this CoT prompt.

Prompt:
<prompt>
{PROMPT}
</prompt>

Input: {INPUT}
Output: {OUTPUT}

Explain:
1. How is the model interpreting the instructions?
2. What triggers the step-by-step reasoning?
3. How does it decide what steps to include?
4. Why did it reach this particular answer?
5. What could cause different behavior?

This helps me:
- Understand model behavior
- Predict edge case behavior
- Design better prompts
- Debug failures
```

---

## Quick Reference: When to Use Each Prompt

| Situation | Recommended Prompt |
|-----------|-------------------|
| Starting new CoT implementation | Design CoT Prompt for Task |
| Choosing technique | Recommend CoT Technique |
| CoT not working | Debug Poor Reasoning Quality |
| Inconsistent results | Fix Inconsistent CoT Outputs |
| High token costs | Optimize CoT Token Usage |
| Need test coverage | Generate CoT Test Cases |
| Understanding failures | Analyze CoT Failure Patterns |
| Learning new technique | Explain CoT Technique |
| Evaluating research | Analyze Research Paper on CoT |

---

## Tips for Using These Prompts

1. **Be specific about context** - Include actual prompts, outputs, and configurations
2. **Provide examples** - Show what's working and what's failing
3. **State constraints** - Token limits, latency requirements, accuracy targets
4. **Include metrics** - Current performance numbers when available
5. **Iterate** - Use improvement prompts multiple times
6. **Test suggestions** - Validate recommendations before deployment
7. **Document learnings** - Keep notes on what works for your use case
