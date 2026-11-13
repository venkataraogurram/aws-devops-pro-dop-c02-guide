[← AWS CodePipeline](codepipeline.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS CodeArtifact →](codeartifact.md)

# AWS CodeDeploy

**Exam domains:** [Domain 1](../01-sdlc-automation.md), [Domain 5](../05-incident-event-response.md) | **Hands-on:** [Lab 02](../labs/02-codedeploy-ec2-rollback/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

**What:** Deploys application revisions to **EC2/on-premises**, **AWS Lambda**, and **Amazon ECS**.

Terms: **Application** -> **Deployment group** (target instances/tags/ASG, or ECS service, or Lambda function; deployment config; alarms; rollback; triggers) -> **Deployment** of a **revision** (from S3 or GitHub for EC2; AppSpec for Lambda/ECS).

## Compute platforms and deployment types

| Platform | In-place | Blue/green | Traffic shifting options |
|---|---|---|---|
| EC2 / on-prem | Yes (stop app, install new version on same instances) | Yes (new instances, ASG copy or manual; reroute LB) | AllAtOnce, HalfAtATime, OneAtATime, or custom minimum healthy hosts |
| Lambda | No (always shifts alias traffic = blue/green style) | Yes | Canary, Linear, AllAtOnce |
| ECS | No | Yes (new task set, ALB/NLB listener switch, optional test listener) | Canary, Linear, AllAtOnce |

## Predefined deployment configurations

| Platform | Configs |
|---|---|
| EC2 | `CodeDeployDefault.AllAtOnce`, `CodeDeployDefault.HalfAtATime`, `CodeDeployDefault.OneAtATime` |
| Lambda | `CodeDeployDefault.LambdaCanary10Percent5Minutes` (also 10, 15, 30 Minutes), `LambdaLinear10PercentEvery1Minute` (also 2, 3, 10 Minutes), `LambdaAllAtOnce` |
| ECS | `CodeDeployDefault.ECSCanary10Percent5Minutes` / `15Minutes`, `ECSLinear10PercentEvery1Minutes` / `3Minutes`, `ECSAllAtOnce` |

- **Canary** = 10% first, wait N min, then 100%.
- **Linear** = +10% every N min until 100%.
- EC2 `OneAtATime`: deployment fails if any instance fails (except last). `HalfAtATime`: up to half down. Custom config = "minimum healthy hosts" as number or %.

## AppSpec file

**EC2/On-prem (`appspec.yml` at root of revision):**
```yaml
version: 0.0
os: linux
files:
  - source: /build
    destination: /var/www/app
permissions:
  - object: /var/www/app
    owner: nginx
hooks:
  ApplicationStop:
    - location: scripts/stop.sh
      timeout: 60
  BeforeInstall:
    - location: scripts/install_deps.sh
  AfterInstall:
    - location: scripts/configure.sh
  ApplicationStart:
    - location: scripts/start.sh
  ValidateService:
    - location: scripts/health_check.sh   # exit non-zero = deployment fails
      timeout: 300
      runas: root
```

**Lambda:**
```yaml
version: 0.0
Resources:
  - MyFunction:
      Type: AWS::Lambda::Function
      Properties:
        Name: my-function
        Alias: live
        CurrentVersion: "3"
        TargetVersion: "4"
Hooks:
  - BeforeAllowTraffic: PreTrafficTestFn     # Lambda that runs tests, calls PutLifecycleEventHookExecutionStatus
  - AfterAllowTraffic: PostTrafficTestFn
```

**ECS:**
```yaml
version: 0.0
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: "arn:aws:ecs:...:task-definition/web:12"
        LoadBalancerInfo:
          ContainerName: "web"
          ContainerPort: 80
Hooks:
  - BeforeInstall: "LambdaFnA"
  - AfterInstall: "LambdaFnB"
  - AfterAllowTestTraffic: "LambdaFnC"   # run tests against the test listener (e.g., port 8080)
  - BeforeAllowTraffic: "LambdaFnD"
  - AfterAllowTraffic: "LambdaFnE"
```

## Lifecycle hook ORDER (memorise)

**EC2 in-place (with load balancer):**
```
BeforeBlockTraffic -> BlockTraffic -> AfterBlockTraffic
-> ApplicationStop -> DownloadBundle -> BeforeInstall -> Install -> AfterInstall
-> ApplicationStart -> ValidateService
-> BeforeAllowTraffic -> AllowTraffic -> AfterAllowTraffic
```
- You can script: ApplicationStop, BeforeInstall, AfterInstall, ApplicationStart, ValidateService, and the Before/After traffic hooks.
- You **cannot** script: DownloadBundle, Install, BlockTraffic, AllowTraffic (CodeDeploy does them).
- **ApplicationStop runs the script from the PREVIOUS successful revision.** If that script is broken, every deployment fails at ApplicationStop. Fix: deploy with `--ignore-application-stop-failures` (or console checkbox), or remove the old revision on the instance.

**EC2 blue/green:** on the **green** (replacement) instances: ApplicationStop ... ValidateService, BeforeAllowTraffic -> AllowTraffic -> AfterAllowTraffic. On the **blue** (original) instances: BeforeBlockTraffic -> BlockTraffic -> AfterBlockTraffic, then they are terminated (after the wait time you set) or kept.

**ECS:** BeforeInstall -> Install -> AfterInstall -> AllowTestTraffic -> AfterAllowTestTraffic -> BeforeAllowTraffic -> AllowTraffic -> AfterAllowTraffic.

**Lambda:** BeforeAllowTraffic -> AllowTraffic -> AfterAllowTraffic.

## CodeDeploy agent (EC2/on-prem)
- Must be installed and running on instances (install via **SSM Distributor / State Manager** association `AWS-ConfigureAWSPackage` with package `AWSCodeDeployAgent` - this is the "least overhead" way, also keeps it updated).
- Instance profile needs **S3 read** for the revision bucket (and KMS decrypt if encrypted).
- On-prem servers: register with IAM user or IAM role session (`aws deploy register-on-premises-instance`), tag them.
- Logs: `/var/log/aws/codedeploy-agent/codedeploy-agent.log`; script output: `/opt/codedeploy-agent/deployment-root/deployment-logs/codedeploy-agent-deployments.log`.
- Keeps **5 revisions** by default on disk (`:max_revisions:` in `/etc/codedeploy-agent/conf/codedeployagent.yml`). Disk full from old revisions -> lower this value.

## Rollbacks
- **Automatic rollback**: on deployment failure and/or when **CloudWatch alarms** (attached to the deployment group) go to ALARM. Rollback = a **new deployment** of the last known good revision (new deployment ID).
- During ECS/Lambda blue/green, rollback just shifts traffic back - fast.
- "Stop deployment" + rollback can also be triggered manually.

## ASG integration
- CodeDeploy installs a lifecycle hook on the ASG, so **new instances launched by scale-out automatically get the latest revision**.
- If a scale-out happens **during** a deployment, new instances get the previously deployed revision; CodeDeploy then starts a **follow-on deployment** to update them. To avoid this, configure the deployment group to **suspend ASG processes during the deployment** (valid values: Terminate, AZRebalance, InstanceRefresh, ScheduledActions). CodeDeploy resumes them when the deployment ends.
- Blue/green with ASG: CodeDeploy copies the ASG (new ASG, new instances), then shifts LB traffic.

## Troubleshooting table

| Symptom | Cause / fix |
|---|---|
| Deployment stuck "Pending"/fails with no instance logs | Agent not installed/running, instance profile missing, no route to CodeDeploy/S3 endpoints |
| Fails at ApplicationStop | Previous revision's stop script broken -> `ignoreApplicationStopFailures` |
| Fails at ValidateService | Health script exit code non-zero or timeout; check deployments log |
| "The overall deployment failed because too many individual instances failed" | Min healthy hosts violated; fix the scripts, check instance health |
| Files already exist at destination | Set `file_exists_behavior` (DISALLOW default, OVERWRITE, RETAIN) |
| AccessDenied downloading revision | Instance profile lacks s3:GetObject / kms:Decrypt |
| ECS deployment fails in Install | Task definition / container health check failing; check ECS service events |
| Lambda deployment rolls back | Alarm went into ALARM during canary, or BeforeAllowTraffic hook reported Failed |

---

---

[← AWS CodePipeline](codepipeline.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS CodeArtifact →](codeartifact.md)
