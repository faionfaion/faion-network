# Hierarchical Index Compression

## Summary

**One-sentence:** Produces an Index Budget Record that bounds what a tiered retrieval index costs to walk — a read ceiling per level, a fan-out that reaches the corpus, entries that discriminate rather than describe, and a numeric shard trigger.

**One-paragraph:** When the graph gate says "no graph, use a hierarchy with compact indexes", this is that hierarchy. The failure it prevents is specific and quiet: index tiers grow with the corpus, each entry acquires a prose summary that restates the leaf it points at, and a lookup ends up paying more for the map than for the destination. Nothing breaks — the answers stay correct — so it is discovered as unexplained context pressure years later. The fix is arithmetic, not machinery. Declare the maximum tokens any single index read may cost; declare the fan-out and depth and check they reach the corpus; cap entries to a discriminator that answers "when would I open this" and nothing else; shard on a number rather than on judgement. Where a corpus already nests, all of that is free restructuring. Where it does not, a recursive summary tree must be built and its build cost budgeted like any other index.

**Ефективно для:**

- A retrieval tree whose index reads now cost more than the bodies they deliver.
- A corpus that already nests — by domain, module, product area — where the hierarchy is free and only the entries need compressing.
- The `warrant: none` exit of a graph decision, which prescribes this structure and stops.
- Deciding between sharding what exists and building a RAPTOR-style summary tree over what does not.

## Applies If (ALL must hold)

- Retrieval routes through one or more index or table-of-contents tiers before reaching content.
- A cost ledger exists showing index reads are a material share of the lookup — this methodology is a remedy, and applying it without the measurement optimises the wrong tier.
- The corpus is too large to enumerate into the context window, and growing.

## Skip If (ANY kills it)

- Index reads are under 20% of lookup cost. The bill is candidates or bodies; compressing the index moves nothing.
- Retrieval is flat vector search with no index the model ever reads — there is no tier to compress.
- The corpus is static, small and fully enumerable in one read that fits the budget; one flat list beats any hierarchy at that size.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Six testable rules. R2 is the one that recovers the most tokens for the least work. |
| `content/02-output-contract.xml` | The Index Budget Record: levels, ceilings, fan-out arithmetic, shard trigger, and what the leaf owns. |
| `content/03-failure-modes.xml` | Six ways a tiered index quietly becomes the bill. |
| `content/06-decision-tree.xml` | Routing from measured index share and corpus shape to shard / build / leave alone. |
| `scripts/validate-hierarchical-index-compression.py` | Validates a record: ceilings, reachability, entry caps, build-cost amortisation. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/index-budget-record.yaml` | Fill-in record; ships valid against the contract. |
| `templates/index-entry-format.md.j2` | The entry shape, with a before/after showing what a discriminator removes. |
| `templates/index-entry-format.md` | The entry shape, with a before/after showing what a discriminator removes. Generated from `templates/index-entry-format.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- `retrieval-cost-per-answer-audit` — the required upstream. It measures the index share; this methodology acts on it. Re-run it afterwards to confirm the cut.
- `context-graph-engineering` — its `warrant: none` exit routes here. This is the structure it declines to replace with a graph.
- `chunking-document-structure` — how a leaf is split. Orthogonal: that governs the body, this governs the map to it.
- `llamaindex-indexes-queries` — one framework's implementation of tiered indexes; the budget arithmetic here is framework-independent and applies to it too.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/index-budget-record.yaml`

```yaml
#
# Validate:  validate-hierarchical-index-compression.py index-budget-record.yaml
#
# The shipped numbers are the TARGET state for the faion-network tree, not its
# state as measured 2026-08-04 (largest single index ~30,000 tokens, well over
# this ceiling). That is the point: a record states the bound, and the level
# that breaches it is what the validator names.

system: "methodology retrieval over a 2600-document corpus"
corpus_size: 2600
median_body_tokens: 3300            # from the upstream cost ledger

# --- Ceiling (r1). Set against the median body, not against the context window. ---
index_read_ceiling_tokens: 4000

# --- Levels, root first. read_tokens is MEASURED, never estimated. ---
levels:
  - name: domains                   # L1: which domain
    entry_count: 20
    read_tokens: 1800
    partition_key: domain
  - name: domain-index              # L2: which leaf, within one domain shard
    entry_count: 160
    read_tokens: 1200
    partition_key: null             # leaf-most index; nothing below it to partition

# --- Shape (r3). fanout^max_depth must reach corpus_size: 160^2 = 25600 >= 2600. ---
max_depth: 2                        # 2 index reads per cold lookup; hard cap is 3
fanout: 160

# --- Entries (r2). Discriminator answers "when would I open this, not its neighbour". ---
discriminator_max_chars: 90
entry_fields: [id, tier, produces, discriminator]
leaf_owns: [summary, body, rationale]   # MUST NOT appear in any index entry

# --- Shard trigger (r4). At or below the ceiling, so the split fires before the breach. ---
shard_trigger_tokens: 4000
shard_stub: true                    # must be true — caller routing does not change

# --- Build (r5). This corpus nests by domain, so the hierarchy is free. ---
corpus_nests_naturally: true
build_pattern: shard                # shard | recursive_summary | hybrid
build_tokens: 0                     # must be 0 for shard
rebuild_trigger: "any leaf added, removed or retiered; stub regenerated in the same job"

# --- Walk skipping (r6). A known leaf path is read directly. ---
skip_walk_when_known: true
```
