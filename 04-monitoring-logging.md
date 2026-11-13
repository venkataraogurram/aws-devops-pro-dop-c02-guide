[← 3. Domain 3: Resilient Cloud Solutions (15%)](03-resilient-cloud.md) | [🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [5. Domain 5: Incident and Event Response (14%) →](05-incident-event-response.md)

# Chapter 4 - Domain 4: Monitoring and Logging (15%)

> CloudWatch (metrics, alarms, logs, Logs Insights, subscriptions, agent, dashboards, anomaly detection, Synthetics), X-Ray, CloudTrail, log storage/encryption, and the "process logs in real time" pipelines.

## Services to study for this domain

Read these service files first, then the sections below.

- [Amazon EC2 Auto Scaling](services/ec2-auto-scaling.md)
- [Elastic Load Balancing and compute high availability](services/elastic-load-balancing.md)
- [AWS Systems Manager](services/systems-manager.md)
- [AWS Config](services/config.md)
- [Amazon S3 (events, integrity, protection)](services/s3.md)
- [Amazon Route 53](services/route53.md)
- [Amazon CloudWatch (metrics, alarms, logs, agent, synthetics)](services/cloudwatch.md)
- [AWS X-Ray](services/xray.md)
- [AWS CloudTrail](services/cloudtrail.md)
- [Athena and QuickSight (log analytics)](services/analytics-athena-quicksight.md)

## 4.1 Other logs you must know

| Log | What | Destination |
|---|---|---|
| **VPC Flow Logs** | IP traffic metadata (src/dst IP, port, protocol, ACCEPT/REJECT) for VPC/subnet/ENI. Not packet contents. Custom format fields (`pkt-srcaddr`, `tcp-flags`, `flow-direction`) | CloudWatch Logs, S3, Firehose. Query with Logs Insights / Athena. REJECT = SG or NACL blocked |
| **ELB access logs** | Each request (client IP, latency, path, status codes, TLS) | S3 only (every 5 min). Bucket policy for ELB service. Connection logs too |
| **CloudFront logs** | Standard logs to S3 (or CloudWatch/Firehose with v2), **real-time logs** to Kinesis Data Streams | |
| **S3 server access logs** | Requests to a bucket (best effort) | Another S3 bucket. (CloudTrail data events are the reliable alternative) |
| **Route 53 query logs** | Public DNS queries (CloudWatch Logs us-east-1); **Resolver query logs** for VPC DNS | |
| **API Gateway logs** | Execution logs + **access logs** (custom format) | CloudWatch Logs (needs account-level role ARN) / Firehose |
| **WAF logs** | Full request logs | CloudWatch Logs, S3, Firehose (names must start `aws-waf-logs-`) |
| **RDS logs** | Error, slow query, general, audit logs | Publish to CloudWatch Logs |
| **Session Manager logs** | Shell session transcripts | S3 / CloudWatch Logs |
| **CodeBuild / Lambda / ECS** | Build/function/container stdout | CloudWatch Logs |
| **EKS control plane logs** | api, audit, authenticator, controllerManager, scheduler | CloudWatch Logs (enable per type) |

## 4.2 Log storage, security and lifecycle
- **CloudWatch Logs retention** per log group (set it - default is never expire = cost). Automate with Config rule `cw-loggroup-retention-period-check` + remediation, or an EventBridge rule on `CreateLogGroup` -> Lambda sets retention.
- Long-term storage: export/stream to **S3** with **lifecycle rules** (Standard -> Standard-IA -> Glacier Flexible Retrieval/Deep Archive -> expire). **S3 Object Lock** (compliance mode) for WORM retention. Glacier **Vault Lock**.
- **Encryption at rest:** CloudWatch Logs with KMS CMK (`associate-kms-key`); S3 SSE-S3/SSE-KMS (bucket key to reduce KMS cost); **client-side** encryption if data must be encrypted before leaving the app. **In transit**: HTTPS/TLS to all endpoints.
- **Access control:** IAM policies on `logs:*` with resource ARNs; **centralised Log Archive account** with bucket policy that allows only `PutObject` from org accounts (condition `aws:PrincipalOrgID`), deny delete; separate read-only role for auditors.
- **IAM for log collection:** instance profile (CloudWatch agent), Lambda execution role, ECS task execution role (`awslogs`), Firehose role to write S3, CloudWatch Logs role to put into Kinesis for subscriptions (`logs.amazonaws.com` trust).

## 4.3 Automating monitoring and event management (Task 4.3)

- **S3 Event Notifications** (to SNS, SQS, Lambda, or EventBridge for advanced filtering and many targets) -> e.g., new log file in S3 -> Lambda parses and loads into OpenSearch / CloudWatch Logs.
- **EventBridge** rules on service events -> SNS/Lambda/SSM Automation/Step Functions.
- **Alarm -> action**: SNS (email/SMS/Chatbot to Slack/Teams), Lambda, EC2 recover/reboot, ASG scaling, OpsItem.
- **EC2 automatic recovery**: alarm on `StatusCheckFailed_System` with `recover` action (same instance ID, private IP, EIP, metadata; not for instance store). Many instance types have simplified automatic recovery by default.
- **Health checks**: ALB target group health checks ([ELB](services/elastic-load-balancing.md)), Route 53 health checks (endpoint/calculated/alarm-based), ECS container health checks (`healthCheck` in task definition), EKS liveness/readiness probes.
- **Auto scaling capabilities**: EC2 ASG, RDS storage auto scaling, DynamoDB auto scaling/on-demand, ECS capacity providers + service auto scaling, EKS Cluster Autoscaler/Karpenter ([Auto Scaling](services/ec2-auto-scaling.md), [Chapter 3](03-resilient-cloud.md)).
- **Install agents at scale**: SSM Agent (in AMI / DHMC), CloudWatch agent (State Manager), Inspector (uses SSM Agent), CodeDeploy agent (Distributor).
- **Config rules to remediate** ([AWS Config](services/config.md)).

## 4.4 Domain 4 scenario quick-map

| Scenario | Answer |
|---|---|
| Monitor EC2 memory / disk usage | CloudWatch agent (config in Parameter Store, deploy via SSM) |
| Count ERROR lines and alert | Metric filter -> alarm -> SNS |
| Process logs in real time with custom code | Subscription filter -> Kinesis Data Streams or Lambda |
| Deliver logs to S3 / OpenSearch / Splunk continuously, no code | Subscription filter -> Firehose |
| Centralise logs from 50 accounts | Cross-account subscription to a destination (Kinesis/Firehose) in Log Archive account, or Logs centralization, or org trail for API logs |
| Ad-hoc query on log groups | Logs Insights |
| SQL over logs in S3 | Athena |
| Send all metrics to Datadog/S3 in near real time | CloudWatch metric streams (Firehose) |
| Threshold hard to define, seasonal traffic | Anomaly detection alarm |
| Reduce alert noise | Composite alarm |
| Alarm on error rate % | Metric math expression alarm |
| Sub-minute metrics | High-resolution custom metrics (1 s) |
| Trace latency across Lambda/API GW/DynamoDB | X-Ray active tracing (Lambda) + stage tracing (API GW) |
| Filter traces by customer ID | X-Ray annotations |
| Traces from ECS tasks | X-Ray daemon / ADOT sidecar |
| Know site is down before users | CloudWatch Synthetics canary |
| Prove CloudTrail logs not modified | Log file integrity validation |
| Detect unusual API volume | CloudTrail Insights |
| Who downloaded object X from S3 | CloudTrail S3 data events |
| SQL over API history, no infra | CloudTrail Lake |
| Why is traffic to instance rejected | VPC Flow Logs (REJECT) |
| Log retention cost growing | Set log group retention, archive to S3 with lifecycle |
| Encrypt CloudWatch Logs with own key | Associate KMS CMK with log group (key policy for logs service principal) |
| Auto-recover EC2 on hardware failure | Alarm on StatusCheckFailed_System with recover action |

---

[← 3. Domain 3: Resilient Cloud Solutions (15%)](03-resilient-cloud.md) | [🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [5. Domain 5: Incident and Event Response (14%) →](05-incident-event-response.md)
