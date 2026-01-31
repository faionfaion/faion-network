# Checklist

## Semantic HTML Phase

- [ ] Use header/nav/main/footer elements
- [ ] Use semantic form elements (form, label, fieldset)
- [ ] Use heading hierarchy (h1 → h6) correctly
- [ ] Use lists (ul, ol) for list content
- [ ] Avoid div/span only (use semantic elements)
- [ ] Use button for clickable actions (not divs)

## ARIA Phase

- [ ] Add aria-label to icon buttons
- [ ] Add aria-describedby to form fields with help text
- [ ] Add role attributes where semantic HTML not applicable
- [ ] Use aria-live for dynamic content updates
- [ ] Add aria-invalid and aria-required to form fields
- [ ] Use aria-hidden for decorative elements

## Form Accessibility Phase

- [ ] Associate labels with inputs (htmlFor)
- [ ] Add required and aria-required attributes
- [ ] Show error messages with id references
- [ ] Use fieldset/legend for grouped fields
- [ ] Test form with keyboard only
- [ ] Provide clear validation messages

## Keyboard Navigation Phase

- [ ] Test Tab navigation order (logical flow)
- [ ] Ensure all interactive elements keyboard accessible
- [ ] Implement focus management
- [ ] Trap focus in modals
- [ ] Test Escape to close dialogs/modals
- [ ] Use roving tabindex for complex widgets

## Color and Contrast Phase

- [ ] Verify WCAG AA contrast ratio (4.5:1 for normal text)
- [ ] Never use color alone for information
- [ ] Add icons/text with color indicators
- [ ] Test in high contrast mode
- [ ] Provide color alternatives
- [ ] Use focus indicators (not outline: none)

## Images and Media Phase

- [ ] Add meaningful alt text to images
- [ ] Use empty alt="" for decorative images
- [ ] Add captions/transcripts to videos
- [ ] Provide audio descriptions for videos
- [ ] Test video player keyboard navigation
- [ ] Add transcript for podcasts/audio

## Testing Phase

- [ ] Run axe accessibility scanner
- [ ] Test with screen reader (NVDA, JAWS)
- [ ] Test keyboard only (no mouse)
- [ ] Test with browser zoom (200%)
- [ ] Test in high contrast mode
- [ ] Test on mobile (VoiceOver, TalkBack)

## Component Testing Phase

- [ ] Test component announced correctly by screen reader
- [ ] Test interactive elements have proper roles
- [ ] Test form fields have associated labels
- [ ] Test error messages announced
- [ ] Test loading states announced
- [ ] Test notifications announced

## Responsive Design Phase

- [ ] Test mobile responsive (375px width)
- [ ] Test tablet responsive
- [ ] Test no horizontal scroll on mobile
- [ ] Test text readable without zoom
- [ ] Test touch targets (minimum 48x48px)
- [ ] Test landscape/portrait orientations

## Automation Phase

- [ ] Set up jest-axe for component tests
- [ ] Run Lighthouse CI for automated audits
- [ ] Fail tests on accessibility violations
- [ ] Include a11y tests in PR validation

## Documentation Phase

- [ ] Document accessible components patterns
- [ ] Create accessibility checklist for dev
- [ ] Document WCAG 2.1 Level AA requirements
- [ ] Create troubleshooting guide

## Deployment

- [ ] Monitor accessibility metrics
- [ ] Track a11y issues in backlog
- [ ] Train team on accessibility