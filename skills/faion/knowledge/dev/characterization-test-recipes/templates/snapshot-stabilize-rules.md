<!--
purpose: Reference list of canonical normalization rules for characterization snapshots.
consumes: nothing — used as authoring guide for normalize.{py,ts,go}.
produces: a stable, central normaliser the suite imports once.
depends-on: snapshot lib (syrupy / jest / approvaltests).
token-budget-impact: ~180 tokens when copied.
-->

# Snapshot Stabilize Rules

These rules belong in ONE central module (`tests/characterization/normalize.*`). Every snapshot test imports this module. NO ad-hoc per-test sanitization.

## Timestamps
- Replace any `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}` with `<TS>`.
- Replace UNIX epoch millis (10+ digit ints in `*_ms` fields) with `<EPOCH_MS>`.

## UUIDs / IDs
- Replace `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` with `<UUID>`.
- Replace auto-increment IDs in `id` / `request_id` fields with `<ID>`.

## Ordering
- Sort dicts by key (deep).
- Sort lists where ordering is unordered-by-contract; keep as-is where ordering matters (specify per field).

## PII
- Hash emails: `sha1(email)[:12]`, prefix `pii:`.
- Drop `name`, `phone`, `address` fields entirely.

## Floating-point
- Round to business-meaningful precision (cents for money, ms for SLA).

## Server-only fields
- Drop `server_version`, `computed_at_ms`, `trace_id`, `region` — incidental.

## Worked example

```python
def normalize(d: dict) -> dict:
    d = sort_keys_deep(d)
    d = replace_field_match(d, r"^\d{4}-\d{2}-\d{2}T", "<TS>")
    d = replace_field_match(d, r"^[0-9a-f]{8}-[0-9a-f]{4}", "<UUID>")
    d.pop("request_id", None)
    d.pop("computed_at_ms", None)
    return d
```
