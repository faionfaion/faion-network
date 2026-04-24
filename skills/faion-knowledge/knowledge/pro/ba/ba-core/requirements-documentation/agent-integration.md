# Agent Integration — Requirements Documentation (BA Core)

> Sibling note: `business-analyst/requirements-documentation/agent-integration.md` covers the broad documentation pipeline (BRD vs `spec.md` vs sprint stories). This file is the **ba-core** angle: formal-document fundamentals — BRD / FRD / URS / SRS templates, IEEE 830, ISO/IEC/IEEE 29148, INVEST, EARS, doc identity / version / approval mechanics — and how to drive them with subagents without losing the formal rigour. Read both; do not duplicate content.

## When to use
- Producing a **classical, sign-off-ready requirements set** (BRD + URS + SRS + FRD) for regulated work: medical (IEC 62304), automotive (ISO 26262), aerospace (DO-178C), banking, government tenders, ISO/SOC2 audits.
- A vendor / client contract names a specific standard (`IEEE 830-1998`, `ISO/IEC/IEEE 29148:2018`, `IREB CPRE`) and the deliverable list is fixed.
- Hand-off across organisations where the **document** is the contract artefact: solution requirements travel from the customer's BA team to a build vendor and must survive without the original authors.
- Re-baselining: a previously approved requirements pack must be re-issued at v2.0 with a redline + changelog and fresh sign-off.
- When auditors will physically read a PDF — not browse a Markdown tree — and look for: cover page, version table, approval block, glossary, traceability matrix, requirement IDs.
- Building a glossary / data dictionary as a first-class document (not a sub-section of an SRS) for a domain with strong terminology overlap (insurance, healthcare, finance).

## When NOT to use
- A solo/agile project where the **code is the contract**: `spec.md` + acceptance tests already cover the audit surface.
- The team has no document custodian — without a named owner who maintains `version`, `approval`, `change-history`, the formal apparatus rots within two sprints.
- Discovery work where requirements are still volatile. Formal docs imply a baseline; baselining in flux is theatre.
- Internal tooling for one team — overhead of formal templates outweighs benefit; use lightweight user stories.
- The reviewer pool will not actually sign. Unsigned formal docs are worse than informal ones because they imply a contract that does not exist.

## Where it fails / limitations
- **Template fundamentalism.** BAs paste a 60-section IEEE 830 outline, then half is left blank or filled with "N/A". Use a **scaled template** that explicitly drops sections instead of stubbing them.
- **BRD ≠ FRD ≠ URS confusion.** Teams treat these as synonyms and produce overlapping content. BRD = *why* (business); URS = *what users need* (operational); SRS / FRD = *what the system shall do* (functional + NFR). Agent prompts must enforce the boundary.
- **INVEST misapplied to non-stories.** INVEST is for user stories, not FRs. Applying "Estimable / Small" to an FR pushes BAs to fragment requirements until they become tasks. Keep INVEST for the story-card view; use SMART + IEEE 830 quality attributes for FR-level docs.
- **EARS adoption fails silently.** Teams claim EARS but write only `Ubiquitous` ("The system shall...") and never `Event-driven` (`When ... the system shall...`) or `State-driven` (`While ... the system shall...`) or `Optional` (`Where ... the system shall...`). Result is unconditional requirements that under-specify state machines.
- **Approval block as ritual.** Names without dated, versioned signatures = no audit trail. Tie sign-off to a Git tag or a signed PDF; agents cannot forge dates.
- **Glossary drift.** Same term defined three different ways across BRD/URS/SRS. Force a single `glossary.md` referenced by all three.
- **Numbering archaeology.** `REQ-FR-001` vs `FR-1` vs `1.4.2.1` — three doc generations, no mapping. Lock a numbering convention in `constitution.md` before a single REQ is written.
- **PDF-only delivery.** A signed PDF is the contract output, but the *source* must be diff-able Markdown. Agents that edit PDFs directly destroy provenance.

## Agentic workflow

The ba-core take treats requirements docs as a **multi-document set** with strict document identity (`{doc_type, version, status, approval_date}`) and a single source-of-truth tree from which BRD / URS / SRS / FRD are rendered. Drive it with a four-role pipeline: (1) a **scaffolder** instantiates the standards-correct outline (IEEE 830 §5 or ISO 29148 clause 9) for the chosen doc type; (2) a **populator** fills sections from elicitation transcripts and the shared `glossary.md`, applying SMART for atomic requirements and EARS for FR phrasing; (3) a **conformance checker** validates structure (mandatory sections present, version table populated, every requirement has an ID, source, priority, AC) against a YAML schema; (4) a **renderer** emits PDF/DOCX via pandoc with a deterministic cover page, version history, approval block, and traceability matrix. `faion-feature-executor` should not move a feature out of `todo/` until the conformance checker passes; the SDD `spec.md` becomes the FRD section, and a separate `BRD.md` is rendered for sponsors.

### Recommended subagents
- `faion-sdd-executor-agent` — owns `spec.md` per feature; treats the FR section as authoritative and forbids editing the rendered FRD directly.
- `faion-feature-executor` — wires scaffolder → populator → checker as a quality gate before estimation; refuses to advance a feature lacking a glossary entry for any non-trivial term used in its requirements.
- `faion-brainstorm` — diverge to surface NFR categories (security, usability, observability, compliance, accessibility, locale, performance, capacity, portability, maintainability) the standards-template lists but the populator skipped; converge to keep only those that apply.
- `password-scrubber-agent` — pre-render pass over the source tree before pandoc emits a PDF that may leave the company perimeter.
- A custom `ba-doc-scaffolder` (haiku) — emits the empty document outline given `{doc_type, standard, scale}` and a list of mandatory sections.
- A custom `ba-doc-conformance` (sonnet) — runs the YAML-schema check, reports missing sections / IDs / priorities / sources / AC.
- A custom `ba-ears-formatter` (sonnet) — rewrites unconditional FRs into the correct EARS pattern (`Ubiquitous` / `Event-driven` / `State-driven` / `Optional` / `Unwanted-behaviour` / `Complex`).
- A custom `ba-glossary-curator` (sonnet) — extracts candidate terms from the corpus, deduplicates against `glossary.md`, proposes definitions, never edits an approved term in place.

### Prompt pattern

Scaffolder:
```xml
<role>BA standards scaffolder. Emit empty document outline only.</role>
<inputs>
  <doc_type>{BRD|URS|SRS|FRD|Glossary}</doc_type>
  <standard>{IEEE-830-1998|ISO-29148-2018|IREB-CPRE}</standard>
  <scale>{minimal|standard|regulated}</scale>
</inputs>
<rules>
  Emit Markdown with section headings only, no example content.
  Include cover page, version history table, approval block, glossary reference.
  For SRS / FRD: include sections for Functional, Non-Functional (Performance, Security, Usability, Reliability, Compatibility, Maintainability, Portability), Interfaces, Constraints, Assumptions, Traceability Matrix.
  Mark sections optional-for-{scale} as `<!-- optional: scale=minimal -->` so populator may skip.
</rules>
```

EARS formatter (one requirement per call):
```xml
<task>Rewrite requirement {req_id} into the correct EARS pattern.</task>
<patterns>
  Ubiquitous:    "The {system} shall {response}."
  Event-driven:  "When {trigger}, the {system} shall {response}."
  State-driven:  "While {state}, the {system} shall {response}."
  Optional:      "Where {feature included}, the {system} shall {response}."
  Unwanted:      "If {trigger}, then the {system} shall {response}."
  Complex:       Combine the above; one pattern per sentence.
</patterns>
<output>JSON: {req_id, original, ears_pattern, rewritten, rationale, fallback_if_unchanged}</output>
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandoc` | Render Markdown source → DOCX/PDF with a custom cover-page template and reference docx | https://pandoc.org |
| `pandoc-crossref` | Numbering for figures, tables, and requirements across a multi-doc set | https://lierdakil.github.io/pandoc-crossref/ |
| `vale` | Prose linter; ban "should/may/might" in `shall`-only documents | https://vale.sh |
| `markdownlint-cli2` | Heading-level + link-validity lint per IEEE 830 outline | `npm i -g markdownlint-cli2` |
| `yq` | Validate YAML frontmatter on every REQ-XXX file (id, type, priority, source, traces_to) | https://github.com/mikefarah/yq |
| `git-lfs` | Track signed PDFs alongside Markdown sources | `git lfs install` |
| `cosign` | Sign released PDFs with a developer key for tamper evidence | https://github.com/sigstore/cosign |
| `pdftotext` (poppler) | Diff a re-rendered PDF against the previous baseline before re-issue | `apt install poppler-utils` |
| `mkdocs-material` + `mkdocs-mermaid2-plugin` | Browseable HTML mirror of the doc set | `pip install mkdocs-material` |
| `req-if-converter` (OSS) | Convert ReqIF (DOORS export) → Markdown source-of-truth | https://github.com/ReqIF |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| IBM ENGINEERING DOORS Next | SaaS / on-prem | OSLC + REST | Standard for regulated industries; ReqIF round-trip with Markdown |
| Jama Connect | SaaS | REST + webhooks | Strong baselining and review cycles; agents can post / fetch via REST |
| Polarion ALM | SaaS / on-prem | REST + WebDAV | Heavy enterprise; aligned to ASPICE / IEC 62304 |
| codeBeamer | SaaS / on-prem | REST | Niche but strong traceability for safety-critical |
| Visure Requirements | SaaS | REST | Lightweight; covers IREB and IEEE templates out-of-box |
| ReqView | Desktop / OS-agnostic | OpenSpecTrace + JSON | Cheapest for solo / consultancy use |
| Modern Requirements4DevOps | SaaS | Azure DevOps API | Inside ADO; renders BRD / FRD / URS as Word from work items |
| Aha! | SaaS | REST + GraphQL | Roadmap to requirements link; weaker on formal sign-off |
| Notion + GitHub source | SaaS / OSS | REST + gh CLI | Cheap "good enough" for non-regulated work; agents own the GitHub side |
| Sphinx-Needs (`sphinx-needs`) | OSS | Python | Pure Markdown / RST source; ideal for fully agentic, audit-friendly |

## Templates & scripts

See sibling `business-analyst/requirements-documentation/templates.md` for BRD / User-Story templates and the existing `req-lint.sh`. Inline below: a YAML conformance schema for a regulated SRS document, plus a Python validator that fails CI when mandatory sections are missing.

```yaml
# srs-conformance.yaml
doc_type: SRS
standard: IEEE-830-1998
mandatory_sections:
  - "1. Introduction"
  - "1.1 Purpose"
  - "1.2 Scope"
  - "1.3 Definitions, Acronyms, Abbreviations"
  - "1.4 References"
  - "1.5 Overview"
  - "2. Overall Description"
  - "3. Specific Requirements"
  - "3.1 External Interfaces"
  - "3.2 Functional Requirements"
  - "3.3 Performance Requirements"
  - "3.4 Logical Database Requirements"
  - "3.5 Design Constraints"
  - "3.6 Software System Attributes"
  - "Appendix A. Traceability Matrix"
mandatory_frontmatter:
  - doc_id
  - version
  - status        # Draft | InReview | Approved | Superseded
  - approval_date
  - owner
  - glossary_ref
requirement_rules:
  id_pattern: "^(BR|UR|FR|NFR)-[0-9]{3}$"
  required_fields: [id, type, priority, source, ac]
  forbidden_words: [fast, slow, easy, user-friendly, intuitive, robust, seamless]
  shall_only: true   # reject "should" / "may" / "might"
```

```python
# srs_conform.py — fail CI if SRS source violates the schema.
import re, sys, yaml
from pathlib import Path

schema = yaml.safe_load(Path("srs-conformance.yaml").read_text())
src = Path(sys.argv[1])
text = src.read_text()
errs: list[str] = []

for s in schema["mandatory_sections"]:
    if s not in text:
        errs.append(f"missing section: {s}")

fm_match = re.search(r"^---\n(.*?)\n---", text, re.S)
fm = yaml.safe_load(fm_match.group(1)) if fm_match else {}
for k in schema["mandatory_frontmatter"]:
    if k not in fm:
        errs.append(f"missing frontmatter: {k}")

req_pat = re.compile(schema["requirement_rules"]["id_pattern"])
for line in text.splitlines():
    m = re.match(r"^\s*[-*]\s*\*\*(REQ-[A-Z]{2}-\d{3})\*\*", line)
    if m and not req_pat.match(m.group(1).removeprefix("REQ-")):
        errs.append(f"bad id: {m.group(1)}")

for w in schema["requirement_rules"]["forbidden_words"]:
    for n, ln in enumerate(text.splitlines(), 1):
        if re.search(rf"\b{w}\b", ln, re.I):
            errs.append(f"line {n}: forbidden word '{w}'")

if schema["requirement_rules"]["shall_only"]:
    for n, ln in enumerate(text.splitlines(), 1):
        if re.search(r"\b(should|may|might)\b", ln, re.I):
            errs.append(f"line {n}: non-shall modal in '{ln.strip()[:60]}'")

if errs:
    sys.stderr.write("\n".join(errs) + "\n"); sys.exit(1)
```

## Best practices
- Pick **one** standard per project (IEEE 830 *or* ISO/IEC/IEEE 29148) and freeze it in `constitution.md`. Mixing produces section-name skew.
- Maintain `BRD.md`, `URS.md`, `SRS.md`/`FRD.md`, and `glossary.md` as separate files at separate ID prefixes (`BR-`, `UR-`, `FR-`, `NFR-`). One requirement per file remains the source-of-truth.
- Write FRs in EARS form. The five canonical patterns map cleanly to test scaffolds (`when` → trigger, `while` → setup state, `where` → feature flag).
- Keep INVEST for the **story-card view** rendered for sprints; do not retrofit Estimable/Small onto formal FRs — they break atomicity.
- Version the document, not just the requirements: `BRD v1.4.0` follows semver-like rules — patch for typos, minor for added requirements, major for scope/baseline change requiring re-sign-off.
- Approval block names a role + named individual + date + Git tag (`approved-2026-04-15-srs-v1.0`). Tags are signed, dates immutable.
- Render PDFs from Markdown with pandoc; never edit PDFs by hand. Track the rendered PDF via Git LFS so reviewers diff source, not output.
- Maintain a single Traceability Matrix (Appendix A of SRS) auto-generated from `traces_to:` frontmatter. Manual matrices rot within one sprint.
- For regulated work, attach a Glossary version reference to every doc — `Glossary v0.7` — so a term redefinition forces an explicit re-baseline of dependent docs.
- When migrating from DOORS / Polarion, use ReqIF as the lossless intermediate. CSV exports drop attribute hierarchy.

## AI-agent gotchas
- **Standard hallucination.** Agents confidently produce "IEEE 830-2025" sections that do not exist. Pin the standard in the prompt and reject any structural claim not present in the schema file.
- **EARS pattern collapse.** Models default everything to Ubiquitous (`The system shall...`). Force a per-requirement EARS classification call before phrasing.
- **Modal-verb drift.** RFC 2119 vs IEEE 830 conventions differ; an agent trained on RFCs writes "MAY", "SHOULD" in an SRS that mandates "shall" only. Lint with the schema; reject `may|should|might`.
- **Glossary forks.** Agents redefine an existing term inline rather than reading the glossary. Provide `glossary.md` in context for every populate call and forbid in-doc definitions.
- **Approval-block fabrication.** An agent emitting a populated approval table with names + dates is forging an audit record. Approval table must be a stub the human fills.
- **Section-completeness theatre.** Agents fill every section with "N/A" rather than dropping it. Force "drop or fill" — emit nothing if no content; track section-coverage as a metric.
- **NFR template-numbness.** Models reproduce IEEE 830 §5.5 categories verbatim without adapting to the project. Run a tailoring pass: prune categories that do not apply (e.g., no portability for an internal-only web app).
- **Re-baseline silence.** Agents edit an `Approved` doc in place. Status must be a CI-checked invariant: any change to an `Approved` file must bump version and reset status to `Draft`.
- **PDF render drift.** Re-rendering yields a binary diff (font kerning, generated date). Pin pandoc version, supply a deterministic timestamp (`SOURCE_DATE_EPOCH`), and diff via `pdftotext`.
- **Traceability matrix overload.** A 5,000-row matrix is unreadable. Auto-generate one matrix per top-level capability instead of one project-wide.

## References
- IEEE Std 830-1998 — Recommended Practice for Software Requirements Specifications
- ISO/IEC/IEEE 29148:2018 — Systems and software engineering — Life cycle processes — Requirements engineering
- IREB CPRE Foundation Level Syllabus v3.1 — Requirements engineering glossary and process
- Karl Wiegers & Joy Beatty, "Software Requirements" 3rd ed. — chapters on BRD/URS/SRS distinctions
- Mavin et al., "Easy Approach to Requirements Syntax (EARS)", IEEE RE 2009
- Bill Wake, "INVEST in Good Stories, and SMART Tasks" (XP123, 2003)
- BABOK Guide v3 — Chapter 7: Requirements Analysis and Design Definition
- DO-178C / ED-12C, IEC 62304, ISO 26262 — domain-specific requirement-document mandates
- `business-analyst/requirements-documentation/agent-integration.md` (sibling) — broad pipeline view
- `requirements-traceability/agent-integration.md`, `requirements-validation/agent-integration.md`, `requirements-lifecycle/agent-integration.md` (siblings) — adjacent ba-core methodologies
