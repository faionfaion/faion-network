# Agent Integration — Backup Basics

## When to use
- Defining a backup *policy* (RPO, RTO, retention, scope) before any tool selection.
- Educating a team on the 3-2-1 / 3-2-1-1-0 / 4-3-2 rules and choosing one based on threat model.
- Deciding what to back up (production stores, configs, secrets state, SaaS data) and what *not* to back up (derived caches, ephemeral compute).
- Compliance gap analysis: SOC 2 / ISO 27001 / HIPAA / GDPR / PCI evidence for backup controls.
- Pre-incident planning: building the recovery runbook before something breaks.

## When NOT to use
- For implementation details (Restic flags, Velero schedules, pg_dump options) — use `backup-implementation` instead.
- When the team already has a documented policy aligned with regulatory requirement; re-creating policy is bikeshedding.
- For SaaS-only stacks where the policy is "vendor SLA + export weekly to cold storage" — a single page suffices.

## Where it fails / limitations
- Policy without verification gives false assurance; teams hit "backup successful" alerts and never restore-test.
- 3-2-1 framing predates ransomware-as-a-service; modern threat actors target backup planes (Veeam credentials, S3 keys) explicitly. 3-2-1-1-0 (immutable + verified) is the new floor.
- RPO/RTO are SLO-class targets; without measurement they devolve into wishful numbers in a runbook.
- SaaS data (Google Workspace, Microsoft 365, Salesforce) is the most common policy gap — vendor retention is not a backup.
- Compliance frameworks ask for "tested annually"; auditors increasingly require quarterly evidence.

## Agentic workflow
This methodology is mostly *advisory*: the agent's job is to interview stakeholders (or read existing infra inventory), output a backup policy document, and produce a gap report against the chosen rule (3-2-1-1-0). Implementation belongs to `backup-implementation`. Keep agent tasks read-only against the cloud accounts; output is markdown policy + a tag-coverage / vault-coverage gap matrix.

### Recommended subagents
- A `backup-policy-author` subagent (define inline) — given an asset inventory + threat model, emits a policy doc and a per-asset RPO/RTO matrix.
- A `compliance-mapper` subagent — maps backup controls to SOC 2 / ISO 27001 / HIPAA clauses; outputs evidence checklist.
- `password-scrubber` — audit any secrets/credentials referenced in the policy doc.

### Prompt pattern
```
Inputs: asset inventory CSV (system, criticality, data class, regulatory),
threat model (insider, ransomware, region outage, accidental delete).
Output a markdown policy with:
- Per-asset RPO and RTO with justification.
- Backup rule applied (3-2-1, 3-2-1-1-0, 4-3-2) per criticality tier.
- Retention matrix.
- Verification cadence (must include restore-drill frequency).
Do NOT recommend specific tools. Stop at policy.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `aws config` | Inventory + tag compliance for backup-coverage gap reports | https://docs.aws.amazon.com/config/ |
| `gcloud asset` | GCP-wide inventory feed | https://cloud.google.com/asset-inventory |
| `az graph` | Azure Resource Graph queries | https://learn.microsoft.com/en-us/azure/governance/resource-graph/ |
| `cloudcustodian` | Policy-as-code for "must have backup tag" | https://cloudcustodian.io/ |
| `chronicle` / `osquery` | On-host inventory (which hosts have backup agent installed) | https://osquery.io/ |
| `prowler` / `scout-suite` | Audit framework with backup coverage checks | https://github.com/prowler-cloud/prowler |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| AWS Config Conformance Pack: Backup | SaaS | Yes — REST | Pre-built backup-policy compliance checks |
| Azure Policy: Backup | SaaS | Yes — REST | Audit + enforce backup vault assignment |
| GCP Security Command Center | SaaS | Yes — REST | Surface assets without backup |
| Drata / Vanta / Sprinto | SaaS (compliance) | Yes — REST | Auto-evidence for SOC 2 backup controls |
| OneTrust | SaaS | Partial | Heavy GRC suite |
| Notion / Confluence | SaaS | Yes | Where the policy doc lives; agent edits via API |

## Templates & scripts
See `templates.md` for the policy and RPO/RTO matrix. Inline gap-check: assets without an `backup-tier` tag (AWS).

```bash
#!/usr/bin/env bash
set -euo pipefail
aws resourcegroupstaggingapi get-resources \
  --resource-type-filters ec2:instance rds:db dynamodb:table efs:file-system \
  --output json \
| jq -r '.ResourceTagMappingList[]
    | select((.Tags // []) | map(.Key) | index("backup-tier") | not)
    | .ResourceARN' \
| tee /tmp/no-backup-tag.txt
echo "Untagged assets: $(wc -l < /tmp/no-backup-tag.txt)"
```

## Best practices
- Define RPO/RTO per data class, not per system. Then map systems to classes — fewer SLOs to defend.
- Enforce a single mandatory tag (`backup-tier=critical|standard|dev|none`); without `none` you have plausible deniability gaps.
- Include SaaS in the policy explicitly: list Workspace / 365 / Salesforce / GitHub / Jira; assign retention.
- Include *recovery* in the policy, not just backup. RTO without a documented restore runbook is a wish.
- Require a quarterly restore drill for `critical` tier, annual for `standard`. Track drill outcomes as an SLO.
- Pair retention with legal hold process — a 30-day retention conflicts with litigation hold; document the override.
- Cover encryption-key custody: a backup is unrecoverable if the key is lost. KMS keys also need backup / cross-region replication.
- Document who can authorize a restore and who can authorize a destructive prune. Separation of duties.

## AI-agent gotchas
- Agents anchor on the 3-2-1 rule from training data and miss 3-2-1-1-0 / 4-3-2. Force the prompt to enumerate immutability and verification explicitly.
- LLMs invent "industry standard RPO of 1 hour" — there is no such standard. RPO is per-org per-data-class. Reject any unjustified number.
- Compliance citations are a hallucination hotspot ("HIPAA 164.308(a)(7)(ii)(A)" — verify before publishing). Provide the agent with a vetted clause list, not free-text.
- Agents conflate "snapshot" with "backup"; policies that allow same-storage-system snapshots as the only copy are a critical gap.
- Generated runbooks often skip the encryption-key recovery step. Add a checklist item: "key custody documented and tested."
- Tag-coverage outputs are eventually consistent; a one-shot gap report can show 0 gaps when 100s exist if the agent queried right after a deploy. Re-run after 24h.
- "Air-gapped" is not "different cloud account" — agents weaken the term. Specify: separate credentials, separate trust domain, ideally offline media for top tier.

## References
- NIST SP 800-34 Rev. 1 (Contingency Planning) — https://csrc.nist.gov/pubs/sp/800/34/r1/final
- ISO/IEC 27031 (Business continuity for ICT) — https://www.iso.org/standard/44374.html
- 3-2-1-1-0 explained (Veeam) — https://www.veeam.com/blog/321-backup-rule.html
- Backblaze 3-2-1 — https://www.backblaze.com/blog/the-3-2-1-backup-strategy/
- AWS Well-Architected Reliability Pillar — https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/
- SOC 2 backup control mapping — https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2
