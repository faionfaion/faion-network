# /faion-net-content — pipeline playbook

This file is the orchestrator's runbook. The skill's main thread reads it, then walks the user through phases.

**Doctrine version**: v4 (as of 2026-05). See `config/style-guide.md` for the full doctrine.

## Phase 1 — Idea funnel

### 1.1 Audience or theme selection (interactive)

Before any subagent fires, you (main thread) propose 5 directions to the user via AskUserQuestion. Mix audience-first and theme-first proposals. For each option provide a 1-2 sentence argument grounded in faion's positioning.

Example proposal set (refresh per call — don't reuse stale options):

| Direction | Argument |
|-----------|----------|
| Solo indie devs/builders | Core target; biggest LTV per article; corpus aligns directly. |
| Small agency owners (1-5 ppl) | Highest willingness to pay; "team-replacement" angle resonates. |
| Technical founders pre-PMF | Buy SDD methodology; long retention; high referral coefficient. |
| Solo consultants/freelancers | Adjacent ICP; underserved by competitors; high CAC efficiency. |
| AI-native operators | Newest segment; commands premium; aligns with "ship in weeks" hook. |

Or theme-first:

| Theme | Argument |
|-------|----------|
| SDD deep dives | Anchors faion as SDD-first; locks in geek tier; high authority signal. |
| Solo-operator economics | Direct path to revenue; highly shareable; cross-tier appeal. |
| AI-augmented engineering | Ships traffic; CLI alignment; differentiates from generic AI content. |
| Distribution for indies | Real pain; few quality resources; positions us as practitioners. |
| AI-stack composition | Authority + lead gen; easy to refresh quarterly. |

User picks one. Save the choice to `.aidocs/content/ultimate-guide/_session/<timestamp>-direction.md`.

### 1.2 Brainstorm — 5 parallel agents

Spawn 5 parallel `Agent` calls with the prompt at `prompts/phase1-brainstorm.md`. Pass each:
- The chosen direction (audience or theme).
- An "angle bias" so the 5 agents cover different sub-perspectives:
  1. `practitioner-pain` — frustration-driven (what blocks them today).
  2. `aspiration` — goal-driven (what they're trying to become).
  3. `economics` — money-driven (revenue/cost/runway problems).
  4. `tooling` — stack-driven (workflow/integration friction).
  5. `meta` — strategic (positioning/distribution/career).

Each agent must:
- Use WebSearch ≥ 3 times against credible sources (HN, indie hackers, Twitter/X threads, sub-Reddits, indie newsletters).
- Identify 5+ concrete pain points.
- Propose **20 article ideas** that solve one or more pain points.
- Return JSON per the schema in `prompts/phase1-brainstorm.md`.

Total raw idea pool: 100 ideas across 5 angles.

Save to `.aidocs/content/ultimate-guide/_session/<ts>/brainstorm-<angle>.json` (5 files).

### 1.3 Scoring — 5 parallel agents

Spawn 5 parallel `Agent` calls with `prompts/phase1-score.md`. Each agent scores **all 100 ideas** across 5 criteria (10-point scale):

| Criterion | Question |
|-----------|----------|
| `strategic_value` | Does this advance faion's positioning (SDD-first, solopreneur stack, CLI moat)? |
| `search_demand` | Realistic SEO/distribution potential based on observed audience signals? |
| `pain_severity` | How urgent/painful is the problem this solves for the ICP? |
| `differentiation` | Do we say something new vs the existing internet on this topic? |
| `corpus_synergy` | How well does this leverage faion-network methodologies/playbooks? |

Each agent independently produces a JSON score file. Aggregate: per-idea final score = mean-of-means across 5 agents. Capture rationale spread to surface controversial picks.

Save each agent output to `.aidocs/content/ultimate-guide/_session/<ts>/scores-agent-score-<N>.json`.

### 1.4 Backlog merge (main thread)

Filter: ideas with final mean ≥ 7.0 → push to `.aidocs/content/ultimate-guide/backlog/by-audience/<audience>.md` (one file per audience) or `.aidocs/content/ultimate-guide/backlog/<slug>.md` (one file per idea, deprecated layout).

Sort by `final` descending. Report N ideas saved + median score + top-3 titles.

## Phase 2 — Per-article workflow

Triggered by user pointing at a backlog item: "напиши цю статтю", "розпиши `<slug>`", or "drive `<slug>` to publish".

### 2.0 SEO + keyword research — 1 agent (BEFORE the brief is finalised)

Spawn 1 `Agent` with `prompts/phase2-seo-keywords.md`. The agent does real keyword research (≥5 WebSearch calls) and produces `.aidocs/content/ultimate-guide/briefs/<slug>-keywords.md` containing:
- Primary keyword (2-5 word head term; the URL slug should match).
- 5-8 secondary keywords (long-tail variants).
- 15-30 LSI / semantically-related terms.
- 3-5 entity anchors (named real people / brands / methodologies + disambiguation clauses).
- 3-5 named related queries (for the FAQ block).
- 15-25 audience-language phrases (sourced from HN / IH / Reddit / X with URLs).
- Top-5 SERP analysis (URLs + angles + word counts + gaps).
- Differentiation thesis (2-3 sentences).
- LLM / GEO optimization notes.

The brief, writer, editor, and reviewer all reference this artefact downstream.

### 2.1 Editorial brief — 1 agent

Spawn 1 `Agent` with `prompts/phase2-editorial-brief.md`. Pass:
- Backlog file path.
- Keywords artefact (`<slug>-keywords.md`).
- Read-access to `~/workspace/projects/faion-net/faion-network/skills/faion/knowledge/` and `playbooks/`.
- Permission to WebSearch.

Agent produces `.aidocs/content/ultimate-guide/briefs/<slug>-brief.md` with thesis, Story Circle beat structure, target audience refinement, methodology hooks (slugs only, internal — NOT cited in body), named framework coinage, character spine, word count target (12K-17K for ultimate-guide longreads), and distribution plan.

### 2.2 Write — 1 agent

Spawn 1 `Agent` with `prompts/phase2-write.md`. Pass:
- Brief file path.
- Keywords artefact.
- Style guide (`config/style-guide.md`).
- Read access to all cited methodologies.

Writer produces `content/ultimate-guide/<slug>/en.mdx` (with frontmatter per `style-guide.md § Frontmatter shape`).

### 2.3 Reviews — 2 parallel agents

Spawn 2 `Agent` calls in parallel:
- **Style reviewer** (`prompts/phase2-review-style.md`) — voice, tone, brand consistency, line-level craft, anti-AI-tell signals, 2-20 ladder, intro structure, list discipline.
- **Content reviewer** (`prompts/phase2-review-content.md`) — thesis fulfilment, named framework, character spine, receipts audit, corpus citation accuracy, fact-check, FAQ accuracy.

Both reviewers MUST run `scripts/check-glossary-coverage.py` before manual audit and include its report.

Each writes a review file under `.aidocs/content/ultimate-guide/reviews/<slug>/<style|content>-review.md` with:
- Verdict: APPROVE / APPROVE-WITH-EDITS / APPROVE-WITH-FOLLOWUPS / REJECT.
- Must-fix list (blocking).
- Should-fix list (judgement).
- Wins.

### 2.4 Edit — 1 agent

Spawn 1 `Agent` with `prompts/phase2-edit.md`. Pass:
- Article draft (`en.mdx`).
- Both reviews.

Editor applies feedback, resolves contradictions (style wins on tone, content wins on facts, brief wins on structure, 2-20 ladder fixes are mandatory), runs `scripts/check-glossary-coverage.py` before status flip, produces final `en.mdx`. Bumps frontmatter status to `ready-to-translate`.

### 2.5 Translate — 7 parallel agents

Spawn 7 `Agent` calls in parallel, one per language: `uk`, `pt`, `es`, `fr`, `de`, `hi`, `pl`. Prompt: `prompts/phase2-translate.md`. Each gets:
- Final `en.mdx`.
- Target language code.
- `config/language-rules/<lang>.md` for translation-specific guidance.
- Keywords artefact (translator picks target-language primary keyword variant).

Translators have explicit licence to ADAPT text + headings to the cultural context of native speakers (per `style-guide.md § Translation cultural adaptation`). Receipts (named real people, dates, $-amounts, places) stay verbatim. Thesis + framework definition stay identical.

Translator produces `content/ultimate-guide/<slug>/<lang>.mdx` with same frontmatter shape (translated title + description, slug stays English-stable for URLs).

### 2.6 Translation review — 7 parallel agents

Spawn 7 `Agent` calls in parallel, one per language. Prompt: `prompts/phase2-review-translation.md`. Each gets:
- Translated `<lang>.mdx`.
- Source `en.mdx`.
- `config/language-rules/<lang>.md`.

Reviewer MUST run `scripts/check-glossary-coverage.py` before manual audit. Applies in-place fixes (writes back to `<lang>.mdx`) and emits a delta report at `.aidocs/content/ultimate-guide/reviews/<slug>/translation-<lang>.md` summarising:
- Glossary-coverage script verdict (0 missed first-mention wraps required).
- English-idiom accuracy (no `long-running` mistranslations etc.).
- Reading register (average sentence length sampled across 3 paragraphs, longest sentence).
- Cultural adaptation audit (thesis / framework / receipts preservation).
- Glossing + naming + intro structure.
- 2-20 attention ladder rungs.
- Per-language hunts (russisms for UA, voseo for ES, BR-leakage for PT, calques for FR, Substantiv-Großschreibung for DE, code-switch ratio for HI, diacritics for PL).
- Final verdict: APPROVE / APPROVE-WITH-EDITS / APPROVE-WITH-FOLLOWUPS / REJECT.

After all 7 translations are reviewed + final, the article status flips to `published` and goes live via the usual Gatsby build path.

## State machine

The frontmatter `status` enum is constrained by the F-070 validator in `src/utils/ultimate-guide-frontmatter.ts`:

```
draft → ready-to-translate → translated → polished → published
```

`backlog → brief → draft` are tracked in session state, not frontmatter. Phase 2.6 polish flips `translated → polished` (intermediate review state) before the main thread flips `polished → published` at deploy.

## Failure modes

- **Brainstorm agent returns < 20 ideas**: re-spawn that agent once. If still short, accept partial.
- **Scoring agents disagree heavily (stddev > 2.0 on a criterion)**: flag in backlog as `controversial: true` for manual triage.
- **SEO research finds no real audience-language phrases**: re-spawn with stricter prompt; primary keyword without verbatim audience signal is REJECT.
- **Writer over/undershoots word count by > 30%**: send back to writer with explicit count instruction; do not silently accept.
- **Glossary-coverage script reports missed first-mention wraps**: editor/translator must fix all before status flip.
- **Translation review rejects**: send back to translator for a v2; if v2 also rejected, escalate to user for manual call.
- **MDX build fails after deploy**: usually frontmatter validation (status enum, methodology_refs / playbook_refs arrays, description 140-160 chars) or unescaped `<X>` placeholders in body. Fix the offending file, rebuild.

## Configuration files

- `config/languages.json` — language list + display names + RTL flags.
- `config/paths.json` — storage paths (overridable).
- `config/style-guide.md` — voice, tone, formatting, multicultural English, 2-20 attention ladder, intro doctrine, lists, SEO + LLM, paywall, anti-AI-tell, translation cultural adaptation. Master reference.
- `config/language-rules/<lang>.md` — per-language polish rules (reading register, anglicism whitelist, target-language anti-AI-tell, audience-register table, name transliteration policy).

## Scripts

- `scripts/check-glossary-coverage.py` (in `faion-net-fe` repo, not in this skill) — automated audit of first-mention `<GlossaryTerm>` wraps against `glossary-map.json` (156 entries). Required step in 2.3, 2.4, 2.6. Default mode reports missed first-mentions only; `--all` flag dumps every unwrapped mention; `--json` for machine-readable output. Exit 0 = clean, 1 = findings.
