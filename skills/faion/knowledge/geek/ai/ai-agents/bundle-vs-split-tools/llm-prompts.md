# LLM Prompts — Bundle vs Split Tools

## Prompt 1: Audit tool list

```
Review this tool list. For each tool, assess:
- Does it overlap with another tool by audience and args?
- Could it be a Resource instead of a Tool?
- Is the description clear about when to use vs not?

Output: list of {tool_name, recommendation: "keep" | "merge_with(X)" | "convert_to_resource" | "split_into(A,B,C)"}.

Tools:
{paste}
```

## Prompt 2: Decide bundle vs split for a new tool family

```
You're adding tools for {domain}. List the operations you'd expose. Then decide: split into N tools, or bundle into one mode-arg tool?

Apply the rule:
- Bundle if: same audience, shared args, training-data prior, total tool count would otherwise > 25.
- Otherwise split.

Output: chosen approach + tool definitions.
```

## Prompt 3: Improve a bundled tool

```
This bundled tool has poor mode-selection accuracy. Improve it by:
- Refining mode enum values (semantic over codes)
- Tightening per-mode descriptions (when to use each)
- Adding explicit "do NOT use" lines to differentiate modes

Output: rewritten tool definition.

Current tool:
{paste}

Recent failure modes:
{examples}
```

## Prompt 4: Decide when to migrate to Resources

```
Given this tool list, identify tools that are:
- Read-only
- Deterministic per inputs
- Could be addressed via stable URI

Recommend conversion to MCP Resources where applicable.

Tools:
{paste}
```
