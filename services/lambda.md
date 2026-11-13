[← Amazon ECS, EKS and Fargate](ecs-eks.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon API Gateway →](api-gateway.md)

# AWS Lambda deployments

**Exam domains:** [Domain 1](../01-sdlc-automation.md), [Domain 3](../03-resilient-cloud.md), [Domain 5](../05-incident-event-response.md) | **Hands-on:** [Lab 03](../labs/03-sam-lambda-canary/README.md), [Lab 10](../labs/10-xray-api-gateway-lambda/README.md), [Lab 11](../labs/11-eventbridge-sqs-dlq/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## Lambda deployments
- **Versions** are immutable snapshots; **aliases** point to versions and can split traffic (weighted alias, e.g., 90/10).
- **CodeDeploy + alias traffic shifting** (canary/linear) with pre/post traffic hooks and CloudWatch alarm rollback.
- **AWS SAM** makes this easy:

```yaml
Transform: AWS::Serverless-2016-10-31
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.12
      Handler: app.handler
      CodeUri: src/
      AutoPublishAlias: live                 # publish a new version + move alias
      DeploymentPreference:
        Type: Canary10Percent5Minutes        # creates CodeDeploy app + deployment group
        Alarms:
          - !Ref ErrorsAlarm                 # rollback if alarm fires
        Hooks:
          PreTraffic: !Ref PreTrafficHookFn
          PostTraffic: !Ref PostTrafficHookFn
```

## Versions, aliases and environment variables
- **$LATEST** is mutable. **Published versions** are immutable (code + config) with their own ARN.
- **Aliases** (`dev`, `prod`, `live`) point to a version and can split traffic between two versions (weighted). Event sources and API Gateway stage variables should point to an alias, not to a version, so you can move the alias without reconfiguring callers.
- Environment variables (up to 4 KB total) are encrypted at rest with KMS (AWS managed key by default, or a CMK). For real secrets, read from Secrets Manager/Parameter Store at runtime.

## Concurrency and throttling
- Default account concurrency limit is **1,000 per Region** (soft, can be raised). One function using all of it throttles every other function.
- **Reserved concurrency**: guarantees and caps one function's concurrency (also used to protect a downstream DB). Setting it to 0 stops all invocations.
- **Provisioned concurrency**: pre-initialised environments, no cold starts. Can be scheduled/scaled with Application Auto Scaling.
- Throttled **synchronous** calls return **429** to the caller.
- Throttled **asynchronous** calls (and 5xx system errors): Lambda keeps the event and retries for up to **6 hours**, with backoff from about 1 second up to 5 minutes. Then it goes to the on-failure destination/DLQ if configured.
- **Cold start**: first request on a new environment loads code and runs init code outside the handler. Reduce with **provisioned concurrency** (the exam answer) and smaller packages.

## Storage options
| Option | Notes |
|---|---|
| `/tmp` | 512 MB default, up to 10 GB, per execution environment, not shared |
| Layers | Up to 5 layers, read-only, shared code/libraries |
| S3 | Durable objects, accessed through the API |
| **EFS** | Shared, persistent file system. Function must be **in a VPC**, uses an **EFS access point**. Watch EFS connection limits under high concurrency. **Cross-account EFS**: VPC peering/Transit Gateway between the VPCs, EFS file system policy allowing the other account, and Lambda role permissions to describe/mount |

---

[← Amazon ECS, EKS and Fargate](ecs-eks.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon API Gateway →](api-gateway.md)
