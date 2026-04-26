-- PostgreSQL schema for DORA metrics collection.
-- Tables: deployments, incidents.
-- Materialized view: dora_metrics_daily (refresh daily via cron or pg_cron).

CREATE TABLE deployments (
    id SERIAL PRIMARY KEY,
    service VARCHAR(255) NOT NULL,
    environment VARCHAR(50) NOT NULL,
    commit_sha VARCHAR(40) NOT NULL,
    commit_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    deployed_at TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) DEFAULT 'success',
    is_rollback BOOLEAN DEFAULT FALSE,
    is_hotfix BOOLEAN DEFAULT FALSE,
    pipeline_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_status CHECK (status IN ('success', 'failed', 'cancelled'))
);

CREATE INDEX idx_deployments_service ON deployments(service);
CREATE INDEX idx_deployments_deployed_at ON deployments(deployed_at);
CREATE INDEX idx_deployments_service_env ON deployments(service, environment);

CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    incident_id VARCHAR(255) UNIQUE NOT NULL,
    service VARCHAR(255) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    detected_at TIMESTAMP WITH TIME ZONE NOT NULL,
    resolved_at TIMESTAMP WITH TIME ZONE,
    deployment_id INTEGER REFERENCES deployments(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_severity CHECK (severity IN ('critical', 'high', 'medium', 'low'))
);

CREATE INDEX idx_incidents_service ON incidents(service);
CREATE INDEX idx_incidents_detected_at ON incidents(detected_at);

-- Materialized view: daily DORA metrics per service
CREATE MATERIALIZED VIEW dora_metrics_daily AS
SELECT
    d.service,
    DATE_TRUNC('day', d.deployed_at) AS date,
    COUNT(*) AS deployments_count,
    AVG(EXTRACT(EPOCH FROM (d.deployed_at - d.commit_timestamp)) / 3600) AS avg_lead_time_hours,
    COUNT(*) FILTER (WHERE d.is_rollback OR d.is_hotfix OR d.status = 'failed') AS failed_deployments,
    CASE
        WHEN COUNT(*) > 0
        THEN COUNT(*) FILTER (WHERE d.is_rollback OR d.is_hotfix OR d.status = 'failed')::FLOAT / COUNT(*) * 100
        ELSE 0
    END AS change_failure_rate,
    AVG(EXTRACT(EPOCH FROM (i.resolved_at - i.detected_at)) / 60) AS avg_mttr_minutes
FROM deployments d
LEFT JOIN incidents i ON i.deployment_id = d.id AND i.resolved_at IS NOT NULL
WHERE d.environment = 'production'
GROUP BY d.service, DATE_TRUNC('day', d.deployed_at);

CREATE UNIQUE INDEX idx_dora_metrics_daily ON dora_metrics_daily(service, date);

-- Refresh function (call via pg_cron: SELECT cron.schedule('0 1 * * *', 'SELECT refresh_dora_metrics()'))
CREATE OR REPLACE FUNCTION refresh_dora_metrics()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY dora_metrics_daily;
END;
$$ LANGUAGE plpgsql;
