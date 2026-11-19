[🏠 Home](../README.md) | [Services](../services/README.md) | [Labs](../labs/README.md)

# Tutorials Dojo DOP-C02 study path: notes and cross-check

**Source:** [AWS Certified DevOps Engineer Professional Exam Guide Study Path DOP-C02](https://tutorialsdojo.com/aws-certified-devops-engineer-professional-exam-guide-study-path-dop-c01-dop-c02/) (Tutorials Dojo, last updated Feb 12, 2025). Read the original for the full text. This page summarises it in my own words, maps each of its scenarios to where this repo covers it, and flags the points that are outdated or need care.

## What the guide recommends
- **Background:** DOP-C02 builds on the SysOps Administrator and Developer Associate topics. Neither is required, but their basics are assumed.
- **Study materials:** the official exam guide, the free AWS exam readiness course and official sample questions, whitepapers, FAQs and documentation, labs, cheat sheets and practice tests.
- **Know the syntax of:** CloudFormation templates, SAM templates, `buildspec.yml`, `appspec.yml`, IAM policies. Also be comfortable with the AWS CLI/SDK/APIs. In this repo: [CloudFormation](../services/cloudformation.md), [SAM/CDK](../services/sam-cdk.md), [CodeBuild](../services/codebuild.md), [CodeDeploy](../services/codedeploy.md), [IAM](../services/iam-sts-identity-center.md).
- **Whitepapers:** Running Containerized Microservices on AWS; Implementing Microservices on AWS; Infrastructure as Code; Introduction to DevOps; Practicing CI/CD on AWS; Blue/Green Deployments on AWS; Development and Test on AWS; Disaster Recovery of Workloads on AWS; AWS Multi-Region Fundamentals. (Added to the resource list in [Chapter 0](../00-exam-strategy.md).)
- **Services it says come up most:** CloudFormation, Lambda, EventBridge, CloudWatch alarms, CodePipeline, CodeDeploy, CodeBuild, CodeCommit, Config, Systems Manager, ECS, Elastic Beanstalk, CloudTrail, OpsWorks, Trusted Advisor. All have files in [services/](../services/README.md) except OpsWorks, which reached end of life in May 2024 (see [Chapter 0](../00-exam-strategy.md)).
- **Practice:** the free AWS sample questions are easier than the real exam, so add a harder practice bank and do full timed mocks. (This matches weeks 5-6 of the [study plan](../09-study-plan.md).)

## Its scenarios, mapped to this repo
The scenarios below are paraphrased. "✅" = covered and consistent; "➕" = added to this repo after this check; "⚠️" = read the note.

### SDLC automation
| Scenario (paraphrased) | Answer | Where in this repo |
|---|---|---|
| Find hardcoded secrets in CodeCommit code | CodeGuru Reviewer secret detection | ⚠️ [Ch 6](../06-security-compliance.md). Reviewer is in maintenance mode since Nov 7, 2025 (no new repository associations). Still the expected answer in older questions |
| Beanstalk: no downtime + easy rollback | Blue/green: new environment, swap URLs | ✅ [Beanstalk](../services/elastic-beanstalk.md) |
| Lambda: no downtime, quick rollback | New version + move the prod alias | ✅ [Lambda](../services/lambda.md), [Lab 03](../labs/03-sam-lambda-canary/README.md) |
| Lambda: 10% of traffic to the new version first | Weighted alias / CodeDeploy canary | ✅ [Lambda](../services/lambda.md) |
| EC2 behind ALB: safe upgrade with rollback | New ALB + fleet, switch the Route 53 alias, switch back to roll back | ✅ blue/green in [Ch 1](../01-sdlc-automation.md); also CodeDeploy blue/green or ALB weighted target groups |
| OpsWorks safe deployment | Clone stack, switch DNS | ⚠️ OpsWorks is end of life; not studied here |
| Developers: full CodeCommit use, can't delete repositories | `AWSCodeCommitPowerUser` | ➕ [CodeCommit](../services/codecommit.md) |
| Run custom actions before / after the new version gets traffic | CodeDeploy `BeforeAllowTraffic` / `AfterAllowTraffic` | ⚠️ [CodeDeploy](../services/codedeploy.md). For "before installing" on EC2 the hook is `BeforeInstall`; read which moment the question means |
| Run CodeBuild on PR events and report back to the PR | EventBridge rule -> CodeBuild, Lambda updates the PR | ✅ [CodeCommit](../services/codecommit.md), [CodeBuild](../services/codebuild.md) |
| Build an artifact and deploy it automatically | CodeBuild -> S3 artifact -> CodePipeline -> CodeDeploy | ✅ [CodePipeline](../services/codepipeline.md) |
| Artifact bucket requirements | Versioning + encryption | ✅ [CodePipeline](../services/codepipeline.md) |
| Build / deployment results to Slack | EventBridge rule -> SNS or Lambda (or Q Developer in chat apps) | ✅ [EventBridge](../services/eventbridge.md), [Lab 01](../labs/01-codebuild-codepipeline/README.md) |
| Run a pipeline daily | EventBridge schedule targeting the pipeline | ✅ [CodePipeline](../services/codepipeline.md) |
| Lambda 10% for 10 minutes | `CodeDeployDefault.LambdaCanary10Percent10Minutes` | ✅ [CodeDeploy](../services/codedeploy.md) |
| Beanstalk: no downtime and full capacity | Rolling with additional batch (Immutable also keeps capacity) | ✅ [Beanstalk](../services/elastic-beanstalk.md) |
| Beanstalk: don't mix old and new versions on instances | Immutable | ✅ [Beanstalk](../services/elastic-beanstalk.md) |

### Configuration management and IaC
| Scenario (paraphrased) | Answer | Where in this repo |
|---|---|---|
| Share values from one stack with other stacks | Outputs `Export` + `Fn::ImportValue` | ⚠️ [CloudFormation](../services/cloudformation.md). That is **cross-stack** referencing. For **nested** stacks, the parent reads child outputs with `!GetAtt ChildStack.Outputs.Name` and passes values down as parameters |
| Where the Lambda zip goes in a template / inline code | `Code` with `S3Bucket`/`S3Key`, or `ZipFile` | ➕ [CloudFormation](../services/cloudformation.md) |
| Replace an ASG and remove old instances only when the new ones are healthy | `AutoScalingReplacingUpdate` `WillReplace: true` | ✅ [CloudFormation](../services/cloudformation.md) |
| OpsWorks time-based instances | - | ⚠️ OpsWorks end of life. Today: ASG scheduled scaling ([Auto Scaling](../services/ec2-auto-scaling.md)) |
| Inventory on-premises servers without an agent | Application Discovery Service agentless collector | ⚠️ Migration service, not on the DOP-C02 in-scope list; not studied here |
| ECS service + task definition + ALB in CloudFormation | `AWS::ECS::Service`, `AWS::ECS::TaskDefinition`, `AWS::ElasticLoadBalancingV2::*` | ✅ [Lab 04](../labs/04-ecs-circuit-breaker/README.md) template, [Lab 12](../labs/12-auto-scaling-lifecycle-hooks/README.md) |

### Monitoring and logging
| Scenario (paraphrased) | Answer | Where in this repo |
|---|---|---|
| Central config view across accounts and Regions | AWS Config aggregator | ✅ [Config](../services/config.md) |
| Consolidate CloudTrail logs from many accounts | Central bucket with a cross-account bucket policy | ⚠️ [CloudTrail](../services/cloudtrail.md). Still valid, but with AWS Organizations the least-effort answer is an **organization trail** |
| Prove CloudTrail logs weren't tampered with | Log file integrity validation | ✅ [CloudTrail](../services/cloudtrail.md) |
| App logs from EC2 / on-premises | Unified CloudWatch agent | ✅ [CloudWatch](../services/cloudwatch.md), [Lab 07](../labs/07-systems-manager-fleet/README.md) |
| Logs from Fargate tasks | `awslogs` log driver in the task definition | ✅ [ECS](../services/ecs-eks.md), [Lab 04](../labs/04-ecs-circuit-breaker/README.md) |
| Real-time log analysis | Subscription filter to Lambda / OpenSearch / Kinesis | ✅ [CloudWatch](../services/cloudwatch.md), [Lab 09](../labs/09-cloudwatch-logs-alarms/README.md). (The guide says "Elasticsearch"; the service is now **OpenSearch**) |
| Alert before hitting EC2 / ASG limits | Trusted Advisor `ServiceLimitUsage` metric + alarm | ✅ [Security detection](../services/security-detection.md) |
| Compliance dashboard | Config data in S3 + QuickSight | ✅ [Athena and QuickSight](../services/analytics-athena-quicksight.md) |

### Security and compliance
| Scenario (paraphrased) | Answer | Where in this repo |
|---|---|---|
| Track CVEs on EC2 | Amazon Inspector | ✅ [Security detection](../services/security-detection.md). (Today's Inspector scans continuously; the guide's wording describes the older assessment-run model) |
| Keys / passwords in plain text in buildspec | Parameter Store SecureString (or Secrets Manager) | ✅ [CodeBuild](../services/codebuild.md), [Lab 01](../labs/01-codebuild-codepipeline/README.md) |
| PowerUser policy but only one repository | Extra Deny policy for other repositories/branches | ➕ [CodeCommit](../services/codecommit.md) |
| S3: allow only HTTPS | Bucket policy Deny when `aws:SecureTransport` is false | ✅ [Ch 6](../06-security-compliance.md) |
| Cheapest place for a secret | Parameter Store SecureString | ✅ [Secrets](../services/secrets-manager-parameter-store.md) |
| Generate and rotate a password automatically | Secrets Manager with rotation | ✅ [Secrets](../services/secrets-manager-parameter-store.md) |
| Job-function permissions | AWS managed policies (ReadOnlyAccess, PowerUserAccess...) | ✅ [IAM](../services/iam-sts-identity-center.md) (for many accounts: Identity Center permission sets) |
| Patch and create an AMI automatically | SSM Automation runbook (e.g., `AWS-UpdateLinuxAmi`) | ✅ [Image Builder](../services/ec2-image-builder.md) (Image Builder is the newer managed answer) |
| Shell access with every command recorded | Session Manager + session logs to S3/CloudWatch | ✅ [Systems Manager](../services/systems-manager.md), [Lab 07](../labs/07-systems-manager-fleet/README.md) |
| See installed versions and patches across instances | SSM Inventory | ✅ [Lab 07](../labs/07-systems-manager-fleet/README.md) |
| Custom patch baseline on a schedule | Patch Manager + Maintenance Windows | ✅ [Systems Manager](../services/systems-manager.md) |

### Incident and event response
| Scenario (paraphrased) | Answer | Where in this repo |
|---|---|---|
| File Gateway share missing objects that are in S3 | `RefreshCache` (or automated cache refresh) | ✅ [Databases and storage](../services/databases-storage.md) |
| Alert on specific log events | Metric filter + alarm | ✅ [Lab 09](../labs/09-cloudwatch-logs-alarms/README.md) |
| Notify when objects are deleted from a bucket | S3 Event Notifications | ➕ [S3](../services/s3.md) |
| Notify on an RDS Multi-AZ failover | RDS event subscriptions | ➕ [Databases and storage](../services/databases-storage.md) |
| IAM key leaked on public GitHub | Health `AWS_RISK_CREDENTIALS_EXPOSED` -> EventBridge -> Step Functions deletes the key | ✅ [Health](../services/health.md) |
| AWS maintenance events on EC2/RDS to Slack/SNS | Health events -> EventBridge -> Lambda/SNS | ✅ [Health](../services/health.md) |
| Monitor ASG launch/terminate | EventBridge ASG events | ✅ [Auto Scaling](../services/ec2-auto-scaling.md) |
| Who uploaded/deleted objects | CloudTrail S3 data events | ✅ [CloudTrail](../services/cloudtrail.md) |
| Custom action when a stage fails | EventBridge rule on CodePipeline FAILED -> SNS/Lambda | ✅ [Lab 01](../labs/01-codebuild-codepipeline/README.md) |
| Roll back CodeDeploy when healthy instances drop too low | "CloudWatch alarm on a MinimumHealthyHosts metric" | ⚠️ [CodeDeploy](../services/codedeploy.md). There is no CloudWatch metric by that name. **Minimum healthy hosts** is part of the **deployment configuration**: if it can't be met, the deployment fails, and **auto rollback on deployment failure** redeploys the last good revision. Separately, CodeDeploy can roll back when **CloudWatch alarms** you attach to the deployment group go to ALARM. If an option says this, pick the one that combines these mechanisms |
| QA sign-off before production | Manual approval action | ✅ [Lab 01](../labs/01-codebuild-codepipeline/README.md) |
| OpsWorks auto-healing events | - | ⚠️ OpsWorks end of life |

### Resilient cloud solutions
| Scenario (paraphrased) | Answer | Where in this repo |
|---|---|---|
| Stacks in many accounts and Regions | StackSets | ✅ [Lab 06](../labs/06-stacksets-multi-region/README.md) |
| Survive an AZ failure (app + DB) | Multi-AZ app + RDS Multi-AZ | ✅ [Databases and storage](../services/databases-storage.md) |
| Survive a Region outage | Copy of the stack in another Region + cross-Region read replica | ✅ [Ch 3](../03-resilient-cloud.md) |
| Switch traffic when the primary Region fails | Route 53 failover + health check | ✅ [Lab 16](../labs/16-multi-region-dr/README.md) |
| Keep a single legacy instance available | ASG with min = max = 1 | ➕ [Auto Scaling](../services/ec2-auto-scaling.md) |
| Download code before the instance joins the LB | Launch lifecycle hook (`Pending:Wait`) | ✅ [Auto Scaling](../services/ec2-auto-scaling.md) |
| Upload logs before termination | Terminate lifecycle hook (`Terminating:Wait`) | ✅ [Lab 12](../labs/12-auto-scaling-lifecycle-hooks/README.md) |

## Sample question topic
The guide's free sample question is about instances that lost internet access and can't download dependencies at boot. The secure answer is to keep the files in **S3** and reach S3 through a **gateway VPC endpoint** with an instance profile, instead of NAT or public IPs. Practice it with [Q61 in Chapter 8](../08-practice-questions.md), which tests the same idea with a different scenario.
