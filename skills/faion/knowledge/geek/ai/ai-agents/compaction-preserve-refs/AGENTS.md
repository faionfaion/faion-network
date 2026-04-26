# Compaction Templates That Preserve References

## Summary

When a long-running agent must compact its conversation to free context, the compaction prompt must hard-code which fields survive and which are dropped. Always preserve: file paths, function names, error messages, decisions, URLs, IDs. Always drop: intermediate reasoning chains and verbatim tool output. The compacted summary is itself a manifest of references — not a narrative — so the agent can re-fetch any dropped detail by path or ID instead of re-reasoning from scratch.

## Why

Free-form compaction prompts ("summarize the conversation so far") let the model invent the schema each time. The result drifts: sometimes the file paths survive, sometimes the reasoning does, sometimes a critical error message gets paraphrased into uselessness. Anthropic's context-engineering cookbook and lethain's "Building an internal agent" both report that the failure mode of post-compaction agents is loss of pointers, not loss of prose: the model has the gist but cannot find the file it was about to edit. A schema'd compaction protects exactly the data the agent needs to resume.

## When To Use

- Any agent loop expected to exceed ~30 turns or its context window — compaction will trigger.
- Multi-session SDD work where the next session reads the compacted output and resumes.
- Pipelines where compaction is automated by middleware (opencode, Claude Code auto-compaction).
- Whenever the agent depends on file paths, error texts, or external IDs to make progress.

## When NOT To Use

- Stateless single-turn agents — there is no later step that needs the references.
- Conversations that compact only the user-facing answer for display, not for the agent's own continuation.
- Agents whose only "state" is a closed-form result (a number, a yes/no) — references add noise.

## Content

| File | What's inside |
|------|---------------|
| `content/01-keep-drop.xml` | The hard rule: which fields are mandatory, which are forbidden in compacted output. |
| `content/02-template.xml` | Concrete YAML schema the compaction prompt must enforce; example output. |

## Templates

| File | Purpose |
|------|---------|
| `templates/compaction-prompt.txt` | Drop-in compaction system prompt enforcing the references-only schema. |
| `templates/compacted-state.yaml` | Reference compacted-state file structure with all required keys. |
