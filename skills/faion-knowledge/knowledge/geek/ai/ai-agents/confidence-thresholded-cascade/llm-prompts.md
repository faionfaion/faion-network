# LLM Prompts — Confidence-Thresholded Cascade

## Prompt 1: Cheap-model answer-with-confidence

```
You are a fast classifier. Read the input and emit STRICT JSON:
{
  "reasoning": "1-2 sentences",
  "answer": "...",
  "confidence_0_to_1": 0.0-1.0,
  "requires_escalation": false
}

Calibration rules:
- 1.0 ONLY if you are certain (textbook case)
- 0.8-0.95 if confident but a slim chance you're wrong
- 0.5-0.8 if you have a good guess but real uncertainty
- < 0.5 means you are guessing — set requires_escalation=true

Input:
{input}
```

## Prompt 2: Strong-model fallback

```
A cheaper model declined this task with low confidence. Solve it with full reasoning.

Cheap model's attempt:
{cheap_attempt}

Confidence: {confidence}

Task:
{task}

Output: STRICT JSON with reasoning then answer.
```

## Prompt 3: Calibration audit

```
Given this evaluation data (confidence vs actual_correctness for 100 tasks), report:
1. Calibration curve (binned)
2. Optimal threshold for ≥ 95% accuracy retention
3. Escalation rate at that threshold
4. Cost savings vs always-strong

Data:
{eval rows}
```

## Prompt 4: Cascade-mode picker

```
For this task, recommend:
- single_strong | cheap_then_strong (2-level) | three_level

Considerations:
- Volume per day
- Mission-critical?
- Confidence elicitable?
- Latency-sensitive?

Output STRICT JSON: {recommendation, rationale}.

Task profile:
{description}
```
