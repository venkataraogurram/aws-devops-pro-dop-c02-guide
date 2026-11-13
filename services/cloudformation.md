[← Elastic Load Balancing and compute high availability](elastic-load-balancing.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS SAM and AWS CDK →](sam-cdk.md)

# AWS CloudFormation

**Exam domains:** [Domain 2](../02-config-mgmt-iac.md), [Domain 5](../05-incident-event-response.md) | **Hands-on:** [Lab 05](../labs/05-cloudformation-signals-changesets-drift/README.md), [Lab 06](../labs/06-stacksets-multi-region/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## Template anatomy
```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: Web tier
Transform: AWS::Serverless-2016-10-31          # optional: SAM, AWS::Include, LanguageExtensions, macros
Metadata: {}                                   # AWS::CloudFormation::Init lives under a resource's Metadata
Parameters:
  Env:
    Type: String
    AllowedValues: [dev, prod]
  LatestAmi:
    Type: AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>   # always latest AMI from Parameter Store
    Default: /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64
Rules: {}                                      # validate parameter combinations before create/update
Mappings:
  RegionMap:
    us-east-1: { InstanceType: t3.micro }
Conditions:
  IsProd: !Equals [!Ref Env, prod]
Resources:                                     # the ONLY required section
  Bucket:
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    UpdateReplacePolicy: Retain
Outputs:
  BucketName:
    Value: !Ref Bucket
    Export:
      Name: !Sub "${AWS::StackName}-BucketName"
```

## Intrinsic functions (know what each returns)
`!Ref` (param value / resource physical ID), `!GetAtt` (attribute, e.g. `ALB.DNSName`), `!Sub`, `!Join`, `!Split`, `!Select`, `!FindInMap`, `!If` / `!Equals` / `!And` / `!Or` / `!Not`, `!ImportValue` (cross-stack), `!GetAZs`, `!Base64` (user data), `!Cidr`, `Fn::ForEach` (LanguageExtensions transform). Pseudo params: `AWS::Region`, `AWS::AccountId`, `AWS::StackName`, `AWS::StackId`, `AWS::Partition`, `AWS::URLSuffix`, `AWS::NoValue`.

## Dynamic references (secrets without hard-coding)
- `{{resolve:ssm:/myapp/ami-id}}` - plain parameter (can pin version `:3`)
- `{{resolve:ssm-secure:/myapp/db-pass}}` - SecureString, only for supported resource properties
- `{{resolve:secretsmanager:prod/db:SecretString:password}}` - **most common answer for RDS master password**. Even better: `ManageMasterUserPassword: true` on RDS (RDS stores and rotates it in Secrets Manager).

## Stack lifecycle tools

| Feature | What it does | Exam use |
|---|---|---|
| **Change sets** | Preview what an update will add/modify/**replace** before executing | "Ensure no resource is replaced unexpectedly"; manual review step in pipeline |
| **Drift detection** | Compares actual resource config to template | "Find manual changes"; Config rule `cloudformation-stack-drift-detection-check` for automation |
| **Stack policy** | JSON policy that protects resources from **updates** (Update:Replace, Update:Delete...) | "Prevent accidental replacement of the prod database during stack updates". Once set, every resource is protected unless allowed; you can update but not delete the policy; override temporarily during an update. |
| **Termination protection** | Prevents stack deletion | "Prevent someone deleting the stack" |
| **DeletionPolicy** | `Delete` (default for most), `Retain`, `RetainExceptOnCreate`, `Snapshot` (EBS volume, RDS instance/cluster, ElastiCache, Redshift, Neptune, DocumentDB) | "Keep data when stack is deleted" |
| **UpdateReplacePolicy** | Same options, applies when an update **replaces** the resource | "Keep old DB snapshot when a property change forces replacement" |
| **Rollback triggers** | CloudWatch alarms monitored during create/update + monitoring time (0-180 min) after; alarm = rollback | "Roll back stack update automatically if errors increase after deploy" |
| **Disable rollback / preserve resources** | Keep successfully created resources on failure to debug, then retry | Faster troubleshooting iterations |
| **Retain on delete / skip** | On DELETE_FAILED, retry delete with resources to retain | Bucket not empty, resource deleted manually |
| **ContinueUpdateRollback** | Fix `UPDATE_ROLLBACK_FAILED` (optionally `--resources-to-skip`) | Resource changed outside CFN, rollback can't restore it |
| **IaC generator** | Scan existing resources, generate a template | Bring manually created resources under IaC |
| **Resource import** | Import existing resources into a stack (needs DeletionPolicy in template) | Adopt resources without recreating |
| **Stack refactoring** | Move resources between stacks | Split a big stack |

## Helper scripts and signals (EC2 bootstrapping)

```yaml
WebServer:
  Type: AWS::EC2::Instance
  CreationPolicy:
    ResourceSignal:
      Count: 1
      Timeout: PT15M                # wait up to 15 min for cfn-signal
  Metadata:
    AWS::CloudFormation::Init:
      configSets:
        default: [install, configure]
      install:
        packages: { yum: { httpd: [] } }
        files:
          /var/www/html/index.html:
            content: "hello"
        services:
          sysvinit:
            httpd: { enabled: true, ensureRunning: true }
      configure:
        commands:
          01_run: { command: "echo configured" }
  Properties:
    ImageId: !Ref LatestAmi
    InstanceType: t3.micro
    UserData:
      Fn::Base64: !Sub |
        #!/bin/bash -xe
        /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource WebServer --region ${AWS::Region}
        /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource WebServer --region ${AWS::Region}
```

| Script | Purpose |
|---|---|
| `cfn-init` | Reads `AWS::CloudFormation::Init` metadata: packages, groups, users, sources, files, commands, services (in that order within a config) |
| `cfn-signal` | Sends success/failure to a **CreationPolicy** or **WaitCondition** |
| `cfn-hup` | Daemon that detects **metadata changes** on stack update and re-runs hooks (e.g., cfn-init). Default check interval **15 minutes**. Config `/etc/cfn/cfn-hup.conf` + `/etc/cfn/hooks.d/*.conf` |
| `cfn-get-metadata` | Print metadata |

- **CreationPolicy** = wait for N signals before marking EC2 instance / ASG `CREATE_COMPLETE`. Timeout -> CREATE_FAILED -> rollback.
- **WaitCondition + WaitConditionHandle** = wait for signals from **outside** (on-prem script, external system) or coordinate ordering. For EC2/ASG prefer CreationPolicy.
- Troubleshooting "stack fails waiting for signal": check `/var/log/cfn-init.log`, `/var/log/cfn-init-cmd.log`, `/var/log/cloud-init-output.log`; instance needs outbound access to CFN endpoint (NAT or VPC endpoint); use "preserve resources on failure" to keep the instance for debugging.

## UpdatePolicy for Auto Scaling groups (frequently tested)

| Policy | Behaviour |
|---|---|
| `AutoScalingRollingUpdate` | Replace instances in batches: `MaxBatchSize`, `MinInstancesInService`, `MinSuccessfulInstancesPercent`, `PauseTime`, `WaitOnResourceSignals: true` (needs cfn-signal from new instances), `SuspendProcesses` (suspend HealthCheck, ReplaceUnhealthy, AZRebalance, AlarmNotification, ScheduledActions during update) |
| `AutoScalingReplacingUpdate` | `WillReplace: true` -> creates a **new ASG**, switches when new one is healthy, deletes old one; rollback is easy (keep old ASG). Immutable style. |
| `AutoScalingScheduledAction` | `IgnoreUnmodifiedGroupSizeProperties: true` so stack updates don't reset sizes changed by scheduled actions |

Updates triggered by changing the **launch template/configuration** (AMI, instance type, user data). Other UpdatePolicy uses: `CodeDeployLambdaAliasUpdate` (Lambda alias traffic shifting via CodeDeploy), `EnableVersionUpgrade` (OpenSearch), `UseOnlineResharding` (ElastiCache).

Alternative for ASGs outside CFN control: **ASG Instance Refresh** (min healthy %, checkpoints, skip matching, auto rollback on alarm).

## Multi-stack architecture

| Pattern | How | Notes |
|---|---|---|
| **Cross-stack references** | Producer `Outputs` with `Export`, consumer `!ImportValue` | Same account + Region. You **cannot delete or modify** an export while it's imported. Good for separately-owned layers (network team VPC stack). |
| **Nested stacks** | `AWS::CloudFormation::Stack` with TemplateURL | Reuse components (common ALB pattern); updated through the root stack. |
| **SSM parameters** | Producer writes value to Parameter Store, consumer reads `{{resolve:ssm:}}` | Loose coupling, works cross-Region via replication logic |
| **StackSets** | One template -> many accounts/Regions | See below |

## StackSets (multi-account / multi-Region)

| Permission model | Setup | Best for |
|---|---|---|
| **Self-managed** | Create `AWSCloudFormationStackSetAdministrationRole` in admin account and `AWSCloudFormationStackSetExecutionRole` in each target account (trusting admin) | Accounts not in your org, fine-grained control |
| **Service-managed** | Uses AWS Organizations (trusted access). Target **OUs**. **Automatic deployment** to new accounts added to the OU (and removal on leave). Can be run from a **delegated administrator** member account. | "Every new account must automatically get this baseline (IAM role, Config rule, CloudTrail...)" |

Deployment options: **maximum concurrent accounts** (number/%), **failure tolerance** (number/%), **Region concurrency** (sequential/parallel), **region order**. Stack instances can have **parameter overrides** per account/Region.
Note: service-managed StackSets do **not deploy to the management account** - deploy it there separately.

## Custom resources
- `Type: Custom::Something` (or `AWS::CloudFormation::CustomResource`) with `ServiceToken` = Lambda ARN or SNS topic.
- CFN sends Create/Update/Delete events. Your function **must send a response (SUCCESS/FAILED) to the pre-signed S3 URL** (`cfn-response` module). If it never responds the stack hangs until timeout (default **1 hour**; configurable with `ServiceTimeout`).
- Common bugs: Lambda crashes before responding; Delete not handled -> stack stuck in DELETE_IN_PROGRESS/DELETE_FAILED; Lambda in VPC with no route to S3 URL.
- Use for: things CFN doesn't support, emptying an S3 bucket before deletion, looking up AMI IDs, calling third-party APIs.
- Modern alternatives: **CloudFormation Registry resource types** (private types) and **Hooks**.

## Macros, transforms, modules, hooks, Guard
- **Transforms**: `AWS::Serverless` (SAM), `AWS::Include` (insert snippets from S3), `AWS::LanguageExtensions` (`Fn::ForEach`, `Fn::Length`, `Fn::ToJsonString`, intrinsic in DeletionPolicy).
- **Macros**: your Lambda processes the template before deployment (custom shorthand, loops).
- **Modules**: package resources + config as a reusable type `MyOrg::Web::Bucket::MODULE`.
- **CloudFormation Hooks**: run validation **before** create/update/delete of resources (proactive control). Control Tower **proactive controls** are Hooks. Can use **Guard** rules or Lambda. Fail = operation blocked.
- **cfn-guard** (policy-as-code) and **cfn-lint** in the pipeline to validate templates before deploy. **Template scanning** via CodeBuild step.

## Common CloudFormation errors -> fix

| Error | Fix |
|---|---|
| `UPDATE_ROLLBACK_FAILED` | Fix the underlying resource manually or `continue-update-rollback --resources-to-skip` |
| `DELETE_FAILED` (S3 bucket not empty, SG in use, resource gone) | Empty bucket / remove dependency / retry delete retaining the resource |
| `Export X cannot be deleted as it is in use by Y` | Remove the import from consumer stack first |
| Resource replaced unexpectedly | Use change sets; stack policy; check "Update requires: Replacement" in docs (e.g., renaming a resource with a custom name) |
| `Requires capabilities: [CAPABILITY_IAM / CAPABILITY_NAMED_IAM / CAPABILITY_AUTO_EXPAND]` | Pass the capability (named IAM resources / macros + nested with transforms) |
| Timeout waiting for signal | cfn-init/cfn-signal logs, network to CFN endpoint, correct resource logical ID |
| Insufficient permissions during deploy | Use a **CFN service role** (`--role-arn`) with needed permissions; users only need `iam:PassRole` + CFN permissions (least privilege pattern) |

---

## StackSets: troubleshooting and drift
- Stack instance status **OUTDATED** = the last operation on that account/Region failed. Common causes:
  - missing permissions in the target account (execution role);
  - no trust between the administration account and the target account's execution role;
  - a resource name that must be globally unique already exists (e.g., S3 bucket name);
  - a quota/limit reached in the target account.
- **StackSet drift detection** checks every stack instance's stack. If a resource drifted, the stack, the stack instance and the StackSet are all reported as drifted. Changes made directly to a stack instance's stack with CloudFormation (not through the StackSet) are **not** counted as drift.

## Other must-knows
- **DependsOn**: force creation order when CloudFormation can't infer it (e.g., an EC2 instance that needs an IGW attachment / route to exist first). References (`!Ref`, `!GetAtt`) already create implicit dependencies.
- **Service role**: CloudFormation uses this role for all stack operations; users only need `iam:PassRole` + CloudFormation permissions (least privilege).
- **Enable a service that may already be on** (e.g., GuardDuty detector across many accounts): a plain resource fails if the detector exists, so use a **Lambda-backed custom resource** that enables it only if needed, deployed with **StackSets** across the org.

---

[← Elastic Load Balancing and compute high availability](elastic-load-balancing.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS SAM and AWS CDK →](sam-cdk.md)
