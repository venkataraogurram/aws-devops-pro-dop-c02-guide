[← 10. Hands-on labs](10-hands-on-labs.md) | [🏠 Home](README.md)

# Chapter 11 - Final Cheat Sheet (read on Dec 28 and the morning of Dec 29)

## Keyword -> answer reflexes

| If the question says... | Think... |
|---|---|
| "least operational overhead" | Managed/native feature. No custom Lambda polling, no EC2 cron |
| "all accounts, including new ones" | Organizations + StackSets service-managed auto-deploy / Control Tower / org Config rules / delegated admin auto-enable |
| "prevent" | SCP, RCP, permission boundary, IAM deny, CFN Hook / CT proactive, stack policy |
| "detect" | Config, GuardDuty, Security Hub, Access Analyzer, Inspector, Macie |
| "remediate automatically" | Config rule + SSM Automation, or EventBridge + Lambda/SSM |
| "no SSH" | Session Manager |
| "run command on fleet" | SSM Run Command (rate control) |
| "keep desired state" | SSM State Manager |
| "patch" | Patch Manager + Maintenance Window / patch policy |
| "golden AMI" | EC2 Image Builder (+ Parameter Store AMI ID, launch template, instance refresh) |
| "secrets rotation" | Secrets Manager |
| "config/flags, gradual, rollback" | AppConfig |
| "Lambda gradual deploy" | CodeDeploy canary/linear via SAM `DeploymentPreference` |
| "ECS test traffic before cutover" | CodeDeploy ECS blue/green + test listener |
| "ECS auto rollback, simple" | Deployment circuit breaker |
| "Beanstalk no capacity loss, safest" | Immutable; "test then switch" = blue/green Swap URLs |
| "Beanstalk send 10% real traffic" | Traffic splitting |
| "EC2 fast rollback" | CodeDeploy blue/green |
| "stack must wait for software install" | cfn-init + cfn-signal + CreationPolicy |
| "update config on running instance from CFN" | cfn-hup |
| "preview changes" | Change set |
| "find manual changes" | Drift detection |
| "protect DB from replacement" | Stack policy + UpdateReplacePolicy/DeletionPolicy Snapshot/Retain |
| "UPDATE_ROLLBACK_FAILED" | ContinueUpdateRollback, skip resources |
| "self-service approved products" | Service Catalog + launch constraint |
| "memory/disk metrics" | CloudWatch agent |
| "count errors in logs" | Metric filter -> alarm |
| "logs in real time to X" | Subscription filter -> Kinesis / Firehose / Lambda |
| "centralise logs" | Cross-account destination + Firehose -> S3 in Log Archive |
| "all metrics to 3rd party" | Metric streams |
| "seasonal threshold" | Anomaly detection |
| "reduce alarm noise" | Composite alarm |
| "trace across services" | X-Ray (annotations to search) |
| "probe before users notice" | Synthetics canary |
| "who did it (API)" | CloudTrail |
| "what changed (config)" | AWS Config |
| "logs not tampered" | CloudTrail log file validation |
| "S3 object reads audited" | CloudTrail data events |
| "unusual API activity" | CloudTrail Insights |
| "IAM/CloudFront event rule" | us-east-1 |
| "fan-out" | SNS -> SQS queues |
| "ordering" | SQS FIFO (group ID) / Kinesis (partition key) |
| "bad message loop" | DLQ (maxReceiveCount) |
| "stream stuck on bad record" | Bisect batch + max retries + on-failure destination |
| ">15 min multi-step" | Step Functions |
| "schedule" | EventBridge Scheduler |
| "EC2 maintenance event" | AWS Health -> EventBridge -> automation |
| "exposed key" | Health/GuardDuty -> EventBridge -> Lambda disables key |
| "compromised instance" | GuardDuty -> isolate SG + snapshot |
| "ops issues + runbooks in one place" | OpsCenter |
| "RPO 1 s / RTO 1 min relational" | Aurora Global Database |
| "multi-Region writes" | DynamoDB global tables |
| "cheapest DR" | Backup and restore |
| "only data running in DR" | Pilot light |
| "scaled-down copy running" | Warm standby |
| "server replication DR" | Elastic Disaster Recovery |
| "test resilience" | FIS; "assess RTO/RPO" = Resilience Hub |
| "immutable backups" | Backup Vault Lock compliance mode |
| "health check for private endpoint" | CloudWatch alarm-based Route 53 health check |
| "static IP, fast failover, UDP" | Global Accelerator |
| "ASG not replacing broken app" | Health check type ELB |
| "instances killed while booting" | Health check grace period |
| "slow boot, slow scale" | Warm pools / predictive scaling |
| "save logs before termination" | Lifecycle hook |
| "ECS tasks pending, no capacity" | Capacity provider managed scaling |
| "EKS nodes fast" | Karpenter |
| "cold starts" | Provisioned concurrency |
| "workforce SSO many accounts" | IAM Identity Center |
| "CI/CD without keys" | OIDC provider + role |
| "third-party role" | ExternalId |
| "delegate role creation safely" | Permissions boundary |
| "scale permissions by project" | ABAC tags |
| "only my org" | `aws:PrincipalOrgID` / RCP |
| "only via VPC endpoint" | `aws:SourceVpce` |
| "share encrypted snapshot/AMI" | CMK + key policy (not AWS managed key) |
| "single-tenant HSM" | CloudHSM |
| "imported cert expiry" | ACM DaysToExpiry / EventBridge / Config rule |
| "PII in S3" | Macie |
| "CVEs" | Inspector |
| "threats" | GuardDuty |
| "all findings + CIS score" | Security Hub |
| "investigate finding" | Detective |
| "external access" | IAM Access Analyzer |
| "block IP at subnet" | NACL deny |
| "SQLi/XSS/rate limit" | WAF |
| "DDoS + response team" | Shield Advanced |
| "egress domain allow-list" | Network Firewall |
| "same firewall rules everywhere" | Firewall Manager |

## Orders to remember
- **buildspec**: install -> pre_build -> build -> post_build.
- **CodeDeploy EC2 in-place**: ApplicationStop -> DownloadBundle -> BeforeInstall -> Install -> AfterInstall -> ApplicationStart -> ValidateService (plus Block/Allow traffic hooks around them with an LB).
- **CodeDeploy ECS**: BeforeInstall -> Install -> AfterInstall -> AllowTestTraffic -> AfterAllowTestTraffic -> BeforeAllowTraffic -> AllowTraffic -> AfterAllowTraffic.
- **CodeDeploy Lambda**: BeforeAllowTraffic -> AllowTraffic -> AfterAllowTraffic.
- **cfn-init config keys**: packages -> groups -> users -> sources -> files -> commands -> services.
- **Secrets Manager rotation**: createSecret -> setSecret -> testSecret -> finishSecret.
- **DR cost/speed**: Backup & restore < Pilot light < Warm standby < Multi-site.
- **IAM evaluation**: explicit deny -> SCP/RCP -> resource policy -> identity policy -> boundary -> session policy.

## Traps to avoid
- ApplicationStop runs the **old** revision's script.
- AWS managed KMS keys **can't** be shared cross-account.
- SCPs **don't** grant permissions and don't affect the management account.
- Config **detects**; it doesn't prevent.
- EC2 has **no** memory metric by default.
- CodeBuild in a public subnet has **no** public IP.
- Logs export to S3 is **not** real time.
- CloudTrail **data events** are off by default.
- Global service events go to **us-east-1**.
- Service-managed StackSets **skip the management account**.
- Lambda max **15 min**; use Step Functions for longer.
- Can't encrypt an existing RDS/EBS **in place**: snapshot -> encrypted copy -> restore.
- CloudFront certificates must be in **us-east-1**.
- ALB with all targets unhealthy **fails open**.
- Don't put the production RDS inside a Beanstalk environment.

**You have prepared. Read slowly, trust the qualifiers, answer everything. All the best, Venkata!**

---

[← 10. Hands-on labs](10-hands-on-labs.md) | [🏠 Home](README.md)
