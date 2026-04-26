# Agent Integration — ADA Title II Compliance 2026

## When to use
- US state/local government entity, public university, or contractor for these — large entities (50K+ population) deadline April 24 2026; smaller April 24 2027.
- Federal-funded program needing Section 508 + ADA Title II dual conformance.
- Vendor responding to RFP that asks for VPAT/ACR + remediation plan.
- Procurement officer evaluating third-party SaaS for accessibility risk before contract.
- Pre-litigation triage after a DOJ complaint or Title II demand letter.

## When NOT to use
- Private commercial sites unrelated to gov funding (use Title III + WCAG 2.2 AA — different standard, different case law).
- EU-only product — use European Accessibility Act (EAA, June 2025) + EN 301 549 instead.
- Internal-only tooling not used by the public — Section 504/508 may apply, not Title II web rule.
- Greenfield design — apply `accessibility-first-design` from day 1 to avoid the remediation cost altogether.

## Where it fails / limitations
- WCAG 2.1 AA is the minimum, not the ceiling — courts have accepted 2.1 conformance, but cognitive criteria added in 2.2 are not yet legally required (still recommended).
- The DOJ rule excludes some content (archived, third-party not under control, pre-effective-date unaltered) — these exceptions are commonly misapplied. Document carefully.
- "Undue burden" defense rarely succeeds at scale — must show specific resources analysis, not just "expensive".
- VPAT 2.5 ≠ proof of conformance — auditors require evidence (test reports, code samples).
- Mobile apps + PDFs are the most-litigated gaps; many entities only audit web HTML and miss them.

## Agentic workflow
Agents excel at: WCAG-criterion mapping of axe/Pa11y findings, drafting accessibility statements, generating VPAT/ACR boilerplate, building remediation roadmap from issue tracker, monitoring CI for regressions. Agents do NOT replace: legal review, real screen-reader user testing, complex video audio description writing, undue-burden analysis. Two-track pipeline: technical agent (audit + fix) + compliance agent (VPAT, statements, contract clauses).

### Recommended subagents
- `faion-sdd-executor-agent` — model each WCAG criterion gap as an SDD task with criterion ID and conformance evidence requirement.
- Compliance-doc subagent — converts audit JSON into VPAT 2.5 INT (Revised Section 508 + WCAG 2.1) markdown.
- Procurement subagent — extracts a11y clauses from a vendor's VPAT, flags non-conformant criteria.
- See also: `a11y-testing/agent-integration.md` (technical scan side) and `wcag-22-compliance` (criterion details).

### Prompt pattern
```
You are an ADA Title II compliance agent. Given the audit JSON
(axe + Pa11y + manual screen-reader notes), produce:
  1) WCAG 2.1 AA conformance table (Supports / Partially / Does Not / N/A) per criterion.
  2) Remediation roadmap: Critical (immediate) / High (3mo) / Med (6mo) / Low (12mo).
  3) Draft accessibility statement using DOJ-aligned template.
Cite the WCAG criterion number for every entry. Never assert "Supports" for
a criterion not directly tested.
```

```
Review this vendor VPAT 2.5 for procurement. List criteria marked "Does Not
Support" or "Partially Supports", their user impact, and required contract
clauses (remediation timeline, escrow, periodic reaudit).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `@axe-core/cli` | WCAG 2.1/2.2 AA scanner | `npm i -g @axe-core/cli` |
| `pa11y-ci` | Sitemap-driven scan with thresholds | `npm i -g pa11y-ci` |
| `lighthouse` | Auditing per page | `npm i -g lighthouse` |
| `pdfix-pdf-accessibility` | PDF/UA validation, remediation | https://pdfix.net |
| `pac-2024` (PAC) | Free PDF accessibility checker | https://pdfua.foundation |
| `andi` (bookmarklet) | Manual ANDI tool from SSA | https://www.ssa.gov/accessibility/andi/ |
| `ffmpeg` + `whisper` | Auto-caption pipeline (still requires human QA) | https://github.com/openai/whisper |
| `accessibility-insights-cli` | MS automated tab-stop & guided checks | https://accessibilityinsights.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Siteimprove | SaaS | REST API | Used widely by US gov; tracks compliance posture, exports gov-style reports. |
| Level Access / AudioEye | SaaS | API + manual audit | Combine automated + human; AudioEye's overlay alone is NOT compliance — DOJ has stated overlays don't substitute for fixes. |
| Deque axe Auditor + axe Monitor | SaaS | API | Continuous monitoring, IGT, regression tracking. |
| 3PlayMedia | SaaS | API | Captioning + audio description for video. |
| Rev | SaaS | API | Captions/transcripts; cheaper than 3PlayMedia for English. |
| CommonLook | SaaS | desktop only | PDF remediation gold standard. |
| Allyant (PDF/document remediation) | SaaS / service | manual | For long-form docs and forms. |
| Section508.gov ICT testing baseline | OSS docs | n/a | Use as procurement baseline. |
| GSA Section508.gov VPAT templates | OSS | downloadable | Always start from VPAT 2.5 INT. |

## Templates & scripts
See README "Accessibility Statement" template + VPAT 2.5 from itic.org. Inline VPAT cell generator from axe JSON:

```bash
#!/usr/bin/env bash
# vpat-cells.sh axe.json → markdown table mapping rule → WCAG → conformance
node -e '
const v = JSON.parse(require("fs").readFileSync(process.argv[1])).violations || [];
const map = {};
v.forEach(r => (r.tags||[]).filter(t=>t.startsWith("wcag")).forEach(t=>{
  const k = t.toUpperCase().replace("WCAG","").replace(/(\d)(\d{2})/,"$1.$2");
  map[k] = map[k] || [];
  map[k].push({rule:r.id, impact:r.impact, count:r.nodes.length});
}));
console.log("| WCAG | Conformance | Notes |");
console.log("|------|-------------|-------|");
Object.keys(map).sort().forEach(k=>{
  const issues = map[k].map(x=>`${x.rule} (${x.count})`).join(", ");
  console.log(`| ${k} | Does Not Support | ${issues} |`);
});
' "$1"
```

## Best practices
- Track conformance per page + per WCAG criterion in a matrix; do NOT report a single global score — DOJ guidance asks for criterion-level evidence.
- Procurement: bake WCAG 2.1 AA conformance + 30-day remediation SLA + reaudit-on-major-version into every vendor contract.
- Maintain a public-facing accessibility statement with feedback email; DOJ rule effectively requires it.
- Run a11y CI on PR; set Pa11y/axe thresholds to monotonically decrease (no new violations).
- Caption ALL videos before publish — agents can pre-fill via Whisper, human edits to ≥99% accuracy.
- Use VPAT 2.5 INT (combined Section 508 + WCAG 2.1 + EN 301 549) — covers federal + state procurement.
- Keep an inventory of pre-effective-date vs. post content; once you "alter" old content, exemption disappears.

## AI-agent gotchas
- **Overlay tools are not compliance** — DOJ has explicitly warned. Agent should refuse to recommend them as the primary fix.
- LLM-generated audio descriptions often misread visuals (logos, charts) — require human QA on every minute of described content.
- Auto-caption (Whisper, etc.) is ~92-96% accurate on clean audio — DOJ accuracy bar is "accurate, synchronized, complete" → human review mandatory before claiming compliance.
- Agents must NOT mark a WCAG criterion "Supports" without evidence — train them to use "Not Tested" by default.
- "Pass on automated scan" is not equivalent to WCAG conformance — courts and DOJ require manual + AT testing.
- Don't auto-publish accessibility statements containing claims the agent can't verify (e.g., "fully conformant"). Always human sign-off.
- Watch for date traps: "last reviewed" must be ≤12 months on most state policies; agent should fail audit if statement is stale.
- Mobile apps require platform-specific testing (XCUITest with Accessibility Inspector, Espresso AccessibilityChecks) — web-only agents will miss app barriers entirely.

## References
- DOJ Final Rule on Web/Mobile (April 2024) — https://www.ada.gov/resources/2024-03-08-web-rule/
- ADA.gov Web Accessibility Guidance — https://www.ada.gov/resources/web-guidance/
- Section508.gov ICT Testing Baseline + VPAT — https://www.section508.gov
- WCAG 2.1 quick reference — https://www.w3.org/WAI/WCAG21/quickref/
- VPAT 2.5 INT template (ITIC) — https://www.itic.org/policy/accessibility/vpat
- WebAIM legal resources — https://webaim.org/articles/laws/
- DOJ statement on accessibility overlays — https://www.ada.gov (search "accessibility overlay")
