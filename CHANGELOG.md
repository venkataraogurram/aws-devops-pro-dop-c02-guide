# Changelog

## v2.1 - 2026-11-13
- Scope audit against the official exam guide (in-scope services list, task statements, Technologies and Concepts, out-of-scope tasks). Added a "What is NOT on the exam" section and the keep/cut rule to Chapter 0.
- Removed services that are not in scope: Amplify (file deleted), Audit Manager, AWS Artifact, DevOps Guru, CloudWatch RUM / Internet Monitor / Evidently / Application Signals / Investigations, Managed Service for Apache Flink, MSK, Route 53 ARC, Verified Access, Nitro Enclaves, AWS Signer, IoT Greengrass, CodePipeline Device Farm/Jenkins providers, non-listed Application Auto Scaling targets.
- Removed features with no exam value (released after the exam content, or not tested): S3 Files volumes, Lambda SnapStart, ALB dual-stack, CloudWatch Logs field indexes, Backup Audit Manager.
- Cut database depth the guide lists as out of scope (ElastiCache data types/endpoints, DynamoDB item limits, DMS metric names). Glue reduced to the Data Catalog note needed for Athena (file renamed to analytics-athena-quicksight.md).
- Kept briefly, with a note, because they appear as answer options: Global Accelerator, Firewall Manager.

## v2.0 - 2026-11-13
- New `services/` folder: 42 service files. Service content moved out of the domain chapters (one place per fact). Domain chapters now list the services to study and keep the cross-service sections and quick-maps.
- New `labs/` folder: 16 step-by-step labs with CloudFormation/SAM templates (all pass cfn-lint), code, expected output, "break it" steps, exam takeaways and cleanup. Written but not run end to end.
- Gap check against a DOP-C02 course slide deck: added CodeCommit migration/replication, CodeBuild triggers/badges, CodePipeline change detection/artifact rules/CloudFormation action modes, CodeArtifact retention, Image Builder AMI tracking, StackSet OUTDATED causes and drift, Beanstalk notifications/worker tier, `sam sync`, CDK vs SAM, SSM documents/hybrid/OpsCenter, Lambda concurrency/storage/EFS, API Gateway endpoint types/stage variables/caching/throttling/errors, ECS roles/volumes (incl. S3 Files)/event patterns/logging, EKS node types/logging, Kinesis capacity modes vs Firehose, SNS DLQ, RDS/Aurora/ElastiCache/DynamoDB details, DMS, Storage Gateway, S3 events and object integrity, warm pools, Application Auto Scaling, ALB/NLB/NAT HA, Route 53 records, Config org rules vs conformance packs, Organizations feature sets/RI sharing/moving accounts, Control Tower levels and enrollment, Identity Center flow and ABAC, Firewall Manager, CloudFront origin protection, GuardDuty IP lists, Inspector requirements, Trusted Advisor quotas, AMI sharing with KMS, EC2 status checks, Health dashboards, Athena/Glue/QuickSight, Amplify. All written in my own words.
- Study plan rows now link the service files and labs for each day.

## v1.1 - 2026-11-13
- Split the single guide into one file per chapter with Prev / Home / Next navigation. Labs moved to their own chapter (10); cheat sheet is now chapter 11. Added a mistakes-log template.
- Fact-check corrections (verified against AWS docs): AWS Proton end of support Oct 7, 2026; SSM Change Manager closed to new customers Nov 7, 2025; AWS Chatbot renamed Amazon Q Developer in chat applications; ASG lifecycle hook heartbeat 30 s-2 h (default 1 h), total wait max 48 h or 100 x heartbeat; Firehose buffer interval 0-900 s (zero buffering); DynamoDB PITR period 1-35 days; CodeBuild phase-failure behaviour; CodeDeploy follow-on deployment and suspendable ASG processes; ALB 503 meaning; Logs Insights filter-before-stats example; KMS/role trust policy evaluation wording; GuardDuty finding name; Inspector trial is 15 days.

## v1.0 - 2026-11-13
- Complete single-file DOP-C02 guide: 11 chapters covering all 6 exam domains, comparisons, 60 practice questions, 46-day plan, labs, cheat sheet.
