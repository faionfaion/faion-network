# Quality Checklist — [Feature Name]

## Code Quality

- [ ] Follows coding standards (ruff / eslint clean)
- [ ] No code smells (SonarQube clean)
- [ ] Error handling implemented for all external calls
- [ ] Logging added for key operations
- [ ] Edge cases covered in tests

## Testing

- [ ] Unit tests written and passing
- [ ] Integration tests passing (if applicable)
- [ ] Manual QA completed in staging
- [ ] Regression testing done on adjacent features

## Performance

- [ ] Page loads within target (p95 < 3s)
- [ ] API response within target (p95 < 500ms)
- [ ] No memory leaks (heap profile checked)
- [ ] Tested with realistic data volume

## Security

- [ ] Input validation on all user-supplied data
- [ ] Authentication and authorization verified
- [ ] No sensitive data exposed in logs or responses
- [ ] gitleaks / semgrep clean

## Accessibility

- [ ] Keyboard navigation functional
- [ ] Screen reader compatible (ARIA labels present)
- [ ] Color contrast ratio meets WCAG AA (4.5:1)
- [ ] Alt text on all meaningful images
