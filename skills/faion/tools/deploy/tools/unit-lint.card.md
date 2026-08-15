# unit-lint

## Purpose
Lints a systemd unit against the filesystem it will run on: an ExecStart never rsynced, a
WorkingDirectory `ProtectHome` hides, a 0644 EnvironmentFile, a `ReadWritePaths` missing where the
app writes, no `Restart`, a contradictory `Type=`. Each finding is a failed start that never happens.

## Invoke
```
python3 {script} --unit {file.service} [--root {path}] [--installed {dir}] [--strict] [--json] [--out {file}] [--self-test]
```

## Inputs
- `--unit {file}` — the unit file to lint. Required unless self-testing. Never modified.
- `--root {path}` — root the unit's absolute paths resolve against: `/` for this machine, a staging
  tree for what the deploy is about to ship. Optional; without it every existence, executable-bit
  and permission check is skipped and only the text is judged.
- `--installed {dir}` — units already installed, usually `/etc/systemd/system`. Optional; reports a
  name that exists there with different content.
- `--strict` — also report advisories: explicit `User=root`, absent `Group=`, a group-readable
  EnvironmentFile, a cwd written to under a read-only sandbox, an unverifiable `Type=notify`.
- `--json` — print one JSON object `{"ok":bool,"unit":name,"findings":[...]}` instead of the summary.
- `--out {file}` — the full parse, every path stat-ed and every finding, as JSON. Never on stdout.
- `--self-test` — run the built-in fixtures and exit. Optional, touches no filesystem.

## Outputs
- Files: `{out}` — the whole parsed unit plus findings, as JSON. Nothing else is ever written.
- stdout: `unit-lint: unit=NAME findings=F probed=yes|no -> path`
- stderr: one line per finding, each naming the directive and the failure it causes.
- Exit: `0` no findings · `1` at least one finding · `2` could not run — no unit given, unreadable
  file, a root or installed directory that is not one, or a file holding no sections.

## When NOT to use
- Checking unit grammar or drop-in resolution: that is `systemd-analyze verify`, the complement.
- Fixing a unit. It writes nothing back — the repo is the source, and a unit corrected in place
  leaves the repo wrong and the runtime edited.
- Proving a service works: nothing is executed, so `Type=notify` is a reported risk, not a verdict.

## Cost
Zero model calls. Zero network calls. One read of the unit plus one stat per path it names.
