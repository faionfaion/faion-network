# source-table

## Purpose
Turn a JSONL of research claims into a markdown evidence table plus a gaps report, and fail the run when a load-bearing claim has no source.

## Invoke
```
python3 {script} --in {claims.jsonl} [--out {table.md}] [--report {gaps.md}] [--title {heading}] [--require-date]
```

## Inputs
- `--in {claims.jsonl}` — one JSON object per line, `-` for stdin. Required. Blank lines and `#` comments ignored. Per object:
  - `claim` — string, required, non-empty.
  - `url` — `http(s)` string; optional in the schema, **required** for a load-bearing claim.
  - `date` — `YYYY-MM-DD`; optional, any other form is reported as a gap.
  - `confidence` — string or number; optional, absence is reported.
  - `load_bearing` — bool; optional, default `true`. Set `false` for colour and context.
- `--out {table.md}` — table destination. Optional, default stdout.
- `--report {gaps.md}` — gaps destination. Optional, default stderr when gaps exist.
- `--title {heading}` — H2 above the table. Optional, default `Evidence table`.
- `--require-date` — also fail when a load-bearing claim carries no valid date. Optional.

## Outputs
- Files: `{out}` — `# | Claim | Source | Date | Confidence | Load-bearing`, unsourced rows marked `**missing**`; `{report}` — one bullet per gap, prefixed with the input line number.
- stdout: `source-table: claims=N sourced=M unsourced_load_bearing=K missing_confidence=J missing_date=D -> path`
- Exit: `0` every load-bearing claim sourced · `1` at least one unsourced (or undated under `--require-date`) · `2` unreadable input, invalid JSON, non-object line, or an empty/missing `claim`.

## When NOT to use
- To fetch, resolve or check that a URL is live — it validates the shape of the field, never the endpoint.
- To judge whether a source actually supports its claim; that is a reading task, not a gate.
- On prose with inline citations — convert to JSONL first.

## Cost
Zero model calls. Milliseconds; a single pass over the input.
