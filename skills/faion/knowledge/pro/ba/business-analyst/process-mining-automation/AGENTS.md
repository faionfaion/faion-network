# Process Mining and Intelligent Automation Analysis

## Summary

A data-driven methodology for discovering actual process execution from IT event logs and identifying automation candidates using objective scoring criteria. Combines process mining tools (Celonis, Disco, ProM) to reconstruct real process flows, conformance checking against documented processes, and an automation readiness matrix that scores candidates on volume, standardization, stability, digital input, error rate, and ROI potential. Produces an automation assessment report with full/partial/no-go recommendations.

## Why

Process documentation relies on subjective stakeholder input that diverges from actual execution; RPA initiatives fail because automation is applied to processes that are not sufficiently rule-based or stable. Process mining replaces "interview the process owner" with event-log evidence, and the scoring matrix replaces intuition-based automation selection with a reproducible, auditable decision framework.

## When To Use

- Pre-RPA or intelligent automation initiative where automation candidates must be ranked objectively
- Process variance analysis where conformance checking reveals deviations between documented and actual flows
- Cost reduction initiative where high-volume, rule-based processes need to be identified from system data
- Audit or compliance context where process evidence must come from system logs, not interviews
- Digital transformation assessment needing a portfolio of automation opportunities with ROI estimates

## When NOT To Use

- Processes with no digital event trail (fully manual, paper-based) — mining requires event logs
- Highly creative or judgment-intensive processes (strategy, design) — automation readiness score will be below threshold
- Processes changing faster than the mining cycle — the discovered model is stale before recommendations land
- Organizations without access to process mining tooling or data engineering capability to extract event logs
- When the goal is process improvement rather than automation — use BPMN and business process analysis instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-process-mining.xml` | Definition, BA competencies required, four-step workflow (extract → discover → conform → enhance), tool landscape |
| `content/02-automation-assessment.xml` | Automation candidate scoring criteria with weights, RPA vs. intelligent automation comparison, key vendor landscape, market data |
| `content/03-examples.xml` | Automation assessment matrix scored example, ROI estimate structure, recommendation thresholds |

## Templates

| File | Purpose |
|------|---------|
| `templates/automation-assessment.md` | Process overview, 6-criterion readiness scoring table, recommendation bands, and ROI estimate section |
