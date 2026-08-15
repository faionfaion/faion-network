# zone-audit

## Purpose
Audits one Cloudflare zone's security settings against a policy and prints only the settings that violate it — a clean zone costs one line, where a raw settings sweep costs ~40 vendor JSON objects the caller then has to compare by hand. Use it as the gate on a zone's TLS and HTTPS posture.

## Invoke
```
python3 {script} --zone {example.com} [--policy {policy.json}] [--out {audit.md}] [--json] [--strict] [--self-test]
```

## Inputs
- `--zone {name}` — the zone to audit. Required unless self-testing. The credential is read from the environment variable `CLOUDFLARE_API_TOKEN` and nowhere else; there is no flag for it, and its least privilege is Zone Read resource-scoped to this one zone.
- `--policy {file}` — JSON object of setting id to rule, merged over the built-in policy (ssl, min_tls_version, always_use_https, security_level, http3, opportunistic_encryption). A rule is a scalar for equality, a list or `{"one_of": [...]}` for membership, `{"at_least": "1.2"}` for the ordered scales (ssl, min_tls_version, security_level), or `null` to drop that check. Optional.
- `--out {file}` — markdown table of every setting checked, its value and its verdict. Optional, nothing written by default.
- `--json` — emit the summary line as one line of JSON, findings included. Optional.
- `--strict` — count a setting this zone or plan does not expose as a violation. Optional; by default such a setting is a skipped check.
- `--self-test` — run the built-in fixtures and exit. Makes no network call and needs no credential. Optional.

## Outputs
- Files: `{out}` — one row per checked setting: id, value, rule, verdict.
- stdout: `zone-audit: zone=example.com checks=N violations=M`, or one line of JSON under `--json`.
- stderr: one line per violation, naming the setting, its value and the rule. A response body is never printed.
- Exit: `0` policy met · `1` at least one violation, or a failed self-test · `2` cannot run: no `--zone`, unreadable policy, no such zone visible to this token, unwritable `--out` · `3` CLOUDFLARE_API_TOKEN is unset · `4` credential rejected, 401 or 403 · `6` vendor API error, including a 429.

## When NOT to use
- Fixing a violation. Every request is a GET; the safe value for `security_level` on a zone under attack is a judgement, and a gate that makes it gets talked past.
- Auditing a whole account. One zone per run by design — the token should not be able to see a second zone.
- Taking an inventory. It prints violations, not values; pass `--out` when you want the full table.

## Cost
Zero model calls. One zone lookup plus one GET per policy key — seven requests for the built-in policy, because the batch settings endpoint is deprecated (EOL 2027-03-31) and the sweep fans out over the per-setting endpoint instead. Read-only, so no purge-style rate limit applies.
