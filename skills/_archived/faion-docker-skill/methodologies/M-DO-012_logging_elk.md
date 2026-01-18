# M-DO-012: Centralized Logging with ELK

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #logging, #elk, #elasticsearch, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Logs scattered across servers are hard to search. Debugging production issues requires SSH access to multiple machines. Log retention is inconsistent.

## Promise

After this methodology, you will centralize logs with Elasticsearch, Logstash, and Kibana. You'll search and analyze logs from a single interface.

## Overview

The ELK stack (Elasticsearch, Logstash, Kibana) provides log aggregation, processing, and visualization. Filebeat or Fluent Bit collect and ship logs.

---

## Framework

### Step 1: ELK Stack Setup

```yaml
# docker-compose.yml
version: "3.9"

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    healthcheck:
      test: curl -s http://localhost:9200 >/dev/null || exit 1
      interval: 30s
      timeout: 10s
      retries: 5

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    ports:
      - "5044:5044"
      - "5000:5000"
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    depends_on:
      elasticsearch:
        condition: service_healthy

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      elasticsearch:
        condition: service_healthy

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.11.0
    user: root
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    depends_on:
      - logstash

volumes:
  elasticsearch_data:
```

### Step 2: Filebeat Configuration

```yaml
# filebeat.yml
filebeat.inputs:
  # Container logs
  - type: container
    paths:
      - '/var/lib/docker/containers/*/*.log'
    processors:
      - add_docker_metadata:
          host: "unix:///var/run/docker.sock"

  # Application logs
  - type: log
    paths:
      - /var/log/app/*.log
    fields:
      type: application
    multiline:
      pattern: '^\d{4}-\d{2}-\d{2}'
      negate: true
      match: after

  # Nginx access logs
  - type: log
    paths:
      - /var/log/nginx/access.log
    fields:
      type: nginx-access
    processors:
      - dissect:
          tokenizer: '%{client_ip} - %{user} [%{timestamp}] "%{method} %{uri} %{protocol}" %{status} %{bytes}'
          field: "message"

output.logstash:
  hosts: ["logstash:5044"]

processors:
  - add_host_metadata: ~
  - add_cloud_metadata: ~
```

### Step 3: Logstash Pipeline

```ruby
# logstash/pipeline/logstash.conf
input {
  beats {
    port => 5044
  }

  tcp {
    port => 5000
    codec => json
  }
}

filter {
  # Parse JSON logs
  if [message] =~ /^\{/ {
    json {
      source => "message"
    }
  }

  # Parse application logs
  if [fields][type] == "application" {
    grok {
      match => {
        "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} \[%{DATA:logger}\] %{GREEDYDATA:log_message}"
      }
    }
    date {
      match => ["timestamp", "ISO8601"]
    }
  }

  # Parse nginx access logs
  if [fields][type] == "nginx-access" {
    grok {
      match => {
        "message" => '%{IPORHOST:client_ip} - %{USER:user} \[%{HTTPDATE:timestamp}\] "%{WORD:method} %{URIPATHPARAM:uri} HTTP/%{NUMBER:http_version}" %{NUMBER:status} %{NUMBER:bytes} "%{DATA:referrer}" "%{DATA:user_agent}"'
      }
    }
    date {
      match => ["timestamp", "dd/MMM/yyyy:HH:mm:ss Z"]
    }
    geoip {
      source => "client_ip"
    }
    useragent {
      source => "user_agent"
    }
  }

  # Remove unnecessary fields
  mutate {
    remove_field => ["@version", "agent", "ecs"]
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{[fields][type]}-%{+YYYY.MM.dd}"
  }
}
```

### Step 4: Structured Logging

```javascript
// Node.js with Winston
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'api',
    environment: process.env.NODE_ENV,
  },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: '/var/log/app/app.log' }),
  ],
});

// Usage
logger.info('User logged in', {
  userId: user.id,
  email: user.email,
  ip: req.ip,
  requestId: req.id,
});

logger.error('Database connection failed', {
  error: err.message,
  stack: err.stack,
  host: dbConfig.host,
});
```

```python
# Python with structlog
import structlog
import logging

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()

# Usage
logger.info(
    "user_logged_in",
    user_id=user.id,
    email=user.email,
    ip=request.remote_addr,
    request_id=request.id,
)

logger.error(
    "database_connection_failed",
    error=str(e),
    host=db_config.host,
    exc_info=True,
)
```

### Step 5: Index Lifecycle Management

```json
// PUT _ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_primary_shard_size": "50gb",
            "max_age": "1d"
          },
          "set_priority": {
            "priority": 100
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          },
          "set_priority": {
            "priority": 50
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "set_priority": {
            "priority": 0
          }
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

### Step 6: Kibana Queries

```
# KQL (Kibana Query Language)

# Find errors
level: error

# Specific service
service: "api" AND level: "error"

# Time range
@timestamp >= "2024-01-01" AND @timestamp < "2024-01-02"

# Status codes
status: (500 OR 502 OR 503)

# Contains text
message: *timeout*

# User activity
userId: "12345" AND (event: "login" OR event: "logout")

# Exclude noise
NOT (path: "/health" OR path: "/metrics")

# Combine
service: "api" AND level: error AND NOT message: *expected*
```

---

## Templates

### Fluent Bit (Lightweight Alternative)

```ini
# fluent-bit.conf
[SERVICE]
    Flush         1
    Log_Level     info
    Parsers_File  parsers.conf

[INPUT]
    Name          tail
    Path          /var/log/app/*.log
    Parser        json
    Tag           app.*
    Mem_Buf_Limit 5MB

[INPUT]
    Name          tail
    Path          /var/log/nginx/access.log
    Parser        nginx
    Tag           nginx.access

[FILTER]
    Name          modify
    Match         *
    Add           hostname ${HOSTNAME}

[OUTPUT]
    Name          es
    Match         *
    Host          elasticsearch
    Port          9200
    Index         logs
    Type          _doc
    Logstash_Format On
    Logstash_Prefix logs
```

### Request ID Middleware

```javascript
// Express middleware
const { v4: uuidv4 } = require('uuid');

app.use((req, res, next) => {
  req.id = req.headers['x-request-id'] || uuidv4();
  res.setHeader('x-request-id', req.id);

  // Add to all logs
  req.log = logger.child({ requestId: req.id });

  next();
});
```

---

## Examples

### Log Analysis Dashboard

```json
{
  "title": "Application Logs",
  "panels": [
    {
      "title": "Log Volume Over Time",
      "type": "line",
      "query": {
        "aggs": {
          "logs_over_time": {
            "date_histogram": {
              "field": "@timestamp",
              "interval": "1m"
            }
          }
        }
      }
    },
    {
      "title": "Error Rate by Service",
      "type": "pie",
      "query": {
        "query": { "match": { "level": "error" } },
        "aggs": {
          "by_service": {
            "terms": { "field": "service.keyword" }
          }
        }
      }
    }
  ]
}
```

### Alerting on Errors

```json
{
  "trigger": {
    "schedule": {
      "interval": "1m"
    }
  },
  "input": {
    "search": {
      "request": {
        "indices": ["logs-*"],
        "body": {
          "query": {
            "bool": {
              "filter": [
                { "range": { "@timestamp": { "gte": "now-5m" } } },
                { "term": { "level": "error" } }
              ]
            }
          }
        }
      }
    }
  },
  "condition": {
    "compare": {
      "ctx.payload.hits.total": { "gt": 10 }
    }
  },
  "actions": {
    "slack": {
      "webhook": {
        "url": "https://hooks.slack.com/..."
      }
    }
  }
}
```

---

## Common Mistakes

1. **No structured logging** - Parsing unstructured logs is hard
2. **Missing request ID** - Can't trace requests across services
3. **No retention policy** - Elasticsearch runs out of disk
4. **Logging sensitive data** - PII, passwords in logs
5. **Too verbose logging** - Info level in production

---

## Checklist

- [ ] ELK stack deployed
- [ ] Filebeat/Fluent Bit configured
- [ ] Structured JSON logging
- [ ] Request ID propagation
- [ ] Index lifecycle management
- [ ] Kibana dashboards
- [ ] Alerting rules
- [ ] Sensitive data filtering

---

## Next Steps

- M-DO-011: Prometheus Monitoring
- M-DO-013: Distributed Tracing
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-012 v1.0*
