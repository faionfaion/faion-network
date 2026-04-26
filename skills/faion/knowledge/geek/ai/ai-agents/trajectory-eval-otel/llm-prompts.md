# LLM Prompts — Trajectory Evaluation with OTel GenAI Spans

## Prompt 1: LLM-as-judge with structured rubric

```
You are evaluating an agent run.

Goal: {goal}
Final answer: {answer}
Trajectory (steps with thoughts/actions/results): {trajectory}

Score on three axes. Output STRICT JSON:
{
  "evidence": ["quotations supporting your scoring"],
  "outcome": {"score_0_to_1": float, "rationale": "..."},
  "trajectory": {"score_0_to_1": float, "rationale": "...", "issues": ["..."]},
  "confidence": "high" | "medium" | "low"
}

Rules:
- Evidence comes BEFORE scores (autoregressive grounding)
- Score 1.0 only if no improvement is suggestable
- "issues" is a list of trajectory anti-patterns observed
```

## Prompt 2: Diagnose a regression

```
Compare two trace summaries:

Baseline: {summary_v1}
Candidate: {summary_v2}

Output STRICT JSON:
{
  "regression_detected": bool,
  "regressed_axes": ["outcome" | "trajectory" | "resource"],
  "likely_causes": ["..."],
  "next_diagnostic_step": "..."
}
```

## Prompt 3: Generate the eval suite

```
Given this agent's role and tools, propose a 50-task eval suite covering:
- Easy / medium / hard buckets
- Edge cases the agent likely fails on
- Adversarial inputs (prompt injection, malformed data)

Output STRICT JSON:
{
  "tasks": [
    {"id": "...", "input": "...", "expected_outcome": "...", "category": "easy|medium|hard|adversarial"}
  ]
}
```

## Prompt 4: Trajectory anti-pattern detector

```
Review this trajectory for anti-patterns:
- Tool repeated 3+ times with same args (loop)
- Long stretch of "thinking" without tool use (overthinking)
- Tool call right after the answer was reachable (wasted work)
- Skipping a recommended preview tool (unsafe action)

Output: list of detected anti-patterns with span_ids that exhibit them.

Trajectory:
{spans}
```
