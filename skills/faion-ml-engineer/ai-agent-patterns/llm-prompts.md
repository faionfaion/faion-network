# LLM Prompts for AI Agent Creation

Prompts for generating, analyzing, and improving AI agents.

---

## Agent Design Prompts

### Generate Agent Architecture

```
Design an AI agent for the following use case:

Use Case: {{USE_CASE}}
Requirements:
- {{REQUIREMENT_1}}
- {{REQUIREMENT_2}}
- {{REQUIREMENT_3}}

Constraints:
- Model: {{MODEL_NAME}}
- Max tokens per call: {{TOKEN_LIMIT}}
- Latency requirement: {{LATENCY_MS}}

Provide:
1. Recommended agent pattern(s)
2. System architecture diagram (text-based)
3. Tool definitions
4. Prompt templates
5. Error handling strategy
6. Observability requirements
```

### Pattern Selection Assistant

```
Help me choose the right agent pattern.

Task Description: {{TASK}}

Answer these questions to guide selection:

1. Is external data or action required?
   YES -> Tool Use pattern

2. Is the task dynamic with uncertain paths?
   YES -> ReAct pattern

3. Are there multiple distinct phases?
   YES -> Plan-Execute pattern

4. Is output quality critical?
   YES -> Add Reflection layer

5. Are multiple expertise areas needed?
   YES -> Multi-Agent pattern

Based on the task, recommend:
- Primary pattern
- Secondary patterns to combine
- Implementation approach
- Expected trade-offs
```

### Tool Design Assistant

```
Design tools for an AI agent.

Agent Purpose: {{AGENT_PURPOSE}}
Target Tasks: {{TASK_EXAMPLES}}

For each tool, provide:
1. Name (verb_noun format)
2. Clear description (what it does, when to use)
3. Parameters with types and descriptions
4. Return value format
5. Error conditions
6. Example usage

Consider:
- Tool granularity (not too broad, not too narrow)
- Parameter clarity (model must understand how to use)
- Error messages (helpful for recovery)
```

---

## Agent Improvement Prompts

### Agent Performance Analysis

```
Analyze the performance of this agent configuration.

Agent System Prompt:
{{SYSTEM_PROMPT}}

Tools Available:
{{TOOLS}}

Sample Interactions:
{{INTERACTION_LOG}}

Analyze:
1. Task completion rate
2. Average steps to completion
3. Tool usage patterns
4. Common failure modes
5. Token efficiency

Provide:
- Specific improvement recommendations
- Prompt refinements
- Tool adjustments
- Pattern modifications
```

### Prompt Optimization

```
Optimize this agent prompt for better performance.

Current Prompt:
{{CURRENT_PROMPT}}

Issues Observed:
{{ISSUES}}

Optimization Goals:
- Clearer instructions
- Fewer unnecessary steps
- Better tool selection
- Reduced token usage

Provide optimized prompt with:
1. Explanation of changes
2. Expected improvements
3. Potential trade-offs
```

### Failure Analysis

```
Analyze this agent failure case.

Task: {{TASK}}

Agent Trace:
{{FULL_TRACE}}

Failure Point: {{FAILURE_DESCRIPTION}}

Analyze:
1. Root cause of failure
2. Could it have been prevented?
3. What signals indicated impending failure?
4. Recovery options that could have worked

Recommend:
- Prompt changes to prevent similar failures
- Additional tools or checks needed
- Error handling improvements
```

---

## Pattern-Specific Prompts

### ReAct Pattern Enhancement

```
Improve this ReAct agent configuration.

Current System Prompt:
{{REACT_PROMPT}}

Available Tools:
{{TOOLS}}

Observed Issues:
- {{ISSUE_1}}
- {{ISSUE_2}}

Improve:
1. Thought generation (more focused, relevant)
2. Action selection (better tool matching)
3. Observation processing (extract key info)
4. Termination (know when to stop)

Provide enhanced prompt with annotations explaining changes.
```

### Reflection Loop Calibration

```
Calibrate this reflection loop.

Current Configuration:
- Max cycles: {{MAX_CYCLES}}
- Critique prompt: {{CRITIQUE_PROMPT}}
- Revision prompt: {{REVISION_PROMPT}}

Observed Issues:
- {{ISSUE}} (e.g., loops too long, never satisfies)

Calibrate:
1. Exit conditions (when is "good enough"?)
2. Critique specificity (actionable feedback)
3. Revision guidance (focused improvements)
4. Cycle limits (cost-benefit balance)

Provide calibrated configuration with rationale.
```

### Plan-Execute Optimization

```
Optimize this Plan-Execute agent.

Planning Prompt:
{{PLANNER_PROMPT}}

Execution Prompt:
{{EXECUTOR_PROMPT}}

Sample Plans Generated:
{{SAMPLE_PLANS}}

Issues:
- {{ISSUE}} (e.g., plans too vague, steps overlap)

Optimize:
1. Plan granularity (right level of detail)
2. Step dependencies (explicit ordering)
3. Execution handoff (clear context passing)
4. Replanning triggers (when to adjust)

Provide optimized prompts with examples.
```

---

## Multi-Agent Prompts

### Agent Team Design

```
Design a multi-agent team for this project.

Project: {{PROJECT_DESCRIPTION}}
Deliverables: {{DELIVERABLES}}

Design:
1. Agent roles needed
2. Capabilities per agent
3. Coordination pattern
4. Communication protocol
5. Conflict resolution
6. Success criteria

For each agent provide:
- Role name
- System prompt
- Tools assigned
- Interaction rules
```

### Coordinator Agent Prompt

```
You are the coordinator for a multi-agent system.

Your Team:
{{#each agents}}
{{name}}: {{capabilities}}
{{/each}}

Your Responsibilities:
1. Decompose incoming tasks
2. Route subtasks to appropriate agents
3. Monitor progress and quality
4. Handle conflicts between agents
5. Synthesize final outputs

Communication Protocol:
- Address agents by name
- Provide clear, specific instructions
- Request status updates when needed
- Escalate issues that can't be resolved

Current Task: {{TASK}}

Plan your coordination approach:
```

### Agent Handoff Protocol

```
Design a handoff protocol between agents.

Agents Involved:
- {{AGENT_A}}: {{CAPABILITIES_A}}
- {{AGENT_B}}: {{CAPABILITIES_B}}

Handoff Context:
{{HANDOFF_POINT}}

Design:
1. Information to transfer
2. Format of handoff message
3. Acknowledgment process
4. Rollback if handoff fails
5. Audit trail

Provide handoff template for both directions.
```

---

## Testing and Validation Prompts

### Agent Test Case Generation

```
Generate test cases for this agent.

Agent Purpose: {{PURPOSE}}
Tools: {{TOOLS}}
Expected Behaviors: {{BEHAVIORS}}

Generate test cases covering:
1. Happy path scenarios
2. Edge cases
3. Error conditions
4. Tool failure recovery
5. Ambiguous inputs
6. Multi-step workflows

For each test case provide:
- Input
- Expected behavior
- Success criteria
- Edge conditions to verify
```

### Agent Benchmark Prompt

```
Create a benchmark suite for agent evaluation.

Agent Type: {{AGENT_TYPE}}
Primary Pattern: {{PATTERN}}

Benchmark Dimensions:
1. Task completion accuracy
2. Step efficiency
3. Token efficiency
4. Error recovery
5. Consistency across runs

For each dimension:
- Define metric
- Create 5+ test cases
- Establish baseline
- Set target thresholds
```

### Regression Testing

```
Design regression tests for agent changes.

Previous Version: {{PREVIOUS_CONFIG}}
New Version: {{NEW_CONFIG}}
Changes Made: {{CHANGES}}

Regression Tests:
1. Core functionality unchanged
2. Performance not degraded
3. New features work correctly
4. Edge cases still handled
5. Integration points stable

Test execution plan:
- Priority order
- Pass/fail criteria
- Rollback triggers
```

---

## Observability Prompts

### Trace Analysis

```
Analyze this agent execution trace.

Trace:
{{FULL_TRACE}}

Extract:
1. Decision points and choices made
2. Tool usage patterns
3. Token consumption by step
4. Latency breakdown
5. Potential improvements

Summary:
- Total tokens:
- Total latency:
- Steps taken:
- Tools used:
- Efficiency score:
```

### Alert Configuration

```
Configure monitoring alerts for this agent.

Agent: {{AGENT_NAME}}
Pattern: {{PATTERN}}
SLA Requirements:
- Max latency: {{MAX_LATENCY}}
- Max tokens: {{MAX_TOKENS}}
- Min success rate: {{SUCCESS_RATE}}

Define alerts for:
1. Latency threshold exceeded
2. Token budget exhausted
3. Error rate spike
4. Infinite loop detection
5. Unusual tool usage

For each alert:
- Trigger condition
- Severity level
- Notification channel
- Remediation steps
```

---

## Cost Optimization Prompts

### Token Budget Analysis

```
Analyze token usage for this agent.

Execution Logs:
{{TOKEN_LOGS}}

Analyze:
1. Token distribution by step type
2. Highest token-consuming operations
3. Unnecessary token usage
4. Caching opportunities
5. Prompt compression potential

Provide:
- Current cost estimate
- Optimization opportunities
- Expected savings
- Implementation priority
```

### Model Selection Optimization

```
Optimize model selection for this agent pipeline.

Current Configuration:
- All steps use: {{CURRENT_MODEL}}

Step Analysis:
{{#each steps}}
{{name}}: {{complexity}}, {{requirements}}
{{/each}}

Recommend model per step:
- Complex reasoning: {{LARGE_MODEL}}
- Simple execution: {{SMALL_MODEL}}
- Structured output: {{STRUCTURED_MODEL}}

Calculate:
- Current estimated cost
- Optimized estimated cost
- Quality trade-offs
```
