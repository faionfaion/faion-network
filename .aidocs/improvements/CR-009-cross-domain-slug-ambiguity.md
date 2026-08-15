---
type: change-request
cr_id: CR-009
title: "99 slugs exist in two domains, and 1,266 links cannot say which one they mean"
priority: P1
created: 2026-08-15
status: executed 2026-08-15 — 77 archived, 19 deliberately left, renames deferred
affected_components: [faion-network/skills/faion/knowledge]
blocks: "publication — a link that resolves arbitrarily is a retrieval defect, not a cosmetic one"
---

# Change Request: cross-domain slug ambiguity

**This document proposes nothing be moved today.** It is the evidence for a decision the repo
owner makes.

Surfaced while closing the last duplicate-summary group. CR-005 recorded, as the reason its 40
deletions were safe, that **wikilinks and `<ref slug=…>` resolve by SLUG, not by path** — so
deleting `backend/api-rest-design` while `dev/api-rest-design` survived left all 24 inbound
`[[api-rest-design]]` links resolving exactly as before.

That property cuts both ways, and the other edge has not been measured until now.

## The measurement

| | |
|---|---|
| Slugs appearing in **more than one domain** | **99** |
| Directories involved | **201** (7.7% of 2,601) |
| `[[wikilinks]]` pointing at an ambiguous slug | **839** across 97 slugs |
| `<ref slug="…">` pointing at an ambiguous slug | **427** across 50 slugs |
| **Total links that cannot name their target** | **1,266** |

The most-linked:

| Links | Slug | Lives in |
|--:|---|---|
| 92 | `architecture-decision-records` | `architecture`, `sdd` |
| 56 | `product-analytics` | `product`, `pm` |
| 42 | `secrets-management` | `backend`, `infra` |
| 40 | `wcag-22-compliance` | `frontend`, `ux` |
| 34 | `continuous-discovery` | `research`, `product` |
| 34 | `feedback-management` | `product`, `pm` |
| 33 | `user-interviews` | `research`, `ux` |
| 32 | `jobs-to-be-done` | `research`, `ux` |

**None of the 99 has byte-identical content across its copies** — but that is not evidence they
are different documents. The `research/ai-assisted-persona-building` pair examined in full differs
*only* where the slug is substituted into a title, a summary and a `$id`; four of its six content
parts are identical to the byte and the other two differ by 9 and 18 bytes. Two documents can be
the same document and still not be byte-equal.

## Why this is a defect and not an inconvenience

A reference that names `[[secrets-management]]` has two candidates and no way to choose. Whatever
the resolver does — first match, alphabetical, manifest order — the answer is a fact about the
resolution order rather than about what the author meant. That is the same failure
`meta-json-spec.md` §12.1 identifies for duplicate summaries, one layer down: **not a document
described badly, a document that cannot be addressed as itself.**

It matters more now than it did. Under ADR-018 the client held a full tier-filtered index and
could see both. Under ADR-019 retrieval runs server-side and returns chunks the caller did not
name, so a caller has no way to notice it was handed the wrong one of two.

## What this is not

It is not the CR-005 population. Those were 100 methodologies carrying a detectable generation
stamp, of which 40 were redundant. **Only some of these 99 are duplicates**; others are two
genuinely different documents that happen to share a name — `dev/accessibility` and
`frontend/accessibility` may well both deserve to exist, under names that say which is which.

So the fix is not one action. It is a triage.

## Triage result, 2026-08-15 — three of this CR's premises were wrong

All 99 classified by reading every shared `content/*.xml` line-by-line and localising where the
bytes differ. The measurement above reproduced exactly; the reasoning did not survive.

**1. The DUPLICATE bucket as defined above is empty — 0 of 99.** Not one pair confines its
differences to `<text title>` / `summary` / `$id` / `est_tokens`. Highest line-similarity in the
corpus is 0.67 (`user-story-mapping` pm~product); the median is ~0.30. These are not one document
filed twice — they are **two independently generated documents per subject**.

**2. Reference counts cannot pick a survivor, anywhere.** Links resolve by slug, so all 1,266 are
per-*slug*, not per-copy: there is no inbound count for either side of any pair. The tiebreak this
CR leaned on does not exist. It also means **archiving is free** — the survivor keeps the slug and
zero links dangle — while **renaming is the expensive move**, because it splits a slug that 1,266
links cannot distinguish, so every one must be re-decided by hand.

**3. The VARIANT bucket is empty, and that is a finding rather than an omission.** A variant
presumes an authored intent, and nothing records one: no `meta.json` field marks a variant
relationship, no `AGENTS.md` names its twin, and across 1,266 links there is exactly **one**
cross-reference between any two twins. Every distinguishable pair is distinguishable by a
qualifier, which makes it a collision; where no qualifier exists, it is the same document written
twice.

Two further corrections fall out:

- **`content_id` is not a content hash.** 47 of the 99 pairs carry an identical one while
  differing in every rule; corpus-wide, 165 ids are shared across 334 directories and **every one
  of those groups differs in content bytes**. Never use it as a duplication test — this CR's own
  earlier siblings did, and are annotated.
- **The CR-005 stamp is gone entirely** (`anchor-evidence-required`: 0 files). The only automatic
  discriminator left is the *partial* stamp — generic `artefact_id` / `template_version` /
  `last_touched` — present in 57 of the 201 directories.

**Link topology is cleanly split and it matters:** all 839 wikilinks originate in `knowledge/**`
`## Related` rows, while all 427 `<ref slug=>` originate in `playbooks/**` as pipeline steps.
Handing back the wrong twin is a broken link in the first case and **broken execution** in the
second.

| Bucket | Slugs | Links |
|---|--:|--:|
| Same subject, one side weaker — archive the loser | 34 | 443 |
| Collision — rename one side | 22 | 371 |
| Variant | **0** | 0 |
| No discriminator — needs a human | **43** | 452 |

**Only 2 of the 34 are provable by defect**, and both are executed below. The other 32 rest on a
single signal — a partial stamp, a missing canonical part, stub rules, or bare `r1..rN` ids — and
each names real content on both sides, so they are **merge-then-archive**: fold the loser's unique
rules into the survivor first, or real material is lost.

Of the 43 unresolved, **28 are one question**: whether `backend/` and `dev/` are permitted to cover
the same subject. A stated authoring policy would settle them in a single stroke. The remaining 15
need a per-pair editorial read, and 12 of those have *conflicting* signals — the stamped side is
the larger or better-ruled one.

### Executed

| Archived | Survivor | Why it is provable rather than judged |
|---|---|---|
| `dev/shadcn-ui` | `frontend/shadcn-ui` | 4 parts / 5.8 KB against 6 / 20.5 KB; its single rule is literally named `r1` and the file carries **12 `TBD` markers**, against seven named subject rules on the survivor |
| `dev/ruby-sidekiq-jobs` | `backend/ruby-sidekiq-jobs` | Its five rules are the generic scaffolding set (`r1-bound-scope`, `r2-typed-input`, …) and **not one concerns Sidekiq**; the survivor carries seven that do, including `r-idempotent-perform` and `r-per-queue-concurrency` |

Both archived to `.archive/knowledge/`. Manifest 3,067 → 3,065, knowledge 2,601 → 2,599, and both
slugs still resolve — to the survivor, as intended.

## Options

1. **Triage the 99 into three buckets and act per bucket.** *Same document* → archive one, repoint
   its links. *Different documents, colliding name* → rename one so the slug says which it is.
   *Deliberate domain-specific variant* → keep both, but the reference syntax must gain a domain
   qualifier, because no renaming fixes a case where both names are correct.
2. **Rename every collision mechanically** — prefix the slug with its domain. Uniform, one pass,
   and wrong: it renames 201 directories including the ones that are genuine duplicates, so the
   corpus keeps both copies forever under tidier names.
3. **Make the reference syntax carry the domain** — `[[ux/user-interviews]]`. Fixes ambiguity
   without touching content, but rewrites 1,266 links, and leaves the actual duplicates in place.
4. **Record and defer.** Defensible only if the resolver is proven deterministic *and* the choice
   it makes is proven correct for all 1,266 — neither of which anyone has measured.

## Recommendation

**Option 1**, sequenced by link count so the triage pays off earliest: the eight slugs listed
above carry 363 of the 1,266 links between them, so triaging eight documents settles 29% of the
ambiguity.

Two things must be settled before any of it, and both are outside this corpus:

- **What the resolver actually does today** with an ambiguous slug. This CR assumes nothing; it
  measures the corpus. If `faion-cli` resolves deterministically and correctly, the priority
  drops. If it takes the first match in walk order, 1,266 links are silently wrong.
- **Whether renaming is affordable.** A slug rename changes the directory path, and `doc_id` is
  `sha256(path + "\n" + body)[:16]` — so every rename invalidates a pinned `cv` for that document.
  Like CR-008, this has to land **before** publication rather than after.

Not fixed here, and deliberately: `research/ai-assisted-persona-building` ↔
`research/ai-persona-building`, the last remaining duplicate-summary group. Archiving one in
isolation would silently redirect its links to the `ux/` copy of the same slug, which is a
resolution change nobody decided. It belongs in this triage.

**Do not execute without the owner's approval.**

---

# Execution record, 2026-08-15

Owner approved. Executed under
[`.aidocs/conventions/domain-boundaries.md`](../conventions/domain-boundaries.md), which was
written for this CR and is the first stated rule for which domain a methodology belongs to.

| | Slugs |
|---|--:|
| Ambiguous at triage | **97** |
| Resolved merge-then-archive | **77** |
| **Deliberately left ambiguous** — both copies are real documents | **19** |
| Remaining undecided | **0** |

Corpus 2,601 → **2,520** methodologies; 81 directories archived to `.archive/knowledge/`.

## What the execution proved wrong about this CR

**1. Its per-pair content claims are unreliable; only its bucket assignment is.** Four pairs were
briefed as "nothing unique on the loser" — `php-laravel-patterns`, `ruby-rails-patterns`,
`java-spring`, `csharp-dotnet-patterns`. **All four were false on reading.** `java-spring`'s loser
held four rules and five templates, one of which (`maven-annotation-processors.xml`) was the only
file backing a rule the *survivor* already had. `csharp-dotnet-patterns`'s loser held eleven rules'
worth, most of it in an `agent-integration.md` the brief never mentioned.

This is why the method is **merge-then-archive** and not archive-then-regret. The ordering is the
safeguard, and it earned its keep four times.

**2. The stance hypothesis is not the boundary.** "Operating policy vs craft/idiom" was tested
against all 28 undecided `backend`↔`dev` pairs: it explains 6, **reverses on 3**, and leaves 18
that are simply the same document written twice. The boundary that fits the corpus is *execution
surface*, evidenced by what each domain already produces — `backend` has written **one checklist
and zero rubrics in 137 documents** while `dev` writes judgement instruments in 21% of 378.

**3. The partial generation stamp does not name a loser.** Tested on the four pairs where it was
the only signal (`database-design`, `go-concurrency-patterns`, `go-error-handling-patterns`,
`ruby-rspec-testing`): in every one the stamped side was the *richer* one. The stamp records how a
document was made, not how good it is.

**4. `content_id` is derived from slug identity.** Confirmed from the other direction during
execution: one id covers three unrelated `workflows` documents, another both `secrets-management`,
another all three continuous-discovery documents. This is very likely *why* several unrelated
documents looked like duplicates to the original triage.

## The 19 left standing, and why that is an answer

Archiving a real document costs more than leaving a slug ambiguous for one more round. In each of
these, both copies are genuinely different documents, so the correct fix is a **rename** — and a
rename changes the path, therefore `doc_id`, therefore any pinned `cv`, and splits a slug that
1,266 inbound links cannot distinguish. Deferred to task #32, to land before publication.

The sharpest cases:

- **`secrets-management`** — the split is authored and **bidirectional**: `backend`'s decision tree
  *skips to* `infra` when audit-logged secrets are required, and `infra`'s Skip-If routes back for
  dev-only `.env`. A merge is structurally impossible — `backend` produces a multi-secret plan,
  `infra` a single-secret record. They also publish **incompatible schemas under one `$id`**, which
  is a broken contract rather than an ambiguous slug.
- **`accessibility`** — the two output schemas share **zero required fields**. `dev`'s is a
  per-screen instrument, `frontend`'s the codebase-wide target that instrument asserts against.
- **`workflows`** — four domains, four unrelated subjects, no scaffold among them.

## Costs incurred, recorded rather than hidden

- **5 merges moved higher-tier material into a lower-tier survivor**, two of them `pro` → `free`.
  CR-009 measured content and links and never measured tier; the boundary policy picks a survivor
  by execution surface, which does not take tier as an input. Neither system could see it. Task #33.
- **3 survivors were the currently weaker copy**, kept because the policy said so and because §5
  makes choosing free while moving is not. `pnpm-package-management` is the clearest: kept in `dev`
  despite being thinner, because a rule that applies only when convenient is not a rule.
- **`ruby-rails` and `java-spring-boot-patterns`** each folded two genuinely distinct documents into
  one. Both are recorded in `domains.xml` §7 as owner's-eye items.

## Verified, not assumed

- **81 archived slugs, 0 orphans** — every archived slug still resolves to a live survivor.
- **0 dangling links.** The five slugs that scan as unresolvable are all false positives:
  `slug` is a literal placeholder inside a template, `bin`/`rules` are path fragments, and
  `non-existent-slug`/`setup-guide` are *deliberate* examples inside
  `sdlc-ai/ai-orphan-link-detection` — a methodology about detecting orphan links.
- L1 `domains.xml` and all 22 L2 `INDEX.xml` regenerated; both index validators clean.
