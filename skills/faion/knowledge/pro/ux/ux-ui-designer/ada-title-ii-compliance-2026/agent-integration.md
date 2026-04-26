# Agent Integration — ADA Title II Compliance 2026

## When to use
- US state, local, and territorial government digital services covered by 28 CFR Part 35 (DOJ final rule, April 24 2024).
- Public universities, transit, libraries, court systems, agency portals — anything a "public entity" delivers digitally.
- Vendors / SaaS supplying covered entities — your product becomes a covered web/mobile content under contract.
- Compliance deadline planning: large entities (≥50K population) by April 24 2026; smaller by April 26 2027.

## When NOT to use
- Private-sector commercial sites — Title III applies instead, often using WCAG 2.1 AA via consent decrees.
- Federal government — Section 508 / ICT Refresh applies (still WCAG 2.0 AA at time of writing, moving toward 2.1).
- Employee-facing internal tools at private employers — Title I applies (different remediation triggers).
- Marketing-only sites for non-covered entities — not in scope for Title II.

## Where it fails / limitations
- Standard pinned to WCAG 2.1 AA, not 2.2 — agents must not auto-apply 2.2 SCs as required (use as recommended).
- Archived content exemption is narrow — "archived" must be unaltered, marked, and not used for current activity.
- Pre-existing PDFs created before deadline get partial relief, but only if not used for current activity (still must be remediated on request).
- Conventional electronic documents (Word, PDF, Excel, PowerPoint) created by/for covered entity *are* in scope.
- "Undue burden" defenses are extremely narrow under Title II — far less generous than ADA Title III.
- Third-party content embedded in covered sites can still trigger compliance obligation.

## Agentic workflow
Use a subagent to inventory all digital surfaces (web pages, mobile apps, PDFs, multimedia, forms, third-party widgets) by crawling and tagging. A second agent maps each surface to a WCAG 2.1 AA gap analysis using axe-core/Pa11y plus manual checkpoints (captions, audio descriptions, accessible PDFs). A third generates the remediation roadmap and conformance documentation (VPAT 2.5 INT/RFI). Legal counsel signs off on the conformance statement and "undue burden" claims — never an agent.

### Recommended subagents
- `faion-usability-agent` — manual SC review, AT walkthroughs, multimedia accessibility audit.
- `faion-sdd-executor-agent` — applies code/ARIA/PDF tag fixes, wires CI gates.
- `faion-ux-researcher-agent` — recruits AT users for validation.

### Prompt pattern
```
Crawl <domain>, output every URL with content type
(html / pdf / video / audio / form / iframe). Flag any iframe
src outside <domain> as third-party-embedded. Group by traffic
volume from <analytics export>.
```

```
For each PDF in inventory, run pdfix-checker / pac3 / Acrobat
preflight. Output: tagged Y/N, lang attr Y/N, alt text on figures
Y/N, table headers Y/N, reading order issues count, total pages.
Sort by traffic descending.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` / `axe-core-cli` | WCAG 2.1 AA automated scan | deque.com/axe |
| `pa11y-ci` | CI-friendly site-wide scan | pa11y.org |
| `pdfix-cli` / `pac` | PDF accessibility check (PDF/UA) | pdfix.net, pac.pdf-accessibility.org |
| `ffmpeg` + `whisper.cpp` | Caption generation pipeline | ffmpeg.org, github.com/ggerganov/whisper.cpp |
| `wcag-em-report-tool` | W3C evaluation methodology report | github.com/w3c/wcag-em-report-tool |
| `lighthouse-ci` | Per-route a11y + performance | github.com/GoogleChrome/lighthouse-ci |
| `iframe-tester` (custom) | Detect and audit third-party embeds | — |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Deque axe DevTools / Auditor | SaaS+OSS | Yes — REST API, CI plugins | Industry default for state/local agencies. |
| Siteimprove | SaaS | Yes — REST | Strong inventory + tracking, popular with .gov. |
| Level Access | SaaS | Yes — REST | VPAT generation, training. |
| TPGi (ARC, JAWS Inspect) | SaaS | Yes — REST | Manual + automated; AT-vendor advantage. |
| Allyant (CommonLook) | SaaS | Yes — REST | PDF/UA remediation specialist. |
| 3Play Media / Rev | SaaS | Yes — REST | Captions, audio description, transcripts. |
| Civic Plus / Granicus | SaaS | Partial — vendor-side compliance | Required vendor a11y attestation. |

## Templates & scripts
See `templates.md` for VPAT/ACR shells. Inline gap-analysis bootstrap (Bash):

```bash
#!/usr/bin/env bash
# scan-title-ii.sh -- nightly Title II baseline
DOMAIN="$1"
OUT="reports/$(date +%F)"
mkdir -p "$OUT"
# crawl
wget --spider --recursive --level=3 --accept=html,pdf "$DOMAIN" 2>"$OUT/urls.log"
# automated WCAG 2.1 AA on HTML
pa11y-ci --sitemap "$DOMAIN/sitemap.xml" --json > "$OUT/pa11y.json"
# PDFs
grep -Eo 'https?://[^ ]+\.pdf' "$OUT/urls.log" | while read u; do
  curl -sSL "$u" -o /tmp/p.pdf
  pac /tmp/p.pdf --json >> "$OUT/pdfs.json" || true
done
# videos missing captions
grep -Eo 'https?://[^ ]+\.(mp4|webm)' "$OUT/urls.log" \
  | xargs -I{} curl -sI {} | grep -L 'caption' > "$OUT/uncaptioned-video.txt" || true
```

## Best practices
- Inventory first, fix second — you cannot remediate what you have not catalogued.
- Prioritize by traffic and by service-criticality (benefits applications, court forms, transit alerts).
- Treat third-party widgets as in-scope — get vendor VPATs and contractually require remediation.
- Build accessibility into procurement: every new SaaS must ship a current VPAT 2.5.
- Train content authors on document accessibility — most violations originate in CMS uploads.
- Maintain a public accessibility statement with feedback channel (a Title II expectation).
- Re-audit after every major content release; baseline drifts within weeks.

## AI-agent gotchas
- Agents apply WCAG 2.2 SCs and call them required — Title II rule pins to 2.1 AA. Mark 2.2 as recommended only.
- "Archived content" is narrow — agent cannot exempt content because it's old; must check the legal definition.
- PDFs flagged "tagged" by Acrobat preflight may still fail PDF/UA — use PAC 2024 / pdfix for ground truth.
- Auto-generated captions (Whisper) have ~5-15% WER — Title II requires accurate captions; mark as draft only.
- Audio description ≠ captions — agents conflate; AD requires separate narration track.
- Avoid overlay widgets; DOJ guidance is skeptical of them. Refuse to recommend overlays as remediation.
- Accessibility statement: agent should not claim "fully conformant" — use "we conform to WCAG 2.1 AA except for…" with known issues list.

## References
- DOJ Final Rule, 28 CFR Part 35 (April 24 2024) — federalregister.gov/documents/2024/04/24/2024-07758
- ADA.gov Title II web/mobile rule fact sheet — ada.gov/notices/2024/04/08/web-rule/
- WCAG 2.1 — w3.org/TR/WCAG21/
- W3C Accessibility Conformance Testing (ACT) Rules — w3.org/WAI/standards-guidelines/act/
- VPAT 2.5 (Section 508 + WCAG + EN 301 549) — itic.org/policy/accessibility/vpat
- Section508.gov ICT Testing Baseline — section508.gov/test/
- W3C WAI-ARIA Authoring Practices — w3.org/WAI/ARIA/apg/
