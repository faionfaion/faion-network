<!--
purpose: Skeleton binary-label LLM-as-judge prompt with positive/negative examples.
consumes: {input, model_output} per case
produces: one line `label=<positive|negative> // reason`
depends-on: content/01-core-rules.xml r5 (no contamination)
token-budget-impact: ~150 tokens per case
-->
# {{label_a}} vs {{label_b}} judge

You are an automated judge. You will receive an INPUT and the MODEL_OUTPUT under test.

Output ONE line: `label=<{{label_a}}|{{label_b}}> // <one-sentence reason>`

## Definitions

- **{{label_a}}**: [precise behavioural definition]
- **{{label_b}}**: [precise behavioural definition; mutually exclusive with {{label_a}}]

## Examples (DO NOT MATCH ON ANY CASE FROM holdout.jsonl)

INPUT: [synthetic example 1 input]
MODEL_OUTPUT: [synthetic example 1 output that exemplifies {{label_a}}]
→ `label={{label_a}} // [1-sentence justification]`

INPUT: [synthetic example 2 input]
MODEL_OUTPUT: [synthetic example 2 output that exemplifies {{label_b}}]
→ `label={{label_b}} // [1-sentence justification]`

## Now judge

INPUT:
{{input}}

MODEL_OUTPUT:
{{model_output}}
