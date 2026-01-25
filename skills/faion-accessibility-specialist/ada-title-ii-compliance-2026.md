# ADA Title II Compliance 2026

## Problem

US government entities and state/local services must comply with ADA Title II by April 2026. Non-compliance risks lawsuits, loss of federal funding, and exclusion of citizens with disabilities.

## Requirements

### Compliance Deadlines

| Entity Size | Deadline |
|-------------|----------|
| Large entities (50K+ population) | April 24, 2026 |
| Smaller entities (<50K population) | April 24, 2027 |

**Standard:** WCAG 2.1 Level AA

### Scope

All digital content must be accessible:
- Public-facing websites
- Mobile applications
- Multimedia content (video, audio)
- PDF documents
- Interactive forms and tools
- Third-party content (social media embeds, widgets)
- Online services and portals

### Video Accessibility Requirements

**Captions:**
- All pre-recorded video must have captions
- Live video must have captions (or real-time alternative)
- Captions must be accurate, synchronized, complete
- Include speaker identification and sound effects

**Audio Descriptions:**
- Visual information not available in soundtrack must be described
- Extended audio descriptions if pauses insufficient
- Can use separate track or integrated description

**Media Player:**
- Keyboard accessible controls
- Screen reader compatible
- Caption and audio description toggle
- Adjustable playback speed

### Document Accessibility

**PDF Requirements:**
- Tagged PDF structure
- Reading order defined
- Alternative text for images
- Form fields labeled
- Bookmarks for navigation
- Accessible tables

**Conversion Tools:**
- Adobe Acrobat Pro (PDF remediation)
- CommonLook PDF (validation)
- PAC 2024 (free checker)

### Web Content Requirements

**WCAG 2.1 Level AA includes:**

| Principle | Requirements |
|-----------|--------------|
| Perceivable | Alt text, captions, contrast 4.5:1, responsive design |
| Operable | Keyboard access, no time limits, skip links, focus visible |
| Understandable | Clear language, predictable navigation, error identification |
| Robust | Valid HTML, ARIA used correctly, compatible with assistive tech |

### Compliance Steps

```
1. Accessibility Audit
   → Automated scan (axe, WAVE, Lighthouse)
   → Manual testing (keyboard, screen reader)
   → Document all issues

2. Gap Analysis
   → Map findings to WCAG 2.1 AA criteria
   → Prioritize by severity and traffic
   → Estimate remediation effort

3. Remediation Roadmap
   → Critical issues (blocks access) → immediate
   → High priority (high-traffic pages) → 3 months
   → Medium priority → 6 months
   → Low priority → 12 months

4. Implementation
   → Fix issues in priority order
   → Test fixes before deploying
   → Document changes

5. Ongoing Monitoring
   → Automated testing in CI/CD
   → Quarterly manual audits
   → User testing with people with disabilities
   → Accessibility statement updated

6. Conformance Documentation
   → Create VPAT (Voluntary Product Accessibility Template)
   → ACR (Accessibility Conformance Report)
   → Publish accessibility statement
   → Provide feedback mechanism
```

### Accessibility Statement

Required on all government websites:

**Must include:**
- Commitment to accessibility
- Conformance level (WCAG 2.1 AA)
- Known limitations
- Contact information for accessibility issues
- Date of statement
- Feedback process

**Example:**
```
[Entity Name] is committed to ensuring digital accessibility
for people with disabilities. We are continually improving
the user experience for everyone and applying the relevant
accessibility standards.

Conformance Status: Partially conformant with WCAG 2.1 Level AA
(some limitations exist, documented below)

Feedback: If you encounter accessibility barriers, please
contact [accessibility@entity.gov] or call [XXX-XXX-XXXX].

Last updated: [Date]
```

### Exemptions and Exceptions

**Not required to be accessible:**
- Content published before compliance date (if not altered)
- Archived content (clearly marked, not updated)
- Third-party content not under control (but must provide alternative)

**Limited exceptions:**
- Undue burden (must document and provide alternative)
- Fundamental alteration (changes nature of service)

### Enforcement and Penalties

**Consequences of non-compliance:**
- DOJ complaints and investigations
- Private lawsuits under ADA Title II
- Loss of federal funding
- Consent decree requiring compliance + monitoring
- Reputation damage

**Proactive measures:**
- Annual accessibility audits
- Staff training on accessibility
- Accessibility procurement standards
- Include in vendor contracts
- User testing with people with disabilities

### Training Requirements

**Required training for:**
- Content creators and editors
- Web developers
- Procurement officers
- Customer service staff
- Leadership and decision-makers

**Training topics:**
- WCAG 2.1 AA requirements
- Creating accessible documents
- Testing with screen readers
- Accessible form design
- Video captioning and descriptions

### Procurement Standards

**Accessibility requirements for vendors:**
- VPAT required for all software/services
- Accessibility conformance in RFPs
- Remediation timeline in contracts
- Ongoing accessibility support commitment
- Testing and validation requirements

### Third-Party Content

**Vendor-provided tools must be:**
- WCAG 2.1 AA conformant
- Include VPAT documentation
- Provide accessible alternatives if limitations exist
- Include remediation timeline for issues

**Social media and embeds:**
- Choose accessible platforms
- Provide alternative access to information
- Caption videos before posting
- Use alt text on images

## Sources

- [DOJ: Web Accessibility Rule (Final Rule)](https://www.ada.gov/resources/2024-03-08-web-rule/)
- [ADA.gov: Guidance on Web Accessibility](https://www.ada.gov/resources/web-guidance/)
- [Section508.gov: ADA and Section 508](https://www.section508.gov/manage/laws-and-policies/)
- [W3C WAI: WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM: Legal Issues in Web Accessibility](https://webaim.org/articles/laws/)
