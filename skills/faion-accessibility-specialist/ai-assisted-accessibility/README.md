# AI-Assisted Accessibility

## Problem

Accessibility testing is time-consuming and requires significant expertise. Manual audits don't scale for continuous deployment. Traditional tools have high false positive rates and limited guidance.

## Solution: AI Tools for Accessibility

### AI-Powered Tools (2026 Update)

| Tool | Type | AI Features | Cost |
|------|------|-------------|------|
| **axe DevTools Pro** | Browser extension | AI suggestions, issue prioritization, chatbot | $$ |
| **Deque axe** | Enterprise platform | Intelligent false-positive reduction, AI fix recommendations | $$$ |
| **Accessibility Insights** | Microsoft suite | Code fix recommendations, automated guidance | Free |
| **WAVE** | Browser extension | Visual feedback with annotations | Free |
| **Lighthouse** | Chrome DevTools | Performance + a11y scoring, AI insights | Free |
| **Stark** | Design plugin | Contrast checking, vision simulation, AI suggestions | Free/$ |
| **UserWay** | Widget + scanner | AI remediation suggestions (caution on overlays) | $$ |
| **Equidox** | PDF accessibility | Automated PDF tagging with AI | $$ |
| **Level Access** | Enterprise platform | Ask Level AI chatbot for WCAG Q&A | $$$ |
| **3Play Media** | Video accessibility | AI-enabled captions, audio description | $$ |
| **Evinced** | Continuous testing | AI-powered scanning in CI/CD | $$$ |
| **Siteimprove** | Enterprise monitoring | AI trend analysis, prioritization | $$$ |

### New AI Capabilities (2026)

**Issue-Level AI Assistance:**
- AI tools attached directly to individual audit issues
- Developers can simplify technical WCAG language with one click
- Get specific code fixes without switching context
- Multiple fix options ranked by best practice

**Automated Documentation:**
- VPAT generation (draft in seconds vs. hours)
- Accessibility conformance reports auto-generated
- Issue documentation with screenshots and code snippets
- Trend reports and executive summaries

**Intelligent Scanning:**
- Reduced false positives (from 30-40% down to 10-15%)
- Context-aware issue detection
- Priority ranking based on user impact
- Related issues grouped together

**Developer Experience:**
- In-IDE accessibility hints (VS Code, JetBrains)
- Real-time accessibility linting
- Fix-on-save capabilities
- Learning from past fixes

### AI for Alt Text

**AI Alt Text Generators:**
- **Microsoft Azure Computer Vision** - Describes image content
- **Google Cloud Vision AI** - Object and scene detection
- **OpenAI GPT-4 Vision** - Contextual descriptions
- **Anthropic Claude 3** - Detailed image analysis

**Best Practice:**
```
1. Generate AI alt text suggestion
2. Review for accuracy and context
3. Edit to match brand voice and purpose
4. Ensure decorative images marked as such
5. Never blindly accept AI suggestions
```

**AI Limitations:**
```
AI can describe what's in image
AI cannot determine:
→ Why image matters to user
→ What should be emphasized
→ Appropriate level of detail
→ Brand voice and tone
→ Cultural context
```

### AI for Captions and Transcripts

**Auto-Captioning Tools:**
- **YouTube** - Free auto-captions (80-85% accuracy)
- **Rev.ai** - AI transcription (90% accuracy)
- **Otter.ai** - Real-time transcription
- **Descript** - Audio/video editing with AI transcription
- **3Play Media** - AI + human review (99% accuracy)

**Accuracy Requirements:**
```
Legal requirement: 99% accuracy for captions
AI-only: 80-90% accuracy
AI + human review: 95-99% accuracy
Always review AI-generated captions before publishing
```

### AI Testing Workflow

**Best Practice Workflow:**
```
1. Automated Scan (30-50% coverage)
   → Run axe, WAVE, Lighthouse
   → AI prioritizes findings
   → False positives filtered

2. AI Suggestions (get fix recommendations)
   → Review AI-proposed code fixes
   → Understand why issue matters
   → Get multiple fix options

3. Manual Verification (validate AI)
   → Test keyboard navigation
   → Verify logical fix makes sense
   → Check edge cases AI missed

4. User Testing (validate everything)
   → Test with people with disabilities
   → Use real assistive technology
   → Validate assumptions

5. Continuous Monitoring (prevent regression)
   → AI scans on every deploy
   → Track trends over time
   → Alert on new critical issues
```

### Caution on AI Overlays

**Accessibility Overlays (AI widgets):**
```
❌ Don't fix underlying code issues
❌ Band-aid solutions, not real fixes
❌ May interfere with assistive tech
❌ Don't provide true WCAG compliance
❌ Can create new barriers

✅ Use AI for testing and fixing
✅ Build accessibility into codebase
✅ Fix root causes, not symptoms
```

**Why overlays fail:**
- Cannot fix semantic HTML issues
- Cannot fix keyboard navigation
- Cannot fix heading structure
- Cannot provide meaningful alt text
- Add complexity and potential conflicts

### AI for Different Content Types

**Web Pages:**
- Automated WCAG scanning
- Code fix suggestions
- Contrast checking
- Heading hierarchy validation

**PDFs:**
- Auto-tagging with AI (needs review)
- Reading order detection
- Table structure identification
- Form field labeling

**Videos:**
- Auto-generated captions (review required)
- Scene description suggestions
- Speaker identification
- Sound effect notation

**Mobile Apps:**
- Automated accessibility scanning
- Screen reader testing simulation
- Touch target validation
- Color contrast checking

### Integration Points

**Design Tools:**
- Figma: Stark plugin (AI contrast, simulation)
- Adobe XD: Accessibility checker built-in
- Sketch: Contrast plugins

**Development:**
- VS Code: axe Linter extension
- JetBrains: Accessibility inspections
- ESLint: jsx-a11y plugin
- Storybook: a11y addon

**Testing:**
- Playwright: axe-playwright integration
- Cypress: cypress-axe plugin
- Jest: jest-axe for unit tests
- Selenium: axe-selenium integration

**CI/CD:**
- GitHub Actions: accessibility-checker
- GitLab CI: pa11y integration
- Jenkins: accessibility plugins
- CircleCI: automated a11y testing

### ROI of AI-Assisted Accessibility

**Time Savings:**
```
Manual audit: 20-40 hours
AI-assisted audit: 5-10 hours
Savings: 60-75% time reduction
```

**Issue Detection:**
```
Manual only: 50-70% of issues
AI + Manual: 85-95% of issues
Continuous AI: Prevent 40% of issues before production
```

**Cost Comparison:**
```
External audit: $5,000-$20,000 per audit
AI tools: $100-$2,000/month
Break-even: 1-3 audits per year
```

### Key Insights

**AI as Force Multiplier:**
> "AI is a force multiplier for accessibility programs. By combining automation with human expertise, organizations can scale faster, reduce manual effort, and demonstrate ROI."

**Human + AI Best:**
- AI finds issues faster and more consistently
- Humans provide context, empathy, and judgment
- Combine both for best results
- Never rely on AI alone

**Continuous > One-time:**
- Shift from annual audits to continuous monitoring
- Catch issues before they reach production
- Build accessibility into development workflow
- Use AI to make it sustainable

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Scan page for WCAG violations | haiku | Pattern-based automated detection |
| Review accessibility audit results | sonnet | Requires expert judgment |
| Design accessible system architecture | opus | Complex trade-offs |

## Sources

- [Deque: AI-Powered Accessibility](https://www.deque.com/blog/ai-accessibility/)
- [Level Access: Ask Level AI](https://www.levelaccess.com/products/ask-level/)
- [Microsoft Accessibility Insights](https://accessibilityinsights.io/)
- [WebAIM: Evaluation Tools](https://webaim.org/articles/tools/)
- [Overlay Fact Sheet (Why overlays fail)](https://overlayfactsheet.com/)
