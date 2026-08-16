# Read-Only Investigation by Default

## Summary

**One-sentence:** During incidents the AI agent operates in read-only mode by default; write actions require explicit per-action approval token; trust-escalation script tracks the trust ratchet.

**One-paragraph:** During production incidents, the worst AI mistake is a confident write action — a rollback to the wrong commit, a misapplied feature flag, a 'helpful' restart that destroys debug state. This methodology pins agents to read-only RBAC by default (Read, Grep, Glob, log/dashboard access, runbook fetch) and requires an explicit per-action signed approval token (`gov-approval-token-signed-jwt`) before any write. A trust-escalation script tracks the ratchet — once an agent earns write rights for a specific action class, the audit log captures the precedent.

**Ефективно для:**

- AI agent (Claude Code, custom SRE bot) participates in incident response.
- Production systems can be materially harmed by misapplied write actions (rollbacks, flags, infra mutations).
- Platform supports per-action RBAC (Kubernetes RBAC, AWS IAM, etc.) and signed approval tokens.

## Applies If (ALL must hold)

- AI agent (Claude Code, custom SRE bot) participates in incident response.
- Production systems can be materially harmed by misapplied write actions (rollbacks, flags, infra mutations).
- Platform supports per-action RBAC (Kubernetes RBAC, AWS IAM, etc.) and signed approval tokens.

## Skip If (ANY kills it)

- Agent is a chat-only assistant with no execution surface — no writes possible.
- Team has no incident-response automation at all — install the basics first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Agent RBAC config | yaml | Repo at `incident/agent-rbac.yaml` |
| Approval token verifier | config | From `gov-approval-token-signed-jwt` |
| Action class catalog | yaml | Repo at `incident/action-classes.yaml` |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-inc-read-only-investigation-default` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-rbac.yaml` | Agent RBAC manifest |
| `templates/escalate_trust.py` | Trust ratchet manager |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-inc-read-only-investigation-default.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[ci-eval-gate-config]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/agent-rbac.yaml`

```yaml
agent_id: sre-agent-prod-01
default_policy: deny
read_allowlist:
  - logs:search
  - dashboards:read
  - code:search
  - runbooks:read
  - pagerduty:read
  - alerts:read
write_allowlist:
  - rollback:payments-service
  - flag-toggle:checkout-feature
token_verifier: https://approvals.internal/verify
revert_after_incident: true
```

### `templates/escalate_trust.py`

```python
"""Record agent write authorisations to trust ratchet."""
from __future__ import annotations
import json
import sys
from pathlib import Path


def record(action_class: str, agent_id: str, approver: str, evidence_url: str, log_path: Path) -> None:
    entry = {"action_class": action_class, "agent_id": agent_id, "approver": approver, "evidence_url": evidence_url, "ts": "auto"}
    existing = []
    if log_path.exists():
        existing = json.loads(log_path.read_text())
    existing.append(entry)
    log_path.write_text(json.dumps(existing, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 6:
        sys.stderr.write("usage: escalate_trust.py <action_class> <agent_id> <approver> <evidence_url> <log_path>\n")
        sys.exit(2)
    record(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], Path(sys.argv[5]))
```
