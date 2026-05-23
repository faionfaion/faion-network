# PMBoK 8 Six Core Principles

## Summary

**One-sentence:** Six canonical principles (Holistic View, Value, Quality, Accountability, Sustainability, Empowered Teams) audited as binary pass/fail with positive evidence quotes; any fail blocks the stage gate.

**One-paragraph:** PMBoK 8 consolidates PMBoK 7's twelve principles into six: Adopt Holistic View, Focus on Value, Embed Quality, Lead Accountably, Integrate Sustainability, Build Empowered Teams. Every PM artefact or decision is audited against these six as binary pass/fail. 'Passed: true' requires positive evidence quoting the artefact; absence of failure is not a pass. Any failing principle stops the stage gate. Sustainability requires a numeric proxy (CO2 estimate, accessibility WCAG level, social-impact metric) — not a paragraph about values.

**Ефективно для:**

- Drafting / reviewing a project charter, decision log, or change request
- Auditing an existing plan for principle gaps
- Anchoring any PM-domain LLM call with a six-question self-check
- Migrating a PMBoK 7 twelve-principle plan to PMBoK 8 six-principle structure

## Applies If (ALL must hold)

- Drafting or reviewing a project charter, decision log, or change request
- Auditing an existing plan for principle gaps (no sustainability, no value statement)
- Anchoring any PM-domain LLM call with a six-question self-check at the end
- Migrating a PMBoK 7 twelve-principle plan to PMBoK 8 six-principle structure

## Skip If (ANY kills it)

- Tactical execution work (sprint planning, ticket triage) — principles too abstract
- Non-PMI environments (PRINCE2, IPMA, SAFe) — vocabulary clashes
- Audit / compliance requiring named standard (ISO 21500, 21502) — principles are guidance
- Technical deep-dives (architecture, security) — principles do not substitute for expertise

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Artefact under review | Markdown | PM |
| Edition pin | string | PMBoK 8 in system prompt |
| Sustainability proxy | metric | CO2 / accessibility / social-impact baseline |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ref-pmbok]] | Edition vocabulary |
| [[seven-performance-domains]] | Domains audited alongside principles |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: positive-evidence-required, fail-blocks-gate, canonical-six-names, sustainability-numeric-proxy, pin-pmbok-edition | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-artefact` | sonnet | Per-principle evidence extraction with quoted source |
| `escalate-fails` | sonnet | Fix-or-escalate sentence per failing principle |

## Templates

| File | Purpose |
|------|---------|
| `templates/principle-audit.md` | Six-row audit table: principle / evidence / pass-fail / fix |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-six-core-principles.py` | Validate audit has exactly 6 rows in canonical order with evidence quotes per pass | Pre-commit; pre-gate |

## Related

- parent skill: `pro/pm/project-manager/`
- [[ref-pmbok]]
- [[seven-performance-domains]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
