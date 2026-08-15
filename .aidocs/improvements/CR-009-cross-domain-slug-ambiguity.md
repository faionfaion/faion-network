---
type: change-request
cr_id: CR-009
title: "99 slugs exist in two domains, and 1,266 links cannot say which one they mean"
priority: P1
created: 2026-08-15
status: proposed
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
