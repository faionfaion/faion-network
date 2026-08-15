---
type: change-request
cr_id: CR-007
title: "12 duplicate playbook pairs, and the stamp that marks which copy is redundant"
priority: P1
created: 2026-08-15
status: executed 2026-08-15 — archived, not deleted
affected_components: [faion-network/skills/faion/playbooks, skills/tier-manifest.json]
blocks: "publication — retrieval-content-contracts.md §4"
---

# Change Request: the duplicate playbook pairs

**This document proposes nothing be deleted today.** It is the evidence for a decision the repo
owner makes. Every directory named below is still on disk and still resolves.

Surfaced by the summary audit for AD-019: a summary must be unique corpus-wide, because two
documents with the same summary score identically against every query and the ranker then orders
them by `doc_id` — the answer becomes a fact about a hash rather than about the question. Fixing
the duplicates by rewriting prose would be wrong if the documents themselves are redundant, so
this is settled first.

**CR-005 audited knowledge only. Nobody had audited playbooks.** This is where the duplication
turns out to be.

## What the pairs are — and what they are not

14 duplicate-summary groups exist: one group of 5 methodologies (`ux/*-a11y`, handled separately)
and **13 pairs, 12 of them playbook↔playbook**.

Two hypotheses were tested and **both are wrong**:

- **Not byte-identical copies.** Unlike `sdd/templates` (CR-006), every pair has two different
  `content_id` values and two different content bodies. Measured on two pairs: 106 of 174 lines
  differ, 152 of 246 differ.
- **Not one directory filed under two goal categories.** `retrieval-content-contracts.md` §4
  suggests "one structural fix, not 12 rewrites". **11 of the 12 pairs sit inside the *same* goal
  category** — `acquire-grow` ×4, `build-ship` ×3, `operate-ritual` ×3, `govern-decide` ×1,
  `migrate-rebuild` ×1. Only `proposal-from-discovery-notes` (acquire-grow) ↔
  `proposal-draft-from-discovery-notes` (build-ship) crosses. There is no structural fix; these
  are 12 independent authoring duplications.

They are two separately written playbooks about the same task, given the same summary.

## The discriminator: a boilerplate `<intent>`

**31 of 455 playbooks carry a generic `<intent>`** that says nothing about the playbook:

> *From the initial trigger to the closed outcome described in scope, deliver every artefact named
> in success_criteria without skipping the decision gates between stages.*

A real one restates its own subject — `weekly-positioning-post` has *"One post per week that
reinforces specialization niche. Done = post published, engagement triaged, follow-up DMs handled
within 48h."*

**Of the 12 pairs, exactly one side is stamped in 9. Neither side is stamped in 3. Both sides are
stamped in none.** That is the CR-005 shape: the stamp marks the redundant copy.

## Evidence table

`refs` counts inbound references from anywhere in `skills/` other than the playbook's own
directory. **`refs: 1` means only its own goal `INDEX.xml` points at it** — no methodology, no
other playbook, nothing.

| Goal | Slug | Stamp | Bytes | Refs |
|---|---|:--:|--:|--:|
| govern-decide | `scope-change-conversation` | — | 4,224 | **2** |
| | `scope-change-conversation-when-client-says-just-one-more-thing` | **YES** | 5,344 | 1 |
| acquire-grow | `reputation-referral-pipeline-ramp` | — | 6,435 | **2** |
| | `reputation-referral-pipeline-ramp-90-day-flywheel` | **YES** | 6,838 | 1 |
| acquire-grow → build-ship | `proposal-from-discovery-notes` | — | 4,506 | 1 |
| | `proposal-draft-from-discovery-notes` | **YES** | 6,149 | 1 |
| acquire-grow | `weekly-positioning-post` | — | 4,155 | **2** |
| | `weekly-positioning-post-linkedin-twitter` | **YES** | 5,269 | 1 |
| acquire-grow | `cold-lead-to-signed-contract` | — | 6,398 | **2** |
| | `cold-lead-to-signed-contract-3-week-acquisition-flow` | — | 6,360 | 1 |
| acquire-grow | `cold-lead-inbound-reply` | — | 3,609 | 1 |
| | `cold-lead-reply-linkedin-email-inbound` | **YES** | 5,254 | 1 |
| build-ship | `project-kickoff-to-handover` | — | 6,897 | **2** |
| | `project-kickoff-to-handover-typical-6-12-week-engagement` | — | 7,873 | 1 |
| build-ship | `productized-service-launch` | — | 7,062 | **9** |
| | `productized-service-launch-4-week-sprint` | — | 7,465 | 1 |
| operate-ritual | `project-closure-debrief` | — | 4,499 | **4** |
| | `project-closure-debrief-retrospective` | **YES** | 6,238 | 1 |
| operate-ritual | `quarterly-portfolio-rebalance` | — | 6,488 | **2** |
| | `quarterly-portfolio-rebalance-cash-clients-capacity` | **YES** | 6,744 | 1 |
| operate-ritual | `year-end-tax-legal-cashflow-close` | — | 6,420 | 1 |
| | `year-end-tax-legal-and-cash-flow-close` | **YES** | 6,662 | 1 |
| migrate-rebuild | `freelance-to-saas-without-losing-runway` | — | 5,448 | 1 |
| | `freelancer-to-saas-transition-without-losing-the-runway` | **YES** | 7,063 | 1 |

**Three signals agree in all 12 pairs**, which is why this is a measurement rather than a
judgement call:

1. The stamped side is stamped; the other is not (9 pairs).
2. The stamped side is **larger** in 9 of 9 — the boilerplate pads it.
3. The stamped side has `refs: 1` in 9 of 9, while the other side has ≥1 and usually more.

**Do not decide by slug length.** The stamp is on the *shorter*-named side in two pairs
(`quarterly-portfolio-rebalance-cash-clients-capacity` is stamped and its twin is not;
`year-end-tax-legal-and-cash-flow-close` likewise). Name length is not the signal; the stamp and
the reference count are.

For the **3 unstamped pairs**, the reference count alone separates them, and cleanly:
`productized-service-launch` at **9** inbound refs against 1, `project-kickoff-to-handover` at 2
against 1, `cold-lead-to-signed-contract` at 2 against 1. In each, the survivor is the one the
corpus actually points at.

## The wider population

31 playbooks carry the stamp. 9 are in a pair. **22 are stamped and have no twin** — the exact
analogue of CR-005's split, where 40 of 100 stamped methodologies were redundant and 60 named a
real subject with no better copy and were rewritten instead of deleted. Those 22 are a separate
item: they are not duplicates and must not be deleted, but their `<intent>` says nothing and
should be written.

## Options

1. **Delete the redundant side of each pair — 12 directories.** Survivor chosen by the stamp
   where it exists, by reference count where it does not; both agree wherever both apply. Then
   regenerate the playbook indexes and the tier manifest. Cost: 12 directories, ~36 files. Risk is
   low — every deletion candidate is referenced only by the index that lists it, so nothing but
   that index needs repointing.
2. **Merge before deleting.** Read each pair and lift anything the survivor lacks. Honest, but
   note that the deletion candidate is the *stamped* one in 9 of 12, and its extra bytes are
   boilerplate rather than substance — so merging mostly means merging padding.
3. **Keep both and rewrite one summary each.** Satisfies §12 uniqueness mechanically while leaving
   the corpus carrying 12 pairs of near-identical playbooks. This makes retrieval return two
   answers to one question, which is the problem §12 exists to prevent, one level up.

## Recommendation

**Option 1**, with a re-verification pass before anything is removed, as CR-005 did: re-check each
candidate against disk for the stamp, confirm the survivor exists and is unstamped, and confirm
the candidate's inbound reference set is exactly its own goal index.

Then the 22 stamped singletons get their `<intent>` written — a separate, non-destructive task.

**Do not execute without the owner's approval.** Corpus deletion carries a re-verification pass
against disk, and this CR is evidence, not a mandate.
