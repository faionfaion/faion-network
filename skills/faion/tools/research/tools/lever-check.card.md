# lever-check

## Purpose
Count a concept's answers against the commercial-lever ledger the evidence stage wrote: applied against declined, every decline with its class and reason printed, and a hard failure on a lever the concept never answered at all.

## Invoke
```
python3 {script} --ledger {levers.jsonl} --concept {verdict.json} [--report {decisions.md}] [--self-test]
```

## Inputs
- `--ledger {levers.jsonl}` — the commercial-lever ledger `source-table` wrote, one JSON object per line, each with an `id` **unique across the file**. Required unless self-testing. Blank lines and `#` comments ignored.
- `--concept {verdict.json}` — the concept verdict JSON. Required. Its `commercial_findings` array is read; absent counts as empty, present-and-not-an-array is malformed. Per entry: `id`, `lever`, `disposition` (`applied` or `declined`), `lands_in`, `reason`, `decline_class` (one of `dark-pattern`, `envelope`, `evidence`, `economics`, `dependency`, or `not-declined` when applied).
- `--report {decisions.md}` — report destination. Optional, default stdout.
- `--self-test` — run the built-in fixtures and exit. Needs no other flag; writes only inside a temporary directory. Optional.

## Outputs
- Files: `{report}` — the counts line, a row per ledger id (`id | lever | disposition | lands in / class | reason`), every decline in full, then the findings. Written whether or not the check passes: the count is the point.
- stdout: `lever-check: levers=N applied=A declined=D unanswered=U findings=F -> path`; each finding also to stderr.
- Exit: `0` every lever answered and well-formed · `1` at least one unanswered, undisposed, applied with nowhere to land, declined with no reason or no class, answered twice, answering an id the ledger does not carry, or carrying an id the ledger repeats; also a failed self-test · `2` an input is missing, unreadable, not JSON, or carries a `commercial_findings` that is not an array.

## When NOT to use
- To judge whether a reason is a good reason — it never reads for quality, only for presence and shape. That is deliberate: a gate that blocks on a judgement is talked past by rewording.
- To decide which levers matter; the ledger is the input, not the output.
- To rank or score a concept — it counts dispositions, it does not weigh them.

## Cost
Zero model calls. Milliseconds; one pass over each input.
