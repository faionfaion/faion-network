# api-call

## Purpose
One authenticated transport for GitHub Issues, Linear and ClickUp, driven by per-vendor profiles, that returns only the fields `--select` names. Reach for it whenever the alternative is an agent paying for a vendor's whole JSON envelope to read three values out of it.

## Invoke
```
python3 {script} --profile {github} --op {list-issues} [--param {k=v}] [--body {payload.json}] [--select {items[].title}] [--out {rows.jsonl}] [--profiles {vendors.json}] [--pages {5}] [--max {25}] [--dry-run] [--yes] [--self-test]
```

## Inputs
- `--profile {name}` — `github`, `linear` or `clickup`. Required unless self-testing. The credential is read from `GITHUB_TOKEN`, `LINEAR_API_KEY` or `CLICKUP_TOKEN`, falling back to the pack-level `FAION_TRACKER_TOKEN`, and from nowhere else — there is no flag for it. GitHub is sent a Bearer prefix; Linear and ClickUp take the raw value and reject a prefixed one.
- `--op {name}` — operation within the profile. Required. GitHub: `list-issues`, `get-issue`, `create-issue`, `update-issue`. Linear: `list-issues`, `query`, `create-issue`, `update-issue`. ClickUp: `list-tasks`, `create-task`, `update-task`.
- `--param {k=v}` — repeatable. Fills the path template (`owner`, `repo`, `number`, `list_id`, `task_id`, `id`, `teamId`); anything left over becomes a query key, or a GraphQL variable on Linear. A missing required param fails before any call.
- `--body {file}` — JSON object, JSON array or JSONL, for a write. An array or JSONL is N paced requests: that is how a bulk create happens on ClickUp, which has no bulk endpoint. Required by `create-issue`, `update-issue`, `query`, `create-task` and `update-task`.
- `--select {paths}` — comma-separated paths over `{"items": [...]}`, `[]` exploding a list, e.g. `items[].number,items[].title`. Optional; without it the items stay whole and nothing is printed.
- `--out {file}` — the selected rows as JSONL. Optional; without it stdout carries at most 20 rows and says how many it withheld.
- `--profiles {file}` — JSON of vendor to profile, merged over the built-ins, so a moved endpoint is repaired as data rather than as a release. Optional.
- `--pages {n}` — page cap, default 5. `--max {n}` — cap on the payloads one write may send, default 25.
- `--dry-run` — print the request and make no call. `--yes` — required before a mutating operation runs at all. Optional.
- `--self-test` — run the built-in fixtures and exit. Makes no network call and needs no credential. Optional.

## Outputs
- Files: `{out}` — one JSON object per line, in the shape `--select` asked for.
- stdout: `api-call: profile=github op=list-issues requests=N items=M rows=R -> path`, preceded by the selected rows when there is no `--out`.
- stderr: the exact change set before any write, and one line per problem. A response body is never printed and the credential never appears anywhere.
- Exit: `0` done · `1` a failed self-test · `2` cannot run: unknown profile or operation, a missing required param, an unreadable body or profiles file, a write over the cap · `3` no credential in the environment · `4` credential rejected, 401 or 403 · `5` a mutating operation without `--yes` · `6` vendor API error, including a 429 that outlived its retries.

## When NOT to use
- Reconciling SDD tasks against a tracker. That is sdd-sync.py, which owns the ledger and hands this tool the transport.
- A vendor with no profile. Add it as data through `--profiles`; do not reach for curl, and do not write a second client.
- Deleting anything. No profile ships a DELETE, deliberately: an irreversible operation has no dry-run worth the name.

## Cost
Zero model calls. One request per page up to `--pages`, one per payload on a write up to `--max`. Rate limits: GitHub 5,000/h authenticated, Linear 5,000/h, ClickUp 100/min on Free through Business and paced at 0.6 s between requests. A 429 is retried three times, honouring `Retry-After` and capping the wait at a minute.
