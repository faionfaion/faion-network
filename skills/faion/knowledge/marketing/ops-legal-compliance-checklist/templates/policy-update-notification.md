<!-- purpose: Material-change notification email for a ToS/Privacy Policy update, plus the internal pre-send checklist. -->
<!-- consumes: redlined policy changes + effective date + recipient first name -->
<!-- produces: Markdown email + internal checklist -->
<!-- depends-on: none -->
<!-- token-budget-impact: ~250-400 tokens when loaded as context -->

# Policy Update Email — Material Change Notification

Subject: Updates to our <subject>

---

Hi <first_name>,

We've updated our [Terms of Service / Privacy Policy] to [one-sentence reason, e.g. "reflect our use of new analytics tools" or "comply with updated GDPR guidance"].

**Key changes:**
- [Change 1: what it is and why it matters to you]
- [Change 2: what it is and why it matters to you]

The updated policy takes effect on **[date — at least 30 days from this email for material changes]**.

[Read the full updated policy →](https://[your-domain]/<policy_path>)

If you have any questions, reply to this email or contact us at [privacy@your-domain].

<company_name> Team

---

## Internal checklist before sending this email

- [ ] Redline of changes reviewed by legal counsel
- [ ] Effective date is at least 30 days out for material changes (GDPR expectation)
- [ ] Change log entry added to the policy page footer
- [ ] Version number / date updated on the policy page
- [ ] Previous version archived in git / version control
- [ ] Email sent to all active users (not just new signups)
- [ ] Unsubscribe mechanism working in this email
