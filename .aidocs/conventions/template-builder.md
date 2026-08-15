---
type: convention
title: "Template builder: decomposed blocks, declared parameters, assembled output"
created: 2026-08-15
status: ratified
applies_to: [skills/faion/tools/template-builder, skills/faion/knowledge/*/*/templates]
implements: "faion-net/.aidocs/conventions/retrieval-content-contracts.md §2.2, §2.3"
---

# Template builder

A methodology ships a template. Today the template is a whole file with placeholder text in it, and
a human fills it by hand. This document specifies the machinery that assembles one instead: from
decomposed blocks, with declared parameters, resolved from a project store or asked for, emitting
Markdown and HTML.

## 0. What is already decided, and is not re-decided here

`retrieval-content-contracts.md` **§2.2 and §2.3 already specify the parameter contract** — the
`variables:` key extending the five-line template header, and the `sections:` key with
`when: <var> in [<literal>, …]`. `scripts/validate-methodology-templates.py` already enforces its
shape.

**Adoption is zero.** Two files match a `variables:` grep and both are false positives — a Terraform
`variable "…" {}` block and a Python docstring. No template in the corpus has ever carried a
spec-conformant declaration.

So this is an implementation of a ratified contract, not a new one. Where this document and §2.2
disagree, §2.2 wins.

**Also not re-decided: the language stays tiny.** §2.3 says *"And nothing else. No expressions,
loops, nesting, partials-in-partials or filters"*, and gives the reason — the server assembles
templates **on behalf of other accounts**, so a general template language is a server-side template
injection surface we would be choosing rather than inheriting. The builder implements variable
substitution and `when: var in [...]` and refuses everything else. **Branching a single `in` cannot
express is two blocks, not a richer syntax.**

## 1. Substitution syntax: `{{name}}`

Measured across 7,344 template files:

| Convention | Files | |
|---|--:|---|
| `<AngleBracket>` | 1,670 (22%) | **rejected** |
| `$VAR` | 269 | ambiguous with shell |
| `{BRACE}` | 150 | ambiguous with f-strings, Go templates |
| `{{mustache}}` | 92 | **chosen** |

`<Angle>` is the incumbent and it is rejected on evidence, not taste. It is already the direct cause
of a defect class — **9 Python templates in the corpus do not parse** because a placeholder lands in
identifier position, and 47 more parse only because their placeholders happen to sit inside strings.
For the HTML output this builder must produce it is worse than unusable: `<Entity>` is
indistinguishable from a tag and will be swallowed or escaped.

`{{name}}` is unambiguous in Markdown, HTML, Python, shell, YAML, JSON and Terraform simultaneously,
and it already has a foothold.

**Legacy is not rewritten wholesale.** A template keeps its `<Angle>` text until someone authors a
`variables:` block for it; the builder only substitutes what is declared. Migration is per-template
and opt-in, exactly as §2.2 makes parameterisation opt-in.

## 2. Block decomposition

```
skills/faion/tools/template-builder/blocks/<kind>/<name>.md
   kind ∈ { header, body, footer }
```

Every block is a fragment of a template plus its own `variables:` declaration in the five-key
header. A block declares only the variables it uses.

**What may become a block:** a fragment that appears in more than one assembled template and whose
text is about the *artefact shape*. Measured redundancy across the canonical content parts, after
normalising the slug out:

| Part | Files | Distinct | Redundant | KiB |
|---|--:|--:|--:|--:|
| `01-core-rules` | 2,513 | **2,467** | 46 | 117 |
| `02-output-contract` | 2,512 | 2,217 | 295 | 816 |
| `03-failure-modes` | 2,512 | 2,256 | 256 | 747 |
| `04-procedure` | 2,238 | 1,906 | 332 | 715 |
| `06-decision-tree` | 2,510 | 2,347 | 163 | 246 |

**This table is the whole decomposition thesis: rules are specific, the envelope is generic.**
`01-core-rules` is 98% distinct — 2,467 different files out of 2,513. Every other part carries
hundreds of copies. So the thing to decompose is the envelope around the rules, never the rules.

**A block library is not a licence to unify content.** A block earns its place by being genuinely the
same in every use. A "failure modes" section that is identical across 19 methodologies is not a
reusable block — it is CR-011's evidence that those 19 documents say nothing. Extracting it would
make the emptiness tidy and permanent. When a fragment is identical because nobody wrote the real
one, the fix is to write it.

## 3. Parameter types

Per §2.2, plus one addition this builder needs:

| type | Resolved by |
|---|---|
| `string`, `integer`, `boolean`, `path` | value supplied directly |
| `enum` | value from `options` |
| **`text`** | **an LLM writes it from the user's answer to `description`** |

`text` is the new one and it is why the builder has an ask mode. A `text` parameter is not a value a
user types — it is prose the agent composes after asking the question in `description`. The builder
never generates it; it reports what must be asked and accepts the answer.

## 4. Resolution order

1. Explicit value passed on the command line
2. The project parameter store
3. The declared `default`
4. **Ask** — emit the question and stop

A required parameter with no default and no value is **refused by name**, never substituted empty.
That is §2.2's rule and it is the difference between a template that fails loudly and one that ships
a document with a hole in it.

## 5. The project store

```
<project>/.faion/template-params.json
```

Lives in the user's project, never in the corpus. Keyed by parameter name.

**A `sensitive: true` parameter is never written to it.** §2.2 is explicit: a sensitive value never
travels — the assembler emits the `placeholder` and the value is substituted locally afterwards. The
store records that the parameter *exists* and its placeholder, never the value. Two independent
checks, neither trusting the other: the corpus declares `sensitive`, and the builder additionally
refuses any value matching the secret shapes it already knows, whatever the declaration says.

## 6. Output

- **`.md` is canonical.** It is what the assembler produces and what the store round-trips against.
- **`.html` is rendered from the Markdown**, self-contained: no external stylesheet, no CDN font, no
  remote image. Same constraint the artifact surface imposes, for the same reason — a document that
  needs the network is a document that breaks.

**The renderer is deliberately partial and says so.** The tool-pack contract is stdlib-only, so
there is no Markdown library. The renderer covers exactly the vocabulary the blocks emit — headings,
paragraphs, lists, tables, fenced code, links, emphasis — and nothing else. It is not a CommonMark
implementation and must not be described as one.

## 7. Where it lives, and at which tier

`skills/faion/tools/template-builder/`, tier **free**.

The precedent is manifest v13, which moved the entire composable layer to free with the argument:
*"The pipeline is the mechanism that makes an agent's output correct, and gating the mechanism does
not sell tiers — it makes free-tier output worse. What a tier buys is the content a pipeline
consumes."* The builder is mechanism. The methodologies whose templates it assembles are content,
and they stay gated.

## 8. What this does not do

- **No expressions, loops, filters or nested partials.** §2.3, and the SSTI reason behind it.
- **No content unification.** See §2 — the block library is for genuinely shared shape.
- **No rewrite of the 1,670 `<Angle>` templates.** Opt-in, per template, as declarations are authored.
- **It does not fix CR-010.** A block library adds a delivery path; it does not make the 602 KB of
  unlisted content reachable. Those are separate, and doing this one first does not excuse that one.
