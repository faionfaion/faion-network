# Checklist — File-Reference Passing

## Design

- [ ] Identify the stage boundaries — where does one LLM call end and another begin?
- [ ] At every boundary, ask: am I passing CONTENT or REFS?
- [ ] If content > 1K tokens crosses a boundary, replace it with refs
- [ ] Define a stable ref format (path-style, URI-style, or domain-prefixed)
- [ ] Decide who validates refs — usually a small code step between LLM calls

## Schema

- [ ] Stage-output schema has a `refs: list[str]` field — never `content: str`
- [ ] Schema includes a brief `rationale` BEFORE the refs (schema-field-order)
- [ ] Schema constrains refs to a known manifest if possible (enum or regex)

## Validation

- [ ] After each LLM call, check every ref exists / resolves
- [ ] On hallucinated ref, retry the call with the failed ref called out — don't silently drop
- [ ] Log refs and resolution outcomes per stage

## Composition

- [ ] Cheap model picks refs (weak-model-preselection)
- [ ] Strong model uses refs to load and reason
- [ ] Subagents return refs + summary, never raw content
- [ ] Pipeline persistence stores refs, not content

## Quality

- [ ] Tested with downstream stage missing — does the pipeline gracefully fail at the load step?
- [ ] Tested with stale refs — does the load step refresh or error usefully?
- [ ] Measured token reduction vs content-passing baseline (typically 50-90%)

## Anti-pattern checks

- [ ] No stage returns "summary AND content" — that's content-passing in disguise
- [ ] No ref string contains content (no "the relevant passage starts with...")
- [ ] No ref points outside the manifest given to the LLM
