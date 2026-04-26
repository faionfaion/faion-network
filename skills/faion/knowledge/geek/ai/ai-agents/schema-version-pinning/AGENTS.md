# Versioned SO Contracts — schema_version Pin in Every Payload

## Summary

Every Pydantic model used as an SO `text_format` or tool `input_schema` carries a `schema_version: Literal["vN"] = "vN"` discriminator field, and each pipeline event/log persists it. When a schema changes you bump the version and keep the previous parser registered for at least one rollback window. Strict mode forces the model to emit the declared literal, so events are guaranteed-tagged at the source. Silent schema drift — the dominant failure mode in multi-stage agent pipelines — becomes a typed branch dispatcher: "v3" events route to the v3 parser, "v4" to v4, unknown versions raise loudly instead of corrupting downstream state.

## Why

Multi-step agent pipelines (extract → enrich → score → publish) span days of replay, weeks of backfill, and months of stored events. Without an in-payload version, a producer change ripples silently — old consumers parse new events, fail in unexpected fields, or produce wrong derived data. Versioned contracts replace this with three guarantees: (1) every event self-identifies its schema, (2) consumers route by version explicitly, (3) backfill jobs can run old and new schemas in parallel for a defined rollback window. This is the same versioning pattern Kafka schema registries enforce — adapted to Pydantic + LLM SO.

## When To Use

- Multi-stage pipelines where output of stage N is input to stage N+1
- Event-sourced agent systems with replay or backfill
- Cross-team contracts where producer and consumer ship independently
- Long-running batch jobs that span schema-change releases
- Stored conversation logs you plan to re-process months later

## When NOT To Use

- One-shot scripts and exploratory notebooks — overhead not justified
- Single-process pipelines where producer and consumer always deploy together
- Schemas with no breaking changes expected ever (rare; usually wrong)

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | The `schema_version` literal rule, multi-version dispatch pattern, rollback window. |

## Templates

| File | Purpose |
|------|---------|
| `templates/versioned_schema.py` | Pydantic models v3 and v4 of the same shape with a typed dispatcher. |

## References

- [Continuous Integration for LLM Prompts — DEV](https://dev.to/kuldeep_paul/continuous-integration-for-llm-prompts-a-step-by-step-guide-to-automated-prompt-deployment-359k)
- [LLM Structured Outputs — Schema Validation for Real Pipelines (2026) — Collin Wilkins](https://collinwilkins.com/articles/structured-output)
