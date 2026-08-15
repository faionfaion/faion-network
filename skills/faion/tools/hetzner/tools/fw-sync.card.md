# fw-sync

## Purpose
Converges a Hetzner cloud firewall from the same infra spec, behind a lockout proof and a revert timer. `set_rules` is a destructive replace and an empty array wipes every rule, so this proves inbound SSH survives for every admin CIDR and for you before it writes, and arms a rollback that only a second invocation cancels.

## Invoke
```
python3 {script} --spec {infra.json} --firewall {name} [--admin-cidr {cidr}] [--apply] [--commit] [--revert-after {min}] [--state {file}] [--out {plan.md}] [--json] [--self-test]
```

## Inputs
- `--spec {file}` — JSON: `admin_cidrs` (required, CIDR list), `ssh_port` (default 22), `public_ports`, `extra_rules` (raw Hetzner rule objects), optional `firewalls` map of per-firewall overrides. Required except for a bare commit. The credential is read from the environment variable `HCLOUD_TOKEN` and nowhere else; there is no flag for it, and it needs Read & Write on one project.
- `--firewall {name}` — the cloud firewall to converge. Required. It must already exist; creating one is a deliberate act you do with `hcloud`.
- `--admin-cidr {cidr}` — where this run is coming from, when you are not on the box. Required for `--apply` unless `SSH_CONNECTION` is set. It feeds the proof only and is never added to the rule set: if your source is outside `admin_cidrs`, put it in the spec. Repeatable; the first is used.
- `--apply` — write the rules and arm the revert. Optional; without it the run is a dry run that writes nothing.
- `--commit` — second invocation, from another shell: cancel the armed revert and keep the change. Optional. Refused alongside `--apply`, because that is the two-phase guard removed.
- `--revert-after {min}` — minutes before the prior rule set goes back. Optional, default 10, minimum 1.
- `--state {file}` — where the armed revert and the prior rule set are recorded, written 0600. Optional, default `fw-sync-state.json` in the working directory. The commit invocation must be given the same path.
- `--out {file}` — the full plan: post-apply rule set, added, removed, unchanged, and the prior rules restored on revert. Optional.
- `--json` — emit the summary line as one line of JSON. Optional.
- `--self-test` — run the built-in fixtures and exit, including a rule set that would lock admin SSH out. No network, no credential. Optional.

## Outputs
- Files: `{out}` — the full plan; `{state}` — the armed revert, replaced atomically.
- stdout: `fw-sync: firewall=X mode=dry-run add=A remove=R keep=K digest=D committed=B reverted=B`, or one line of JSON.
- stderr: the capped diff, one rule per line, plus notes and any refusal. A response body is never printed.
- Exit: `0` converged and committed, or nothing to do · `1` drift found in a dry run, or the change was reverted because nobody committed it · `2` cannot run: bad arguments, unreadable spec, no such firewall, nothing to commit · `3` HCLOUD_TOKEN is absent · `4` credential rejected · `5` refused by a safety guard — the post-apply rules would lose admin SSH, the caller's own source is unknown, the spec produces an empty or oversized rule set, `--apply` and `--commit` arrived together, or a commit arrived after the window closed · `6` vendor API error, including a rate limit past RateLimit-Reset.

## When NOT to use
- Attaching, detaching or creating a firewall, or touching a server, volume, snapshot or image. It converges rules only and prints the `hcloud` command for the rest.
- Unattended automation. The revert is cancelled by a human running the tool a second time; an apply nobody commits ends with the firewall it started with, by design.
- Hetzner Robot dedicated servers. Different API, different auth, out of scope.

## Cost
Zero model calls. One GET to read the firewall, one POST per rule change plus action polls, and one more POST if the revert fires — roughly two requests for a dry run and six for an apply that reverts, against a 3600-request hourly account limit. An apply holds the terminal for the whole revert window.
