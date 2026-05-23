-- purpose: Slowly Changing Dimension Type 2 template.
-- consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
-- produces: a data-modeling artefact validating against scripts/validate-data-modeling.py
-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml
-- token-budget-impact: ~400-1500 tokens once filled
-- SCD Type 2 dimension table with upsert procedure
-- Full history: one row per version; valid_from/valid_to/is_current pattern
-- Engine: PostgreSQL

CREATE TABLE dim_customer (
    surrogate_key   BIGSERIAL    PRIMARY KEY,
    customer_nk     VARCHAR(50)  NOT NULL,  -- natural/business key

    -- SCD Type 2 versioning columns
    valid_from      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    valid_to        TIMESTAMPTZ,            -- NULL = current record
    is_current      BOOLEAN      NOT NULL DEFAULT TRUE,

    -- Change hash: MD5 of all tracked attributes for change detection
    hash_diff       TEXT         NOT NULL,

    -- Dimension attributes (tracked for history)
    first_name      VARCHAR(255),
    last_name       VARCHAR(255),
    email           VARCHAR(255),
    country_code    CHAR(2),
    tier            VARCHAR(30),

    -- ETL audit columns
    load_dts        TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    record_source   VARCHAR(100) NOT NULL
);

-- Indexes
CREATE INDEX idx_dim_customer_nk_current
    ON dim_customer(customer_nk)
    WHERE is_current = TRUE;

CREATE UNIQUE INDEX uq_dim_customer_nk_current
    ON dim_customer(customer_nk)
    WHERE is_current = TRUE;  -- enforce single current record per natural key

CREATE INDEX idx_dim_customer_valid
    ON dim_customer(customer_nk, valid_from, valid_to);


-- -------------------------------------------------------------------
-- Upsert procedure: call once per source row on each ETL run
-- Handles: no change (skip), attribute change (expire + insert), new (insert)
-- -------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE upsert_dim_customer(
    p_customer_nk   VARCHAR(50),
    p_first_name    VARCHAR(255),
    p_last_name     VARCHAR(255),
    p_email         VARCHAR(255),
    p_country_code  CHAR(2),
    p_tier          VARCHAR(30),
    p_record_source VARCHAR(100)
)
LANGUAGE plpgsql AS $$
DECLARE
    v_hash_diff TEXT;
    v_existing  RECORD;
    v_now       TIMESTAMPTZ := NOW();
BEGIN
    -- Compute hash of all tracked attributes
    v_hash_diff := MD5(
        COALESCE(p_first_name,   '') ||
        COALESCE(p_last_name,    '') ||
        COALESCE(p_email,        '') ||
        COALESCE(p_country_code, '') ||
        COALESCE(p_tier,         '')
    );

    -- Find current record (if any)
    SELECT * INTO v_existing
    FROM dim_customer
    WHERE customer_nk = p_customer_nk AND is_current = TRUE;

    IF NOT FOUND THEN
        -- New natural key: insert first version
        INSERT INTO dim_customer (
            customer_nk, first_name, last_name, email, country_code, tier,
            hash_diff, valid_from, valid_to, is_current, record_source
        ) VALUES (
            p_customer_nk, p_first_name, p_last_name, p_email, p_country_code, p_tier,
            v_hash_diff, v_now, NULL, TRUE, p_record_source
        );

    ELSIF v_existing.hash_diff <> v_hash_diff THEN
        -- Attributes changed: expire current row and insert new version
        UPDATE dim_customer
        SET    valid_to   = v_now,
               is_current = FALSE
        WHERE  surrogate_key = v_existing.surrogate_key;

        INSERT INTO dim_customer (
            customer_nk, first_name, last_name, email, country_code, tier,
            hash_diff, valid_from, valid_to, is_current, record_source
        ) VALUES (
            p_customer_nk, p_first_name, p_last_name, p_email, p_country_code, p_tier,
            v_hash_diff, v_now, NULL, TRUE, p_record_source
        );
    END IF;
    -- If hash is unchanged: no action needed
END;
$$;

-- Usage:
-- CALL upsert_dim_customer('C-1001', 'John', 'Doe', 'john@example.com', 'US', 'gold', 'crm-system');
