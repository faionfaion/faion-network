# AI Agent Patterns Templates

Reusable templates for implementing agent design patterns.

---

## ReAct Agent Template

### System Prompt Template

```
You are an AI assistant that uses the ReAct framework to solve tasks.

For each step, you will:
1. THOUGHT: Reason about what you need to do next
2. ACTION: Choose an action from available tools
3. OBSERVATION: Observe the result (provided by the system)
4. Repeat until you can provide a final answer

Available Tools:
{{TOOL_LIST}}

Response Format:
Thought: <your reasoning about the current situation>
Action: <tool_name>[<tool_input>]

When you have the final answer:
Thought: I now have enough information to answer.
Action: finish[<your final answer>]

Remember:
- Think before acting
- Use observations to inform next steps
- Be concise but thorough
```

### Tool Definition Template

```json
{
  "name": "{{TOOL_NAME}}",
  "description": "{{CLEAR_DESCRIPTION_OF_WHAT_TOOL_DOES}}",
  "parameters": {
    "type": "object",
    "properties": {
      "{{PARAM_NAME}}": {
        "type": "{{TYPE}}",
        "description": "{{PARAM_DESCRIPTION}}"
      }
    },
    "required": ["{{REQUIRED_PARAMS}}"]
  }
}
```

---

## Chain-of-Thought Templates

### Zero-Shot CoT

```
{{QUESTION}}

Let's approach this step by step:
```

### Few-Shot CoT

```
I'll solve problems by showing my reasoning step by step.

Example 1:
Question: {{EXAMPLE_Q1}}
Reasoning: {{STEP_BY_STEP_REASONING_1}}
Answer: {{ANSWER_1}}

Example 2:
Question: {{EXAMPLE_Q2}}
Reasoning: {{STEP_BY_STEP_REASONING_2}}
Answer: {{ANSWER_2}}

Now solve this:
Question: {{USER_QUESTION}}
Reasoning:
```

### Self-Consistency Aggregation

```
I've generated multiple reasoning paths:

Path 1: {{REASONING_1}} -> Answer: {{ANSWER_1}}
Path 2: {{REASONING_2}} -> Answer: {{ANSWER_2}}
Path 3: {{REASONING_3}} -> Answer: {{ANSWER_3}}

Most consistent answer: {{MAJORITY_ANSWER}}
Confidence: {{ANSWER_COUNT}}/{{TOTAL_PATHS}} paths agree
```

---

## Tool Use Templates

### Tool System Prompt

```
You have access to the following tools:

{{#each tools}}
## {{name}}
Description: {{description}}
Parameters:
{{#each parameters}}
  - {{name}} ({{type}}{{#if required}}, required{{/if}}): {{description}}
{{/each}}
{{/each}}

When you need to use a tool, respond with:
```json
{
  "tool": "<tool_name>",
  "parameters": {
    "<param1>": "<value1>",
    ...
  }
}
```

After receiving the tool result, incorporate it into your response.
Only use tools when necessary. If you can answer directly, do so.
```

### Tool Result Integration

```
Tool: {{TOOL_NAME}}
Input: {{TOOL_INPUT}}
Result: {{TOOL_OUTPUT}}

Based on this information, {{CONTINUE_REASONING}}
```

---

## Plan-Execute Templates

### Planner Prompt

```
You are a strategic planner. Create a detailed plan to accomplish the objective.

Objective: {{OBJECTIVE}}

Context:
{{CONTEXT}}

Create a numbered step-by-step plan:
1. Each step should be specific and actionable
2. Include dependencies between steps
3. Estimate complexity for each step (Low/Medium/High)

Plan:
```

### Executor Prompt

```
You are an executor. Complete the assigned step based on the plan.

Overall Objective: {{OBJECTIVE}}

Previous Steps Completed:
{{#each completed_steps}}
Step {{index}}: {{description}}
Result: {{result}}
{{/each}}

Current Step: {{current_step}}

Execute this step. Provide:
1. The completed work
2. Any observations or issues
3. Recommendations for next steps
```

### Replanner Prompt

```
The original plan needs adjustment based on execution results.

Original Objective: {{OBJECTIVE}}

Original Plan:
{{ORIGINAL_PLAN}}

Completed Steps:
{{COMPLETED_STEPS}}

Issue Encountered:
{{ISSUE}}

Create a revised plan that:
1. Accounts for completed work
2. Addresses the encountered issue
3. Maintains progress toward the objective

Revised Plan:
```

---

## Reflection Templates

### Critique Prompt

```
Evaluate the following output against specific criteria.

Task: {{ORIGINAL_TASK}}

Output to Evaluate:
{{OUTPUT}}

Evaluation Criteria:
{{#each criteria}}
- {{name}}: {{description}}
{{/each}}

For each criterion, provide:
1. Score (1-5)
2. Specific issues found
3. Concrete suggestions for improvement

If all criteria score 4 or above, respond: "SATISFACTORY"
Otherwise, provide detailed critique.
```

### Revision Prompt

```
Revise the output based on the critique provided.

Original Task: {{ORIGINAL_TASK}}

Previous Output:
{{PREVIOUS_OUTPUT}}

Critique:
{{CRITIQUE}}

Create an improved version that:
1. Addresses each point in the critique
2. Maintains the original intent
3. Improves overall quality

Revised Output:
```

### Self-Critique Prompt

```
Review your own work critically.

Task: {{TASK}}

Your Output:
{{OUTPUT}}

Self-Evaluation Questions:
1. Does this fully address the task requirements?
2. Are there any logical errors or inconsistencies?
3. Is the output clear and well-organized?
4. What could be improved?

If satisfied, respond: "APPROVED"
Otherwise, identify specific improvements needed.
```

---

## Tree-of-Thoughts Templates

### Thought Generation

```
Problem: {{PROBLEM}}

Current State:
{{CURRENT_STATE}}

Generate {{NUM_BRANCHES}} different approaches to proceed:

Approach 1: [Description of first approach]
Approach 2: [Description of second approach]
Approach 3: [Description of third approach]

For each approach, briefly explain the reasoning and potential outcomes.
```

### Thought Evaluation

```
Problem: {{PROBLEM}}

Proposed Approach:
{{APPROACH}}

Evaluate this approach:
1. Likelihood of success (0-1):
2. Potential risks:
3. Resource requirements:
4. Key assumptions:

Overall viability score (0-1):
```

### Path Synthesis

```
Problem: {{PROBLEM}}

Explored Paths:
{{#each paths}}
Path {{index}}:
Steps: {{steps}}
Score: {{score}}
{{/each}}

Best Path: Path {{best_path_index}}

Synthesize the solution following this path:
```

---

## Multi-Agent Templates

### Agent Definition

```yaml
name: {{AGENT_NAME}}
role: {{ROLE_DESCRIPTION}}
goal: {{SPECIFIC_GOAL}}
backstory: {{BACKGROUND_CONTEXT}}
tools:
  {{#each tools}}
  - {{name}}
  {{/each}}
constraints:
  {{#each constraints}}
  - {{description}}
  {{/each}}
```

### Coordinator Prompt

```
You are the coordinator agent managing a team of specialists.

Specialists Available:
{{#each specialists}}
- {{name}}: {{capabilities}}
{{/each}}

Current Task: {{TASK}}

Task History:
{{HISTORY}}

Decide your next action:
1. DELEGATE: Assign subtask to a specialist
2. SYNTHESIZE: Combine results from specialists
3. FINISH: Task complete, return final result

Response format:
Action: <DELEGATE|SYNTHESIZE|FINISH>
Target: <specialist_name or "all">
Instructions: <specific instructions or final result>
```

### Agent Handoff

```
You are receiving a handoff from {{PREVIOUS_AGENT}}.

Context:
{{HANDOFF_CONTEXT}}

Previous Work:
{{PREVIOUS_WORK}}

Your Role: {{YOUR_ROLE}}

Your Task:
{{SPECIFIC_TASK}}

Complete your portion and prepare handoff for the next agent.
```

---

## Utility Templates

### Error Recovery

```
An error occurred during execution.

Step: {{FAILED_STEP}}
Error: {{ERROR_MESSAGE}}
Context: {{ERROR_CONTEXT}}

Recovery Options:
1. Retry with different parameters
2. Skip and proceed to next step
3. Abort and return partial results

Choose recovery strategy and explain reasoning:
```

### Token Budget Management

```
Current token usage: {{CURRENT_TOKENS}} / {{MAX_TOKENS}}
Remaining budget: {{REMAINING_TOKENS}}

Based on remaining budget:
- If > 80% remaining: Continue with full detail
- If 50-80% remaining: Summarize intermediate steps
- If 20-50% remaining: Focus on essential information only
- If < 20% remaining: Conclude immediately

Current recommendation: {{RECOMMENDATION}}
```

### Observability Logging

```json
{
  "timestamp": "{{TIMESTAMP}}",
  "agent": "{{AGENT_ID}}",
  "pattern": "{{PATTERN_TYPE}}",
  "step": {{STEP_NUMBER}},
  "action": "{{ACTION_TYPE}}",
  "input": "{{INPUT_SUMMARY}}",
  "output": "{{OUTPUT_SUMMARY}}",
  "tokens_used": {{TOKENS}},
  "latency_ms": {{LATENCY}},
  "success": {{SUCCESS}},
  "error": "{{ERROR_IF_ANY}}"
}
```
