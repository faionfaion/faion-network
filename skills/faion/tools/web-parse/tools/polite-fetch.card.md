# polite-fetch

## Purpose
Fetches a URL list into an on-disk cache with a ledger, obeying robots.txt, a one-second floor between requests to a host, and per-host caps. Every other tool in the pack reads that cache, so a page is fetched once and parsed many times, and the politeness rules exist in one place instead of in each caller's throwaway loop.

## Invoke
```
python3 {script} --urls {urls.txt} --cache {dir} [--ua-contact {you@example.com}] [--max-per-domain {200}] [--rps {1}] [--timeout {20}] [--allow-domain {host}] [--refresh] [--self-test]
```

## Inputs
- `--urls {file}` — file of http(s) URLs, one per line, blank and `#` lines ignored, deduplicated and sorted. Required.
- `--cache {dir}` — cache directory, created if absent. Required.
- `--ua-contact {address}` — contact published in the User-Agent `faion-web-parse/<ver> (+<contact>)`. Optional, default `tools@faion.net`. Set your own address: it is how an operator tells you to stop. The rest of the User-Agent is fixed and cannot be made to look like a browser.
- `--max-per-domain {n}` — request cap per host per run. Optional, default 200, and silently held at 200 for any host not named by `--allow-domain`.
- `--rps {n}` — requests per second per host. Optional, default 1. It can only slow the crawl down: the one-second floor and the host's own Crawl-delay both win when they are slower.
- `--timeout {seconds}` — per-request timeout. Optional, default 20.
- `--allow-domain {host}` — a host you own or have written permission to crawl; raises its request cap to `--max-per-domain` and its wall-clock budget to 1200 s. Optional, repeatable.
- `--refresh` — revalidate cached URLs with a conditional GET carrying the stored ETag and Last-Modified. Optional; without it a URL already in the cache is never refetched.
- `--self-test` — run the built-in fixtures and exit. Optional, opens no socket.

## Outputs
- Files: `{cache}/bodies/<key>.body` the bytes as served · `{cache}/meta/<key>.json` status, content type and validators · `{cache}/ledger.jsonl` one record per URL, sorted by URL, carrying its outcome and the reason.
- stdout: `polite-fetch: urls=N fetched=F cached=C skipped=S errors=E`
- stderr: one line per skipped or errored URL, plus one per host whose robots.txt could not be read.
- Exit, first that applies: `2` cannot run — missing arguments, unreadable list, unwritable cache · `3` robots.txt disallowed a URL or could not be read, so the run was skipped or truncated · `4` a per-host request or wall-clock cap truncated the run · `1` a URL errored · `0` every URL is in the cache.

## When NOT to use
- Anything behind a login, a paywall or a consent wall. No cookie jar is installed, no Authorization header is ever synthesised, a URL carrying credentials is refused, and no flag overrides a robots.txt verdict. Wanting one means you want permission, not a flag.
- Harvesting personal data. Fetch public pages for what they say, never for whom to contact.
- Rendering JavaScript. This retrieves bytes; a page that assembles itself client-side arrives empty, and reproducing a browser is not this tool's job.

## Cost
Zero model calls. One robots.txt per host, then one request per uncached URL, at a minimum of one second between requests to a host and at most 200 requests and 120 s per host per run. A 100-URL single-host crawl therefore takes at least 100 seconds by design.
