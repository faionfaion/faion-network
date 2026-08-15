# cache-purge

## Purpose
Purges a Cloudflare zone's edge cache by url, tag, host, or entirely — chunked to the vendor's 100 operations per request, paced to the plan's rate limit, backing off on a 429, and dry-run until confirmed. It reports how many operations went through, never the vendor's echo of them.

## Invoke
```
python3 {script} --zone {example.com} (--files {urls.txt} | --tags {t1,t2} | --hosts {h1,h2} | --everything) [--dry-run] [--yes] [--self-test]
```

## Inputs
- `--zone {name}` — the zone to purge. Required unless self-testing. The credential is read from the environment variable `CLOUDFLARE_API_TOKEN` and nowhere else; there is no flag for it, and its least privilege is Cache Purge resource-scoped to this one zone.
- `--files {file}` — file of absolute urls, one per line, blanks and `#` comments skipped. Cap 1000 per run. Exactly one of the four mode options is required.
- `--tags {list}` — comma-separated cache tags. Cap 500 per run.
- `--hosts {list}` — comma-separated hostnames. Cap 500 per run.
- `--everything` — purge every cached object for the zone. The origin absorbs the whole refill, so this mode needs the zone name as the confirmation value.
- `--dry-run` — print the plan, verify the credential with one read-only call, purge nothing. Optional.
- `--yes` — execute. Bare for url, tag and host purges; with `--everything` its value must be the zone name (`--yes example.com`). Without it, and without `--dry-run`, the run is refused.
- `--self-test` — run the built-in fixtures and exit. Makes no network call and needs no credential. Optional.

## Outputs
- Files: none.
- stdout: `cache-purge: zone=example.com mode=tags ops=N requests=M purged=K digest=abc123abc123` — the digest fingerprints the change set, so a preview and the run that follows it must match.
- stderr: the plan, capped at ten operations plus a count, in both modes; then the refusal, if any. No response body is printed.
- Exit: `0` purged, or previewed under `--dry-run` · `1` a failed self-test · `2` cannot run: no `--zone`, not exactly one mode, unreadable url list, a relative url, an empty change set, no such zone visible to this token · `3` CLOUDFLARE_API_TOKEN is unset · `4` credential rejected, 401 or 403 · `5` refused: unconfirmed, or a change set over the cap · `6` vendor API error, including a 429 that outlived three backoffs.

## When NOT to use
- Shipping a deploy. Content-hash the asset urls instead; a purge is the fix for what you cannot rename.
- Deleting anything. A purge evicts cached copies only — the origin is untouched, and no origin object is reachable from here.
- Bulk invalidation past the caps. Over them the run is refused, because tag, host and everything purges share five requests per minute on Free and a longer run is a decision, not a flag.

## Cost
Zero model calls. One request per 100 operations plus a zone lookup; `--dry-run` costs exactly one read-only call. Paced 12 s between tag, host and everything requests (the five-per-minute Free limit) and 1 s between url requests; a 429 retries after 15 s, then 30 s, then 60 s.
