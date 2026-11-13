[← Lab 04](../04-ecs-circuit-breaker/README.md) | [Labs index](../README.md) | [🏠 Home](../../README.md) | [Lab 06 →](../06-stacksets-multi-region/README.md)

# Lab 05 - CloudFormation: signals, cfn-hup, change sets, stack policy, drift, DeletionPolicy

**Goal:** see the CloudFormation behaviours the exam asks about most, on one small EC2 stack:
- **CreationPolicy** waiting for **cfn-signal**;
- a cfn-init failure and how to debug it;
- **cfn-hup** applying a metadata change without replacing the instance;
- **change sets** showing Replacement;
- a **stack policy** blocking replacement;
- **drift detection**;
- **termination protection** and **DeletionPolicy: Retain**.

**Services:** [CloudFormation](../../services/cloudformation.md), [Systems Manager](../../services/systems-manager.md)
**Time:** ~2 h | **Cost:** ~$0.05 (one t3.micro)

## Step 0 - Variables
```bash
export SUBNET1=${SUBNETS%%,*}; export SUBNET2=${SUBNETS##*,}; echo $SUBNET1 $SUBNET2
export AMI=$(aws ssm get-parameter --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 --query Parameter.Value --output text); echo $AMI
cd labs/05-cloudformation-signals-changesets-drift
```
**Why pin the AMI?** With a parameter of type `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>`, CloudFormation reads the latest AMI from Parameter Store again on **every** update. If AWS published a new AMI in the meantime, a "small" update would replace your instance. That's handy for golden-AMI pipelines, but a surprise in this lab. So the template takes a fixed `AmiId`.

## Step 1 - Create the stack and watch the signal
```bash
aws cloudformation create-stack --stack-name dop-lab05 --template-body file://template.yaml \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=VpcId,ParameterValue=$VPC_ID ParameterKey=SubnetId,ParameterValue=$SUBNET1 ParameterKey=AmiId,ParameterValue=$AMI
aws cloudformation describe-stack-events --stack-name dop-lab05 \
  --query 'StackEvents[?LogicalResourceId==`WebServer`].[Timestamp,ResourceStatus,ResourceStatusReason]' --output table
```
Run the events command a few times. The instance stays `CREATE_IN_PROGRESS` after EC2 launches it, until cfn-init finishes and **cfn-signal** sends success. Then you see `Received SUCCESS signal with UniqueId i-...` and `CREATE_COMPLETE`.

```bash
aws cloudformation wait stack-create-complete --stack-name dop-lab05
export IID=$(aws cloudformation describe-stacks --stack-name dop-lab05 --query "Stacks[0].Outputs[?OutputKey=='InstanceId'].OutputValue" --output text)
```

Helper to run a command on the instance through SSM and print the output:
```bash
run() { local id=$(aws ssm send-command --instance-ids $IID --document-name AWS-RunShellScript \
  --parameters "commands=[\"$1\"]" --query Command.CommandId --output text); sleep 6;
  aws ssm get-command-invocation --command-id $id --instance-id $IID --query StandardOutputContent --output text; }
run "curl -s localhost"
```
Expected: `<h1>DOP Lab 05 - Version 1</h1>`.

## Step 2 - Break it: cfn-init fails, so the stack fails
Create a second stack with a wrong package name and **rollback disabled**, so the instance stays for debugging:
```bash
aws cloudformation create-stack --stack-name dop-lab05-fail --template-body file://template.yaml \
  --capabilities CAPABILITY_IAM --disable-rollback \
  --parameters ParameterKey=VpcId,ParameterValue=$VPC_ID ParameterKey=SubnetId,ParameterValue=$SUBNET1 ParameterKey=AmiId,ParameterValue=$AMI \
               ParameterKey=PackageName,ParameterValue=httpd-does-not-exist
```
After a few minutes the `WebServer` event shows **`Received FAILURE signal`** and `CREATE_FAILED`. Find the cause on the instance:
```bash
FAIL_IID=$(aws cloudformation describe-stack-resource --stack-name dop-lab05-fail --logical-resource-id WebServer --query StackResourceDetail.PhysicalResourceId --output text)
CMD=$(aws ssm send-command --instance-ids $FAIL_IID --document-name AWS-RunShellScript --parameters 'commands=["tail -20 /var/log/cfn-init.log"]' --query Command.CommandId --output text); sleep 6
aws ssm get-command-invocation --command-id $CMD --instance-id $FAIL_IID --query StandardOutputContent --output text
```
You see the `dnf install` command fail. The other logs to know: `/var/log/cfn-init-cmd.log` (command output) and `/var/log/cloud-init-output.log` (user data).

Delete the failed stack: `aws cloudformation delete-stack --stack-name dop-lab05-fail`.

**Exam links:** "stack waits then fails with a signal timeout" = cfn-signal never called. Causes: user data error, no internet/VPC endpoint to reach CloudFormation, wrong logical ID. Debug with `--disable-rollback` (preserve successfully provisioned resources) and the cfn logs.

## Step 3 - cfn-hup: update metadata, keep the instance
```bash
aws cloudformation update-stack --stack-name dop-lab05 --use-previous-template --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=VpcId,UsePreviousValue=true ParameterKey=AmiId,UsePreviousValue=true ParameterKey=SubnetId,UsePreviousValue=true \
               ParameterKey=Message,ParameterValue="Version 2 via cfn-hup"
aws cloudformation wait stack-update-complete --stack-name dop-lab05
sleep 90; run "curl -s localhost"
```
Expected: the page now says `Version 2 via cfn-hup`, and the **instance ID is the same**. CloudFormation updated only the metadata. The cfn-hup daemon (interval 1 minute here, default 15) noticed it and re-ran cfn-init.

## Step 4 - Change sets: see Replacement before it happens
Change set A, the instance type (modify, no replacement, but the instance is stopped and started):
```bash
aws cloudformation create-change-set --stack-name dop-lab05 --change-set-name type-change --use-previous-template --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=VpcId,UsePreviousValue=true ParameterKey=AmiId,UsePreviousValue=true ParameterKey=SubnetId,UsePreviousValue=true ParameterKey=Message,UsePreviousValue=true ParameterKey=InstanceType,ParameterValue=t3.small
sleep 15
aws cloudformation describe-change-set --stack-name dop-lab05 --change-set-name type-change \
  --query 'Changes[].ResourceChange.[LogicalResourceId,Action,Replacement]' --output table
```
Change set B, the subnet (forces **replacement**):
```bash
aws cloudformation create-change-set --stack-name dop-lab05 --change-set-name subnet-change --use-previous-template --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=VpcId,UsePreviousValue=true ParameterKey=AmiId,UsePreviousValue=true ParameterKey=SubnetId,ParameterValue=$SUBNET2 ParameterKey=Message,UsePreviousValue=true
sleep 15
aws cloudformation describe-change-set --stack-name dop-lab05 --change-set-name subnet-change \
  --query 'Changes[].ResourceChange.[LogicalResourceId,Action,Replacement]' --output table
```
Expected: A shows `WebServer Modify False`; B shows `WebServer Modify True` (replacement = new instance, new ID). Don't execute either yet.

## Step 5 - Stack policy blocks the replacement
```bash
aws cloudformation set-stack-policy --stack-name dop-lab05 --stack-policy-body file://stack-policy.json
aws cloudformation execute-change-set --stack-name dop-lab05 --change-set-name subnet-change
sleep 30
aws cloudformation describe-stack-events --stack-name dop-lab05 --max-items 8 \
  --query 'StackEvents[].[LogicalResourceId,ResourceStatus,ResourceStatusReason]' --output table
```
Expected: the update fails with an "Action denied by stack policy" reason for `WebServer`, and the stack rolls back to `UPDATE_ROLLBACK_COMPLETE`. Other resources could still be updated. Only `Update:Replace` on `WebServer` is denied. You can **update** a stack policy, or override it for one update with `--stack-policy-during-update-body`, but you can't remove it.

Delete the leftover change set: `aws cloudformation delete-change-set --stack-name dop-lab05 --change-set-name type-change`.

## Step 6 - Drift detection
Make a manual change outside CloudFormation (an inbound rule, restricted to a documentation-only IP range, so nothing can actually connect):
```bash
SG=$(aws cloudformation describe-stacks --stack-name dop-lab05 --query "Stacks[0].Outputs[?OutputKey=='SecurityGroupId'].OutputValue" --output text)
aws ec2 authorize-security-group-ingress --group-id $SG --protocol tcp --port 8080 --cidr 192.0.2.10/32
DID=$(aws cloudformation detect-stack-drift --stack-name dop-lab05 --query StackDriftDetectionId --output text); sleep 20
aws cloudformation describe-stack-drift-detection-status --stack-drift-detection-id $DID --query '[DetectionStatus,StackDriftStatus]'
aws cloudformation describe-stack-resource-drifts --stack-name dop-lab05 --stack-resource-drift-status-filters MODIFIED \
  --query 'StackResourceDrifts[].[LogicalResourceId,PropertyDifferences[0].PropertyPath,PropertyDifferences[0].DifferenceType]' --output table
```
Expected: `DRIFTED`, `WebSG` with a `/SecurityGroupIngress` difference. Remove the rule: `aws ec2 revoke-security-group-ingress --group-id $SG --protocol tcp --port 8080 --cidr 192.0.2.10/32`.

To automate this: AWS Config rule `cloudformation-stack-drift-detection-check`.

## Step 7 - Termination protection and DeletionPolicy
```bash
aws cloudformation update-termination-protection --stack-name dop-lab05 --enable-termination-protection
aws cloudformation delete-stack --stack-name dop-lab05    # fails: termination protection is enabled
aws cloudformation update-termination-protection --stack-name dop-lab05 --no-enable-termination-protection
```

## Cleanup (also shows DeletionPolicy: Retain)
```bash
RB=$(aws cloudformation describe-stacks --stack-name dop-lab05 --query "Stacks[0].Outputs[?OutputKey=='RetainedBucketName'].OutputValue" --output text)
aws cloudformation delete-stack --stack-name dop-lab05
aws cloudformation wait stack-delete-complete --stack-name dop-lab05
aws s3api head-bucket --bucket $RB && echo "bucket $RB still exists (DeletionPolicy: Retain)"
aws s3 rb s3://$RB
aws cloudformation wait stack-delete-complete --stack-name dop-lab05-fail 2>/dev/null; echo done
```

## Exam takeaways
- **CreationPolicy + cfn-signal**: the stack waits for the app, and fails if the app's setup fails.
- **cfn-hup** applies metadata changes in place. Without it, changing `AWS::CloudFormation::Init` does nothing to running instances.
- **Change sets** show `Replacement: True` before you commit.
- **Stack policies** protect specific resources from specific update actions.
- **Drift detection** finds manual changes. **Termination protection** stops stack deletion. **DeletionPolicy/UpdateReplacePolicy** keep data.
