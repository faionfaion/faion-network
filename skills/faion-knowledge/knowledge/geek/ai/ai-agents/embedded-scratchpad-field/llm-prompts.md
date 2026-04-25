# LLM Prompts — Embedded Scratchpad Field

## Prompt 1: Add a scratchpad to a schema

```
Take this schema and add ONE scratchpad field BEFORE the answer-y fields.

Pick the right name based on the task:
- "reasoning" for analysis/decision
- "evidence" for classification with quotation
- "plan_steps" for multi-step
- "scratchpad" for free-form thinking

Write a precise description that says what to think about.

Schema:
{paste here}
```

## Prompt 2: Audit for misplaced scratchpads

```
Review every schema in this codebase. Flag any:
- Scratchpad/reasoning field placed AFTER the answer (anti-pattern)
- Multiple competing scratchpad fields in one schema
- Scratchpad description that's empty or vague
- Schemas with non-trivial answers but NO scratchpad

Output: list of issues with proposed fixes.

Schemas:
{paste}
```

## Prompt 3: Pick the right variant

```
Given this task, pick the best scratchpad variant:
- reasoning: str
- plan_steps: list[str]
- evidence: list[str]
- scratchpad: str
- tab_cot: list[Step]

Output: chosen variant + 1-sentence rationale.

Task:
{description}
```

## Prompt 4: Write the description

```
You're adding a scratchpad field to a schema. The downstream answer field is: {answer_field}.

Write a 1-2 sentence description that:
- Tells the model WHAT to think about
- References {answer_field} so the dependency is clear
- Sets a length expectation if needed

Output: just the description string.
```
