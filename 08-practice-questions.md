[← 7. "Which one?" comparisons + numbers](07-service-comparisons-numbers.md) | [🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [9. 46-day study plan + exam-day checklist →](09-study-plan.md)

# Chapter 8 - Practice Questions (exam style, with explanations)

> 61 original questions written in the DOP-C02 style. Try each one before opening the answer. Track wrong answers by domain and re-read that chapter's quick-map.
> These are for practice; they are not real exam questions.

---

## Domain 1 - SDLC Automation

**Q1.** A team deploys a Lambda function with AWS SAM. They want 10% of traffic to go to the new version for 10 minutes, and an automatic rollback if the function's error alarm fires. Which approach has the LEAST operational overhead?

A. Create two aliases and update weights with a scheduled Lambda function.
B. Set `AutoPublishAlias` and `DeploymentPreference` with `Type: Canary10Percent10Minutes` and the alarm in `Alarms`.
C. Use API Gateway canary release on the stage pointing to the new version.
D. Use CodePipeline with a manual approval after deploying to 10% of traffic.

<details><summary>Answer</summary>

**B.** SAM creates the CodeDeploy application and deployment group, shifts alias traffic in canary mode and rolls back on alarm. A needs custom code. C shifts API traffic, not alias traffic, and has no alarm rollback. D is manual.
</details>

---

**Q2.** A CodeDeploy in-place deployment to EC2 fails at the `ApplicationStop` lifecycle event on every instance. The previous deployment had a bug in `stop.sh`. The new revision has a fixed script. What should the engineer do?

A. Fix the script in the new revision and redeploy normally.
B. Redeploy with the option to ignore ApplicationStop failures.
C. Change the deployment configuration to OneAtATime.
D. Reinstall the CodeDeploy agent on each instance.

<details><summary>Answer</summary>

**B.** ApplicationStop runs the script from the **last successfully deployed revision**, which is still broken, so fixing the new revision alone doesn't help (A). Ignoring ApplicationStop failures lets the new revision install. C and D don't address the cause.
</details>

---

**Q3.** A company has a CodePipeline in a tools account that must deploy CloudFormation stacks into a production account. The pipeline fails with an access denied error when the production account tries to read artifacts. The artifact bucket uses the default `aws/s3` key. What must be changed? (Choose TWO.)

A. Use a customer managed KMS key for the artifact bucket and grant the production account role decrypt access in the key policy.
B. Make the artifact bucket public with a bucket policy condition on the production account ID.
C. Add a bucket policy that allows the production account's cross-account role to get objects.
D. Enable S3 Cross-Region Replication to the production account.
E. Create an IAM user in the tools account for the production account to use.

<details><summary>Answer</summary>

**A and C.** AWS managed keys can't be used cross-account, so a CMK with a key policy grant is required, plus bucket access for the role. B is insecure, D is unnecessary, E uses long-term credentials.
</details>

---

**Q4.** A team builds Docker images in CodeBuild. Builds fail with "Cannot connect to the Docker daemon". What is the fix?

A. Add the `docker` runtime to `runtime-versions`.
B. Enable privileged mode in the CodeBuild project environment.
C. Attach `AmazonEC2ContainerRegistryFullAccess` to the service role.
D. Run the build in a VPC.

<details><summary>Answer</summary>

**B.** Running the Docker daemon in CodeBuild requires privileged mode. C fixes push permissions, not the daemon.
</details>

---

**Q5.** A CodeBuild project was moved into a VPC to reach a private RDS database for integration tests. Now the `npm install` step times out. The project uses public subnets. What should the engineer do?

A. Assign Elastic IPs to the CodeBuild build containers.
B. Move the project to private subnets that route to a NAT gateway.
C. Add an internet gateway to the VPC.
D. Increase the build timeout.

<details><summary>Answer</summary>

**B.** CodeBuild in a VPC does not get public IPs, even in public subnets. It needs private subnets with a NAT gateway (or VPC endpoints / CodeArtifact via endpoints).
</details>

---

**Q6.** An ECS service on Fargate uses rolling updates. Sometimes a bad image is deployed, and tasks keep failing health checks. The team wants ECS to automatically roll back to the last working version with minimal effort. What should they do?

A. Migrate to CodeDeploy blue/green.
B. Enable the deployment circuit breaker with rollback on the service.
C. Create an EventBridge rule on task stopped events that calls UpdateService with the previous task definition.
D. Set `minimumHealthyPercent` to 100.

<details><summary>Answer</summary>

**B.** The circuit breaker detects deployments that can't reach steady state and rolls back. A works but is more effort. C is custom code. D doesn't roll back.
</details>

---

**Q7.** A company wants to validate a new ECS task version with test traffic on port 8080 before shifting production traffic, and to shift production traffic 10% at a time every minute. Which solution meets these requirements?

A. ECS rolling update with `maximumPercent` 200.
B. CodeDeploy ECS blue/green with a test listener, an `AfterAllowTestTraffic` hook, and `CodeDeployDefault.ECSLinear10PercentEvery1Minutes`.
C. Two ECS services behind Route 53 weighted records.
D. Elastic Beanstalk traffic splitting.

<details><summary>Answer</summary>

**B.** Only CodeDeploy ECS blue/green offers a test listener, lifecycle hooks for tests and linear shifting.
</details>

---

**Q8.** An Elastic Beanstalk application must be updated without reducing capacity, and rollback must be as fast and safe as possible if new instances fail health checks. Data is in an external RDS database. Which deployment policy should be used?

A. Rolling
B. Rolling with additional batch
C. Immutable
D. All at once

<details><summary>Answer</summary>

**C.** Immutable launches new instances in a temporary ASG. If they fail, only the new instances are terminated. B keeps capacity but rollback means redeploying.
</details>

---

**Q9.** A company stores Python packages from PyPI and internal packages. Builds must not reach the public internet, and the security team wants to block a public package name that collides with an internal package name. What should they use?

A. An S3 bucket as a PyPI mirror.
B. CodeArtifact with an upstream repository that has an external connection to PyPI, package origin controls, and CodeArtifact VPC endpoints.
C. ECR pull-through cache.
D. A self-hosted PyPI server on EC2 behind an NLB.

<details><summary>Answer</summary>

**B.** CodeArtifact proxies PyPI, origin controls prevent dependency confusion, and VPC endpoints keep builds private. C is for container images.
</details>

---

**Q10.** A security team requires that new container images with CRITICAL vulnerabilities never reach production. Images are pushed to ECR by CodeBuild. What is the MOST automated approach?

A. Run a weekly manual review of ECR basic scan results.
B. Enable ECR enhanced scanning (Inspector). In the pipeline, add a step after push that checks the image's findings and fails the pipeline if CRITICAL findings exist.
C. Enable tag immutability.
D. Use ECR lifecycle policies to delete vulnerable images.

<details><summary>Answer</summary>

**B.** Inspector scans the image and the pipeline gates on findings. C and D don't evaluate vulnerabilities.
</details>

---

**Q11.** A CodePipeline V2 pipeline should run only when files under `infra/` change on the `main` branch of a GitHub repository connected through CodeConnections. What should be configured?

A. An EventBridge rule with a path filter.
B. A pipeline trigger with a push filter on branch `main` and file path `infra/**`.
C. A Lambda function that inspects every commit and starts the pipeline.
D. A CodeBuild webhook.

<details><summary>Answer</summary>

**B.** V2 pipeline triggers support branch, tag and file path filters natively.
</details>

---

**Q12.** A company runs 800 EC2 instances across several ASGs. The CodeDeploy agent must be installed on all current and future instances and kept up to date. Which approach has the LEAST overhead?

A. Add install commands to each launch template's user data.
B. Create an SSM State Manager association that runs `AWS-ConfigureAWSPackage` for `AWSCodeDeployAgent` on a schedule, targeting instances by tag.
C. Bake the agent into the AMI monthly.
D. Use a Lambda function to SSH into each new instance.

<details><summary>Answer</summary>

**B.** State Manager applies to new instances automatically and keeps the agent updated. A and C don't keep it updated without more work.
</details>

---

## Domain 2 - Configuration Management and IaC

**Q13.** A company needs an IAM role and an AWS Config rule in every account of its organization, including accounts that will be created later, with the least effort. What should they use?

A. StackSets with self-managed permissions.
B. StackSets with service-managed permissions targeting the root/OUs with automatic deployment enabled.
C. A pipeline that loops over accounts and runs `create-stack`.
D. Control Tower Account Factory only.

<details><summary>Answer</summary>

**B.** Service-managed StackSets with automatic deployment add stack instances to new accounts in target OUs automatically.
</details>

---

**Q14.** A CloudFormation stack contains a production RDS instance. An engineer must make sure no stack update can replace or delete the database, while other resources can still be updated. What should they do?

A. Enable termination protection on the stack.
B. Apply a stack policy that denies `Update:Replace` and `Update:Delete` on the database's logical ID and allows everything else.
C. Set `DeletionPolicy: Retain` on the database.
D. Use an SCP denying `rds:DeleteDBInstance`.

<details><summary>Answer</summary>

**B.** Stack policies protect resources during stack updates. A only blocks deleting the whole stack. C only applies when the resource is deleted from the stack, not to replacement. (Adding `UpdateReplacePolicy: Snapshot` is also good practice.)
</details>

---

**Q15.** EC2 instances in a CloudFormation stack install software with `cfn-init`. Sometimes the stack reports CREATE_COMPLETE before the software is ready, and sometimes installation fails silently. What should the engineer add?

A. A `DependsOn` attribute on the instance.
B. A `CreationPolicy` with a ResourceSignal and a `cfn-signal` call after `cfn-init` in user data.
C. A `WaitConditionHandle` with no signal.
D. A custom resource that sleeps for 10 minutes.

<details><summary>Answer</summary>

**B.** `cfn-signal -e $?` reports the cfn-init exit code to the CreationPolicy, so the stack waits and fails if installation fails.
</details>

---

**Q16.** After updating `AWS::CloudFormation::Init` metadata in a template and updating the stack, the running instances don't pick up the new configuration. What is missing?

A. `cfn-hup` configured to watch the resource metadata and re-run `cfn-init`.
B. A new AMI.
C. A stack policy.
D. Drift detection.

<details><summary>Answer</summary>

**A.** cfn-hup polls for metadata changes and runs hook actions.
</details>

---

**Q17.** A stack update failed and the stack is now in `UPDATE_ROLLBACK_FAILED` because someone manually deleted a security group the stack manages. How can the engineer return the stack to a working state?

A. Delete and recreate the stack.
B. Use ContinueUpdateRollback and skip the deleted resource.
C. Run drift detection.
D. Update the stack again.

<details><summary>Answer</summary>

**B.** You can't update a stack in UPDATE_ROLLBACK_FAILED. ContinueUpdateRollback with `--resources-to-skip` completes the rollback.
</details>

---

**Q18.** Developers need to launch preapproved EC2 and RDS configurations. They must not have IAM permissions to create these resources directly. What is the BEST solution?

A. Give developers PowerUserAccess with an SCP.
B. Create Service Catalog products in a portfolio, use a launch constraint with an IAM role that can create the resources, and grant developers access to the portfolio.
C. Share CloudFormation templates in S3.
D. Use permissions boundaries.

<details><summary>Answer</summary>

**B.** The launch constraint role provisions resources, so end users only need Service Catalog permissions.
</details>

---

**Q19.** A company must patch 3,000 instances across 25 accounts and 4 Regions every second Sunday, and see compliance centrally. What has the LEAST overhead?

A. Cron jobs on each instance running `yum update`.
B. A Systems Manager Quick Setup patch policy for the organization, with patch baselines and a schedule.
C. A Lambda function in each account calling Run Command.
D. Rebuild all AMIs monthly.

<details><summary>Answer</summary>

**B.** Quick Setup patch policies configure Patch Manager across the organization and Regions with central compliance reporting.
</details>

---

**Q20.** An operations team needs to make sure the CloudWatch agent is installed and configured with the same configuration on every EC2 instance, including new instances, and that the configuration is re-applied if someone changes it. What should they do?

A. Run Command once.
B. Store the agent config in Parameter Store and create State Manager associations to install the agent and apply the configuration on a schedule, targeting by tag.
C. Put the config in user data.
D. Use AWS Config to detect missing agents.

<details><summary>Answer</summary>

**B.** State Manager keeps the desired state and targets new instances automatically.
</details>

---

**Q21.** An organization wants to prevent any member account from leaving the organization or disabling GuardDuty, including account administrators. What should they use?

A. IAM policies in each account.
B. An SCP that denies `organizations:LeaveOrganization` and GuardDuty delete/disable actions, attached to the root.
C. AWS Config rules.
D. Permissions boundaries on all roles.

<details><summary>Answer</summary>

**B.** SCPs restrict all principals in member accounts, including admins and the root user. Config only detects.
</details>

---

**Q22.** A company wants to block creation of any S3 bucket without default encryption and versioning **before** the resource is created through CloudFormation across governed accounts. Which option fits best?

A. AWS Config detective rule.
B. Control Tower proactive control (CloudFormation Hook).
C. Security Hub standard.
D. GuardDuty S3 protection.

<details><summary>Answer</summary>

**B.** Proactive controls run as CloudFormation Hooks and fail non-compliant resource operations before provisioning. The others only detect after creation.
</details>

---

**Q23.** A company wants to change application behaviour (enable a new checkout flow) for 20% of users at a time, validate the configuration against a JSON schema, and roll back automatically if errors increase. Which service should they use?

A. Parameter Store with a Lambda that updates values.
B. AWS AppConfig feature flag with a validator, a linear deployment strategy and a CloudWatch alarm.
C. CodeDeploy canary.
D. Environment variables in ECS.

<details><summary>Answer</summary>

**B.** AppConfig provides validators, gradual deployment strategies and alarm-based rollback.
</details>

---

**Q24.** A nightly process must: snapshot a database, start a CodeBuild job that runs for 90 minutes, wait for it, then notify on failure. Which solution is MOST reliable with least custom code?

A. A single Lambda function.
B. EventBridge Scheduler starting a Step Functions Standard workflow that uses SDK integrations (with `.sync` for CodeBuild) and a Catch that publishes to SNS.
C. Cron on an EC2 instance.
D. CodePipeline with a scheduled trigger.

<details><summary>Answer</summary>

**B.** Lambda's max is 15 minutes. Step Functions waits for CodeBuild with `.sync` and handles errors natively.
</details>

---

## Domain 3 - Resilient Cloud Solutions

**Q25.** A financial application uses Aurora MySQL in us-east-1. Requirements: RPO of 1 second and RTO of 1 minute for a Regional failure. What should they do?

A. Cross-Region snapshot copy every hour.
B. Aurora Global Database with a secondary cluster in another Region.
C. RDS Multi-AZ.
D. AWS Backup cross-Region copy.

<details><summary>Answer</summary>

**B.** Global Database replicates with typically under 1 s lag and can fail over in about a minute. C protects against AZ failure only.
</details>

---

**Q26.** A company needs DR for a web app with RTO 4 hours and RPO 1 hour at the lowest cost. The app runs on EC2 with RDS PostgreSQL. What should they choose?

A. Multi-site active-active.
B. Warm standby.
C. Backup and restore: AWS Backup hourly backups copied cross-Region, AMIs copied, CloudFormation template to rebuild.
D. Pilot light with Aurora Global Database.

<details><summary>Answer</summary>

**C.** Hourly backups meet the 1 h RPO. A rebuild from templates fits within 4 h. It's the cheapest option.
</details>

---

**Q27.** ALB targets in an ASG sometimes return HTTP 500 due to a hung application while the EC2 status checks still pass. The ASG doesn't replace them. What should be changed?

A. Increase the ALB idle timeout.
B. Change the ASG health check type to ELB.
C. Enable detailed monitoring.
D. Add a lifecycle hook.

<details><summary>Answer</summary>

**B.** With ELB health checks, the ASG replaces instances that fail the target group health check.
</details>

---

**Q28.** An ASG for an application that takes 12 minutes to initialise can't keep up with sudden morning spikes. Spikes happen every weekday around 9 AM. Which TWO actions help most?

A. Configure a warm pool.
B. Enable predictive scaling (or scheduled scaling for 8:45 AM).
C. Lower the target tracking target to 10% CPU.
D. Use simple scaling with a 1-hour cooldown.
E. Disable health checks.

<details><summary>Answer</summary>

**A and B.** Warm pools cut launch time. Predictive or scheduled scaling adds capacity before the known spike.
</details>

---

**Q29.** Instances in an ASG write important logs locally. When scale-in terminates an instance, the logs are lost. What is the BEST fix?

A. Disable scale-in.
B. Add a termination lifecycle hook. An EventBridge rule runs an SSM Run Command that uploads logs to S3, then completes the lifecycle action.
C. Use instance store volumes.
D. Take EBS snapshots hourly.

<details><summary>Answer</summary>

**B.** The lifecycle hook pauses termination so logs can be copied. (Streaming logs with the CloudWatch agent is also a good long-term practice.)
</details>

---

**Q30.** A Route 53 failover setup must check the health of an application running only in private subnets. Route 53 health checkers can't reach it. What should be done?

A. Make the application public.
B. Create a CloudWatch alarm on an application metric and a Route 53 health check that monitors the alarm.
C. Use a calculated health check only.
D. Use geolocation routing.

<details><summary>Answer</summary>

**B.** CloudWatch alarm-based health checks support private resources.
</details>

---

**Q31.** A gaming company uses UDP and needs players worldwide to fail over between Regions within seconds. Some clients cache DNS for a long time. What should they use?

A. Route 53 latency routing.
B. AWS Global Accelerator with endpoint groups in two Regions.
C. CloudFront.
D. Route 53 failover with TTL 60.

<details><summary>Answer</summary>

**B.** Global Accelerator uses static anycast IPs and supports UDP. Failover doesn't depend on DNS caching.
</details>

---

**Q32.** An ECS cluster on EC2 has tasks stuck in PENDING when the service scales out, because instances are full. What is the MOST automated fix?

A. Manually raise the ASG desired capacity.
B. Use an ECS capacity provider linked to the ASG with managed scaling enabled.
C. Switch to `binpack` placement.
D. Increase task CPU.

<details><summary>Answer</summary>

**B.** Managed scaling scales the ASG based on task demand (CapacityProviderReservation).
</details>

---

**Q33.** A company wants to verify, before each release, that its application still meets an RTO of 30 minutes and an RPO of 5 minutes, and get recommendations when it doesn't. What service should be used?

A. AWS Trusted Advisor.
B. AWS Resilience Hub with a resiliency policy, run from the pipeline.
C. AWS FIS.
D. AWS Config.

<details><summary>Answer</summary>

**B.** Resilience Hub assesses the app against RTO/RPO policies and recommends fixes. FIS runs experiments but doesn't assess against targets.
</details>

---

**Q34.** Backups must be protected so that nobody, including the root user of the account, can delete them before 1 year. What should be used?

A. S3 versioning.
B. AWS Backup Vault Lock in compliance mode with minimum retention of 365 days.
C. An IAM policy denying `backup:DeleteRecoveryPoint`.
D. An SCP.

<details><summary>Answer</summary>

**B.** Compliance-mode Vault Lock is immutable, and even root can't remove it. IAM policies and SCPs can be changed by admins.
</details>

---

**Q35.** A DynamoDB-backed application must accept writes in two Regions simultaneously with low latency for users in both Regions. What should be used?

A. DynamoDB Streams + Lambda to copy items.
B. DynamoDB global tables.
C. Cross-Region backups.
D. DAX.

<details><summary>Answer</summary>

**B.** Global tables are multi-active and fully managed.
</details>

---

## Domain 4 - Monitoring and Logging

**Q36.** The operations team needs to alarm when memory utilization exceeds 80% on Linux EC2 instances. What must be done first?

A. Enable detailed monitoring.
B. Install and configure the CloudWatch agent to publish memory metrics.
C. Enable VPC Flow Logs.
D. Use the `MemoryUtilization` metric from `AWS/EC2`.

<details><summary>Answer</summary>

**B.** EC2 doesn't publish memory metrics by default. D doesn't exist.
</details>

---

**Q37.** An application writes JSON logs to CloudWatch Logs. The team wants an alarm when the number of events with `"statusCode": 500` exceeds 50 in 5 minutes. What should they do?

A. Logs Insights scheduled query.
B. Metric filter `{ $.statusCode = 500 }` creating a custom metric, then a CloudWatch alarm.
C. Export logs to S3 and query with Athena.
D. Subscription filter to OpenSearch.

<details><summary>Answer</summary>

**B.** Metric filter plus alarm is the native approach.
</details>

---

**Q38.** Logs from 40 accounts must be delivered in near real time to a central Log Archive account and stored in S3 with no custom code. What should they use?

A. CreateExportTask in each account every hour.
B. Subscription filters in each account sending to a CloudWatch Logs destination in the central account backed by Data Firehose writing to S3.
C. Cross-account IAM roles and a Lambda that reads logs.
D. CloudTrail organization trail.

<details><summary>Answer</summary>

**B.** Cross-account log destinations with Firehose deliver continuously. A isn't near real time. D only covers API events.
</details>

---

**Q39.** A team wants all CloudWatch metrics from an account delivered continuously to a third-party observability platform. What is the MOST efficient approach?

A. Lambda calling GetMetricData every minute.
B. CloudWatch metric streams through Data Firehose to the partner's HTTP endpoint.
C. Export metrics to S3 daily.
D. CloudWatch dashboards shared publicly.

<details><summary>Answer</summary>

**B.** Metric streams are designed for this.
</details>

---

**Q40.** Request volume to an API varies heavily by hour and day of week, so static thresholds cause false alarms. What should be used?

A. Composite alarm.
B. CloudWatch anomaly detection alarm.
C. A higher threshold.
D. Metric math.

<details><summary>Answer</summary>

**B.** Anomaly detection models seasonality.
</details>

---

**Q41.** Developers need to find which downstream call is slow in a request that goes through API Gateway, Lambda and DynamoDB, and filter traces by customer ID. What should they do? (Choose TWO.)

A. Enable X-Ray tracing on the API Gateway stage and active tracing on the Lambda function.
B. Add the customer ID as an X-Ray annotation.
C. Add the customer ID as X-Ray metadata.
D. Enable VPC Flow Logs.
E. Enable CloudTrail data events.

<details><summary>Answer</summary>

**A and B.** Annotations are indexed and searchable. Metadata (C) isn't.
</details>

---

**Q42.** An auditor needs proof that CloudTrail log files in S3 were not modified or deleted after delivery. What should be enabled?

A. S3 versioning.
B. CloudTrail log file integrity validation.
C. SSE-KMS.
D. CloudTrail Insights.

<details><summary>Answer</summary>

**B.** Digest files allow validation of log integrity.
</details>

---

**Q43.** The security team wants to know who downloaded a specific object from a sensitive S3 bucket. What must be configured?

A. CloudTrail management events.
B. CloudTrail data events for the S3 bucket.
C. VPC Flow Logs.
D. AWS Config.

<details><summary>Answer</summary>

**B.** Object-level API calls such as GetObject are data events, which aren't logged by default.
</details>

---

**Q44.** A company's CloudWatch Logs costs keep growing because log groups never expire. Policy says 30-day retention in CloudWatch and 7 years in archive. What is the BEST solution?

A. Delete log groups monthly.
B. Set 30-day retention on log groups (enforced with a Config rule and remediation), stream logs with Firehose to S3, and use S3 lifecycle rules to move them to Glacier Deep Archive and expire after 7 years.
C. Export to S3 manually.
D. Use Logs Insights to compress logs.

<details><summary>Answer</summary>

**B.** This automates retention and long-term low-cost archival.
</details>

---

**Q45.** A team wants to know a public website's checkout flow is broken before customers report it. What should they use?

A. RUM.
B. CloudWatch Synthetics canary scripting the checkout flow, with an alarm on SuccessPercent.
C. ALB access logs.
D. X-Ray.

<details><summary>Answer</summary>

**B.** Canaries test the flow proactively on a schedule.
</details>

---

## Domain 5 - Incident and Event Response

**Q46.** AWS Health sends scheduled retirement events for EC2 instances. The team wants instances to be stopped and started automatically during a maintenance window. What should they do?

A. Poll the Health API every hour from EC2.
B. Create an EventBridge rule for AWS Health EC2 scheduled change events that targets an SSM Automation runbook (or a Lambda function) to stop and start the instance.
C. Enable EC2 auto recovery.
D. Use Trusted Advisor.

<details><summary>Answer</summary>

**B.** This is the event-driven native pattern. (Combine with a Maintenance Window or Change Calendar for timing.)
</details>

---

**Q47.** An EventBridge rule in eu-west-1 is supposed to catch IAM `CreateUser` API calls, but it never fires. What is the cause?

A. IAM events are not supported by EventBridge.
B. IAM is a global service, and its CloudTrail events are delivered to us-east-1. The rule must be in us-east-1.
C. The rule needs a schedule expression.
D. CloudTrail Insights must be enabled.

<details><summary>Answer</summary>

**B.**
</details>

---

**Q48.** Order events must be processed by three independent systems (billing, shipping, analytics). Each must retry independently and not affect the others. What design should be used?

A. One SQS queue with three consumers.
B. SNS topic with three SQS queue subscriptions (fan-out), each with its own DLQ.
C. Kinesis with one consumer.
D. Lambda calling the three systems sequentially.

<details><summary>Answer</summary>

**B.** Fan-out gives each system its own queue and retry behaviour. In A, each message is consumed by only one consumer.
</details>

---

**Q49.** A Lambda function consumes a Kinesis stream. A malformed record causes the function to fail repeatedly, and processing of the shard stalls. What should be configured? (Choose TWO.)

A. Bisect batch on function error.
B. Maximum retry attempts and an on-failure destination (SQS).
C. Increase the stream retention period.
D. Increase Lambda memory.
E. Enable enhanced fan-out.

<details><summary>Answer</summary>

**A and B.** Bisecting isolates the bad record. Limited retries plus an on-failure destination move it aside so the shard continues.
</details>

---

**Q50.** GuardDuty reports `CryptoCurrency:EC2/BitcoinTool.B!DNS` for an instance. The company wants automatic isolation and evidence preservation. What should be implemented?

A. Terminate the instance manually.
B. EventBridge rule on that GuardDuty finding type triggering Step Functions/Lambda: replace the instance's security groups with an isolation SG, create EBS snapshots, tag the instance and notify the security team.
C. Enable Inspector.
D. Create a NACL to block all traffic in the VPC.

<details><summary>Answer</summary>

**B.** This isolates the instance while keeping evidence. Terminating destroys evidence. D affects all workloads in the VPC.
</details>

---

**Q51.** An ECS Fargate task in a private subnet without a NAT gateway stops with `CannotPullContainerError`. Which TWO actions fix it with no internet access?

A. Create interface VPC endpoints for `ecr.api` and `ecr.dkr`, and a gateway endpoint for S3.
B. Ensure the task execution role has ECR pull permissions.
C. Add a public IP to the task.
D. Give the task role `AmazonS3FullAccess`.
E. Increase task memory.

<details><summary>Answer</summary>

**A and B.** Image layers come from S3, so the S3 gateway endpoint is needed too. The execution role (not the task role) pulls images. If logs go to CloudWatch, a `logs` endpoint is also needed.
</details>

---

**Q52.** A CloudFormation stack creation fails with many `CREATE_FAILED` events. How should the engineer find the root cause fastest?

A. Read the last event.
B. Find the first `CREATE_FAILED` event in chronological order (or use the console's root cause detection).
C. Run drift detection.
D. Check CloudTrail for `CreateStack`.

<details><summary>Answer</summary>

**B.** Later failures are usually "Resource creation cancelled" cascades.
</details>

---

**Q53.** An ASG keeps launching instances that are terminated a few minutes later as unhealthy. The application needs 5 minutes to start. What should be changed?

A. Increase the health check grace period beyond the startup time.
B. Change health check type to EC2.
C. Increase max capacity.
D. Use Spot instances.

<details><summary>Answer</summary>

**A.** The grace period stops the ASG from replacing instances that are still booting. B would hide real failures.
</details>

---

**Q54.** An operations team wants a single place where operational issues from CloudWatch alarms, Config non-compliance and EventBridge events are aggregated, with related resources and runbooks to resolve them. What should they use?

A. Security Hub.
B. Systems Manager OpsCenter.
C. Trusted Advisor.
D. CloudWatch dashboards.

<details><summary>Answer</summary>

**B.** OpsItems aggregate operational work with associated runbooks.
</details>

---

## Domain 6 - Security and Compliance

**Q55.** A company's developers deploy from GitHub Actions to AWS using IAM user access keys stored as GitHub secrets. Security wants to remove long-term credentials. What should be done?

A. Rotate the keys monthly with Secrets Manager.
B. Create an IAM OIDC identity provider for GitHub and a role whose trust policy restricts `token.actions.githubusercontent.com:sub` to the repository and branch. Workflows assume it with `AssumeRoleWithWebIdentity`.
C. Use IAM Identity Center users.
D. Store keys in Parameter Store.

<details><summary>Answer</summary>

**B.** OIDC federation gives short-lived credentials without stored keys.
</details>

---

**Q56.** Team leads must be able to create IAM roles for their applications, but must not be able to create roles with more permissions than a defined maximum. What should be implemented?

A. SCP.
B. Permissions boundary policy. Leads may only create roles if the `iam:PermissionsBoundary` condition equals that boundary, and can't modify or remove the boundary.
C. Access Analyzer.
D. Service Catalog.

<details><summary>Answer</summary>

**B.** This is the delegation pattern for permissions boundaries.
</details>

---

**Q57.** A company has 300 projects and wants engineers to manage only EC2 instances belonging to their project, without writing a policy per project. What should be used?

A. One IAM group per project.
B. ABAC: tag resources and principals with `Project`, and use a policy condition `aws:ResourceTag/Project` equal to `${aws:PrincipalTag/Project}`.
C. One account per project.
D. Resource-based policies on EC2.

<details><summary>Answer</summary>

**B.** ABAC scales without new policies. EC2 doesn't support resource-based policies (D).
</details>

---

**Q58.** An RDS PostgreSQL master password must rotate every 30 days automatically, and applications must always get the current value. What should be used?

A. Parameter Store SecureString with a Lambda.
B. Secrets Manager with managed rotation (or RDS `ManageMasterUserPassword`), with applications retrieving the secret at runtime.
C. An environment variable updated by a pipeline.
D. KMS automatic key rotation.

<details><summary>Answer</summary>

**B.** KMS rotation (D) rotates encryption keys, not passwords.
</details>

---

**Q59.** A company wants to share an encrypted AMI with another account. The EBS snapshots are encrypted with the AWS managed key `aws/ebs`. The other account can't launch the AMI. What should be done?

A. Make the AMI public.
B. Copy the AMI and re-encrypt it with a customer managed KMS key, grant the target account use of the key in the key policy, and share the new AMI.
C. Share the `aws/ebs` key.
D. Disable encryption.

<details><summary>Answer</summary>

**B.** AWS managed keys can't be shared across accounts.
</details>

---

**Q60.** A security team wants a single view of security findings from GuardDuty, Inspector and Macie across all accounts and Regions, plus automated checks against the CIS AWS Foundations Benchmark. Which approach has the LEAST overhead?

A. Collect findings with Lambda into DynamoDB.
B. Enable Security Hub with a delegated administrator, auto-enable for member accounts, enable the CIS standard, and configure cross-Region aggregation.
C. Use Amazon Detective.
D. Use CloudTrail Lake.

<details><summary>Answer</summary>

**B.** Detective is for investigation, not aggregation or standards.
</details>

---

**Q61.** A company moved its build agents (EC2 in an ASG) to private subnets with no NAT gateway, to meet a "no internet access" rule. At launch, user data must download a 200 MB toolchain archive that used to come from a vendor website. Which solution meets the rule with the LEAST operational overhead?

A. Add a NAT gateway and allow only the vendor's IP range in a network ACL.
B. Store the archive in an S3 bucket, add an S3 gateway VPC endpoint to the private route tables, and give the instance profile `s3:GetObject` on that object. User data downloads it with the AWS CLI.
C. Run a proxy server on EC2 in a public subnet that downloads the archive for the build agents.
D. Attach Elastic IPs during launch and remove them after the download.

<details><summary>Answer</summary>

**B.** A gateway endpoint keeps S3 traffic on the AWS network without internet access, and it costs nothing extra. A and D still give the instances internet access. C adds a server to manage. You can also add an endpoint policy, or a bucket policy with `aws:SourceVpce`, so the bucket is reachable only through that endpoint.
</details>

---

## Scoring guide
- 55+ correct (90%): you are ready. Focus on full timed mocks.
- 46-54 (75-89%): re-read the quick-maps for the domains where you missed questions.
- Below 46: re-study those chapters fully, then retest in 3 days.

Track it like this:

| Domain | Questions | My wrong answers |
|---|---|---|
| 1 SDLC | Q1-Q12 | |
| 2 Config/IaC | Q13-Q24 | |
| 3 Resilience | Q25-Q35 | |
| 4 Monitoring | Q36-Q45 | |
| 5 Incident | Q46-Q54 | |
| 6 Security | Q55-Q61 | |

---

[← 7. "Which one?" comparisons + numbers](07-service-comparisons-numbers.md) | [🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [9. 46-day study plan + exam-day checklist →](09-study-plan.md)
