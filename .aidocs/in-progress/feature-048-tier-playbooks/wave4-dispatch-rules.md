# Wave 4 Dispatch Rules (Geek)

## Repo

- Path: `/home/nero/workspace/projects/faion-net/faion-network`
- Branch: `_temp_main` → `origin/main`
- Push: `flock /tmp/faion-network-merge.lock bash -c 'git pull --rebase --autostash origin main && git push origin _temp_main:main'`

## Tier scope (geek)

ALL tiers allowed for citation: free + solo + pro + geek. Geek paths:

```
faion/knowledge/geek/ai/ml-engineer
faion/knowledge/geek/ai/ai-agents
faion/knowledge/geek/ai/rag-engineer
faion/knowledge/geek/ai/ml-ops
faion/knowledge/geek/ai/multimodal-ai
faion/knowledge/geek/ai/llm-integration
faion/knowledge/geek/ai/claude-code
```

To find an exact methodology folder before citing:

```
ls skills/faion/knowledge/geek/ai/<skill>/
```

## Output location

```
skills/faion/playbooks/geek/<group>/<slug>/playbook.md
```

## Required structure

Read `.aidocs/conventions/playbooks/playbook-spec.md` § 4–6 BEFORE writing.

Front-matter (8 keys), `tier: geek`. H2 sections in fixed order: `Goal`, `Prerequisites`, `Steps`, `Verify`, `Troubleshooting`, `Next`, `References`.

## Citation format

```markdown
- [knowledge/<tier>/<group>/<skill>/<methodology>](../../../knowledge/<tier>/<group>/<skill>/<methodology>) — <playbook-specific rationale, ≥10 chars>
```

Path must resolve. Rationale playbook-specific.

## Validator

```
python3 scripts/validate-tier-playbook.py skills/faion/playbooks/geek/<group>/<slug>/playbook.md
```

Must exit 0.

## CHANGELOG

Edit `CHANGELOG.md`: under FIRST `## [Unreleased]`, add as FIRST bullet:

```
- add: tier-playbook geek/<group>/<slug>
```

## Commit + push

```
git add skills/faion/playbooks/geek/<group>/<slug>/ CHANGELOG.md
git commit -m "add: tier-playbook geek/<group>/<slug>"
flock /tmp/faion-network-merge.lock bash -c 'git pull --rebase --autostash origin main && git push origin _temp_main:main'
```

NO `--no-verify`. NO `Co-Authored-By`. NO emojis.

## Last-line marker (required)

```
done=<slug> commit=<short-sha>
```

## Quality bar

Geek-tier audience: AI agent engineers, RAG builders, AI consultants, indie AI product founders. Real working code in Python/TypeScript using actual SDKs (Anthropic Python SDK 2026, Pydantic v2, LangChain ≥0.3, Qdrant, pgvector). Real model IDs: `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`. Body ≤5k tokens. No `foo`/`bar`/`example.com` placeholders.
