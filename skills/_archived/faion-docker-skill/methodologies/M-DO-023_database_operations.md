# M-DO-023: Database Operations

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #database, #rds, #postgresql, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Database outages cause business disruption. Unoptimized queries slow applications. Poor backup strategies risk data loss.

## Promise

After this methodology, you will operate production databases reliably. Your databases will be performant, highly available, and recoverable.

## Overview

Database operations include provisioning, monitoring, backups, migrations, and performance tuning. This covers RDS/Aurora patterns.

---

## Framework

### Step 1: RDS Provisioning

```hcl
resource "aws_db_instance" "main" {
  identifier = "${var.project}-${var.environment}"

  # Engine
  engine               = "postgres"
  engine_version       = "16.1"
  instance_class       = "db.t3.medium"
  parameter_group_name = aws_db_parameter_group.main.name

  # Storage
  allocated_storage     = 100
  max_allocated_storage = 500
  storage_type          = "gp3"
  storage_encrypted     = true
  kms_key_id            = aws_kms_key.db.arn

  # Credentials
  db_name  = "app"
  username = "admin"
  password = random_password.db.result

  # Network
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]
  publicly_accessible    = false
  port                   = 5432

  # High Availability
  multi_az = var.environment == "production"

  # Backups
  backup_retention_period   = 7
  backup_window             = "03:00-04:00"
  delete_automated_backups  = false
  copy_tags_to_snapshot     = true
  skip_final_snapshot       = false
  final_snapshot_identifier = "${var.project}-final"

  # Maintenance
  maintenance_window         = "Mon:04:00-Mon:05:00"
  auto_minor_version_upgrade = true
  allow_major_version_upgrade = false

  # Monitoring
  performance_insights_enabled          = true
  performance_insights_retention_period = 7
  monitoring_interval                   = 60
  monitoring_role_arn                   = aws_iam_role.rds_monitoring.arn
  enabled_cloudwatch_logs_exports       = ["postgresql", "upgrade"]

  # Protection
  deletion_protection = true

  tags = {
    Name = "${var.project}-${var.environment}"
  }
}

resource "aws_db_parameter_group" "main" {
  name   = "${var.project}-${var.environment}"
  family = "postgres16"

  parameter {
    name  = "log_statement"
    value = "ddl"
  }

  parameter {
    name  = "log_min_duration_statement"
    value = "1000"  # Log queries > 1 second
  }

  parameter {
    name  = "shared_preload_libraries"
    value = "pg_stat_statements"
  }
}
```

### Step 2: Database Monitoring

```hcl
# CloudWatch alarms
resource "aws_cloudwatch_metric_alarm" "cpu" {
  alarm_name          = "${var.project}-db-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 3
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = 300
  statistic           = "Average"
  threshold           = 80

  dimensions = {
    DBInstanceIdentifier = aws_db_instance.main.id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "storage" {
  alarm_name          = "${var.project}-db-storage"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 1
  metric_name         = "FreeStorageSpace"
  namespace           = "AWS/RDS"
  period              = 300
  statistic           = "Average"
  threshold           = 10737418240  # 10 GB

  dimensions = {
    DBInstanceIdentifier = aws_db_instance.main.id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "connections" {
  alarm_name          = "${var.project}-db-connections"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 3
  metric_name         = "DatabaseConnections"
  namespace           = "AWS/RDS"
  period              = 300
  statistic           = "Average"
  threshold           = 90  # Percentage of max

  dimensions = {
    DBInstanceIdentifier = aws_db_instance.main.id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
}
```

### Step 3: Database Migrations

```bash
# Using golang-migrate
migrate -path ./migrations -database "postgres://user:pass@host:5432/db?sslmode=require" up

# Using Flyway
flyway -url=jdbc:postgresql://host:5432/db -user=admin -password=pass migrate

# Using sqitch
sqitch deploy db:pg://user:pass@host/db
```

```sql
-- migrations/001_create_users.up.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- migrations/001_create_users.down.sql
DROP TABLE IF EXISTS users;
```

```yaml
# CI/CD migration
name: Database Migration

on:
  push:
    branches: [main]
    paths:
      - 'migrations/**'

jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run migrations
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          curl -L https://github.com/golang-migrate/migrate/releases/download/v4.17.0/migrate.linux-amd64.tar.gz | tar xvz
          ./migrate -path ./migrations -database "$DATABASE_URL" up
```

### Step 4: Read Replicas

```hcl
# Read replica
resource "aws_db_instance" "replica" {
  identifier          = "${var.project}-${var.environment}-replica"
  replicate_source_db = aws_db_instance.main.identifier
  instance_class      = "db.t3.medium"

  vpc_security_group_ids = [aws_security_group.db.id]

  # Replicas don't need backups (inherit from primary)
  backup_retention_period = 0
  skip_final_snapshot     = true

  # Performance Insights
  performance_insights_enabled = true

  tags = {
    Name = "${var.project}-${var.environment}-replica"
  }
}

# Application connection pooling
# pgbouncer or RDS Proxy
resource "aws_db_proxy" "main" {
  name                   = "${var.project}-proxy"
  engine_family          = "POSTGRESQL"
  role_arn               = aws_iam_role.proxy.arn
  vpc_security_group_ids = [aws_security_group.proxy.id]
  vpc_subnet_ids         = aws_subnet.private[*].id

  auth {
    auth_scheme = "SECRETS"
    secret_arn  = aws_secretsmanager_secret.db.arn
    iam_auth    = "DISABLED"
  }
}

resource "aws_db_proxy_default_target_group" "main" {
  db_proxy_name = aws_db_proxy.main.name

  connection_pool_config {
    max_connections_percent = 100
    max_idle_connections_percent = 50
  }
}

resource "aws_db_proxy_target" "main" {
  db_instance_identifier = aws_db_instance.main.id
  db_proxy_name          = aws_db_proxy.main.name
  target_group_name      = aws_db_proxy_default_target_group.main.name
}
```

### Step 5: Performance Tuning

```sql
-- Enable pg_stat_statements
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find slow queries
SELECT
    calls,
    round(total_exec_time::numeric, 2) as total_time_ms,
    round(mean_exec_time::numeric, 2) as mean_time_ms,
    round((100 * total_exec_time / sum(total_exec_time) OVER())::numeric, 2) as percentage,
    query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Find missing indexes
SELECT
    relname as table_name,
    seq_scan - idx_scan as too_much_seq,
    CASE
        WHEN seq_scan - idx_scan > 0 THEN 'Missing Index?'
        ELSE 'OK'
    END as status,
    pg_size_pretty(pg_relation_size(relid)) as table_size,
    idx_scan,
    seq_scan
FROM pg_stat_user_tables
WHERE seq_scan - idx_scan > 100
ORDER BY too_much_seq DESC
LIMIT 10;

-- Find unused indexes
SELECT
    indexrelname as index_name,
    relname as table_name,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size,
    idx_scan as scans
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND indexrelname NOT LIKE 'pg_%'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Analyze query plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM users WHERE email = 'test@example.com';
```

### Step 6: Disaster Recovery

```bash
# Manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier mydb \
  --db-snapshot-identifier mydb-manual-snapshot

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier mydb-restored \
  --db-snapshot-identifier mydb-manual-snapshot \
  --db-instance-class db.t3.medium

# Point-in-time recovery
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier mydb \
  --target-db-instance-identifier mydb-restored \
  --restore-time 2024-01-15T10:00:00Z
```

```hcl
# Cross-region backup
resource "aws_db_instance_automated_backups_replication" "dr" {
  source_db_instance_arn = aws_db_instance.main.arn
  kms_key_id             = aws_kms_key.dr.arn
  retention_period       = 7

  provider = aws.dr_region
}
```

---

## Templates

### Connection String Management

```javascript
// Node.js with environment-based config
const config = {
  development: {
    connectionString: process.env.DATABASE_URL,
    ssl: false,
    max: 5,
  },
  production: {
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: true },
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
  },
};

const pool = new Pool(config[process.env.NODE_ENV]);
```

### Health Check Query

```sql
-- Simple health check
SELECT 1;

-- Detailed health check
SELECT
    pg_is_in_recovery() as is_replica,
    pg_postmaster_start_time() as started_at,
    current_setting('server_version') as version,
    pg_database_size(current_database()) as db_size_bytes,
    (SELECT count(*) FROM pg_stat_activity) as connections;
```

---

## Common Mistakes

1. **Public databases** - Always use private subnets
2. **No Multi-AZ** - Single point of failure
3. **Untested backups** - Recovery will fail
4. **No connection pooling** - Connections exhausted
5. **Missing indexes** - Sequential scans kill performance

---

## Checklist

- [ ] Multi-AZ for production
- [ ] Encryption at rest
- [ ] Automated backups
- [ ] Performance Insights enabled
- [ ] CloudWatch alarms
- [ ] Connection pooling
- [ ] Read replicas for read-heavy loads
- [ ] DR procedure documented and tested

---

## Next Steps

- M-DO-016: Backup and Recovery
- M-DO-010: Infrastructure Patterns
- M-DO-011: Prometheus Monitoring

---

*Methodology M-DO-023 v1.0*
