[← 1. Domain 1: SDLC Automation (22%)](01-sdlc-automation.md) | [🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [3. Domain 3: Resilient Cloud Solutions (15%) →](03-resilient-cloud.md)

# Chapter 2 - Domain 2: Configuration Management and IaC (17%)

> CloudFormation is the single most important service on this exam. Then Systems Manager, Organizations/Control Tower, Config, Service Catalog, CDK/SAM, Step Functions/Lambda automation.

## Services to study for this domain

Read these service files first, then the sections below.

- [EC2 Image Builder](services/ec2-image-builder.md)
- [AWS Step Functions and Lambda automation](services/step-functions.md)
- [AWS CloudFormation](services/cloudformation.md)
- [AWS SAM and AWS CDK](services/sam-cdk.md)
- [AWS Systems Manager](services/systems-manager.md)
- [AWS Config](services/config.md)
- [AWS AppConfig](services/appconfig.md)
- [AWS Service Catalog](services/service-catalog.md)
- [AWS Organizations and SCPs](services/organizations.md)
- [AWS Control Tower](services/control-tower.md)

## 2.1 IaC options on AWS

| Tool | What | When the exam picks it |
|---|---|---|
| **CloudFormation** | Declarative JSON/YAML templates -> stacks | Default IaC answer; StackSets for multi-account |
| **AWS SAM** | CFN extension (Transform) for serverless | Lambda + API Gateway + DynamoDB apps, gradual Lambda deploys, `sam local` testing |
| **AWS CDK** | Write infra in TypeScript/Python/Java/Go/C#, synthesises to CFN | Reusable constructs, loops/logic, developer-friendly; CDK Pipelines |
| **Service Catalog** | Approved CFN/Terraform products in portfolios for self-service | "Let users launch only approved, compliant resources without giving them broad IAM" |
| **CloudFormation modules / registry** | Reusable resource blocks / third-party types | Standard building blocks in many templates |
| **Terraform** | HashiCorp IaC (Service Catalog supports Terraform products, Control Tower AFT uses Terraform) | When question explicitly uses Terraform |
| **Elastic Beanstalk / App Runner / Copilot / Proton** | Higher-level app platforms | Developers want to deploy apps without managing infra |

---

## 2.2 Configuration management services: which one?

| Service | What it manages | Pick when |
|---|---|---|
| **Systems Manager** | Instances (EC2 + on-prem + edge): commands, patching, state, inventory, sessions, parameters, runbooks | Almost every "manage the fleet" question |
| **AWS Config** | Records resource configuration + evaluates compliance rules; remediates via SSM | "Detect / audit / remediate non-compliant resources" |
| **AWS AppConfig** | Application configuration + feature flags deployed gradually with validation and rollback | "Change app behaviour without redeploying code, safely" |
| **OpsWorks** (EOL) | Managed Chef / Puppet | Only if the question insists on Chef/Puppet; otherwise SSM |
| **CloudFormation** | Infrastructure lifecycle | Provision resources |
| **Elastic Beanstalk `.ebextensions`** | App env config | App running on Beanstalk |

## 2.3 Domain 2 scenario quick-map

| Scenario | Answer |
|---|---|
| Deploy IAM role/Config rule to all current and future accounts in an OU | StackSets **service-managed** with automatic deployment |
| Deploy to accounts not in the org | StackSets self-managed (admin + execution roles) |
| Prevent stack update from replacing RDS | Stack policy denying `Update:Replace` on the DB (and DeletionPolicy/UpdateReplacePolicy Snapshot/Retain) |
| Preview impact of template change | Change set |
| Detect manual changes to stack resources | Drift detection (automate with Config rule) |
| EC2 must finish configuration before stack completes | cfn-init + cfn-signal + CreationPolicy |
| Apply config changes to running instances on stack update | cfn-hup |
| ASG update with zero downtime, rollback easy | UpdatePolicy `AutoScalingReplacingUpdate` (or rolling with `WaitOnResourceSignals`) |
| Stack stuck in UPDATE_ROLLBACK_FAILED | ContinueUpdateRollback (skip resources) |
| Use latest AMI always | Parameter type `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>` with public param |
| Reusable infra in a programming language | CDK |
| Users launch approved stacks without IAM rights | Service Catalog + launch constraint |
| Org-wide account vending with Terraform | Control Tower AFT |
| Block non-compliant resource before creation | CloudFormation Hook / CT proactive control |
| Desired-state config on instances, re-applied automatically | SSM State Manager |
| Report and fix config drift on AWS resources | AWS Config rule + SSM Automation remediation |
| Org-wide patching | SSM Patch Manager patch policy via Quick Setup |
| Feature flag gradual rollout + auto rollback | AppConfig + CloudWatch alarm |
| Long multi-step automation with retries | Step Functions |

---

[← 1. Domain 1: SDLC Automation (22%)](01-sdlc-automation.md) | [🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [3. Domain 3: Resilient Cloud Solutions (15%) →](03-resilient-cloud.md)
