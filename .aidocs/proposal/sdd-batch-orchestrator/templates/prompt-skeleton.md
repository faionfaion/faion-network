# Subagent prompt: <Phase Name>

You <one-paragraph mission statement: what this subagent is for, what side effects it may have, what language it communicates in>.

## Inputs (orchestrator passes these in spawn message)

- `<param-1>` — <type and meaning>
- `<param-2>` — <type and meaning>
- `<optional-param>` (optional) — <when used>

## Pre-flight

- <env vars / credentials that must be present>
- <state assumptions that must hold (e.g., default branch matches origin)>
- <reference files to read first>

## Workflow

1. <concrete first step>
2. <concrete second step>
3. <concrete third step>
   - <sub-step>
   - <sub-step>
4. <concrete final step that produces the output>

## Output

<Either the report shape (markdown block schema), the files written (paths + meaning), or the structured result returned to the orchestrator.>

## Constraints

- ❌ NO <hard prohibition 1>
- ❌ NO <hard prohibition 2>
- ✅ <required positive 1>
- ✅ <required positive 2>

## Done condition

<Observable check that lets the orchestrator decide success vs failure. One paragraph.>
