# AGENTS.md standard
**Layer:** 1 — Context · **Verdict:** 🟢 take (the convention), with hard size discipline — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is
AGENTS.md is a plain-Markdown file placed at a repository root that coding agents read at task start to learn project-specific facts: build and test commands, conventions, and boundaries. It was published by OpenAI in August 2025 and contributed to the Linux Foundation's Agentic AI Foundation (AAIF) at the foundation's launch on 2025-12-09, alongside MCP (Anthropic) and goose (Block). It has no schema, no required fields and no version number as of 2026-08-03 — the "standard" is the filename and its location, not a grammar. Its real value is interoperability: one file that 27+ agent tools read, instead of one proprietary rules file per vendor.

## Current state
| Fact | Value | Date |
|------|-------|------|
| Spec version | none — no versioned spec exists; AAIF roadmap lists "AGENTS.md v1.0, first stable behavioral specification" as a future workstream | 2026-08-03 |
| Canonical site | https://agents.md/ | fetched 2026-08-03 |
| Canonical repo | `github.com/agentsmd/agents.md` (formerly `openai/agents.md`) | fetched 2026-08-03 |
| License | MIT | fetched 2026-08-03 |
| Steward | Agentic AI Foundation, under the Linux Foundation | since 2025-12-09 |
| AAIF membership | 47 orgs at launch (8 Platinum / 18 Gold / 21 Silver); **190 orgs** after 43 additions | 2025-12-09 → 2026-05-18 |
| AAIF working groups | 7, formed Q1 2026: identity-and-trust, accuracy-and-reliability, workflows-and-process-integration, agentic-commerce, security-and-privacy, observability-and-traceability, governance-risk-regulatory-alignment | Q1 2026 |
| Adoption | "more than 60,000 open source projects"; the same 60k figure is still the one quoted in AAIF material as of mid-2026 — no newer official count found | figure dated 2025-12-09 |
| Price | free (MIT, no service component) | 2026-08-03 |

## Mechanics

**Format.** Standard Markdown. Quoting agents.md verbatim: *"AGENTS.md is just standard Markdown. Use any headings you like; the agent simply parses the text you provide."* There are no mandatory fields, no frontmatter requirement, no linter, no conformance test.

**Location and resolution.** Root-level `AGENTS.md`. For monorepos, additional `AGENTS.md` files go in subdirectories; **"the closest AGENTS.md to the edited file wins."** agents.md cites OpenAI's own main repo as carrying 88 nested files. Precedence, top to bottom:
1. Explicit user instruction in chat — overrides everything.
2. Nearest `AGENTS.md` walking up from the edited file.
3. Ancestor `AGENTS.md` files.

**Conventional sections** (recommended, not required): project overview; build and test commands; code style; testing instructions; security considerations; commit/PR guidelines; deployment steps.

**Claude Code interop — the exact, official mechanism.** From the Claude Code docs page `code.claude.com/docs/en/memory`, section "AGENTS.md" (fetched 2026-08-03), verbatim: *"Claude Code reads `CLAUDE.md`, not `AGENTS.md`."* The documented fix is the one-line import:

```markdown
@AGENTS.md

## Claude Code

Use plan mode for changes under `src/billing/`.
```

Import rules that matter: `@path/to/import` syntax; relative paths resolve against the *importing file*, not the cwd; recursion allowed to a **maximum depth of four hops**; import parsing skips code spans and fenced blocks, so `` `@README` `` is literal text while `@README` imports. Imported files are expanded **at launch** — so the import saves duplication, not tokens.

Symlink alternative, also documented:
```bash
ln -s AGENTS.md CLAUDE.md
```
Caveat stated in the same doc: *"On Windows, creating a symlink requires Administrator privileges or Developer Mode, so use the `@AGENTS.md` import instead."*

**Claude Code loading order** (same doc): files are concatenated, not overridden — managed policy → `~/.claude/CLAUDE.md` → ancestor dirs root-downward → cwd `CLAUDE.md` → `CLAUDE.local.md`. Subdirectory `CLAUDE.md` files load lazily, when Claude reads a file in that directory. Anthropic's own stated size target: **"target under 200 lines per CLAUDE.md file."** `/init` with `CLAUDE_CODE_NEW_INIT=1` also reads `AGENTS.md`, `.cursor/rules/`, `.github/copilot-instructions.md`, `.devin/rules/`, `.windsurf/rules/`, `.clinerules`.

**Where the file is delivered in the prompt** (matters for reliability): *"CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself... there's no guarantee of strict compliance."* For hard enforcement Anthropic points at PreToolUse hooks, not context files.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|-------|-----|--------------|---------|
| 1 | AGENTS.md (canonical site) | https://agents.md/ | Format statement, nesting rule, precedence, 27+ supporting tools, 60k adoption | 2026-08-03 |
| 2 | agentsmd/agents.md repo | https://github.com/agentsmd/agents.md | MIT license, example file, Next.js site source | 2026-08-03 |
| 3 | LF press: AAIF formation | https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | Dated 2025-12-09; 47 founding members by tier; AGENTS.md released Aug 2025, 60k repos | 2026-08-03 |
| 4 | LF press: AAIF adds 43 members | https://www.linuxfoundation.org/press/agentic-ai-foundation-adds-43-new-members-as-enterprise-and-government-adoption-of-open-agent-standards-accelerates | Dated 2026-05-18; total 190 members; 4 Gold (F5, GoDaddy, Stripe, TRON), 27 Silver, 12 Associate | 2026-08-03 |
| 5 | Claude Code — How Claude remembers your project | https://code.claude.com/docs/en/memory | "Claude Code reads CLAUDE.md, not AGENTS.md"; `@AGENTS.md` import; symlink; 4-hop import depth; 200-line target; `claudeMdExcludes`; `.claude/rules/` with `paths:` frontmatter | 2026-08-03 |
| 6 | Gloaguen, Mündler, Müller, Raychev, Vechev — *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?* | https://arxiv.org/abs/2602.11988 | arXiv v1 2026-02-12, v2 2026-06-23. Abstract verbatim: context files *"increased inference cost by over 20% on average"*, *"did not generally improve task success"*, *"repository overviews, while popular, proved unhelpful"*, *"instructions within context files were well followed"* | 2026-08-03 |
| 7 | AAIF blog — *Measuring AGENTS.md: What Five Runs Show That One Doesn't*, A. Griffiths | https://aaif.io/blog/measuring-agents-md-what-five-runs-show-that-one-doesn-t | Dated 2026-07-22. 12-line AGENTS.md, GitHub Copilot CLI, 5 runs/condition: ambiguous task **−27% wall time, −24% credits, −26% diff size**; multi-file task median win 9–10%. Her single first run showed AGENTS.md **44% slower / 41% more expensive** — reversed by the median | 2026-08-03 |
| 8 | Upsun — *The research is in: your AGENTS.md is probably too long* | https://developer.upsun.com/posts/ai/agents-md-less-is-more | Dated 2026-02-23. Secondary, but reports the paper's per-cell numbers: GPT-5.2 **+22%** and GPT-5.1 Mini **+14%** reasoning tokens on SWE-bench Lite; developer-written files **up to +19%** cost; LLM-generated **>+20%** | 2026-08-03 |
| 9 | Engineer's Codex — *Your Agents.md Might Be Making AI Worse* | https://www.engineerscodex.com/agents-md-making-ai-worse/ | Dated 2026-02-18. Secondary. LLM-generated: **−0.5%** SWE-bench Lite, **−2%** AGENTbench. Human-written: **+4%** avg on AGENTbench. Benchmarks: SWE-bench Lite 300 tasks; AGENTbench 138 issues / 12 niche Python repos. Agents: Claude Code + Sonnet 4.5, Codex + GPT-5.2 and GPT-5.1 mini, Qwen Code + Qwen3-30B | 2026-08-03 |

## Adjudication of the user's claims

**Claim 1 — "AGENTS.md is de-facto standard under AAIF (Linux Foundation) since Dec 2025, 170+ member orgs, 60,000+ repos."**
✅ **Confirmed, and the membership number is stale-low.** AAIF was announced 2025-12-09 with AGENTS.md as a founding project. Membership was 47 at launch, passed 170 by April 2026, and reached **190 as of 2026-05-18** (LF press release). 60,000 repos is the officially quoted figure but it is dated **2025-12-09** — eight months old, and no refresh has been published. Do not present 60k as a current number; present it as "60k+ as of Dec 2025." Also correct the word "standard": there is **no versioned specification**; v1.0 is a roadmap item. It is a de-facto *convention*.

**Claim 2 — "Claude Code is the main holdout — reads only CLAUDE.md."**
✅ **Confirmed verbatim from the primary source**, dated 2026-08-03: *"Claude Code reads `CLAUDE.md`, not `AGENTS.md`."* Two corrections of tone: (a) "holdout" overstates it — Anthropic documents the bridge in its own docs and `/init` under `CLAUDE_CODE_NEW_INIT=1` reads `AGENTS.md` when generating; (b) the widely repeated claim that Claude Code reads AGENTS.md "as a fallback" is **false**.

**Claim 3 — "Correct pattern: AGENTS.md is the real file, CLAUDE.md is one line `@AGENTS.md`."**
✅ **Confirmed — this is Anthropic's own documented recommendation**, with the exact snippet reproduced in the Mechanics section. One nuance worth adding to any faion methodology: the import is expanded **at launch**, so it buys deduplication and portability, **not** context savings. Anthropic states this explicitly: *"Splitting into `@path` imports helps organization but doesn't reduce context, since imported files load at launch."*

## What to borrow for faion
1. **The file convention itself.** Zero-cost, MIT, vendor-neutral, already the shape our repos use. It is the correct default answer to "where do I write down what the agent should know."
2. **The exact bridge snippet** (`@AGENTS.md` + a Claude-only section beneath it) with the Windows symlink caveat. This is a 10-line, high-frequency, dated fact — ideal free-tier content and a natural CLI answer.
3. **The cost discipline the ETH paper actually justifies.** Rules that follow directly from dated evidence, not vibes:
   - Instructions and constraints in, **repository overviews out** — the paper singles out overviews as *"unhelpful"*, and Claude Code's own `/doctor` trim (v2.1.206+) cuts exactly that: *"content Claude can derive from the codebase, such as directory layouts, dependency lists, and architecture overviews."*
   - **Never ship a `/init`-generated file unedited.** LLM-generated context files measured **−0.5%** (SWE-bench Lite) and **−2%** (AGENTbench).
   - Hard ceiling: **200 lines**, Anthropic's own stated target.
   - Budget every line: any context file costs **+19–23% inference** and up to **+22% reasoning tokens**. A line must earn that.
4. **Nesting as scope control**, not as volume: "the closest AGENTS.md wins", plus `claudeMdExcludes` globs and `.claude/rules/` `paths:` frontmatter for path-scoped instructions that only load when matching files are touched. This is the only mechanism that gets context cost *down* while keeping coverage.
5. **The five-run measurement protocol** from the AAIF blog. Its most useful result is methodological: one run said AGENTS.md was 44% slower and 41% more expensive; the five-run median said it was 27% faster and 24% cheaper. Any faion methodology that claims a context-file improvement must specify **≥5 runs and report medians**.

## What NOT to borrow — and why
- **"Comprehensive AGENTS.md" templates.** Every published "complete 2026 template" pushes toward the exact shape the paper shows is net-negative: long, overview-heavy, LLM-drafted. Faion should not ship a big template.
- **Auto-generation as a product feature.** A "faion generates your AGENTS.md" command would be selling the measured-harmful variant. If we ever ship generation, it must generate a *draft to be cut down by a human*, and say so.
- **`AGENTS.md` as the place for procedures.** Multi-step procedures belong in skills or path-scoped rules that load on demand. Claude Code's docs say this directly. Faion's own methodology corpus is the loaded-on-demand layer — this is a competitive point, not just hygiene.
- **The "170+ members" / "60,000 repos" figures used as current.** Both are dated snapshots; the membership one is already wrong (190).
- **Any claim that AGENTS.md improves agent success.** The honest, defensible line is: *it makes agent behaviour predictable and portable across tools; measured accuracy gains are small and inconsistent, and it always costs tokens.*
- **Over-specification.** The paper's own explanation of the failure mode: agents follow the file *faithfully* and then over-comply — running more tests, searching and reading more files. Every "always do X" line is a hard constraint the agent will pay for on every unrelated task.

## Mapping to our corpus
Verified against `skills/faion/knowledge/*/INDEX.xml` on 2026-08-03.

Existing overlap:
| Slug | Domain | Tier | Overlap |
|------|--------|------|---------|
| `agents-md-per-module-bootstrap` | sdlc-ai | solo | Nesting / per-module files — direct overlap with the "closest file wins" rule |
| `agents-md-for-receiving-team` | sdd | pro | Handoff framing of the same file |
| `claude-md-creation` | dev | geek | CLAUDE.md authoring |
| `claude-md-creation-quality` | dev | geek | Quality bar for CLAUDE.md |
| `context-window-curation-for-coding-agents` | dev | solo | The cost side of context files |

Gaps worth new methodologies:
1. **`agents-md-claude-md-bridge`** — domain `dev`, tier **free**. The `@AGENTS.md` one-liner, the symlink, the Windows caveat, the 4-hop import limit, and the explicit "imports do not save context" fact. Short, verifiable, high query frequency; strong free-tier hook that leads into the paid context-budget material.
2. **`context-file-cost-budget`** — domain `sdlc-ai`, tier **solo**. Turns the ETH numbers into a rule set: 200-line ceiling, instructions-in/overviews-out, no unedited `/init` output, path-scoped rules for anything conditional, and the ≥5-run median protocol for claiming any improvement. Nothing in the corpus currently carries dated evidence on this.
3. **`agents-md-per-module-bootstrap` needs a dated update**, not a new slug: it should cite the "closest file wins" rule and the 2026 cost evidence, and should now point at `claudeMdExcludes` and `.claude/rules/` `paths:` scoping as the volume-control mechanism.

No new methodology needed for the plain "what is AGENTS.md" question — covered by the two existing `agents-md-*` slugs once refreshed.

## Open questions / staleness risk
- **High churn risk on the Claude Code side.** The memory docs page carries per-version notes down to v2.1.217. Anything we write about `claudeMdExcludes`, `.claude/rules/` `paths:` budgets, or `/doctor` trims is version-pinned and should be dated in-line.
- **AGENTS.md v1.0 is on the AAIF roadmap.** When a real spec lands, "no required fields" stops being true and any faion content asserting it goes stale overnight. Set a re-check.
- **Adoption number is unmaintained.** 60k is a Dec 2025 figure repeated into mid-2026. If we quote it, we date it.
- **Unverified precision in the user's doc:** "failed in 5 of 8 settings." The study covers 4 agent/model configurations × 2 benchmarks = 8 cells, so the shape is right, but I could not extract the per-cell table from the PDF (arXiv HTML build 404s; the PDF is image-heavy). Direction is confirmed by three independent sources; treat the exact "5 of 8" as unverified.
- **Counter-evidence tension is unresolved and should stay unresolved in our content.** The ETH paper (438 tasks, 4 agents, peer-review-track) says context files cost >20% and don't reliably help. The AAIF blog (2026-07-22, 1 repo, 2 tasks, 5 runs, GitHub Copilot CLI, 12-line file) says a *tiny* file cuts time and cost by ~25%. These are compatible: the AAIF test is the "short file" cell the paper never isolated. That reconciliation — *length is the variable* — is the most sellable insight here, and nobody else has published it as a rule.
