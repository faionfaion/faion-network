-- Data Vault 2.0: Hub, Link, Satellite DDL templates
-- Engine: PostgreSQL; replace schema prefix as needed

-- -------------------------------------------------------------------
-- HUB: one row per unique business key
-- Stores the business key; descriptive attributes go in Satellites
-- -------------------------------------------------------------------
CREATE TABLE dv.hub_customer (
    hub_customer_hk  BYTEA        PRIMARY KEY,  -- MD5/SHA1 of business key
    customer_number  VARCHAR(50)  NOT NULL,      -- the business key
    load_dts         TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    record_source    VARCHAR(100) NOT NULL        -- source system identifier
);

-- Hash key generation (consistent with other hubs):
-- hub_customer_hk = MD5(UPPER(TRIM(customer_number)))::BYTEA
-- Or using pgcrypto: digest(upper(trim(customer_number)), 'md5')

CREATE UNIQUE INDEX uq_hub_customer_bk ON dv.hub_customer(customer_number);
CREATE INDEX idx_hub_customer_load_dts ON dv.hub_customer(load_dts);


-- -------------------------------------------------------------------
-- LINK: one row per unique relationship between hubs
-- -------------------------------------------------------------------
CREATE TABLE dv.lnk_customer_order (
    lnk_customer_order_hk  BYTEA       PRIMARY KEY,  -- MD5 of composite BK
    hub_customer_hk        BYTEA       NOT NULL REFERENCES dv.hub_customer(hub_customer_hk),
    hub_order_hk           BYTEA       NOT NULL,     -- references hub_order
    load_dts               TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    record_source          VARCHAR(100) NOT NULL
);

CREATE INDEX idx_lnk_co_customer ON dv.lnk_customer_order(hub_customer_hk);
CREATE INDEX idx_lnk_co_order    ON dv.lnk_customer_order(hub_order_hk);

-- Hash key for link: MD5(customer_hk || order_hk) — concatenate hub HKs


-- -------------------------------------------------------------------
-- SATELLITE: one row per change to descriptive attributes
-- Attached to a hub (or link); tracks full history
-- -------------------------------------------------------------------
CREATE TABLE dv.sat_customer_details (
    hub_customer_hk  BYTEA        NOT NULL REFERENCES dv.hub_customer(hub_customer_hk),
    load_dts         TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    -- End-dating: NULL = current row; set by the next load
    load_end_dts     TIMESTAMPTZ,

    -- Change detection: hash of all attribute values
    hash_diff        BYTEA        NOT NULL,

    record_source    VARCHAR(100) NOT NULL,

    -- Descriptive attributes (volatile data)
    first_name       VARCHAR(255),
    last_name        VARCHAR(255),
    email            VARCHAR(255),
    phone            VARCHAR(50),
    country_code     CHAR(2),

    PRIMARY KEY (hub_customer_hk, load_dts)
);

-- Active record lookup
CREATE INDEX idx_sat_customer_active
    ON dv.sat_customer_details(hub_customer_hk, load_end_dts)
    WHERE load_end_dts IS NULL;

-- Change detection: only INSERT if hash_diff differs from latest row
-- SELECT hash_diff FROM dv.sat_customer_details
-- WHERE hub_customer_hk = $hk AND load_end_dts IS NULL;


-- -------------------------------------------------------------------
-- POINT-IN-TIME (PIT) table — optional performance helper
-- Pre-join satellite snapshots to avoid correlated subqueries
-- -------------------------------------------------------------------
CREATE TABLE dv.pit_customer (
    hub_customer_hk        BYTEA       NOT NULL,
    snapshot_dts           TIMESTAMPTZ NOT NULL,

    -- One HK per satellite that participates in this PIT
    sat_customer_details_hk BYTEA,
    sat_customer_details_ldts TIMESTAMPTZ,

    PRIMARY KEY (hub_customer_hk, snapshot_dts)
);
