# Agency Rebrand Methodology

## Summary

**One-sentence:** Coordinated agency-rebrand spec covering name change, narrower niche, raised prices, client comms, portfolio migration, SEO continuity, and contract addenda — one versioned plan owned by a named human, not a kicked-off design brief.

**One-paragraph:** Coordinated agency-rebrand spec covering name change, narrower niche, raised prices, client comms, portfolio migration, SEO continuity, and contract addenda — one versioned plan owned by a named human, not a kicked-off design brief. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Founder-name or generic-name agency wants to shift to a niched company brand.
- Existing retainer clients (≥ 3) need active comms — silent rebrand will erode trust.
- Founder has 60-90 days runway to execute without rush-shipping the comms.

## Skip If (ANY kills it)

- Logo refresh only — use a visual-rebrand-light playbook, not this methodology.
- No clients yet — pick a name and ship; rebrand methodology overhead does not pay back.
- M&A-driven rebrand with legal counsel — defer to corporate counsel playbook.

**Ефективно для:**

- Founder-name agency (Ruslan Faion) що хоче перейти на бренд-агенцію (Faion Net).
- Команди з існуючими retainer-клієнтами що треба провести через comms без втрати.
- Рестарт з підвищенням цін на 30-100% і вужчою нішою водночас.
- Аудит SEO-traffic перед rebrand: мінімум втрат при URL migration.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/marketing-manager` | Parent role context — agency operating discipline. |
| `solo/marketing/content-marketer` | Adjacent role context — content + portfolio surface. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from input to filled artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill from header + section list. |
| `populate-decisions` | sonnet | Per-section judgment + tradeoff selection. |
| `review-tradeoffs` | opus | Cross-decision synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton with required sections (overview / decisions / tradeoffs / fitness functions / open questions). |
| `templates/_smoke-test.md` | Minimum viable filled-in instance. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-rebrand-methodology.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[agency-niche-positioning]]
- [[agency-case-study-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
