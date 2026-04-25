# Agent Integration — Regulatory Compliance 2026

## When to use
- Pre-launch a11y audit for a US/EU public-facing site or app (post-ADA April 2026 / EAA June 2025).
- Drafting an accessibility statement and conformance documentation per WCAG 2.1/2.2 AA.
- Mapping product surface area (web, native, kiosk, e-book) to specific regulations (ADA Title II, EAA, AODA, Section 508).
- Quarterly/annual a11y audit cycle planning + remediation backlog.

## When NOT to use
- Implementation-level a11y fixes — see `accessibility-evaluation`, `wcag-22-compliance`, `testing-with-assistive-technology`.
- Privacy/data regulation (GDPR, CCPA, HIPAA) — different methodology.
- Pure design tokens / visual contrast — covered in `accessibility-first-design`.

## Where it fails / limitations
- Regulations are jurisdictional; this methodology gives a US/EU snapshot but ignores UK Equality Act, Japanese JIS X 8341, Australian DDA, etc.
- The compliance checklist is necessary but not sufficient — passes don't preclude lawsuits.
- WCAG 2.1 AA is a floor; some agencies (US federal contracts, EU public sector) require 2.2 AA or AAA in places.
- "Statement published" can be a false-comfort metric — wrong claims of conformance increase legal exposure.
- Automated checkers catch only 30-40% of WCAG issues; human + AT testing required.

## Agentic workflow
Drive Claude to inventory product surfaces (sites, apps, e-books, kiosks), map each to applicable regulations, and produce a remediation backlog ordered by deadline + risk. A second agent runs axe-core / pa11y / Lighthouse against staging URLs and merges results into the backlog. A legal-review checkpoint validates the accessibility statement language before publication.

### Recommended subagents
- `faion-accessibility-specialist-agent` (or generic) — translate regulation requirements into testable acceptance criteria.
- `faion-ux-researcher-agent` — plan AT user testing panels (screen reader, switch, magnifier, voice).
- A custom `compliance-mapper` — given product manifest + regulations, output applicability matrix + deadlines.

### Prompt pattern
```
Given <product surfaces JSON> and <region list>, output:
- Regulation applicability matrix (surface × regulation).
- WCAG version + level required per cell.
- Earliest deadline + responsible team.
- Top 5 a11y risks per surface.
```

```
Given <axe JSON output> + <regulation map>, generate
remediation tickets sorted by (regulation severity × user impact).
Each ticket: WCAG SC, surface, repro steps, suggested fix, deadline.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` (CLI / `@axe-core/cli`) | Automated WCAG 2.1/2.2 checks | `npm i -g @axe-core/cli` |
| `pa11y` / `pa11y-ci` | Batch URL audits in CI | `npm i -g pa11y-ci` |
| `lighthouse` | Includes a11y category, JSON output | `npm i -g lighthouse` |
| `accessibility-insights-cli` | Microsoft AC tooling, FastPass | accessibilityinsights.io |
| `arc-toolkit` (TPGi) | Manual + automated, exportable | tpgi.com |
| `nu-html-checker` (vnu) | Validate HTML which feeds a11y issues | validator.github.io |
| `linkml` / `wcag-em-tool` | Apply WCAG-EM evaluation methodology | wcag-em-report-tool |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Deque axe DevTools | SaaS + OSS | Yes (REST/Lib) | Industry standard; CI integrations |
| Siteimprove | SaaS | Yes (REST) | Crawl-based monitoring; statement generator |
| Level Access | SaaS | Partial | Enterprise; legal-review-grade reports |
| Tenon.io | SaaS | Yes (REST) | Single-page or batch URL checks |
| WAVE (WebAIM) | SaaS | Limited | Free; manual UI; useful for spot checks |
| AudioEye | SaaS | No | Overlay vendor; treat with caution — overlays often increase legal risk |
| UserWay | SaaS | No | Same caveat as AudioEye |
| Fable | SaaS | Partial | Recruit AT users for moderated testing |
| Applause Accessibility | SaaS | Partial | Crowd of disabled testers |

## Templates & scripts
See `templates.md` for accessibility statement template. Inline pa11y-ci CI runner (≤50 lines):

```bash
#!/usr/bin/env bash
set -euo pipefail
URLS=( "https://example.com/" "https://example.com/checkout" "https://example.com/account" )
THRESHOLD=0   # zero allowed errors at 2.1 AA before launch
TOTAL=0
for url in "${URLS[@]}"; do
  out=$(pa11y --standard WCAG2AA --reporter json "$url" || true)
  count=$(jq 'length' <<<"$out")
  echo "::group::$url ($count issues)"
  jq -r '.[] | "\(.code)  \(.selector)  \(.message)"' <<<"$out"
  echo "::endgroup::"
  TOTAL=$((TOTAL + count))
done
echo "TOTAL=$TOTAL"
[ "$TOTAL" -le "$THRESHOLD" ]
```

## Best practices
- Treat WCAG 2.2 AA as the design baseline even where 2.1 is the legal minimum — gap-closing later is more expensive.
- Publish a dated accessibility statement linking to a feedback channel; courts and regulators view absence as bad faith.
- Document the testing methodology (manual + automated + AT users) — "we ran axe" is not a defense.
- Schedule audits at least annually; flag every major release for an incremental audit.
- Avoid overlay widgets that "auto-fix" a11y; they have lost cases in US courts.
- Train content authors — most violations enter via CMS, not engineering.

## AI-agent gotchas
- LLMs paraphrase WCAG success criteria inaccurately — quote the spec, don't summarize.
- "WCAG 2.1 AA" vs. "EN 301 549" overlap heavily but diverge on hardware/IT — agents conflate them. Always check the specific regulation's referenced version.
- Auto-generated statements often claim more conformance than evidence supports — legal exposure. Human-in-loop checkpoint required: legal/compliance reviewer signs off on every public statement.
- Agents should not produce final "we are compliant" copy — only "we test against WCAG 2.1 AA and remediate" hedged language.
- ADA/EAA dates change via guidance updates — pull current dates from official sources, not the model's memory.

## References
- WCAG 2.2 — w3.org/TR/WCAG22
- ADA Title II Final Rule (DOJ, April 2024) — ada.gov/notices/2024-final-rule-title-ii
- European Accessibility Act — eur-lex.europa.eu (Directive (EU) 2019/882)
- EN 301 549 v3.2.1 — etsi.org
- Section 508 — section508.gov
- W3C Accessibility Statement Generator — w3.org/WAI/planning/statements
