# Examples — Trajectory Evaluation with OTel GenAI Spans

## Example 1: A regression caught by trajectory score

After upgrading from Sonnet 4.5 → Sonnet 4.6, outcome stayed at 96%, but trajectory score dropped from 0.78 to 0.61: average steps went from 4.1 → 7.3.

Root cause: a tool description had been removed during the upgrade. The model now meandered before picking the right tool. Outcome eval alone would have called this a "no regression"; trajectory eval flagged it.

## Example 2: Cost regression

Outcome flat. Trajectory flat. But cost score dropped from 0.85 to 0.42 — average run cost went from $0.04 → $0.18. Cause: an upstream tool started returning verbose output (10× longer); each tool result inflated context. Trajectory looked similar but each step was 10× more expensive.

## Example 3: Cache hit rate as health metric

Tracking `gen_ai.usage.cache_read_tokens` over time showed a plateau at 65%. After investigation: a per-user variable was being interpolated into the system prompt. Removing it (moved to user message) raised cache hit rate to 92%. Cost per call dropped 35%.

## Example 4: Subagent depth detection

A subagent depth metric (how nested are the spans?) showed average depth 1.2 in week 1 → 3.4 in week 4. Cause: a refactor introduced subagents-spawning-subagents-spawning-subagents. Each layer added latency and cost without clear benefit. Flattening reduced p99 latency from 180s → 60s.

## Example 5: Replay-based debugging

Production failure: agent emitted nonsense for one specific user. Trace for the failed run showed the exact prompt + tool calls. Replaying the spans against a sandbox model reproduced the issue (was a prompt-injection from a CMS field). Fix: input sanitization. The replay capability turned a 4-hour debug session into 20 minutes.

## Example 6: LLM-as-judge with structured rubric

```python
class Judgment(BaseModel):
    evidence: list[str]      # quotations from agent's output
    matches_goal: bool
    completeness_0_to_1: float
    confidence: Literal["high", "medium", "low"]

judgment = sonnet_judge(trace=trace, rubric=rubric)
```

Schema-field-order: evidence first, judgments later — model has to ground its score in citations.

## Example 7: Exporting to Langfuse

```python
import os
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://cloud.langfuse.com/api/public/otel"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = "Authorization=Basic ..."
```

After this, all OTel spans flow to Langfuse where they're queryable as "traces" — searchable by attributes like `agent.tool.name == 'apply_patch'`.

## Example 8: Anti-example — token counts not captured

A team built a custom OTel wrapper that captured "agent_step" spans but didn't fill in token counts. Cost analytics were impossible; the only visible metric was duration. Instrumentation cost: ~30 LOC; benefit lost: ~$5K/month overspend that took 3 months to surface via the cloud bill.
