[🏠 Home](../README.md)

# Services Reference

One file per service: concepts, must-know facts, YAML/JSON samples, traps. This is the main study material. The domain chapters (01-06) say what each exam domain tests, link here, and hold the cross-service "scenario → answer" tables.

**Scope:** every file covers a service from the official DOP-C02 in-scope list or task statements, at the depth the exam asks. Two services not on the list are kept briefly because they show up as answer options: Global Accelerator (in the CloudFront file) and Firewall Manager (in Network security). See [Chapter 0](../00-exam-strategy.md) for the rule.

## Developer tools (CI/CD)

| Service | Exam domains | Hands-on lab |
|---|---|---|
| [AWS CodeCommit (and Git sources)](codecommit.md) | 1 | [01](../labs/01-codebuild-codepipeline/README.md) |
| [AWS CodeBuild](codebuild.md) | 1, 5 | [01](../labs/01-codebuild-codepipeline/README.md) |
| [AWS CodePipeline](codepipeline.md) | 1, 5 | [01](../labs/01-codebuild-codepipeline/README.md) |
| [AWS CodeDeploy](codedeploy.md) | 1, 5 | [02](../labs/02-codedeploy-ec2-rollback/README.md) |
| [AWS CodeArtifact](codeartifact.md) | 1 | - |
| [Amazon ECR](ecr.md) | 1, 6 | [04](../labs/04-ecs-circuit-breaker/README.md) |
| [EC2 Image Builder](ec2-image-builder.md) | 1, 2 | - |

## Compute, containers and serverless

| Service | Exam domains | Hands-on lab |
|---|---|---|
| [AWS Elastic Beanstalk](elastic-beanstalk.md) | 1 | - |
| [Amazon ECS, EKS and Fargate](ecs-eks.md) | 1, 3, 5 | [04](../labs/04-ecs-circuit-breaker/README.md) |
| [AWS Lambda deployments](lambda.md) | 1, 3, 5 | [03](../labs/03-sam-lambda-canary/README.md), [10](../labs/10-xray-api-gateway-lambda/README.md), [11](../labs/11-eventbridge-sqs-dlq/README.md) |
| [Amazon API Gateway](api-gateway.md) | 1, 3 | [10](../labs/10-xray-api-gateway-lambda/README.md) |
| [AWS Step Functions and Lambda automation](step-functions.md) | 2, 5 | - |
| [Amazon EC2 Auto Scaling](ec2-auto-scaling.md) | 3, 4, 5 | [12](../labs/12-auto-scaling-lifecycle-hooks/README.md) |
| [Elastic Load Balancing and compute high availability](elastic-load-balancing.md) | 3, 4 | [12](../labs/12-auto-scaling-lifecycle-hooks/README.md) |

## Infrastructure as code and configuration

| Service | Exam domains | Hands-on lab |
|---|---|---|
| [AWS CloudFormation](cloudformation.md) | 2, 5 | [05](../labs/05-cloudformation-signals-changesets-drift/README.md), [06](../labs/06-stacksets-multi-region/README.md) |
| [AWS SAM and AWS CDK](sam-cdk.md) | 2 | [03](../labs/03-sam-lambda-canary/README.md) |
| [AWS Systems Manager](systems-manager.md) | 2, 4, 5 | [07](../labs/07-systems-manager-fleet/README.md) |
| [AWS Config](config.md) | 2, 4, 5, 6 | [08](../labs/08-config-auto-remediation/README.md) |
| [AWS AppConfig](appconfig.md) | 2 | - |
| [AWS Service Catalog](service-catalog.md) | 2 | - |

## Multi-account governance

| Service | Exam domains | Hands-on lab |
|---|---|---|
| [AWS Organizations and SCPs](organizations.md) | 2, 6 | [15](../labs/15-organizations-scp/README.md) |
| [AWS Control Tower](control-tower.md) | 2, 6 | - |

## Resilience, data and networking

| Service | Exam domains | Hands-on lab |
|---|---|---|
| [Amazon S3 (events, integrity, protection)](s3.md) | 1, 3, 4, 5, 6 | [16](../labs/16-multi-region-dr/README.md) |
| [Databases and storage: HA and replication](databases-storage.md) | 3 | [16](../labs/16-multi-region-dr/README.md) |
| [Amazon Route 53](route53.md) | 3, 4 | [16](../labs/16-multi-region-dr/README.md) |
| [CloudFront and Global Accelerator](cloudfront-global-accelerator.md) | 3 | - |
| [AWS Backup](aws-backup.md) | 3 | - |
| [Resilience Hub, FIS and Elastic Disaster Recovery](resilience-hub-fis-drs.md) | 3 | - |

## Monitoring and events

| Service | Exam domains | Hands-on lab |
|---|---|---|
| [Amazon CloudWatch (metrics, alarms, logs, agent, synthetics)](cloudwatch.md) | 4, 5 | [09](../labs/09-cloudwatch-logs-alarms/README.md) |
| [AWS X-Ray](xray.md) | 4 | [10](../labs/10-xray-api-gateway-lambda/README.md) |
| [AWS CloudTrail](cloudtrail.md) | 4, 6 | [14](../labs/14-guardduty-security-response/README.md) |
| [Amazon EventBridge](eventbridge.md) | 5 | [11](../labs/11-eventbridge-sqs-dlq/README.md), [14](../labs/14-guardduty-security-response/README.md) |
| [AWS Health](health.md) | 5 | - |
| [SQS, SNS, Kinesis, Firehose and Lambda event handling](sqs-sns-kinesis.md) | 3, 5 | [11](../labs/11-eventbridge-sqs-dlq/README.md) |
| [Athena and QuickSight (log analytics)](analytics-athena-quicksight.md) | 4 | - |

## Security

| Service | Exam domains | Hands-on lab |
|---|---|---|
| [IAM, STS and IAM Identity Center](iam-sts-identity-center.md) | 6 | [13](../labs/13-iam-boundary-abac/README.md) |
| [Secrets Manager and Parameter Store](secrets-manager-parameter-store.md) | 1, 6 | [01](../labs/01-codebuild-codepipeline/README.md) |
| [AWS KMS, CloudHSM and encryption](kms-cloudhsm.md) | 6 | - |
| [AWS Certificate Manager (ACM)](acm.md) | 6 | - |
| [Network security (SG, NACL, WAF, Shield, Network Firewall)](network-security.md) | 6 | [08](../labs/08-config-auto-remediation/README.md) |
| [Security detection services (GuardDuty, Inspector, Macie, Security Hub, Detective, Access Analyzer)](security-detection.md) | 6 | [14](../labs/14-guardduty-security-response/README.md) |
