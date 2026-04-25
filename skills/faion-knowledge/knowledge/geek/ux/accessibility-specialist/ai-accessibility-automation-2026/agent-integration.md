# Agent Integration — AI Accessibility Automation 2026

## When to use
- Establishing continuous accessibility monitoring in a CI/CD pipeline for a product with frequent deployments
- Generating ADA Title II compliance documentation (effective 2026) for public-sector or higher-education digital products
- Scaling accessibility remediation across a large codebase where manual triaging is cost-prohibitive
- Producing AI-assisted VPAT drafts for enterprise procurement processes
- Automating captioning and audio description pipelines for video-heavy content operations
- Setting up regression prevention so new code does not reintroduce fixed violations

## When NOT to use
- The team has no existing accessibility baseline — start with a manual audit first to understand the real state
- Product is in pre-MVP prototyping — defer automation until the UI stabilizes
- AI automation is being proposed as a replacement for user testing with people who use assistive technology
- The team plans to deploy AI overlay widgets as the compliance strategy (overlays do not satisfy ADA Title II)
- Budget is the only driver — automation tools cost $100–$2,000/month; weigh against compliance risk

## Where it fails / limitations
- Even AI-enhanced scanning covers only 60–70% of WCAG success criteria; 30–40% requires human judgment
- Cognitive accessibility (WCAG 2.2 new SCs: 3.3.7, 3.3.8) is almost entirely outside current AI detection
- AI-suggested code fixes for complex ARIA patterns are frequently wrong — require human validation
- VPAT drafts require legal/compliance review before submission; AI cannot assess organizational conformance claims
- Video auto-captions at AI-only accuracy (80–90%) violate ADA Title II requirements — always pair with human review
- AI prioritization reflects traffic-based impact estimates, not the actual severity for individual users with disabilities
- The ADA Title II deadline for state/local government compliance was April 2026 — late adopters face immediate legal risk

## Agentic workflow
A Claude subagent (Haiku) orchestrates a multi-tool scan pipeline: axe-playwright for WCAG violations, 3Play Media API for video caption jobs, and Azure Computer Vision for bulk alt text generation. A Sonnet subagent receives the aggregated issue JSON and produces ranked remediation tickets with code fix suggestions attached. A Haiku subagent generates the VPAT draft from the scan summary and uploads it to a shared document store. All outputs are gated by a human accessibility lead before entering the developer backlog.

### Recommended subagents
- General Claude subagent (Haiku) — scan orchestration, false-positive filtering, VPAT section drafting
- General Claude subagent (Sonnet) — code fix generation, WCAG criterion explanation, issue ticket authoring
- General Claude subagent (Haiku) — bulk alt text generation, caption job submission, report aggregation

### Prompt pattern
```
You are an accessibility automation engineer. Given this axe-core scan report (JSON),
perform the following:
1. Remove violations where the element is aria-hidden or display:none (likely false positives)
2. Rank remaining violations: Critical (A failures affecting all users), High (AA failures),
   Medium (A failures with workarounds), Low (AAA or minor)
3. Group related violations by component type
4. For each Critical and High issue, generate a concrete code fix in [framework]
5. Output: { summary: {...}, issues: [...], fixes: {...} }
Do not invent issues not present in the scan data.
```

```
Draft the following VPAT 2.5 sections based on this scan summary: [summary JSON].
For each WCAG criterion, output one of: Supports | Partially Supports | Does Not Support | Not Applicable.
Add a one-sentence note for each non-"Supports" entry explaining what fails.
Mark all entries as DRAFT — human review required before publication.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-playwright` | Headless WCAG scanning — most accurate OSS tool | `npm install @axe-core/playwright` |
| `pa11y-ci` | Batch URL scanning in CI pipelines | `npm install -g pa11y-ci` |
| `lighthouse-ci` | Combined perf + a11y scoring gate | `npm install -g @lhci/cli` |
| `jest-axe` | Unit-level component a11y assertions | `npm install jest-axe` |
| `cypress-axe` | E2E a11y assertions in Cypress tests | `npm install cypress-axe` |
| `eslint-plugin-jsx-a11y` | Static JSX a11y linting (catches issues at write time) | `npm install eslint-plugin-jsx-a11y` |
| `htmlhint` | Validates accessible HTML structure | `npm install htmlhint` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Deque axe DevTools Pro | SaaS | Yes — CLI + API | AI issue extraction + fix suggestions; ADA Title II reporting |
| Evinced | SaaS | Yes — CI/CD integration | AI-powered continuous scanning; REST API for issue data |
| AudioEye | SaaS | Partial | AI remediation with human oversight; not overlay-based |
| 3Play Media | SaaS | Yes — REST API | ADA-compliant captions (AI + human review, 99% accuracy) |
| Rev.ai | SaaS | Yes — REST API | 80–90% accuracy AI captions; needs human review step |
| Microsoft Azure Computer Vision | SaaS | Yes — REST API | Bulk alt text generation from image URLs/bytes |
| Siteimprove | SaaS | Yes — REST API | Enterprise monitoring + trend analysis; API for issue data |
| Level Access | SaaS | Partial — chatbot only | Ask Level AI for WCAG Q&A; no programmatic scan API |

## Templates & scripts
See `templates.md` for the VPAT 2.5 template skeleton and CI gate configuration.

CI gate script (blocks deployment on new Critical violations):
```bash
#!/usr/bin/env bash
# ci-a11y-gate.sh — fail build if new Critical a11y violations introduced
set -euo pipefail

BASELINE="${1:-a11y-baseline.json}"
CURRENT="a11y-current.json"

npx axe-cli \
  --browser chrome \
  --tags wcag2a,wcag2aa \
  --reporter json \
  "$(cat urls.txt)" > "$CURRENT"

python3 - <<'EOF'
import json, sys

baseline = json.load(open("a11y-baseline.json")) if __import__("os").path.exists("a11y-baseline.json") else {"violations": []}
current = json.load(open("a11y-current.json"))

baseline_ids = {v["id"] for v in baseline.get("violations", [])}
new_violations = [v for v in current.get("violations", []) if v["id"] not in baseline_ids and v["impact"] == "critical"]

if new_violations:
    print(f"FAIL: {len(new_violations)} new Critical a11y violations introduced:")
    for v in new_violations:
        print(f"  - {v['id']}: {v['description']}")
    sys.exit(1)
print("PASS: No new Critical a11y violations.")
EOF
```

## Best practices
- Set a WCAG 2.2 AA baseline on the current codebase before enabling CI gates — gate on regressions, not the full backlog
- Separate the automated backlog (AI-found) from the manual backlog (human-found); never merge them without tagging the source
- For ADA Title II compliance: document both what passes and what does not pass; VPAT requires honest assessment, not just wins
- Prioritize Critical violations on high-traffic pages first; AI traffic-based ranking is a useful starting point
- Caption pipeline: submit to 3Play Media (or equivalent) immediately on video upload; never publish without 99%-accuracy captions
- Track false positive rate monthly — if AI filter is marking real issues as false positives, retune the filter rules
- Brief developers on WCAG intent, not just rule ID — "why" knowledge reduces recurrence of the same violation type

## AI-agent gotchas
- VPAT drafts are legal documents; any AI-generated conformance claim that is inaccurate exposes the organization to legal risk — mandatory human review before any external use
- Axe JSON from large single-page applications can exceed 100KB — chunk by page/component before sending to LLM
- Agent-generated code fixes for ARIA roles are error-prone for complex widget patterns (combobox, tree, grid) — flag these for senior review
- Alt text agents lack brand voice and image purpose context; always provide surrounding page context in the prompt
- Human-in-loop checkpoint: accessibility lead must approve ranked issue list before developer tickets are created
- Do not auto-close issues based on AI re-scan alone — require a human to confirm the fix works with real assistive technology

## References
- WebAIM Million 2026: https://webaim.org/projects/million/
- ADA Title II final rule: https://www.ada.gov/resources/web-guidance/
- Deque AI accessibility: https://www.deque.com/blog/ai-accessibility-testing/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- VPAT 2.5 template: https://www.itic.org/policy/accessibility/vpat
- 3Play Media captioning API: https://www.3playmedia.com/solutions/features/apis/
