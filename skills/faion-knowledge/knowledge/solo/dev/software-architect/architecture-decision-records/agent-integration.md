# Agent Integration — Architecture Decision Records (ADRs)

## When to use
- Capturing any architecturally significant decision: tech selection, style change, cross-cutting pattern, third-party service, breaking API change.
- Kicking off a new repo — bootstrap `docs/adr/` with ADR-0001 (the architecture you're starting from) so future agents have a baseline.
- During design phase: agent drafts MADR options analysis from a spec, human picks an option, agent finalizes.
- Migration / refactor planning: each phase becomes a superseding ADR linked to the original.
- Compliance/audit prep (SOC2, ISO 27001, FDA): ADRs are the cheapest way to satisfy "show your decision rationale" controls.
- Onboarding: new contributors read ADL (Architecture Decision Log) instead of pestering tenured engineers.

## When NOT to use
- Trivial decisions (file naming, single-developer code style) — methodology explicitly says skip.
- Reversible / cheap-to-change choices (variable names, internal helpers).
- Throwaway PoCs or hackathon code where decisions don't outlive the demo.
- Ultra-confidential decisions (M&A, vendor pricing) that cannot live in a Git repo without redaction.

## Where it fails / limitations
- **Write-once-rot-forever:** ADRs accepted and never revisited become stale; status fields (Deprecated, Superseded) demand discipline that solo teams skip.
- **Bikeshedding magnet:** PR review on an ADR can stall for weeks while the decision needs to ship — process eats the value.
- **Format drift:** team starts on Nygard, switches to MADR mid-stream, ends with five formats coexisting.
- **Missing alternatives:** authors list "Option A, do nothing" and "Option B, the thing we already decided." Genuine option exploration is rare without a critic agent.
- **Decision laundering:** ADR is written *after* the code shipped to retroactively justify it; loses its forecasting value.
- **Too short (Y-statements) lose context, too long (Tyree & Akerman) never get read.** MADR is the practical sweet spot but still gets ignored if > 2 pages.
- **No backlinks:** ADRs reference code, but code rarely references ADRs — readers find one side or the other, not both.

## Agentic workflow
Run a four-pass pipeline: (1) **trigger detector** scans PRs/specs/SDD docs for words like "we will use", "switch to", "replace X with Y" and proposes an ADR draft (status: Draft); (2) **alternatives generator** produces 3–5 options with pros/cons and rough TCO; (3) **critic / red-team agent** challenges the chosen option ("what if Y becomes EOL?", "what's the migration cost when wrong?"); (4) **human owner** accepts/rejects via PR; (5) **link-back agent** edits the touched files to add `# See ADR-0042` comments. Persist as `docs/adr/NNNN-slug.md`. Re-run pass (1) on each merged PR; re-run a **superseder agent** quarterly that flags ADRs whose context is invalidated by recent commits.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — turns each accepted ADR into SDD `todo/` tasks for any follow-up implementation work.
- `faion-research-agent` (`skills/faion-knowledge/knowledge/pro/research/researcher/`) — sources external benchmarks, vendor comparisons, and market data for the alternatives section; cites links agents can't fabricate.
- A **MADR generator agent** (purpose-built, worth creating): single job is to take a problem statement plus optional context files and emit a fully-formatted MADR-4 markdown.
- A **link-back agent** (purpose-built): scans accepted ADRs and inserts `# ADR: NNNN` comments where relevant (controllers, infra modules, schema migrations).
- A **superseder agent** (purpose-built, scheduled monthly): cross-references ADRs vs current `package.json` / `go.mod` / `Dockerfile` / Terraform; flags drift.

### Prompt pattern
Drafting:
```
You are an architect drafting a MADR-4 ADR. Decision needed: <one
sentence>. Context: <paste from spec / README / discussion>.
Constraints: <team size, stack, budget>.
Produce 3–5 considered options. For each: 1-paragraph description,
pros, cons, and rough TCO bucket (low/medium/high). Recommend one,
explain why. Do not fabricate vendor data; if uncertain, write
"NEEDS VERIFICATION".
```

Critic / red-team:
```
You are a hostile reviewer of ADR <path>. Identify (a) any alternative
not seriously considered, (b) any 12-month risk not listed in
consequences, (c) any reversibility cost the author understates.
Output as bullet list; max 8 items. Do NOT propose a different decision.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `adr-tools` | Bash CLI: create, list, link, supersede ADRs | `brew install adr-tools` / https://github.com/npryce/adr-tools |
| `pyadr` | Python ADR lifecycle (Nygard + MADR) | `pip install pyadr` |
| `log4brains` | CLI + static-site generator with hot reload, MADR default | `npm i -g log4brains` |
| `adr-viewer` | Static-site generator for an existing `docs/adr/` | `pip install adr-viewer` |
| `adr-log` | Generate Markdown TOC of all ADRs | `npm i -g adr-log` |
| `gh` CLI | Open PRs for ADR review; agents can attach to issue threads | https://cli.github.com |
| `mermaid-cli` | Render relationships between ADRs as a graph | `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Convert ADRs to PDF for board / audits | `apt install pandoc` |
| `claude` (Anthropic CLI) | Run drafting + critic passes headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Pages + log4brains | Static site | yes | Best practical "ADR portal" — agents push, log4brains rebuilds. |
| GitLab Pages + adr-viewer | Static site | yes | Same pattern, GitLab-native. |
| Notion ADR database | SaaS docs | API yes | OK for non-engineers; risk: drifts from repo, breaks Git-as-source-of-truth. |
| Confluence ADR template | SaaS docs | API yes | Common at enterprises; slow, hard to lint, but stakeholders read it. |
| Backstage TechDocs (Spotify) | OSS dev portal | yes | Catalogs ADRs alongside service ownership; agent-callable via API. |
| Structurizr | SaaS / OSS | yes | Pairs ADRs with C4 diagrams in one model — see `c4-model/`. |
| Architectural Decision Records by AWS | docs | n/a | Reference content + opinionated templates. |
| Y-Statement annotations (`@YStatementJustification`) | OSS Java lib | yes | Inline ADR snippets in source — agent can scan/aggregate. |
| ArchiMate / Sparx EA | SaaS / paid | partial | Heavy enterprise tools; ADR is a side feature. |
| Joel Parker Henderson's ADR repo | docs | n/a | Largest public collection of real-world ADRs — reference for agent few-shot examples. |

## Templates & scripts

`templates.md` ships 10 formats (Nygard, MADR, Y-statement, etc.). The gap is automation: there's no script to lint ADRs for required sections + status hygiene. Inline drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# adr-lint.sh — validate ADR markdown files against MADR/Nygard requirements.
# Exit non-zero if any ADR is missing required sections or has illegal status edits.
# Usage: adr-lint.sh docs/adr
set -euo pipefail
dir=${1:?"usage: adr-lint.sh <adr-dir>"}
fail=0
required=(Status Context Decision Consequences)
allowed_status="^(Draft|Proposed|Accepted|Rejected|Deprecated|Superseded)( by ADR-[0-9]{4})?$"
for f in "$dir"/[0-9]*.md; do
  for sec in "${required[@]}"; do
    grep -q "^## $sec" "$f" || { echo "MISS  $f: ## $sec"; fail=1; }
  done
  status=$(awk '/^## Status/{getline; print; exit}' "$f")
  if ! [[ "$status" =~ $allowed_status ]]; then
    echo "BAD   $f: Status='$status'"; fail=1
  fi
  # Superseded ADRs must link successor.
  if [[ "$status" == Superseded* ]] && ! grep -q "Supersedes" "$f"; then
    echo "WARN  $f: Superseded but no 'Supersedes' link to original"; fail=1
  fi
done
[[ $fail -eq 0 ]] && echo "OK $(ls $dir/[0-9]*.md | wc -l) ADRs"
exit $fail
```
Wire into pre-commit + CI; the critic agent reads its output to know which ADRs are malformed.

## Best practices
- Bootstrap every new repo with ADR-0001 ("we are starting with monolith / Postgres / FastAPI"); makes future ADRs make sense.
- Treat ADRs as PRs: branch, draft, request review, merge — never edit accepted ADRs.
- Cap MADR at ~2 pages; require an "Alternatives" section with at least 2 real options.
- Use Y-statements as inline annotations (`# Y-stmt: in context of …`) for sub-decisions that don't deserve a full ADR.
- Schedule a quarterly ADL review where the superseder agent's drift report is the agenda.
- Always link ADR ↔ code: ADR header has `Affects:` paths; code touched by ADR has `# ADR-NNNN` comment.
- For multi-repo orgs, keep ADRs in a single docs repo and reference by URL in dependent repos.

## AI-agent gotchas
- LLM-drafted ADRs love to invent "industry standards" and benchmark numbers. Pin a rule that all numeric/vendor claims must include a source URL or `NEEDS VERIFICATION`.
- Same agent should not draft and accept; require a separate critic pass before any merge.
- Status field is the most-edited field and the most-broken; lint it in CI (`adr-lint.sh`) — don't trust agents to maintain immutability.
- Long context-rich decisions blow context windows. Feed the agent only the spec excerpt + currently-affected ADRs, not the whole ADL.
- Agents tend to recommend the trendy choice (microservices, Rust, Kubernetes) by default — counter by including team-size and budget constraints in every prompt.
- Human-in-loop checkpoints: (1) before status moves Proposed → Accepted, (2) any Supersedes change, (3) any cross-team ADR (auth, billing, tenancy) — these decisions outlive the team that took them.

## References
- Michael Nygard — Documenting Architecture Decisions (2011) — https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- MADR (Markdown Any Decision Records) — https://adr.github.io/madr/
- ADR GitHub Org — https://adr.github.io/
- Joel Parker Henderson's ADR collection — https://github.com/joelparkerhenderson/architecture-decision-record
- Spotify Engineering — When to Write an ADR — https://engineering.spotify.com/2020/04/when-should-i-write-an-architecture-decision-record
- AWS Prescriptive Guidance — ADRs — https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/
- Google Cloud — ADR Overview — https://cloud.google.com/architecture/architecture-decision-records
- Microsoft Azure — Architect Role + ADR — https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
- log4brains — https://github.com/thomvaill/log4brains
- adr-tools — https://github.com/npryce/adr-tools
- Local methodology: `architecture-decision-records/README.md`, `templates.md`, `examples.md`, `llm-prompts.md`
