# Agent Integration — Requirements Documentation

## When to use
- Producing the canonical `spec.md` for an SDD feature: business requirements (BR), stakeholder requirements, functional requirements (FR), non-functional requirements (NFR), and acceptance criteria — all in one machine-readable document.
- Migrating loose Notion / Confluence / Google Doc requirement notes into a Markdown + YAML-frontmatter `requirements/REQ-XXX.md` repository that diff/grep/Git can manage.
- Generating a Business Requirements Document (BRD) for stakeholder sign-off when an SDD spec is too dense for non-technical readers — a parallel artefact, not a replacement.
- Translating user-story backlogs (Jira, Linear, GitHub Issues) into the standard `REQ-XXX` format for regulated review (audits, SOC2, ISO).
- Pairing with `requirements-traceability/`, `requirements-lifecycle/`, and `requirements-validation/` to close the Document → Trace → Validate loop.
- Pre-development: enforcing structure before code. Acceptance criteria in Given/When/Then form become Playwright/pytest scaffolds via codegen.

## When NOT to use
- Solo founder pre-PMF: a BRD is theatre when the spec changes weekly. Use opportunity-solution-trees plus living user stories.
- Pure ops tasks (cron edits, nginx vhost tweaks, infra rotations) — runbooks, not requirement docs.
- Discovery spikes whose deliverable is a learning, not a baseline — use research notes and a stop condition.
- When stakeholders refuse written sign-off — without an Approved gate, the document degrades to a status spreadsheet.
- One-off scripts where the cost of writing REQ-XXX exceeds the cost of just rewriting the script.

## Where it fails / limitations
- **Implementation leak.** Agents producing FRs from elicitation transcripts repeatedly emit "the system shall use Postgres" — a how, not a what. README mistake #3 holds for LLMs in spades; lint for forbidden tokens (`Postgres`, `React`, `Redis`, `S3`, `Lambda`).
- **Vagueness camouflaged as confidence.** "System shall be fast" passes a generic LLM review because the model defaults to amiable. Force a measurable-or-reject gate (numeric threshold + unit + measurement method).
- **NFR amnesia.** LLMs over-index on functional requirements and silently drop NFRs (security, usability, accessibility, observability). Always run an NFR-coverage pass with an explicit category checklist.
- **ID collisions.** Parallel agents writing into the same `requirements/` directory race on `REQ-XXX` numbering. Use a lock file or pre-allocate ranges per agent.
- **AC explosion.** Generating 12 Gherkin scenarios per FR makes the spec unmanageable. Cap at 3-5 scenarios per FR; defer edge cases to test-plan.
- **Stale acceptance criteria.** Once code ships, AC drift from production behaviour. Tie a pre-commit hook to `spec.md` so any FR edit re-flags downstream tests.
- **One-doc-fits-all fallacy.** A 200-page BRD nobody reads. Split: BRD for sponsors (5-10 pages), `spec.md` for builders, story cards for sprints. Same source, three views.

## Agentic workflow

Treat the requirements set as a directory of small Markdown files (`spec/REQ-XXX.md` or `requirements/REQ-XXX.md`) with YAML frontmatter for `id`, `type` (BR / SR / FR / NFR), `priority`, `source`, `state`, `traces_to`. A documentation pipeline runs in four stages: (1) a draft agent (Sonnet) consumes elicitation notes / interview transcripts and emits one REQ-XXX file per atomic requirement; (2) a lint agent applies the SMART + INVEST + measurability rules and rejects vague tokens; (3) a coverage agent (Opus) checks that every business objective has at least one BR, every BR has at least one FR, every FR has at least one AC, every AC is testable; (4) a render agent assembles the BRD / `spec.md` / sprint-story views from the same source via Jinja or pandoc. `faion-feature-executor` should refuse to advance a feature into `in-progress/` until stages 1-3 pass.

### Recommended subagents
- `faion-sdd-executor-agent` — owns the per-feature `spec.md` lifecycle: drafts requirements as SDD tasks, produces commits per requirement batch, blocks `done/` if AC are missing.
- `faion-feature-executor` — wires the documentation pipeline as a quality gate between `backlog/ → todo/`. Initial draft → lint → coverage must pass before estimation.
- `faion-brainstorm` — diverge to surface NFR categories the draft missed (security, accessibility, locale, observability, performance, compliance); converge to keep only those that actually apply to the project.
- `password-scrubber-agent` — pre-commit pass over `requirements/` to catch credentials pasted from stakeholder transcripts before the spec hits a public repo.
- `faion-improver` — periodic audit: scans `done/` features for AC that drifted from production behaviour, flags re-documentation candidates.
- A custom `ba-doc-drafter` (sonnet) — turns transcript snippets into REQ-XXX skeletons with rationale, source, and AC stubs.
- A custom `ba-doc-linter` (haiku) — cheap rule-based pass: SMART regex, forbidden implementation tokens, ID uniqueness, frontmatter completeness.

### Prompt pattern

Draft (Stage 1, structured output):
```xml
<role>BA drafter. Convert one elicitation snippet into one atomic requirement.</role>
<inputs>
  <snippet>{transcript_chunk}</snippet>
  <feature_id>{feature_slug}</feature_id>
  <next_id>{REQ-NNN}</next_id>
</inputs>
<rules>
  Emit YAML frontmatter + Markdown body matching templates.md.
  type ∈ {BR, SR, FR, NFR}. priority ∈ {Must, Should, Could, Wont}.
  Body MUST contain: Description, Rationale, Source, Acceptance Criteria (Given/When/Then).
  No implementation tokens (Postgres|Redis|React|S3|Lambda|specific framework names).
  No subjective adjectives (fast|easy|user-friendly|intuitive) without numeric threshold.
  Output ONE requirement only. No prose outside the file body.
</rules>
```

Lint (Stage 2):
```xml
<task>Score requirement {req_id} against SMART + measurability + non-implementation.</task>
<output>JSON: {req_id, smart:{S,M,A,R,T:pass|fail}, measurability:pass|fail,
  forbidden_tokens:[], subjective_terms:[], severity:high|med|low,
  fix_suggestions:[<=3 items]}</output>
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `markdownlint-cli2` | Lint REQ-XXX Markdown structure (heading levels, link validity) | `npm i -g markdownlint-cli2` |
| `vale` | Prose linter — banned-word lists for implementation/subjective terms | https://vale.sh |
| `pandoc` | Render REQ-XXX → DOCX/PDF for stakeholder review packs | https://pandoc.org |
| `mkdocs` + `mkdocs-material` | Browseable requirements site from the same Markdown source | `pip install mkdocs mkdocs-material` |
| `gherkin-lint` | Validate Given/When/Then AC syntax | `npm i -g gherkin-lint` |
| `behave` / `pytest-bdd` | Execute AC as test scaffolds in Python projects | `pip install behave` |
| `cucumber` | Same for JS/TS projects | `npm i -g @cucumber/cucumber` |
| `yq` | Query/transform YAML frontmatter across many REQ files | https://github.com/mikefarah/yq |
| `gh issue create --json` | Mirror REQ-XXX into GitHub Issues for sprint use | https://cli.github.com |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jama Connect | SaaS | REST API, OAuth | Heavyweight, regulated industries; agents drive via REST |
| ReqView | SaaS / desktop | OpenSpecTrace export | Lightweight; CSV/JSON I/O |
| IBM ENGINEERING DOORS Next | SaaS / on-prem | OSLC API | Enterprise standard; steep auth setup |
| Modern Requirements4DevOps | SaaS | Azure DevOps API | Lives inside ADO; agents call ADO REST |
| Aha! | SaaS | REST + GraphQL | Strong roadmap link; agent-friendly |
| Notion | SaaS | REST API + databases | Good for BRD; weak for REQ-XXX strictness |
| Confluence | SaaS | REST API | Standard for BRDs; agents read via REST |
| Linear | SaaS | GraphQL | Best for sprint-story view; not a spec store |
| Jira | SaaS | REST + JQL | Heavy; agents drive via `jira-cli` |
| GitHub Issues + Markdown specs | OSS | gh CLI + MCP | Recommended for solo/agentic; spec.md as source-of-truth |

## Templates & scripts

See `templates.md` for the BRD and User Story templates. Inline below: a small lint script that flags vague terms and implementation leaks across a `requirements/` tree.

```bash
#!/usr/bin/env bash
# req-lint.sh — fail if any REQ-XXX.md contains banned tokens.
set -euo pipefail
DIR="${1:-requirements}"
SUBJECTIVE='\b(fast|slow|easy|user-friendly|intuitive|simple|robust|seamless|nice)\b'
IMPLEMENTATION='\b(Postgres|MySQL|Redis|React|Vue|Angular|S3|Lambda|Kafka|Docker)\b'
fail=0
shopt -s globstar nullglob
for f in "$DIR"/**/REQ-*.md; do
  if grep -nEi "$SUBJECTIVE" "$f"; then
    echo "FAIL subjective: $f"; fail=1
  fi
  if grep -nE "$IMPLEMENTATION" "$f"; then
    echo "FAIL implementation leak: $f"; fail=1
  fi
  if ! grep -q '^## Acceptance Criteria' "$f"; then
    echo "FAIL missing AC: $f"; fail=1
  fi
  if ! grep -qE '^- \*\*Priority:\*\* (Must|Should|Could|Wont)' "$f"; then
    echo "FAIL priority not set: $f"; fail=1
  fi
done
exit $fail
```

## Best practices
- Store requirements as one Markdown file per `REQ-XXX` with YAML frontmatter — diff-friendly, grep-friendly, agent-friendly. A monolithic BRD is a render output, not a source.
- Number atomically and never reuse: `REQ-001` retired stays retired. Keep a `RETIRED.md` index for archaeology.
- Co-locate requirements with the feature folder (`backlog/<feature>/spec/REQ-*.md`) — the SDD lifecycle moves the whole folder, traceability stays intact.
- Force one requirement per file. Multi-requirement files defeat ID granularity and break traceability tools.
- Use Given/When/Then AC even for NFRs — "Given 500 concurrent users, when page loads, then 95th percentile < 2 s" is testable; "system shall be fast" is not.
- Prefix every NFR with its category (`PERF-`, `SEC-`, `USAB-`, `REL-`, `COMPAT-`, `OBS-`) so coverage agents can scan for missing categories.
- Treat the BRD and `spec.md` as views, not sources. Both render from the same `REQ-XXX` files via templates.
- Re-baseline on every signed-off scope change; don't edit-in-place silently. Bumping the version costs nothing and keeps the audit trail honest.
- Run lint + coverage in CI on every PR touching `requirements/`. Pre-commit hook is faster but bypassable.
- Translate AC to plain-language scenarios for stakeholder review. Engineers read Gherkin; sponsors do not.

## AI-agent gotchas
- **Agent-generated AC are too clean.** Real systems have edge cases (locale, currency, timezone, empty input, error fallback) the model omits. Add an explicit "edge case enumeration" pass driven by `faion-brainstorm`.
- **Hallucinated sources.** Agents cite "Sales Manager interview 2026-03-04" with no transcript backing it. Require a `source_url` or `transcript_id` in frontmatter; fail lint if missing.
- **Priority inflation.** LLMs default everything to Must. Force a quota: max 40 % Must, min 20 % Could/Wont — or require pairwise comparison output.
- **Implementation creep.** Drafts written from architect transcripts smuggle the architecture into the FR. Run a forbidden-token regex before commit.
- **Acceptance criteria copy-paste.** Agents reuse the same Given/When/Then across requirements with only the noun swapped. Diff-cluster AC and flag near-duplicates for human review.
- **One-shot summarisation drift.** Asking a single agent to produce all REQ for a feature loses fidelity. Chunk transcripts and emit one REQ per chunk; merge afterwards.
- **Sign-off forgery.** An agent that auto-fills "Approved" because a `--yes` flag was set has just falsified an audit record. Sign-off must be human-keyed and time-stamped, never agent-generated.
- **Long-context spec rot.** A 50 k-token `spec.md` exceeds the working window of small models. Index it: each REQ-XXX is its own file, the agent loads only what is needed.
- **Sycophantic validation.** Validation agents that rubber-stamp the drafter's output. Use a different model class (Opus to validate Sonnet, Sonnet to validate Haiku) and adversarial prompts ("find three reasons this requirement will fail in production").

## References
- BABOK Guide v3 — Chapter 7: Requirements Analysis and Design Definition
- IEEE Std 830-1998 — Recommended Practice for Software Requirements Specifications (still useful for NFR taxonomy)
- ISO/IEC/IEEE 29148:2018 — Requirements engineering process and content
- Karl Wiegers, "Software Requirements" 3rd ed. — implementation-leak / SMART playbook
- Mike Cohn, "User Stories Applied" — INVEST criteria for AC
- `requirements-traceability/agent-integration.md` (sibling) — closes the loop on traceability
- `requirements-lifecycle/agent-integration.md` (sibling) — state-machine that this doc feeds
- `requirements-validation/agent-integration.md` (sibling) — pre-baseline gate
