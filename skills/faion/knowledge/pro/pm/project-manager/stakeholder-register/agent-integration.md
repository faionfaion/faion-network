# Agent Integration — Stakeholder Register

## When to use
- Project initiation: before charter sign-off, identify who funds, approves, uses, blocks.
- Bid/proposal phase: capture buyer, economic buyer, technical buyer, end users (Challenger Sale model).
- Cross-functional rollout (e.g. pricing change, ToS update): map regulators, support, sales, legal.
- Agency engagements: register both client-side and agency-side stakeholders to prevent gaps.
- Re-baselining after a reorg or M&A — old register is stale; rebuild within first week.

## When NOT to use
- Fully internal personal-tool project where you and your manager are the only stakeholders.
- Pure agile team building for itself with one PO and no external dependencies.
- Pre-discovery exploration where stakeholders are not yet defined; do problem framing first.

## Where it fails / limitations
- Captures snapshot, not dynamics — attitudes shift; pair with Stakeholder Engagement (advanced).
- Overlooks indirect/silent stakeholders (legal, security, data privacy, accessibility, end users).
- Power-Interest grid hides time dynamics: someone Low-Low at kickoff can become High-High at launch.
- Privacy/PII concern when emails, phone numbers, salaries are stored — apply access control (e.g. NDA, role-gated repo paths).
- "Influence" rating is subjective; two PMs produce different grids. Use evidence (org chart, RACI, budget authority) not gut feel.

## Agentic workflow
A subagent can mine the project charter, kickoff transcripts, org chart, and Slack/email metadata to produce a draft register, then prompt the human for missing fields (interests, attitude). Treat the register as data: store as YAML/CSV in repo, generate the Markdown view from it. Human-in-loop required for attitude classification — agents systematically over-rate "Supportive" because written communication is polite. Refresh schedule: weekly at minimum during execution; daily during launch week.

### Recommended subagents
- `faion-pm-agent` — initial draft from charter + org data.
- `faion-business-analyst` — cross-checks register against requirement sources (every elicited requirement traces to a stakeholder).
- `faion-improver` — periodic audit: which stakeholders haven't been engaged in N weeks?

### Prompt pattern
```
Input: charter.md, kickoff_transcript.md, org_chart.csv
Output: stakeholders.yaml with id, name, role, dept, interests[], influence{H,M,L},
impact{H,M,L}, attitude{supportive,neutral,resistant,unknown},
power_interest_quadrant, contact, notes.
Rules: never invent attitude; mark unknown when no evidence in inputs.
```

```
Audit register against last 30 days of <comms_log>:
flag stakeholders with zero touches that are quadrant=Manage-Closely.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `yq` | Query/update YAML stakeholder data | https://github.com/mikefarah/yq |
| `jq` | Process JSON exports from Salesforce/HubSpot | https://stedolan.github.io/jq |
| `gh api` | Pull GitHub org members for tech stakeholder identification | https://cli.github.com/manual/gh_api |
| `pandoc` | Render YAML → DOCX register for sponsor | https://pandoc.org |
| `csvkit` | Pivot register CSV by quadrant | https://csvkit.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Salesforce | SaaS | Yes — REST + Bulk API | Source of truth for external stakeholders (accounts, contacts, opportunity roles) |
| HubSpot CRM | SaaS | Yes — REST API + Operations Hub | Free tier covers smaller projects |
| Notion | SaaS | Yes — official API + relations | Native database, link to engagement notes |
| Airtable | SaaS | Yes — REST API + automations | Easy power-interest visualisation via grouping |
| Smartsheet | SaaS | Yes — REST API + cell-link triggers | Common in enterprise PMOs |
| Stakeholder Circle | SaaS | Limited — no public API | Specialist tool; manual data entry |
| Confluence + Jira | SaaS | Yes — REST API | Pages for register + Jira components for engagement tasks |
| 1Password | SaaS | Yes — `op` CLI | Store sensitive contact credentials separately from register |

## Templates & scripts
See `templates.md` for the register table and individual profile. Inline schema (≤50 lines) for an agent-maintained register:

```yaml
# stakeholders.yaml — single source of truth
- id: S-01
  name: Olena Kravchenko
  role: VP Engineering
  dept: Engineering
  interests:
    - delivery cadence
    - tech-debt reduction
  influence: H        # H | M | L
  impact: H
  attitude: supportive  # supportive | neutral | resistant | unknown
  quadrant: manage-closely  # auto-computed from influence × interest
  comms:
    cadence: weekly
    channel: 1:1 + Slack DM
  notes: Sponsor for Q2 platform initiative.
  last_touch: 2026-04-22
- id: S-02
  name: Security Council
  role: Group
  dept: Security
  interests: [compliance, audit-trail]
  influence: H
  impact: M
  attitude: resistant
  quadrant: keep-satisfied
  comms:
    cadence: bi-weekly
    channel: review meeting
  last_touch: 2026-04-15
```

## Best practices
- Identify groups, not individuals only — "Security Council", "Beta Customers" — when a single person is not authoritative.
- Capture interests in concrete language: not "wants project to succeed" but "wants <50ms p95 latency at launch".
- Verify attitude in conversation, not from inference — written tone is a poor signal.
- Refresh after each stage gate; archive the previous version (audit trail of how perception changed).
- Use the register as input to RACI, Communications Plan, and Risk Register (resistant high-influence stakeholder = risk).
- Privacy: keep PII in a separate access-controlled file; the register in repo holds only ID and role.

## AI-agent gotchas
- Agents extract names from email signatures and assume seniority from job title; many bottlenecks are mid-level gatekeepers (procurement, security review). Prompt explicitly for "who can stop this project for 2+ weeks".
- LLMs over-classify as "Supportive" because polite English looks supportive; require attitude evidence quote.
- Group stakeholders ("Customer Success") get split into individuals if you ask the LLM to "list people"; preserve the group when authority is collective.
- Stale registers go undetected: build a `last_touch` field and an automated weekly diff vs comms logs.
- Do not let agents publish full register externally — it's an internal artefact; redact attitude fields when sharing with stakeholders themselves.

## References
- PMBOK Guide 7th Edition — Stakeholder Performance Domain.
- ISO 21500/21502 — Stakeholder management guidance.
- Mendelow A. "Stakeholder Mapping" (Power-Interest Grid, 1991).
- "Managing Project Stakeholders" — Lynda Bourne (Stakeholder Circle methodology).
