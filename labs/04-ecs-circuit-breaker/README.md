[← Lab 03](../03-sam-lambda-canary/README.md) | [Labs index](../README.md) | [🏠 Home](../../README.md) | [Lab 05 →](../05-cloudformation-signals-changesets-drift/README.md)

# Lab 04 - ECS Fargate: circuit breaker rollback, stopped-task alerts, ECR lifecycle and scanning

**Goal:** run an ECS service on Fargate, deploy a broken image, and watch the **deployment circuit breaker** roll back automatically. Get an email for every stopped task. Optionally push images to ECR and see tag immutability, scanning and lifecycle rules.

**Exam topics:** rolling update `minimumHealthyPercent`/`maximumPercent`, circuit breaker with rollback, `CannotPullContainerError`, task execution role, awslogs driver, EventBridge "ECS Task State Change", ECR immutability/scan on push/lifecycle policy, CloudFormation waiting for service stability.
**Services:** [ECS and EKS](../../services/ecs-eks.md), [ECR](../../services/ecr.md), [EventBridge](../../services/eventbridge.md)
**Time:** ~1 h | **Cost:** ~$0.10 (2 small Fargate tasks for ~1 h)

## Step 1 - Deploy the healthy service
```bash
cd labs/04-ecs-circuit-breaker
aws cloudformation deploy --stack-name dop-lab04 --template-file template.yaml \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides VpcId=$VPC_ID Subnets=$SUBNETS NotificationEmail=you@example.com
```
Confirm the SNS subscription email. Check the service:
```bash
aws ecs describe-services --cluster dop-lab04 --services dop-lab04-web \
  --query 'services[0].{running:runningCount,desired:desiredCount,deployments:deployments[].{status:status,rollout:rolloutState,td:taskDefinition}}'
```
Expected: `running: 2`, one deployment with `rolloutState: COMPLETED`.

## Step 2 - Break it: deploy an image tag that does not exist
```bash
aws cloudformation deploy --stack-name dop-lab04 --template-file template.yaml \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides VpcId=$VPC_ID Subnets=$SUBNETS NotificationEmail=you@example.com ImageTag=does-not-exist
```
While it runs (10-15 minutes), watch in another terminal:
```bash
aws ecs describe-services --cluster dop-lab04 --services dop-lab04-web \
  --query 'services[0].deployments[].{status:status,rollout:rolloutState,reason:rolloutStateReason,failed:failedTasks}'
aws ecs describe-services --cluster dop-lab04 --services dop-lab04-web --query 'services[0].events[0:5].message'
```
What you should see:
1. New tasks start and stop with `CannotPullContainerError` (the tag doesn't exist). You get an email for each stopped task with that reason.
2. **The old 2 tasks keep running**, because `minimumHealthyPercent: 100` means ECS never removes healthy old tasks before new ones are healthy. Users see no outage.
3. After the failure threshold (at least 3 failed tasks), the circuit breaker marks the new deployment `FAILED` and **rolls back** to the last completed deployment.
4. CloudFormation sees the failed deployment, fails the stack update and rolls back the stack too, so the template and the service are consistent again.

Check the stack events: `aws cloudformation describe-stack-events --stack-name dop-lab04 --max-items 15 --query 'StackEvents[].[LogicalResourceId,ResourceStatus,ResourceStatusReason]' --output table`.

**Exam link:** without the circuit breaker, this deployment would retry forever and CloudFormation would wait up to 3 hours. With a private subnet and no NAT, you'd see the same `CannotPullContainerError` for a real image. The fix then is VPC endpoints (`ecr.api`, `ecr.dkr`, S3 gateway, `logs`) plus execution role permissions.

## Step 3 (optional, needs Docker or Finch) - ECR immutability, scanning, lifecycle
```bash
REPO=$(aws cloudformation describe-stacks --stack-name dop-lab04 --query "Stacks[0].Outputs[0].OutputValue" --output text)
aws ecr get-login-password | docker login --username AWS --password-stdin ${REPO%/*}     # or: finch login ...
docker pull public.ecr.aws/nginx/nginx:stable
docker tag public.ecr.aws/nginx/nginx:stable $REPO:v1 && docker push $REPO:v1
docker pull public.ecr.aws/nginx/nginx:mainline
docker tag public.ecr.aws/nginx/nginx:mainline $REPO:v1 && docker push $REPO:v1   # a DIFFERENT image with the same tag
```
- The second push fails: the repository has **immutable tags**, so `v1` can't be moved to another image. Push it as `v2` instead: `docker tag public.ecr.aws/nginx/nginx:mainline $REPO:v2 && docker push $REPO:v2`.
- Scan results (scan on push, basic scanning):
  `aws ecr describe-image-scan-findings --repository-name dop-lab04-app --image-id imageTag=v1 --query 'imageScanFindings.findingSeverityCounts'`
- Push 4+ tags (`v2`, `v3`, `v4`). Within about 24 hours, the lifecycle policy expires the oldest so only 3 remain. Preview it now: `aws ecr start-lifecycle-policy-preview --repository-name dop-lab04-app`, then `get-lifecycle-policy-preview`.

## Exam takeaways
- **Circuit breaker + rollback** = least-effort automatic rollback for ECS rolling updates. CodeDeploy blue/green is the answer when you need test traffic or traffic shifting.
- `minimumHealthyPercent`/`maximumPercent` control capacity during deployments.
- `CannotPullContainerError` -> network path to ECR/registry, or execution role permissions, or a wrong image tag.
- EventBridge "ECS Task State Change" with `lastStatus: STOPPED` -> SNS = crash alerts.
- ECR: **immutable tags**, **scan on push** (enhanced scanning = Inspector, continuous), **lifecycle policies**.

## Cleanup
```bash
aws cloudformation delete-stack --stack-name dop-lab04
aws cloudformation wait stack-delete-complete --stack-name dop-lab04
```
(`EmptyOnDelete: true` lets CloudFormation delete the ECR repo even if you pushed images.)
