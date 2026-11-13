[← Lab 06](../06-stacksets-multi-region/README.md) | [Labs index](../README.md) | [🏠 Home](../../README.md) | [Lab 08 →](../08-config-auto-remediation/README.md)

# Lab 07 - Systems Manager: manage a fleet without SSH

**Goal:** manage two instances that have **no inbound ports**:
- **Session Manager** shell;
- **Run Command** with rate control and error thresholds;
- **State Manager** associations that install and configure the **CloudWatch agent** (memory and disk metrics + log file) and re-apply it;
- **Inventory**;
- a **Patch Manager** compliance scan.

**Exam topics:** managed node prerequisites, tag targeting, rate control, State Manager desired state, CloudWatch agent config in Parameter Store, `AWS-RunPatchBaseline` Scan vs Install, patch groups, compliance, inventory.
**Services:** [Systems Manager](../../services/systems-manager.md), [CloudWatch](../../services/cloudwatch.md)
**Time:** ~2 h | **Cost:** ~$0.10 (2 t3.micro + a few custom metrics)

## Step 1 - Deploy
```bash
cd labs/07-systems-manager-fleet
aws cloudformation deploy --stack-name dop-lab07 --template-file template.yaml --capabilities CAPABILITY_IAM \
  --parameter-overrides VpcId=$VPC_ID Subnets=$SUBNETS
# if it fails on InventoryAssociation (inventory already collected by Quick Setup), redeploy with CreateInventoryAssociation=false
export N1=$(aws cloudformation describe-stacks --stack-name dop-lab07 --query "Stacks[0].Outputs[?OutputKey=='Node1Id'].OutputValue" --output text)
export N2=$(aws cloudformation describe-stacks --stack-name dop-lab07 --query "Stacks[0].Outputs[?OutputKey=='Node2Id'].OutputValue" --output text)
```

## Step 2 - Are they managed nodes?
```bash
aws ssm describe-instance-information --filters Key=tag:Lab,Values=dop-lab07 \
  --query 'InstanceInformationList[].[InstanceId,PingStatus,AgentVersion,PlatformName]' --output table
```
Expected after 2-3 minutes: both `Online`. The three prerequisites are all met here:
- **SSM Agent** (preinstalled on Amazon Linux);
- an **instance profile** with `AmazonSSMManagedInstanceCore`;
- **network** to the SSM endpoints (public subnet with internet; private subnets need VPC endpoints).

## Step 3 - Session Manager (no SSH, no port 22)
Console: **EC2 > Instances > dop-lab07-node1 > Connect > Session Manager > Connect**. Or from your terminal with the [Session Manager plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html) installed: `aws ssm start-session --target $N1`.

Run `whoami` (you are `ssm-user`) and `sudo ss -tlnp` (nothing listens on port 22 from the outside; the security group has no inbound rules at all). In **Session Manager > Session history** you see who connected and when (also in CloudTrail as `StartSession`). Session logging to S3/CloudWatch Logs is set in **Session Manager > Preferences**.

## Step 4 - Run Command with rate control
A command that succeeds everywhere:
```bash
aws ssm send-command --document-name AWS-RunShellScript --targets Key=tag:Lab,Values=dop-lab07 \
  --parameters 'commands=["uptime","df -h /"]' --max-concurrency 1 --max-errors 0 \
  --comment "fleet check" --query Command.CommandId --output text
```
A command that fails, with `--max-errors 0` and one instance at a time:
```bash
CMD=$(aws ssm send-command --document-name AWS-RunShellScript --targets Key=tag:Lab,Values=dop-lab07 \
  --parameters 'commands=["echo simulating a failure","exit 1"]' --max-concurrency 1 --max-errors 0 \
  --query Command.CommandId --output text); sleep 30
aws ssm list-command-invocations --command-id $CMD --query 'CommandInvocations[].[InstanceId,Status]' --output table
aws ssm list-commands --command-id $CMD --query 'Commands[0].[Status,ErrorCount,CompletedCount,TargetCount]'
```
Expected: the first instance `Failed`. Because the error threshold (0) was passed, **the second instance is not run**, and the command's overall status is `Failed`. That is how you protect a fleet from a bad script: small `--max-concurrency` + low `--max-errors`.

## Step 5 - State Manager installed and configured the CloudWatch agent
```bash
aws ssm list-associations --association-filter-list key=AssociationName,value=dop-lab07 \
  --query 'Associations[].[Name,Overview.Status,LastExecutionDate]' --output table
```
`dop-lab07-install-cw-agent` should be `Success`. The configure association may have run **before** the agent was installed and failed. Run it again now (State Manager also re-runs it on its schedule):
```bash
CFG=$(aws ssm list-associations --association-filter-list key=AssociationName,value=dop-lab07-configure-cw-agent --query 'Associations[0].AssociationId' --output text)
aws ssm start-associations-once --association-ids $CFG
```
After 3-5 minutes, the custom metrics appear:
```bash
aws cloudwatch list-metrics --namespace DOP-Lab07 --query 'Metrics[].[MetricName,Dimensions[0].Value]' --output table
aws logs describe-log-streams --log-group-name /dop-lab07/dnf --query 'logStreams[].logStreamName'
```
Expected: `mem_used_percent` and `disk_used_percent` per instance, and one log stream per instance. **EC2 never publishes memory or disk usage by itself.**

**Desired state test:** stop the agent on node 1 (`aws ssm send-command --instance-ids $N1 --document-name AWS-RunShellScript --parameters 'commands=["systemctl stop amazon-cloudwatch-agent"]'`). Then run `start-associations-once` for the configure association again. It restarts the agent, as State Manager would on its next scheduled run.

## Step 6 - Inventory
```bash
aws ssm list-inventory-entries --instance-id $N1 --type-name AWS:Application --max-results 5 \
  --query 'Entries[].[Name,Version]' --output table
```
Expected: installed packages (it may take up to 30 minutes for the first collection; run `start-associations-once` on `dop-lab07-inventory` to speed it up). For a whole org, a **Resource Data Sync** sends inventory from all accounts/Regions to S3, which you query with Athena.

## Step 7 - Patch compliance scan (no changes made)
```bash
aws ssm send-command --document-name AWS-RunPatchBaseline --targets Key=tag:Lab,Values=dop-lab07 \
  --parameters Operation=Scan --query Command.CommandId --output text
sleep 120
aws ssm describe-instance-patch-states --instance-ids $N1 $N2 \
  --query 'InstancePatchStates[].[InstanceId,PatchGroup,BaselineId,InstalledCount,MissingCount,Operation]' --output table
```
- `Scan` reports missing patches. `Install` would install them (and may reboot, controlled by `RebootOption`).
- `PatchGroup` shows `dop-lab07` from the **`Patch Group` tag**. Register a custom baseline for that group with `aws ssm register-patch-baseline-for-patch-group`; otherwise the default baseline for the OS is used.
- In production you run `Install` inside a **Maintenance Window**, or org-wide with a **Quick Setup patch policy**.

## Exam takeaways
- Managed node = **agent + role + network**.
- **Run Command** = run now, with rate control. **State Manager** = keep it that way (new instances too, on a schedule).
- CloudWatch agent config lives in **Parameter Store** (`AmazonCloudWatch-*`) and is deployed by SSM.
- **Patch Manager**: baselines, patch groups, Scan/Install, Maintenance Windows, compliance.
- **Session Manager** replaces SSH and bastions, with IAM control and logging.

## Cleanup
```bash
aws cloudformation delete-stack --stack-name dop-lab07
aws cloudformation wait stack-delete-complete --stack-name dop-lab07
aws logs delete-log-group --log-group-name /dop-lab07/dnf
```
Custom metrics expire on their own (no cost once nothing publishes them).
