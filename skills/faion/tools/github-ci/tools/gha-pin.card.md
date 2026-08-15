# gha-pin

## Purpose
Resolves every `uses: owner/repo@tag` to the 40-char commit SHA behind it and rewrites the line as `owner/repo@<sha> # tag`. A tag is
a mutable pointer: tj-actions/changed-files was compromised in March 2025 by retagging every version at a malicious commit, and
~23,000 repositories pulled it without touching their own workflow. `--check` keeps a repository pinned once it has been pinned.

## Invoke
```
python3 {script} --dir {.github/workflows} [--check] [--write] [--allow {owner/*}] [--max-age-days {180}] [--out {file}] [--self-test]
```

## Inputs
- `--dir {path}` — directory of workflow YAML, non-recursive, `.yml` and `.yaml`. Required.
- `--check` — report drift, write nothing, fail when anything is unpinned. Optional.
- `--write` — rewrite the files in place. Optional; contradicts `--check`. With neither flag the run is a dry run.
- `--allow {glob}` — `owner/repo` glob left unpinned, e.g. your own org. Optional, repeatable.
- `--max-age-days {n}` — also report a pin whose commit is older than n days; `0` disables it and its extra request. Default `180`.
- `--out {file}` — ledger destination: one line per action, then the findings. Optional.
- `--self-test` — run the built-in fixtures and exit; no network, no credential. Optional.
- `GITHUB_TOKEN` — read from the environment, never from an argument. Least privilege for public repositories is no scope at all: a
  classic token with nothing ticked, or a fine-grained token with read-only public-repository access. It buys 5,000 requests/hour.

## Outputs
- Files: workflow YAML under `{dir}`, rewritten only under `--write`; `{out}` — the ledger.
- stdout: `gha-pin: files=N actions=A unpinned=U rewritten=W stale=S requests=R`.
- stderr: one line per finding — a mutable ref and the SHA to pin it to, an aged pin, a bad ref.
- Exit: `0` clean · `1` unpinned under `--check`, or a ref that does not exist · `2` the tool could not run — bad `--dir`, both mode
  flags, unreadable or unwritable file, network failure · `3` `GITHUB_TOKEN` unset · `4` the token was rejected · `6` GitHub API
  failure, rate limit included.

## When NOT to use
- Judging whether a workflow is *safe*: that is `gha-audit`, which needs no token and reads 14 rules.
- Detecting that a tag was retagged. Once pinned the tag no longer matters, so it is not checked; staleness of the pin is.
- Docker (`docker://…`) and local (`./…`) actions, and any `uses:` inside a folded or quoted YAML construct — the scanner matches a
  plain `uses:` line and skips the rest.

## Cost
Zero model calls. One GET per distinct `owner/repo@ref`, cached in process, plus one per pinned action when `--max-age-days` is on.
Authenticated rate limit is 5,000 requests/hour.
