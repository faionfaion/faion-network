<!-- purpose: Activity list template (PERT + dependency types) -->
<!-- consumes: WBS work packages -->
<!-- produces: sequenced activity list with FS/SS/FF/SF deps -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens populated -->

# Activity List — <project>

| ID  | Activity (verb-led)         | WBS pkg | Predecessors | Dep type | O | M | P | PERT | Resource | Buffer |
|-----|-----------------------------|---------|--------------|----------|---|---|---|------|----------|--------|
| A01 | Design data model           | 1.2     |              |          | 2 | 3 | 5 | 3.2  | team A   |        |
| A02 | Implement ingest pipeline   | 1.3     | A01          | FS       | 4 | 6 | 10| 6.3  | team A   | 1.5d   |
