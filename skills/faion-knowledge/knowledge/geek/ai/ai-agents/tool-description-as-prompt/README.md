# Tool Description as Prompt

**Category:** `tu-` (tool use)

## The Rule

A tool's `description` field is part of the prompt the model sees on every turn. Treat tool descriptions as zero-shot teaching: state when to call this tool, what inputs are required, what output to expect, and when NOT to call it. Tool description quality moves benchmark scores more than swapping the model.

## Empirical anchor

Anthropic's engineering team reported that improving tool descriptions (without changing the model) achieved **state-of-the-art on SWE-bench**. Description engineering is now part of the eval loop, not a docstring afterthought.

## Why It Works

A tool definition becomes part of the system context every time the model decides whether to call a tool. The description IS the prompt the model uses to:

1. Decide whether *this* tool is the right one for the current sub-goal
2. Decide what to put in `input` (arguments)
3. Interpret the result when it comes back

A vague description ("get info about a thing") collapses the model's discrimination between similar tools — wrong tool gets called, or the model invents implausible arguments.

## When To Use

- Always — but most teams under-invest. The bar is "write your tool descriptions as if they were the system prompt of a junior engineer being asked to use this for the first time."

## What Belongs in a Tool Description

1. **Verb_object name** that hints at what it does (`search_docs`, not `docs`)
2. **One-sentence "use this when ..."** trigger
3. **One-sentence "do NOT use this when ..."** anti-trigger (very high leverage)
4. **Input contract** if not obvious from the schema (e.g., "path is relative to repo root")
5. **Output shape & limits** ("returns up to 50 results, ranked by relevance, JSON-line format")
6. **Composition hints** ("call `validate_path` first if path source is untrusted")

## When NOT To Use

- Skipping tool descriptions altogether (very common — and very wrong)
- Copying the function docstring verbatim — function docs target humans, tool descriptions target the LLM. Different audiences, different priorities.
- Tool descriptions that contradict the input_schema (e.g., describing pagination but no `page` param)

## Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| `description: "Search the docs"` | Add when-to-use, when-NOT-to-use, output shape |
| Marketing prose ("Powerful, AI-driven, real-time...") | Strip all of it — model doesn't care |
| Description longer than 200 tokens | Tighten — long descriptions lose the model's attention |
| Describes implementation ("uses Bedrock under the hood") | Cut — model only needs the contract |
| Tools with overlapping descriptions | Differentiate via the "do NOT use this when..." line |

## Composition

- + **tool naming**: verb_object names + tight description = lowest tool-selection error rate
- + **strict mode**: input_schema enforced; description teaches *when* to use, schema enforces *how*
- + **idempotent + preview/apply pairs**: descriptions explicitly state side-effects ("modifies the database; pair with `dry_run_query` first")

## References

Source: [Anthropic Engineering — Tool Use Best Practices (Claude Code/SWE-bench)](https://www.anthropic.com/engineering/swe-bench-sonnet) | [Anthropic Tool Use docs](https://docs.anthropic.com/claude/docs/tool-use)

See `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.
