[← 6. Domain 6: Security and Compliance (17%)](06-security-compliance.md) | [🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [8. 60 practice questions →](08-practice-questions.md)

# Chapter 7 - "Which one?" Comparisons and Numbers to Memorise

> The exam is mostly "pick between 2 similar services". These tables are the fastest revision you can do in the last week.

## 7.1 Confusing pairs

| A | B | Pick A when | Pick B when |
|---|---|---|---|
| CloudTrail | AWS Config | "**Who** called which API, when, from where" | "**What** the resource configuration was/is, is it compliant" |
| CloudTrail | CloudWatch Logs | API audit | Application/OS logs |
| CloudWatch Logs subscription | Export to S3 | Real time | One-off batch archive |
| Kinesis Data Streams | Data Firehose | Custom consumers, replay, ordering, real time (ms) | Managed delivery to S3/OpenSearch/Redshift/Splunk, near real time (buffer 0-900 s), no code |
| SQS | SNS | Buffer, pull, one consumer group, retries | Push to many subscribers (fan-out) |
| SNS | EventBridge | Very high throughput fan-out, mobile/SMS/email | Content-based rules on AWS service events, SaaS, cross-account buses, schedules, archive/replay |
| SQS Standard | SQS FIFO | Max throughput, order not required | Order + exactly-once per group |
| Lambda | Step Functions | One short task (<15 min) | Multi-step, waits, retries, branching, human approval, long-running |
| Step Functions | SSM Automation | App/business workflow, any service | Operational runbook on AWS resources/instances, Config remediation |
| SSM Run Command | SSM State Manager | One-off command now | Keep desired state on a schedule, new instances too |
| SSM Automation | Run Command | Multi-step AWS API actions (stop, snapshot, AMI) | Script inside the OS |
| Session Manager | Bastion host | Always on exam (no SSH, audited) | Never on exam if Session Manager is an option |
| Parameter Store | Secrets Manager | Config, cheap, no rotation | Rotation, cross-Region replicas, cross-account secret sharing |
| Secrets Manager | KMS | Store secret values | Manage encryption keys |
| KMS | CloudHSM | Managed, multi-tenant, integrated with services | Single-tenant HSM, you own keys, FIPS L3, custom crypto |
| AWS managed key | Customer managed key | Default, no control needed | Cross-account sharing, key policy control, custom rotation, disable/delete |
| Security group | NACL | Stateful allow rules per ENI | Stateless, explicit **deny** (block an IP), subnet-level |
| WAF | Shield Advanced | L7 rules (SQLi, XSS, rate, geo, bots) | DDoS response team, cost protection, L3/L4/L7 DDoS |
| WAF | Network Firewall | HTTP(S) at CloudFront/ALB/API GW | VPC-level any protocol, domain filtering, IPS |
| GuardDuty | Inspector | Threats/active compromise | Vulnerabilities (CVEs) |
| GuardDuty | Detective | Detect | Investigate root cause |
| Security Hub | Config | Aggregate findings + standards score | Evaluate configuration (Security Hub uses Config under the hood) |
| Macie | Inspector | Sensitive data in S3 | Software vulnerabilities |
| Access Analyzer | Trusted Advisor | External/unused access, policy validation | Broad best-practice checks incl. limits and cost |
| SCP | Permissions boundary | Org/OU/account-level max | Per-user/role max (delegation inside an account) |
| SCP | IAM policy | Restrict (never grant) | Grant |
| Control Tower | Organizations | Turn-key governed landing zone, account factory, controls | Raw account grouping, SCPs, consolidated billing |
| StackSets self-managed | StackSets service-managed | Accounts outside org / custom roles | Org OUs, auto-deploy new accounts, delegated admin |
| Nested stacks | Cross-stack exports | Reuse components inside one deployment unit | Share values between independently managed stacks |
| Change set | Drift detection | Before update: what will change | After: what changed outside CFN |
| Stack policy | Termination protection | Protect resources from updates/replacement | Protect stack from deletion |
| DeletionPolicy | UpdateReplacePolicy | On stack/resource deletion | On replacement during update |
| CreationPolicy | WaitCondition | Wait for EC2/ASG signals | External/ordering signals |
| cfn-init | cfn-hup | Initial configuration | Re-apply on metadata change |
| CloudFormation | CDK | YAML/JSON declarative | Programming languages, higher-level constructs |
| CloudFormation | Service Catalog | Infra team deploys | End users self-service approved products |
| CodeDeploy in-place | CodeDeploy blue/green | Cheaper, same instances, downtime per instance | Zero-downtime, fast rollback, new instances |
| Beanstalk Immutable | Beanstalk Blue/Green | Same env, new instances, safe rollback | Separate env, DNS swap, test before swap, platform/major changes |
| Beanstalk Rolling | Rolling with additional batch | OK to reduce capacity | Must keep full capacity |
| Canary | Linear | Small test slice then all | Equal steps over time |
| ECS circuit breaker | CodeDeploy ECS blue/green | Rolling updates with auto rollback, least effort | Test traffic, controlled shifting, instant rollback |
| Route 53 failover | Global Accelerator | DNS-based DR, cheap | Static IPs, fast failover not affected by DNS caching, non-HTTP |
| Route 53 latency | Geolocation | Best performance | Compliance / content by country |
| Aurora Global DB | RDS cross-Region read replica | RPO ~1 s, RTO < 1 min, managed switchover | Cheaper, non-Aurora engines, manual promote |
| DynamoDB global tables | DynamoDB PITR | Multi-Region active-active | Recover from accidental writes/deletes |
| RDS Multi-AZ | Read replica | HA (sync standby, auto failover) | Read scaling (async), cross-Region DR |
| Pilot light | Warm standby | Only data running in DR | Scaled-down full stack running |
| AWS Backup | DRS (Elastic Disaster Recovery) | Policy-based backups, cheap, hours RTO | Server replication, seconds RPO, minutes RTO |
| Target tracking | Step scaling | Keep metric at a value (default best) | Different actions for different breach sizes |
| Scheduled scaling | Predictive scaling | Known fixed times | Recurring patterns learned automatically |
| Cluster Autoscaler | Karpenter | Existing node groups/ASGs | Fast, right-sized, Spot-aware node provisioning |
| Reserved concurrency | Provisioned concurrency | Limit/guarantee concurrency | Remove cold starts |
| X-Ray annotations | X-Ray metadata | Searchable/indexed | Extra data, not searchable |
| Metric filter | Subscription filter | Logs -> metric -> alarm | Logs -> stream to other service |
| Logs Insights | Athena | Query CloudWatch Logs | Query S3 data (CloudTrail, ALB, VPC flow logs in S3) |
| CloudWatch dashboards | QuickSight | Ops metrics | BI / business analytics from Athena/S3 |
| CloudTrail Lake | Athena on CloudTrail S3 | Managed SQL over events, no table setup | You already have logs in S3, cheapest |
| Synthetics | RUM | Scripted probes 24x7 | Real users' browser experience |
| AppConfig | Parameter Store | Validated, gradual config/feature flag rollout with rollback | Simple config storage |
| CodeArtifact | ECR | Language packages (npm, pip, Maven) | Container images |
| Image Builder | Packer on EC2 | Managed AMI/container pipeline (exam answer) | Only if question requires Packer |
| Health event | Trusted Advisor | AWS-side events affecting you | Account best practices |
| OpsCenter | Incident Manager | Aggregate operational work items (OpsItems) | Major incident response with on-call/escalation |
| Instance refresh | CFN rolling update | ASG not owned by CFN / just new AMI | ASG defined in CFN template |

## 7.2 Numbers to memorise

| Item | Number |
|---|---|
| Exam | 75 Q (65 scored), 180 min, pass 750/1000 |
| CloudTrail event history | 90 days (management events) |
| CloudTrail delivery to S3 | ~5 min average |
| CloudTrail Lake retention | up to ~10 years (3,653 days) depending on pricing option |
| CloudWatch metric retention | 1 s: 3 h, 1 min: 15 days, 5 min: 63 days, 1 h: 15 months |
| EC2 basic / detailed monitoring | 5 min / 1 min |
| High-resolution metric | 1 s; alarm periods 10 s / 30 s |
| Logs export task | up to 12 h |
| Log group subscription filters | 2 per log group |
| CodePipeline manual approval timeout | 7 days |
| CodeBuild timeout | 5 min - 36 h (default 60 min) |
| CodeDeploy agent revisions kept | 5 (default) |
| CodeArtifact token | max 12 h |
| CFN custom resource default timeout | 1 hour |
| CFN rollback trigger monitoring time | 0-180 min |
| cfn-hup interval | 15 min default |
| StackSets | Max concurrent accounts / failure tolerance in number or % |
| ASG lifecycle hook | heartbeat default 1 h (30 s-2 h); total wait max 48 h or 100 x heartbeat |
| ASG predictive scaling history | 14 days used to forecast (needs 24 h min) |
| ELB deregistration delay | 300 s default |
| Lambda timeout | 15 min max |
| Lambda async retries | 2 (event age up to 6 h) |
| SQS retention | 1 min - 14 days (default 4 days) |
| SQS visibility timeout | 0 s - 12 h (default 30 s) |
| SQS message size | 1 MiB (was 256 KB) |
| SQS long polling | up to 20 s |
| SQS delay | up to 15 min |
| Kinesis retention | 24 h default, up to 365 days |
| Kinesis shard | 1 MB/s or 1,000 rec/s in; 2 MB/s out |
| Step Functions Standard / Express | 1 year / 5 min |
| EventBridge targets per rule | 5 |
| EventBridge retry | up to 24 h / 185 attempts |
| RDS automated backups | 1-35 days |
| RDS Multi-AZ failover | ~60-120 s (Multi-AZ DB cluster ~35 s) |
| Aurora | 6 copies / 3 AZs; up to 15 replicas; Global DB replication < 1 s, RTO < 1 min |
| DynamoDB PITR | 1-35 days (configurable) |
| S3 RTC | 99.99% replicated within 15 min |
| Secrets Manager rotation | as often as every 4 h |
| Parameter Store | standard 4 KB / 10,000 params; advanced 8 KB / 100,000, policies |
| KMS key deletion wait | 7-30 days |
| KMS direct encrypt | 4 KB |
| KMS automatic rotation | default yearly (90 days - 7 years) |
| ACM expiry events | from 45 days before |
| STS role session | 1 h default, up to 12 h; role chaining 1 h |
| API Gateway REST integration timeout | 29 s default |
| SLA 99.9 / 99.99 / 99.999 | 43.8 min / 4.4 min / 26 s per month |

## 7.3 "Least operational overhead" defaults (when in doubt)
- Notifications -> **EventBridge rule -> SNS**.
- Scheduled jobs -> **EventBridge Scheduler**.
- Fleet commands -> **SSM Run Command**; desired state -> **State Manager**; patching -> **Patch Manager** (+ Quick Setup policy).
- Compliance -> **AWS Config managed rule + SSM Automation remediation** (org conformance pack for many accounts).
- Multi-account deployment -> **StackSets service-managed** / **Control Tower**.
- Human access -> **IAM Identity Center**.
- Secrets -> **Secrets Manager** with rotation.
- Logs to S3/OpenSearch -> **Firehose**.
- Lambda gradual deploy -> **SAM DeploymentPreference**.
- ECS rollback -> **circuit breaker**; ECS blue/green -> **CodeDeploy**.
- Golden AMIs -> **EC2 Image Builder**.
- Packages cache -> **CodeArtifact**.
- Vulnerability scanning -> **Inspector**; threat detection -> **GuardDuty**; aggregation -> **Security Hub**.

---

[← 6. Domain 6: Security and Compliance (17%)](06-security-compliance.md) | [🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [8. 60 practice questions →](08-practice-questions.md)
