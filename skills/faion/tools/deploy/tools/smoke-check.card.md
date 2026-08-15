# smoke-check

## Purpose
Asserts what a deployed site actually serves, not that something answered — a curl gate passes
against a stale, half-copied or empty build, since all of those return 200. Each check adds the two
assertions that catch them: `not_contains` for the string that must have gone, and `min_bytes`.

## Invoke
```
python3 {script} --spec {smoke.json} [--base {url}] [--timeout {10}] [--retries {3}] [--out {file}] [--json] [--self-test]
```

## Inputs
- `--spec {file}` — JSON, a list of checks or `{"base":url,"checks":[...]}`. A check takes `path`
  (joined to the base) or absolute `url`; `name`; `method` `GET` or `HEAD`; `status` int or list,
  default 200; `contains`; `not_contains`; `content_type` as a substring; `min_bytes`; `max_ms`.
- `--base {url}` — origin the paths hang off, overriding the spec's. Optional; aims one spec at
  staging and then at production. Required, in one place or the other, for any check using `path`.
- `--timeout {seconds}` — per-request timeout. Optional, default 10.
- `--retries {n}` — attempts before a check is failed, a second apart. Optional, default 3.
- `--out {file}` — every check's full result as JSON. Optional; the inventory never hits stdout.
- `--json` — print one JSON object `{"ok":bool,"failed":[...]}` instead of the summary line.
- `--self-test` — run the built-in fixtures and exit. Optional, opens no socket.
- Auth: a check may name an `auth_header`; its value is read from `SMOKE_AUTH_VALUE` in the
  environment, never from the spec, an argument, or the output.

## Outputs
- Files: `{out}` — `{"ok":bool,"failed":[names],"checks":[...]}` with status, bytes, latency, findings.
- stdout: `smoke-check: checks=N failed=F slowest=Mms -> path`
- stderr: one line per failing assertion, naming the check and what it got.
- Exit: `0` all passed · `1` an assertion failed, a refused connection included · `2` could not run
  — no spec, a malformed one, a host that will not resolve, or an auth header with no env value.

## When NOT to use
- Testing behaviour: GET and HEAD only, so a login or a form post belongs in an end-to-end suite.
- Asserting on a redirect. Redirects are followed, so the status is the final response's.
- Reading past 4 MiB of a body, or a client-rendered page: what JavaScript builds is not there.

## Cost
Zero model calls. One request per check, up to `--retries` attempts, one second between attempts.
