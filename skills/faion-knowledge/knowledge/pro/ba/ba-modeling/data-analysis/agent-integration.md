# Agent Integration — Data Analysis (BA)

## When to use
- Greenfield feature spec needs a data dictionary: agent reads the spec + existing schema, emits new entities + attributes with types, validations, and ownership before any DDL is written.
- Pre-migration data quality assessment: agent profiles a source table, fills the README's six-dimension scorecard (accuracy / completeness / consistency / timeliness / validity / uniqueness), and flags blockers per entity.
- Cross-system definition reconciliation: agent diffs `customer.email` semantics across CRM, billing, and product DBs and produces a canonical definition + mapping table for the data dictionary.
- Conceptual → logical → physical drift check: agent compares `data-dictionary.md` against live schema (Postgres `information_schema`, dbt manifest) and opens issues per drift.
- ERD generation from spec: agent writes Mermaid / dbml ERD from the entity table, keeps it in git, regenerates on every dictionary change.
- Business-rule extraction from legacy code/SQL: agent reads stored procedures or app validators and reverse-engineers the validation/derivation/constraint rule rows for the data dictionary.
- Data-volume sizing for capacity planning: agent reads dictionary + traffic assumptions and produces the README's volumes table (current / 1yr / 3yr).

## When NOT to use
- Greenfield prototypes pre-PMF where the schema changes weekly — formal data dictionaries become stale faster than they are written; use lightweight typed models (Pydantic, Zod) and skip the BA-grade artefact.
- Statistical / exploratory data analysis (EDA, pandas, notebooks) — that is data science, not BA Data Analysis. This methodology is about *requirements* on data, not insights from data.
- Pure ML feature engineering — features evolve through training pipelines, not through a BA-owned dictionary.
- Tiny CRUD apps with under ~10 entities — the ceremony costs more than it saves; a single annotated schema file is sufficient.
- One-off ad-hoc reports where data lives only in a spreadsheet for a week.
- High-trust regulated domains (HIPAA, PCI, SOX) where data classification and lineage MUST be human-signed — agents may draft, humans must approve in writing.

## Where it fails / limitations
- **Definition drift between systems.** The README's data dictionary is single-system; real businesses have the "same" entity (Customer, Order, Product) defined differently in 4-7 systems. The methodology offers no reconciliation pattern, and agents will happily emit one definition without flagging conflicts.
- **No lineage column.** A data element without lineage (source system → transformations → consumers) is half-documented. Agents and humans both omit it because the README's templates do not require it.
- **Static quality scorecard.** The six dimensions are point-in-time; quality decays. Without a recurring re-assessment, the scorecard is outdated within a quarter.
- **PII / classification handled as an afterthought.** "Data Security" is one row at the bottom of the requirements template. In practice, classification (Public / Internal / Confidential / Restricted) drives storage, retention, masking, and access — should be a first-class column on every attribute.
- **Volume estimates without growth model.** The 1yr/3yr columns invite linear extrapolation; agents will plug numbers in without questioning the growth model behind them.
- **No event / state-transition modelling.** Real entities have lifecycles (Order: created → paid → shipped → returned); the methodology models attributes but not state machines, so agents miss invariants like "ShippedDate ≥ PaidDate".
- **Conflates relational with non-relational data.** ERD assumes relational; document stores, event streams, and graph data need different modelling primitives. Agents force everything into entity-attribute-relationship form.
- **Business rules in prose.** The README's rule examples are English sentences; not executable. Agents cannot mechanically verify them without a DSL (e.g., JSON Schema, OPA Rego, dbt tests).

## Agentic workflow
Drive BA Data Analysis as a four-stage pipeline owned by a `data-modeller` subagent: (1) **extract** — ingest the feature spec, existing dictionary, and live schema (`information_schema`, dbt `manifest.json`, Prisma `schema.prisma`); (2) **draft** — produce or update the data dictionary with attributes, validations, classification, lineage, and Mermaid/dbml ERD; (3) **validate** — run quality probes against sample data (Great Expectations / dbt tests / Soda checks) and fill the six-dimension scorecard; (4) **govern** — diff against canonical dictionary, open PRs per drift, request human sign-off for any classification change. Persist `data-dictionary.md`, `erd.mmd`, and `quality-scorecard.md` in git so every agent run is a reviewable diff, never a live mutation.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts approved dictionary changes into SDD tasks (`.product/features/.../todo/`) and lands the corresponding migrations + dbt models with tests.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — mandatory pre-step before any prompt that includes sample rows; data-quality work routinely surfaces emails, IDs, free-text PII.
- A purpose-built **data-modeller agent** (worth creating; not yet in repo): system prompt holds the canonical dictionary + classification rules; tools are read-only DB introspection + git PR creation; output is structured (JSON Schema for entities) so downstream codegen is deterministic.
- A **schema-drift agent** (cron, daily): pulls `information_schema.columns` for tracked DBs, diffs against `data-dictionary.md`, opens GitHub issues per drift (new column, type change, dropped column).
- A **data-quality agent** (cron, weekly): runs Great Expectations / Soda / dbt-test suites, fills the README's quality assessment template, posts a markdown report to `.product/data-quality/scorecard-YYYY-MM-DD.md`.

### Prompt pattern
Dictionary draft from spec:
```
You are a BA data modeller. Read the feature spec in <spec> and the
canonical dictionary in <data-dictionary.md>. Output the diff: new
entities, new attributes on existing entities, deprecated attributes.
For every attribute provide: name (PascalCase entity, snake_case
attr), type, required (Y/N), valid values / range, validation rule
(executable: regex, enum, FK), source system, owner (GitHub handle),
classification (Public/Internal/Confidential/Restricted), lineage
(source → transforms → consumers). Reject any attribute lacking
classification or owner. Output as the README's Data Dictionary
table format plus a Mermaid ER diagram.
```

Quality scorecard:
```
You profiled <table> with sample size <n>. Fill the six-dimension
scorecard (accuracy, completeness, consistency, timeliness, validity,
uniqueness). For each: state metric, finding, examples (redacted),
score (1-5), priority (H/M/L). Use a 4-week rolling window for
timeliness. For consistency, compare against <reference-system>.
No claim without a count + percentage. End with the top three
remediation actions, each with owner and effort estimate.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt` (data build tool) | Logical/physical model + executable tests; the metrics layer agents query | https://docs.getdbt.com |
| `dbt-osmosis` | Auto-propagates column descriptions and tests across dbt models | https://github.com/z3z1ma/dbt-osmosis |
| `great_expectations` | Data quality suites (mapping to README's six dimensions) | https://docs.greatexpectations.io |
| `soda-core` | YAML-defined quality checks runnable in CI | https://docs.soda.io |
| `sqlfluff` | Lint dictionary-bound SQL before agents run it | https://docs.sqlfluff.com |
| `schemaspy` | Generates HTML + ERDs from any JDBC database | https://schemaspy.org |
| `tbls` | CI-friendly DB documentation (markdown + Mermaid ERD) from live schema | https://github.com/k1LoW/tbls |
| `dbml-cli` (`@dbml/cli`) | Render ERDs from `.dbml`; round-trips to SQL | https://dbml.dbdiagram.io/cli |
| `mermaid-cli` (`mmdc`) | Render `erDiagram` Mermaid blocks to SVG/PNG in CI | https://github.com/mermaid-js/mermaid-cli |
| `datacontract-cli` | Lint and verify a Data Contract YAML against a source | https://cli.datacontract.com |
| `sqlglot` | Parse + transpile SQL, extract column lineage programmatically | https://github.com/tobymao/sqlglot |
| `openlineage` / `marquez` | Capture column-level lineage from dbt, Airflow, Spark | https://openlineage.io |
| `presidio` (Microsoft) | PII detection/redaction before LLM ingestion | https://microsoft.github.io/presidio |
| `liquibase` / `flyway` / `alembic` | Migrations as the executable physical model | https://www.liquibase.org / https://flywaydb.org / https://alembic.sqlalchemy.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| dbt Cloud / dbt Core | SaaS / OSS | Yes — manifest.json + REST API | Canonical contract layer; agents read `manifest.json` for typed model graph. |
| dbdiagram.io / dbdocs.io | SaaS | Yes — `.dbml` is plain text, git-versionable | Best-fit when ERD needs to be reviewable in PR. |
| DataHub | OSS (LinkedIn) | Yes — GraphQL + REST | Catalog + lineage; agents push/pull definitions, classifications. |
| OpenMetadata | OSS | Yes — REST + Python SDK | Catalog with column-level lineage and quality test integration. |
| Atlan / Alation / Collibra | SaaS | Partial — REST APIs exist | Enterprise catalogs; SSO + governance gates often slow agent loops. |
| Monte Carlo / Bigeye / Anomalo | SaaS | Yes — APIs for incidents | Observability layer feeding the timeliness dimension automatically. |
| Soda Cloud | SaaS | Yes — checks API | Pairs with `soda-core` for quality reports. |
| Great Expectations Cloud | SaaS | Yes | Hosted GX with API; agents post expectation suites. |
| ERDPlus / Lucidchart / drawio | SaaS / OSS | Partial | drawio + `.drawio` is git-friendly; the others are GUI-bound. |
| dbdiagram, Prisma Studio, Supabase Studio | SaaS / Local | Yes for Prisma / Supabase (text schemas); No for visual editors | Prefer text-first tools so agents can diff. |
| Postgres / MySQL / SQL Server / Snowflake / BigQuery | DB | Yes — `information_schema` / `INFORMATION_SCHEMA.COLUMNS` | Agents introspect live schema as source of truth for physical layer. |
| Apache Atlas | OSS | Yes — REST | Heavyweight; pick only if you already run Hadoop ecosystem. |

## Templates & scripts

The README ships dictionary, requirements, and quality-assessment templates but no enforcement. Two gaps: (a) lineage + classification columns are not required, (b) no automated drift check between dictionary and live schema. Inline drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# data-dictionary-lint.sh — enforce required columns + naming on a
# Data Dictionary that follows ba-modeling/data-analysis/README.md.
# Usage: data-dictionary-lint.sh path/to/data-dictionary.md
set -euo pipefail
file="${1:?usage: data-dictionary-lint.sh DICT.md}"
python3 - "$file" <<'PY'
import re, sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text()
required = {"Name", "Type", "Required", "Owner", "Classification", "Source"}
errs, entities = [], []
# Each Entity block starts with `## Entity:`
for block in re.split(r"(?m)^##\s+Entity:\s*", src)[1:]:
    name = block.splitlines()[0].strip()
    entities.append(name)
    header_match = re.search(r"^\|(.+?)\|\s*$", block, re.M)
    if not header_match:
        errs.append(f"{name}: no attribute table"); continue
    cols = [c.strip() for c in header_match.group(1).split("|")]
    missing = required - set(cols)
    if missing:
        errs.append(f"{name}: missing columns {sorted(missing)}")
    # Validate row content for snake_case attr + non-empty owner/class
    for row in re.findall(r"^\|(?!\s*-)(.+?)\|\s*$", block, re.M)[1:]:
        cells = [c.strip() for c in row.split("|")]
        if len(cells) < len(cols): continue
        d = dict(zip(cols, cells))
        attr = d.get("Name", "")
        if attr and not re.fullmatch(r"[a-z][a-z0-9_]*", attr):
            errs.append(f"{name}.{attr}: not snake_case")
        if not d.get("Owner") or d["Owner"].startswith("TODO"):
            errs.append(f"{name}.{attr}: missing Owner")
        if d.get("Classification") not in {"Public", "Internal", "Confidential", "Restricted"}:
            errs.append(f"{name}.{attr}: invalid Classification")
if errs:
    print("Dictionary lint errors:")
    [print(" -", e) for e in errs]; sys.exit(1)
print(f"OK: {len(entities)} entities, all attributes have owner + classification.")
PY
```

Wire into pre-commit on the repo that owns `data-dictionary.md`. Pair with a daily cron agent that diffs this file against `information_schema.columns` (Postgres) or `INFORMATION_SCHEMA.COLUMNS` (BigQuery/Snowflake) and opens GitHub issues per drift.

## Best practices
- **Classification is mandatory, not optional.** Every attribute carries Public / Internal / Confidential / Restricted; downstream tooling (masking, retention, exports) keys off it.
- **Owner is a human handle, not a team.** "Data team" is unowned. GitHub username or email; one per attribute.
- **Lineage column on every attribute.** `source_system → transforms → consumers`. Without it the dictionary is a graveyard.
- **Executable rules, not English.** Validation expressed as regex, enum, FK, or dbt/GX test ID. Prose rules drift; tests fail loudly.
- **Naming is an ADR.** Pick `snake_case` columns + `PascalCase` entities + singular table names (or the inverse) and write it down once; agents and humans both reference the ADR.
- **Conceptual model first, in Mermaid, in git.** Stakeholder review happens in PR comments, not Visio.
- **Reconcile before extending.** When adding `customer.email`, search every system for an existing `email` column and document the mapping before adding a new one.
- **Quality scorecard is recurring, not point-in-time.** Schedule weekly; treat trend, not snapshot.
- **State machines for entities with lifecycles.** Add a `status` enum + a transitions table; reject transitions outside the table.
- **Retention + DPA columns for any Confidential / Restricted attribute.** Tie to the records-of-processing-activity (Article 30 GDPR) document.
- **Volumes assume an explicit growth model.** Linear / exponential / seasonal; cite the assumption next to the number.
- **Definitions are versioned.** A definition change is a semantic-versioned PR with deprecation notice; consumers get migration time.

## AI-agent gotchas
- **Hallucinated columns.** Agents invent `created_at` / `updated_at` columns that the live schema does not have. Always pass the introspected schema in the prompt and reject any column not present without an explicit ADD task.
- **Type-coercion blind spots.** Agents map `varchar(50)` to `text` interchangeably; in some warehouses (BigQuery STRING vs SQL Server NVARCHAR) the difference matters for collation, length limits, indexing. Pin types to the target dialect.
- **Silent classification downgrade.** Agent re-emits an attribute and drops the `Confidential` tag because it was not in the immediate context. Always include classification of every existing attribute in the prompt; reject diffs that lower classification without an ADR.
- **Definition collision.** Two systems both define `Customer`; agent picks one and overwrites the other. Force a reconciliation step that requires both sources cited before a merge.
- **PII leakage in sample rows.** "Show me 5 example rows" → real emails in a prompt. Always pre-redact via Presidio or run on synthetic samples generated from the schema.
- **Volume math fabrication.** Agents will produce confident 3-year volume numbers from a single growth multiplier. Require the agent to state the model (linear / exp / seasonal) and the assumption inputs; otherwise emit "needs human estimate".
- **Cardinality misnaming.** `1:N` vs `N:M` confusion creates wrong ERDs. Constrain the agent to derive cardinality from FK + uniqueness constraints in `information_schema`, never from prose.
- **Dropped historical context.** Agents rewrite an entity's description, losing the rationale captured by the previous BA. Always require a `change-log` row appended, never a description replacement.
- **No nullability invariants.** Agents flag `Required: Y` but emit no NOT NULL constraint. Bind the dictionary's `Required` column to the migration generator (alembic / liquibase) so they cannot diverge.
- **Inferring meaning from name.** `is_active` is not the same in CRM (current customer) and billing (active subscription). Agents conflate. Force lineage + business definition on every Boolean.
- **Token bombs from full schema dumps.** A 400-table catalog blows the context window. Slice by feature scope; pass only the entities the spec touches.
- **Dictionary becomes the only source of truth, then rots.** Agent updates the dictionary but not the migration; the live schema diverges. Always pair dictionary PRs with migration + dbt tests in the same commit, gated by `tbls`/`schemaspy` diff.
- **Mermaid ERD limits.** Diagrams over ~30 entities become unreadable; agents will keep adding to one file. Force per-bounded-context diagrams (one Mermaid file per domain).

## References
- Chen, P. (1976). "The Entity-Relationship Model — Toward a Unified View of Data." ACM TODS. https://dl.acm.org/doi/10.1145/320434.320440
- IIBA — BABOK v3, Chapter 10.12 "Data Modelling" + 10.13 "Data Dictionary". https://www.iiba.org/standards-and-resources/babok/
- Kimball, R., Ross, M. — "The Data Warehouse Toolkit," 3rd ed. (Conformed dimensions, slowly changing dimensions.) https://www.kimballgroup.com
- DAMA-DMBOK 2 — Data Management Body of Knowledge. https://www.dama.org/cpages/body-of-knowledge
- Hellerstein, J. (2008). "Quantitative Data Cleaning for Large Databases." UN Stats. (Quality dimensions taxonomy.) https://homes.cs.washington.edu/~suciu/cse534/Hellerstein-cleaning.pdf
- "Data Contracts" pattern — Andrew Jones et al. https://datacontract.com
- "Schemata" — Maxime Beauchemin's note on dbt-driven dictionaries. https://medium.com/@maximebeauchemin
- ISO/IEC 11179 — Metadata registries (formal data-element specification). https://www.iso.org/standard/35343.html
- Sibling methodologies in this repo: `pro/ba/ba-modeling/business-process-analysis/`, `pro/ba/ba-modeling/decision-analysis/`, `pro/ba/ba-modeling/interface-analysis/`, `pro/ba/business-analyst/requirements-documentation/`, `solo/dev/api-developer/` (data contracts).
