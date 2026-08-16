---
type: change-request
id: CR-013
title: "Two placeholder classes the converter gets wrong, and both fail silently"
created: 2026-08-16
status: open
affected_components: [faion-network/skills/faion/knowledge, faion-network/skills/faion/tools/template-builder]
relates_to: ".aidocs/conventions/template-jinja-migration.md §1b, §5; .aidocs/improvements/variable-dictionary-findings.md §1"
---

# CR-013 — invisible placeholders and collapsed variables

The Jinja migration converted 2,875 of 2,878 declared templates. Two defect classes survived it,
found by verification rather than by the tool. **Both fail silently, which is what makes them worth
a CR rather than a backlog line.**

The migration exists to guarantee one thing: **a parameter is either declared or refused, never
silently passed through.** Each of these breaks that guarantee in a different direction.

## 1. Mixed-case brace placeholders are invisible — 177 templates, 1,663 tokens

The scanner recognises four placeholder forms: `<angle>`, `[bracket]`, **ALL-CAPS** `{BRACE}`, and
escaped `&lt;angle&gt;`. A mixed-case `{Word}` matches none of them, so it is not flagged `unclear`
— it is **not seen at all**.

Measured across the migrated corpus:

| | count |
|---|--:|
| templates carrying unrecognised `{Word}` tokens | **177** |
| tokens | **1,663** |
| …in prose and tables | **1,621** |
| …inside fenced code blocks | 35 |

The most common are unmistakably placeholders, not code: `{artefact_id}` ×51, `{name}` ×41,
`{YYYY-MM-DD}` ×34, `{Title}` ×25, `{owner}` ×25, `{one-line decision the artefact records}` ×20.
Worst-hit is `sdd` — `template-spec/spec.md` alone carries 58.

**The consequence is a false clean.** `product-analytics/tracking-plan.md` and
`backlog-management-product-ops/backlog-item.md` reported `variables=0`, exited 0, and passed every
gate — drift-free, validator-clean — while carrying placeholders nobody can fill. A rendered
document ships `{Product}` literally to a paying user.

The narrow all-caps rule looks deliberate: `template-builder.md` §1 measured `{BRACE}` at 150 files
and rejected it as *"ambiguous with f-strings, Go templates"*. That reasoning holds **inside code**
and nowhere else, and the 1,621-vs-35 split is the evidence. **Decision: recognise mixed-case
`{word}` as a placeholder outside fenced blocks and inline code spans.**

## 2. A repeated placeholder collapses into one variable — 197 templates, 305 variables

Where the same placeholder text appears several times meaning different things each time, the
converter declares **one** variable and binds every site to it. Filling it once fills them all
identically.

`hr/employee-value-proposition/evp-competitive-analysis.md` is the clearest specimen:

```
## Competitor A: {{ name }}
## Competitor B: {{ name }}
## Competitor C: {{ name }}
```

Three competitors, one variable. The same file also turned the literal words "same format as above"
into `{{ same_format }}` twice — prose promoted to a parameter, which §5 explicitly warns against.

Measured: **305 variables across 197 templates** are bound to 2+ sites under 2+ different headings.
`value` ×11 in a config spec and `yes_no` ×12 under six headings are unambiguously distinct slots;
`owner_full_name` ×10 under ten headings in a QBR deck is plausibly one person.

**This is `variable-dictionary-findings.md` §1 showing up as damage instead of as a refusal.** That
section established that a repeating row structure cannot be a variable while §2.3 has no loops. The
correct behaviour is therefore to leave such a placeholder **literal**; declaring one variable for
all its sites is the one outcome worse than either.

The existing collision guard does not catch it because it fires on the same *name* proposed from
*different* text. Here the text is identical, so there is no collision to detect.

**Decision: refuse to declare a placeholder that would bind more than one substitution site, unless
every site sits under the same heading.** This deliberately refuses some legitimate repeats —
`owner_full_name` in a QBR deck will land in the review queue — and that is the correct trade, on the
same asymmetry the resolver's precision bar uses: **a false negative costs one line in a queue a
human is already reading; a false positive ships a document with the wrong value in it and nothing
downstream can detect that.**

## Repair path — and the trap in it

Both repairs need affected templates re-converted. **`--migrate` must NOT be re-run on an
already-converted template.** The regenerated `.md` carries no `variables:` block — it moved into the
schema — so a second pass has no declarations to honour, re-proposes from scratch, and demotes
backticked tokens to examples. Re-running it across the corpus rewrote **78 templates backwards** on
2026-08-16, turning hand-declared `{{ audit_log_path }}` into literal `<audit_log_path>`.

`--check` being drift-free does **not** license re-migration: it proves the generator is
self-consistent against its current source, and says nothing about feeding a generated output back
in as source.

So the repair restores each affected template from its **pre-migration** source with
`git show <commit>:<path>` and converts that, once, with the corrected scanner.

## Out of scope

The 38 `_smoke-test*.md` files remain undeclared on purpose: they are filled worked examples, not
templates a user fills. Declaring them would offer a "template" that is actually a sample. Their
delivery is a content-taxonomy question, not a migration one.
