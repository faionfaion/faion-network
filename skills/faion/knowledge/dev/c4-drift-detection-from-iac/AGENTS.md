# C4 Drift Detection From IaC

## Summary

**One-sentence:** Produces a drift report comparing the canonical C4 diagram against the live Terraform/Pulumi/CloudFormation state — new components, removed components, edge changes — so the living architecture diagram stays trustable.

**One-paragraph:** Produces a drift report comparing the canonical C4 diagram against the live Terraform/Pulumi/CloudFormation state — new components, removed components, edge changes — so the living architecture diagram stays trustable. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** software architects keeping a living C4 diagram who need a scheduled, evidence-backed drift report rather than slack-screenshot updates whenever someone happens to remember.

## Applies If (ALL must hold)

- A machine-readable C4 model exists or can be transcribed once: Structurizr DSL or JSON, LikeC4, or a version-controlled YAML / JSON model with stable element ids.
- The same system's infrastructure is managed by Terraform, Pulumi or CloudFormation, and the applied state (terraform show -json, pulumi stack export, DescribeStackResources) is readable by the comparison.
- The IaC pipeline has a post-apply hook and a scheduler, so the comparison can run after every apply and at least weekly.
- Someone is on rotation to close findings by model commit, IaC change or a time-boxed accepted entry.
- The comparison is at container or system-context level; nobody expects component-level findings from state.

## Skip If (ANY kills it)

- The infrastructure is hand-managed with no applied IaC state; build an inventory source first, there is nothing live to compare against.
- The only architecture diagram is a picture and nobody will transcribe it into a model with element ids; without ids there is no diff, only impressions.
- The system is a single deployable with no infrastructure of its own (a static site on a shared platform) and its C4 container view has one element.
- A platform team already runs a C4-versus-state drift report over this system's state and model; subscribe to it rather than running a second comparison.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Machine-readable C4 model | Structurizr DSL / JSON, LikeC4, or model YAML / JSON with stable ids, at a commit | architecture repo (docs/c4/) |
| Applied IaC state output | terraform show -json, pulumi stack export, or DescribeStackResources output with its identity | IaC pipeline after apply |
| Resource-to-element mapping table | version-controlled YAML: resource type to C4 level, kind and id attribute | architecture repo |
| Noise allowlist | version-controlled YAML of plumbing types that never map | architecture repo |
| Post-apply hook and schedule | pipeline step after apply plus a weekly or more frequent job | CI / scheduler |
| Previous report | last report JSON with finding ids and reports_open | .product/c4-drift-detection-from-iac/ |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: machine-readable model, applied state not source, versioned mapping table, three drift classes with ids, level stated, noise allowlist, run on apply and schedule, close by commit or expiry | ~2050 |
| `content/02-output-contract.xml` | essential | Draft-07 schema for the report: machine-readable c4_model at a commit, iac_state with an applied-state source and per-tool identity (serial and lineage, export version, stack id), comparison_level container or system-context, versioned mapping_table and allowlist with suppressed counts and no hardcoded skips, post-apply run at least weekly, findings in three classes with both ids and a closure by commit, expiring acceptance or open, unmapped residue, reconciliation, escalations; valid and invalid examples | ~4250 |
| `content/03-failure-modes.xml` | essential | 6 subject-specific antipatterns with detector + repair | ~1050 |
| `content/04-procedure.xml` | recommended | 8 steps: machine-readable model, applied state and identity, mapping table and allowlist, post-apply and schedule, three-class difference, reconcile residue, close or escalate, validate and publish | ~1750 |
| `content/05-examples.xml` | recommended | Complete post-apply report at Terraform serial 412 with notes on every non-obvious value, plus the first script's report breaking six rules and what the validator and architect say | ~2100 |
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
| `scripts/validate-c4-drift-detection-from-iac.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
