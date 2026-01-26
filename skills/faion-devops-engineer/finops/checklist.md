# FinOps Implementation Checklist

## Phase 1: INFORM (Visibility)

### Billing & Data Collection

- [ ] Enable detailed billing exports (AWS CUR, GCP BigQuery, Azure Cost Management)
- [ ] Configure billing data refresh frequency (daily minimum)
- [ ] Set up centralized cost data storage
- [ ] Integrate multi-cloud billing (if applicable)
- [ ] Enable resource-level cost attribution

### Tagging Strategy

- [ ] Define mandatory tag schema:
  - [ ] `Environment` (prod, staging, dev, test)
  - [ ] `Owner` (team or individual)
  - [ ] `Project` or `Application`
  - [ ] `CostCenter` or `BusinessUnit`
- [ ] Implement tag enforcement policies
- [ ] Create untagged resource reports
- [ ] Set up tag compliance dashboards
- [ ] Achieve >80% tag coverage (initial target)
- [ ] Achieve >90% tag coverage (mature target)

### Cost Allocation

- [ ] Map organizational hierarchy to cost structure
- [ ] Define shared cost allocation rules
- [ ] Implement showback reports per team
- [ ] Set up chargeback (if required)
- [ ] Configure cost allocation for:
  - [ ] Compute resources
  - [ ] Storage resources
  - [ ] Network/data transfer
  - [ ] SaaS subscriptions

### Dashboards & Reporting

- [ ] Create executive cost summary dashboard
- [ ] Build team-level cost views
- [ ] Set up daily/weekly cost reports
- [ ] Configure cost trend visualizations
- [ ] Enable real-time cost visibility

### Anomaly Detection

- [ ] Enable cloud-native anomaly detection
- [ ] Configure custom anomaly thresholds
- [ ] Set up alert routing (Slack, email, PagerDuty)
- [ ] Define anomaly investigation workflow
- [ ] Create anomaly response runbook

## Phase 2: OPTIMIZE (Efficiency)

### Compute Optimization

- [ ] Run rightsizing analysis (weekly)
- [ ] Identify idle instances (>7 days low utilization)
- [ ] Implement auto-scaling policies
- [ ] Evaluate Spot/Preemptible instance opportunities
- [ ] Review and optimize instance families
- [ ] Implement scheduling for non-production workloads

### Commitment Discounts

- [ ] Analyze usage patterns (minimum 30 days data)
- [ ] Calculate Reserved Instance / Savings Plan recommendations
- [ ] Determine optimal commitment term (1yr vs 3yr)
- [ ] Review payment options (all upfront, partial, no upfront)
- [ ] Implement Savings Plans for compute
- [ ] Evaluate Reserved Instances for databases

### Storage Optimization

- [ ] Implement storage lifecycle policies
- [ ] Move infrequently accessed data to cold storage
- [ ] Delete orphaned snapshots and volumes
- [ ] Optimize backup retention policies
- [ ] Review and compress large datasets
- [ ] Implement intelligent tiering (S3, GCS)

### Network Optimization

- [ ] Analyze data transfer costs
- [ ] Optimize cross-region traffic
- [ ] Review NAT Gateway usage
- [ ] Evaluate CDN for static content
- [ ] Implement VPC endpoints where applicable

### AI/ML Workload Optimization

- [ ] Implement GPU utilization monitoring
- [ ] Use Spot instances for training with checkpointing
- [ ] Implement model quantization for inference
- [ ] Set up response caching for LLM calls
- [ ] Configure request batching
- [ ] Establish approval workflows for expensive resources

### Waste Elimination

- [ ] Identify and terminate zombie resources
- [ ] Remove unattached volumes
- [ ] Clean up unused IP addresses
- [ ] Delete old container images
- [ ] Review and cancel unused Reserved Instances

## Phase 3: OPERATE (Continuous Improvement)

### Governance

- [ ] Establish FinOps team/role
- [ ] Define cost ownership model
- [ ] Create budget allocation process
- [ ] Implement cost approval workflows
- [ ] Set up cost anomaly escalation procedures

### Budgeting & Forecasting

- [ ] Set monthly/quarterly budgets per team
- [ ] Configure budget alerts (50%, 80%, 100%, 120%)
- [ ] Implement forecasting models
- [ ] Review forecast accuracy monthly
- [ ] Establish variance analysis process

### Automation

- [ ] Automate rightsizing recommendations
- [ ] Implement auto-termination for dev resources
- [ ] Set up automated scaling policies
- [ ] Configure automated tagging remediation
- [ ] Enable automated cost optimization suggestions

### Culture & Process

- [ ] Conduct monthly cost review meetings
- [ ] Include cost metrics in engineering reviews
- [ ] Add cost awareness to CI/CD pipelines
- [ ] Create FinOps documentation and runbooks
- [ ] Establish cost optimization KPIs

### Metrics & Reporting

- [ ] Track cost per unit of work
- [ ] Monitor commitment utilization rate
- [ ] Measure waste percentage trends
- [ ] Report savings achieved
- [ ] Calculate FinOps ROI

## Maturity Assessment

### Crawl Stage

- [ ] Basic visibility into cloud costs
- [ ] Initial tagging in place
- [ ] Manual cost reviews
- [ ] Reactive optimization

### Walk Stage

- [ ] >80% tag coverage
- [ ] Regular cost review meetings
- [ ] Some automation in place
- [ ] Proactive rightsizing

### Run Stage

- [ ] >90% tag coverage
- [ ] Automated optimization
- [ ] Real-time cost visibility
- [ ] Cost-aware engineering culture
- [ ] Continuous improvement cycle

## Sources

- [FinOps Foundation Framework](https://www.finops.org/framework/)
- [FinOps Capabilities](https://www.finops.org/framework/capabilities/)
- [How to Optimize Cloud Usage](https://www.finops.org/wg/how-to-optimize-cloud-usage/)
