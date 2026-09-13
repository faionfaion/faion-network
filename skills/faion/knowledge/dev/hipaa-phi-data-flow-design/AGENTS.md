# Hipaa Phi Data Flow Design

## Summary

**One-sentence:** Designs a HIPAA-compliant PHI data flow: minimum-necessary, BAA boundary, §164.312(b) audit controls.

**One-paragraph:** Designs a HIPAA-compliant PHI data flow: minimum-necessary, BAA boundary, §164.312(b) audit controls. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness without re-deriving the rationale.

**Ефективно для:**

- Pro-tier dev workflow, де потрібен auditable artefact замість ad-hoc decision.
- Команди, де ≥2 stakeholders читають один артефакт і повинні дійти однакового висновку.
- Cases where input must be cited (no fabrication) і decision-trail зберігається для review.
- Recurring trigger, що з'являється ≥1 раз на cycle і виправдовує methodology overhead.

## Applies If (ALL must hold)

- The system creates, receives, stores or transmits PHI for a HIPAA covered entity or business associate, and the data carries at least one of the 18 identifier classes in 45 CFR §164.514(b)(2).
- The infrastructure inventory (cloud accounts, SaaS integrations, backup and export jobs) can be enumerated, so every hop can be drawn.
- Vendor contracts are accessible, so a BAA can be linked or its absence established per external hop.
- The organisation has a designated Security Officer or Privacy Officer who will sign the design (45 CFR §164.308(a)(2), §164.530(a)).
- The logging layer and identity provider can be configured (scrubber, roles, automatic logoff).

## Skip If (ANY kills it)

- The data is de-identified under §164.514(b) (Safe Harbor or Expert Determination) before it enters the system; record the method and proceed without this design.
- The organisation is neither a covered entity nor a business associate under 45 CFR §160.103; another privacy regime applies.
- The infrastructure inventory cannot be enumerated; a diagram with unknown hops is a defect, not a design.
- Vendor contracts are unreachable, so no BAA can be verified; the external hops cannot be assessed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Infrastructure inventory: every service, database, queue, cache, index, log pipeline, error tracker, analytics tool, backup, export and third-party API | cloud account export + SaaS integration list | platform / SRE |
| Request routing table (every request path the synthetic-record test must cover) | route list from the framework | application repository |
| Field-level data dictionary of the PHI the system handles, mapped to the 18 identifier classes | table | data owner |
| Executed BAAs with vendor, plan and covered service | signed PDFs | legal / procurement |
| KMS configuration, TLS policy per link, log platform retention settings | infrastructure config | platform / SRE |
| Identity provider roles and group membership for every principal touching PHI | IdP export | security |
| Retention requirements per data class and the backup, replica, cache and export topology | policy + topology diagram | compliance / platform |
| Named Security Officer or Privacy Officer | name + contact | compliance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/dev/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: every hop inventoried, minimum necessary per hop, BAA per external hop, encryption in transit and at rest, audit event per access, no PHI in logs or URLs, unique identity and roles, retention and deletion per store | 2250 |
| `content/02-output-contract.xml` | essential | Draft-07 schema: hops with the 18 identifier classes, justified fields, de-identification for analytics / ML / LLM hops, BAA with plan and covered service per external hop, KMS encryption at rest per storing hop, TLS 1.2+ per link with termination point, PHI-free append-only audit log kept 6+ years, allow-list scrubber with synthetic-record test in CI, unique identities with roles, logoff and break-glass, retention and deletion propagation, Security Officer sign-off; valid + invalid examples, forbidden patterns | ~6500 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns with detector + repair | 950 |
| `content/04-procedure.xml` | essential | 9 steps: inventory every hop, minimum necessary and de-identification, BAA per external hop, encrypt links and stores, audit event and store, scrub logs and prove it, identities and roles, retention and deletion propagation, route to the Security Officer | ~1950 |
| `content/05-examples.xml` | recommended | Complete five-hop design for a clinician portal (API, RDS, snapshots, Sentry under BAA, de-identified embeddings API), a note per non-obvious value, and a bad design with the validator output | ~3850 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/output.md.j2` | Spec skeleton matching the schema in 02-output-contract.xml |
| `templates/output.md` | Spec skeleton matching the schema in 02-output-contract.xml Generated from `templates/output.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in canonical example for calibration |
| `templates/_smoke-test.md` | Filled-in canonical example for calibration Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-hipaa-phi-data-flow-design.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[pci-dss-scope-minimisation]]
- [[compliance-control-matrix-soc2-gdpr]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
