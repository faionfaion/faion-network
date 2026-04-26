# Checklist — Subagent as Context Firewall

## Design

- [ ] Subagent has its own system prompt instructing it to return summary + refs only
- [ ] Subagent output schema is strict: `summary`, `refs`, `confidence` — no raw content
- [ ] Parent's prompt does NOT ask the subagent to "include everything you found"
- [ ] Subagent has a token cap (typically 500-2000 output tokens)

## Quality

- [ ] Subagent runs on a fresh context — no parent state leaks in
- [ ] Subagent return is < 500 tokens 95% of the time
- [ ] Refs returned by subagent are validated (parent should be able to re-read each)
- [ ] On subagent failure, parent receives `{confidence: "low", summary: "subagent failed: ..."}` — never silent

## Composition

- [ ] Heavy work (reading, searching, planning) lives inside the firewall
- [ ] Light work (synthesis, decision) lives in parent context
- [ ] Multiple subagents share state via FILES, not via parent context
- [ ] Subagent boundary slims content — parent does not re-pass full subagent output to another subagent

## Cost & Latency

- [ ] Subagent uses appropriate model — not always strongest (Haiku for filter-style tasks)
- [ ] Subagent latency is acceptable for the parent's loop budget
- [ ] Subagent invocations are logged with token-cost per invocation

## Anti-pattern checks

- [ ] No subagent returns "the full text of what I read"
- [ ] No subagent's report contains > 5 quotations of > 10 words from sources
- [ ] No subagent inherits parent's full context (if it needs main context, pass refs not content)
