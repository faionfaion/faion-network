# BRIEF — feature-046 methodology decomposition

You are a decomposition agent. You receive a batch of OVERSIZED methodology folders (each one ≥25KB total markdown + XML body). The source content is actually multiple distinct concepts glued into a single methodology — a violation of the canonical spec ("one concept per file"). Your job: split each into 2-7 new methodology folders, each holding **one concept**, each ≤15KB, each as a complete `methodology.xml` per the schema.

This is NOT a format-only migration. It is an **editorial split** — you must understand the source, identify natural concept boundaries, and produce independent methodologies.

## Mandatory pre-flight (Read before any write)

1. `docs/skill-authoring.md` — canonical structure (size budgets, "one concept per file", anti-patterns).
2. `docs/methodology-xml-schema.md` — XML schema for `methodology.xml` (root, metadata, content).
3. `docs/methodology-tag-glossary.xml` — closed tag vocabulary; unknown tags fail validation.
4. `docs/examples/methodology-reference.xml` — fully migrated reference example.
5. `scripts/validate-methodology-xml.py` — validator (run after every write).

Skipping these guarantees rejected commits. The validator is a pre-commit gate.

## Working directory

`/home/nero/workspace/projects/faion-net/faion-network`

## Batch input

Each batch line is one absolute oversized methodology folder path:

```
/home/nero/workspace/projects/faion-net/faion-network/skills/faion/knowledge/<tier>/<group>/<domain>/<old-slug>/
```

Default batch size: 1. Hard cap: 2. Decomposition is expensive — small batches.

## Per-folder procedure

### Step 1 — read every existing body file

OLD shapes possible:
- 5-file pattern: `README.md`, `agent-integration.md`, `checklist.md`, `examples.md`, `llm-prompts.md`, `templates.md`
- AGENTS.md + `content/*.xml` shape

Also read `templates/*` and `scripts/*` filenames (NOT bodies — keep them as-is) so you can route them to the correct new slug.

### Step 2 — identify natural concept boundaries

Read the full source. List the distinct concepts present. Examples:

| Old slug | Concepts inside | New slugs |
|----------|-----------------|-----------|
| `reranking` (156K) | cross-encoder, two-stage retrieve+rerank, listwise, learning-to-rank, diversity-aware | `reranking-cross-encoder`, `reranking-two-stage`, `reranking-listwise`, `reranking-ltr`, `reranking-diversity` |
| `creational-patterns` (115K) | singleton, factory, builder, prototype, abstract-factory | `pattern-singleton`, `pattern-factory`, `pattern-builder`, `pattern-prototype`, `pattern-abstract-factory` |
| `django-pytest` (137K) | fixtures, factories, integration tests, parametrize, mocking, conftest | `django-pytest-fixtures`, `django-pytest-factories`, `django-pytest-integration`, `django-pytest-parametrize`, `django-pytest-mocking` |
| `security-architecture` (130K) | threat-modeling, defense-in-depth, zero-trust, secure-defaults, least-privilege | `security-threat-modeling`, `security-defense-in-depth`, `security-zero-trust`, `security-secure-defaults`, `security-least-privilege` |

**Rules for new slugs:**
- kebab-case
- 3-7 words max
- Same parent path: `<tier>/<group>/<domain>/<new-slug>/`
- Each new slug captures ONE concept testable as a single rule
- Naming consistency: prefix with the original domain when natural (e.g. `reranking-*`, `django-pytest-*`)
- Avoid duplication with existing peer methodologies in the same domain — `Glob skills/faion/knowledge/<tier>/<group>/<domain>/*/` to verify

Min 2 new slugs, max 7. If you cannot identify ≥2 distinct concepts the source is not actually oversized — abort and report `failed=1 reason=not-oversized`.

### Step 3 — produce one `methodology.xml` per new slug

For each new slug:

1. Create `<tier>/<group>/<domain>/<new-slug>/`
2. Write `methodology.xml` per the schema in `docs/methodology-xml-schema.md`:
   - `<metadata>` — tier, group, domain, summary (≤200 chars), tags (3-5), category if applicable, difficulty, created (today's ISO date), tools/languages/frameworks if relevant
   - `<content>` — title, summary, why, when-to-use, when-not-to-use, body sections (rules + examples + antipatterns)
3. Total `methodology.xml` size: target ≤15K, hard cap 30K
4. Verbatim preservation: prose extracted from the source for THIS concept must be ≥80% of the source-fragment length (validator's LENGTH_PARITY runs on the new methodology against the slice of source markdown that this concept covers)
5. Distribute `templates/` and `scripts/` files: each goes to ONE new slug based on relevance. Move with `git mv` to preserve history. If a template is shared, prefer the most relevant slug. Empty folders are forbidden — drop the directory.

### Step 4 — delete the old folder

After all new slugs validated:
- `git rm -r <tier>/<group>/<domain>/<old-slug>/` (entirely, including all body files, content/, templates/, scripts/, AGENTS.md, etc.)

### Step 5 — validate every new slug

```bash
python3 scripts/validate-methodology-xml.py <new-slug-folder>
```

Common failures:

| Code | Fix |
|------|-----|
| `XML_PARSE` | Unescaped `<`/`>`/`&` in prose — wrap code in CDATA, escape inline. |
| `UNKNOWN_TAG` | Tag not in glossary. Pick existing tag; do NOT extend glossary. |
| `META_*` | Mandatory metadata missing. |
| `LENGTH_PARITY` | Re-add cut prose verbatim from the source slice. |
| `EMPTY_CONTAINER` | `<rule>`, `<example>` etc. has no body. |

### Step 6 — commit per new slug

ONE commit per NEW methodology, NOT one per batch. Format:

```
chore: decompose <old-slug> → <new-slug>

Source: <old-slug>/{README.md,...} (concept: <one-line>)
```

Plus ONE final commit per batch removing the old folder:

```
chore: drop <old-slug> after decomposition

New slugs: <slug-1>, <slug-2>, ...
```

Update `CHANGELOG.md` once per BATCH:

```
- decompose: <old-slug> → N slugs (<list>)
```

## Hard rules

1. NEVER use `--no-verify`. If pre-commit fails, fix it.
2. NEVER summarize source content — verbatim within each new slug's slice.
3. NEVER touch `templates/` or `scripts/` file BODIES — only relocate via `git mv`.
4. NEVER leave the old folder after decomposition. `git rm -r` it.
5. NEVER invent tags outside `methodology-tag-glossary.xml`.
6. NEVER produce <2 new slugs from a single oversized source. If you can't, the source is wrongly classified — abort and report.
7. NEVER write absolute paths inside any `methodology.xml`. All file references relative to the methodology folder.
8. NEVER overlap content across new slugs — each prose block lives in exactly one new methodology.

## Worktree merge protocol

Subagents run in isolated worktrees. To merge:

```bash
flock /tmp/faion-network-merge.lock bash -c '
  cd /home/nero/workspace/projects/faion-net/faion-network
  git fetch origin main
  git merge --ff-only <worktree-branch> || (git rebase origin/main && git merge --ff-only <worktree-branch>)
  git push origin main
'
```

If `CHANGELOG.md` conflicts: keep both entries, re-stage.

## Reporting

After the batch, output exactly:

```
batch=<old-slug-list> done=<N-new-slugs> failed=<M> commits=<sha-list>
```

If you abort one source as not-oversized:

```
batch=<old-slug> done=0 failed=1 reason=not-oversized
```

Nothing else. Parent thread parses this.
