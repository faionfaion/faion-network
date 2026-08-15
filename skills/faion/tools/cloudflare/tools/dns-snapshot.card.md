# dns-snapshot

## Purpose
Writes one Cloudflare zone's DNS records as canonically ordered JSONL and fails when they differ from a committed baseline, printing only the names that moved. Commit the snapshot, run it in CI, and a hand edit in the dashboard becomes a failed build instead of a discovery during an outage.

## Invoke
```
python3 {script} --zone {example.com} [--out {dns.jsonl}] [--baseline {dns.jsonl}] [--type {A,CNAME}] [--self-test]
```

## Inputs
- `--zone {name}` — the zone to snapshot. Required unless self-testing. The credential is read from the environment variable `CLOUDFLARE_API_TOKEN` and nowhere else; there is no flag for it, and its least privilege is Zone Read plus DNS Read, resource-scoped to this one zone.
- `--out {file}` — write the canonical JSONL snapshot here; this is the file you commit as the next baseline. Optional, nothing written by default.
- `--baseline {file}` — a previously committed snapshot to diff against. Optional; without it the run only snapshots and can never report drift.
- `--type {list}` — comma-separated record types to keep, e.g. `A,CNAME`. Optional, default every type. The filter is applied to the baseline too, so a filtered diff stays honest.
- `--self-test` — run the built-in fixtures and exit. Makes no network call and needs no credential. Optional.

## Outputs
- Files: `{out}` — one JSON object per line, keys sorted, records ordered by name then type then content, each reduced to name, type, content, ttl, proxied, priority. Same remote state, same bytes.
- stdout: `dns-snapshot: zone=example.com records=N drift=M`
- stderr: one line per changed name and type — `added`, `removed`, or `changed old -> new`. Never the whole zone and never a response body.
- Exit: `0` no drift, or no baseline given · `1` the zone differs from the baseline, or a failed self-test · `2` cannot run: no `--zone`, unreadable or malformed baseline, no such zone visible to this token, unwritable `--out` · `3` CLOUDFLARE_API_TOKEN is unset · `4` credential rejected, 401 or 403 · `6` vendor API error, including a 429.

## When NOT to use
- Editing DNS. It only reads, and the token it wants has no write permission at all.
- Judging whether a record is correct. It reports difference from the baseline and nothing else.
- Following one record through a type change. In-place type changes were removed from the API (EOL 2026-06-30), so A to CNAME correctly arrives as one `removed` and one `added` line.

## Cost
Zero model calls. One zone lookup plus one GET per 100 records, with `result_info.total_pages` driving the loop and a 200-page ceiling. Read-only, so no purge-style rate limit applies.
