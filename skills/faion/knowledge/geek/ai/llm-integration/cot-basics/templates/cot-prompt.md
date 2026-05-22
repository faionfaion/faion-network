<!--
purpose: Zero-shot CoT prompt skeleton with structured tag output.
consumes: task text + sample inputs
produces: model output with reasoning + answer blocks
depends-on: content/01-core-rules.xml r1; content/02-output-contract.xml
token-budget-impact: doubles output tokens vs direct answer; budget accordingly
-->
# CoT prompt skeleton

You are solving a multi-step task. Work through it carefully.

First, output your reasoning between `<reasoning>` and `</reasoning>` tags.

Then, output the final answer (one line, no extra commentary) between `<answer>` and `</answer>` tags.

Output nothing outside these tags.

## Task

{{task}}

## Input

{{input}}
