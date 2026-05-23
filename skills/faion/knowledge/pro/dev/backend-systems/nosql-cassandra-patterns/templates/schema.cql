-- purpose: smoke CQL schema for nosql-cassandra-patterns
-- consumes: access-pattern list
-- produces: table set
-- depends-on: scripts/validate-nosql-cassandra-patterns.py
-- token-budget-impact: ~250 tokens
-- query: get telemetry for a sensor on a day
CREATE TABLE IF NOT EXISTS telemetry_by_sensor_day (
    sensor_id TEXT,
    date DATE,
    timestamp TIMESTAMP,
    value DOUBLE,
    PRIMARY KEY ((sensor_id, date), timestamp)
) WITH CLUSTERING ORDER BY (timestamp ASC);
