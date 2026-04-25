# Agent Integration — Mobile UX Design Basics

## When to use
- Starting a new product or feature that must run on mobile — apply mobile-first constraints from the design phase
- Auditing an existing web product for mobile usability issues before a mobile traffic spike (e.g., a campaign)
- Reviewing PRs that add UI components to ensure touch targets, input types, and thumb-zone placement are correct
- Before submitting to App Store or Google Play — checklist sweep against HIG and Material Design guidelines
- Performance audit for mobile: LCP, FID, CLS targets are more critical on mobile than desktop

## When NOT to use
- Internal tools used exclusively on desktop (admin panels, data dashboards accessed via VPN)
- Projects where mobile is explicitly out of scope for the current phase — apply only when mobile is a target
- Prototyping in high fidelity before mobile constraints are validated — wireframe mobile flows first
- Accessibility-only audits — mobile UX overlaps but is not a replacement for dedicated accessibility review

## Where it fails / limitations
- Emulator testing misses real-device performance issues (thermal throttling, memory pressure, real touch latency)
- Thumb-zone models assume standard one-handed grip — left-handed users, large phones, and accessibility needs break the model
- Mobile-first design forced on a product with inherently complex desktop tasks (e.g., video editing, code editors) produces a degraded desktop experience
- Android fragmentation (1000+ device sizes, GPU variations) makes visual QA incomplete without a real device lab
- Gesture navigation assumptions differ between iOS (swipe from edge to go back) and Android (back gesture or button) — cannot be tested in browser

## Agentic workflow
An agent can review UI component specifications (JSX/HTML/CSS) and flag touch-target violations, missing input types, and non-mobile-friendly navigation patterns. It can also run Lighthouse mobile audits via CLI and parse results into actionable tickets. For design files, agents can analyze Figma frame dimensions and component spacing. Human testing on real devices remains the irreplaceable checkpoint — performance and real-touch behavior are not detectable by static analysis.

### Recommended subagents
- `faion-usability-agent` — full heuristic review including mobile-specific patterns (thumb zone, one-screen-one-action)
- general Lighthouse/performance agent — runs `lighthouse --preset=perf --form-factor=mobile` and parses Core Web Vitals output

### Prompt pattern
```
Review the following React component for mobile UX compliance. Check:
1. Touch targets: all interactive elements must be at least 44x44px (iOS) or 48x48dp (Android)
2. Input types: text inputs must use appropriate type= attributes (email, tel, number, search)
3. Viewport: no fixed-width elements that would cause horizontal scroll on 375px width
4. Navigation: confirm no critical actions are in the top 20% of screen height (hard reach zone)
Report violations with file:line references and proposed fixes.
```

```
Given this Lighthouse mobile audit JSON, extract all issues with severity >= "medium",
group by category (Performance / Accessibility / Best Practices), and write a prioritized
fix list with estimated complexity (Low/Med/High) for each item.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `lighthouse` CLI | Automated mobile performance and best-practice audit | `npm i -g lighthouse` / github.com/GoogleChrome/lighthouse |
| `puppeteer` | Headless Chrome with mobile device emulation for screenshot and interaction testing | `npm i puppeteer` / pptr.dev |
| `axe-core` CLI | Accessibility audit including mobile-relevant rules (touch targets, focus) | `npm i -g @axe-core/cli` / github.com/dequelabs/axe-core |
| `imagemin-cli` | Batch optimize images for mobile (WebP conversion, compression) | `npm i -g imagemin-cli` / github.com/imagemin/imagemin-cli |
| `size-limit` | Enforce JS bundle size budget for mobile performance | `npm i -D size-limit` / github.com/ai/size-limit |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| BrowserStack | SaaS | Yes — REST API | Real device cloud; agent can trigger test runs on specific devices and retrieve screenshots |
| Sauce Labs | SaaS | Yes — REST API | Similar to BrowserStack; supports Appium for native app testing |
| Firebase Test Lab | SaaS | Yes — gcloud CLI | Google-hosted real device lab; integrates with CI/CD for automated mobile tests |
| Vercel Analytics | SaaS | Yes — API | Core Web Vitals by device type; agent can query mobile-specific CWV scores |
| PageSpeed Insights API | SaaS | Yes — REST API (free) | Google CWV data for real users on mobile; `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?strategy=mobile` |
| Smartlook | SaaS | Partial | Mobile session recordings; visual review required, no structured API for findings |

## Templates & scripts
See `checklist.md` for the full design/development/testing phase checklists.

Inline script — run Lighthouse mobile audit and extract key metrics:
```bash
#!/usr/bin/env bash
# Usage: ./mobile-audit.sh https://example.com
URL=$1
OUT="lighthouse-mobile-$(date +%Y%m%d-%H%M).json"

lighthouse "$URL" \
  --output=json \
  --output-path="$OUT" \
  --form-factor=mobile \
  --throttling-method=simulate \
  --preset=perf \
  --chrome-flags="--headless" \
  --quiet

echo "=== Core Web Vitals ==="
jq '{
  LCP: .audits["largest-contentful-paint"].displayValue,
  FID: .audits["max-potential-fid"].displayValue,
  CLS: .audits["cumulative-layout-shift"].displayValue,
  TTI: .audits["interactive"].displayValue,
  score: .categories.performance.score
}' "$OUT"

echo "=== Failed Audits ==="
jq '[.audits | to_entries[] | select(.value.score != null and .value.score < 0.9) |
  {id: .key, title: .value.title, score: .value.score}] | sort_by(.score)' "$OUT"
```

## Best practices
- One primary action per screen is a hard constraint, not a guideline — if a screen has two equally weighted CTAs, it needs to be split or redesigned
- Bottom navigation bar (3-5 items) consistently outperforms hamburger menus for discoverability on mobile — reserve hamburger for secondary or overflow navigation only
- Always set input `type` attributes correctly — `type="email"` triggers the right keyboard on mobile, reducing form errors
- Skeleton screens reduce perceived load time better than spinners for content-heavy pages — implement them for any list or feed that takes >500ms
- Test with OS-level text scaling set to "larger" (150-200%) — most mobile UX breaks at large text sizes because absolute units were used
- Use `srcset` and `sizes` attributes on all images — a retina image served to a 2G user wastes bandwidth and degrades performance
- Never disable zoom (`user-scalable=no`) — it is an accessibility violation and is blocked by Safari

## AI-agent gotchas
- Agents analyzing CSS cannot detect actual rendered touch target size when styles are computed dynamically (e.g., from parent flex layout) — static analysis gives false positives and false negatives
- Lighthouse emulation uses network throttling simulation, not real 3G/4G — real-device results will differ, sometimes significantly
- Agents may suggest touch targets are compliant based on CSS width/height, but padding and margin overlap can make adjacent targets effectively smaller — visual review required
- Mobile-first means designing the mobile layout first, not just adding `@media (max-width)` breakpoints after — agents reviewing CSS-only may miss layout logic in JS components
- Android and iOS differ on swipe-back gesture behavior — a recommended gesture interaction for one platform may break on the other; agents should flag platform-specific patterns

## References
- https://www.nngroup.com/articles/mobile-ux/
- https://developer.apple.com/design/human-interface-guidelines/
- https://material.io/design/platform-guidance/android-bars.html
- Mobile First — Luke Wroblewski (A Book Apart)
- Touch Design for Mobile Interfaces — Steven Hoober
- https://web.dev/vitals/
