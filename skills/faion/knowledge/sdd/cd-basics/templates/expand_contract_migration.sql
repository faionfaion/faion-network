-- __faion_header_v1__
-- purpose: Expand–contract migration: phase 1 (add nullable column) + phase 2 (backfill) + phase 3 (drop old)
-- consumes: see content/02-output-contract.xml
-- produces: spec
-- depends-on: content/01-core-rules.xml#expand-contract-migrations
-- token-budget-impact: ~240 tokens when loaded as context
-- faion_header_json: {"__faion_header__":{"purpose":"Expand\u2013contract migration: phase 1 (add nullable column) + phase 2 (backfill) + phase 3 (drop old)","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#expand-contract-migrations","token_budget_impact":"~240 tokens when loaded as context"}}
-- PHASE 1: expand (deploy with new column nullable)
ALTER TABLE users ADD COLUMN email_canonical TEXT;

-- PHASE 2: backfill (run as a job; idempotent)
UPDATE users SET email_canonical = LOWER(TRIM(email)) WHERE email_canonical IS NULL;

-- PHASE 3: contract (only after writers stopped using old column)
ALTER TABLE users DROP COLUMN email_old;
