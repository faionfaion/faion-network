# Checklist — Weak-Model Preselection

## Design

- [ ] Identify the input volume — is it >5K tokens with mostly irrelevant content?
- [ ] Identify the EXPENSIVE part of the task — reasoning, not filtering
- [ ] Pick a small/cheap model from the same family if possible (consistent tokenizer)
- [ ] Define the filter contract — return REFS or BOOLS, never raw content
- [ ] Set a target keep-rate (5-30% is the sweet spot)

## Implementation

- [ ] Cheap-model schema returns minimal data: `list[int]`, `list[str]`, `list[{id, score}]`
- [ ] Strong-model receives ONLY the filtered subset
- [ ] Fallback path: empty filter result → pass full set OR retry with relaxed prompt
- [ ] Log keep-rate per run for monitoring

## Quality gates

- [ ] Sample 20 runs — measure recall (did the cheap model drop important items?)
- [ ] If recall < 95% on critical items, tighten the cheap-model prompt or use a slightly stronger filter model
- [ ] Track latency: cheap-model stage should add <30% overhead (cheap models are fast)

## Cost

- [ ] Measured tokens-saved per run
- [ ] Confirmed cost-per-task is lower (not just compute-time per stage)
- [ ] No regression in answer quality vs single-strong-model baseline (validate on 50+ tasks)

## Composition

- [ ] Cheap model uses schema-field-order rule (reasoning before refs)
- [ ] Pipeline state stores ONLY refs between stages, never the cheap model's full reasoning trace
- [ ] When chaining 3+ stages, each is preselected by the previous one's cheap-stage output
