---
name: deploy-blue-green-canary
description: Run zero-downtime releases via blue/green ECS+ALB cutover (10 s) or canary weighted routing (5%→25%→100%).
tier: pro
group: devops-cicd
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have two repeatable release patterns wired into your AWS environment: a blue/green deployment that switches 100% of traffic between two ECS services in under 10 seconds with instant rollback, and a canary deployment that progressively shifts traffic through 5% → 25% → 100% stages using ALB weighted target groups. You will know which pattern to pick for each release type and how to roll back either one in under two minutes.

## Prerequisites

- AWS CLI v2 installed and configured (`aws configure`). Profile must have `ecs:*`, `elasticloadbalancing:*`, `iam:PassRole` on the target cluster.
- An ECS cluster with at least one running service (`myapp-blue`) behind an Application Load Balancer. The ALB listener must forward on port 443 (or 80 for internal).
- Two ECS task definitions already registered — `myapp:blue-revision` and `myapp:green-revision`. Both use the same container port (e.g., 8080).
- Three ALB target groups created in advance: `myapp-blue-tg`, `myapp-green-tg`, `myapp-canary-tg`. All three point to port 8080, health-check path `/health`.
- `jq` installed locally (used in verification commands).
- For canary: nginx is acceptable as an alternative to ALB weighted routing — see Steps.
- Prior playbook: `production-cicd-pipeline` (CI pipeline that builds and pushes the container image).

## Steps

### Blue/Green with ECS + ALB

Blue/green swaps the ALB listener rule's default forward action from the active (blue) target group to the idle (green) target group. The green service has already been started and has passed health checks before the cutover.

1. Register the new task definition revision and capture its ARN:

   ```bash
   GREEN_TASK_DEF=$(aws ecs register-task-definition \
     --cli-input-json file://task-def-green.json \
     --query 'taskDefinition.taskDefinitionArn' \
     --output text)
   echo "Green task def: $GREEN_TASK_DEF"
   ```

2. Update the idle ECS service (`myapp-green`) to run the new revision:

   ```bash
   aws ecs update-service \
     --cluster myapp-cluster \
     --service myapp-green \
     --task-definition "$GREEN_TASK_DEF" \
     --desired-count 2
   ```

3. Wait for the green service to stabilise (all tasks healthy in target group):

   ```bash
   aws ecs wait services-stable \
     --cluster myapp-cluster \
     --services myapp-green
   # Exits 0 when all tasks are RUNNING; max wait ~10 minutes.
   ```

4. Retrieve the ALB listener ARN and the current default-action rule ARN:

   ```bash
   LISTENER_ARN=$(aws elbv2 describe-listeners \
     --load-balancer-arn arn:aws:elasticloadbalancing:eu-west-1:123456789012:loadbalancer/app/myapp-alb/abc123 \
     --query 'Listeners[?Port==`443`].ListenerArn' \
     --output text)

   RULE_ARN=$(aws elbv2 describe-rules \
     --listener-arn "$LISTENER_ARN" \
     --query 'Rules[?IsDefault==`true`].RuleArn' \
     --output text)
   ```

5. Switch 100% of traffic to the green target group (the cutover — completes in < 10 seconds):

   ```bash
   GREEN_TG_ARN=$(aws elbv2 describe-target-groups \
     --names myapp-green-tg \
     --query 'TargetGroups[0].TargetGroupArn' \
     --output text)

   aws elbv2 modify-rule \
     --rule-arn "$RULE_ARN" \
     --actions '[{"Type":"forward","TargetGroupArn":"'"$GREEN_TG_ARN"'"}]'
   ```

6. Scale the old blue service down to 0 (keep it registered for fast rollback):

   ```bash
   aws ecs update-service \
     --cluster myapp-cluster \
     --service myapp-blue \
     --desired-count 0
   ```

7. **Rollback (if needed)** — point the listener back at the blue target group and scale blue up:

   ```bash
   BLUE_TG_ARN=$(aws elbv2 describe-target-groups \
     --names myapp-blue-tg \
     --query 'TargetGroups[0].TargetGroupArn' \
     --output text)

   aws elbv2 modify-rule \
     --rule-arn "$RULE_ARN" \
     --actions '[{"Type":"forward","TargetGroupArn":"'"$BLUE_TG_ARN"'"}]'

   aws ecs update-service \
     --cluster myapp-cluster \
     --service myapp-blue \
     --desired-count 2
   ```

---

### Canary with ALB weighted routing (5% → 25% → 100%)

Use canary for high-risk migrations: schema changes, payment-flow rewrites, third-party API switches. Weighted routing lets you observe error rates at each stage before committing.

1. Deploy the canary revision to `myapp-canary` ECS service (same cluster):

   ```bash
   aws ecs update-service \
     --cluster myapp-cluster \
     --service myapp-canary \
     --task-definition "$GREEN_TASK_DEF" \
     --desired-count 1

   aws ecs wait services-stable \
     --cluster myapp-cluster \
     --services myapp-canary
   ```

2. Retrieve all three target group ARNs:

   ```bash
   BLUE_TG_ARN=$(aws elbv2 describe-target-groups --names myapp-blue-tg \
     --query 'TargetGroups[0].TargetGroupArn' --output text)
   CANARY_TG_ARN=$(aws elbv2 describe-target-groups --names myapp-canary-tg \
     --query 'TargetGroups[0].TargetGroupArn' --output text)
   ```

3. Stage 1 — send 5% of traffic to the canary:

   ```bash
   aws elbv2 modify-rule \
     --rule-arn "$RULE_ARN" \
     --actions '[
       {"Type":"forward","ForwardConfig":{"TargetGroups":[
         {"TargetGroupArn":"'"$BLUE_TG_ARN"'","Weight":95},
         {"TargetGroupArn":"'"$CANARY_TG_ARN"'","Weight":5}
       ]}}
     ]'
   ```

4. Monitor for 10 minutes. Check error rate in CloudWatch (substitute your log group):

   ```bash
   aws cloudwatch get-metric-statistics \
     --namespace AWS/ApplicationELB \
     --metric-name HTTPCode_Target_5XX_Count \
     --dimensions Name=TargetGroup,Value="$(basename $CANARY_TG_ARN)" \
     --start-time "$(date -u -d '10 minutes ago' +%Y-%m-%dT%H:%M:%SZ)" \
     --end-time "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
     --period 600 --statistics Sum \
     --query 'Datapoints[0].Sum'
   ```

   Accept if result is `null` or `0`. Abort and roll back to 0% canary if > 1% error increase.

5. Stage 2 — raise to 25%:

   ```bash
   aws elbv2 modify-rule \
     --rule-arn "$RULE_ARN" \
     --actions '[
       {"Type":"forward","ForwardConfig":{"TargetGroups":[
         {"TargetGroupArn":"'"$BLUE_TG_ARN"'","Weight":75},
         {"TargetGroupArn":"'"$CANARY_TG_ARN"'","Weight":25}
       ]}}
     ]'
   ```

   Monitor for another 10 minutes using the same CloudWatch query.

6. Stage 3 — cut over to 100% (same as blue/green cutover step 5 above, targeting the canary TG):

   ```bash
   aws elbv2 modify-rule \
     --rule-arn "$RULE_ARN" \
     --actions '[{"Type":"forward","TargetGroupArn":"'"$CANARY_TG_ARN"'"}]'
   ```

   Scale old blue service to 0. Rename canary → blue for the next release cycle.

7. **nginx alternative** — if you run nginx in front of ECS instead of ALB, weighted upstream config:

   ```nginx
   upstream myapp_weighted {
       server 10.0.1.20:8080 weight=95;   # blue
       server 10.0.1.30:8080 weight=5;    # canary
   }
   ```

   Adjust weights progressively in the same 5/25/100 pattern, reload with `nginx -s reload` (zero downtime).

   **Rollback canary** — set canary weight to 0 and scale `myapp-canary` desired count to 0:

   ```bash
   aws elbv2 modify-rule \
     --rule-arn "$RULE_ARN" \
     --actions '[{"Type":"forward","TargetGroupArn":"'"$BLUE_TG_ARN"'"}]'

   aws ecs update-service \
     --cluster myapp-cluster \
     --service myapp-canary \
     --desired-count 0
   ```

---

### Decision rule: blue/green vs. canary

| Criteria | Blue/Green | Canary |
|----------|-----------|--------|
| Stateless service (no DB schema change) | ✅ preferred | acceptable |
| DB migration / backwards-incompatible API | ❌ avoid | ✅ required |
| High-traffic launch with unknown load profile | acceptable | ✅ preferred |
| Hotfix — need 100% cutover immediately | ✅ preferred | ❌ too slow |
| Third-party integration change | acceptable | ✅ preferred |

## Verify

After completing blue/green cutover, confirm the listener routes only to the green target group:

```bash
aws elbv2 describe-rules \
  --listener-arn "$LISTENER_ARN" \
  --query 'Rules[?IsDefault==`true`].Actions[0].TargetGroupArn' \
  --output text
```

The output must match `$GREEN_TG_ARN`.

For canary stage verification, check the healthy host count in the canary target group:

```bash
aws elbv2 describe-target-health \
  --target-group-arn "$CANARY_TG_ARN" \
  --query 'TargetHealthDescriptions[*].{id:Target.Id,state:TargetHealth.State}' \
  --output table
```

All targets must show `healthy`. If any show `draining` or `unhealthy`, do not advance to the next stage.

For a live smoke test after 100% cutover:

```bash
curl -sf https://myapp.faion.net/health | jq '.version'
```

The returned version string must match the newly deployed image tag.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `aws ecs wait services-stable` times out after 10 min | New tasks crash-looping (OOM, missing env var, bad image tag) | Check `aws ecs describe-tasks --cluster myapp-cluster --tasks $(aws ecs list-tasks --cluster myapp-cluster --service-name myapp-green --query 'taskArns[0]' --output text)` for `stoppedReason`; fix the task definition before retrying |
| ALB returns 502 after cutover | Target group health check failing on new revision | Run `aws elbv2 describe-target-health --target-group-arn "$GREEN_TG_ARN"` — if `unhealthy`, check container port mapping and `/health` endpoint response code (must be 200) |
| `modify-rule` returns `InvalidAction` | ALB listener does not support weighted forwarding (must use ALBv2 with `ForwardConfig`) | Confirm listener type: `aws elbv2 describe-listeners --listener-arns "$LISTENER_ARN" --query 'Listeners[0].Protocol'` — must be `HTTPS` or `HTTP`, not `TCP` |
| Canary error rate spikes at 5% stage | New code path error under real traffic | Roll back immediately (step 7 of canary section), open CloudWatch Logs Insights on the canary task log group for the root cause before rescheduling the release |
| Blue service fails to scale back up after rollback | Desired count reset but launch config missing Fargate capacity | Check `aws ecs describe-services --services myapp-blue` for `deploymentConfiguration`; ensure `capacityProviderStrategy` still references `FARGATE` or `FARGATE_SPOT` |
| nginx `weight=0` still routes some requests | nginx master process not reloaded | Run `nginx -t && nginx -s reload`; verify with `nginx -T | grep upstream -A4` |

## Next

- `production-cicd-pipeline` — integrate the blue/green cutover commands as a post-deploy stage in your GitHub Actions pipeline, gated behind a manual approval step.
- Read `gitops-progressive-delivery` methodology for ArgoCD-native progressive delivery with automatic rollback on Prometheus alert thresholds.
- `infra-engineering` playbooks — automate target group creation with Terraform so each environment (`staging`, `prod`) has its own isolated blue/green pair.

## References

- [knowledge/pro/infra/devops-engineer/devops-lb-health-checks](../../../knowledge/pro/infra/devops-engineer/devops-lb-health-checks) — defines the health-check contract (path, interval, thresholds) that the green and canary target groups must pass before any traffic shift proceeds in Steps 3 and 3-canary.
- [knowledge/pro/infra/devops-engineer/devops-lb-high-availability](../../../knowledge/pro/infra/devops-engineer/devops-lb-high-availability) — underpins the two-service (blue + green) topology: HA requirements mean the idle service stays registered at desired-count 0, not deleted, enabling sub-60-second rollback.
- [knowledge/pro/infra/cicd-engineer/gha-deployment-patterns](../../../knowledge/pro/infra/cicd-engineer/gha-deployment-patterns) — maps the manual-gate pattern used between canary stages to GitHub Actions `environment: production` protection rules, referenced in the Next section pipeline integration.
- [knowledge/pro/infra/cicd-engineer/gitops-progressive-delivery](../../../knowledge/pro/infra/cicd-engineer/gitops-progressive-delivery) — provides the automated rollback framework (metric thresholds → weight-to-zero) that the Next section upgrade path builds on.
