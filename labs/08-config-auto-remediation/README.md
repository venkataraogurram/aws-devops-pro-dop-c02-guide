[← Lab 07](../07-systems-manager-fleet/README.md) | [Labs index](../README.md) | [🏠 Home](../../README.md) | [Lab 09 →](../09-cloudwatch-logs-alarms/README.md)

# Lab 08 - AWS Config rule with automatic remediation

**Goal:** detect a security group that allows SSH from the whole internet with the managed rule **restricted-ssh**, fix it automatically with the SSM Automation runbook **AWS-DisablePublicAccessForSecurityGroup**, and get an email from EventBridge when it happens.

**Exam topics:** Config recorder + delivery channel, managed rules and change-triggered evaluation, remediation configuration (automatic, retries, assume role, `RESOURCE_ID` parameter), "Config Rules Compliance Change" events, detect vs prevent.
**Services:** [AWS Config](../../services/config.md), [Systems Manager](../../services/systems-manager.md), [Network security](../../services/network-security.md)
**Time:** ~1 h | **Cost:** < $0.10 (a few configuration items and evaluations)

> **Safety:** the security group you open in this lab is **not attached to any instance or ENI**, so nothing is exposed. The remediation closes it within minutes anyway.

## Step 1 - Is AWS Config already recording in this Region?
```bash
aws configservice describe-configuration-recorders --query 'ConfigurationRecorders[].[name,recordingGroup.allSupported]'
aws configservice describe-configuration-recorder-status --query 'ConfigurationRecordersStatus[].[name,recording]'
```
- **Empty output**: deploy the optional recorder stack (records only security groups, to keep it cheap):
  ```bash
  cd labs/08-config-auto-remediation
  aws cloudformation deploy --stack-name dop-lab08-recorder --template-file config-recorder.yaml --capabilities CAPABILITY_IAM
  aws configservice describe-configuration-recorder-status --query 'ConfigurationRecordersStatus[].[name,recording]'
  ```
  If `recording` is `false`, start it: `aws configservice start-configuration-recorder --configuration-recorder-name <name>`.
- **A recorder exists and records all resources or security groups**: use it, skip the recorder stack. (Only one recorder per Region is allowed.)

## Step 2 - Deploy the rule, remediation and alert
```bash
cd labs/08-config-auto-remediation
aws cloudformation deploy --stack-name dop-lab08 --template-file template.yaml --capabilities CAPABILITY_IAM \
  --parameter-overrides VpcId=$VPC_ID NotificationEmail=you@example.com
export SG=$(aws cloudformation describe-stacks --stack-name dop-lab08 --query "Stacks[0].Outputs[0].OutputValue" --output text)
```
Confirm the SNS subscription email. Check the remediation configuration:
```bash
aws configservice describe-remediation-configurations --config-rule-names dop-lab08-restricted-ssh \
  --query 'RemediationConfigurations[0].[TargetId,Automatic,MaximumAutomaticAttempts]'
```

## Step 3 - Break it: open SSH to the world
```bash
aws ec2 authorize-security-group-ingress --group-id $SG --protocol tcp --port 22 --cidr 0.0.0.0/0
```
Watch the sequence (a few minutes in total):
```bash
# 1) Config records the change and evaluates the rule (change-triggered)
aws configservice get-compliance-details-by-config-rule --config-rule-name dop-lab08-restricted-ssh \
  --query 'EvaluationResults[].[EvaluationResultIdentifier.EvaluationResultQualifier.ResourceId,ComplianceType]' --output table
# 2) Remediation runs
aws configservice describe-remediation-execution-status --config-rule-name dop-lab08-restricted-ssh \
  --query 'RemediationExecutionStatuses[].[ResourceKey.ResourceId,State,StepDetails[0].Name]' --output table
aws ssm describe-automation-executions --filters Key=DocumentNamePrefix,Values=AWS-DisablePublicAccessForSecurityGroup \
  --query 'AutomationExecutionMetadataList[0:3].[AutomationExecutionId,AutomationExecutionStatus]' --output table
# 3) The rule is gone
aws ec2 describe-security-groups --group-ids $SG --query 'SecurityGroups[0].IpPermissions'
```
Expected:
1. The group shows `NON_COMPLIANT`, and you get the email.
2. An automation execution `Success`.
3. `IpPermissions` is `[]`.
4. On the next evaluation the group is `COMPLIANT` again.

Open **Config > Resources > the security group > Resource timeline**. It shows the configuration change, with a CloudTrail link to who made it (`AuthorizeSecurityGroupIngress` by your user), and the remediation change after it.

## Step 4 - Think like the exam
- Config **detected** and **fixed** this after it happened. To **prevent** it, use:
  - an SCP / IAM deny on `ec2:AuthorizeSecurityGroupIngress` with a CIDR condition;
  - **Firewall Manager** security group policies;
  - a CloudFormation Hook for IaC.
- For many accounts: an **organization Config rule** or **conformance pack** with the same remediation, deployed from the delegated admin account, plus an **aggregator** for one view.
- Faster alternative without Config: an **EventBridge rule on the CloudTrail event `AuthorizeSecurityGroupIngress`** -> Lambda that revokes the rule (near real time, but custom code).

## Cleanup
```bash
aws cloudformation delete-stack --stack-name dop-lab08
aws cloudformation wait stack-delete-complete --stack-name dop-lab08
# only if you created the recorder stack:
CB=$(aws cloudformation describe-stacks --stack-name dop-lab08-recorder --query "Stacks[0].Outputs[0].OutputValue" --output text)
aws s3 rm s3://$CB --recursive
aws cloudformation delete-stack --stack-name dop-lab08-recorder
```
