# Deprecated API Sweeper Recipe

## Summary

**One-sentence:** Produces a sweep report listing deprecated k8s APIs found in chart libraries + live clusters with cited tool + replacement API per finding.

**One-paragraph:** Detecting deprecated k8s APIs in chart libraries and live clusters is a chore with known tooling (pluto for charts, kubent for clusters) — worth a single packaged methodology. Mechanism: typed input (cluster name + chart path set), bounded transformation (run both tools, normalize output, deduplicate), contract-checked output (findings list with source + tool + replacement API per row). The report drives the upgrade task list for the Kubernetes major-version upgrade.

**Ефективно для:**

- Kubernetes major-version upgrade (3 тижні) — потрібен deprecated-API sweep перед cutover.
- коли pluto / kubent існують, але немає packaged methodology їх послідовно прогнати.
- chart libraries + live clusters: одночасний sweep по обох поверхнях.
- tier=pro команд з >=3 Helm chart releases та активним workflow upgrade.

## Applies If (ALL must hold)

- Cluster + chart-set targeted is the same one slated for Kubernetes major-version upgrade.
- pluto and kubent (or equivalents) can be run against the chart path and the live cluster respectively.
- A named owner is accountable for the upgrade task list the report feeds.
- Replacement API for each deprecated call is known or researchable in the upstream Kubernetes deprecation notes.

## Skip If (ANY kills it)

- Cluster is on a Kubernetes version with no scheduled upgrade in the next 6 months.
- Chart libraries are externally maintained and the team has no upgrade authority.
- Sweep already ran within the last 30 days — re-run only if charts changed.
- Cluster is a one-off ephemeral dev environment — sweep cost exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cluster name + kube context | string | platform team |
| Chart path set | list of paths | repo |
| Tools (pluto + kubent) installed | binaries | local / CI |
| Replacement-API table | Markdown | Kubernetes deprecation notes |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent role skill |
| `pro/sdd/sdd` | SDD discipline for the artefact lifecycle |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes r4-bound-scope) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/05-examples.xml` | medium | One full worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `run-pluto-sweep` | haiku | Mechanical tool invocation against chart path |
| `run-kubent-sweep` | haiku | Mechanical tool invocation against live cluster |
| `synthesize-report` | sonnet | Merge + dedupe + cite replacement API per finding |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Deprecated-API sweep report skeleton |
| `templates/skeleton.md` | Deprecated-API sweep report skeleton Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/skeleton.json` | JSON schema for the sweep report |
| `templates/sweep-config.yaml` | Pluto/kubent configuration template |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-deprecated-api-sweeper-recipe.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[argocd-gitops]]
- [[helm-basics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the Deprecated API Sweeper Recipe methodology when in doubt about scope or fit.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/skeleton.json`

```json
{
  "artefact_id": "<slug-or-uuid>",
  "owner": "<single-named-handle>",
  "inputs_used": [],
  "decision": "<the-answer>",
  "rationale": "<>=2 sentences referencing at least one input by name>",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23"
}
```

### `templates/sweep-config.yaml`

```yaml
# Deprecated API Sweeper Recipe — sweep-config.yaml
# Replace placeholder values per instance.

artefact_id: "<slug-or-uuid>"
owner: "<single-named-handle>"
inputs_used: []
decision: "<the-answer>"
rationale: "<>=2 sentences referencing at least one input by name>"
version: "1.0.0"
last_reviewed: "2026-05-23"
```
