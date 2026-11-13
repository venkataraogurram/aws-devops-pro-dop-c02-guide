[🏠 Home](../README.md) | [Services index](../services/README.md)

# Hands-on Labs

Step-by-step practical guides. Each lab has a CloudFormation/SAM template or CLI commands, the output you should expect, a **"break it"** step that recreates a real exam scenario, the exam takeaways, and cleanup.

> These guides were written and lint-checked but **not run end to end** in an AWS account. If a step behaves differently, the "what to check" notes in each lab and the service docs are the source of truth. Tell me what you saw and I'll fix the guide.

## Before you start (once)
1. Use a **sandbox account**, never production. Sign in with admin rights in that account.
2. Install **AWS CLI v2** and check: `aws sts get-caller-identity`.
3. For labs 03 and 10, install **AWS SAM CLI** (`brew install aws-sam-cli`).
4. Set a Region for the session (all labs use it unless they say otherwise):
   ```bash
   export AWS_REGION=us-east-1
   export AWS_DEFAULT_REGION=us-east-1
   export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
   ```
5. Labs that create EC2/ECS use your **default VPC** and its public subnets:
   ```bash
   export VPC_ID=$(aws ec2 describe-vpcs --filters Name=is-default,Values=true --query 'Vpcs[0].VpcId' --output text)
   export SUBNETS=$(aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC_ID Name=default-for-az,Values=true --query 'Subnets[0:2].SubnetId' --output text | tr '\t' ',')
   echo $VPC_ID $SUBNETS
   ```
6. Have an email address ready for SNS notifications, and **click "Confirm subscription"** in the mail AWS sends.

## Cost and safety rules
- Every lab lists an estimated cost. Most cost less than USD 0.50 if you clean up the same day.
- **Always run the Cleanup section.** Check *Billing > Bills* the next day.
- No lab opens SSH/RDP ports or creates public unauthenticated endpoints. Instances are reached with **Systems Manager** (Session Manager / Run Command).

## Lab list

| Lab | Topic | Exam domains | Time | Est. cost |
|---|---|---|---|---|
| [01](01-codebuild-codepipeline/README.md) | CodeCommit + CodeBuild + CodePipeline V2: tests, reports, Parameter Store, approval, failure alerts | 1, 5 | 1.5 h | < $0.10 |
| [02](02-codedeploy-ec2-rollback/README.md) | CodeDeploy on an Auto Scaling group: hooks, auto rollback, the ApplicationStop trap | 1, 5 | 2 h | ~$0.10 |
| [03](03-sam-lambda-canary/README.md) | SAM Lambda canary deployment with pre-traffic hook and alarm rollback | 1, 2 | 1 h | < $0.05 |
| [04](04-ecs-circuit-breaker/README.md) | ECS Fargate rolling deploy with circuit breaker rollback + ECR lifecycle/scan | 1, 3, 5 | 1 h | ~$0.10 |
| [05](05-cloudformation-signals-changesets-drift/README.md) | CloudFormation: cfn-init, cfn-signal, cfn-hup, change sets, stack policy, drift | 2, 5 | 2 h | ~$0.05 |
| [06](06-stacksets-multi-region/README.md) | StackSets (self-managed) to two Regions: failure, OUTDATED, overrides, drift | 2 | 1 h | ~$0 |
| [07](07-systems-manager-fleet/README.md) | Systems Manager: Session Manager, Run Command rate control, State Manager, CloudWatch agent, Patch scan, Inventory | 2, 4, 5 | 2 h | ~$0.10 |
| [08](08-config-auto-remediation/README.md) | AWS Config rule + automatic SSM remediation of an open SSH security group | 2, 5, 6 | 1 h | < $0.10 |
| [09](09-cloudwatch-logs-alarms/README.md) | CloudWatch Logs: metric filter, alarm, Logs Insights, subscription filter to Lambda | 4 | 1 h | < $0.05 |
| [10](10-xray-api-gateway-lambda/README.md) | X-Ray tracing for API Gateway + Lambda + DynamoDB, annotations | 4 | 1 h | < $0.05 |
| [11](11-eventbridge-sqs-dlq/README.md) | EventBridge custom bus, content filtering, SQS + DLQ, partial batch failures, redrive, archive/replay | 5 | 1 h | < $0.05 |
| [12](12-auto-scaling-lifecycle-hooks/README.md) | Auto Scaling: ELB health checks, termination lifecycle hook saves logs, instance refresh | 3, 4, 5 | 2 h | ~$0.20 |
| [13](13-iam-boundary-abac/README.md) | IAM permissions boundary delegation, ABAC with tags, Access Analyzer policy validation | 6 | 1 h | $0 |
| [14](14-guardduty-security-response/README.md) | GuardDuty sample findings -> EventBridge -> SNS + responder Lambda; CloudTrail API-call rule | 4, 5, 6 | 1 h | ~$0 (trial) |
| [15](15-organizations-scp/README.md) | Organizations SCPs on a test OU (optional, needs an organization) | 2, 6 | 1 h | $0 |
| [16](16-multi-region-dr/README.md) | Multi-Region DR: S3 CRR, DynamoDB global table, Route 53 failover on a CloudWatch alarm health check | 3 | 1.5 h | < $0.50 |

Shared helper: [`tools/empty-versioned-bucket.sh`](tools/empty-versioned-bucket.sh) empties a versioned bucket before deletion.
