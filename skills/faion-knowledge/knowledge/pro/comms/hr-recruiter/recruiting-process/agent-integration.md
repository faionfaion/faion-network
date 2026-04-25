# Agent Integration — Recruiting Process

How to drive the full-cycle recruiting bundle (sourcing, screening, JD writing, persona dev, outreach, internal mobility, pipeline, metrics, ATS, AI tools, recruitment marketing, offer management) with Claude subagents and TA stack tooling. Pairs with `README.md`, `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.

## When to use

- Designing or rewriting a TA function for a 20-200 person company that has outgrown ad-hoc hiring.
- Onboarding a new TA leader who needs a defensible process baseline before measuring teams.
- Building a multi-channel sourcing engine when LinkedIn / Indeed alone has stalled the funnel.
- Standing up a passive-candidate outreach motion with clear conversion targets (25-40% response).
- Creating an ATS-native automated workflow for high-volume req types.

## When NOT to use

- Agency / executive search where the pipeline is bespoke per search and process homogenization destroys the differentiator.
- Pre-seed startups (< 10 hires/year) — process overhead exceeds throughput benefit.
- Internships / campus hiring at scale — different funnel, different timelines, different compliance regime.
- Single critical-role searches that need a retainer or executive-search firm — internal process won't outperform.

## Where it fails / limitations

- The bundle treats sourcing channels as substitutable; in practice each role family responds to specific channels (engineering ≠ sales ≠ design).
- Multi-channel sourcing scales spend faster than it scales hires; cost-per-hire trends up before it trends down.
- "Skills-based hiring" framings push agents toward dropping degree filters, but downstream calibration (interview questions, scoring rubrics) often still encodes the old proxies.
- Passive-candidate outreach response rates of 25-40% are conditional on segment + brand strength; LLM-generated benchmarks ignore both.
- ATS optimization tied to a specific platform breaks on migration; agents must abstract over a platform-agnostic interface.
- AI-recruiting-tool bias audits are non-trivial; the bundle mentions ethics but does not specify a method.
- "Talent pipeline" warm-keeping at scale falls into anti-spam, GDPR, and CCPA traps.

## Agentic workflow

Drive recruiting as a seven-stage pipeline owned by `faion-recruiter-agent`. Stage 1 (req intake, opus) — interrogates the hiring manager into a structured req: role, level, comp band, must-have / nice-to-have, success criteria. Stage 2 (JD authoring, sonnet) — produces an inclusive, scannable JD; runs through the inclusive-language linter. Stage 3 (channel mix planning, opus) — selects channels per the role family + budget. Stage 4 (outbound drafting, sonnet) — produces personalized outreach per identified prospect, with deliverability and reply-rate checks. Stage 5 (screen + scoring, sonnet) — rubric-based resume + screen note synthesis; never a hire/no-hire decision. Stage 6 (offer management, opus) — comp negotiation playbook, pulls market data; humans own the math and the commitments. Stage 7 (metrics + closure, sonnet) — funnel data, source effectiveness, candidate NPS, post-mortem.

### Recommended subagents

- `faion-recruiter-agent` — primary; owns intake → screen → offer.
- `faion-employer-brand-agent` — JDs that match brand voice, careers-page assets, recruitment marketing.
- `faion-research-agent (mode: market)` — comp benchmarks and competitor signals at offer stage.
- `faion-onboarding-agent` — clean handoff after offer-acceptance.
- `general-purpose` reviewer (sonnet, fresh context) — inclusive-language audits on JDs, outreach copy.

### Prompt pattern

Req intake interrogation:
```
You are running req intake per skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/recruiting-process/README.md.
Hiring manager input (raw): <pasted>. Ask only the missing-information questions to fill: title, level, location/remote, must-have skills (5-7), nice-to-have (3-4), top 3 success criteria at 12 months, comp band source-of-truth, panel composition, deal-breakers, scope vs adjacent roles, urgency. Output: a structured req markdown + the unanswered questions list.
```

Outbound message draft (passive candidate):
```
Compose a 100-130 word LinkedIn InMail to <prospect_name>. Reference 1 specific signal from their public profile (named project, named company, named talk). Lead with why this role is interesting for THEM, not us. CTA: a 20-min chat, not "apply". No "I came across your profile" / "I'd love to chat" filler. Forbidden: "rockstar", "ninja", "ground floor", "passionate".
```

Screen synthesis:
```
Given a candidate's resume + 30-min screen notes, score the rubric (attached) per competency on a 1-5 scale with a verbatim quote as evidence. Mark gaps. Recommend next-step focus areas. Do not output a hire/no-hire recommendation.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Greenhouse Harvest API | Full-cycle ATS automation | developers.greenhouse.io |
| Lever API v1 | Same | hire.lever.co/developer/documentation |
| Ashby API | Newer ATS with stronger structured-hiring primitives | developers.ashbyhq.com |
| Workable API | SMB-friendly | workable.readme.io |
| LinkedIn Recruiter / RSC API | Sourcing, InMail, project tracking | learn.microsoft.com/linkedin/talent |
| Gem / SeekOut API | Prospect data + outbound automation | developers.gem.com (limited public) |
| `pandas` + `dbt` + `duckdb` | Cross-source funnel warehousing | pypi, getdbt.com, duckdb.org |
| `mailgun-cli` / Postmark / Customer.io | Outbound deliverability | docs of each |
| `gh` | Version-control TA artefacts as repo | cli.github.com |
| Levels.fyi / Radford / Mercer feeds | Comp benchmarking | each provider |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Greenhouse | SaaS ATS | Yes (REST + webhooks) | Strongest structured-hiring + reporting. |
| Lever | SaaS ATS | Yes | Cleaner sourcing CRM than Greenhouse. |
| Ashby | SaaS ATS | Yes | Best agent-day-1 primitives. |
| Workable | SaaS ATS | Yes | SMB sweet spot. |
| iCIMS / Workday Recruiting / SAP SuccessFactors | SaaS ATS (enterprise) | Partial | Heavy auth + rate limits. |
| Gem | SaaS sourcing CRM | Yes | Outbound automation, pipeline nurturing. |
| SeekOut / hireEZ / Findem | SaaS AI-sourcing | Yes (REST) | Diversity filters; bias audits required. |
| LinkedIn Recruiter | SaaS | Limited (RSC only) | Industry standard; rate-limited. |
| Indeed / Glassdoor / Built In | SaaS job board | Yes (REST) | Top-of-funnel. |
| HackerRank / CodeSignal / CoderPad | SaaS | Yes | Technical screens. |
| BrightHire / Metaview / Pillar | SaaS | Yes | Interview intelligence. |
| Calendly / GoodTime / Modernloop | SaaS | Yes | Scheduling. |
| Checkr / Certn / HireRight | SaaS | Yes | Background checks; consent stays human. |
| Levels.fyi / PayScale / Radford | SaaS comp data | Partial | Some have APIs, most are scrape-only. |

## Templates & scripts

See `templates.md` for: req intake doc, JD template, persona doc, outreach sequences, scorecards, offer letter. Worked examples per role family in `examples.md`.

Inline helper — JD inclusive-language linter (run before publishing):

```python
# jd_lint.py — flag exclusionary or biased phrasing in a JD
import sys, json, re

PATTERNS = {
    "masculine_coded": r"\b(rockstar|ninja|guru|aggressive|dominant|competitive|hacker|warrior|champion)\b",
    "feminine_coded":  r"\b(nurture|support|empathetic|collaborative|interpersonal|sympathetic)\b",
    "ageist":          r"\b(digital native|young|recent grad|energetic|fresh|fast-paced young team)\b",
    "ableist":         r"\b(walk you through|stand up|see what I mean|crazy|insane|sanity check)\b",
    "exclusionary":    r"\b(culture fit|cultural fit|like family|like-minded)\b",
    "vague_must":      r"\b(\d+\+? years? of experience|degree required|must have a (BA|BS|BSc))\b",
    "filler":          r"\b(world-class|ground floor|fast-paced|wear many hats|self-starter|passionate)\b",
}

def lint(text):
    findings = []
    for name, pat in PATTERNS.items():
        for m in re.finditer(pat, text, re.I):
            findings.append({"category": name, "phrase": m.group(0), "pos": m.start()})
    return findings

if __name__ == "__main__":
    text = sys.stdin.read()
    out = lint(text)
    json.dump({"jd_chars": len(text), "findings": out, "count": len(out)},
              sys.stdout, indent=2)
```

Pipe JD text in. Block publish if `count > 0` for high-bias categories (masculine/ageist/ableist/exclusionary).

## Best practices

- Treat req intake as the highest-leverage 30 minutes of the entire process. A bad req leaks through every downstream stage.
- Define "must-have" in observable terms: shipped X, scaled Y, hired Z. Years-of-experience filters are weak proxies.
- Channel mix: weight by historical cost-per-hire and quality-of-hire by source, not by recruiter preference. Refresh quarterly.
- Outbound: 3 touches over 12 days, each with a distinct angle, then disengage. Anything more is harassment with diminishing returns.
- JDs: <= 350 words for the body; one paragraph on impact, one on what they'll do, one on must-haves, one on team/culture, one on comp/benefits.
- Keep a comp band source-of-truth doc that the agent reads — never let the LLM "estimate" market.
- Offer-stage speed dominates: every additional day from final-interview-to-offer reduces acceptance by ~2pp at senior levels.
- Source diversity slate (>= 2 underrepresented in final round) belongs in the design, not as a post-hoc audit.
- Internal mobility: post all roles internally first for >= 3 days before external. Otherwise mobility metrics decline silently.

## AI-agent gotchas

- LLM-written outreach is detectable and now carries a brand penalty in many candidate cohorts. Force a "would a human delete this filler line?" pass.
- Auto-rejection on resume parsing is a legal risk in many jurisdictions (NYC AEDT, EU AI Act). Document criteria, retain logs, never let an agent send rejection without human sign-off on the rule, not the candidate.
- AI screening tools (Eightfold, HireVue) require periodic disparate-impact audits; an agent that integrates them must record the model version + date for each screening decision.
- Agents tend to widen "nice-to-have" to "must-have" during JD writing, narrowing the pool unintentionally.
- Comp data hallucination: LLMs cite outdated numbers as current. Always pull from a versioned, dated source.
- Scheduling agents create back-to-back loops that fatigue interviewers; cap interviews-per-day per interviewer (3) at the tool layer.
- Talent-pipeline / nurture: agent-driven "stay-in-touch" emails at scale violate CAN-SPAM, CASL, GDPR if there's no opt-in. Treat warm-keep lists as marketing data, not internal CRM.
- Mandatory human-in-loop: (1) req intake sign-off, (2) any rejection sent (final-stage), (3) every offer extended, (4) any change to channel budget, (5) any AI screening tool turned on for a new role family.

## References

- LinkedIn Talent Solutions — "Future of Recruiting" annual reports.
- SHRM — "Talent Acquisition" toolkit (shrm.org).
- Lever — "Recruiting Best Practices" blog series.
- Datapeople — JD language and apply-rate effects.
- Schmidt & Hunter (1998) — selection method validity.
- NYC Local Law 144 (AEDT) — automated employment decision tools.
- EU AI Act — high-risk AI in employment (recruitment classed as high-risk).
- Internal: `skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/recruitment-funnel-optimization/agent-integration.md`.
- Internal: `skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/structured-interview-design/agent-integration.md`.
- Internal: `skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/onboarding/agent-integration.md`.
