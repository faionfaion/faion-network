---
type: change-request
cr_id: CR-011
title: "69 methodologies contain no rule about their own subject, and the gate cannot tell"
priority: P0
created: 2026-08-15
status: proposed
affected_components: [faion-network/skills/faion/knowledge, scripts/validate-methodology-v2.py]
blocks: "publication — a pro-tier document whose rules are shared verbatim with sixteen unrelated documents delivers nothing"
---

# Change Request: rules that say nothing about their subject

The rules are the product. Everything else in a methodology exists to support them. This CR is
about the share of them that are not about anything.

## 0. The gate is vacuous, and that is why none of this was caught

`validate-methodology-v2.py` enforces exactly one thing about rules: **at least one
`<rule testable="true">` must exist somewhere under `content/`.**

**All 16,147 rules in the corpus declare `testable="true"`. Zero exceptions.** The attribute is a
constant, so the check is satisfied by any document containing one rule of any quality. Rule ids,
source authenticity, rationale content and cross-document duplication are not validated at all.

This is the fifth check found this week that reports success without testing anything — after the
pre-commit path gate (a `pipefail` race), `validate-recipes.py` (treats a failed publish as
"skipped" and still prints `4/4 pass`), the lexicon attestation check (`ua-en.tsv` sits inside the
tree it scans, so every term self-attests from its own row), and `content_id` (declared as a content
hash, matching 0 of 2,520). **The pattern is now the finding: this corpus's gates are green in
proportion to how little they check.**

## 1. The two defects that void a document

### 69 methodologies contain not one rule about their own subject

Every rule classified as literal stub / universal skip-gate / cross-document filler (a statement
repeated verbatim ≥10× corpus-wide) / subject-bearing. Corpus-wide the split is healthy — 84.8%
subject-bearing. But **69 documents land at zero**: 42 `pro`, 23 `geek`, 3 `solo`, 1 `free`. A
further 235 are ≥40% filler-or-stub.

- `marketing/google-analytics` (**pro**) — six rules, **not one mentions GA4**.
- `dev/hipaa-phi-data-flow-design` (**pro**) — four rules about template field sets and semver,
  **nothing about PHI**.
- `pm/rag-policy-thresholds` (**pro**) — a document named for thresholds that **states none**.

### 83 methodologies share a byte-identical rule set with another methodology

18 clusters. The two largest are **19 documents × 5 identical rules** and **17 documents × 4**.
Corpus-wide, **15.4% of all rule statements are byte-identical to a rule elsewhere.**

**The sourcing is the part that will not survive a customer noticing it.** The citations are real
books, pasted across unrelated subjects: *"Form-discipline research (Cooper, About Face, 2014)"*
appears in **25 documents across 6 domains** — on a HIPAA data-flow document and on a freelancer
payment-chase script. *"Operational hygiene (PMBOK 7 Tailoring)"* in 22. A grep for generation
markers will never find these: the rules parse clean and the sources are genuine works.

**This is the case a customer detects in ten seconds** by opening two paid documents side by side.

## 2. What is shipped to the free tier

**129 rules are literal placeholders** reading *"Stub rule for conclusion 'X' … Replace with the
real testable rule"*, all carrying `source="phase-d-autofix"` and the rationale *"Auto-added by
fix-methodology-phase-d.py to keep tree refs resolvable"* — a script that satisfied the decision
tree's reference check by inventing rules for it to point at.

They sit in 57 documents. **21 are `free` tier — 18.3% of the entire 115-document free tier** —
including the flagship `dev/code-review`, `dev/documentation`, `dev/code-coverage`,
`dev/django-pytest` and `dev/python-typing`. The shop window instructs the reader to replace the
content with real content.

## 3. Sourcing, measured

| Measure | Result | Basis |
|---|--:|---|
| Rules whose `source` is a marker, empty, self-referential or a bare abstract noun | **4,146 (25.7%)** | exhaustive |
| Documents where **every** rule has one | **288** | exhaustive |
| `source="v1-source"` | 669 rules / 111 docs | exhaustive |
| `"F-066 wave-NN chunk-NN grounding"` | 379 rules / 103 docs | exhaustive |
| `"faion-network methodology DoD (F-066)"` | 414 | exhaustive |
| Rationale **byte-identical to its own rule statement** | **345 rules / 69 docs** | exhaustive |
| Source judged fake on reading | **54.2%** | sampled, 684 rules / 105 docs |

## 4. What is NOT the problem

**Testability.** A lexical proxy flags 30.9% of rules as lacking an observable condition; reading
684 of them says **1.8%**. The proxy over-flags prose that is checkable without a number. *Do not
quote the 30.9%* — it measures a different thing and would send a fix at the wrong target.

**Rule counts.** Median 6, mean 6.43. Only 10 documents have fewer than 4 and 11 have more than 15.

## 5. A cost of CR-009, measured

**Merged documents are ~6× more likely to contradict themselves**: 5 contradictions in 82 CR-009
survivors against 1 in 105 randomly sampled documents. Six are named, including
`dev/python-type-hints` (a queue message must be a `TypedDict` by one rule and a Pydantic
`BaseModel` by another, while a third forbids defining both) and `backend/csharp-entity-framework`
(data annotations "forbidden", then `[Timestamp]` required on every aggregate root).

Merge survivors also run median 10 rules against the corpus's 6, with 61% at ≥10 rules against 4.2%
corpus-wide — a 14.5× enrichment. **Merging preserved content and did not edit it down**, which was
the instruction, and this is its bill.

## 6. Options

1. **Fix the 69 zero-subject documents and the 31 worst stub-carriers, then stop.** ~100 documents.
   The other defects *degrade* a document; these two *void* it. A bare `r1` id is ugly but the rule
   under it still says something true; a `v1-source` citation is unverifiable but the rule is still
   checkable — 98.2% of rules are.
2. **Mechanical sweep first.** The 305 bare-ordinal-id documents and 4,146 marker sources are
   greppable. Cheap, and it fixes the *appearance* while leaving the 69 empty documents empty.
3. **Retire rather than rewrite.** For the 83 clone-set members, ask whether the subject deserves a
   document at all. Several are template-shaped subjects that never had rules.
4. **Do nothing and publish.** Defensible only if no customer opens two paid documents side by side.

## 7. Recommendation

**Option 1, and the free-tier subset first.** The 21 stub-carrying free documents are the shop
window and they literally say *"Replace with the real testable rule."*

**And give the validator something to check.** Two rules would have caught all of this:

- **No two methodologies may share a rule statement set.** Catches the 83 clones, which no existing
  check can see because they were found by comparing statements *across* documents — something no
  script in `scripts/` does.
- **A `source` must not be a generation marker, a self-reference, or the document's own slug.**
  Catches 4,146 rules and 288 fully-unattributed documents.

Neither is expensive. Both fail loudly today, which is the argument for adding them: a gate is worth
having when it is red, and this corpus has spent a long time proving that a gate which is always
green is indistinguishable from no gate at all.
