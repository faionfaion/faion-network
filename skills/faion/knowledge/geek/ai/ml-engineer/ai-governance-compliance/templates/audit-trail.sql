-- purpose: Hash-chained append-only audit table DDL
-- consumes: Inputs declared in `AGENTS.md` Prerequisites.
-- produces: Filled artefact for `ai-governance-compliance` matching `content/02-output-contract.xml`.
-- depends-on: `content/01-core-rules.xml`, `scripts/validate-ai-governance-compliance.py`.
-- token-budget-impact: small.
-- Minimal append-only audit table for ai-governance-compliance artefacts.
CREATE TABLE IF NOT EXISTS ai_governance_compliance_audit (
    id BIGSERIAL PRIMARY KEY,
    produced_at TIMESTAMPTZ NOT NULL,
    owner TEXT NOT NULL,
    approver TEXT NOT NULL,
    payload JSONB NOT NULL,
    hash TEXT NOT NULL
);

-- Forbid UPDATE / DELETE — append-only.
CREATE OR REPLACE RULE no_update AS ON UPDATE TO ai_governance_compliance_audit DO INSTEAD NOTHING;
CREATE OR REPLACE RULE no_delete AS ON DELETE TO ai_governance_compliance_audit DO INSTEAD NOTHING;
