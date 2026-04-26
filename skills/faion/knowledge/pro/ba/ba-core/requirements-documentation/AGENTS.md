# Requirements Documentation

## Summary

Produce sign-off-ready requirements sets (BRD + URS + SRS/FRD) aligned to a single locked standard (IEEE 830-1998 or ISO/IEC/IEEE 29148:2018). Write functional requirements in EARS patterns (Ubiquitous, Event-driven, State-driven, Optional, Unwanted-behaviour, Complex). Validate structure via a YAML conformance schema before any document is rendered to PDF. Source is Markdown with frontmatter; the PDF is a generated artifact via pandoc.

## Why

Unstructured requirements documents with ambiguous phrasing ("should be fast", "easy to use"), no acceptance criteria, and no version control produce test gaps and failed audits. EARS patterns map cleanly to test scaffolds, a conformance schema catches missing sections before review, and pandoc-from-Markdown gives a diffable source that generates a deterministic PDF.

## When To Use

- Producing a classical, sign-off-ready requirements set for regulated work (IEC 62304, ISO 26262, DO-178C, BCBS 239, SOC2 audits)
- A vendor or client contract names a specific standard (IEEE 830, ISO 29148, IREB CPRE) and the deliverable list is fixed
- Hand-off across organizations where the document is the contract artifact
- Re-baselining: a previously approved pack must be re-issued at v2.0 with a redline, changelog, and fresh sign-off
- Auditors will physically read a PDF expecting: cover page, version table, approval block, glossary, traceability matrix, requirement IDs

## When NOT To Use

- Solo or agile project where spec.md + acceptance tests already cover the audit surface
- Team has no document custodian — without a named owner the formal apparatus rots within two sprints
- Discovery work where requirements are still volatile — formal docs imply a baseline; baselining in flux is theatre
- Internal tooling for one team — lightweight user stories are sufficient
- The reviewer pool will not actually sign — unsigned formal docs are worse than informal ones

## Content

| File | What's inside |
|------|---------------|
| `content/01-doc-model.xml` | Requirements hierarchy (BR/SR/FR/NFR), document-set structure (BRD/URS/SRS/FRD), SMART attributes, EARS patterns |
| `content/02-agentic.xml` | Scaffolder and EARS-formatter prompt patterns, four-role pipeline, AI gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/brd-template.md` | Business Requirements Document with cover, version, approval, and BR table sections |
| `templates/user-story-template.md` | Agile user story with Gherkin acceptance criteria |
| `templates/srs-conformance.yaml` | IEEE 830-aligned conformance schema for CI validation |
| `templates/srs_conform.py` | Python validator that fails CI when mandatory sections or phrasing rules are violated |
