<!--
purpose: Few-shot CoT prompt skeleton with 2 worked reasoning examples.
consumes: task + new input
produces: model output following the shown reasoning shape
depends-on: content/01-core-rules.xml r1
token-budget-impact: + ~400 tokens for the worked examples; output still doubles
-->
# Few-shot CoT prompt

Solve the following task. Show your reasoning between `<reasoning>` and `</reasoning>` and the final answer between `<answer>` and `</answer>`.

## Example 1

Input: {{example_1_input}}
<reasoning>
{{example_1_reasoning_steps}}
</reasoning>
<answer>{{example_1_answer}}</answer>

## Example 2

Input: {{example_2_input}}
<reasoning>
{{example_2_reasoning_steps}}
</reasoning>
<answer>{{example_2_answer}}</answer>

## Now solve

Input: {{actual_input}}
