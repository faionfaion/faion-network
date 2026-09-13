# Multi-Region Failover Pattern Pack

## Summary

**One-sentence:** Produces a multi-region failover pattern pack — active-active vs active-passive vs warm-standby vs pilot-light decision, RPO/RTO bounds, DNS / database / object-store mechanics — paired with a live drill checklist so DR isn't 'we think it works'.

**One-paragraph:** Produces a multi-region failover pattern pack — active-active vs active-passive vs warm-standby vs pilot-light decision, RPO/RTO bounds, DNS / database / object-store mechanics — paired with a live drill checklist so DR isn't 'we think it works'. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** software architects responsible for disaster-recovery posture in multi-region deployments who need a written choice between active-active / active-passive / warm-standby / pilot-light plus a drillable live-failover script.

## Applies If (ALL must hold)

- The workload runs, or must run, in more than one cloud region because of a regulatory requirement, a customer commitment, or an RTO a single-region restore cannot meet.
- A business owner has agreed numeric RPO and RTO for the workload's tier, or will in the first step.
- Replication metrics exist for the database (30-day p99 lag) and the object store (backlog, replication time), so achievable numbers can be measured rather than assumed.
- A live drill on a bounded slice of real traffic can be scheduled, with a named architect owning the pack as `role:handle`.
- The secondary region's capacity and service quotas can be verified or requested before the pattern is claimed.

## Skip If (ANY kills it)

- The workload is single-region by design and a tested backup-and-restore plan meets its RPO/RTO; a multi-region pack is cost without a driver.
- RPO and RTO cannot be obtained as numbers from anyone accountable; the pattern cannot be chosen or costed until they exist.
- The platform is a managed multi-region service whose failover the vendor owns end to end (a global database with automatic promotion and vendor-run drills); record the vendor's published figures instead.
- The workload is stateless with no database or object store of its own and fails over through a global load balancer already drilled by the platform team.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| RPO and RTO per tier | integers in minutes, with the business owner's `role:handle` | business owner / service catalogue |
| Database replication metrics | replication mode and 30-day p99 lag in seconds | database monitoring (RDS, Cloud SQL, self-managed exporter) |
| Object-store replication state | replication rule, versioning, backlog metric, backfill job id | cloud console / Batch Replication job history |
| Dependency inventory | IdP, secrets manager, CI/CD, DNS provider, certificates, payments, email, control plane with region | architecture diagram / infra repo |
| Secondary-region quotas | quota request ids for full production load | cloud service-quota console |
| Last drill report | date, scope, traffic percent, measured RTO/RPO, manual steps | DR drill records |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: numeric RPO/RTO per tier, pattern from RPO/RTO and cost, DNS TTL and health check, DB replication mode and promotion, object-store replication verified, region-scoped dependencies, live drill with measured results, failback procedure | ~2000 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the pack: rpo/rto inputs, one pattern with achievable numbers and secondary capacity, DNS TTL / health check / propagation, database replication mode with p99 lag, fencing and promotion, object-store backfill and backlog alert, dependency list with bypasses, drill checklist and last result, failback; valid and invalid packs; 8 forbidden patterns | ~5650 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | recommended | 9 steps: agree RPO/RTO per tier, collect replication facts, list region-scoped dependencies, choose pattern and capacity, write DNS mechanics, write promotion and fencing, write failback, run the live drill, decide and label verified or unverified | ~1850 |
| `content/05-examples.xml` | recommended | Complete warm-standby pack for a tier-1 payments API (async PostgreSQL at 12 s lag, S3 backfill job, six dependencies with one bypass, 5 percent drill measuring RTO 22) with a note per value, plus the pilot-light 'zero data loss' pack and what the validator prints | ~2550 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Parse inputs + check preconditions | haiku | Mechanical schema parse. |
| Author the artefact body | sonnet | Bounded synthesis from typed inputs. |
| Review for compliance + cross-cutting impact | opus | Cross-input judgement when stakes are high. |
| Outcome-review synthesis at cadence | opus | Did the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Markdown skeleton of the artefact with all required sections. |
| `templates/skeleton.md` | Markdown skeleton of the artefact with all required sections. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum-viable filled JSON instance, parseable by the validator. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-region-failover-pattern-pack.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
