<!-- purpose: Minimal viable filled-in version of pr-coaching-comment.md -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~250 tokens when loaded as context -->

# PR coaching comment template

## What worked

- Nice coverage on the happy-path parsing tests (lines 80-120 in OrderParserTest).

## Signals I'd like to discuss

- **library-of-the-day** — `axios` was added to the dependency list. Our codebase standardizes on JdkHttpClient (see services/payment/JdkHttpClient.java). What pushed you toward axios specifically?
- **undefended-exception** — Line 42 catches IOException with `e.printStackTrace();` and continues. What should happen to the request if the upstream call genuinely failed?

## Without-AI check

Walk me through how you'd write lines 38-46 without the AI suggestion. What would your first instinct be? Did the AI suggest anything that surprised you?

## Resolution

- [ ] Address library-of-the-day (block)
- [ ] Address undefended-exception (block)
- [ ] Reply to without-AI question
