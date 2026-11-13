[← Lab 11](../11-eventbridge-sqs-dlq/README.md) | [Labs index](../README.md) | [🏠 Home](../../README.md) | [Lab 13 →](../13-iam-boundary-abac/README.md)

# Lab 12 - Auto Scaling: ELB health checks, a termination lifecycle hook, instance refresh

**Goal:**
- see the ASG **replace** an instance whose app is broken but whose EC2 status checks pass, because `HealthCheckType: ELB`;
- catch the termination with a **lifecycle hook** that copies the instance's log file to S3 before it disappears;
- roll a new launch template version through the fleet with **instance refresh**.

**Exam topics:** EC2 vs ELB health checks, health check grace period, target group health checks and deregistration delay, lifecycle hooks (`Terminating:Wait`, heartbeat, `complete-lifecycle-action`, default result), EventBridge lifecycle events, instance refresh vs CloudFormation UpdatePolicy.
**Services:** [EC2 Auto Scaling](../../services/ec2-auto-scaling.md), [ELB](../../services/elastic-load-balancing.md), [Systems Manager](../../services/systems-manager.md)
**Time:** ~2 h | **Cost:** ~$0.20 (internal ALB + 2-3 t3.micro for 2 hours)

The ALB is **internal**: only the VPC can reach it. You test from inside an instance via SSM.

## Step 1 - Deploy
```bash
cd labs/12-auto-scaling-lifecycle-hooks
aws cloudformation deploy --stack-name dop-lab12 --template-file template.yaml --capabilities CAPABILITY_IAM \
  --parameter-overrides VpcId=$VPC_ID Subnets=$SUBNETS
out() { aws cloudformation describe-stacks --stack-name dop-lab12 --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text; }
export ALB=$(out AlbDns) TG=$(out TargetGroupArn) LOGS=$(out LogBucketName)
health() { aws elbv2 describe-target-health --target-group-arn $TG --query 'TargetHealthDescriptions[].[Target.Id,TargetHealth.State]' --output table; }
sleep 120; health
```
Expected: 2 targets `healthy`.

Call the ALB from one instance (it alternates between the two hosts):
```bash
I1=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names dop-lab12-asg --query 'AutoScalingGroups[0].Instances[0].InstanceId' --output text)
C=$(aws ssm send-command --instance-ids $I1 --document-name AWS-RunShellScript \
  --parameters "commands=[\"for i in 1 2 3 4; do curl -s http://$ALB/; done\"]" --query Command.CommandId --output text); sleep 6
aws ssm get-command-invocation --command-id $C --instance-id $I1 --query StandardOutputContent --output text
```

## Step 2 - Break the app (not the instance)
Delete the health file on instance 1. The OS and EC2 status checks stay fine.
```bash
aws ssm send-command --instance-ids $I1 --document-name AWS-RunShellScript --parameters 'commands=["rm -f /var/www/html/health"]' >/dev/null
sleep 40; health
```
Expected: `$I1` becomes `unhealthy` (2 failed checks x 10 s). Because the ASG uses **ELB health checks**, it marks the instance unhealthy and **terminates and replaces** it:
```bash
aws autoscaling describe-scaling-activities --auto-scaling-group-name dop-lab12-asg --max-items 3 \
  --query 'Activities[].[StatusCode,Description,Cause]' --output text
```
With the default `EC2` health check type, the ASG would keep this broken instance forever. That's a classic exam trap.

## Step 3 - The lifecycle hook saved the logs
Termination paused the instance in **`Terminating:Wait`**. EventBridge invoked `dop-lab12-terminate-hook`, which sent a Run Command to the instance: upload `/var/log/app.log` to S3, then call `complete-lifecycle-action CONTINUE`.
```bash
aws logs tail /aws/lambda/dop-lab12-terminate-hook --since 10m --format short
aws s3 ls s3://$LOGS/ --recursive
```
Expected: `<instance-id>/app.log` exists in the bucket. If the command had failed, the hook would continue on its own after the **heartbeat timeout** (300 s here) because `DefaultResult: CONTINUE`.

## Step 4 - Roll out a new version with instance refresh
Update the launch template (new `AppVersion` in user data). CloudFormation updates the ASG's launch template version, but **does not replace running instances**: this ASG has no `UpdatePolicy`.
```bash
aws cloudformation deploy --stack-name dop-lab12 --template-file template.yaml --capabilities CAPABILITY_IAM \
  --parameter-overrides VpcId=$VPC_ID Subnets=$SUBNETS AppVersion=v2
aws autoscaling start-instance-refresh --auto-scaling-group-name dop-lab12-asg \
  --preferences '{"MinHealthyPercentage":50,"InstanceWarmup":120}'
watch -n 20 "aws autoscaling describe-instance-refreshes --auto-scaling-group-name dop-lab12-asg --query 'InstanceRefreshes[0].[Status,PercentageComplete]' --output text"
```
(Press Ctrl+C when `Successful`. Without `watch`, re-run the command.)

The refresh replaces instances in batches while keeping 50% healthy. Each replaced instance also goes through the lifecycle hook, so more logs appear in S3. Call the ALB again (Step 1 command with a current instance ID): the page shows `v2`.

**Exam contrast:**
- Instance refresh: for any ASG, including ones not managed by CloudFormation, or "just roll the new AMI". Supports checkpoints and **auto rollback**.
- CloudFormation `UpdatePolicy` (`AutoScalingRollingUpdate` / `AutoScalingReplacingUpdate`): CloudFormation replaces instances as part of the stack update.

## Cleanup
```bash
aws s3 rm s3://$LOGS --recursive
aws cloudformation delete-stack --stack-name dop-lab12
aws cloudformation wait stack-delete-complete --stack-name dop-lab12
aws logs delete-log-group --log-group-name /aws/lambda/dop-lab12-terminate-hook
```
(While the stack deletes, each instance passes through the hook too. That's expected; it continues after the command or the timeout.)

## Exam takeaways
- **HealthCheckType ELB** + a sensible **grace period**. Too short a grace period = instances killed while booting.
- **Lifecycle hooks**: launch hooks (install/configure before InService) and terminate hooks (drain, save logs, deregister). Finish with `complete-lifecycle-action`, extend with `record-lifecycle-action-heartbeat`.
- **Instance refresh** = rolling replacement to a new launch template/AMI.
