---
type: change-request
cr_id: CR-010
title: "602 KB of hand-written methodology content ships and is never delivered"
priority: P1
created: 2026-08-15
status: proposed
affected_components: [faion-network/skills/faion/knowledge]
blocks: "publication — the corpus is paid for by the token, and 40% of the median affected document is unreachable"
supersedes_context: "CR-008 recorded 251 non-canonical part names as a naming defect. This is what those names are actually costing."
---

# Change Request: the corpus ships content it cannot deliver

**This document proposes nothing be changed today.** It is the evidence for a decision the repo
owner makes once, for 69 directories, rather than 69 times.

## The measurement

A methodology's `AGENTS.md` carries a `## Content` table. That table is what a retrieval call
resolves against — a `content/*.xml` file not listed in it is packed by `vfs-pack`, shipped to the
client, cached under `~/.faion/corpus/<cv>/`, and **never returned**.

| | |
|---|---|
| Methodology directories checked | 2,528 |
| Directories holding content the table does not list | **76** |
| Files | **185** |
| Unreachable bytes | **621 KB** |
| Median share of an affected directory's content that is unreachable | **40%** (worst: 57%) |

7 of those directories were withholding a **canonical** part — `03-failure-modes`, `04-procedure`
or `05-examples`. A canonical part is mandatory by the corpus spec, so that was a straightforward
defect and is **already fixed**. This CR is about the other **69 directories, 177 files, 602 KB**.

## The cause, and it is a single one

Every one of the 69 already has 4–6 canonical parts. **There are no legacy-only directories.** The
unlisted files sit *beside* a complete canonical set.

That is the signature of a generation pass: **F-066/F-067 generated a canonical wrapper around an
existing hand-written body, listed only the wrapper in the table, and left the body on disk under
its original names.** One directory still says so out loud — `marketing/ops-customer-success-basics`
has a canonical `01-core-rules.xml` whose own summary reads *"Migrated testable rules …
`source="v1-source"`"*, with the file it migrated from still sitting next to it.

Two consequences follow, and the second is the trap:

1. Every one of the 69 has a **numeric-prefix collision** — `01-ga4-setup.xml` beside
   `01-core-rules.xml`, `02-examples.xml` beside `02-output-contract.xml`.
2. So **the obvious fix is blocked**: you cannot rename the legacy file to its canonical name,
   because the slot is already occupied by the generated wrapper.

## What is actually in there

Sampled 9 files in full plus targeted analysis across all 177. The classification is lopsided:

| Group | Files | KB |
|---|--:|--:|
| **(a) genuinely unique content** | **172** | **586** |
| (b) duplicates of a canonical part | 1 clear + 4 partial | 3.6 + 12.6 |
| (c) empty or boilerplate stubs | **0** | 0 |

**Group (c) is empty, and that is the finding that decides the CR.** The smallest file is 1.7 KB,
the median 3.4 KB; all 177 parse and carry real sections. Seven matched a TODO/TBD/PLACEHOLDER
grep and all seven turned out to be *subject matter* — an accessibility rule about placeholder
text, an SDD rule forbidding TBDs — not authoring stubs.

**The inversion is the point.** In every directory opened, the canonical parts are the generated
scaffolding — *"≥5 testable rules with rationale + source"*, *"JSON Schema draft-07 + valid/invalid"*
— while the unlisted legacy files hold the hand-authored subject matter the methodology is named
after:

- `marketing/ads-analytics-setup/01-ga4-setup.xml` — GA4 custom-dimension hard limits,
  `transaction_id` dedup, the BigQuery-export-cannot-backfill trap. None of it in the canonical parts.
- `dev/clean-architecture-quality/02-domain-layer.xml` (+ `03-`, `04-`) — the actual entity,
  value-object and repository-interface code. That directory has **no canonical `05-examples.xml`**;
  these files *are* its examples.
- `sdd/key-trends-summary/03-platform-observability.xml` — the methodology's stated purpose is
  "6 SDD trends" and **all six live in unlisted files**.
- `research/competitor-analysis/03-gotchas.xml` — the Crunchbase-hallucination rule, G2
  paid-placement skew, geography pinning. Its canonical `03-failure-modes.xml` shares under 30%.
- `ai-agents/terse-default-tool-output/01-terse-default.xml` — the same rule as the canonical file,
  but carrying the good/bad examples and the arXiv references the canonical rewrite dropped.

Supporting datum: **26 of the 69 have no canonical `05-examples.xml` and 5 have no
`04-procedure.xml`.** The unreachable files are frequently the only examples or procedure the
methodology has.

## Why this outranks the naming problem

CR-008 recorded 251 non-canonical part names and was deferred as a tidiness item. That
classification was wrong, and this is the correction: the names are not the cost. **The cost is
that the best content in these documents is the content an agent never sees.**

It bears directly on the business model. The corpus is sold on token economy and answer quality —
so a document whose generated wrapper is delivered while its hand-written body is withheld
delivers the *worse* half at full token price. And under ADR-019 retrieval moved server-side, so a
caller receives chunks it did not name: there is no way for a user to notice that the good part
was never in the response.

## Options

1. **Fold each legacy file's substance into the canonical part that should own it, then delete the
   legacy file.** The only option that puts the content in front of an agent. Cost: ~586 KB of
   editorial work across 69 directories. Directional fold destinations, regex-bucketed: ~47 files
   read as core-rules material, ~32 as worked examples, ~21 as procedure, ~5 as failure modes, and
   **~72 as reference/orientation content with no obvious canonical home** — that last bucket is
   the real difficulty and may force a schema decision anyway.
2. **Renumber into a free canonical slot.** Works only where the slot is empty — the 26 directories
   missing `05-examples` and the 5 missing `04-procedure`. Covers under half the population and
   does nothing for the rest.
3. **Accept a documented non-canonical extension in the schema and list the files.** Cheap and
   immediate. It blesses 60+ ad-hoc part names and contradicts CR-008 — but it is the only option
   that makes 602 KB reachable this week rather than this quarter.
4. **Delete the legacy files.** Defensible only if the canonical wrapper genuinely supersedes them,
   and group (a) at 97% says it does not.

Group (b)'s 5 files can be deleted regardless of which way (a) goes.

## Recommendation

**Option 3 as a stopgap, then Option 1 as the real fix**, in that order and stated as such rather
than pretending the stopgap is a solution. The argument: today the content is 100% unreachable and
every day of editorial work leaves it unreachable; a documented extension makes it reachable
immediately and costs a schema concession that Option 1 later reverses directory by directory.

Anything that ships before this is decided ships a corpus whose median affected document withholds
40% of itself.

## What this does not settle

- **Whether the generated wrapper should exist at all** in these 69. If the hand-written body is
  the better document, the wrapper may be the thing to fold *into it*, not the reverse.
- **The 19-directory boilerplate question.** Three of the 7 canonical parts just listed are
  near-identical text shared by 19 methodologies. Listing them matched the corpus norm — 16 of the
  19 already did. If boilerplate should not be delivered at all, that is a 19-directory decision
  and not one this CR takes.
