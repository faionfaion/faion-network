# Rule: Tool Authoring

**Applies when:** adding, renaming or editing anything under `skills/faion/tools/` — a pack, a
script, a card or a `meta.json`.

**Mandatory before any edit or new file:**

1. `Read` [`docs/tool-authoring.md`](../docs/tool-authoring.md) — the linear checklist, the
   failure modes, and the `.sh` / network deltas.
2. `Read` [`skills/faion/tools/INDEX.xml`](../skills/faion/tools/INDEX.xml) — the tool may already
   exist. Writing a second one is the failure this layer was built to prevent.
3. Start from `docs/templates/tool-script.py.template`, `tool-card.md.template` and
   `tool-pack-meta.json.template`. They validate clean as stamped; anything hand-rolled starts red.

Do not skip step 1. `scripts/validate-tools.py` has **zero** entries in
`scripts/validator-baseline.txt`, so it is a clean gate: any finding you introduce blocks the
commit for everyone, not just you.
