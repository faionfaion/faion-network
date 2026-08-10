# faion.net article style guide

The reference all writers, reviewers, editors, and translators share. Updated after the content-restructure research synthesis (May 2026). Replaces the original short-article style guide; ultimate-guide longreads now target 14,000-16,000 words with explicit structural commitments.

## What this guide is for

Ultimate-guide longreads (12K-17K words) on faion.net. The piece must PULL the reader, ARGUE the case, TEACH the action, and not read like AI. Five layers stacked:

## Multicultural English doctrine (TOP-LEVEL RULE)

The English-language version is the canonical SOURCE for translation AND a published article in its own right. English-speaking readers come from India, the Philippines, Singapore, Nigeria, Brazil, Eastern Europe, the EU, the UK, Canada, Australia, US, Latin America. **The English text must be readable by ALL of them, not the US-FAANG subset only.**

Rules:

1. **No un-contextualised US-only jargon** anywhere in the article. Allowed terms with first-mention parenthetical gloss: W-2 (US tax form marking permanent salaried employment), 1099 (US contractor tax form), Senior IC (Senior Individual Contributor — non-manager engineer ladder), TC (Total Compensation — base + bonus + equity), RSU-cliff (Restricted Stock Unit vesting cliff), 401(k) (US employer-sponsored retirement account), COBRA (US post-employment health insurance bridge), S-Corp / Sole Prop (US tax-entity types), FICA (US payroll tax), put option (the financial-derivative metaphor — must be glossed if used in non-technical sense). After first gloss, the term can repeat without re-explanation.
2. **No un-contextualised cultural terms** — words like *salaryman*, *kabuki*, *omakase*, *naginata*, *zaibatsu*, *kanban* (in pre-Toyota sense), *bushido* must be glossed at first mention with a 5-15 word parenthetical: "salaryman (Japanese white-collar career employee in lifetime corporate employment)". The same rule applies to American-only cultural terms ("FAANG", "Big 4", "Y Combinator", "Indie Hackers", "Show HN", "Hacker News", "Stripe Atlas") — gloss at first mention if the meaning is load-bearing for non-US readers.
3. **No un-contextualised people** — every named real person gets a one-clause introduction at first mention: "Patrick McKenzie (Stripe Atlas founder and writer of the long-read Kalzumeus essays)", "Sahil Lavingia (Gumroad founder, author of *The Minimalist Entrepreneur*)", "Pieter Levels (Nomad List / Photo AI / Remote OK founder)". After first introduction, the name can repeat alone.
4. **Currency**: $-amounts stay verbatim (the article's receipts are USD-denominated and that's part of the credibility contract), but on the first $-amount of the article add a parenthetical that anchors local feel: "$250K Total Compensation (≈ €230K / ₹2 crore / ₴10M)" or a "for the senior-IC ladder in expensive US tech markets" qualifier. After first occurrence, plain $ amounts are fine.
5. **Idioms**: avoid US-only idioms whose meaning doesn't translate ("hit a home run", "out of left field", "Hail Mary", "Monday-morning quarterback"). Use globally-legible idioms or the literal phrasing.
6. **Spelling**: US English is the default (`color`, `optimize`, `realize`). Don't mix UK/US within the article.

**Severity**: every multicultural-readability finding is a MUST-FIX, never a should-fix. A reader who has to Google three terms in the first paragraph is a reader who bounces.

### Pain-hook is body — glossing applies there too

The pain-hook Paragraph A (defined under § "Pain-hook intro + TLDR setup" below) is the FIRST body content — it precedes Beat 1 but it IS body, not frontmatter. Every term that appears in the pain-hook for the first time in the article counts as "first body mention" and gets the same gloss treatment as any other first body mention.

Specifically forbidden: leaving *runway* / *ramen profitable* / *MRR* / *burn rate* / *vesting cliff* / *RSU* in the pain-hook without a same-breath explanation (parenthetical gloss or `<GlossaryTerm>` wrap, either works). The gloss is part of the recognition moment, not a footnote.

Example:

> *In October you did the math on your own savings, sketched what* ramen profitable *(the Paul Graham coinage: a one-person business earning enough to cover instant noodles and rent, the minimum survivable threshold) looks like at your numbers, and quietly closed the tab.*

The automated `scripts/check-glossary-coverage.py` script flags missed first-mention wraps in the pain-hook the same way it flags them anywhere else in the body.

## Pain-hook intro + TLDR setup (TOP-LEVEL RULE)

Before the Story Circle's in-medias-res Beat 1 opening, the article carries a TWO-PARAGRAPH lead structure that earns the next 20 seconds and frames the rest of the piece:

### Paragraph A — Pain-hook (50-90 words, direct address, second-person "you")

The first paragraph addresses the reader as "you" and stages a SPECIFIC moment of recognition. Not abstract setup ("if you're a senior engineer thinking about going indie…"). A concrete scene with sensory texture the reader instantly verifies against their own life. Example pattern:

> *It's 11pm. You closed Slack two hours ago, but you can still feel the channel pings in your shoulders. Indie Hackers is open in the next tab. You scrolled to that user's $7,200 MRR thread again. You did the math on your own savings on the back of a meeting note in October. The number was good, and you closed the tab without telling anyone. Three months later, the tab is still re-opened every evening, and you still haven't told anyone.*

Rules for the pain-hook:
- Second-person ("you") direct address.
- A specific moment in time, not a state of being.
- Sensory details (sound, light, time of day, body) that bypass intellectual screening.
- The reader recognises themselves OR they bounce — both are acceptable, the article isn't for everyone.
- NO framework name, NO US-jargon (other than what the multicultural doctrine permits), NO numbers that lock out non-FAANG readers.
- NO "if you've ever…" hedging. Make a claim about a specific moment, let the reader self-validate.

### Paragraph B — TLDR setup (80-140 words, third-person, frames the article)

The second paragraph leaves the reader's scene and frames what the article delivers. This is the TLDR a reader who bounces here still gets value from. It includes:

- One sentence naming the PROBLEM in plain target-language.
- One sentence naming the SHAPE of the answer (the named framework — coined here, defined in Beat 3).
- A 3-5 item bullet list of what the reader will walk away with. The bullets are concrete deliverables, not topics.
- One sentence on WHO this is for (the audience, by problem-shape, not persona-label).
- One sentence on who it is NOT for (so the wrong reader self-excludes).

Example:

> *The article you are reading is a framework for senior engineers thinking about leaving permanent corporate employment for an independent product or service business — without making the leap an all-or-nothing bet. The Reversible Pivot is a five-stage path with numerical entry triggers, a written exit clause, and a built-in plan to walk back into salary employment without scars on your résumé. By the end you will have:*
> - *A capacity model that turns "should I go solo?" into a single number you can compute on a Sunday afternoon.*
> - *Five entry triggers — one per stage — that say "yes, advance" or "no, hold" in cash, not in feeling.*
> - *A written reversal clause: the exact text you sign with yourself, your partner, or your accountability buddy that lets you walk back without identity damage.*
> - *Six named real cases (Patrick McKenzie, Sahil Lavingia, Pieter Levels, Tony Dinh, Karri Saarinen, Tuomas Artman) on what worked, what didn't, and which paths generalise.*
> - *A 25-minute task you can complete tonight that turns the framework into a file on your disk.*
>
> *This article is for senior engineers — five or more years in — who are at or past the median salary band in their market. It is NOT for first-job engineers, for non-technical founders without a salaried fallback, or for anyone who has already left salary employment for more than 12 months.*

Rules for the TLDR setup:
- 3-5 deliverable bullets, each a CONCRETE artifact or skill, not a topic.
- Names of the 4-7 real people who appear in the article (so the reader can pattern-match before committing).
- "For… NOT for…" disqualification (it's a confidence signal, not a filter).
- The named framework appears here ONCE. The full definition still lands in Beat 3.
- No "in this article" filler. The article BEGINS here, not is described here.

After the TLDR setup, the in-medias-res Beat 1 (Story Circle "You" beat) starts. The pain-hook + TLDR setup adds ~150-230 words to the free chunk, factor that into the paywall split.

## Translation cultural adaptation (TOP-LEVEL RULE for translators)

Translators have explicit licence to adapt text AND headings to the cultural context of native speakers — beyond hero adaptation. The English source is the canonical SOURCE for the thesis and the framework; the target-language article is the canonical EDITION for the target reader. The thesis stays, the framework stays, the receipts (named real people + dates + $-amounts + places) stay verbatim — but everything around them can be localised.

### What translators MAY adapt

1. **Headings (H2/H3)** — translate to a phrase a target-language reader would actually search. UA: "Стадія 2 — Перехідний раннвей: вікно перекриття зарплати" is fine; a literal calque "Stage 2 — Transition Runway" is allowed but not required. The named-framework stage names (e.g., "Stealth-Validation", "Half-Step", "Full-Solo") may stay English-coined OR be translated per the per-language rules.
2. **Local-context examples** — where the English source uses a US-only example that's confusing to the target audience (US tax forms, US tech-ladder titles, US visa rules), the translator MAY add a parenthetical or short bridging sentence with a target-language equivalent: "$250K Total Compensation (≈ €230K у Європі / ₹2 crore в Індії / ₴10M в Україні — для сеньйор-інженерів у дорогих ринках)". Add, don't replace.
3. **Audience-language phrasing** — where the English uses an idiom or phrasing that doesn't carry in the target language, replace with the closest target-language idiom that carries the same load (per `language-rules/<lang>.md`).
4. **Cultural references** — where the English uses a US-only cultural marker that's load-bearing (a movie reference, a sports metaphor, a political moment), translators can swap for a target-language equivalent that lands the same point. Don't strip the reference; replace it with one that works.
5. **Quoted dialog tone** — if dialogue in the English source uses US-tech-bro register and the target language has no equivalent, translators can adjust the register to land the same emotional weight in the target. The character and the named person stay; the voicing localises.
6. **Pain-hook Paragraph A** — the sensory scene in the pain-hook is rewritable for the target audience. Slack pings still translate. But a target-audience-specific scene (e.g., for an Indian engineer the scene might be 1am because they're on a global team) is permitted if it lands the same recognition for that reader.
7. **TLDR setup audience qualification** — "for senior engineers — 5+ years in" stays. "At or past median salary in their market" — translator may anchor with a target-market salary band: "at or past ₹35L/yr in India / €70K in EU / ₴2M in Ukraine senior bands".
8. **FAQ questions** — the questions are queries readers would type into target-language search. Translators rephrase to match how the target audience actually queries (verify against the keywords.md audience-register phrases per language).

### What translators MUST NOT adapt

1. **The thesis** — the article still defends the same claim. Reversible Pivot stays as a framework whose 5 stages have the same structure and the same numerical entry/exit triggers.
2. **The named framework** — "The Reversible Pivot" carries either as English-with-target-language-parenthetical, OR as a fully translated coinage, per per-language rules. But its definition is identical across languages.
3. **Receipts** — Patrick McKenzie / Sahil Lavingia / Pieter Levels / Tony Dinh + their named products + dates + $-amounts + places stay verbatim. The receipt density is the article's credibility contract. Adding LOCAL named examples alongside is fine (e.g., a UA translator may add a named Ukrainian founder as a parallel case — but only if the case is verifiable and the addition is documented in the translator's report).
4. **Methodology references** (PromptCallouts) — the `/faion <natural language prompt>` invocations stay structurally identical; the prompt body translates per the existing hero-adaptation rule.
5. **Numerical claims** — "$4,200 MRR plateau", "$172,800 runway", "18 months", "6 senior engineers" — these are evidence anchors. They stay.

### Reporting cultural adaptations

In the translator's report, include a section "CULTURAL ADAPTATIONS" with:
- List of headings translated freely (vs literal calque).
- List of local-context bridges added (parentheticals, short sentences with target-market anchors).
- List of cultural references swapped (with English original + target replacement + reasoning).
- List of LOCAL named examples added (if any), with verifiable source for each.
- Confirmation that thesis / framework / receipts / methodology references stay unchanged.

The translation reviewer audits these adaptations for: (a) thesis preservation, (b) receipt verbatim status, (c) local-example verifiability, (d) cultural reference equivalence (the swap actually lands the same point in the target culture).

## The 2-20 attention ladder (TOP-LEVEL RULE)

Before any layer below kicks in, the piece must survive the 2-20 ladder. Each rung earns the right to the next; fail any one and the rest of the article is dead air for that reader.

| Rung | Surface | Window | What MUST land |
|------|---------|--------|----------------|
| **2 seconds** | Hero: title + description (frontmatter) + above-fold first 2 sentences | Reader scanning a feed / search result / shared link | A concrete problem the reader RECOGNISES AS THEIRS, in their own vocabulary. Not the persona snapshot. Not the framework name. Not US-tax jargon. The PAIN or the PROMISE. |
| **20 seconds** | Opening scene + first paragraph + the lede that follows | Reader has clicked, given you ~20 seconds before they bounce | A named character in a real moment + the stakes. The reader sees a person doing something specific, not abstract setup. They get one specific thing they didn't know before. |
| **2 minutes** | Beats 1-2 (You + Need) + first crystallisation of the problem-framing | Reader is committed-curious; will skim ahead if you don't deliver | The PROBLEM stated clearly in the reader's frame. The promise of the SHAPE of the answer (NOT the answer). They should be able to verbalise "this article is about X, and X is mine." |
| **20 minutes** | Beats 3-5 (Go + Search + Find — named framework + teaching middle + crystallisation) | Reader is now reading, not scanning; the bulk of the work happens here | The framework lands. The mechanics deliver. The reader gets enough payload to act on, even if they bounce before Take/Return. By minute 2 they must be locked in for the rest. |

### How to apply 2-20 to the hero

The hero is the most-read 50 words of the entire piece. Treat it as the most-edited 50 words. **Audit each one against the 2-second rung:**

1. **Vocabulary opacity**: would a target-language reader who is NOT in the US tech ladder know what every word means without lookup? US-specific tax/legal/comp jargon (W2, 1099, Senior-IC, Staff/Principal, TC, RSU-cliff, put-option, 401(k), Treasury ladder, COBRA, S-Corp) is allowed INSIDE the article body where context teaches it, but **forbidden in the hero unless contextualised in the same breath**. If your hero says "leave the W2", the description must immediately say what that means in target-audience terms.
2. **Persona-snapshot trap**: a hero that lists numbers ($250K TC, 11pm, Indie Hackers) is a US-FAANG-engineer-only signal. Most target-language readers are NOT that persona. The hero must lead with the PROBLEM or PROMISE, then earn the persona-detail as supporting receipt — not the other way round.
3. **Promise weight**: at least one half-sentence of the description must be a forward-leaning promise the reader can imagine getting from the read ("a five-stage framework with numerical exits + a written reversal clause so you can leave AND come back without CV scars"). Without the promise, the hero is descriptive but inert.
4. **Translator authority**: the translator OWNS the hook for their reader. Hero adaptation across languages is NOT verbatim receipt-preservation — it's audience-adapted reframing. The English hero is the canonical SOURCE meaning; the translation hero is the canonical TARGET-AUDIENCE hook. Receipt-preservation rule applies to body anecdotes, not the hero.

### How to apply 2-20 across the body

- **Opening scene (20-second rung)**: word 1 = mid-action with a named real person. Specific place + date + dollar amount within the first paragraph. No setup, no exposition, no "in today's world".
- **Nut graf (2-minute rung)**: by word 800. One paragraph that frames the entire piece in the reader's own terms. Promises the SHAPE of the journey, not the endpoint.
- **First crystallisation (2-minute → 20-minute hinge)**: by minute 2 (~roughly word 1200-1400) the framework must be NAMED and the reader must see ONE concrete mechanic that hints at the payload. Not the full reveal — but a tangible "here's the kind of thing this piece delivers".
- **Locked-in by minute 4 (~word 2400)**: by the end of the free chunk (beat 3 / Go) the reader has had a complete, valuable thought that stands alone. If they bounce here, they got value. If they continue, they're locked.

The 2-20 ladder is enforced by writer, editor, AND reviewers. Hero opacity is a MUST-FIX, never a should-fix.



1. **Narrative spine** — Dan Harmon's Story Circle (8 beats). Reader is protagonist.
2. **Argument architecture** — Stratechery style: name the thesis as a framework, evidence pillars, named counter-arguments.
3. **Texture** — Long-form journalism: in medias res opening, nut graf, one recurring character as spine, exposition inside scenes.
4. **Voice + density** — Patio11-relentless (default) or Graham-aphoristic (rare, voice-driven). Structural pull every 800 words.
5. **Pedagogy** — Worked example + isomorphic exercise per concept. Active-recall prompts at section ends. One forced binary decision. One 24-hour next action.

Each layer is non-optional. The piece without spine reads as listicle. Without architecture reads as memoir. Without texture reads as outline. Without voice/density reads as textbook. Without pedagogy doesn't change the reader's behaviour.

## Layer 1 — Story Circle spine (8 beats)

The reader's journey. Target weights for a 15K-word piece:

| # | Beat | Function | Words | Free or Gated |
|---|------|----------|-------|---------------|
| 1 | You | Reader's current state — open in medias res with a real moment | 600-900 | Free |
| 2 | Need | Surface the pull + the obstacle | 500-700 | Free |
| 3 | Go | Cross into unfamiliar territory. NAME the framework, but don't reveal the endpoint | 800-1100 | Free (end of free chunk) |
| 4 | Search | The teaching middle. Phases / mechanics / case studies / math | 4500-5500 | Gated |
| 5 | Find | The framework crystallises. Reader sees the path. Lands at ~60% (word ~9000 of 15000) | 1500-2000 | Gated |
| 6 | Take | The price. What this costs. Author's own scars. Skipping this kills the piece. | 1500-2200 | Gated |
| 7 | Return | Bring the lesson home. Concrete 24-hour next action. | 1200-1500 | Gated |
| 8 | Change | The post-decision identity. Forward-leaning prediction, not recap. | 600-900 | Gated |

**Total**: 12,200-14,800 baseline. Add 1-2K of receipts (tables, dialog, code, screenshots-described-in-prose) → 14-17K target.

**The midpoint rule**: "Find" lands at ~60%, NOT 50%. Landing it at 50% signals END; readers bail before Take/Return/Change.

**The premature reveal pitfall**: do NOT state the thesis cleanly in beat 3 (Go). Promise the SHAPE of the journey, not the endpoint. If reader sees the conclusion in beat 3, beats 4-6 read as filler.

## Layer 2 — Stratechery argument architecture

Inside the Story Circle spine, the argument is built Stratechery-style.

- **Coin the thesis as a NAMED framework.** "Reversible Pivot Doctrine" / "Five-Phase Bridge" / "The Take-Return Compression". The coinage IS the deliverable. Don't argue for it; name it, then show what it explains.
- **3-5 evidence pillars** under the thesis. Each pillar carries its own mini-arc: claim → data → analogy → counter-example → reframe.
- **Counter-arguments volunteered by NAME** (not strawmanned). "Pieter Levels would tell you to just leap. Here's why his case doesn't generalise."
- **Closing = forward-leaning prediction OR diagnostic question.** Never "in conclusion".

Anti-pattern: confident essays built on a sample of one. Each pillar needs at least 2 named public cases or it's not a pillar.

## Layer 3 — Long-form journalism texture

The reading experience comes from journalism's toolkit.

- **In medias res opening.** Word 1 is mid-action. Forbidden openers: "in today's world", "if you're a senior engineer thinking about", "many developers face", "we live in a time".
- **Nut graf by word 800.** The 5-sentence paragraph that frames the entire piece. WRITE IT LAST — drafting it first produces sideways argument.
- **One recurring CHARACTER as spine.** Pick ONE founder whose story you return to 5-6 times across the piece. Not a roster of citations.
- **Exposition INSIDE scenes**, not between. Interpolate analysis mid-action.
- **2 threads max, braided.** Primary character + 1 secondary thread. Don't sprawl to 6 case studies.

Anti-pattern: New Yorker scene-craft over-applied to indie-tech audience reads as overdressed. McPhee invisibility test: if a scene or sensory detail can be deleted without weakening the argument, it's costume. Cut it.

## Layer 4 — Voice + density

Pick ONE temperament and commit. Don't blend.

### Graham-aphoristic (rare)

- Every paragraph survives standalone.
- Thesis recovered cumulatively.
- Use only when voice is once-per-decade-distinctive.
- Default to NOT this. Most writers can't pull it off.

### Patio11-relentless (default)

- One big thesis with relentless detail.
- Structural pull every ~800 words: bold-faced thesis line, table, dialogue, code, prompt-callout, decision tree.
- If you can't justify 800 words without a structural break, you're padding.

For ultimate-guide longreads: default to Patio11-relentless. Senior-IC audience wants mechanics, not aphorisms.

### Receipts-as-argument

Indie-tech reader converts skepticism into trust ONLY when shown receipts. Required throughout:

- Real numbers ($4,387 — not "high"; 47% — not "many").
- Real names (Patrick McKenzie at Stripe, October 2010 — not "a senior engineer at a startup").
- Real dates (2024-09-15 — not "recently").
- Real places (the Bay Area / Vietnam / Lisbon — not "lower-cost geography").
- Real dollar amounts (Tony Dinh's $600 MRR at month 6 — not "small initial revenue").

**Single most important rule of the entire guide**: every personal anecdote contains **name + date + place + $ amount** — minimum 3 of 4. Fail this test → no voice polish rescues the piece.

## Layer 5 — Pedagogy density spec

For a 15K-word piece:

- **10-12 worked examples** (1 per ~1200-1500 words).
- **8-10 visuals** (tables, decision trees, diagrams described in prose, code blocks, prompt-callouts) — 1 per major section.
- **10-12 isomorphic exercises**: after each worked example, hand the reader a prompt-callout to "run it on your own numbers".
- **1 named framework**, repeated 4-6 times across the piece.
- **1 forced binary decision** somewhere in Find or Take. The reader makes a call on their actual situation.
- **1 24-hour next action** in Return. One specific action within 24 hours of reading.
- **Active-recall prompt at end of each major section** (replaces summary recap): "Before you continue, name the one decision rule from this section." Never a recap closing.

Write the spine for **intermediates, not experts**. Intermediates remember more — still building schema.

## Prompt-callouts (replaces `faion get-content <slug>`)

Articles NEVER cite methodologies by slug. Reader invokes through natural-language prompts they paste into Claude Code or Codex. The `/faion` umbrella skill resolves the prompt to the right methodology. Slug stays hidden.

### MDX format

```mdx
<PromptCallout target="claude-code">
/faion давай прорахуємо мій runway: ощадження $50K, поточний burn $4K/міс, MRR $800
</PromptCallout>
```

Renders as a code-block-styled prompt with a copy button. Reader pastes into their Claude Code or Codex session.

### Targets

- `claude-code` — Claude Code prompt
- `codex` — Codex prompt
- `cli` — direct `faion` CLI invocation (uses ephemeral hash, not slug)

### Article writing rule

**Every methodology invocation = a prompt-callout, not a slug.** The reader never sees the slug. The prompt is in the target language (UA reader sees Ukrainian prompt; pt reader sees Portuguese prompt — translators rewrite the prompt text, not just preserve it).

### Placement rule

Prompt-callouts live INSIDE the relevant Story Circle beat, at the point where the reader would naturally want to act. Not in a sidebar. Not at the end. Inline at the natural moment.

## Lists discipline (SEO + LLM density)

Bullet and numbered lists serve THREE roles in an ultimate-guide longread, and they're MANDATORY in those roles. They are FORBIDDEN in the AI-tell-flagged role of "bullet lists for things that should be prose" (long discursive text broken into one-sentence bullets).

### Required-list patterns (use ≥6 of these across the article)

1. **TLDR deliverables list** (Paragraph B of intro) — 3-5 concrete artifacts the reader walks away with.
2. **Audience qualification list** (intro) — "for X… NOT for Y".
3. **Cast-of-characters list** — at first introduction of multiple real people in one beat, list each with one-line bio.
4. **Stage / phase list** — when the named framework has N enumerated stages, present them ONCE as a numbered list with one-line definitions (Beat 3 or 4).
5. **Checklist** — entry criteria, exit criteria, or "12 things people miss" gathered as a numbered checklist with verb-led items.
6. **Comparison table** — when comparing 3+ options (this is NOT a list but follows the same enumerable-data rule).
7. **FAQ block** — at the end of the article OR at the end of the free chunk, a 4-7 question Q&A block where each question is a real query a reader would type and each answer is 40-100 words. (Q&A blocks are the single highest-impact LLM-optimization move.)
8. **Decision rules** — "if X, do Y; if Z, do W" as a numbered list, not as prose.

### Forbidden list-patterns

- A wall of 12 bullets where each bullet is a full paragraph (means the prose should be prose).
- A list of 3-4 sentences with no concrete items (means it's filler dressed as structure).
- Nested 3+ levels deep (means the hierarchy is broken).
- Lists where every item starts with the same auto-generated phrasing ("First, X. Second, Y. Third, Z.").

### Anchor rule for SEO

Every H2 and H3 heading should be expressible as a phrase a reader would type into a search box. Not anodyne ("Stage 2") but specific ("Stage 2 — Transition Runway: the salary-overlap window"). Headings double as a TOC and as Google's understanding of the article — make them legible to both.

## SEO + LLM optimization (semantic core + GEO best practices)

Articles are read by humans AND by LLM crawlers (Google's SGE, ChatGPT browsing, Perplexity, Claude search). The free chunk (everything pre-paywall, ~30%) is the indexable, citable surface. Optimization happens during Phase 2.0 (a dedicated keyword-research subagent) and is enforced by the writer + editor + reviewer.

### Phase 2.0 — Semantic core + keyword research

Before the editorial brief is finalised, a research subagent produces `keywords.md` containing:

- **Primary keyword phrase** (1-2 words, head term, the URL slug should match).
- **5-8 secondary keywords** (long-tail variants the article should rank for — e.g., "senior engineer leaving corporate", "indie hacker exit framework", "leaving salary employment safely").
- **15-30 LSI / semantically-related terms** (concepts the article should mention naturally to demonstrate semantic completeness — e.g., "runway", "burn rate", "MRR plateau", "vesting cliff", "trigger contract", "reversibility").
- **3-5 entity references** (named people / brands / methodologies — these double as anti-AI-tell receipts AND as schema.org entity anchors).
- **2-3 named related queries** (questions the article should explicitly answer in an FAQ block).
- **Audience-language register** — exact phrases the target audience uses (from forums, podcasts) so the article reads as native, not as marketing.

The writer + editor weave the primary keyword into the title, description, first paragraph, first H2, and ~3-5 times naturally in the free-chunk body. Secondary keywords land in H2/H3 headings and across the body. LSI terms are scattered naturally — no keyword stuffing.

### LLM / GEO (Generative Engine Optimization) discipline

LLMs cite articles that are easy to extract claims from. Six rules:

1. **TLDR-at-top** (the intro TLDR setup paragraph IS this) — LLMs ingest the first 300-500 words for the answer-shape.
2. **Hierarchical H2/H3 with semantic intent** — headings tell the LLM "this section is about X" so it can route a sub-query to the right span.
3. **Explicit attributable claims** — "Patrick McKenzie sold Appointment Reminder in March 2016 for an undisclosed amount" beats "the founder sold his product a while ago". LLMs cite verifiable claims with named entities and dates.
4. **FAQ / Q&A block** — explicit Q&A is the single highest-leverage LLM move. Place ONE 4-7 question block at the end of the free chunk OR end of the article, with questions phrased as real queries a reader would type.
5. **Structured data (JSON-LD)** — Article schema is in the page Head; add `FAQPage` schema for the FAQ block and `HowTo` schema if the article has a clear numbered procedure.
6. **Disambiguation on first mention** — every named entity (person, brand, methodology) introduced with a clause that disambiguates it from other entities with the same name. "Patrick McKenzie (Stripe Atlas)" beats "Patrick McKenzie" because there are multiple McKenzies in tech.

The `keywords.md` artifact ships alongside the brief and is referenced by writer + editor + reviewer audits.

## Paywall split (free 30% / gated 70%)

MDX contract:

```mdx
<!-- ... beats You / Need / Go (~30%, ~4500 words) ... -->

<PaywallGate tier="solo">
<!-- ... beats Search / Find / Take / Return / Change (~70%, ~10500 words) ... -->
</PaywallGate>
```

The free portion MUST stand alone — read complete on its own, leave reader wanting more. Not a cliffhanger trick — a genuine self-contained chunk that's valuable even if reader doesn't subscribe.

Default tier: `solo` for most ultimate-guide content. `geek` for advanced / niche material.

## Anti-AI-tell — 20 forbidden moves

Every paragraph audited against:

1. "Not just X — it's Y" pivot.
2. Tricolons everywhere ("X, Y, and Z" pattern overuse).
3. Em-dash overload (>2 per paragraph).
4. "In other words" + restate.
5. Empty intensifiers: deeply, incredibly, absolutely.
6. Hedging while pretending to be direct ("perhaps, even, one might argue").
7. Symmetric balanced paragraphs (everything 3 sentences, 4 lines).
8. Section-ending summary sentences.
9. "Let's dive in / unpack / explore".
10. Faux-personal anecdotes without name/date/$ amount.
11. Sentence-length monoculture in the 14-22 word band.
12. Textbook paragraph rigidity (topic sentence → 3 supporting → wrap).
13. Bullet lists for things that should be prose.
14. Subheaders every 200 words.
15. "First / Second / Third / Finally" overuse.
16. 3-pillar / 4-corner / 5-step decorative frameworks.
17. Symmetry between sections (equal depth everywhere).
18. "In conclusion" / "To summarise" closers.
19. Banned vocabulary: **delve, tapestry, landscape, realm, navigate (as in 'navigating challenges'), robust, leverage-as-verb**.
20. Anodyne titles ("The Ultimate Guide to X").

## Anti-AI-tell — 15 mandatory human signatures

1. **Verifiable specificity** in every anecdote: name + date + place + $ amount (≥3 of 4).
2. **Asymmetric paragraphs** — dense blocks alternating with one-line punches.
3. **Sentence-length variance**. Fragments. Long sentences that earn their length through compound clauses each doing real work. Mix.
4. **Genuine self-correction or wrestled counter-argument left visible.**
5. **Register breaks earned by context** — fragment, slang, register-drop where warranted.
6. **Specific numbers that feel chosen** (37%, not 35%; $4,387, not $4,000).
7. **References to obscure shared knowledge** — HN thread shorthand, era markers, in-jokes the target audience catches.
8. **Idiosyncratic formatting choices** the author would defend (line breaks in unusual places, italics on a single word, a code block to make a point).
9. **Topic drift inside paragraphs** that comes back. Loops, not lines.
10. **Direct address to reader by actual context** ("if you're at $2K MRR with two months runway"), not "you, dear reader".
11. **Closing sentence CLAIMS, ASKS, or JUDGES** — never recaps.
12. **Numbered framework appears ONCE in skeleton, then disappears** — the prose carries it forward; the numbers don't drum.
13. **Profanity** when the surrounding measured prose has earned it.
14. **Genuine doubt left visible** in 2-3 places ("I don't know if this generalises beyond US tax brackets, but…").
15. **The one-line punch paragraph** at least 5 times across the piece.

## Voice contract

Confident. Opinionated. Sharp. The reader paid for a perspective, not a survey. Same NERO-adjacent voice as before but now backed by structural commitments.

### Banned phrases (carry-over)

| Phrase | Why banned |
|--------|-----------|
| "in today's fast-paced world" | empty opener |
| "let's dive in" / "let's explore" | filler |
| "in this article we'll" | meta narration |
| "as we'll see" | meta narration |
| "great question" | sycophant |
| "leverage" (verb) | hollow corporate |
| "actionable insights" | hollow corporate |
| "ever-evolving landscape" | filler |
| "industry-leading" / "best-in-class" | hollow superlative |
| "synergy" / "ecosystem play" | LinkedIn |
| "10x your X" | overused hype |
| "the ultimate guide to" (as title) | empty — use specific titles |
| "step-by-step guide" (as title) | empty — describe the goal |
| "you might want to consider" | hedge |
| "various" / "things" / "stuff" | non-specific |
| "in conclusion" / "to summarise" | closing is the closing |

## Glossary terms (MANDATORY)

Unchanged from previous guide. Every glossary-mapped term wraps in `<GlossaryTerm slug="X">display</GlossaryTerm>`. First mention expanded for acronyms. Display text consistent within article AND across articles (per language).

```mdx
<GlossaryTerm slug="mrr">monthly recurring revenue (MRR)</GlossaryTerm>
```

See `~/workspace/projects/faion-net/faion-net-fe/content/glossary/` for the 151-entry corpus. Use `ls -1 content/glossary/ | grep .mdx | sed 's/.mdx$//'` to dump available slugs.

## Methodology citations

DEPRECATED: `faion get-content <slug>` callouts.
NEW (mandatory): prompt-callouts (see § Prompt-callouts above). The reader never sees the slug.

## Frontmatter shape (ultimate-guide article)

```yaml
---
slug: <kebab-case>
title: "<title>"
description: "<140-160 chars>"
pillar: SDD | Economics | Engineering | Distribution | Stack | Other
language: en
status: draft | ready-to-translate | translated | polished | published
created: "<YYYY-MM-DD>"
brief_ref: <relative path>
methodology_hooks: [<slug>, ...]  # internal — for editor/reviewer tracing only; NOT cited in article body
character_spine_primary: <name>    # the recurring character
character_spine_secondary: <name>  # optional 1 secondary
named_framework: <coinage>          # the Stratechery-named thesis
free_chunk_word_count: <int>        # for paywall split
paywall_tier: solo | pro | geek | ultimate
est_read_time_minutes: <int>
word_count: <int>
---
```

## Length

| Type | Target | Range |
|------|--------|-------|
| Ultimate-guide longread | 15000 | 12000-17000 |
| Engineering / SDD short-form (legacy) | 2500 | 1800-4000 |

Use the longread spec unless brief explicitly says otherwise. Default to longread.

## Anti-patterns checklist (writer / editor / reviewer)

- [ ] File extension is `.mdx`.
- [ ] In medias res opening (word 1 = mid-action).
- [ ] Nut graf landed by word 800.
- [ ] One named character spine, returned to 5-6 times.
- [ ] Story Circle 8-beat structure with named framework in Go and crystallisation in Find.
- [ ] Find lands at ~60% of word count.
- [ ] Take section pays the price (author's own scars / what this costs).
- [ ] 1 forced binary decision in Find or Take.
- [ ] 1 24-hour next action in Return.
- [ ] Closing claims/asks/judges; no "in conclusion".
- [ ] Density: 10+ worked examples, 8+ visuals, 10+ isomorphic exercises, active-recall (not recap) section endings.
- [ ] Every anecdote contains name + date + place + $ amount (≥3 of 4).
- [ ] Voice: Patio11-relentless OR Graham-aphoristic (one or the other, not blended).
- [ ] Methodology citations are prompt-callouts (`<PromptCallout>...</PromptCallout>`), NOT slug citations.
- [ ] Paywall `<PaywallGate>` splits at ~30% (end of beat 3 / Go).
- [ ] Free portion stands alone — valuable without subscription.
- [ ] Glossary terms wrapped (`<GlossaryTerm>...`), consistent within and across articles.
- [ ] No banned phrases (see list).
- [ ] No 20 AI tells (see anti-AI-tell list).
- [ ] At least 5 one-line punches in the piece.
- [ ] At least 2 wrestled-counter-arguments left visible.
- [ ] No emojis.
- [ ] Word count 12K-17K.
