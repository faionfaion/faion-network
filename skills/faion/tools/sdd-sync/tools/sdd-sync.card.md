# sdd-sync

## Purpose
Reconciles one feature's SDD task files — the `todo/`, `in-progress/`, `done/` directory-as-status lifecycle — against an issue-tracker snapshot through a hash ledger, so a second run updates instead of creating the task set again. Tells local-ahead from remote-ahead from a conflict, and refuses to pick a winner.

## Invoke
```
python3 {script} --aidocs {feature-049} --map {sync-map.json} [--remote {rows.jsonl}] [--profile {github}] [--plan {plan.jsonl}] [--push] [--pull] [--report] [--dry-run] [--yes] [--self-test]
```

## Inputs
- `--aidocs {dir}` — one feature directory holding `todo/`, `in-progress/` and `done/`. Required unless self-testing. Only `TASK-*.md` files are read; the directory is the status, never a front-matter field.
- `--map {file}` — the hash ledger: task key to remote id to last hash on both sides. Required. Created on the first apply; it is what makes a second run idempotent, so it belongs in git beside the feature.
- `--remote {file}` — the tracker as JSONL, produced by api-call's select expression. Required for a push or a pull, optional for a report. Rows are matched to tasks by the `TASK-nnn-nnn` key in their title, so a row without one is ignored rather than adopted.
- `--profile {name}` — which tracker's field names the rows use: `github`, `linear` or `clickup`. Optional, default `github`. The ledger records it and refuses a snapshot from a different one.
- `--plan {file}` — where the change set is written as JSONL for api-call to execute as request payloads. Optional; written only on an apply.
- `--push` — plan the local side onto the tracker. `--pull` — move task files to match the tracker's state. `--report` — reconcile and change nothing. Optional, default report; push and pull together is an error.
- `--dry-run` — print the change set and write nothing, exiting clean. Optional.
- `--yes` — apply: write the ledger, the plan, and any file moves. Without it a push or pull prints the change set and refuses. Optional.
- `--self-test` — run the built-in fixtures and exit, including the two-run idempotence proof. No network, no credential, no temporary files. Optional.

## Outputs
- Files: `{map}` — the ledger, sorted and stable. `{plan}` — one JSON object per change, ready for `api-call`. On a pull, task files move between the status directories and nothing else in the tree is touched.
- stdout: `sdd-sync: mode=push tasks=N remote=M changes=C applied=A findings=F`.
- stderr: one line per planned change, then one per finding, naming the task key.
- Exit: `0` in sync, or applied · `1` at least one finding — a conflict, a task the tracker lost, a remote-ahead task a push would overwrite, a plan never executed, two files claiming one key · `2` cannot run: no status directories, an unreadable ledger or snapshot, a snapshot from the wrong tracker · `5` changes were refused for want of `--yes`.

## When NOT to use
- Talking to a tracker. It makes no network call at all: api-call.py fetches the snapshot and executes the plan, which is what keeps the reconcile provable offline.
- Merging text. A two-sided change is reported as a conflict and left alone; picking a winner between two humans is not a gate's job.
- Syncing prose. Only the title and the open/done state cross the boundary, so a body-only edit records the hash and sends nothing.

## Cost
Zero model calls, zero requests. One pass over the task files and the snapshot; milliseconds for a feature's worth of tasks.
