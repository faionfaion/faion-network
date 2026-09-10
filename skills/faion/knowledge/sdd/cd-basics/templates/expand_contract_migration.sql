-- __faion_header_v1__
-- purpose: Expand–contract migration: phase 1 (add nullable column) + phase 2 (backfill) + phase 3 (drop old)
-- consumes: see content/02-output-contract.xml
-- produces: spec
-- depends-on: content/01-core-rules.xml#expand-contract-migrations
-- token-budget-impact: ~240 tokens when loaded as context
--
-- Three phases, three DEPLOYS. Phase 3 never ships in the same commit as the
-- code that stops reading the old column (rule expand-contract-migrations);
-- the first version of this file dropped `email_old`, a column no phase here
-- creates and nothing else in the methodology mentions.

-- PHASE 1: expand. Deploy with the new column nullable; old code ignores it.
ALTER TABLE users ADD COLUMN IF NOT EXISTS email_canonical TEXT;

-- PHASE 2: backfill. Run as a job, in batches, idempotent — re-running it
-- touches only rows still NULL. Application code now writes BOTH columns.
UPDATE users
   SET email_canonical = LOWER(TRIM(email))
 WHERE email_canonical IS NULL;

-- Gate before phase 3: nothing left to backfill, and readers have switched.
-- Expect 0. If it is not 0, phase 3 does not run.
SELECT COUNT(*) AS still_null FROM users WHERE email_canonical IS NULL;

-- PHASE 3: contract. Only after every writer writes email_canonical and every
-- reader reads it — a separate deploy, after the gate above returns 0.
-- Rename first, drop later: the rename is instant and reversible, the drop is not.
ALTER TABLE users RENAME COLUMN email TO email_old;
-- ...one more release cycle with email_old unused, then:
-- ALTER TABLE users DROP COLUMN email_old;
