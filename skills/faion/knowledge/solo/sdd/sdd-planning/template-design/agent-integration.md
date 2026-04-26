# Agent Integration — Template: Design Document

## When to use
- Generating a new `design.md` for any feature that has an approved `spec.md`
- Reviewing an existing design doc for structural completeness against the template
- Calibrating output format when a new design-writing agent is added to the pipeline
- Providing to a Sonnet agent as a fill-in-the-blanks scaffold to reduce hallucination of structure

## When NOT to use
- Before `spec.md` is approved — template fields will be guesswork without grounded requirements
- For a task that affects a single file — full design doc overhead is unjustified; write the task directly
- As a living document — design.md should be frozen after approval; use task files for implementation details
- As a substitute for `contracts.md` — API endpoints belong in contracts, not in design

## Where it fails / limitations
- Template's "Overview" section (2-3 sentences) forces premature summarization — write it last, not first
- AD options format (A/B bullets) breaks down when there are 4+ viable options — agents collapse them to 2
- "Files" table omits migration rollback scripts and generated files, which are always needed in practice
- Testing strategy section does not distinguish between test-driven (write tests first) and test-after approaches
- Template does not capture API rate limits, external service SLAs, or operational runbooks

## Agentic workflow
A design-generation agent receives the approved spec and constitution as inputs, then instantiates the template section by section. The agent fills AD sections using Opus for decision quality, then fills the remaining structural sections (components, data flow, files, testing, risks) with Sonnet. The FR Coverage table is generated last, as a reconciliation step ensuring every FR from spec.md appears in at least one AD and one file. The completed design is passed to `faion-sdd-reviewer-agent (mode: design)` before being saved.

### Recommended subagents
- `faion-sdd-reviewer-agent (mode: design)` — structural review against this template; checks all required sections
- Opus agent (ad-hoc) — invoke specifically for the AD sections; Sonnet produces shallow alternatives

### Prompt pattern
```
Fill design.md template for feature: {feature_name}
Spec: {spec_path} (approved)
Constitution: {constitution_path}

Section order: Reference Documents → Overview → Architecture Decisions →
Components → Data Flow → Data Models → API Endpoints → Files → Testing → Risks → FR Coverage

Fill section by section. For each AD: minimum 2 alternatives, explicit rationale, traces to FR-X.
Do not write Overview until all other sections are complete.
```

```
Review design.md structural completeness:
- All required sections present?
- Each AD: Context, Options (min 2), Decision, Rationale, Consequences, Traces to?
- Files table: every file from design has Action (CREATE/MODIFY/DELETE)?
- FR Coverage table: every FR-X from spec has entry with AD and Files?
- Testing strategy: unit AND integration targets?
- Risks table: Impact, Probability, Mitigation for each risk?
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `grep -c "^#### AD-"` | Count architecture decisions (good designs: 3-7) | built-in |
| `grep "Traces to"` | Verify all ADs trace to functional requirements | built-in |
| `grep "^| CREATE\|^| MODIFY\|^| DELETE"` | Extract file change list for implementation plan | built-in |
| `markdownlint design.md` | Lint markdown structure | `npm i -g markdownlint-cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Structurizr | OSS/SaaS | Yes | DSL-based C4 diagrams; generate from component section |
| PlantUML | OSS | Yes | Component and sequence diagrams from text; Docker image |
| GitHub | SaaS | Yes | Design docs stored as markdown; PR review for approval |
| Backstage TechDocs | OSS | Partial | Renders design docs in developer portal; needs mkdocs setup |

## Templates & scripts
The canonical template is in `README.md` of this methodology. Copy as-is, then fill.

Section completeness checker:
```python
import re

REQUIRED_SECTIONS = [
    "## Reference Documents",
    "## Overview",
    "## Architecture Decisions",
    "## Components",
    "## Data Flow",
    "## Files",
    "## Testing Strategy",
    "## Risks",
    "## FR Coverage",
]

def check_design_sections(design_text: str) -> list[str]:
    missing = []
    for section in REQUIRED_SECTIONS:
        if section not in design_text:
            missing.append(section)
    return missing

def count_ads(design_text: str) -> int:
    return len(re.findall(r"^### AD-\d+", design_text, re.MULTILINE))

def check_fr_traceability(design_text: str) -> list[str]:
    ads = re.findall(r"(AD-\d+).*?(?=### AD-|\Z)", design_text, re.DOTALL)
    missing_traces = []
    for ad_block in ads:
        if "Traces to" not in ad_block:
            ad_id = re.search(r"AD-\d+", ad_block)
            if ad_id:
                missing_traces.append(ad_id.group())
    return missing_traces
```

## Best practices
- Fill the FR Coverage table last — it catches missed requirements that were not assigned to any AD or file
- Write each AD as a standalone mini-ADR: someone reading only that AD must understand the full decision context
- "Consequences" subsection in each AD is the most valuable part for future agents — do not skip it
- Keep the Files table synchronized with the implementation plan; drift here causes task conflicts
- API Endpoints section must say "See contracts.md" if `contracts.md` exists — never redefine endpoints
- Mark design status explicitly (Draft / Review / Approved) and do not modify after Approved
- Version bump design.md if significant changes are needed post-approval; link old version in git history

## AI-agent gotchas
- Agents generate AD-1, AD-2 labels but start content with AD-001 in body — use consistent numbering
- "Alternatives Considered" tables are frequently filled with straw men (obviously inferior options) rather than real alternatives — reviewer must check
- Data Models section: agents omit constraint column, which causes migration failures when executor implements
- Agents write "See spec.md" in Overview instead of summarizing — Overview must add technical context, not just reference
- Template's component diagram placeholder causes agents to insert ASCII art — replace with a description or directory tree
- Files table misses test files — agents stop after source files; tests are required entries

## References
- [Architecture Decision Records — Michael Nygard pattern](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [C4 Model — lightweight architecture documentation](https://c4model.com/)
- [RFC 2119 — requirement level keywords (MUST/SHOULD)](https://www.rfc-editor.org/rfc/rfc2119)
- [Design Doc best practices — Google eng practices](https://google.github.io/eng-practices/)
