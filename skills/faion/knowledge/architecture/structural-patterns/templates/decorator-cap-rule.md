<!-- __faion_header_v1__ -->
<!-- purpose: Lint / convention enforcing decorator stack depth ≤ 2. -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: decision-record; depends-on: content/01-core-rules.xml#r1-signal-to-pattern -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Lint / convention enforcing decorator stack depth \u2264 2.","consumes":"see content/02-output-contract.xml","produces":"decision-record","depends_on":"content/01-core-rules.xml#r1-signal-to-pattern","token_budget_impact":"~150 tokens when loaded"}} -->
# Decorator Stack Cap

Convention
- Maximum decorator stack depth = 2 per call site.
- Cross-cutting concerns (logging, auth, retry, caching, tracing) MUST be composed via a single middleware pipeline.
- Anything beyond depth 2 → refactor to middleware composition or chain-of-responsibility.

Detection
- Static check: count `@decorator` markers per function definition; fail if > 2 across decorator-class symbols.
