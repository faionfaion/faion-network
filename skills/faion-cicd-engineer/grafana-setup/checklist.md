# Grafana Setup Checklists

## Pre-Installation Checklist

### Infrastructure Requirements

- [ ] Define deployment target (Docker, Kubernetes, VM)
- [ ] Allocate resources (CPU: 2+ cores, RAM: 4GB+, Disk: 20GB+)
- [ ] Prepare network access (ports 3000, 9090, 3100)
- [ ] Set up DNS/hostname
- [ ] Obtain SSL certificates (production)
- [ ] Choose database backend (SQLite dev / PostgreSQL prod)

### Planning

- [ ] Define data sources to connect
- [ ] List dashboards to provision
- [ ] Plan user authentication method
- [ ] Design folder structure for dashboards
- [ ] Define alerting requirements
- [ ] Plan backup strategy

---

## Docker Compose Deployment Checklist

### Initial Setup

- [ ] Create project directory structure
  ```
  grafana-stack/
  ├── docker-compose.yaml
  ├── provisioning/
  │   ├── datasources/
  │   ├── dashboards/
  │   └── alerting/
  ├── dashboards/
  └── .env
  ```
- [ ] Create docker-compose.yaml with services
- [ ] Configure environment variables in .env
- [ ] Create provisioning YAML files
- [ ] Place dashboard JSON files

### Deployment

- [ ] Pull images: `docker compose pull`
- [ ] Start stack: `docker compose up -d`
- [ ] Verify startup: `docker compose logs -f`
- [ ] Access Grafana UI: `http://localhost:3000`
- [ ] Change admin password
- [ ] Verify data sources connected
- [ ] Import/verify dashboards

### Post-Deployment

- [ ] Configure alerts
- [ ] Set up notification channels
- [ ] Create additional users/teams
- [ ] Test alerting pipeline
- [ ] Document access credentials

---

## Kubernetes Helm Deployment Checklist

### Preparation

- [ ] Add Grafana Helm repository
  ```bash
  helm repo add grafana https://grafana.github.io/helm-charts
  helm repo update
  ```
- [ ] Create namespace: `kubectl create namespace monitoring`
- [ ] Prepare values.yaml with configuration
- [ ] Create secrets for sensitive data
- [ ] Configure persistent volume claims
- [ ] Prepare ingress configuration

### Installation

- [ ] Dry-run installation
  ```bash
  helm install grafana grafana/grafana -n monitoring --dry-run
  ```
- [ ] Install Grafana
  ```bash
  helm install grafana grafana/grafana -n monitoring -f values.yaml
  ```
- [ ] Verify pods running
  ```bash
  kubectl get pods -n monitoring
  ```
- [ ] Check service endpoints
  ```bash
  kubectl get svc -n monitoring
  ```

### Configuration

- [ ] Apply ingress rules
- [ ] Configure TLS certificates
- [ ] Set up persistent storage
- [ ] Configure data source provisioning
- [ ] Deploy dashboard ConfigMaps
- [ ] Set up RBAC (ServiceAccount, ClusterRole)

### Validation

- [ ] Access Grafana through ingress
- [ ] Verify authentication works
- [ ] Test data source connectivity
- [ ] Validate dashboards loaded
- [ ] Test alerting pipeline
- [ ] Verify metrics collection

---

## High Availability Setup Checklist

### Database Setup (PostgreSQL)

- [ ] Deploy PostgreSQL cluster (or use managed service)
- [ ] Create Grafana database and user
  ```sql
  CREATE DATABASE grafana;
  CREATE USER grafana WITH PASSWORD 'secure_password';
  GRANT ALL PRIVILEGES ON DATABASE grafana TO grafana;
  ```
- [ ] Test database connectivity from all nodes
- [ ] Configure database replication (optional)
- [ ] Set up database backups

### Grafana Nodes

- [ ] Install Grafana on each node
- [ ] Configure grafana.ini on all nodes:
  - [ ] Set `database` section to PostgreSQL
  - [ ] Set `server.root_url` to cluster hostname
  - [ ] Enable `unified_alerting` with HA settings
- [ ] Sync provisioning files across nodes
- [ ] Start Grafana on all nodes
- [ ] Verify all nodes can connect to database

### Load Balancer

- [ ] Deploy load balancer (nginx, HAProxy, cloud LB)
- [ ] Configure backend server pool
- [ ] Set up health checks (`/api/health`)
- [ ] Configure SSL termination
- [ ] Test failover scenarios
- [ ] Configure monitoring for load balancer

### Alerting HA

- [ ] Configure `ha_listen_address` on each node
- [ ] Set `ha_peers` with all node addresses
- [ ] Or configure Redis for HA alerting
- [ ] Test alert deduplication
- [ ] Verify alert routing consistency

### Validation

- [ ] Test failover: stop one node, verify access
- [ ] Verify dashboard edits persist across nodes
- [ ] Test alert firing from different nodes
- [ ] Verify session persistence
- [ ] Load test the cluster
- [ ] Document failover procedures

---

## Provisioning Checklist

### Data Sources

- [ ] Create datasources YAML file
- [ ] Configure each data source:
  - [ ] Name (unique)
  - [ ] Type (prometheus, loki, etc.)
  - [ ] URL
  - [ ] Access mode (proxy/direct)
  - [ ] Authentication
  - [ ] Default settings
- [ ] Set one as default (`isDefault: true`)
- [ ] Test connectivity after provisioning

### Dashboards

- [ ] Create dashboard provider YAML
- [ ] Organize dashboards in folders
- [ ] Export dashboards as JSON
- [ ] Configure update interval
- [ ] Set `editable` based on requirements
- [ ] Validate JSON syntax before deployment

### Alerting

- [ ] Define alert rules in YAML
- [ ] Configure contact points
- [ ] Set up notification policies
- [ ] Define mute timings (maintenance windows)
- [ ] Create alert templates
- [ ] Test full alerting pipeline

---

## Security Hardening Checklist

### Authentication

- [ ] Disable anonymous access (unless required)
- [ ] Configure OAuth/LDAP/SAML
- [ ] Set strong admin password
- [ ] Enable two-factor authentication (if available)
- [ ] Configure session timeout
- [ ] Set up API key rotation policy

### Authorization

- [ ] Create organizations for multi-tenancy
- [ ] Define roles (Viewer, Editor, Admin)
- [ ] Assign users to appropriate roles
- [ ] Configure data source permissions
- [ ] Set dashboard folder permissions
- [ ] Enable audit logging

### Network

- [ ] Enable HTTPS only
- [ ] Configure HSTS headers
- [ ] Set up firewall rules
- [ ] Use private networks for data sources
- [ ] Configure CORS if needed
- [ ] Enable rate limiting

### Secrets

- [ ] Store credentials in secrets manager
- [ ] Use environment variables for sensitive config
- [ ] Never commit secrets to version control
- [ ] Rotate credentials regularly
- [ ] Audit secret access

---

## Upgrade Checklist

### Pre-Upgrade

- [ ] Review release notes for breaking changes
- [ ] Backup database
- [ ] Backup provisioning files
- [ ] Export critical dashboards
- [ ] Test upgrade in staging environment
- [ ] Plan rollback procedure
- [ ] Schedule maintenance window

### Upgrade Process

- [ ] Stop Grafana service(s)
- [ ] Upgrade packages/images
- [ ] Run database migrations (automatic on start)
- [ ] Start Grafana service(s)
- [ ] Verify startup logs
- [ ] Test critical functionality

### Post-Upgrade

- [ ] Verify all data sources connected
- [ ] Check dashboards render correctly
- [ ] Test alerting pipeline
- [ ] Verify authentication works
- [ ] Update documentation
- [ ] Monitor for issues

---

## Grafana Alloy Migration Checklist

### Assessment

- [ ] Inventory existing Agent deployments
- [ ] Document current configurations
- [ ] Identify custom integrations
- [ ] List scrape targets
- [ ] Document remote write endpoints
- [ ] Plan migration timeline (before EOL Nov 2025)

### Conversion

- [ ] Install Grafana Alloy
- [ ] Convert static config:
  ```bash
  alloy convert --source-format=static --output=config.alloy config.yaml
  ```
- [ ] Or convert flow config:
  ```bash
  alloy convert --source-format=flow --output=config.alloy config.river
  ```
- [ ] Review converted configuration
- [ ] Fix any conversion warnings/errors

### Testing

- [ ] Run Alloy with converted config
- [ ] Verify all scrape targets discovered
- [ ] Check metrics flowing to remote write
- [ ] Compare metric counts before/after
- [ ] Test log collection (if applicable)
- [ ] Verify dashboards still work

### Deployment

- [ ] Deploy Alloy alongside Agent (parallel run)
- [ ] Monitor both for discrepancies
- [ ] Gradually shift traffic to Alloy
- [ ] Remove Agent deployment
- [ ] Update documentation
- [ ] Clean up old configurations

---

## Monitoring Grafana Checklist

### Metrics

- [ ] Enable `/metrics` endpoint
- [ ] Configure Prometheus to scrape Grafana
- [ ] Create Grafana self-monitoring dashboard
- [ ] Set up alerts for:
  - [ ] High request latency
  - [ ] Error rate increase
  - [ ] Database connection issues
  - [ ] Memory usage
  - [ ] Active sessions

### Logging

- [ ] Configure log level (info for production)
- [ ] Set up log aggregation (Loki, ELK)
- [ ] Create log-based alerts for errors
- [ ] Enable access logging
- [ ] Configure log rotation

### Health Checks

- [ ] Configure `/api/health` monitoring
- [ ] Set up uptime monitoring
- [ ] Create synthetic checks for critical dashboards
- [ ] Monitor data source health
- [ ] Set up PagerDuty/Opsgenie integration
