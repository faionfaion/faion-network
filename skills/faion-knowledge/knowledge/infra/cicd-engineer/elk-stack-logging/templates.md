# ELK Stack Templates

## Docker Compose Deployment

### Single-Node Development

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0
    container_name: elasticsearch
    environment:
      - node.name=es01
      - cluster.name=dev-cluster
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
      - xpack.security.enabled=false
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - elk
    healthcheck:
      test: ["CMD-SHELL", "curl -s http://localhost:9200/_cluster/health | grep -q 'green\\|yellow'"]
      interval: 30s
      timeout: 10s
      retries: 5

  kibana:
    image: docker.elastic.co/kibana/kibana:8.12.0
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      elasticsearch:
        condition: service_healthy
    networks:
      - elk

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.12.0
    container_name: filebeat
    user: root
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    depends_on:
      elasticsearch:
        condition: service_healthy
    networks:
      - elk

volumes:
  elasticsearch-data:

networks:
  elk:
    driver: bridge
```

### Production Cluster with Security

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  setup:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0
    container_name: es-setup
    volumes:
      - certs:/usr/share/elasticsearch/config/certs
    user: "0"
    command: >
      bash -c '
        if [ ! -f config/certs/ca.zip ]; then
          echo "Creating CA";
          bin/elasticsearch-certutil ca --silent --pem -out config/certs/ca.zip;
          unzip config/certs/ca.zip -d config/certs;
        fi;
        if [ ! -f config/certs/certs.zip ]; then
          echo "Creating certs";
          echo -ne \
          "instances:\n"\
          "  - name: es01\n"\
          "    dns:\n"\
          "      - es01\n"\
          "      - localhost\n"\
          "    ip:\n"\
          "      - 127.0.0.1\n"\
          "  - name: kibana\n"\
          "    dns:\n"\
          "      - kibana\n"\
          "      - localhost\n"\
          "    ip:\n"\
          "      - 127.0.0.1\n"\
          > config/certs/instances.yml;
          bin/elasticsearch-certutil cert --silent --pem -out config/certs/certs.zip --in config/certs/instances.yml --ca-cert config/certs/ca/ca.crt --ca-key config/certs/ca/ca.key;
          unzip config/certs/certs.zip -d config/certs;
        fi;
        echo "Setting file permissions"
        chown -R root:root config/certs;
        find . -type d -exec chmod 750 \{\} \;;
        find . -type f -exec chmod 640 \{\} \;;
        echo "All done!";
      '
    healthcheck:
      test: ["CMD-SHELL", "[ -f config/certs/es01/es01.crt ]"]
      interval: 1s
      timeout: 5s
      retries: 120

  es01:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0
    container_name: es01
    depends_on:
      setup:
        condition: service_healthy
    environment:
      - node.name=es01
      - cluster.name=production-cluster
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms4g -Xmx4g"
      - ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
      - xpack.security.enabled=true
      - xpack.security.http.ssl.enabled=true
      - xpack.security.http.ssl.key=certs/es01/es01.key
      - xpack.security.http.ssl.certificate=certs/es01/es01.crt
      - xpack.security.http.ssl.certificate_authorities=certs/ca/ca.crt
      - xpack.security.transport.ssl.enabled=true
      - xpack.security.transport.ssl.key=certs/es01/es01.key
      - xpack.security.transport.ssl.certificate=certs/es01/es01.crt
      - xpack.security.transport.ssl.certificate_authorities=certs/ca/ca.crt
      - xpack.security.transport.ssl.verification_mode=certificate
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - certs:/usr/share/elasticsearch/config/certs
      - esdata01:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - elk
    healthcheck:
      test: ["CMD-SHELL", "curl -s --cacert config/certs/ca/ca.crt https://localhost:9200 | grep -q 'missing authentication credentials'"]
      interval: 10s
      timeout: 10s
      retries: 120

  kibana:
    image: docker.elastic.co/kibana/kibana:8.12.0
    container_name: kibana
    depends_on:
      es01:
        condition: service_healthy
    environment:
      - SERVERNAME=kibana
      - ELASTICSEARCH_HOSTS=https://es01:9200
      - ELASTICSEARCH_USERNAME=kibana_system
      - ELASTICSEARCH_PASSWORD=${KIBANA_PASSWORD}
      - ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES=config/certs/ca/ca.crt
      - XPACK_SECURITY_ENCRYPTIONKEY=${ENCRYPTION_KEY}
      - XPACK_ENCRYPTEDSAVEDOBJECTS_ENCRYPTIONKEY=${ENCRYPTION_KEY}
      - XPACK_REPORTING_ENCRYPTIONKEY=${ENCRYPTION_KEY}
    volumes:
      - certs:/usr/share/kibana/config/certs
    ports:
      - "5601:5601"
    networks:
      - elk
    healthcheck:
      test: ["CMD-SHELL", "curl -s -I http://localhost:5601 | grep -q 'HTTP/1.1 302 Found'"]
      interval: 10s
      timeout: 10s
      retries: 120

  logstash:
    image: docker.elastic.co/logstash/logstash:8.12.0
    container_name: logstash
    depends_on:
      es01:
        condition: service_healthy
    volumes:
      - certs:/usr/share/logstash/config/certs
      - ./logstash/pipeline:/usr/share/logstash/pipeline:ro
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml:ro
    environment:
      - "LS_JAVA_OPTS=-Xms1g -Xmx1g"
      - LOGSTASH_PASSWORD=${LOGSTASH_PASSWORD}
    ports:
      - "5044:5044"
      - "9600:9600"
    networks:
      - elk

volumes:
  certs:
  esdata01:

networks:
  elk:
    driver: bridge
```

### Environment File

```bash
# .env
ELASTIC_PASSWORD=changeme_elastic_password
KIBANA_PASSWORD=changeme_kibana_password
LOGSTASH_PASSWORD=changeme_logstash_password
ENCRYPTION_KEY=32-character-encryption-key-here
STACK_VERSION=8.12.0
CLUSTER_NAME=production-cluster
```

## Kubernetes (ECK) Templates

### Elasticsearch Cluster

```yaml
# elasticsearch.yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: production-logs
  namespace: elastic-system
spec:
  version: 8.12.0
  http:
    tls:
      selfSignedCertificate:
        disabled: false
  nodeSets:
    # Master nodes
    - name: master
      count: 3
      config:
        node.roles: ["master"]
        xpack.ml.enabled: false
      podTemplate:
        spec:
          containers:
            - name: elasticsearch
              resources:
                requests:
                  memory: 4Gi
                  cpu: 1
                limits:
                  memory: 4Gi
                  cpu: 2
              env:
                - name: ES_JAVA_OPTS
                  value: "-Xms2g -Xmx2g"
          affinity:
            podAntiAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                - labelSelector:
                    matchLabels:
                      elasticsearch.k8s.elastic.co/cluster-name: production-logs
                      elasticsearch.k8s.elastic.co/node-master: "true"
                  topologyKey: kubernetes.io/hostname
      volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes: ["ReadWriteOnce"]
            storageClassName: fast-ssd
            resources:
              requests:
                storage: 50Gi

    # Data nodes (Hot tier)
    - name: data-hot
      count: 3
      config:
        node.roles: ["data_hot", "data_content", "ingest"]
        node.attr.data_tier: hot
      podTemplate:
        spec:
          containers:
            - name: elasticsearch
              resources:
                requests:
                  memory: 16Gi
                  cpu: 4
                limits:
                  memory: 16Gi
                  cpu: 8
              env:
                - name: ES_JAVA_OPTS
                  value: "-Xms8g -Xmx8g"
          affinity:
            podAntiAffinity:
              preferredDuringSchedulingIgnoredDuringExecution:
                - weight: 100
                  podAffinityTerm:
                    labelSelector:
                      matchLabels:
                        elasticsearch.k8s.elastic.co/cluster-name: production-logs
                    topologyKey: kubernetes.io/hostname
      volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes: ["ReadWriteOnce"]
            storageClassName: fast-ssd
            resources:
              requests:
                storage: 500Gi

    # Data nodes (Warm tier)
    - name: data-warm
      count: 2
      config:
        node.roles: ["data_warm"]
        node.attr.data_tier: warm
      podTemplate:
        spec:
          containers:
            - name: elasticsearch
              resources:
                requests:
                  memory: 8Gi
                  cpu: 2
                limits:
                  memory: 8Gi
                  cpu: 4
              env:
                - name: ES_JAVA_OPTS
                  value: "-Xms4g -Xmx4g"
      volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes: ["ReadWriteOnce"]
            storageClassName: standard-hdd
            resources:
              requests:
                storage: 1Ti
```

### Kibana

```yaml
# kibana.yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: production-kibana
  namespace: elastic-system
spec:
  version: 8.12.0
  count: 2
  elasticsearchRef:
    name: production-logs
  http:
    tls:
      selfSignedCertificate:
        disabled: true
  podTemplate:
    spec:
      containers:
        - name: kibana
          resources:
            requests:
              memory: 1Gi
              cpu: 500m
            limits:
              memory: 2Gi
              cpu: 1
          env:
            - name: XPACK_ENCRYPTEDSAVEDOBJECTS_ENCRYPTIONKEY
              valueFrom:
                secretKeyRef:
                  name: kibana-encryption-key
                  key: key
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: kibana-ingress
  namespace: elastic-system
  annotations:
    nginx.ingress.kubernetes.io/backend-protocol: "HTTP"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - kibana.example.com
      secretName: kibana-tls
  rules:
    - host: kibana.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: production-kibana-kb-http
                port:
                  number: 5601
```

### Filebeat DaemonSet

```yaml
# filebeat.yaml
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: filebeat
  namespace: elastic-system
spec:
  type: filebeat
  version: 8.12.0
  elasticsearchRef:
    name: production-logs
  kibanaRef:
    name: production-kibana
  config:
    filebeat.autodiscover:
      providers:
        - type: kubernetes
          node: ${NODE_NAME}
          hints.enabled: true
          hints.default_config:
            type: container
            paths:
              - /var/log/containers/*${data.kubernetes.container.id}.log
          templates:
            - condition:
                contains:
                  kubernetes.namespace: "production"
              config:
                - type: container
                  paths:
                    - /var/log/containers/*${data.kubernetes.container.id}.log
                  processors:
                    - add_kubernetes_metadata:
                        host: ${NODE_NAME}
                        matchers:
                          - logs_path:
                              logs_path: "/var/log/containers/"
    processors:
      - add_cloud_metadata: {}
      - add_host_metadata: {}
      - add_kubernetes_metadata:
          host: ${NODE_NAME}
          matchers:
            - logs_path:
                logs_path: "/var/log/containers/"
  daemonSet:
    podTemplate:
      spec:
        serviceAccountName: filebeat
        automountServiceAccountToken: true
        dnsPolicy: ClusterFirstWithHostNet
        hostNetwork: true
        containers:
          - name: filebeat
            securityContext:
              runAsUser: 0
            volumeMounts:
              - name: varlogcontainers
                mountPath: /var/log/containers
              - name: varlogpods
                mountPath: /var/log/pods
              - name: varlibdockercontainers
                mountPath: /var/lib/docker/containers
            env:
              - name: NODE_NAME
                valueFrom:
                  fieldRef:
                    fieldPath: spec.nodeName
            resources:
              requests:
                memory: 100Mi
                cpu: 100m
              limits:
                memory: 200Mi
                cpu: 200m
        volumes:
          - name: varlogcontainers
            hostPath:
              path: /var/log/containers
          - name: varlogpods
            hostPath:
              path: /var/log/pods
          - name: varlibdockercontainers
            hostPath:
              path: /var/lib/docker/containers
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: filebeat
  namespace: elastic-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: filebeat
rules:
  - apiGroups: [""]
    resources:
      - namespaces
      - pods
      - nodes
    verbs: ["get", "watch", "list"]
  - apiGroups: ["apps"]
    resources:
      - replicasets
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: filebeat
subjects:
  - kind: ServiceAccount
    name: filebeat
    namespace: elastic-system
roleRef:
  kind: ClusterRole
  name: filebeat
  apiGroup: rbac.authorization.k8s.io
```

## Terraform Module

### AWS Elasticsearch Service

```hcl
# main.tf
resource "aws_elasticsearch_domain" "logs" {
  domain_name           = var.domain_name
  elasticsearch_version = "OpenSearch_2.11"

  cluster_config {
    instance_type            = var.instance_type
    instance_count           = var.instance_count
    dedicated_master_enabled = var.dedicated_master_enabled
    dedicated_master_type    = var.dedicated_master_type
    dedicated_master_count   = var.dedicated_master_count
    zone_awareness_enabled   = var.zone_awareness_enabled

    zone_awareness_config {
      availability_zone_count = var.availability_zone_count
    }
  }

  ebs_options {
    ebs_enabled = true
    volume_type = "gp3"
    volume_size = var.volume_size
    iops        = var.volume_iops
    throughput  = var.volume_throughput
  }

  vpc_options {
    subnet_ids         = var.subnet_ids
    security_group_ids = [aws_security_group.elasticsearch.id]
  }

  encrypt_at_rest {
    enabled = true
  }

  node_to_node_encryption {
    enabled = true
  }

  domain_endpoint_options {
    enforce_https       = true
    tls_security_policy = "Policy-Min-TLS-1-2-2019-07"
  }

  advanced_security_options {
    enabled                        = true
    internal_user_database_enabled = true
    master_user_options {
      master_user_name     = var.master_user_name
      master_user_password = var.master_user_password
    }
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.elasticsearch.arn
    log_type                 = "INDEX_SLOW_LOGS"
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.elasticsearch.arn
    log_type                 = "SEARCH_SLOW_LOGS"
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.elasticsearch.arn
    log_type                 = "ES_APPLICATION_LOGS"
  }

  tags = var.tags
}

resource "aws_security_group" "elasticsearch" {
  name        = "${var.domain_name}-elasticsearch-sg"
  description = "Security group for Elasticsearch domain"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = var.allowed_security_groups
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.tags
}

resource "aws_cloudwatch_log_group" "elasticsearch" {
  name              = "/aws/elasticsearch/${var.domain_name}"
  retention_in_days = 30
  tags              = var.tags
}

resource "aws_cloudwatch_log_resource_policy" "elasticsearch" {
  policy_name = "${var.domain_name}-elasticsearch-log-policy"
  policy_document = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "es.amazonaws.com"
        }
        Action = [
          "logs:PutLogEvents",
          "logs:CreateLogStream"
        ]
        Resource = "${aws_cloudwatch_log_group.elasticsearch.arn}:*"
      }
    ]
  })
}

# variables.tf
variable "domain_name" {
  description = "Name of the Elasticsearch domain"
  type        = string
}

variable "instance_type" {
  description = "Instance type for data nodes"
  type        = string
  default     = "r6g.large.elasticsearch"
}

variable "instance_count" {
  description = "Number of data nodes"
  type        = number
  default     = 3
}

variable "dedicated_master_enabled" {
  description = "Enable dedicated master nodes"
  type        = bool
  default     = true
}

variable "dedicated_master_type" {
  description = "Instance type for master nodes"
  type        = string
  default     = "r6g.large.elasticsearch"
}

variable "dedicated_master_count" {
  description = "Number of master nodes"
  type        = number
  default     = 3
}

variable "zone_awareness_enabled" {
  description = "Enable zone awareness"
  type        = bool
  default     = true
}

variable "availability_zone_count" {
  description = "Number of availability zones"
  type        = number
  default     = 3
}

variable "volume_size" {
  description = "EBS volume size in GB"
  type        = number
  default     = 500
}

variable "volume_iops" {
  description = "EBS volume IOPS"
  type        = number
  default     = 3000
}

variable "volume_throughput" {
  description = "EBS volume throughput in MiB/s"
  type        = number
  default     = 125
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs for the domain"
  type        = list(string)
}

variable "allowed_security_groups" {
  description = "Security groups allowed to access Elasticsearch"
  type        = list(string)
}

variable "master_user_name" {
  description = "Master username"
  type        = string
  sensitive   = true
}

variable "master_user_password" {
  description = "Master password"
  type        = string
  sensitive   = true
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}

# outputs.tf
output "domain_endpoint" {
  description = "Elasticsearch domain endpoint"
  value       = aws_elasticsearch_domain.logs.endpoint
}

output "kibana_endpoint" {
  description = "Kibana endpoint"
  value       = aws_elasticsearch_domain.logs.kibana_endpoint
}

output "domain_arn" {
  description = "Elasticsearch domain ARN"
  value       = aws_elasticsearch_domain.logs.arn
}
```

## Helm Values Template

```yaml
# values.yaml for Elastic Helm charts
elasticsearch:
  enabled: true
  replicas: 3
  minimumMasterNodes: 2

  resources:
    requests:
      cpu: "1000m"
      memory: "4Gi"
    limits:
      cpu: "2000m"
      memory: "4Gi"

  volumeClaimTemplate:
    accessModes: ["ReadWriteOnce"]
    resources:
      requests:
        storage: 100Gi
    storageClassName: fast-ssd

  esJavaOpts: "-Xmx2g -Xms2g"

  esConfig:
    elasticsearch.yml: |
      xpack.security.enabled: true
      xpack.security.transport.ssl.enabled: true
      xpack.security.http.ssl.enabled: false

kibana:
  enabled: true
  replicas: 2

  resources:
    requests:
      cpu: "500m"
      memory: "1Gi"
    limits:
      cpu: "1000m"
      memory: "2Gi"

  elasticsearchHosts: "http://elasticsearch-master:9200"

  kibanaConfig:
    kibana.yml: |
      server.basePath: ""
      xpack.security.enabled: true

filebeat:
  enabled: true
  daemonset:
    resources:
      requests:
        cpu: "100m"
        memory: "100Mi"
      limits:
        cpu: "200m"
        memory: "200Mi"

  filebeatConfig:
    filebeat.yml: |
      filebeat.autodiscover:
        providers:
          - type: kubernetes
            node: ${NODE_NAME}
            hints.enabled: true
      output.elasticsearch:
        hosts: ["http://elasticsearch-master:9200"]

logstash:
  enabled: false  # Enable if complex processing needed
  replicas: 2

  resources:
    requests:
      cpu: "500m"
      memory: "1Gi"
    limits:
      cpu: "1000m"
      memory: "2Gi"
```

---

*ELK Stack Templates | faion-cicd-engineer*
