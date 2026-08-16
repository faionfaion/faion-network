# Rust Project Structure (Axum/Actix)

## Summary

**One-sentence:** src/{config,error,routes,handlers,services,models,db,middleware}/ layout with AppState behind Arc; main.rs ≤80 lines; new modules added via scaffold script.

**One-paragraph:** Directory layout for Rust HTTP services: src/{config,error,routes,handlers,services,models,db,middleware}/ with a single AppState struct holding Arc-wrapped resources, main.rs limited to ~80 lines (config + state + router + serve), and a new-module scaffold that creates the model + db + service + handler + route stub for a new entity. Output is the Cargo project skeleton + scaffold script.

**Ефективно для:**

- Greenfield Rust service onboarding.
- Standardising layout across multiple Rust services in one organisation.
- Adding a new entity quickly with the scaffold script.
- Keeping main.rs slim so the wiring stays readable.

## Applies If (ALL must hold)

- Rust HTTP service (Axum or Actix-web).
- Team owns more than one Rust service and wants a common shape.
- Service has multiple resources / entities (orders, users, products).
- Layout is allowed to be slightly larger than 'one file' for clarity.

## Skip If (ANY kills it)

- Tiny CLI / one-off script — flat layout wins.
- Library crate exposing a single trait — module-by-feature is simpler.
- Embedded / no_std code.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Crate name | string | team |
| Resource list | yaml / md | team |
| Cargo.toml dependencies | list | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-modules` | sonnet | Module choice needs judgement when adding new layers. |
| `draft-main` | sonnet | main.rs wiring benefits from sonnet. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/main_rs.rs` | main.rs ≤80 lines: config + state + router + serve |
| `templates/new_module.sh` | Scaffold model+db+service+handler+route stubs for a new entity |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-project-structure.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/dev/backend-systems/`
- [[rust-backend]]
- [[rust-http-handlers]]
- [[rust-error-handling]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/main_rs.rs`

```rust
// src/main.rs — ≤80 lines: config, state, router composition, serve.
use std::sync::Arc;

use axum::Router;
use tower_http::trace::TraceLayer;

mod config;
mod db;
mod error;
mod handlers;
mod middleware;
mod models;
mod routes;
mod services;

use crate::{config::Config, db::Database};

#[derive(Clone)]
pub struct AppState {
    pub db:     Database,
    pub config: Arc<Config>,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();

    let config = Config::from_env()?;
    let db = Database::connect(&config.database_url).await?;

    let state = AppState { db, config: Arc::new(config) };

    let app = Router::new()
        .nest("/api/v1", routes::api_routes())
        .layer(TraceLayer::new_for_http())
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    tracing::info!("listening on http://0.0.0.0:3000");
    axum::serve(listener, app).await?;
    Ok(())
}
```

### `templates/new_module.sh`

```bash
# new_module.sh <name>
# Creates stub files for a new domain entity across routes/handlers/services/db/models.
# Usage: ./scripts/new_module.sh products
set -euo pipefail

N="${1:?Usage: new_module.sh <name>}"

for dir in routes handlers services db models; do
    f="src/$dir/${N}.rs"
    if [ -e "$f" ]; then
        echo "ERROR: $f already exists" >&2
        exit 1
    fi
    printf "// %s/%s.rs\n\n// TODO: implement %s %s\n" "$dir" "$N" "$dir" "$N" > "$f"
    # Add pub mod declaration if not present
    MOD="src/$dir/mod.rs"
    if ! grep -q "pub mod $N;" "$MOD" 2>/dev/null; then
        echo "pub mod $N;" >> "$MOD"
    fi
    echo "created $f"
done

echo "Done. Created $N stubs in routes/handlers/services/db/models."
echo "Next: implement each file, then register routes in src/routes/mod.rs."
```
