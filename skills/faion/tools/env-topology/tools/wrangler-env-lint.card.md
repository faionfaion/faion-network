# wrangler-env-lint

## Purpose
Names every binding and var a named Wrangler environment silently loses. Cloudflare documents bindings and environment variables as
non-inheritable: `vars`, `kv_namespaces`, `d1_databases`, `r2_buckets`, `durable_objects`, `queues`, `services` and secrets never reach
`[env.production]` from the top level, while `routes` and `workers_dev` do. It never fails a deploy; it fails a request in production.

## Invoke
```
python3 {script} --config {wrangler.jsonc} [--envs {staging,production}] [--out {matrix.md}] [--json] [--self-test]
```

## Inputs
- `--config {file}` — `wrangler.jsonc`, `wrangler.json` or `wrangler.toml`. Required unless self-testing. JSONC is parsed by a
  string-aware stripper written into the tool (comments and trailing commas; a `//` inside a string literal survives); `.toml`
  goes through `tomllib`, which needs python 3.11 or newer.
- `--envs {a,b}` — comma-separated environment names to check. Optional, default every environment under `env`. A name the config
  does not define is itself a finding.
- `--out {file}` — markdown matrix of every binding identity against every environment, `declared` or `ABSENT` per cell. Optional,
  nothing written by default. The matrix is deliberately kept off stdout.
- `--json` — emit the summary line as one line of JSON, findings included. Optional.
- `--self-test` — run the built-in fixtures and exit. Reads no file. Optional.

## Outputs
- Files: `{out}` — the binding-by-environment matrix plus the finding list.
- stdout: `wrangler-env-lint: config=path environments=N findings=M`, or one line of JSON under `--json`.
- stderr: one line per finding — a non-inheritable key or named binding absent from an environment, an unset `compatibility_date`,
  or a durable object class that is bound and never created by a migration.
- Exit: `0` every checked environment redeclares everything · `1` at least one finding, or a failed self-test · `2` cannot run: no
  `--config`, unreadable file, unparseable JSONC or TOML, or an unwritable `--out`.

## When NOT to use
- Deploying or reading account state. It opens no socket, needs no `CLOUDFLARE_API_TOKEN`, and cannot tell you what is bound on the
  live worker — only what this file says. For live zone posture use the `cloudflare` pack.
- Configs whose environments are assembled by a script or a `--var` at deploy time; it lints the file as written, nothing else.
- Deciding whether a binding *should* exist. A staging worker with no R2 bucket is a design, not a bug — the tool reports the delta
  and the caller judges it. It also cannot see secrets, which live in the dashboard and are non-inheritable too.

## Cost
Zero model calls. Zero network calls. One parse and one pass per environment; milliseconds for any real config.
