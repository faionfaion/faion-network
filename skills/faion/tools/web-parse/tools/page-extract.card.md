# page-extract

## Purpose
Turns the HTML in a polite-fetch cache into readable text or markdown plus its structured layer — JSON-LD, OpenGraph, microdata — one pass per page, into a JSONL file. Read the JSONL, never the HTML: that is the whole compression argument. It also tells you which pages yielded nothing worth reading, so a scrape that silently produced boilerplate fails loudly.

## Invoke
```
python3 {script} --cache {dir} --out {pages.jsonl} [--format {text|markdown}] [--structured] [--min-text-len {200}] [--self-test]
```

## Inputs
- `--cache {dir}` — a cache directory written by polite-fetch, holding `ledger.jsonl`. Required; the ledger is the page list and its outcomes.
- `--out {file}` — destination JSONL, one object per page with url, title, lang, words, chars and text. Required, because extracted content never goes to stdout.
- `--format {text|markdown}` — prose shape. Optional, default `text`. Markdown keeps heading level, list, quote and code-block shape, and renders links.
- `--structured` — add the JSON-LD, OpenGraph and microdata block to each record. Optional, off by default; parsing happens either way, in the same pass.
- `--min-text-len {n}` — characters below which a page counts as a finding. Optional, default 200.
- `--self-test` — run the built-in fixtures and exit. Optional, opens no socket.

## Outputs
- Files: `{out}` — JSONL, one object per extracted page, keys sorted, non-ASCII kept as itself.
- stdout: `page-extract: pages=N extracted=E short=S degraded=D -> path`
- stderr: one line per short page, per body that is not HTML, and per unreadable body.
- Exit, first that applies: `2` cannot run — missing arguments, no ledger, unwritable output · `3` the ledger records a robots.txt skip, so the corpus is truncated and any conclusion drawn from it is partial · `4` a page parsed degraded: undecodable bytes, unusable JSON-LD, or a body that is not HTML · `1` a page fell under `--min-text-len` · `0` every page extracted.

## When NOT to use
- Authenticated pages. It reads what polite-fetch cached, and polite-fetch declines to log in; a members-only page in the cache means someone bypassed the pack, and the fix is upstream.
- Personal data extraction. No email, phone or address field is ever emitted from any structured block, and an email in prose is redacted to `[email]`. That is deliberate and not configurable.
- Anything needing a real DOM: computed styles, script-built content, iframe contents, or CSS selectors against a live tree. This is a token stream with a corrected depth stack, not a browser.

## Cost
Zero model calls. Zero network calls. One parse per cached page, linear in page size; a few hundred pages is seconds. Output size is the real cost driver — keep it in the file and read what you need.
