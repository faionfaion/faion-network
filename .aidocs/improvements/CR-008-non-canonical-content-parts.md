---
type: change-request
cr_id: CR-008
title: "251 content files no --parts name can address, and 7 documents that are wholly unreachable"
priority: P1
created: 2026-08-15
status: proposed
affected_components: [faion-network/skills/faion/knowledge]
blocks: "publication — retrieval-content-contracts.md §1"
---

# Change Request: the non-canonical content parts

**This document proposes nothing be renamed today.** It is the evidence for a decision the repo
owner makes.

`retrieval-content-contracts.md` §1 fixes the chunk boundary at the corpus's own numbered parts
and closes the `--parts` vocabulary at six names. It records ~200 non-canonical filenames as an
open question: fold them into a canonical name, or admit them to the vocabulary — noting that
admitting widens a closed vocabulary, which is the thing the closure exists to prevent.

Measured: **251 files, 202 distinct names, across 93 of 2,601 slugs (3.6%)**. But they are not one
problem. They are two, and only one of them is urgent.

## Population A — 86 slugs: extras beside a complete canonical set

| Canonical parts present | Slugs |
|---|--:|
| 6 of 6 | 45 |
| 5 of 6 | 38 |
| 4 of 6 | 3 |

These documents already have their canonical parts. The non-canonical file sits **beside** one, at
an ordinal the canonical file already occupies:

```
ai-agents/claude-code-headless-default
  01-cli-vs-sdk-decision   01-core-rules   02-invocation-shape   02-output-contract
  03-failure-modes         04-procedure    06-decision-tree

ai-agents/two-pass-reason-then-extract
  01-core-rules   01-rule   02-cost-model   02-output-contract
  03-failure-modes   04-procedure   06-decision-tree
```

So `01-cli-vs-sdk-decision` is not a *replacement* for `01-core-rules` — it is an additional part
sharing its ordinal. **223 of the 251 sit at an ordinal already taken by a canonical file.**

That rules out the obvious fix: these cannot simply be renamed to a canonical name, because the
canonical name in that slot is occupied by a different file with different content.

What they are is **authored content the corpus cannot deliver** — a caller asking for
`--parts core-rules` gets `01-core-rules.xml` and never learns `01-cli-vs-sdk-decision.xml`
exists.

## Population B — 7 slugs: no canonical part at all

These have **zero** of the six. Nothing in them is addressable, so the whole document is
unreachable through the chunk contract:

| Slug | Its parts |
|---|---|
| `sdd/cr-bug-tracking` | `01-cr-flow`, `02-bug-flow`, `03-numbering`, `04-feature-linkage` |
| `sdd/plan-md-structure` | `01-shape`, `02-when-to-skip`, `03-rationale` |
| `sdd/project-spec-structure` | `01-folder-shape`, `02-rebuild-test`, `03-delta-update`, `04-location-decision` |
| `sdd/quality-gates` | `01-stack-matrix`, `02-enforcement`, `03-test-tools` |
| `sdd/readiness-checklist` | `01-checklist`, `02-quality-gates`, `03-surface-coupling` |
| `sdd/ui-ux-design-template` | `01-when-required`, `02-nielsen-five`, `03-norman-principles`, `04-template-sections` |
| `sdd/user-flows-template` | `01-when-required`, `02-shape`, `03-positive-negative` |

**All seven are in `sdd/`**, which reads as a cluster authored to a different shape rather than
seven independent mistakes.

**These are not obscure.** `faion-cli/.aidocs/project-spec/AGENTS.md` names
`project-spec-structure` as the methodology its own spec directory implements — *"First pilot of
the `project-spec-structure` methodology shipped in `faion-network`"*. A live, cited methodology
whose content the delivery path cannot return is the sharpest form of this defect.

`validate-methodology-v2.py` accepts all of them, which is why nothing has flagged it.

## Options

1. **Fold Population B into canonical names; leave A.** The 7 sdd documents get their parts mapped
   onto the six canonical names — `01-shape` → `core-rules`, `02-when-to-skip` → `decision-tree`,
   and so on per document. 7 documents, ~24 files, and every one of them becomes retrievable.
   Population A stays unreachable but its documents are not: their canonical parts already carry
   the load-bearing content. **Cheapest fix for the sharpest half of the problem.**
2. **Fold both.** Population A's 223 extras must be *merged into* the canonical file at their
   ordinal, not renamed, since the name is taken. That is 223 content merges across 86 documents —
   real editorial work, and each merge risks blurring a part that was deliberately split.
3. **Admit the names to the vocabulary.** Rejected by §1's own reasoning: 202 distinct names, 179
   of them used exactly once, would turn a closed six-name vocabulary into an open one whose
   unknown-name error can no longer be raised before the corpus loads.
4. **Do nothing and record it.** Defensible for A, not for B: a document with no addressable part
   is not a document the retrieval contract can serve at all.

## Recommendation

**Option 1.** It closes the case where the contract is actually broken — 7 documents, ~24 files,
one domain, one coherent authoring pass — and leaves the larger, blurrier half recorded rather
than half-done. Population A should then get its own decision with its own evidence, because
"merge 223 files" is a different kind of change from "rename 24".

Renaming a content file changes its `doc_id`, since the id is `sha256(path + "\n" + body)[:16]`.
Any `cv` pinned before the change stops resolving those parts, so this must land **before**
publication rather than after — which is what makes it a blocker rather than a cleanup.

**Do not execute without the owner's approval.**
