# Wave 2 Dispatch Rules (Solo)

## Repo

- Path: `/home/nero/workspace/projects/faion-net/faion-network`
- Local branch: `_temp_main`
- Remote: `origin/main`
- Push: `flock /tmp/faion-network-merge.lock bash -c 'git pull --rebase --autostash origin main && git push origin _temp_main:main'`

## Tier scope (solo)

Allowed methodology citations from these paths (free + solo only):

```
faion/knowledge/free/dev/software-developer
faion/knowledge/free/dev/python-developer
faion/knowledge/free/dev/javascript-developer
faion/knowledge/free/dev/testing-developer
faion/knowledge/free/dev/code-quality
faion/knowledge/free/dev/backend-developer
faion/knowledge/free/dev/devtools-developer
faion/knowledge/free/marketing/marketing-manager
faion/knowledge/solo/dev/frontend-developer
faion/knowledge/solo/dev/api-developer
faion/knowledge/solo/dev/software-architect
faion/knowledge/solo/dev/automation-tooling
faion/knowledge/solo/infra/server-craft
faion/knowledge/solo/sdd/sdd
faion/knowledge/solo/sdd/sdd-planning
faion/knowledge/solo/product/product-planning
faion/knowledge/solo/product/product-operations
faion/knowledge/solo/ux/ui-designer
faion/knowledge/solo/marketing/content-marketer
faion/knowledge/solo/marketing/seo-manager
faion/knowledge/solo/comms/communicator
```

To find an exact methodology folder before citing:

```
ls skills/faion/knowledge/<tier>/<group>/<skill>/
```

The methodology is the subfolder name. NEVER cite a `pro/` or `geek/` methodology — validator will reject.

## Output location

```
skills/faion/playbooks/solo/<group>/<slug>/playbook.md
```

## Required structure

Read `.aidocs/conventions/playbooks/playbook-spec.md` § 4–6 BEFORE writing.

Front-matter (8 keys, all required), `tier: solo`. H2 sections in fixed order: `Goal`, `Prerequisites`, `Steps`, `Verify`, `Troubleshooting`, `Next`, `References`.

## Citation format

```markdown
- [knowledge/<tier>/<group>/<skill>/<methodology>](../../../knowledge/<tier>/<group>/<skill>/<methodology>) — <playbook-specific rationale, ≥10 chars>
```

Tier ≤ solo (so free or solo). Path must resolve. Rationale must be playbook-specific.

## Validator

```
python3 scripts/validate-tier-playbook.py skills/faion/playbooks/solo/<group>/<slug>/playbook.md
```

Must exit 0.

## CHANGELOG

Edit `CHANGELOG.md`: under FIRST `## [Unreleased]`, add as FIRST bullet:

```
- add: tier-playbook solo/<group>/<slug>
```

## Commit + push

```
git add skills/faion/playbooks/solo/<group>/<slug>/ CHANGELOG.md
git commit -m "add: tier-playbook solo/<group>/<slug>"
flock /tmp/faion-network-merge.lock bash -c 'git pull --rebase --autostash origin main && git push origin _temp_main:main'
```

NO `--no-verify`. NO `Co-Authored-By`. NO emojis.

## Last-line marker (required)

The very last line of your final response must be exactly:

```
done=<slug> commit=<short-sha>
```

## Quality bar

- Action-leading verbs in step headers.
- Real URLs, real commands. No `foo`/`bar`/`example.com` placeholders.
- `## Verify` runnable as one observable check.
- `## Troubleshooting` ≥1 named pitfall (Symptom → Cause → Fix).
- Body ≤5k tokens.
- Citation rationale playbook-specific (not "this methodology covers X").
