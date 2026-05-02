# Wave 3 Dispatch Rules (Pro)

## Repo

- Path: `/home/nero/workspace/projects/faion-net/faion-network`
- Branch: `_temp_main` → `origin/main`
- Push: `flock /tmp/faion-network-merge.lock bash -c 'git pull --rebase --autostash origin main && git push origin _temp_main:main'`

## Tier scope (pro)

Allowed citations from `knowledge/free/ + solo/ + pro/`. NEVER cite `geek/` — validator rejects.

Pro paths:

```
faion/knowledge/pro/dev/backend-systems
faion/knowledge/pro/dev/backend-enterprise
faion/knowledge/pro/infra/devops-engineer
faion/knowledge/pro/infra/cicd-engineer
faion/knowledge/pro/infra/infrastructure-engineer
faion/knowledge/pro/pm/project-manager
faion/knowledge/pro/pm/pm-agile
faion/knowledge/pro/pm/pm-traditional
faion/knowledge/pro/product/product-manager
faion/knowledge/pro/ba/business-analyst
faion/knowledge/pro/ba/ba-core
faion/knowledge/pro/ba/ba-modeling
faion/knowledge/pro/ux/ux-ui-designer
faion/knowledge/pro/ux/ux-researcher
faion/knowledge/pro/ux/user-researcher
faion/knowledge/pro/ux/accessibility-specialist
faion/knowledge/pro/marketing/growth-marketer
faion/knowledge/pro/marketing/gtm-strategist
faion/knowledge/pro/marketing/ppc-manager
faion/knowledge/pro/marketing/smm-manager
faion/knowledge/pro/marketing/conversion-optimizer
faion/knowledge/pro/research/market-researcher
faion/knowledge/pro/research/researcher
faion/knowledge/pro/comms/hr-recruiter
```

To find an exact methodology folder before citing:

```
ls skills/faion/knowledge/<tier>/<group>/<skill>/
```

## Output location

```
skills/faion/playbooks/pro/<group>/<slug>/playbook.md
```

## Required structure

Read `.aidocs/conventions/playbooks/playbook-spec.md` § 4–6 BEFORE writing.

Front-matter (8 keys), `tier: pro`. H2 sections in fixed order: `Goal`, `Prerequisites`, `Steps`, `Verify`, `Troubleshooting`, `Next`, `References`.

## Citation format

```markdown
- [knowledge/<tier>/<group>/<skill>/<methodology>](../../../knowledge/<tier>/<group>/<skill>/<methodology>) — <playbook-specific rationale, ≥10 chars>
```

Tier ≤ pro (free/solo/pro). Path must resolve. Rationale playbook-specific.

## Validator

```
python3 scripts/validate-tier-playbook.py skills/faion/playbooks/pro/<group>/<slug>/playbook.md
```

Must exit 0.

## CHANGELOG

Edit `CHANGELOG.md`: under FIRST `## [Unreleased]`, add as FIRST bullet:

```
- add: tier-playbook pro/<group>/<slug>
```

## Commit + push

```
git add skills/faion/playbooks/pro/<group>/<slug>/ CHANGELOG.md
git commit -m "add: tier-playbook pro/<group>/<slug>"
flock /tmp/faion-network-merge.lock bash -c 'git pull --rebase --autostash origin main && git push origin _temp_main:main'
```

NO `--no-verify`. NO `Co-Authored-By`. NO emojis.

## Last-line marker (required)

```
done=<slug> commit=<short-sha>
```

## Quality bar

Pro-tier audience: agency owners, senior contractors, growing team leads, growth marketers — concrete real-world examples, real tooling and commands. Body ≤5k tokens. No `foo`/`bar`/`example.com` placeholders. Real Markdown link citations only.
