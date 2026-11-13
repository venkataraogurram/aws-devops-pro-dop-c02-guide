[← Lab 05](../05-cloudformation-signals-changesets-drift/README.md) | [Labs index](../README.md) | [🏠 Home](../../README.md) | [Lab 07 →](../07-systems-manager-fleet/README.md)

# Lab 06 - CloudFormation StackSets across Regions

**Goal:** deploy one baseline template to two Regions with a StackSet, use per-Region parameter overrides, break a deployment so a stack instance becomes **OUTDATED**, fix it, and detect **StackSet drift**.

**Exam topics:** self-managed vs service-managed permissions, administration/execution roles, operation preferences (concurrency, failure tolerance, Region order), parameter overrides, OUTDATED troubleshooting (global names, permissions, trust, quotas), StackSet drift.
**Services:** [CloudFormation](../../services/cloudformation.md)
**Time:** ~1 h | **Cost:** ~$0 (SSM parameters, SNS topics, empty buckets)

This lab uses **one account** as both administrator and target, which is allowed with self-managed permissions. Regions used: `us-east-1` and `us-west-2`.

A small helper that waits for a StackSet operation:
```bash
waitop() { while true; do s=$(aws cloudformation describe-stack-set-operation --stack-set-name dop-lab06-baseline --operation-id $1 --region us-east-1 --query StackSetOperation.Status --output text); echo $s; [[ $s == RUNNING || $s == QUEUED ]] || break; sleep 10; done; }
instances() { aws cloudformation list-stack-instances --stack-set-name dop-lab06-baseline --region us-east-1 --query 'Summaries[].[Region,Status,StackInstanceStatus.DetailedStatus,DriftStatus,StatusReason]' --output table; }
cd labs/06-stacksets-multi-region
```

## Step 1 - Create the StackSet roles
```bash
aws cloudformation deploy --region us-east-1 --stack-name dop-lab06-roles --template-file stackset-roles.yaml --capabilities CAPABILITY_NAMED_IAM
```
- `AWSCloudFormationStackSetAdministrationRole`: CloudFormation in the admin account assumes it.
- `AWSCloudFormationStackSetExecutionRole`: in every target account, trusted by the admin role, and has the permissions to create the resources.

These default names are what StackSets uses when you don't pass role ARNs.

## Step 2 - Create the StackSet and deploy to two Regions
```bash
aws cloudformation create-stack-set --region us-east-1 --stack-set-name dop-lab06-baseline \
  --template-body file://baseline.yaml --permission-model SELF_MANAGED
OP=$(aws cloudformation create-stack-instances --region us-east-1 --stack-set-name dop-lab06-baseline \
  --accounts $ACCOUNT_ID --regions us-east-1 us-west-2 \
  --operation-preferences RegionConcurrencyType=SEQUENTIAL,FailureToleranceCount=0,MaxConcurrentCount=1 \
  --query OperationId --output text); waitop $OP; instances
```
Expected: `SUCCEEDED`, two instances `CURRENT`. Check one Region:
```bash
aws ssm get-parameter --name /dop-lab06/baseline --region us-west-2 --query Parameter.Value --output text
```

## Step 3 - Per-Region parameter override
Make `us-west-2` the DR environment without a second template:
```bash
OP=$(aws cloudformation update-stack-instances --region us-east-1 --stack-set-name dop-lab06-baseline \
  --accounts $ACCOUNT_ID --regions us-west-2 --parameter-overrides ParameterKey=Environment,ParameterValue=dr \
  --query OperationId --output text); waitop $OP
aws ssm get-parameter --name /dop-lab06/baseline --region us-west-2 --query Parameter.Value --output text   # env=dr
aws ssm get-parameter --name /dop-lab06/baseline --region us-east-1 --query Parameter.Value --output text   # env=sandbox
```

## Step 4 - Break it: a globally unique name -> OUTDATED
S3 bucket names are global. The template's `global` naming uses the same bucket name in both Regions:
```bash
OP=$(aws cloudformation update-stack-set --region us-east-1 --stack-set-name dop-lab06-baseline --template-body file://baseline.yaml \
  --parameters ParameterKey=Environment,UsePreviousValue=true ParameterKey=CreateBucket,ParameterValue=true ParameterKey=BucketNameSuffix,ParameterValue=global \
  --operation-preferences RegionConcurrencyType=SEQUENTIAL,FailureToleranceCount=1,MaxConcurrentCount=1 \
  --query OperationId --output text); waitop $OP; instances
```
Expected: the first Region creates the bucket, the second fails. That instance is **`OUTDATED`** and the reason says the bucket already exists. `FailureToleranceCount=1` let the operation continue past one failure. With 0 it would stop.

The stack in the failed Region rolled back. Its events show the real error:
```bash
aws cloudformation describe-stacks --region us-west-2 --query "Stacks[?starts_with(StackName,'StackSet-dop-lab06-baseline')].StackName" --output text
```

Fix it with per-Region names and redeploy:
```bash
OP=$(aws cloudformation update-stack-set --region us-east-1 --stack-set-name dop-lab06-baseline --template-body file://baseline.yaml \
  --parameters ParameterKey=Environment,UsePreviousValue=true ParameterKey=CreateBucket,ParameterValue=true ParameterKey=BucketNameSuffix,ParameterValue=region \
  --operation-preferences RegionConcurrencyType=PARALLEL,FailureToleranceCount=0,MaxConcurrentCount=2 \
  --query OperationId --output text); waitop $OP; instances
```
Both are `CURRENT` again.

## Step 5 - StackSet drift
Change a resource by hand in one Region, then detect drift on the whole StackSet:
```bash
aws ssm put-parameter --name /dop-lab06/baseline --value "changed by hand" --overwrite --region us-west-2
OP=$(aws cloudformation detect-stack-set-drift --region us-east-1 --stack-set-name dop-lab06-baseline --query OperationId --output text); waitop $OP; instances
aws cloudformation describe-stack-set --region us-east-1 --stack-set-name dop-lab06-baseline --query 'StackSet.StackSetDriftDetectionDetails'
```
Expected: the `us-west-2` instance is `DRIFTED`, and so is the StackSet. To fix it, run an `update-stack-instances` for that Region, which reapplies the template.

## How service-managed would differ (read only, needs AWS Organizations)
```bash
aws cloudformation create-stack-set --stack-set-name org-baseline --template-body file://baseline.yaml \
  --permission-model SERVICE_MANAGED --auto-deployment Enabled=true,RetainStacksOnAccountRemoval=false
aws cloudformation create-stack-instances --stack-set-name org-baseline \
  --deployment-targets OrganizationalUnitIds=ou-xxxx-yyyyyyyy --regions us-east-1 us-west-2
```
- No roles to create (StackSets uses service-linked roles via trusted access).
- Targets are **OUs**, and **new accounts in the OU get the stacks automatically**.
- Can be run from a **delegated administrator** account (`--call-as DELEGATED_ADMIN`).
- The management account itself is not targeted.

## Cleanup
```bash
OP=$(aws cloudformation delete-stack-instances --region us-east-1 --stack-set-name dop-lab06-baseline \
  --accounts $ACCOUNT_ID --regions us-east-1 us-west-2 --no-retain-stacks --query OperationId --output text); waitop $OP
aws cloudformation delete-stack-set --region us-east-1 --stack-set-name dop-lab06-baseline
aws cloudformation delete-stack --region us-east-1 --stack-name dop-lab06-roles
aws s3 ls | grep dop-lab06 || echo "no lab06 buckets left"
```
If a bucket is left over from the failed attempt, delete it: `aws s3 rb s3://dop-lab06-$ACCOUNT_ID`.

## Exam takeaways
- **Self-managed** = you create admin + execution roles (works outside an org). **Service-managed** = Organizations, OU targets, auto-deploy to new accounts, delegated admin.
- **OUTDATED** = the last operation failed for that instance. Look at the instance's stack events in the target account/Region.
- **Failure tolerance / max concurrent** control blast radius during rollouts.
- StackSet drift rolls up from stack instances. Direct changes to an instance's stack through CloudFormation aren't counted as drift.
