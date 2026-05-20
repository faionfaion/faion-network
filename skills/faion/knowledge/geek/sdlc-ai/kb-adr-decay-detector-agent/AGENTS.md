---
slug: adr-decay-detector-agent
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "3ef6d1f703c0b814"
summary: AI agent that diffs Architecture Decision Records against code reality on a schedule and surfaces contradictions for human review.
tags: [adr, ai-agent, architecture, sdlc-ai, governance, claude-code]
---
# ADR Decay Detector Agent

## Summary

**One-sentence:** AI agent that diffs Architecture Decision Records against code reality on a schedule and surfaces contradictions for human review.

**One-paragraph:** ADRs decay silently — a decision "we use Postgres exclusively" becomes "we use Postgres + MongoDB + Redis as a primary store" with no ADR update. The agent ingests `docs/adr/*.md`, extracts each ADR's "Decision" + "Consequences" as testable propositions (e.g., "package_manager == pnpm", "no_redis_in_critical_path"), and runs a scheduled scan against the repo (file globs, dependency manifests, IaC) to detect violations. Output: a markdown report with violated ADRs + evidence snippets, posted as a PR comment or a tracker issue. The agent NEVER auto-edits ADRs — humans decide whether to update the code or supersede the ADR.

## Applies If (ALL must hold)

- repo has ≥ 5 ADRs in MADR or Nygard format under a documented path (e.g., `docs/adr/`)
- ADRs are written with explicit "Decision" + "Consequences" sections
- repo has CI infrastructure that can run a scheduled job (GitHub Actions, GitLab CI, etc.)
- a human (architect, tech lead) owns ADR governance and triages agent output
- AI coding agent or LLM API is available (Claude Code, Codex, or direct Anthropic/OpenAI SDK)

## Skip If (ANY kills it)

- &lt; 5 ADRs — drift unlikely to be measurable; manual quarterly review sufficient
- ADRs in narrative form without testable propositions (Decision: "use modern tech") — detector cannot extract assertions
- repo monorepo size &gt; 1M LOC without symbol index — agent would scan forever; install RAG first
- decision-velocity higher than detection cadence (daily decisions, weekly scans) — agent will always be stale
- no CI / no scheduled jobs — agent has nowhere to run

## Prerequisites (must be true before starting)

- ADR location and format documented (path + frontmatter schema)
- decision proposition extraction prompt (LLM extracts testable claims from each ADR)
- repo scan targets defined (which globs / manifests / files relate to each proposition)
- LLM API credentials + cost budget (~$0.50-2 per scan for &lt; 100 ADRs)
- output destination: PR comment, Slack channel, tracker, or commit-summary doc
- human triage queue: who reads agent output, how often

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/architecture-decision-records` | Source format the agent reads |
| `pro/dev/software-architect/adr-staleness-audit` | Manual / quarterly counterpart; agent informs it |
| `geek/sdlc-ai/kb-codebase-rag-symbol-chunked` | Provides the symbol index the agent queries against |
| `geek/sdlc-ai/kb-agents-md-context-pyramid` | Pattern for how agent loads minimal context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: extract testable propositions, NEVER auto-edit ADRs, scoped scan targets, human triage required, idempotent runs | ~950 |
| `content/02-output-contract.xml` | essential | Decay report schema, PR comment schema, forbidden patterns | ~750 |
| `content/03-failure-modes.xml` | essential | 7 failure modes (false positive flood, hallucinated violations, narrative ADR misparse, scope creep, silent-fail run, comment spam, missing rationale) | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_propositions_per_adr` | sonnet | Bounded extraction with structured output |
| `scan_repo_against_proposition` | haiku | Many cheap glob + regex checks per scan |
| `synthesize_violation_evidence` | sonnet | Compose evidence snippet + rationale per violation |
| `prioritize_violations_for_pr_comment` | opus | Cross-violation reasoning: which 5 to surface this run |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-proposition-extract.json` | Schema: per-ADR list of testable propositions + scan targets |
| `templates/decay-report.md` | Markdown report posted to PR / tracker |
| `templates/github-action.yml` | GitHub Actions workflow that runs the agent on schedule |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/run-decay-scan.py` | Orchestrator: load ADRs, extract propositions, scan repo, write report | On schedule (weekly) |
| `scripts/validate-decay-report.py` | Verify report has no hallucinated file paths or commit refs | Before posting comment |

## Related

- parent skill: `geek/sdlc-ai/`
- peer methodologies: `adr-staleness-audit`, `adr-reversibility-tagging`, `architecture-decision-records`
- external: [Michael Nygard - Documenting Architecture Decisions (2011)](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) · [MADR format](https://adr.github.io/madr/) · [ThoughtWorks Tech Radar ADRs](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
