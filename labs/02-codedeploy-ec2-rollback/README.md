[← Lab 01](../01-codebuild-codepipeline/README.md) | [Labs index](../README.md) | [🏠 Home](../../README.md) | [Lab 03 →](../03-sam-lambda-canary/README.md)

# Lab 02 - CodeDeploy on an Auto Scaling group: hooks, rollback, and the ApplicationStop trap

**Goal:** deploy an app to 2 EC2 instances in an ASG with CodeDeploy, watch every lifecycle hook, make a deployment fail and roll back automatically, reproduce the famous **ApplicationStop** trap, and see new ASG instances get the app automatically.

**Exam topics:** CodeDeploy agent, instance profile S3 permissions, AppSpec hooks and order, OneAtATime config, automatic rollback, `--ignore-application-stop-failures`, ASG integration, agent log locations.
**Services:** [CodeDeploy](../../services/codedeploy.md), [EC2 Auto Scaling](../../services/ec2-auto-scaling.md), [Systems Manager](../../services/systems-manager.md)
**Time:** ~2 h | **Cost:** ~$0.10 (2-3 t3.micro for 2 hours)

## Step 1 - Deploy the infrastructure
```bash
cd labs/02-codedeploy-ec2-rollback
aws cloudformation deploy --stack-name dop-lab02 --template-file template.yaml \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides VpcId=$VPC_ID Subnets=$SUBNETS
export BUCKET=$(aws cloudformation describe-stacks --stack-name dop-lab02 \
  --query "Stacks[0].Outputs[?OutputKey=='RevisionBucketName'].OutputValue" --output text)
```
Wait about 3 minutes for the instances to boot and install the agent.

## Step 2 - Check the agent with Run Command (no SSH)
```bash
CMD=$(aws ssm send-command --document-name AWS-RunShellScript \
  --targets Key=tag:Lab,Values=dop-lab02 \
  --parameters 'commands=["systemctl is-active codedeploy-agent"]' \
  --query Command.CommandId --output text)
sleep 10
aws ssm list-command-invocations --command-id $CMD --details \
  --query 'CommandInvocations[].[InstanceId,CommandPlugins[0].Output]' --output text
```
Expected: `active` for both instances. If an instance is missing, it isn't an SSM managed node yet. Check the instance profile and outbound internet.

**At scale (exam answer):** install and update the agent with a State Manager association instead of user data:
`aws ssm create-association --name AWS-ConfigureAWSPackage --targets Key=tag:Lab,Values=dop-lab02 --parameters action=Install,name=AWSCodeDeployAgent --schedule-expression "rate(14 days)"`. Check that the package supports your OS version before relying on it.

## Step 3 - Deploy version 1
```bash
aws deploy push --application-name dop-lab02-app \
  --s3-location s3://$BUCKET/app-v1.zip --source revision --ignore-hidden-files
DEP=$(aws deploy create-deployment --application-name dop-lab02-app \
  --deployment-group-name dop-lab02-dg \
  --s3-location bucket=$BUCKET,key=app-v1.zip,bundleType=zip \
  --query deploymentId --output text); echo $DEP
```
Watch it:
```bash
aws deploy get-deployment --deployment-id $DEP --query 'deploymentInfo.[status,deploymentOverview]'
aws deploy list-deployment-instances --deployment-id $DEP
aws deploy get-deployment-instance --deployment-id $DEP --instance-id <one-instance-id> \
  --query 'instanceSummary.lifecycleEvents[].[lifecycleEventName,status]' --output table
```
You see the hook order: `ApplicationStop -> DownloadBundle -> BeforeInstall -> Install -> AfterInstall -> ApplicationStart -> ValidateService`. With `OneAtATime`, the instances are done one after the other.

Check the site from inside an instance:
```bash
aws ssm send-command --document-name AWS-RunShellScript --targets Key=tag:Lab,Values=dop-lab02 \
  --parameters 'commands=["curl -s localhost"]' --query Command.CommandId --output text
# then list-command-invocations as in step 2 -> "DOP Lab 02 - Version 1"
```

## Step 4 - Break it: failing ValidateService -> automatic rollback
Make the health check fail. Edit `revision/scripts/validate_service.sh` and change `grep -q "Version"` to `grep -q "Healthy"`. Then deploy v2:
```bash
aws deploy push --application-name dop-lab02-app --s3-location s3://$BUCKET/app-v2.zip --source revision --ignore-hidden-files
aws deploy create-deployment --application-name dop-lab02-app --deployment-group-name dop-lab02-dg \
  --s3-location bucket=$BUCKET,key=app-v2.zip,bundleType=zip --query deploymentId --output text
```
What you should see:
- The first instance fails at **ValidateService** (after the 30 s retry loop). With OneAtATime, the deployment stops: status `Failed`.
- Because auto rollback is on, CodeDeploy starts a **new deployment** that redeploys the last good revision (v1). `aws deploy list-deployments --application-name dop-lab02-app --deployment-group-name dop-lab02-dg` shows a new ID. `get-deployment` on it shows `rollbackInfo`.

**Read the logs** (Session Manager: `aws ssm start-session --target <instance-id>` needs the Session Manager plugin, or use the EC2 console "Connect > Session Manager"):
```bash
sudo tail -50 /var/log/aws/codedeploy-agent/codedeploy-agent.log
sudo tail -50 /opt/codedeploy-agent/deployment-root/deployment-logs/codedeploy-agent-deployments.log
```
The second file contains your script's output ("service did not become healthy").

Put `grep -q "Version"` back.

## Step 5 - The ApplicationStop trap
1. Make v3 with a **broken stop script**. Add `exit 1` as the last line of `revision/scripts/stop_server.sh` (replace `exit 0`). Change the page text to `Version 3`. Push and deploy v3.
   It **succeeds**. ApplicationStop ran the script from the previous revision (v1), which was fine.
2. Make v4. Change only the page text to `Version 4` (leave the bad stop script). Push and deploy v4.
   It **fails at ApplicationStop**, because CodeDeploy now runs v3's broken `stop_server.sh`. The automatic rollback (to v3) fails for the same reason.
3. Fix it the exam way. Put `exit 0` back in the stop script (that fixes future deployments), then deploy with the flag:
   ```bash
   aws deploy push --application-name dop-lab02-app --s3-location s3://$BUCKET/app-v5.zip --source revision --ignore-hidden-files
   aws deploy create-deployment --application-name dop-lab02-app --deployment-group-name dop-lab02-dg \
     --s3-location bucket=$BUCKET,key=app-v5.zip,bundleType=zip --ignore-application-stop-failures
   ```
   It succeeds. The next deployment uses v5's good stop script.

## Step 6 - New ASG instances get the app automatically
```bash
aws autoscaling set-desired-capacity --auto-scaling-group-name dop-lab02-asg --desired-capacity 3
```
After about 3 minutes:
```bash
aws deploy list-deployments --application-name dop-lab02-app --deployment-group-name dop-lab02-dg --max-items 1
aws deploy get-deployment --deployment-id <newest-id> --query 'deploymentInfo.[creator,status]'
```
The creator is `autoscaling`. CodeDeploy's lifecycle hook on the ASG held the new instance in `Pending:Wait` and deployed the **last successful revision** to it before it went `InService`. (The agent must already be running on the new instance; here, user data installs it.)

## Exam takeaways
- Agent + instance profile with **S3 read on the revision bucket** are required. Missing either = deployment hangs or fails with no script output.
- Hook order, and which hooks you can script.
- **ApplicationStop uses the previous revision's script.** Fix with `--ignore-application-stop-failures`.
- Rollback = a **new deployment** of the last good revision.
- ASG integration deploys to scale-out instances automatically. Scale-outs **during** a deployment trigger a follow-on deployment (or configure the group to suspend ASG processes).

## Cleanup
```bash
aws s3 rm s3://$BUCKET --recursive
aws cloudformation delete-stack --stack-name dop-lab02
aws cloudformation wait stack-delete-complete --stack-name dop-lab02
```
If you created the optional State Manager association, delete it: `aws ssm list-associations` then `aws ssm delete-association --association-id <id>`.
