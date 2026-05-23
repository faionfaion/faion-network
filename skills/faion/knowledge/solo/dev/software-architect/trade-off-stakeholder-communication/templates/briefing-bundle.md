<!-- purpose: Markdown skeleton for the 4-artefact stakeholder briefing bundle -->
<!-- consumes: validated bundle JSON -->
<!-- produces: human-readable briefing for distribution -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300 tokens when loaded -->

# Briefing — `<decision_id>` `<decision_title>`

**Reversibility:** `<type-1 | type-2>`
**Key risk (verbatim across all four artefacts):**
> `<key_risk>`

## Exec summary (≤120 words)

`<gain> + Key risk: <key_risk>. <re-evaluate trigger>.`

## PM brief

**Roadmap impact:** `<one-line>`
**Dependency changes:**
- `<dep change 1>`
- `<dep change 2>`

`<body — embeds key_risk verbatim>`

## Engineer note

**Chosen option:** `<name>`
**Sacrificed:**
- `<sacrifice 1>`
- `<sacrifice 2>`

`<body — embeds key_risk verbatim>`

## Ops delta

**Runbook changes:**
- `<runbook delta 1>`

**Alert changes:**
- `<alert delta 1>`

`<body — embeds key_risk verbatim>`

## Convergence check

- [ ] key_risk paragraph appears verbatim in all four artefacts
- [ ] exec_summary word_count ≤120
- [ ] engineer_note.sacrificed has ≥1 entry
- [ ] No two artefacts share identical body text
