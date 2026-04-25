# Agent Integration — PM Tools Overview

## When to use
- Selecting a PM tool for a new team or replacing an outgrown one (10–500 users typical decision band).
- Consolidating multiple tools across an organization (post-merger, post-acquisition, vendor renewal).
- Producing a defensible RFP / vendor-comparison brief in a regulated procurement.
- Updating an existing decision when growth, compliance, or pricing shift the calculus.
- Pair with `pm-tool-selection/` (deeper selection process), `pm-tools-comparison/` (tool-by-tool deep dives), `tool-migration-basics/`, `tool-migration-process/` (after the choice).

## When NOT to use
- Single-team / solo decision with low switching cost — pick by gut, time-box a 2-week trial, ship.
- "Switch to escape a personality conflict" — change the people/process, not the tool.
- A tool already works with no measurable pain — gold-plating.
- Decisions driven purely by exec preference / vendor relationship — no analysis will change them.
- Pre-product-market-fit startups — tool-selection theatre distracts from product.

## Where it fails / limitations
- The README compares ~10 tools at a feature-list level; real fit comes from workflow + integrations + admin model, not feature parity.
- Pricing tables go stale fast; vendors change tiers, free seats, and AI-add-on bundling quarterly.
- "Best for X" labels are marketing — Linear is sometimes too opinionated, Jira sometimes the right call for small teams.
- Migration cost is the hidden majority of TCO; tool-overview frameworks underweight it.
- Compliance posture (SOC 2, ISO 27001, HIPAA, FedRAMP, GDPR data residency) flips the shortlist; do not skip.
- Agent-friendliness varies (REST coverage, GraphQL maturity, webhook stability, rate limits) — surface it explicitly when AI agents will drive the tool.
- Network effects in your org (existing Slack/Teams, IDP, SCIM) frequently dominate the choice; pure tool merit is rarely decisive.

## Agentic workflow
A `requirements-distiller` interviews stakeholders (or reads transcripts) and emits a MoSCoW table grounded in evidence. A `vendor-shortlister` prunes the universe to 3–5 candidates by hard constraints (price ceiling, deployment, compliance, IDP). A `poc-runner` runs scripted tasks against trial instances of each shortlisted tool (create issue, transition, run query, fire webhook) and records latency/success. A `scoring-agent` builds a weighted scorecard with citations to the evidence. A `decision-writer` produces an ADR-format recommendation. Humans approve scope, evidence collection, and final pick.

### Recommended subagents
- `requirements-distiller` (sonnet) — distill stakeholder transcripts into MoSCoW; cite verbatim quotes.
- `vendor-shortlister` (haiku) — apply hard constraints; return shortlist with rejection reasons.
- `poc-runner` (haiku, calls tool APIs) — drive scripted POC scenarios in trial instances.
- `scoring-agent` (sonnet) — apply weights, compute totals, sensitivity analysis.
- `decision-writer` (opus) — produce ADR with risks, mitigations, migration plan outline.
- `pricing-tracker` (haiku, scheduled) — monitor vendor pricing pages and update the comparison.

### Prompt pattern
```
You are requirements-distiller. Inputs: meeting_transcript.md, prior_tools.md.
Emit a MoSCoW table: { "must": [...], "should": [...], "could": [...],
"wont": [...] }. Each item: { "id": "R-NN", "name": "...", "evidence": [
{"quote": "...", "speaker": "...", "transcript_offset": ...} ], "metric":
"...|null" }. Refuse to invent requirements without an evidence quote.
```

```
You are scoring-agent. Inputs: requirements.json, weights.json, vendor_findings/*.json.
For each vendor, compute weighted score; return top 3 + sensitivity table that
shows ranking under ±20% weight perturbations. Highlight any item where rank
flips under sensitivity.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli`, `glab`, `gh`, `linear` (community), `azdo` | Drive POC scenarios per tool | per project |
| `httpie` / `curl` | Quick REST checks during evaluation | preinstalled |
| `jq` / `yq` | Manipulate JSON/YAML evaluation artifacts | `apt install jq yq` |
| `pandoc` | Render the comparison + ADR to PDF for procurement | https://pandoc.org |
| `mermaid-cli` | Render decision-tree / scoring radar | `npm i -g @mermaid-js/mermaid-cli` |
| `dvc` / `git-lfs` | Version artefacts (transcripts, POC outputs) | https://dvc.org |
| `mkdocs` / `mdbook` | Publish the evaluation as a navigable site | per tool |
| `playwright` | Drive UI-only flows where APIs are missing | `npm i -D @playwright/test` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira | SaaS | REST + JQL | Most customizable; complex; ecosystem. |
| Linear | SaaS | GraphQL | Fast, opinionated, GitHub-first. |
| ClickUp | SaaS | REST | All-in-one; deep customization; some perf. |
| Notion | SaaS | REST | Docs + light PM. |
| GitHub Projects (v2) | SaaS | GraphQL | Free for OSS, integrated with code. |
| GitLab | SaaS/OSS | REST + GraphQL | Full DevOps; self-host option. |
| Azure DevOps | SaaS | REST | Microsoft shops; SAFe templates. |
| Trello | SaaS | REST | Simple kanban; light PM. |
| Asana | SaaS | REST | Marketing/ops slant; goals + portfolios. |
| Monday.com | SaaS | GraphQL | Visual; expensive at scale. |
| Smartsheet | SaaS | REST | Gantt + PPM heritage. |
| Wrike | SaaS | REST | Enterprise PM with proofing/marketing slant. |
| Targetprocess (Apptio) | SaaS | REST | SAFe/portfolio. |
| Hansoft | On-prem/SaaS | REST | Game/aerospace heritage. |
| OpenProject / Redmine / Tuleap / Plane | OSS | REST | Self-hosted alternatives. |

## Templates & scripts
README ships requirements-doc, MoSCoW, and stakeholder-interview templates. Inline below: a script that runs a fixed POC scenario against any REST tool with a thin adapter.

```python
#!/usr/bin/env python3
"""poc_runner.py — minimal scenario harness; vendor adapters in adapters/*.py"""
from __future__ import annotations
import argparse, importlib, json, time, sys

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vendor", required=True)  # e.g., jira, linear, gitlab
    ap.add_argument("--config", required=True)  # JSON path with creds + project
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    adapter = importlib.import_module(f"adapters.{args.vendor}").Adapter(cfg)

    results = {}
    for step in ("create_issue", "transition", "search_jql", "fire_webhook"):
        t0 = time.perf_counter()
        try:
            getattr(adapter, step)()
            results[step] = {"ok": True, "ms": int((time.perf_counter() - t0) * 1000)}
        except Exception as exc:  # noqa: BLE001
            results[step] = {"ok": False, "error": str(exc)}
    json.dump({"vendor": args.vendor, "steps": results}, sys.stdout, indent=2)
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

Adapters: ~30 lines each, one per shortlisted vendor.

## Best practices
- Anchor evaluation to actual workflows, not feature checklists. A 1-hour pilot of a real epic + sprint beats a week of spec-reading.
- MoSCoW with evidence; no Must without a stakeholder quote or measured pain point.
- Two-week time-box for POC; longer == decision-fatigue.
- Score with weights + sensitivity; if the winner flips under reasonable weight changes, the choice is fragile.
- Always include "do nothing" as a baseline option in the ADR.
- Quantify migration cost (data, automations, integrations, training, parallel-run period) — frequently 30–50% of year-1 TCO.
- Procurement: get vendor security questionnaires (SIG Lite, CAIQ) signed; do not assume marketing claims.
- Check IDP/SCIM and SSO before features; failing here forces re-platforming.
- Check egress: full data export, automation export, custom-field export. Lock-in proportional to import-only support.
- Check rate limits and webhook reliability — agent-driven workflows find these limits fast.
- Document the decision (ADR) with date, weights, scoring matrix; re-review annually.

## AI-agent gotchas
- Vendor marketing pages mislead LLMs about feature availability per tier; always confirm against changelogs and trial instance.
- Pricing pages and tier names change quarterly; cache with date stamp, refresh before publication.
- "Recommendations" from generic LLM training are out of date; require an evidence-based scoring against the team's MoSCoW, not a vibe-vote.
- POC results from API-only scenarios miss UI quality issues that drive real adoption; pair with one Playwright UI test per vendor.
- Compliance attestations (SOC 2 etc.) need the report (not the badge); LLMs accept badges naively.
- Migration estimates from LLMs are systematically low; multiply by 2× and add a parallel-run period.
- Auto-pruned shortlists: the LLM will silently drop candidates on weak grounds; require explicit rejection reasons per filtered vendor.
- Region/data residency: LLMs forget tenant region — surface it as a hard constraint in the prompt.
- Do not let an agent submit RFP responses or sign DPAs; humans only.
- Human-in-the-loop checkpoints (mandatory): MoSCoW finalization, shortlist, POC scope, final pick, ADR signoff.

## References
- "The Right Tool for the Job" — Camille Fournier, "The Manager's Path".
- Gartner Magic Quadrant — Collaborative Work Management / PPM (paid).
- G2, Capterra, TrustRadius — peer reviews; treat as directional, not authoritative.
- PMI Library — tool selection frameworks: https://www.pmi.org/learning/library
- ADR template — Michael Nygard's "Documenting Architecture Decisions".
- Sibling methodologies: `pm-tool-selection/`, `pm-tools-comparison/`, `tool-migration-basics/`, `tool-migration-process/`.
