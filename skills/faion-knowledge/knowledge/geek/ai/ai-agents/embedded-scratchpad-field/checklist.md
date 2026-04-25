# Checklist — Embedded Scratchpad Field

## Design

- [ ] Identified which schemas have non-trivial decisions
- [ ] Each such schema has a scratchpad / reasoning / plan_steps / evidence field
- [ ] Scratchpad field comes BEFORE the answer field
- [ ] Field name matches the type of thinking required (reasoning vs evidence vs plan)

## Description

- [ ] Scratchpad description tells the model WHAT to think about (not just "think")
- [ ] Description references the input (or the goal) so the model re-grounds
- [ ] Description sets a length expectation if the answer benefits from a specific depth

## Verify

- [ ] Compared output quality with vs without scratchpad on 20+ tasks
- [ ] Scratchpad isn't just paraphrase of input — measure originality
- [ ] Scratchpad output is being USED in production (not just generated and ignored)
- [ ] No regression in latency that outweighs the quality gain

## Anti-pattern checks

- [ ] No scratchpad placed after the answer
- [ ] No multiple competing scratchpads in one schema
- [ ] No scratchpad on schemas where the answer is forced by enum (already constrained enough)
- [ ] No scratchpad on simple transformation tasks (waste of tokens)

## Composition

- [ ] Field order: scratchpad → intermediate fields → answer
- [ ] Descriptions reinforce the dependency (later fields explicitly reference earlier ones)
- [ ] If using extended thinking + scratchpad: pick one; doubling adds cost without gain
