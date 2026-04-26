# Agent Integration — Employee Value Proposition (EVP)

## When to use
- The company has 50+ employees and an inconsistent narrative across careers page, job descriptions, recruiter outreach, and offer letters.
- Offer-acceptance rate is dropping or candidates cite "didn't know what makes you different" in post-decline surveys.
- Annual employer brand refresh: agents can synthesize survey data, exit interviews, and competitor pages into a draft EVP statement and pillar messaging.
- Localizing or segmenting EVP for different audiences (engineering vs. sales, US vs. EU vs. LATAM).

## When NOT to use
- Pre-PMF startup (<20 people): EVP is whatever the founder says today and will change in three months — premature.
- Acute reputation crisis (layoffs, scandal): the EVP exercise will produce aspirational copy that contradicts reality and fuels Glassdoor backlash. Fix the underlying issue first.
- One-off role hiring without brand intent: a job description suffices.
- The company offers below-market compensation and refuses to address it — no narrative compensates.

## Where it fails / limitations
- LLMs default to "innovative, fast-paced, mission-driven" — generic clichés that any company could claim. Force evidence-backed claims with "proof points" tied to specific programs, budgets, or data.
- Aspirational vs. actual gap: agents synthesize what should be true from leadership talking points, not what employees experience. Mandatory cross-check against Glassdoor and exit interviews.
- Translating EVP into 30+ touchpoints (JDs, recruiter scripts, careers page, social, offer letters) is rote, but each touchpoint has channel-specific voice; one prompt rarely fits all.
- DEI claims without internal data are reputation risk; agents should never invent diversity statistics.
- EVP becomes stale; agents should set a calendar reminder for annual refresh, not produce a one-time artifact.

## Agentic workflow
A subagent ingests three input streams: employee survey CSV, competitor careers pages (scraped), and exit-interview themes (from HRIS export or anonymized notes). It synthesizes 3–5 candidate pillars, drafts an EVP statement using the methodology's template, and produces an audit table comparing claims to evidence. A second sonnet pass adapts the EVP into channel-specific copy: one-line tagline, careers-page hero, JD intro paragraph, recruiter outreach opener, offer letter section. Human review is mandatory at the pillar-selection step before any external publication.

### Recommended subagents
- `faion-employer-brand-agent` (referenced in README) — domain agent for EVP work.
- `faion-recruiter-agent` — adapts EVP into recruiter outreach and call scripts.
- A custom `evp-evidence-auditor` (sonnet) scoped to `Read` only — compares draft pillars to an internal proof-point doc and flags unsupported claims.
- `faion-marketing-manager` (knowledge skill) — for channel-specific copy adaptation (LinkedIn, careers page, video script).

### Prompt pattern
```
Given <employee-survey.csv> (importance ratings per attribute) and
<exit-interviews.md> (themes), identify the top 3-5 EVP attributes
where score > 4.0 AND mentioned positively in exits. For each, list
3 proof points (programs, budgets, data) from <internal-programs.md>.
Reject any pillar without 3 proof points.
```

```
Adapt the EVP statement <statement> into:
1) careers page hero (max 12 words)
2) JD intro paragraph (≤60 words)
3) recruiter cold outreach opener (≤30 words, no "I hope this finds you well")
4) offer letter section (≤80 words, second person).
Maintain pillar order; cite proof points inline.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `op` (1Password CLI) | Pull HRIS / survey credentials securely | https://developer.1password.com/docs/cli |
| `csvkit` | Slice survey CSVs (`csvstat`, `csvgrep`) | `pip install csvkit` |
| `pandoc` | Convert EVP brief between MD/DOCX/PDF | OS package |
| `gh` CLI | Open PR adding EVP copy to careers-page repo | https://cli.github.com |
| `playwright` (CLI) | Scrape competitor careers pages | `npm i -D @playwright/test` |
| `ffprobe` / `ffmpeg` | Extract testimony video metadata | OS package |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Culture Amp / Lattice | SaaS | Partial | Engagement and employee-survey APIs (read-only). |
| Workday / BambooHR / Rippling | SaaS HRIS | Partial | Pull tenure/comp data via APIs; gated by perms. |
| Glassdoor / Comparably / InHerSight | SaaS | Read-only | Public review pages scrape-able; APIs minimal. |
| LinkedIn Talent Insights | SaaS | Partial | Talent-pool, competitor follower data. |
| Universum / Employer Brand Index | SaaS | No | Reports are PDF; agents extract via pdf-to-text. |
| Greenhouse / Lever ATS | SaaS | Yes | Candidate-experience NPS surveys, source-of-hire data via API. |
| LinkedIn / Indeed Career Pages | SaaS | Yes | Standard JD + brand block fields; agent can post via API. |
| Canva / Figma | App | Partial | Pillar visuals; humans finalize. |

## Templates & scripts
See `templates.md` for the EVP statement template, discovery survey, and competitive analysis. Inline pillar-evidence audit:

```bash
#!/usr/bin/env bash
# evp-audit.sh - check pillar claims against proof-point doc
set -euo pipefail
PILLARS="${1:?pillars.md}"
PROOFS="${2:?proof-points.md}"
while IFS= read -r pillar; do
  count=$(grep -ic "$pillar" "$PROOFS" || true)
  printf "%-40s %s proof points\n" "$pillar" "$count"
  [[ $count -ge 3 ]] || echo "  WARN: needs 3+ proof points"
done < <(grep -E '^## Pillar' "$PILLARS" | sed 's/^## Pillar [0-9]*: //')
```

## Best practices
- Pillars must be true today, not aspirational; agents reject any claim without a named program or measurable data.
- Test EVP draft with a 5-person employee panel before external publication; write the test plan as a checklist agents can execute.
- Segment by audience but keep one master EVP — agents producing 5 contradictory taglines is a known failure mode.
- Embed EVP in every recruiting touchpoint via templates (JD opener, recruiter scripts, offer letter); audit drift quarterly.
- Tie EVP to measurable outcomes (offer-acceptance, application rate, Glassdoor rating) and revisit annually with the same survey instrument.
- Keep the EVP statement short — one sentence test: can a recruiter say it on a phone screen without reading?

## AI-agent gotchas
- Generic-claim injection: LLMs add "great culture", "smart people", "make a difference" — strip these in a post-pass.
- Unverified diversity stats are reputation risk; agents must never invent percentages. Force `<UNVERIFIED>` placeholders that humans fill from HRIS.
- Plagiarism risk when scraping competitor pages: agents lift phrasings verbatim. Run a Levenshtein check vs. competitor corpus before publication.
- LLMs over-promise on benefits ("unlimited PTO", "fully remote forever") — humans must confirm each benefit is current policy.
- Localization gotcha: direct translation of US-centric EVP ("equity") into countries where stock options are taxed at grant produces awkward offers.
- Human-in-loop checkpoint: pillar selection AND any external-facing copy. Never let an agent autopublish to careers page or LinkedIn.
- Tone drift across touchpoints: agent generates JD copy in marketing voice, recruiter script in HR voice — establish a voice guide first.
- Privacy: employee testimonial drafts must be reviewed and consented by named employees before publication; agents should produce DRAFT-only with `[NAME] [TITLE]` tokens until consent is captured.

## References
- LinkedIn Talent Solutions EVP Guide: https://business.linkedin.com/talent-solutions/resources/talent-engagement/employer-brand
- Gartner: "Redesign Your Employee Value Proposition" (Human Deal framework)
- Brett Minchington, "Employer Brand Leadership"
- AIHR: "Employee Value Proposition: All You Need to Know" — https://www.aihr.com/blog/employee-value-proposition/
- Universum Global EVP research reports (annual)
- LinkedIn "Global Talent Trends" annual report
- SHRM: "Creating an Employee Value Proposition" — https://www.shrm.org
