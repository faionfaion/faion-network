# Wave 1 Dispatch Rules

Authored once by orchestrator; read by every Wave 1 subagent before authoring its assigned playbook.

## Repo

- Path: `/home/nero/workspace/projects/faion-net/faion-network`
- Local branch: `_temp_main`
- Remote: `origin/main`
- Push command: `flock /tmp/faion-network-merge.lock bash -c 'git pull --rebase origin main && git push origin _temp_main:main'`

## Tier scope (free)

Allowed methodology citations from these paths only:

```
faion/knowledge/free/dev/software-developer
faion/knowledge/free/dev/python-developer
faion/knowledge/free/dev/javascript-developer
faion/knowledge/free/dev/testing-developer
faion/knowledge/free/dev/code-quality
faion/knowledge/free/dev/backend-developer
faion/knowledge/free/dev/devtools-developer
faion/knowledge/free/marketing/marketing-manager
```

To find the exact methodology folder before citing:

```
ls skills/faion/knowledge/free/<group>/<skill>/
```

The methodology is the subfolder name. Example: `knowledge/free/dev/devtools-developer/github-repo-bootstrap`.

## Output location

```
skills/faion/playbooks/free/<group>/<slug>/playbook.md
```

Optional companion files in the same folder: `checklist.md`, `templates.md`, `examples.md`.

## Required structure

Read `.aidocs/conventions/playbooks/playbook-spec.md` § 4–6 BEFORE writing.

Front-matter (8 keys, all required):

```yaml
---
name: <slug>
description: <≤200 chars, action-leading, one line>
tier: free
group: <group from catalog>
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---
```

H2 sections in fixed order: `Goal`, `Prerequisites`, `Steps`, `Verify`, `Troubleshooting`, `Next`, `References`.

## Citation format

In `## References`, use Markdown link:

```markdown
- [knowledge/free/<group>/<skill>/<methodology>](../../../knowledge/free/<group>/<skill>/<methodology>) — <playbook-specific rationale, ≥10 chars>
```

Path must resolve under `skills/faion/knowledge/`. Rationale must be playbook-specific (not "explains X" or "covers Y").

## Validator

```
python3 scripts/validate-tier-playbook.py skills/faion/playbooks/free/<group>/<slug>/playbook.md
```

Must exit 0. Fix all errors before committing.

## CHANGELOG

Edit `CHANGELOG.md`: under the FIRST `## [Unreleased]` line, add a single entry as the FIRST bullet:

```
- add: tier-playbook free/<group>/<slug>
```

## Commit + push (single, granular)

```
git add skills/faion/playbooks/free/<group>/<slug>/ CHANGELOG.md
git commit -m "add: tier-playbook free/<group>/<slug>"
flock /tmp/faion-network-merge.lock bash -c 'git pull --rebase origin main && git push origin _temp_main:main'
```

NO `--no-verify`. NO `Co-Authored-By`. NO emojis.

If `git pull --rebase` finds conflicts in CHANGELOG.md, resolve by keeping BOTH bullets (yours and theirs).

## Last-line marker (required)

The very last line of your final response must be exactly:

```
done=<slug> commit=<short-sha>
```

Anything after this line is ignored.

## Quality bar

- Steps action-leading (`Sign in at https://github.com/`, not `GitHub`).
- Real URLs, real commands. Don't use `foo`/`bar`/`example.com`.
- `## Verify` runnable as one observable check.
- `## Troubleshooting` ≥1 named pitfall (Symptom → Cause → Fix).
- Body ≤5k tokens. If longer, split off a `examples.md`.
- Citation rationale playbook-specific.
