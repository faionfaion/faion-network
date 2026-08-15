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

| Path | Retired | Why | Record |
|---|---|---|---|
| `playbooks/` | 2026-08-15 | 12 duplicate playbook pairs — the redundant side of each | [CR-007](../.aidocs/improvements/CR-007-playbook-duplicate-pairs.md) |
| `knowledge/` | 2026-08-15 | Cross-domain slug twins whose loser is provable by defect, not judged | [CR-009](../.aidocs/improvements/CR-009-cross-domain-slug-ambiguity.md) |
