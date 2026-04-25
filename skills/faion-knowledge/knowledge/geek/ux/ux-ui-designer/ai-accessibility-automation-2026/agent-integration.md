# Agent Integration — AI Accessibility Automation 2026

## When to use
- Establishing a continuous accessibility baseline in CI/CD where every PR is scanned before merge
- Scaling accessibility audits across a large site (100+ pages) where manual review is impractical
- Generating ADA/VPAT documentation in response to procurement or legal requirements
- Integrating video captioning and audio description workflows for ADA Title II compliance (2026)
- Post-launch regression monitoring to catch accessibility regressions introduced by routine updates

## When NOT to use
- As the only accessibility validation method — AI automation covers 60-70% of detectable issues; the rest requires human + AT testing
- Replacing user testing with people with disabilities — automation cannot validate cognitive accessibility, task success, or assistive technology compatibility
- For auditing complex interactive patterns (custom data grids, drag-and-drop, real-time updates) — dynamic AT behavior is not captured by static scanners
- On SPAs that require authentication — scanners without session management will scan the login page only
- As a legal compliance proof without human expert review and sign-off

## Where it fails / limitations
- 94.8% of homepages still fail detectable WCAG 2 checks despite AI tooling being widely available — automation does not drive compliance on its own; process and accountability do
- AI detection rates plateau at 60-70% for automatable issues; the remaining 30-40% are context-dependent and require human judgment
- False negatives are common for ARIA live regions, focus management, and keyboard trap detection — these require runtime AT interaction
- AI-generated VPAT drafts contain factual errors for complex criteria (e.g., 4.1.3 Status Messages in SPAs) — always human-reviewed before publishing
- ADA Title II video captioning requirements (2026): AI captions achieve ~95% accuracy on standard English speech; accuracy drops significantly for accents, technical terminology, and non-English content

## Agentic workflow
A Claude subagent running as an accessibility automation pipeline can: trigger axe-core scans via Playwright, parse and prioritize violations by WCAG criterion and user impact, generate developer-facing remediation briefs with code fix suggestions, and draft VPAT sections. The agent pipeline runs unattended in CI/CD for detection and reporting. Human accessibility specialists own: AT testing validation, VPAT legal review, and closure of complex issues. Video captioning can be submitted to 3Play Media or Deepgram via API and polled for completion — agent handles submission and output retrieval, human reviews output quality.

### Recommended subagents
- Custom a11y-ci-agent — triggered on PR, runs axe-core, posts violation summary as PR comment, fails PR on critical/serious violations
- Custom vpat-drafter agent — takes scan results + manual test notes, generates structured VPAT 2.5 draft in Markdown
- Custom caption-pipeline agent — submits video files to captioning API, polls for completion, validates output format, delivers to content team

### Prompt pattern
```
You are an accessibility engineer reviewing automated scan results.
<scan_results>{{axe_json_violations}}</scan_results>

For each violation:
1. WCAG 2.2 criterion (number + name)
2. Impact level: critical / serious / moderate / minor
3. Affected users: describe which disability groups are impacted
4. Code fix: show before/after HTML/CSS/ARIA
5. Test to verify fix: specific AT + browser combination to validate

Flag violations that cannot be verified by automation — mark as "requires AT testing".
Do not mark any issue as resolved — that is the developer's responsibility.
```

```
Draft a VPAT 2.5 Section 508 conformance statement for:
Product: {{product_name}}
Test date: {{test_date}}
Automated scan results: {{scan_summary}}
Manual test notes: {{manual_notes}}
Known issues not yet fixed: {{open_issues}}

For each WCAG criterion:
- Conformance level: Supports / Partially Supports / Does Not Support / Not Applicable
- Remarks: specific explanation (not generic)

Flag all criteria where the conformance claim requires human legal review before publishing.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` (via Playwright) | WCAG automated scanning with JSON output | `npm install axe-core playwright` / github.com/dequelabs/axe-core |
| `lighthouse` CLI | Chrome-based a11y + performance audit | `npm install -g lighthouse` / developer.chrome.com/docs/lighthouse |
| `pa11y-ci` | Batch URL accessibility scanning with CI config | `npm install -g pa11y-ci` / github.com/pa11y/pa11y-ci |
| `siteimprove` CLI | Enterprise monitoring CLI | siteimprove.com/accessibility |
| `wave-api` | WebAIM WAVE API for page-level scanning | wave.webaim.org/api |
| `ffmpeg` | Video format preprocessing before caption submission | ffmpeg.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Deque axe DevTools Enterprise | SaaS | Yes — REST API + CLI | AI-powered false-positive reduction; issue extraction with code context |
| Level Access | SaaS | Partial — API | "Ask Level AI" Q&A chatbot; VPAT generation; enterprise only |
| Siteimprove Accessibility | SaaS | Yes — REST API | Continuous monitoring; webhook alerts for regression |
| 3Play Media | SaaS | Yes — REST API | AI-enabled captions + audio descriptions; ADA Title II workflow |
| Deepgram | SaaS | Yes — REST API | ASR for caption generation; lower cost than 3Play; less editorial review |
| UserWay | SaaS | Yes — JS/REST API | AI scan + overlay; use scan API only, not overlay for compliance |
| Equally AI | SaaS | Yes — REST API | Automated scanning + AI remediation suggestions |
| Cloudflare Turnstile | SaaS | Yes | Not a11y tool, but needed to handle CAPTCHAs during automated scanning |

## Templates & scripts
See templates.md for VPAT 2.5 template and CI scan configuration.

Inline: pa11y-ci batch scanner with JSON output:
```python
import subprocess, json, sys
from pathlib import Path

def run_pa11y(urls_file: str, output_file: str):
    config = {
        "defaults": {
            "standard": "WCAG2AA",
            "runners": ["axe", "htmlcs"],
            "timeout": 30000,
            "wait": 2000,
        },
        "urls": open(urls_file).read().splitlines()
    }
    config_path = "/tmp/pa11y-config.json"
    with open(config_path, "w") as f:
        json.dump(config, f)

    result = subprocess.run(
        ["pa11y-ci", "--config", config_path, "--json"],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    total = sum(len(v) for v in data.get("results", {}).values())
    print(f"Scanned {len(data.get('results', {}))} URLs, found {total} issues")

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

run_pa11y(sys.argv[1], sys.argv[2])
```

## Best practices
- Run axe-core at PR level (block on critical/serious), and full pa11y-ci scan weekly (report on all levels) — different cadences for different audiences
- Separate issue detection (automated) from issue resolution (human) in your workflow; don't merge these into a single AI step
- For ADA Title II video compliance: submit to captioning service early in content pipeline, not as a post-publish step
- Track violation counts per WCAG criterion over time — a rising trend in one criterion indicates a systemic code pattern problem
- Integrate axe results into your issue tracker (Jira/Linear) automatically; issues not tracked don't get fixed
- Use AI-generated VPAT drafts as a starting point for the annual compliance review, not a finished document — legal must review each claim

## AI-agent gotchas
- Playwright-based scanners must handle cookie consent banners and auth walls before scanning; agents that skip these steps produce incomplete results
- SPA route coverage requires explicit navigation triggers; axe-core scans the current DOM snapshot — it misses routes not visited during the scan session
- AI false-positive reduction in tools like axe DevTools is model-dependent; tool upgrades can change which issues are surfaced — pin tool versions in CI
- Caption APIs return files asynchronously; agents must implement polling with timeout and retry, not synchronous wait
- VPAT criterion language is legally precise; LLM paraphrasing of WCAG success criteria introduces compliance risk — use exact W3C wording

## References
- WebAIM Million Report 2026 — webaim.org/projects/million
- WCAG 2.2 specification — w3.org/TR/WCAG22
- ADA Title II Final Rule (video accessibility) — ada.gov/notices/2024/04/24/accessibility-web-mobile-apps
- Deque axe-core GitHub — github.com/dequelabs/axe-core
- 3Play Media captioning API — 3playmedia.com/solutions/products/api
- Level Access "2026 State of Digital Accessibility" report — levelaccess.com
- pa11y-ci documentation — github.com/pa11y/pa11y-ci
