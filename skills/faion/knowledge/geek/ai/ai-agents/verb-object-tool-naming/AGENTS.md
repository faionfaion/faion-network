# Verb-Object Tool Naming with Namespace Prefix

## Summary

Name every agent tool as `verb_object` (`create_issue`, `search_files`) and prefix with a service namespace (`github_create_issue`, `asana_search_tasks`) when the catalog spans multiple servers or MCP gateways. Tool names matter MORE than descriptions for selection accuracy — the model parses the name first and uses the description only to disambiguate close matches. Single-token, opaque names (`search`, `manage`, `do_thing`) are the most common reason an agent picks the wrong tool.

## Why

Anthropic's tool-writing guidance reports that prefix and naming schemes meaningfully change selection accuracy on internal evals, and that small renames produce outsized swings. The mechanism: the model treats the tool list as part of the prompt, and selection is biased by lexical similarity between the user's request and the tool name. A name like `search` collides with every other server's `search` in an aggregator; a name like `manage_files` forces the model to read the full description on every turn just to figure out what verbs the tool actually supports. `verb_object` mirrors how engineers name CRUD endpoints, which Claude has seen millions of times in pre-training.

## When To Use

- Any tool catalog with five or more tools.
- Anytime tools come from multiple MCP servers or pass through an MCP gateway/aggregator.
- When wrapping third-party SDKs that already use `verb_object` (GitHub, Stripe, Asana, Jira) — keep the verb, add the namespace.
- During tool-eval iteration: rename, re-run eval, keep the better name.

## When NOT To Use

- Single-tool hobby scripts where there is only ever one `search` and no aggregator — naming is not the bottleneck.
- Inside an SDK that already enforces a non-snake_case convention (e.g., GraphQL camelCase) — match the host convention instead of fighting it.
- Don't pad with marketing nouns (`acme_corp_internal_v2_search_documents_advanced`) — long names hurt context budget and selection alike.

## Content

| File | What's inside |
|------|---------------|
| `content/01-naming-rule.xml` | The verb_object + namespace rule, mechanism, good/bad examples, antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool-naming-checklist.txt` | One-line checks before shipping a tool name. |

## References

- https://www.anthropic.com/engineering/writing-tools-for-agents
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
