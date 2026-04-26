# Requirements Traceability

## Summary

Requirements traceability links every artifact (business requirement, stakeholder requirement, solution requirement, design, code, test) to its origin and its downstream dependents, enabling forward coverage analysis (need → test) and backward justification (test → need). The RTM is a generated artifact, not a hand-edited file: typed links in source artifact frontmatter (`traces: [BR-05, SR-12]`) feed a generator script that builds the matrix and computes coverage metrics. Agents propose links, detect orphans, and walk the graph for impact analysis — they never write the matrix directly.

## Why

Without traceability, a changed business goal propagates invisibly through the artifact stack. Test coverage gaps go undetected until late. Requirements exist without justification and components exist without requirements. In regulated builds, auditors require a complete forward+backward chain from business need to code to test; traceability is the contractual deliverable that enables incremental acceptance in vendor/outsourced delivery.

## When To Use

- Regulated builds (ISO 13485, IEC 62304, ISO 26262, DO-178C, SOX) where auditors demand a complete chain.
- Multi-team programs where a single change request hits four or more artifact types.
- Pairing with `requirements-lifecycle/` and `requirements-validation/` to close the Specify → Verify loop with coverage numbers.
- Migrations where every legacy capability must be provably preserved or explicitly retired.
- Vendor/outsourced delivery where the RTM is the contractual acceptance deliverable.

## When NOT To Use

- Pre-PMF/discovery work — opportunity-solution-trees and lightweight user stories suffice; an RTM ossifies premature decisions.
- Solo developer or 2-person team — `git log --grep` plus issue links already provide enough trace.
- Pure infrastructure/SRE work where requirements are SLOs, not features.
- When the team will not enforce maintenance discipline — an outdated RTM gives false assurance to auditors.

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Traceability directions (forward/backward), coverage analysis, gap analysis, traceability metrics with targets. |
| `content/02-process.xml` | Four-step traceability process: define strategy, create matrix, maintain on change, analyze coverage. Link role vocabulary. |
| `content/03-examples.xml` | E-commerce checkout traceability tree; impact analysis table example; tools and antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rtm.md` | Requirements Traceability Matrix template with coverage summary and orphan/gap sections. |
| `templates/per-req-trace.md` | Single-requirement trace template showing upstream and downstream links with change history. |
| `templates/rtm.py` | Python script generating the RTM from frontmatter `traces:` links across a docs tree. |
