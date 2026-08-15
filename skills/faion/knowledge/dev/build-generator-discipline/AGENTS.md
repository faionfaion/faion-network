# Build-Generator Discipline

## Summary

**One-sentence:** Ten rules for a static-site or codegen build — autoescape on with exactly one audited `|safe`, render everything to memory before writing anything, converter stderr and short bodies fatal, the markup flavour pinned by name, an explicit unpublished list so an unmapped source fails by name, and `--check` kept as a separate mode because the build repairs drift — each rule citing the defect that produced it.

**One-paragraph:** A generator is trusted in a way its output never is: nobody reads twenty regenerated pages. That trust is what makes its failure modes silent. Every rule here was written after a specific shipped defect. A converter failure on page 14 of 20 left thirteen pages rewritten, seven stale and the derived precache list carrying its old hash, so installed clients served the old copies of exactly the pages that had changed — hence render-all-then-write. `$14.1M` opened a TeX formula and swallowed the rest of the sentence across five pages — hence pinning the flavour to something like `gfm-tex_math_dollars` rather than a bare default. An emptied source produced a page with a header, a pager and no content — hence a short-body floor. A comment claimed a test asserted every entry point carried the shared head block; the file had never been written and the blocks matched by coincidence. And the load-bearing structural rule: `--check` is a separate entry point, never a post-build assertion, because the build *repairs* drift, so building and then checking always passes and proves nothing.

**Ефективно для:** static-site generators, documentation builds, template-driven codegen, any pipeline where one command regenerates many files from many sources through an external converter.

## Applies If (ALL must hold)

- A build step turns source files into the artefact that ships.
- More than one output file is produced, or a derived index/manifest is generated.
- Templates, an external converter, or both, sit in the path.
- The generated output is committed or deployed without being read file by file.

## Skip If (ANY kills it)

- No generator — the artefact is authored directly, so there is no drift to repair.
- One output file, no external converter, no derived artefacts — the rules cost more than they buy.
- The generator's output is fully re-reviewed by a human on every run — then the silence these rules break is not silent.
- A framework already owns atomicity, escaping and the flavour, and you are not allowed to change how it does so — port the `--check` split and the unpublished list, drop the rest.

## Prerequisites

| Input artefact | Format | Source |
|---|---|---|
| Site map / source-to-output mapping | code, one place | the generator |
| Explicit unpublished list | list of source paths | the generator, next to the map |
| Converter invocation with a pinned flavour | command line | the generator |
| Deterministic subset of the check | a named CLI mode | the generator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[cdn-fronted-static-deploy]]` | The stamping step this build must perform atomically, and why a half-written tree defeats content-hashed URLs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 rules: one audited `\|safe`, render-all-then-write, stderr and short bodies fatal, pinned flavour, unmapped source fails by name, `--check` separate, check split by determinism, measurements generated not transcribed, explicit encoding and newline, no comment may claim a test exists | ~1400 |
| `content/02-output-contract.xml` | essential | The run contract: three modes and their separation of duties, seven guarantees a build must satisfy, what the run must print, and a shell one-liner showing why `build && build --check` is meaningless | ~900 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns (write-as-you-go, build-then-check, a second `\|safe`, default flavour, silent skip of an unmapped source, transcribed measurements, a comment claiming coverage) + cheap symptoms | ~900 |
| `content/06-decision-tree.xml` | essential | Root: "is there a generator at all?" then one branch per observable gap, ordered so the unrecoverable failure is fixed first | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Convert a write-as-you-go generator to render-all-then-write | sonnet | Mechanical restructuring with a clear end state. |
| Add a `--check` mode and split it by determinism | sonnet | Needs care about which assertions survive the split. |
| Audit templates for escape-hatch creep | haiku | Grep-shaped. |
| Diagnose "the source looks right but the page is wrong" | opus | Flavour and extension interactions are where the non-obvious bugs live. |

## Related

- [[cdn-fronted-static-deploy]] — where the generated URLs go, and why atomicity here decides invalidation there
- [[ai-generated-code-lint-presets]] — the same "make the rule mechanical" posture applied to lint config
- [[coverage-rebuild-playbook]] — rebuilding a derived artefact from ground truth rather than trusting the last run

## Decision tree

See `content/06-decision-tree.xml`. It gates on whether a generator exists at all, then routes each observable gap — writes-as-it-renders, missing or folded-in `--check`, a full check running in CI, escape-hatch creep, ignored stderr, an unpinned flavour, silently skipped sources, literal counts, a comment claiming coverage — to the single rule that closes it. The ordering matters: write-as-you-go is fixed first, because it is the only failure that leaves the tree in a state no later run can diagnose.
