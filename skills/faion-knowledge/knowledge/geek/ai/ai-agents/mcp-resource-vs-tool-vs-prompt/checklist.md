# Checklist — MCP Resource vs Tool vs Prompt

## Design

- [ ] Listed every capability the MCP server will expose
- [ ] For each, applied the three-question test
- [ ] Classified each as exactly one of {Tool, Resource, Prompt}
- [ ] No capability classified as Tool that always returns the same content
- [ ] No capability classified as Resource that has side effects
- [ ] No capability classified as Tool that's meant for user invocation

## Tools

- [ ] Each Tool has verb_object name (`search_docs` not `docs`)
- [ ] Each Tool has structured description (use-when / NOT-use-when / I/O / side-effects)
- [ ] Mutating tools tagged with explicit "MUTATING" in description
- [ ] Idempotent tools clearly stated
- [ ] Preview/apply pairs exist for high-risk mutations

## Resources

- [ ] Each Resource has a stable URI scheme
- [ ] Resource content is deterministic per URI (or has a clear refresh policy)
- [ ] Large resources are split or paginated
- [ ] Read-only — no mutation possible

## Prompts

- [ ] Each Prompt is parameterized for user invocation
- [ ] Prompt names reflect user-facing slash-command UX
- [ ] Prompt body composes Tools/Resources where useful

## Composition

- [ ] Tools and Resources are NOT duplicated (the same data exposed both ways)
- [ ] Prompts can call Tools internally where helpful
- [ ] Cross-runtime parity considered (Anthropic / OpenAI / Vercel / LangChain)
