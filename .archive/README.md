# .archive/

Corpus content retired from `skills/` but kept on disk.

**Why it is here and not deleted.** git history already preserves anything removed, but a deleted
directory is only findable by someone who knows it existed. Retired content stays browsable, so a
later question — *did we ever write this? what did it say?* — is answered by looking rather than by
archaeology.

**Why it is outside `skills/`.** Everything that reads the corpus is rooted at `skills/`:
`vfs-pack` walks it to publish, `regen-tier-manifest.py` walks it for `meta.json`, and every
validator resolves paths beneath it. A directory here is therefore invisible to all of them by
construction rather than by an exclusion rule someone has to remember to maintain — which is what
makes this safe to grow.

**What is here does not resolve.** An archived slug is not gated, not indexed, not packed and not
retrievable. It is a record, not a tier.

## Layout

```
.archive/<kind>/<original path under skills/faion/>/
```

so a retired playbook keeps its goal category and slug, and the path it came from is readable from
the path it sits at.

## Contents

| Path | Retired | Count | Why | Record |
|---|---|--:|---|---|
| `playbooks/` | 2026-08-15 | 12 | Duplicate playbook pairs — the redundant side of each | [CR-007](../.aidocs/improvements/CR-007-playbook-duplicate-pairs.md) |
| `knowledge/` | 2026-08-15 | 81 | Cross-domain slug twins: the redundant side of each, **after its unique content was merged into the survivor** | [CR-009](../.aidocs/improvements/CR-009-cross-domain-slug-ambiguity.md) · [domain-boundaries](../.aidocs/conventions/domain-boundaries.md) |

## Reading an archived methodology

**Nothing here was retired because it was worthless.** Under CR-009 the rule was
merge-*then*-archive: every rule, example, failure mode, template and script that the archived copy
held and its survivor lacked was folded into the survivor first. Four separate "this copy has
nothing unique" claims were tested by reading and **all four were false**, which is why the
ordering exists.

So a directory here is a *superseded* copy, not a rejected one. Two things are still worth coming
back for:

- **Material that had no canonical home.** Vendor and SaaS catalogues, reference lists, and
  orientation prose do not fit `01-core-rules` … `06-decision-tree`, so they were deliberately left
  here rather than forced into a part that does not fit. `.archive/knowledge/dev/csharp-dotnet/` and
  `.archive/knowledge/dev/csharp-dotnet-patterns/` are the clearest examples.
- **The original wording.** Where a merge folded a document into a delimited section of its
  survivor — `ruby-rails`, `php-laravel`, `java-spring-boot-patterns` — the archived copy is the
  only place the subject still reads as its own document.

Which slug survived each pair, and why, is recorded per pair in `CHANGELOG.md` under the CR-009
entries.
