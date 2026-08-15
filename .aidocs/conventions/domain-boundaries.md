---
type: convention
title: "Which domain a methodology belongs to"
created: 2026-08-15
status: ratified
applies_to: [skills/faion/knowledge]
supersedes: "nothing — this is the first stated boundary; the corpus was authored without one"
---

# Domain boundaries

The corpus grew to 2,599 methodologies across 22 domains with no written rule for which domain a
document belongs to. The cost of that showed up as **97 slugs existing in two domains at once**
(CR-009), 47 of them straddling `backend/` and `dev/` alone. This document states the boundary,
and states it in a form a validator can check.

It is derived from what the corpus already contains, not from a taxonomy imposed on it. Where the
corpus and a tidy principle disagreed, the corpus won.

## 1. The evidence the boundary rests on

Two domains are told apart most reliably not by subject but by **what they produce**:

| Domain | Docs | `produces` profile |
|---|--:|---|
| `dev` | 378 | spec 103, code 90, report 44, config 37, **playbook-step 31, checklist 30, rubric 19** |
| `backend` | 137 | code 49, spec 43, report 21, config 18, **playbook-step 2, checklist 1, rubric 0** |
| `frontend` | 21 | spec 12, code 4, config 2, checklist 1, playbook-step 1, **rubric 0** |
| `infra` | 295 | **config 127**, spec 69, report 30, decision-record 26 |
| `architecture` | 64 | spec 23, **decision-record 22** |

`backend` has written **one checklist and zero rubrics in 137 documents**. `dev` writes judgement
instruments in 21% of its documents. `architecture` writes decision records in 34% of its.

The second piece of evidence: **all 47 `backend/`↔`dev/` collisions name a technology** — a
framework, ORM, queue, test runner or transport. Not one is a practice topic. The two domains do
not overlap on practice at all; they overlap only where both claimed *technology* documents. So
the boundary that needs stating is the one about technology.

## 2. What each domain holds

### `backend/` — the server-side runtime, and the machine under it

Server frameworks and their idioms, ORMs, background workers, caches, message queues, API
transport (REST/GraphQL/WebSocket), databases as operated, and the operation of **one host you SSH
into**: systemd, nginx, firewall, TLS, backups, deploy scripts.

> **Test:** does a rule here constrain something executing while a user waits — or the machine
> hosting it?

### `frontend/` — the browser-side runtime

Rendering and component architecture, styling systems, design tokens, browser APIs, the shipped
UI's accessibility and performance, client bundling.

> **Test:** does a rule here constrain something that executes in the user's browser?

### `dev/` — the practice of building, plus language-level craft

QA, testing strategy, code review, tech debt, refactoring, delivery discipline, AI-pairing, team
process, rubrics, checklists, templates, decision frames; runtime-agnostic architecture patterns
(DDD, CQRS, event sourcing, microservices, clean architecture); and language and tooling craft not
bound to a server or a browser — typing, ownership, error idioms, package managers, linters, the
shell, git.

> **Test:** would this rule still bind on a project that never deploys? If yes, `dev`.

### `infra/` — a platform you configure rather than code into

Cloud identity, Kubernetes, Terraform, CI runners, managed secret stores, multi-host networking.

> **Test:** is the artefact configuration for a *platform*, rather than code or config for one
> service on one host?

### `architecture/` — the shape decided before code exists

ADRs, C4, system boundaries, quality attributes, build-vs-buy, pattern selection.

> **Test:** is the deliverable a decision about the shape of the system rather than an
> implementation of it?

## 3. The ordering rule

Runtime beats practice beats platform beats decision. Read top to bottom, **first match wins**:

1. Does the document name a **server framework, ORM, queue, or transport**? → `backend`. *Even
   when the subject is testing it, laying it out, or versioning it.*
2. Does it name a **browser framework, styling system, or browser API**? → `frontend`.
3. Does it configure a **platform** rather than a service? → `infra`.
4. Does it **decide a shape** rather than implement one? → `architecture`.
5. Otherwise → `dev`.

**Rule 5 — family tie-break.** When two domains both pass, the document goes where the rest of its
technology family already lives; count sibling directories sharing its dominant tag. This stops
the boundary from shredding coherent families (`go-layout-*`, `django-pytest-*`, `rust-testing-*`).

**Rule 6 — stance is not a reason for two documents.** "How you write it" and "how it runs" are
two sections of one document, not two documents. This is stated explicitly because it is the rule
the corpus broke most often: 6 of the 28 unresolved pairs are one subject split by stance, and
3 more split by stance *in the opposite direction*, which is what proves it was never a policy.

A stance hypothesis was tested against all 28 pairs before this was written, and discarded as the
primary boundary: it explains 6, reverses on 3, and leaves 18 that are simply the same document
written twice. It survives only as the tie-break above.

## 4. Invariants a validator can check

| # | Check | State at ratification |
|---|---|--:|
| V1 | **A slug exists in at most one domain** | 97 violations |
| V2 | Tags naming a server framework ⇒ `domain: backend`; browser framework ⇒ `frontend` | ~44 violations |
| V3 | `produces: rubric` forbidden in `backend` and `frontend` | already satisfied |
| V4 | `produces: checklist` + `playbook-step` in `backend` ≤ 5% of domain | already satisfied (3/137) |

V1 is the one CR-009 closes. **V2 is deliberately not enforced yet** — see §5.

## 5. The cost asymmetry, which is the whole design constraint

**Choosing between two copies that already exist is free.** Links resolve by slug, so the survivor
keeps the slug, zero of the 1,266 ambiguous links dangle, and no `doc_id` changes.

**Moving a document is not.** A rename is a new path, and `doc_id = sha256(path + "\n" + body)[:16]`
— so it invalidates any pinned `cv`, and it splits a slug that 1,266 links cannot distinguish, so
every inbound link must be re-decided by hand.

That asymmetry is why this policy resolves the 28 collisions by **choice** even where the choice
keeps the currently-weaker copy, and why the ~44 documents it declares misfiled are *named* and
*left where they are*. Enforcing V2 corpus-wide means ~24 renames out of `backend/` and ~20 out of
`dev/` into `frontend/`. That is a post-publication project, tracked as debt, not a cleanup.

**`frontend/` is the visible consequence.** It holds 21 documents against `dev`'s 378 because it
was authored as a design-system corner rather than as the browser runtime. Under this boundary it
roughly doubles to ~41. It stays at 21 until the rename budget exists.

## 6. Applying it does not mean deleting

Every collision is resolved **merge-then-archive**: fold the loser's unique rules into the survivor
first, *then* archive the loser to `.archive/knowledge/`. Archiving before merging loses real
material — in 18 of the 28 pairs both sides carry named, subject-specific rules.

## 7. What this does not settle

- **What the resolver actually does** with an ambiguous slug today. Every number here is a fact
  about the corpus, not about `faion-cli`. This policy shrinks the ambiguous population; it does
  not make the remainder safe.
- **Three calls that deserve the owner's eye**, recorded in CR-009 §4: `csharp-aspnet-core` (both
  copies are stubs, so the survivor must be rewritten rather than merged into), `ruby-rails` (the
  rule genuinely folds two useful documents into one), and `java-spring-boot-patterns` (the cheap
  answer keeps a slug that no longer describes its contents; the clean answer is a rename).
- **`secrets-management`**, where both documents are correct and must both live: `backend/` is
  `.env` + systemd + 1Password on a solo VPS, `infra/` is IRSA / Workload Identity / OIDC / ESO.
  Only the shared slug is wrong. This is the one rename the policy requires, and it is deferred
  with the rest.
