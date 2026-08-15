# source-table

## Purpose
Turn a JSONL of research claims into a markdown evidence table, a gaps report and a numbered ledger of the claims that could move what the product earns; fail the run when a load-bearing claim has no source or a commercial claim has no lever.

## Invoke
```
python3 {script} --in {claims.jsonl} [--out {table.md}] [--report {gaps.md}] [--levers {levers.jsonl}] [--title {heading}] [--require-date] [--self-test]
```

## Inputs
- `--in {claims.jsonl}` — one JSON object per line, `-` for stdin. Required unless self-testing. Blank lines and `#` comments ignored. Per object:
  - `claim` — string, required, non-empty.
  - `url` — `http(s)` string; optional in the schema, **required** for a load-bearing claim.
  - `date` — `YYYY-MM-DD`; optional, any other form is reported as a gap.
  - `confidence` — string or number; optional, absence is reported.
  - `load_bearing` — bool; optional, default `true`. Set `false` for colour and context.
  - `commercial` — bool; optional, default `false`. `true` when the claim names something that could move what the product earns. Anything but a bool is malformed input. A `true` claim marked not load-bearing is a gap.
  - `lever` — string; **required** when `commercial` is `true`: the action the claim implies, in the product's own terms, not the claim restated.
- `--out {table.md}` — table destination. Optional, default stdout.
- `--report {gaps.md}` — gaps destination. Optional, default stderr when gaps exist.
- `--levers {levers.jsonl}` — ledger destination. Optional; written whenever given, empty when nothing is tagged.
- `--title {heading}` — H2 above the table. Optional, default `Evidence table`.
- `--require-date` — also fail when a load-bearing claim carries no valid date. Optional.
- `--self-test` — run the built-in fixtures and exit. Needs no other flag; writes only inside a temporary directory. Optional.

## Outputs
- Files: `{out}` — `# | Claim | Source | Date | Confidence | Load-bearing | Commercial lever`, unsourced rows marked `**missing**`; `{report}` — one bullet per gap, prefixed with the input line number; `{levers}` — one JSON object per tagged claim, `{"id","lever","claim","url","date","confidence"}`, ids `C1..Cn` in input order.
- stdout: `source-table: claims=N sourced=M unsourced_load_bearing=K missing_confidence=J missing_date=D commercial=C unnamed_levers=U -> path`
- Exit: `0` every load-bearing claim sourced and every commercial claim levered · `1` at least one unsourced (or undated under `--require-date`, or commercial without a lever), or a failed self-test · `2` no `--in`, unreadable input, invalid JSON, non-object line, a non-bool `commercial`, or an empty/missing `claim`.

## When NOT to use
- To fetch, resolve or check that a URL is live — it validates the shape of the field, never the endpoint.
- To judge whether a source actually supports its claim; that is a reading task, not a gate.
- On prose with inline citations — convert to JSONL first.

## Cost
Zero model calls. Milliseconds; a single pass over the input.
