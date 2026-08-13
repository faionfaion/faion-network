# Tool-Tier Approval Gate

## Summary

**One-sentence:** Tools the agent can use are tiered (T0 read / T1 mutable-self / T2 customer-impact / T3 multi-cluster); higher tiers require additional approval gates.

**One-paragraph:** Treating every agent tool with the same RBAC blunts safety on dangerous tools and friction on safe ones. This methodology tiers tools by blast radius (T0 read-only, T1 mutable-self-only, T2 customer-impact, T3 multi-cluster / cross-tenant) and gates each tier with progressively stricter approval: T0 free, T1 audit log only, T2 signed token, T3 two-person rule + cooling period. Output is the tool catalog YAML + per-tier gate config consumed by the agent runtime.

**Ефективно для:**

- Agent has access to ≥5 distinct tools (Bash, kubectl, Terraform, secrets-manager, deploy, etc.).
- Blast radius varies substantially across tools (read-grep vs cluster-wide rolling restart).
- Approval infrastructure exists (signed tokens, two-person rule) or can be installed.

## Applies If (ALL must hold)

- Agent has access to ≥5 distinct tools (Bash, kubectl, Terraform, secrets-manager, deploy, etc.).
- Blast radius varies substantially across tools (read-grep vs cluster-wide rolling restart).
- Approval infrastructure exists (signed tokens, two-person rule) or can be installed.

## Skip If (ANY kills it)

- Agent has only 1-2 tools — tiering overhead exceeds benefit.
- Existing flat RBAC works because all tools are read-only.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tool catalog | yaml | Repo at `agents/tools.yaml` |
| Approval verifier | config | From `gov-approval-token-signed-jwt` |
| Two-person rule mechanism | config | Team policy + audit |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-inc-tool-tier-approval-gate` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tools.yaml` | Tool tier catalog |
| `templates/gate-runtime.py` | Reference tier gate evaluator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-inc-tool-tier-approval-gate.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tools.yaml`

```yaml
default_tier: T3
gates:
  T0: audit
  T1: audit
  T2: signed-token
  T3: two-person-cooling
tools:
  - name: grep
    tier: T0
  - name: kubectl-logs
    tier: T0
  - name: dashboard-fetch
    tier: T0
  - name: agent-self-restart
    tier: T1
  - name: rollback-service
    tier: T2
    action_class: rollback:payments-service
  - name: cluster-drain
    tier: T3
    action_class: drain:prod-cluster
```

### `templates/gate-runtime.py`

```python
"""Tier-gate evaluator."""
from __future__ import annotations


def evaluate(tool: dict, ctx: dict) -> tuple[bool, str]:
    tier = tool.get("tier", "T3")
    if tier in ("T0", "T1"):
        return True, "audit-only"
    if tier == "T2":
        if not ctx.get("signed_token_valid"):
            return False, "T2 requires signed token"
        return True, "token-ok"
    if tier == "T3":
        if not ctx.get("two_person_approved"):
            return False, "T3 requires two-person rule"
        if ctx.get("cooling_seconds_remaining", 0) > 0:
            return False, f"T3 cooling {ctx['cooling_seconds_remaining']}s remaining"
        return True, "two-person-cooling-ok"
    return False, f"unknown tier {tier}"
```
