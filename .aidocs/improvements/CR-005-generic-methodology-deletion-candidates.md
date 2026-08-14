---
type: change-request
cr_id: CR-005
title: "Deletion candidates: 40 template-stamped methodologies"
priority: P2
created: 2026-08-13
status: executed
executed: 2026-08-14
affected_components: [faion-network/skills/faion/knowledge, skills/tier-manifest.json]
related_tasks: [P2.2]
---

# Change Request: 40 deletion candidates from the generic-signature audit

> **EXECUTED 2026-08-14 — approved by the repo owner.** All 40 directories below have been
> removed. The proposal text is kept verbatim as the record of the evidence the decision rested
> on; read it in the past tense. What actually happened, and where the outcome differed from the
> estimate, is in [Execution record](#execution-record) at the end.

**This document proposes nothing be deleted today.** It is the evidence for a decision the repo
owner makes. No file listed here has been removed; every one is still on disk and still resolves.

## How the set was found

A bulk generation run stamped a fixed template over part of the corpus. The stamp is detectable by
exact signature, so the affected set is a measurement, not an estimate.

| Signature | Where | Count |
|-----------|-------|-------|
| The 5 generic rule ids `anchor-evidence-required` / `owner-and-last-touched` / `template-version-pinned` / `human-checkpoint-before-binding-action` / `skip-when-prerequisites-missing` | `content/01-core-rules.xml` | **100** |
| Generic antipattern ids `fabricated-fields` / `self-approval` / `generic-owner` / `version-drift` | `content/03-failure-modes.xml` | **100** |
| Generic step names `check-prerequisites` / `gather-evidence` / `fill-artefact` / `surface-for-review` | `content/04-procedure.xml` | **100** |
| Generic required keys `artefact_id` / `template_version` / `last_touched` | `content/02-output-contract.xml` | **120** |
| Generic question ids `q-prereqs-ok` / `q-trigger-fits` / `q-evidence-available` | `content/06-decision-tree.xml` | **120** |
| Generic `## Applies If` boilerplate (3 stock lines) | `AGENTS.md` | **100** |

The sets are perfectly nested: **120** methodologies carry the stamp, of which **100** carry it in
every file including the routing `AGENTS.md` — those 100 contain no domain content anywhere. The
remaining 20 (contiguous runs in `dev/` and `frontend/`) have real rules and failure modes under a
generic output contract and decision tree, and are **not** proposed for deletion.

## Why these 40 and not the other 60

Of the 100, **40 are redundant** — the subject already exists elsewhere in the corpus, in a copy
that has real rules. The other 60 name a real subject with no better copy anywhere, and have been
rewritten under this task rather than deleted.

The dominant pattern: **35 of the 40 have a same-slug twin in another domain**, and the twin is the
real one. `backend/api-authentication` is the generic template; `dev/api-authentication` cites OWASP
API Security Top 10, caps access-token lifetime, and requires a named revocation path. This is not
a judgement call — it is visible in the rule ids.

## The reference question

Deleting a referenced methodology is what creates dangling links. For this set the risk is close to
zero, for a structural reason worth stating explicitly:

**Wikilinks and `<ref slug=…>` resolve by SLUG, not by path.** `skills/tier-manifest.json` carries
both twins under the same `slug` and even the same `content_id`. So deleting `backend/api-rest-design`
while `dev/api-rest-design` survives leaves all 24 inbound `[[api-rest-design]]` links resolving
exactly as before.

Total inbound references across all 40: **242 wikilinks + 66 slug refs**. Of those, **3 would
actually dangle**:

| Would-dangle link | In file | Fix |
|---|---|---|
| `[[voice-ui-patterns]]` ×2 | `frontend/core-vui-design-principles/AGENTS.md`, `frontend/error-handling-in-vui/AGENTS.md` | both files are themselves on this list — deleting the set resolves it to 0 |
| `[[motion-and-microinteraction-spec]]` ×1 | `ux/motion-and-micro-interaction-system/AGENTS.md` | one edit, repoint to the surviving sibling |

Plus one playbook XML slug ref to `motion-and-microinteraction-spec` in
`playbooks/plan-design/zero-to-one-product-design-brief-to-dev-handoff-8-weeks/content/01-playbook.xml`.

**Net: 1 wikilink edit and 1 playbook ref edit** for the whole 40-item deletion.

## Impact if accepted

| Metric | Value |
|--------|-------|
| Directories | 40 |
| Files | 562 |
| Bytes | 1,441,400 (1.37 MB) |
| Manifest entries removed | 40 (3,107 → 3,067) |
| `INDEX.xml` entries to remove by hand | 40 across `backend`, `frontend`, `research`, `ux` |
| Corpus count | 2,638 → 2,598 |
| Genuinely unique subjects lost | **0** for 35 of 40; 5 are subject-level duplicates whose survivor is named per row |

`skills/tier-manifest.json` must be regenerated with `scripts/regen-tier-manifest.py`, never
hand-edited. `INDEX.xml` entries must be removed by hand — `scripts/build-domain-index-v2.py` is
broken and silently empties the file it targets.

## Tier note

35 of the 40 are `pro` or `solo` tier. A paying tier is where the duplicate stubs concentrate;
see the survival sampling in the P2.2 report for the wider version of this problem.

## The table

| # | slug | domain | tier | why waste | inbound refs | KB |
|---|------|--------|------|-----------|--------------|----|
| 1 | `api-authentication` | backend | solo | duplicate stub; real twin `dev/api-authentication` has domain-specific sourced rules | 7 wl / 1 ref -- **0 dangle** (twin keeps the slug) | 39 |
| 2 | `api-contract-first` | backend | solo | duplicate stub; real twin `dev/api-contract-first` has domain-specific sourced rules | 10 wl / 5 ref -- **0 dangle** (twin keeps the slug) | 39 |
| 3 | `api-documentation` | backend | solo | duplicate stub; real twin `dev/api-documentation` has domain-specific sourced rules | 12 wl / 3 ref -- **0 dangle** (twin keeps the slug) | 38 |
| 4 | `api-error-handling` | backend | solo | duplicate stub; real twin `dev/api-error-handling` has domain-specific sourced rules | 18 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 37 |
| 5 | `api-gateway-patterns` | backend | solo | duplicate stub; real twin `dev/api-gateway-patterns` has domain-specific sourced rules | 6 wl / 4 ref -- **0 dangle** (twin keeps the slug) | 37 |
| 6 | `api-graphql` | backend | solo | duplicate stub; real twin `dev/api-graphql` has domain-specific sourced rules | 1 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 35 |
| 7 | `api-openapi-spec` | backend | solo | duplicate stub; real twin `dev/api-openapi-spec` has domain-specific sourced rules | 9 wl / 1 ref -- **0 dangle** (twin keeps the slug) | 39 |
| 8 | `api-rate-limiting` | backend | solo | duplicate stub; real twin `dev/api-rate-limiting` has domain-specific sourced rules | 10 wl / 2 ref -- **0 dangle** (twin keeps the slug) | 36 |
| 9 | `api-rest-design` | backend | solo | duplicate stub; real twin `dev/api-rest-design` has domain-specific sourced rules | 24 wl / 1 ref -- **0 dangle** (twin keeps the slug) | 33 |
| 10 | `api-testing` | backend | solo | duplicate stub; real twin `dev/api-testing` has domain-specific sourced rules | 5 wl / 2 ref -- **0 dangle** (twin keeps the slug) | 40 |
| 11 | `core-vui-design-principles` | frontend | pro | duplicate stub; real twin `ux/core-vui-design-principles` has domain-specific sourced rules | 5 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 33 |
| 12 | `cross-platform-token-distribution` | frontend | pro | duplicate stub; real twin `ux/cross-platform-token-distribution` has domain-specific sourced rules | 8 wl / 5 ref -- **0 dangle** (twin keeps the slug) | 33 |
| 13 | `design-system-success-factors` | frontend | pro | duplicate stub; real twin `ux/design-system-success-factors` has domain-specific sourced rules | 3 wl / 7 ref -- **0 dangle** (twin keeps the slug) | 40 |
| 14 | `enterprise-xr-applications` | frontend | pro | duplicate stub; real twin `ux/enterprise-xr-applications` has domain-specific sourced rules | 4 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 35 |
| 15 | `error-handling-in-vui` | frontend | pro | duplicate stub; real twin `ux/error-handling-in-vui` has domain-specific sourced rules | 5 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 30 |
| 16 | `nextjs-app-router` | frontend | solo | duplicate stub; real twin `dev/nextjs-app-router` has domain-specific sourced rules | 2 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 38 |
| 17 | `react-component-architecture` | frontend | solo | duplicate stub; real twin `dev/react-component-architecture` has domain-specific sourced rules | 10 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 37 |
| 18 | `semantic-tokens-and-modes` | frontend | pro | duplicate stub; real twin `ux/semantic-tokens-and-modes` has domain-specific sourced rules | 6 wl / 5 ref -- **0 dangle** (twin keeps the slug) | 33 |
| 19 | `seo-for-spas` | frontend | solo | duplicate stub; real twin `dev/seo-for-spas` has domain-specific sourced rules | 5 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 37 |
| 20 | `shadcn-ui-architecture` | frontend | solo | duplicate stub; real twin `dev/shadcn-ui-architecture` has domain-specific sourced rules | 6 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 33 |
| 21 | `spatial-computing-overview` | frontend | pro | duplicate stub; real twin `ux/spatial-computing-overview` has domain-specific sourced rules | 5 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 30 |
| 22 | `spatial-design-tools` | frontend | pro | duplicate stub; real twin `ux/spatial-design-tools` has domain-specific sourced rules | 3 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 30 |
| 23 | `spatial-interaction-patterns` | frontend | pro | duplicate stub; real twin `ux/spatial-interaction-patterns` has domain-specific sourced rules | 7 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 30 |
| 24 | `spatial-ui-patterns` | frontend | pro | duplicate stub; real twin `ux/spatial-ui-patterns` has domain-specific sourced rules | 8 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 32 |
| 25 | `storybook-setup` | frontend | solo | duplicate stub; real twin `dev/storybook-setup` has domain-specific sourced rules | 4 wl / 1 ref -- **0 dangle** (twin keeps the slug) | 32 |
| 26 | `tailwind` | frontend | solo | duplicate stub; real twin `dev/tailwind` has domain-specific sourced rules | 5 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 34 |
| 27 | `tailwind-architecture` | frontend | solo | duplicate stub; real twin `dev/tailwind-architecture` has domain-specific sourced rules | 8 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 34 |
| 28 | `token-organization` | frontend | pro | duplicate stub; real twin `ux/token-organization` has domain-specific sourced rules | 3 wl / 4 ref -- **0 dangle** (twin keeps the slug) | 31 |
| 29 | `voice-ui-patterns` | frontend | pro | superset container; parts covered by ux/core-vui-design-principles + ux/error-handling-in-vui (both real) | 2 wl / 0 ref -- 2 would dangle | 32 |
| 30 | `vui-iot-integration` | frontend | pro | duplicate stub; real twin `ux/vui-iot-integration` has domain-specific sourced rules | 4 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 30 |
| 31 | `vui-privacy-security` | frontend | pro | duplicate stub; real twin `ux/vui-privacy-security` has domain-specific sourced rules | 5 wl / 0 ref -- **0 dangle** (twin keeps the slug) | 32 |
| 32 | `audience-segmentation` | research | pro | duplicate stub; real twin `ux/audience-segmentation` has domain-specific sourced rules | 8 wl / 6 ref -- **0 dangle** (twin keeps the slug) | 46 |
| 33 | `product-development-trends-2026-market-research` | research | pro | dated instance of research/product-development-trends-market-research | 0 wl / 0 ref -- 0 would dangle | 43 |
| 34 | `motion-and-microinteraction-spec` | ux | pro | near-identical slug to ux/motion-and-micro-interaction-system; same domain, same subject | 1 wl / 0 ref -- 1 would dangle | 31 |
| 35 | `opportunity-solution-trees` | ux | pro | duplicate stub; real twin `research/opportunity-solution-trees` has domain-specific sourced rules | 2 wl / 12 ref -- **0 dangle** (twin keeps the slug) | 32 |
| 36 | `persona-building` | ux | pro | duplicate stub; real twin `research/persona-building` has domain-specific sourced rules | 10 wl / 4 ref -- **0 dangle** (twin keeps the slug) | 34 |
| 37 | `personas-ux-research` | ux | pro | duplicate subject of research/persona-building (which has real rules) | 0 wl / 0 ref -- 0 would dangle | 33 |
| 38 | `survey-design` | ux | pro | duplicate stub; real twin `research/survey-design` has domain-specific sourced rules | 3 wl / 2 ref -- **0 dangle** (twin keeps the slug) | 36 |
| 39 | `surveys-ux-research` | ux | pro | duplicate subject of research/survey-design (which has real rules) | 0 wl / 0 ref -- 0 would dangle | 33 |
| 40 | `user-research-at-scale` | ux | pro | duplicate stub; real twin `research/user-research-at-scale` has domain-specific sourced rules | 8 wl / 1 ref -- **0 dangle** (twin keeps the slug) | 32 |


## What is NOT on this list

The other 60 members of the generic-100 were rewritten under P2.2 rather than deleted: their
subject is real and no better copy exists. Their `content/01-core-rules.xml` now carries 5-7 rules
about the actual subject with mechanism-bearing rationales, and their `content/06-decision-tree.xml`
routes on subject-specific signals. After that work, the generic 5-rule signature survives in
**exactly the 40 directories listed above and nowhere else in the corpus**.

The 20 partially-stamped methodologies (generic `02-output-contract.xml` + `06-decision-tree.xml`
over real rules, in contiguous `dev/` and `frontend/` runs) are untouched and not proposed for
deletion. They are a smaller, separate cleanup.

## Recommended sequencing if accepted

1. Repoint the 1 wikilink in `ux/motion-and-micro-interaction-system/AGENTS.md` and the 1 playbook
   slug ref, both to the surviving sibling.
2. `git rm -r` the 40 directories.
3. Remove the 40 `<methodology>` blocks from the 4 affected `INDEX.xml` files **by hand**, and
   decrement each file's `count=` attribute. Do not run `scripts/build-domain-index-v2.py`.
4. `python3 scripts/regen-tier-manifest.py --dry-run`, confirm the diff is exactly -40 entries,
   then run it for real.
5. `bash scripts/f066-validate-all.sh` and diff the failing SETS against the pre-change report.

## Open question for the owner

The 35 duplicate pairs are one instance of a wider pattern: **133 slugs exist in more than one
domain, covering 270 directories (10.2% of the corpus)**. This CR only proposes removing the 35
whose duplicate copy is provably generic. The remaining ~235 duplicated directories have not been
compared pair-by-pair, and some of them are presumably also redundant. Deciding the general policy
— are cross-domain slug duplicates ever legitimate? — is a bigger call than this CR, and it should
probably be made before the next content-generation run rather than after.

## Execution record

Executed 2026-08-14. Commits: `aff68a925` (reference repair) · `770c47b2f` (deletion + L2 indexes
+ lexicon) · `54cbf07cb` (tier manifest).

### Re-verification: 40 of 40 survived

Every row was re-checked against disk before anything was removed, on four tests: the directory
exists; its `content/01-core-rules.xml` carries all five generic rule ids; the other four content
files carry their generic markers; and `AGENTS.md` carries the stock `## Applies If` lines. For
the 39 rows naming a survivor, the survivor had to exist, carry no generic rule ids, and hold at
least three real rules of its own.

**All 40 passed. None was spared, and none needed re-classifying.** The survivors are real: the
`dev/*` API twins carry 6-10 subject rules each, `ux/core-vui-design-principles` pins
`fifteen-second-ceiling` and `barge-in-supported`, `research/survey-design` pins
`twelve-question-cap` and `sample-size-120-per-segment`.

Three survivors — `ux/audience-segmentation`, `research/product-development-trends-market-research`
and `ux/motion-and-micro-interaction-system` — turned out to be *partially* stamped themselves
(generic output contract, procedure and failure modes over real, sourced core rules and a real
decision tree). They are strictly better than the candidates they replace, so the deletions stand,
but this widens the "20 partially-stamped" set noted above beyond the contiguous `dev/` and
`frontend/` runs. Worth folding into that separate cleanup.

### Measured impact

| Metric | Predicted | Actual |
|--------|-----------|--------|
| Directories | 40 | **40** |
| Files | 562 | **562** |
| Bytes | 1,441,400 | **1,441,400** |
| Manifest entries | 3,107 → 3,067 | **3,107 → 3,067** (`+0 added, -40 removed, ~0 changed`) |
| Corpus count | 2,638 → 2,598 | **2,638 → 2,598** |
| Dangling references | 21 → 21 | **21 → 21**, same set: 20 × `[[Related]]` + 1 × `[[bin]]` |

`INDEX.xml` and `domains.xml` counts, both re-derived from disk and now agreeing with it:

| Domain | Removed | count= |
|--------|---------|--------|
| `backend` | 10 | 147 → 137 |
| `frontend` | 21 | 42 → 21 |
| `research` | 2 | 82 → 80 |
| `ux` | 7 | 186 → 179 |

### Where the estimate was wrong

- **The motion references were 4, not 1.** `ux/motion-and-micro-interaction-system` linked
  `[[motion-and-microinteraction-spec]]` twice (`## Assumes Loaded` row *and* `## Related` bullet),
  and named the dead slug twice more in prose — a skip-rule in `01-core-rules.xml` and a verdict in
  `06-decision-tree.xml` both routing the caller to it. All four fixed. The links were dropped
  rather than repointed: the only survivor is the referring file itself, and a self-link is not a
  reference.
- **The playbook reference was a `<gap>`, not a `<ref>`.** `<gap>` declares a slug the corpus is
  *missing* — `design-dev-handoff-package`, its neighbour, genuinely does not exist. So
  `motion-and-microinteraction-spec` was already wrongly filed as a gap while it sat on disk. It
  became a `<ref>` to the surviving sibling in stage 7, whose task line already reads
  "spec: states, tokens, motion". (`design-qa-during-build` is a second spurious gap in the same
  block — it exists at `ux/design-qa-during-build`. Left alone; out of scope.)
- **One unpredicted knock-on: the lexicon.** `frontend/spatial-design-tools` was the only place in
  the corpus tagged `unity`, so after deletion the `юніті` row no longer qualified as `src=title`
  and `validate-lexicon.py` failed. Provenance is data re-derived from the corpus, so the fix was
  to record what the corpus now says — `observed`. The validator baseline was **not** widened, and
  no baseline row pointed at a deleted directory, so none became obsolete.
