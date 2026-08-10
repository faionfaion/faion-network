# Decision journal / ADR
**Layer:** 1 — Context · **Verdict:** 🟢 take (the practice), 🟡 on the tooling — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is
An Architecture Decision Record is a short, immutable, numbered Markdown file recording one decision: the context that forced it, the options considered, the choice, and its consequences. The practice dates to Michael Nygard (2011); the dominant template today is MADR (Markdown Any Decision Records), maintained in the `adr` GitHub organisation. A decision journal is the accumulated directory of those files, ordered and cross-linked by supersession. In an agentic setting the argument for it is not documentation hygiene — it is that an agent which cannot see *why* a piece of code exists will refactor the reason away.

## Current state
| Fact | Value | Date |
|------|-------|------|
| MADR version | **4.0.0** | released 2024-09-17 |
| Prior versions | 4.0.0-beta 2024-09-02 · 3.0.0 (2022-10-09) introduced YAML frontmatter · 2.1.2 (2022-02-17) | — |
| Repo | `github.com/adr/madr` | fetched 2026-08-03 |
| Site | https://adr.github.io/madr/ | fetched 2026-08-03 |
| License | dual **MIT** and **CC0-1.0** | 2026-08-03 |
| Maintainer | ADR GitHub organisation (community, no foundation, no vendor) | 2026-08-03 |
| Price | free | 2026-08-03 |
| YAML variant | "YAML ADRs" / YADR reported available as of **March 2026** — machine-processable form of the same abstract template. Not mentioned on adr.github.io/madr as of 2026-08-03; treat as unconfirmed | 2026-03 (unverified) |
| AI/LLM guidance | **none.** MADR 4.0.0 and its site contain no mention of AI agents or LLMs | 2026-08-03 |

MADR has been stable for ~2 years. That is a feature, not neglect: nothing here is going to break under you.

## Mechanics

### The MADR 4.0.0 template, verbatim

```markdown
---
status: "{proposed | rejected | accepted | deprecated | … | superseded by ADR-0123}"
date: {YYYY-MM-DD when the decision was last updated}
decision-makers: {list everyone involved in the decision}
consulted: {list everyone whose opinions are sought (typically subject-matter experts); and with whom there is a two-way communication}
informed: {list everyone who is kept up-to-date on progress; and with whom there is a one-way communication}
---

# {short title, representative of solved problem and found solution}

## Context and Problem Statement

{Describe the context and problem statement, e.g., in free form using two to three sentences or in the form of an illustrative story. You may want to articulate the problem in form of a question. Consider adding links to collaboration boards or issue management systems. Make the scope of the decision explicit, for instance, by calling out or pointing at structural architecture elements (components, connectors, ...).}

## Decision Drivers

* {decision driver 1, for instance, a desired software quality, faced concern, constraint or force}
* {decision driver 2}

## Considered Options

* {title of option 1}
* {title of option 2}
* {title of option 3}

## Decision Outcome

Chosen option: "{title of option 1}", because {justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force {force} | comes out best (see below)}.

### Consequences

* Good, because {positive consequence, e.g., improvement of one or more desired qualities, …}
* Bad, because {negative consequence, e.g., compromising one or more desired qualities, …}

### Confirmation

{Describe how the implementation / compliance of the ADR can/will be confirmed. Is there any automated or manual fitness function? If so, list it and explain how it is applied.}

## Pros and Cons of the Options

### {title of option 1}

{example | description | pointer to more information | …}

* Good, because {argument a}
* Good, because {argument b}
* Neutral, because {argument c}
* Bad, because {argument d}

## More Information

{You might want to provide additional evidence/confidence for the decision outcome here and/or document the team agreement on the decision and/or define when/how this decision should be realized and if/when it should be re-visited.}
```

**Mandatory sections in MADR 4.0.0** are only: title, *Context and Problem Statement*, *Considered Options*, *Decision Outcome*. Everything else is optional — MADR ships four variants: `adr-template.md` (all sections + explanations), `adr-template-minimal.md` (mandatory only), `adr-template-bare.md` (all sections, no explanations), `adr-template-bare-minimal.md`.

**Filing convention:** `docs/decisions/NNNN-kebab-case-title.md`, zero-padded four digits, monotonically increasing, never renumbered. Status transitions are additive — a superseded ADR is never deleted or edited in place; its `status` becomes `superseded by ADR-0123` and the new record links back.

**The `Confirmation` section is the one that matters for agents.** It is where you name the mechanism that enforces the decision — a test, a lint rule, a CI check, a hook. This is the bridge from "written down" to "actually binding".

### Getting it in front of an agent

Nothing in MADR does this; you have to wire it. Three mechanisms, in increasing order of enforcement strength, all documented for Claude Code on 2026-08-03:

1. **Index, not corpus.** A one-line-per-decision index in `AGENTS.md`, with links. Costs ~1 line per decision; the agent reads the full record only when it touches the relevant area. This is the only variant that stays affordable past ~10 decisions.
2. **Path-scoped rules.** `.claude/rules/*.md` with `paths:` frontmatter loads the record only when the agent reads a matching file:
   ```markdown
   ---
   paths:
     - "src/billing/**/*.ts"
   ---
   # ADR-0007: idempotency keys on all payment writes
   Superseding this requires re-reading docs/decisions/0007-*.md first.
   ```
3. **Hooks.** Anthropic is explicit that context files are not enforcement: *"Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead."* An ADR whose `Confirmation` section names a test or a hook is binding. One that doesn't is a suggestion.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|-------|-----|--------------|---------|
| 1 | MADR template (develop branch, raw) | https://raw.githubusercontent.com/adr/madr/develop/template/adr-template.md | The full template, quoted verbatim above | 2026-08-03 |
| 2 | About MADR | https://adr.github.io/madr/ | MADR 4.0.0 released 2024-09-17; dual MIT + CC0-1.0; no AI/LLM content | 2026-08-03 |
| 3 | adr/madr releases | https://github.com/adr/madr/releases | Version/date history: 4.0.0 (2024-09-17), 4.0.0-beta, 3.0.0, 3.0.0-beta.2/beta, 2.1.2, 2.1.1, 2.1.0, 2.0.3, 2.0.2 | 2026-08-03 |
| 4 | Claude Code — How Claude remembers your project | https://code.claude.com/docs/en/memory | `.claude/rules/` with `paths:` frontmatter; "context, not enforced configuration"; PreToolUse hooks for hard enforcement; 200-line CLAUDE.md target; `/doctor` trims overviews | 2026-08-03 |
| 5 | Gloaguen et al., *Evaluating AGENTS.md* | https://arxiv.org/abs/2602.11988 | v1 2026-02-12, v2 2026-06-23. The two findings that bear directly on ADRs: *"instructions within context files were well followed by agents"* and *"repository overviews, while popular, proved unhelpful"*; overall >20% cost increase | 2026-08-03 |
| 6 | *Handoff Debt: The Rediscovery Cost When Coding Agents Take Over Interrupted Tasks* | https://arxiv.org/pdf/2606.02875 | June 2026 arXiv preprint. Adjacent, not direct evidence — quantifies rediscovery cost on handoff, which is the mechanism ADRs claim to reduce. **Not read in full; cited as a lead, not as support** | listed 2026-08-03 |
| 7 | Practitioner writing on ADRs-as-agent-context (Rick Pollick; Janis Explains Architecture; Mnemé; Catio) | rickpollick.com/blog/adr-comeback-anchoring-agentic-engineering-teams · janisexplainsarchitecture.com · mnemehq.com/insights/how-ai-coding-agents-use-adrs/ | 2026 practitioner consensus + the recurring anecdote (an agent refactoring away an idempotency layer written after a double-charge incident). **Opinion, not evidence** | 2026-08-03 |

## Adjudication of claim 5

**Claim — "ADR-style decision journals prevent agents from reopening settled questions."**

🟡 **Directionally right, evidentially unsupported, and overstated by the word "prevent."**

What I could and could not find, as of 2026-08-03:
- **No controlled study exists** measuring whether ADRs reduce agent regressions on settled decisions. Everything published in 2026 on this is blog-tier: consistent, plausible, and uncontrolled. The recurring case (an agent replacing a "verbose" idempotency layer that existed because of a Black Friday double-charge incident) is an anecdote repeated across posts, not a measurement.
- **The strongest real evidence is indirect and comes from the counter-evidence paper.** ETH Zurich/LogicStar found two things that cut in opposite directions for context files generally but *both favour ADR-shaped content specifically*: *"instructions within context files were well followed by agents"* and *"repository overviews, while popular, proved unhelpful."* An ADR is an instruction with a reason attached. A repo overview is the thing that measurably doesn't work. So the evidence base that damages "write a big AGENTS.md" is the same evidence base that supports "write down decisions and constraints."
- **"Prevent" is wrong.** Anthropic says so in its own docs: context files are *"context, not enforced configuration"*, with *"no guarantee of strict compliance."* An ADR raises the probability the agent respects a decision. Only the `Confirmation` mechanism — a test, a lint rule, a PreToolUse hook — prevents anything.
- **The cost is real and applies here too.** Every ADR line loaded into context carries the same +19–23% inference tax the paper measured. A 40-decision journal loaded wholesale is a self-inflicted wound. This is why the *index + path-scoped loading* pattern is not a nicety; it is the thing that makes the practice affordable.

**Defensible restatement for faion:** *Decision records make an agent's reasoning start from your precedent instead of from first principles, and the one measured finding we have says agents follow written instructions faithfully. They do not prevent anything — a decision is only enforced by the check named in its Confirmation section. Load them by index and by path, never wholesale.*

## What to borrow for faion
1. **The MADR 4.0.0 minimal template as our canonical shape.** MIT + CC0, two years stable, four mandatory sections. Do not invent a faion ADR format; adopt MADR and add the agent-loading layer on top. That layer is where our value is.
2. **The `Confirmation` section, promoted to mandatory.** MADR treats it as optional. For agentic work it is the whole point: it converts a record into an enforcement mechanism. A faion rule — *"an ADR without a Confirmation is a wish"* — is short, memorable and correct.
3. **The three-tier loading pattern** (index line in AGENTS.md → path-scoped `.claude/rules/` → PreToolUse hook), because it is the answer to the cost objection and nobody has published it as a pattern.
4. **Supersession as the anti-relitigation mechanism.** The value is not the record, it is the *chain*: `status: superseded by ADR-0123`. An agent that can see a decision was already revisited once, and why the revision landed where it did, is materially less likely to propose the original alternative a third time.
5. **Reversibility tagging as a triage rule** (we already own the slug). One-way-door decisions get an ADR and a hook; two-way-door decisions get a commit message. A solopreneur cannot afford an ADR per decision and should not write one.
6. **The honest framing on evidence.** Saying plainly "no controlled study exists; here is the indirect evidence and here is the mechanism" is a differentiator in a market where every competing post asserts causation.

## What NOT to borrow — and why
- **Heavy MADR with all optional sections.** *Decision Makers / Consulted / Informed* are RACI fields for organisations with more than one person. For a solopreneur they are pure token cost. Ship the minimal variant.
- **"Document every decision."** The volume kills it. The failure mode of ADR advocacy since 2011 has been an abandoned `docs/decisions/` directory with four records from the first week.
- **Loading the whole journal into context.** Direct violation of everything in the cost evidence, and the reason context files measure +19–23%.
- **LLM-generated ADRs written unsupervised.** Same failure class as `/init`-generated context files (measured −0.5% to −2%). An agent writing the record of its own decision produces a plausible post-hoc rationalisation, which is worse than no record because it *reads* authoritative. The existing `adr-ai-drafted-with-review` slug is the right shape — the review is load-bearing.
- **Any dedicated ADR tool** (adr-tools, log4brains, Log4brains-style static sites). A solopreneur needs numbered Markdown in git and one index line. A generator, a viewer, and a CI job are three more things to maintain for zero added agent benefit — the agent reads the Markdown, not the rendered site.
- **The causal claim.** Do not write "ADRs prevent agents from reopening settled questions" into a methodology. It is not established and it will be the first thing a technical buyer challenges.
- **YADR / YAML ADRs** until confirmed. Single unverified secondary reference dated March 2026; not on the MADR site. Do not build on it.

## Mapping to our corpus
Verified against `skills/faion/knowledge/*/INDEX.xml` on 2026-08-03. This area is **already well covered** — the densest ADR cluster I found in the corpus:

| Slug | Domain | Tier | Covers |
|------|--------|------|--------|
| `architecture-decision-records` | architecture | solo | Core practice (also duplicated in `sdd`, same slug, same tier) |
| `architecture-decision-records-planning` | sdd | solo | ADRs inside the planning phase |
| `adr-reversibility-tagging` | architecture | solo | One-way vs two-way door triage |
| `adr-staleness-audit` | architecture | pro | Detecting records that no longer describe reality |
| `adr-consequence-evidence-binding` | sdd | geek | Tying consequences to observable evidence |
| `adr-supersession-detection` | sdlc-ai | geek | Finding decisions that were silently superseded |
| `adr-ai-drafted-with-review` | sdlc-ai | geek | AI-drafted ADRs with human review — exactly the right guardrail |
| `decision-rationale-capture` | ba | pro | The "why", from the BA side |
| `decision-log-reconstruction-from-git` | (see INDEX) | — | Recovering a journal that was never written |
| `design-decision-log-template` | (see INDEX) | — | Template artefact |

Note: `architecture-decision-records` exists at **both** `knowledge/architecture/` and `knowledge/sdd/` with the same slug and tier. Worth checking whether that is intentional duplication or a manifest artefact.

**The genuine gap is not "ADRs" — it is "ADRs as agent context."** Nothing in the cluster addresses loading, cost, or enforcement. Proposed:

1. **`adr-as-agent-context`** — domain `sdlc-ai`, tier **solo**. The three-tier loading pattern (index line → `.claude/rules/` `paths:` → PreToolUse hook), the token budget, and the rule that `Confirmation` is mandatory for agentic work. This is the one new record worth writing.
2. **No new methodology** for the base practice, the template, supersession, staleness, or reversibility — all covered by the slugs above.
3. **Refresh `architecture-decision-records`** with the MADR 4.0.0 pin (2024-09-17, MIT + CC0) if it isn't already versioned, and resolve the architecture/sdd duplication.

## Open questions / staleness risk
- **Low staleness risk overall.** MADR 4.0.0 has been stable since 2024-09-17 and has no vendor dependency. This is the most durable item in Layer 1.
- **YADR is unverified.** One secondary source, dated March 2026, not reflected on adr.github.io/madr as of 2026-08-03. Confirm before any faion content references it.
- **The evidence gap is the interesting one.** No controlled study on ADRs-as-agent-context exists. That is a research opportunity: the ETH methodology (agent × benchmark × context-variant, ≥5 runs, median) applied to decision records instead of overviews would be publishable and would be a genuine differentiator for faion's corpus. Cost is the obvious barrier.
- **`Handoff Debt` (arXiv 2606.02875, June 2026) is a lead I did not run down.** If it quantifies rediscovery cost, it is the closest thing to indirect quantitative support for the decision-journal argument. Worth a dedicated read before we make any evidentiary claim.
- **Claude Code mechanism churn.** `.claude/rules/` `paths:` behaviour has version-pinned notes (v2.1.198 symlink matching, v2.1.207 invalid-bracket handling, v2.1.211 `--setting-sources` interaction, v2.1.217 brace-expansion budget). Any faion methodology naming those mechanisms must date them.
