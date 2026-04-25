# Checklist — Schema Field Order

Apply this when designing or reviewing a structured-output schema.

## Design

- [ ] List every field your schema produces
- [ ] For each pair (A, B), ask: does B depend on A? If yes, A must come before B
- [ ] Identify the "final answer" field — it should be LAST
- [ ] Identify any "reasoning / scratchpad / plan" fields — they go BEFORE the answer
- [ ] Identify "echo / restate" fields — they re-ground long inputs; place near the start

## Review

- [ ] No field commits to a value before its inputs exist
- [ ] No `id` / `slug` / `tags` field is positioned before the content it derives from
- [ ] No `confidence` / `score` field is before the answer it scores
- [ ] No `next_action` / `decision` is before the `analysis`
- [ ] Field descriptions explicitly reference earlier fields where useful

## Verify

- [ ] Compared output quality: schema-correct order vs reversed order, on at least 5 tasks
- [ ] Counted hallucinations on the dependent field — should drop with correct order
- [ ] Kept the schema; no need for an extra reasoning step or post-hoc fix

## Composition with other tricks

- [ ] If using extended thinking / `thinking` blocks, the in-schema reasoning still helps as additional grounding for the OUTPUT phase
- [ ] If using prompt caching, the schema is part of the cached prompt — order is fixed at cache time
- [ ] If chaining steps, the *output* of step N becomes the *input* of step N+1 — make sure step N's last field is what step N+1 cares about most
