[← Amazon API Gateway](api-gateway.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon EC2 Auto Scaling →](ec2-auto-scaling.md)

# AWS Step Functions and Lambda automation

**Exam domains:** [Domain 2](../02-config-mgmt-iac.md), [Domain 5](../05-incident-event-response.md) | **Hands-on:** none (read-only topic)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

- **Lambda** for event-driven automation: triggered by EventBridge (schedules, AWS events), S3, SNS, SQS, Config custom rules, CloudWatch alarms (direct action), CFN custom resources. Use **SDK (boto3)** with IAM execution role.
- **Step Functions** when the automation has **multiple steps, waits, retries, branching, parallel work, human approval, or runs longer than 15 minutes** (Lambda max timeout = 15 min).
  - **Standard** workflows: up to 1 year, exactly-once, audit history. **Express**: up to 5 minutes, at-least-once, high volume, cheap.
  - States: Task, Choice, Parallel, Map (distributed map for millions of S3 objects), Wait, Pass, Succeed, Fail.
  - **Retry** (ErrorEquals, IntervalSeconds, MaxAttempts, BackoffRate) and **Catch** (fallback state) per state.
  - **SDK integrations** for 200+ services (call any API directly without Lambda), `.sync` (wait for job like CodeBuild/ECS task/Glue to finish), `.waitForTaskToken` (callback pattern, e.g., human approval via email).
- **SSM Automation** when the steps are operational actions on AWS resources (prefer it for remediation, it has built-in runbooks).
- **EventBridge Scheduler** for one-time or recurring scheduled invocations (replaces cron EC2).

**Scenario:** "Nightly process: snapshot DB, run a CodeBuild job, wait for it, if fails notify, takes 2 hours" -> EventBridge Scheduler -> Step Functions Standard with `.sync` integrations + Catch -> SNS.

---

---

[← Amazon API Gateway](api-gateway.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon EC2 Auto Scaling →](ec2-auto-scaling.md)
