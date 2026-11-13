[← AWS Elastic Beanstalk](elastic-beanstalk.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Lambda deployments →](lambda.md)

# Amazon ECS, EKS and Fargate

**Exam domains:** [Domain 1](../01-sdlc-automation.md), [Domain 3](../03-resilient-cloud.md), [Domain 5](../05-incident-event-response.md) | **Hands-on:** [Lab 04](../labs/04-ecs-circuit-breaker/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## ECS deployments
- **Rolling update** (ECS controller): `minimumHealthyPercent` and `maximumPercent` control how many tasks stay up / extra tasks launched.
- **Deployment circuit breaker** with `rollback: true` -> if new tasks keep failing to reach steady state, ECS automatically rolls back to the last completed deployment. Also **CloudWatch alarm-based rollback** for ECS deployments.
- **Blue/green via CodeDeploy**: two target groups, production listener + optional test listener, task sets. Traffic shifting canary/linear/all-at-once. Termination wait time for original tasks.
- ECS also has native blue/green, canary and linear deployments (2025) without CodeDeploy - know they exist; most questions still use CodeDeploy.
- Pipeline: CodeBuild writes `imagedefinitions.json` (for ECS standard deploy action) or `imageDetail.json` + `appspec.yaml` + `taskdef.json` (for "Amazon ECS (Blue/Green)" CodeDeploy action).

## EKS deployments
- Kubernetes rolling updates (`maxSurge`, `maxUnavailable`), blue/green with two services/ingress, canary with service mesh or Argo Rollouts / Flagger.
- CI/CD: CodeBuild builds image -> pushes to ECR -> `kubectl`/Helm in CodeBuild (role mapped via **EKS access entries** or aws-auth ConfigMap) or GitOps (Argo CD / Flux).

## Containers and serverless platforms (exam task 3.2)
- **ECS** launch types: EC2 (you manage instances), **Fargate** (serverless). ECS Anywhere for on-prem. Task definitions, services, task role (app permissions) vs **task execution role** (pull ECR image, push logs, read secrets).
- **EKS**: managed control plane; node types: managed node groups, self-managed, Fargate profiles, Auto Mode. Pod IAM: **IRSA** (OIDC provider) or **EKS Pod Identity** (simpler). Add-ons: VPC CNI, CoreDNS, kube-proxy, EBS CSI driver, ADOT.
- **App Runner**: fully managed web apps from source/image, auto scaling, least overhead for simple web services. (Closed to new customers from Apr 30, 2026; AWS recommends ECS Express Mode now. Know the concept.)
- **Copilot** CLI for ECS/App Runner apps with pipelines. **App2Container** containerises existing .NET/Java apps.
- **API Gateway + Lambda + DynamoDB** = classic serverless. Use **Lambda Powertools**, X-Ray, DLQs / on-failure destinations.

## ECS IAM roles
- **Task execution role**: used by the ECS agent to pull images from ECR, send logs to CloudWatch, read secrets referenced in the task definition.
- **Task role**: used by your application code (e.g., read S3, write DynamoDB). One per task definition, different apps get different roles.
- **EC2 instance profile** (EC2 launch type only): lets the ECS agent register the instance and call ECS APIs.

## Load balancing, storage and scaling
- **ALB** (most common, dynamic host port mapping on EC2 launch type, path/host routing), **NLB** (high throughput, TCP/UDP, PrivateLink). Classic LB is not recommended.
- **EFS volumes** for persistent shared storage across tasks and AZs (Fargate + EC2). **S3 Files volumes** (2026): mount S3 data as a file system for tasks on **Fargate and ECS Managed Instances only (not the EC2 launch type)**; changes sync to the bucket.
- **Service auto scaling** (Application Auto Scaling): target tracking on CPU/memory/ALB `RequestCountPerTarget`, step, scheduled. For the EC2 launch type also scale the instances: **capacity provider with managed scaling** (recommended) or ASG scaling on cluster reservation.

## Event-driven ECS patterns
- EventBridge rule -> **run an ECS task** (e.g., when an object lands in S3, process it in a Fargate task).
- EventBridge **schedule** -> run a task every hour (batch jobs without servers).
- SQS queue -> ECS service workers poll it, scale on queue depth.
- EventBridge rule on **ECS Task State Change** with `lastStatus: STOPPED` (filter on `stoppedReason`/exit code) -> SNS to alert on crashed tasks.

## Logging
- `awslogs` log driver sends container stdout/stderr to CloudWatch Logs (execution role needs logs permissions).
- **FireLens** / sidecar log router container (Fluent Bit) to send logs to many destinations (CloudWatch, Firehose, OpenSearch, third parties).

## EKS
- **Node types**: managed node groups (AWS manages the ASG lifecycle), self-managed nodes, **Fargate** profiles (no nodes), **EKS Auto Mode** (AWS manages nodes, scaling and core add-ons).
- **Storage**: CSI drivers + StorageClass - **EBS** (one AZ), **EFS** (works with Fargate), FSx for Lustre / NetApp ONTAP.
- **Control plane logging** to CloudWatch Logs: choose types `api`, `audit`, `authenticator`, `controllerManager`, `scheduler`.
- **Node and container logs/metrics**: CloudWatch agent / Fluent Bit (DaemonSet) with **Container Insights**, or ADOT.

---

[← AWS Elastic Beanstalk](elastic-beanstalk.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Lambda deployments →](lambda.md)
