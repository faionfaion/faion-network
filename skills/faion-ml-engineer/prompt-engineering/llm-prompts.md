# LLM Prompts for Prompt Engineering

Effective prompts for using LLMs to assist with prompt engineering tasks.

## Table of Contents

1. [Prompt Analysis and Improvement](#prompt-analysis-and-improvement)
2. [Prompt Generation](#prompt-generation)
3. [Debugging and Troubleshooting](#debugging-and-troubleshooting)
4. [Testing and Evaluation](#testing-and-evaluation)
5. [Learning Prompts](#learning-prompts)
6. [Advanced Techniques](#advanced-techniques)

---

## Prompt Analysis and Improvement

### Analyze Prompt Quality

```
Analyze the following prompt for effectiveness and suggest improvements.

Prompt to analyze:
<prompt>
{PROMPT_TO_ANALYZE}
</prompt>

Evaluate these aspects:

1. **Clarity**
   - Are instructions unambiguous?
   - Is the task clearly defined?

2. **Specificity**
   - Is the output format specified?
   - Are constraints explicit?

3. **Completeness**
   - Are edge cases addressed?
   - Is error handling defined?

4. **Efficiency**
   - Are there unnecessary tokens?
   - Could it be more concise?

5. **Security**
   - Is user input safely handled?
   - Are there injection vulnerabilities?

Provide:
- Score for each aspect (1-5)
- Specific issues found
- Concrete improvement suggestions
- Rewritten improved version
```

### Optimize Prompt for Specific Model

```
Optimize the following prompt for {MODEL_NAME} (Claude/GPT-4/Gemini).

Original prompt:
<prompt>
{ORIGINAL_PROMPT}
</prompt>

Model-specific considerations for {MODEL_NAME}:
- {MODEL_SPECIFIC_FEATURES}

Optimize for:
1. Best formatting practices for this model
2. Effective use of model-specific features
3. Token efficiency
4. Reliable output quality

Provide:
- Optimized prompt
- Explanation of changes made
- Model-specific tips applied
```

### Simplify Complex Prompt

```
Simplify the following prompt while maintaining its effectiveness.

Original prompt:
<prompt>
{COMPLEX_PROMPT}
</prompt>

Goals:
- Reduce token count by at least 30%
- Maintain same output quality
- Keep essential instructions
- Remove redundancy

Provide:
1. Simplified prompt
2. Token count comparison (estimate)
3. What was removed and why
4. Any potential quality trade-offs
```

### Add Structure to Prompt

```
Add proper structure to this unstructured prompt.

Unstructured prompt:
<prompt>
{UNSTRUCTURED_PROMPT}
</prompt>

Apply these structural improvements:
1. Separate sections with clear delimiters/tags
2. Organize instructions logically
3. Add explicit output format
4. Include examples if beneficial
5. Add error handling

Output:
- Restructured prompt using XML tags
- Explanation of structural decisions
```

---

## Prompt Generation

### Generate Prompt from Task Description

```
Create an effective prompt based on this task description.

Task: {TASK_DESCRIPTION}

Input type: {INPUT_TYPE}
Output type: {OUTPUT_TYPE}
Use case: {USE_CASE}
Target audience: {AUDIENCE}

Requirements:
- {REQUIREMENT_1}
- {REQUIREMENT_2}
- {REQUIREMENT_3}

Generate a prompt that:
1. Has clear instructions
2. Specifies output format
3. Includes 2-3 examples if helpful
4. Handles edge cases
5. Is optimized for production use

Provide:
- Complete prompt template
- Variable placeholders clearly marked
- Usage notes
- Example of filled prompt
```

### Generate Few-Shot Examples

```
Generate few-shot examples for the following task.

Task description:
{TASK_DESCRIPTION}

Input format:
{INPUT_FORMAT}

Output format:
{OUTPUT_FORMAT}

Generate 3-5 diverse examples that:
1. Cover typical cases
2. Include at least one edge case
3. Show correct output format
4. Are realistic and representative
5. Don't overlap significantly

Format each example as:
<example>
Input: [example input]
Output: [example output]
Note: [why this example is useful]
</example>
```

### Generate System Prompt

```
Create a system prompt for the following use case.

Use case: {USE_CASE}
Role: {DESIRED_ROLE}
Domain: {DOMAIN}
Tone: {DESIRED_TONE}

Constraints:
- {CONSTRAINT_1}
- {CONSTRAINT_2}

Behaviors to encourage:
- {BEHAVIOR_1}
- {BEHAVIOR_2}

Behaviors to avoid:
- {AVOID_1}
- {AVOID_2}

Generate a system prompt that:
1. Establishes clear identity and role
2. Sets appropriate boundaries
3. Defines response style
4. Includes guardrails for safety
5. Addresses common edge cases

Provide:
- Complete system prompt
- Explanation of key design decisions
- Suggested user prompt format
```

### Generate Chain-of-Thought Prompt

```
Convert this task into a chain-of-thought prompt.

Task:
{TASK_DESCRIPTION}

Current prompt (if exists):
<prompt>
{CURRENT_PROMPT}
</prompt>

Create a CoT version that:
1. Breaks down reasoning into steps
2. Shows how to approach the problem
3. Includes thinking and answer sections
4. Has example reasoning path

Provide:
- CoT prompt template
- Example of filled reasoning
- When to use vs. direct prompting
```

---

## Debugging and Troubleshooting

### Debug Incorrect Outputs

```
Help me debug this prompt that produces incorrect outputs.

Prompt:
<prompt>
{PROMPT}
</prompt>

Expected output:
<expected>
{EXPECTED_OUTPUT}
</expected>

Actual output (example):
<actual>
{ACTUAL_OUTPUT}
</actual>

Analyze:
1. What's the discrepancy?
2. Why might the model produce this output?
3. What in the prompt is causing this?

Provide:
- Root cause analysis
- Specific fix recommendations
- Fixed prompt version
- Test cases to verify fix
```

### Fix Inconsistent Outputs

```
This prompt produces inconsistent outputs. Help me make it more reliable.

Prompt:
<prompt>
{PROMPT}
</prompt>

Example outputs (same input, different runs):
Output 1: {OUTPUT_1}
Output 2: {OUTPUT_2}
Output 3: {OUTPUT_3}

Desired output format/style:
{DESIRED_OUTPUT}

Analyze:
1. What's causing the inconsistency?
2. Which parts of the prompt are ambiguous?

Provide:
- More specific prompt version
- Additional constraints to add
- Recommended temperature setting
- Format enforcement techniques
```

### Fix Format Compliance Issues

```
The model isn't following the specified output format. Help me fix this.

Prompt:
<prompt>
{PROMPT}
</prompt>

Expected format:
{EXPECTED_FORMAT}

Actual outputs (examples):
{ACTUAL_OUTPUTS}

Diagnose and fix:
1. Is the format specification clear enough?
2. Are there conflicting instructions?
3. Would examples help?

Provide:
- Improved format specification
- Additional instructions if needed
- Example-based format demonstration
- Validation approach
```

### Reduce Hallucinations

```
This prompt causes the model to hallucinate information. Help me ground it.

Prompt:
<prompt>
{PROMPT}
</prompt>

Context/Source (if any):
<context>
{CONTEXT}
</context>

Example hallucination:
{HALLUCINATION_EXAMPLE}

Modify the prompt to:
1. Anchor responses to provided context
2. Encourage "I don't know" responses
3. Require source citations
4. Prevent fabrication

Provide:
- Grounded prompt version
- Specific anti-hallucination instructions
- Validation approach
```

### Handle Edge Cases

```
Identify and address edge cases for this prompt.

Prompt:
<prompt>
{PROMPT}
</prompt>

Normal use case:
{NORMAL_USE_CASE}

Generate:
1. List of potential edge cases
2. How the prompt might fail on each
3. Instructions to handle each edge case

Provide:
- Comprehensive edge case list
- Updated prompt with edge case handling
- Test cases for each edge case
```

---

## Testing and Evaluation

### Generate Test Cases

```
Generate comprehensive test cases for evaluating this prompt.

Prompt:
<prompt>
{PROMPT}
</prompt>

Expected behavior:
{EXPECTED_BEHAVIOR}

Generate test cases covering:
1. Normal inputs (3-5 cases)
2. Edge cases (3-5 cases)
3. Invalid inputs (2-3 cases)
4. Adversarial inputs (2-3 cases)

Format each test case as:
{
  "id": "TC-001",
  "category": "normal/edge/invalid/adversarial",
  "input": "test input",
  "expected_output": "what should happen",
  "rationale": "why this test is important"
}

Provide test cases as JSON array.
```

### Create Evaluation Rubric

```
Create an evaluation rubric for assessing outputs from this prompt.

Prompt:
<prompt>
{PROMPT}
</prompt>

Use case: {USE_CASE}

Create a rubric with:
1. 4-6 evaluation criteria
2. 1-5 scale for each criterion
3. Clear descriptions for each score level
4. Relative importance weights

Format:
## Criterion: [Name]
Weight: [X%]
Description: [What this measures]

| Score | Description |
|-------|-------------|
| 5 | [Exceptional - description] |
| 4 | [Good - description] |
| 3 | [Acceptable - description] |
| 2 | [Below average - description] |
| 1 | [Poor - description] |
```

### Compare Prompt Versions

```
Compare these prompt versions and recommend the better one.

Version A:
<version_a>
{PROMPT_VERSION_A}
</version_a>

Version B:
<version_b>
{PROMPT_VERSION_B}
</version_b>

Use case: {USE_CASE}

Compare on:
1. Clarity of instructions
2. Output quality (estimated)
3. Token efficiency
4. Edge case handling
5. Consistency (estimated)

Provide:
- Side-by-side comparison table
- Strengths/weaknesses of each
- Recommendation with reasoning
- Suggested hybrid version if applicable
```

### Evaluate Prompt Security

```
Evaluate this prompt for security vulnerabilities.

Prompt:
<prompt>
{PROMPT}
</prompt>

System context:
{SYSTEM_CONTEXT}

Check for:
1. Prompt injection vulnerabilities
2. Jailbreak susceptibility
3. Data leakage risks
4. Privilege escalation risks
5. Output manipulation risks

For each vulnerability found:
- Severity: High/Medium/Low
- Attack vector: How it could be exploited
- Mitigation: How to fix it

Provide:
- Security assessment summary
- Specific vulnerabilities found
- Hardened prompt version
- Testing recommendations
```

---

## Learning Prompts

### Explain Prompting Technique

```
Explain the {TECHNIQUE_NAME} prompting technique.

Cover:
1. What it is
2. When to use it
3. When NOT to use it
4. Step-by-step implementation
5. Simple example
6. Advanced example
7. Common mistakes
8. Best practices

Format with clear sections and code examples where applicable.
```

### Compare Prompting Techniques

```
Compare these prompting techniques for my use case.

Use case: {USE_CASE}

Techniques to compare:
1. {TECHNIQUE_1}
2. {TECHNIQUE_2}
3. {TECHNIQUE_3}

For each technique, explain:
- How it works
- Pros for this use case
- Cons for this use case
- Implementation complexity
- Token cost implications

Recommend which technique(s) to use and why.
```

### Learn from Example Prompts

```
Analyze this effective prompt and explain why it works well.

Prompt:
<prompt>
{EFFECTIVE_PROMPT}
</prompt>

Context: This prompt is used for {USE_CASE} and performs well.

Analyze:
1. Structure and organization
2. Instruction clarity
3. Use of examples
4. Output specification
5. Edge case handling
6. Any advanced techniques used

Extract:
- Key patterns to reuse
- Principles demonstrated
- Transferable techniques
```

### Understand Failure Mode

```
Help me understand why this prompt fails in certain cases.

Prompt:
<prompt>
{PROMPT}
</prompt>

Failure case:
Input: {FAILING_INPUT}
Expected: {EXPECTED}
Actual: {ACTUAL}

Explain:
1. What's happening in the model's "mind"
2. Why the prompt leads to this failure
3. What principles are being violated
4. How to think about preventing similar failures

This should be educational - I want to understand the underlying issue.
```

---

## Advanced Techniques

### Meta-Prompt for Prompt Generation

```
You are a prompt engineering expert. Generate an optimal prompt for the following task.

Task requirements:
{TASK_REQUIREMENTS}

Constraints:
{CONSTRAINTS}

Target model: {MODEL}

Your process:
1. Understand the core task
2. Identify key components needed
3. Choose appropriate technique(s)
4. Structure the prompt effectively
5. Add necessary safeguards
6. Optimize for the target model

Generate:
- Complete prompt
- Explanation of design choices
- Alternative approaches considered
- Testing recommendations
```

### Prompt Self-Improvement

```
Iteratively improve this prompt through self-critique.

Starting prompt:
<prompt>
{INITIAL_PROMPT}
</prompt>

Target performance: {TARGET}

Perform 3 improvement iterations:

Iteration 1:
- Critique current version
- Identify top 3 issues
- Apply improvements
- Show improved version

Iteration 2:
- Critique iteration 1 result
- Identify remaining issues
- Apply improvements
- Show improved version

Iteration 3:
- Critique iteration 2 result
- Final polish
- Show final version

Summary:
- What changed from start to finish
- Key improvements made
- Remaining limitations
```

### Prompt Decomposition

```
Break down this complex task into a prompt chain.

Complex task:
{COMPLEX_TASK}

Current single prompt (if exists):
<prompt>
{CURRENT_PROMPT}
</prompt>

Decompose into:
1. Identify subtasks
2. Define dependencies between subtasks
3. Create prompt for each subtask
4. Define data flow between prompts

Output:
- Decomposition diagram (text-based)
- Individual prompts for each step
- How to chain them together
- Error handling between steps
```

### Hybrid Technique Design

```
Design a hybrid prompting approach for this challenging task.

Task: {TASK_DESCRIPTION}

Challenges:
- {CHALLENGE_1}
- {CHALLENGE_2}
- {CHALLENGE_3}

Available techniques:
- Zero-shot
- Few-shot
- Chain-of-thought
- Self-consistency
- ReAct
- Tree-of-thought

Design a hybrid approach that:
1. Combines multiple techniques
2. Addresses each challenge
3. Balances quality vs. cost
4. Is practically implementable

Provide:
- Hybrid design explanation
- Complete implementation
- When to use simpler alternatives
- Complexity justification
```

### Domain-Specific Prompt Adaptation

```
Adapt this general prompt for the {DOMAIN} domain.

General prompt:
<prompt>
{GENERAL_PROMPT}
</prompt>

Target domain: {DOMAIN}
Domain specifics:
- Terminology: {DOMAIN_TERMINOLOGY}
- Constraints: {DOMAIN_CONSTRAINTS}
- Quality standards: {QUALITY_STANDARDS}

Adapt by:
1. Adding domain-specific terminology
2. Incorporating domain constraints
3. Adding relevant examples
4. Adjusting output format for domain needs
5. Including domain-specific guardrails

Provide:
- Domain-adapted prompt
- Domain-specific examples
- Glossary of added terms
- Validation criteria for domain
```

---

## Quick Reference: When to Use Each Prompt

| Situation | Recommended Prompt |
|-----------|-------------------|
| Have a prompt, need improvement | Analyze Prompt Quality |
| Starting from scratch | Generate Prompt from Task Description |
| Wrong outputs | Debug Incorrect Outputs |
| Inconsistent outputs | Fix Inconsistent Outputs |
| Model makes things up | Reduce Hallucinations |
| Need test coverage | Generate Test Cases |
| Learning new technique | Explain Prompting Technique |
| Complex task | Prompt Decomposition |
| Multiple techniques needed | Hybrid Technique Design |
| Need domain expertise | Domain-Specific Prompt Adaptation |
| Security concerns | Evaluate Prompt Security |
| Optimizing for model | Optimize Prompt for Specific Model |

---

## Tips for Using These Prompts

1. **Be specific about context** - Include actual prompts, outputs, and requirements
2. **Provide examples** - Show what's working and what's not
3. **State constraints** - Token limits, model, use case
4. **Iterate** - Use improvement prompts multiple times
5. **Validate results** - Test suggested improvements before deploying
6. **Learn from analysis** - Extract principles, not just fixes
