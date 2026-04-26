-- Cassandra / ScyllaDB table template
-- Design: one table per query; partition key in every WHERE clause

-- -------------------------------------------------------------------
-- Query-first pattern example
-- Query: "Get last N events for a user, in reverse chronological order"
-- -------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS app.user_event_by_user (
    -- Partition key: determines which node stores the row
    -- Avoid hot partitions: bucket by time if single user generates >100k rows/day
    user_id     UUID,
    -- For high-volume users, add a time bucket: (user_id, event_month)

    -- Clustering columns: define sort order within the partition
    occurred_at TIMESTAMP,
    event_id    UUID,

    -- Payload columns
    event_type  TEXT,
    metadata    MAP<TEXT, TEXT>,

    PRIMARY KEY ((user_id), occurred_at, event_id)
)
WITH CLUSTERING ORDER BY (occurred_at DESC, event_id ASC)
AND  default_time_to_live = 7776000  -- 90 days TTL; remove if retention is indefinite
AND  compaction = {
    'class': 'org.apache.cassandra.db.compaction.TimeWindowCompactionStrategy',
    'compaction_window_unit': 'DAYS',
    'compaction_window_size': 1
}
AND  compression = {
    'sstable_compression': 'org.apache.cassandra.io.compress.LZ4Compressor'
};

-- -------------------------------------------------------------------
-- Second table for a DIFFERENT query on the same logical data
-- Query: "Get all users who triggered a specific event type today"
-- This cannot reuse the table above — model a new table.
-- -------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS app.user_event_by_type (
    event_type  TEXT,
    event_date  DATE,           -- time bucket to bound partition size
    occurred_at TIMESTAMP,
    event_id    UUID,
    user_id     UUID,
    metadata    MAP<TEXT, TEXT>,

    PRIMARY KEY ((event_type, event_date), occurred_at, event_id)
)
WITH CLUSTERING ORDER BY (occurred_at DESC, event_id ASC)
AND  default_time_to_live = 2592000  -- 30 days
AND  compaction = {
    'class': 'org.apache.cassandra.db.compaction.TimeWindowCompactionStrategy',
    'compaction_window_unit': 'DAYS',
    'compaction_window_size': 1
};

-- -------------------------------------------------------------------
-- Materialized view (ScyllaDB / Cassandra 3+)
-- Alternative to a second table when the data is identical.
-- NOTE: MV have known performance caveats; prefer manual dual-write for
-- high-throughput tables.
-- -------------------------------------------------------------------
-- CREATE MATERIALIZED VIEW IF NOT EXISTS app.user_event_by_type_mv
-- AS SELECT * FROM app.user_event_by_user
-- WHERE event_type IS NOT NULL AND event_date IS NOT NULL
--   AND occurred_at IS NOT NULL AND event_id IS NOT NULL
-- PRIMARY KEY ((event_type, event_date), occurred_at, event_id)
-- WITH CLUSTERING ORDER BY (occurred_at DESC, event_id ASC);
