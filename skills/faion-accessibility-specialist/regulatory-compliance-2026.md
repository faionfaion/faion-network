# Regulatory Compliance 2026

## Problem

Digital accessibility regulations vary by region with different standards, deadlines, and enforcement mechanisms. Non-compliance risks lawsuits, fines, and exclusion of customers.

## Key Regulations

### United States

| Regulation | Applies To | Deadline | Standard | Enforcement |
|------------|-----------|----------|----------|-------------|
| **ADA Title II (DOJ Rule)** | State/local government | April 2026 (large) / April 2027 (small) | WCAG 2.1 AA | DOJ, lawsuits |
| **ADA Title III** | Private businesses (courts) | Ongoing | WCAG 2.0/2.1 AA | Private lawsuits |
| **Section 508** | Federal agencies | Now | WCAG 2.0 AA | Agency oversight |
| **CVAA** | Video programming, communications | Now | WCAG 2.0 AA | FCC |

### European Union

| Regulation | Applies To | Deadline | Standard | Enforcement |
|------------|-----------|----------|----------|-------------|
| **European Accessibility Act (EAA)** | E-commerce, banking, transport, e-books | June 2025 (new products) / June 2030 (existing) | EN 301 549 (≈ WCAG 2.1 AA) | EU member states |
| **Web Accessibility Directive** | Public sector websites/apps | Now | EN 301 549 | Member state authorities |
| **GDPR** | All processing personal data | Now | Accessibility of privacy notices | Data protection authorities |

**EAA Scope:**
- E-commerce websites and services
- Banking services (ATMs, websites, mobile apps)
- Electronic communications (phones, messaging)
- Transport services (websites, apps, ticketing)
- E-books and dedicated e-book readers
- Consumer-facing services

### Canada

| Regulation | Jurisdiction | Deadline | Standard |
|------------|-------------|----------|----------|
| **AODA** | Ontario | Now | WCAG 2.0 AA |
| **ACA (Federal)** | Federally regulated entities | Now / 2025 | WCAG 2.1 AA |
| **Standards Canada** | Procurement | Ongoing | WCAG 2.1 AA |

### United Kingdom

| Regulation | Applies To | Standard |
|------------|-----------|----------|
| **Equality Act 2010** | All service providers | No specific standard (WCAG 2.1 AA recommended) |
| **Public Sector Bodies Regulations** | Public sector | WCAG 2.1 AA |

### Australia

| Regulation | Applies To | Standard |
|------------|-----------|----------|
| **Disability Discrimination Act** | All organizations | WCAG 2.1 AA (recommended) |
| **Government standards** | Federal/state government | WCAG 2.1 AA |

### Other Regions

**Japan:** JIS X 8341-3 (based on WCAG 2.0)
**Israel:** IS 5568 (WCAG 2.0 AA)
**India:** GIGW (Guidelines for Indian Government Websites)
**Brazil:** e-MAG (WCAG 2.0 based)

## Compliance Checklist

### Documentation Requirements

**Accessibility Statement:**
- [ ] Published and easy to find
- [ ] Conformance level stated (WCAG 2.1 AA)
- [ ] Known limitations documented
- [ ] Contact information for accessibility issues
- [ ] Date of statement
- [ ] Feedback mechanism described
- [ ] Alternative access methods if applicable

**VPAT/ACR (Voluntary Product Accessibility Template):**
- [ ] Created for products/services
- [ ] All WCAG criteria addressed
- [ ] Evidence of conformance provided
- [ ] Known issues documented
- [ ] Remediation timeline for issues
- [ ] Updated annually or on major changes

**Accessibility Policy:**
- [ ] Organizational commitment to accessibility
- [ ] Responsible parties identified
- [ ] Testing and remediation processes
- [ ] Training requirements
- [ ] Procurement standards
- [ ] Complaint process

### Technical Compliance

**WCAG 2.1 Level AA includes:**

| Success Criteria | Examples |
|------------------|----------|
| **Perceivable** | Alt text, captions, contrast 4.5:1, responsive |
| **Operable** | Keyboard access, no keyboard traps, skip links |
| **Understandable** | Clear language, predictable, error identification |
| **Robust** | Valid HTML, ARIA, assistive tech compatible |

**Testing Requirements:**
- [ ] Automated testing (axe, WAVE, Lighthouse)
- [ ] Manual keyboard testing
- [ ] Screen reader testing (NVDA, JAWS, VoiceOver)
- [ ] Color contrast verification
- [ ] Mobile accessibility testing
- [ ] User testing with people with disabilities

### Ongoing Monitoring

**Regular Audits:**
- Quarterly automated scans
- Annual comprehensive audit
- Testing after major updates
- Monitoring user feedback
- Tracking remediation progress

**Training:**
- Developers trained on accessible coding
- Designers trained on accessible design
- Content creators trained on accessible content
- Procurement staff trained on accessibility requirements
- Leadership aware of legal obligations

### Procurement Standards

**Vendor Requirements:**
- [ ] VPAT required for all software/services
- [ ] Accessibility testing in RFP
- [ ] Remediation timeline in contracts
- [ ] Ongoing support commitment
- [ ] Regular accessibility audits

**Third-Party Content:**
- [ ] Choose accessible platforms
- [ ] Provide alternatives if not accessible
- [ ] Include accessibility in vendor agreements
- [ ] Regular third-party audits
- [ ] Escalation path for issues

## Enforcement and Penalties

### United States (ADA)

**Consequences:**
- Private lawsuits (thousands per year)
- Settlement costs: $5,000 - $75,000+ average
- Legal fees: $50,000 - $200,000+
- Consent decrees requiring compliance
- Ongoing monitoring requirements
- Reputation damage

**Proactive Measures:**
- Regular accessibility audits
- VPAT documentation
- Accessibility statement published
- User testing with people with disabilities
- Developer training

### European Union (EAA)

**Penalties:**
- Fines up to 4% of annual revenue
- Product withdrawal from market
- Prohibition of services
- Compensation to affected individuals
- Member state enforcement varies

### Other Regions

- **Canada:** Complaints to accessibility authorities
- **UK:** Unlawful discrimination claims
- **Australia:** Complaints to Human Rights Commission
- **Varies by jurisdiction:** Research local requirements

## Exemptions and Exceptions

**Common exemptions:**
- Pre-existing content (if not updated)
- Archived content (clearly marked)
- Third-party content (if providing alternative)
- Undue burden (must document and provide alternative)
- Fundamental alteration (changes nature of service)

**Note:** Exemptions are narrow and must be documented. Always provide alternative access.

## Resources

**Standards:**
- WCAG 2.1: w3.org/WAI/WCAG21/quickref/
- EN 301 549: etsi.org/deliver/etsi_en/301500_301599/301549/
- Section 508: section508.gov

**Testing:**
- axe DevTools: deque.com/axe
- WAVE: wave.webaim.org
- Lighthouse: Built into Chrome DevTools

**Guidance:**
- WebAIM: webaim.org
- A11y Project: a11yproject.com
- W3C WAI: w3.org/WAI/

## Sources

- [DOJ: ADA Web Accessibility Rule](https://www.ada.gov/resources/2024-03-08-web-rule/)
- [European Commission: European Accessibility Act](https://ec.europa.eu/social/main.jsp?catId=1202)
- [W3C: WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Section508.gov: ICT Accessibility Standards](https://www.section508.gov/)
- [WebAIM: Legal Issues in Web Accessibility](https://webaim.org/articles/laws/)
