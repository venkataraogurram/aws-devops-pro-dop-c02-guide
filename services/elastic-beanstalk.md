[← EC2 Image Builder](ec2-image-builder.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon ECS, EKS and Fargate →](ecs-eks.md)

# AWS Elastic Beanstalk

**Exam domains:** [Domain 1](../01-sdlc-automation.md) | **Hands-on:** none (read-only topic)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## Elastic Beanstalk deployment policies (exam favourite)

| Policy | Behaviour | Downtime | Deploy time | Rollback |
|---|---|---|---|---|
| All at once | All instances updated together | Yes | Fastest | Manual redeploy |
| Rolling | Batch by batch on existing instances | No, reduced capacity | Medium | Manual redeploy |
| Rolling with additional batch | New batch launched first, full capacity kept | No | Longer | Manual redeploy |
| Immutable | New instances in a temporary ASG, then moved to original ASG | No | Longest | Terminate new instances (fast, safe) |
| Traffic splitting | Canary: new instances get X% of traffic for an evaluation time | No | Long | Automatic if health fails |
| Blue/green (not a policy) | Clone env, deploy, **Swap environment URLs** (CNAME swap) | No | - | Swap back |

Other Beanstalk must-knows:
- `.ebextensions/*.config` = YAML/JSON config (option_settings, packages, commands, container_commands, resources in CFN syntax). `container_commands` run after app is extracted, before deployment; `leader_only: true` runs on one instance (e.g., DB migrations).
- `.platform/hooks/` (prebuild, predeploy, postdeploy) and `.platform/nginx/` on Amazon Linux 2/2023 platforms.
- **Don't create the production RDS inside the Beanstalk environment** (it's deleted with the env). Create RDS separately and pass the endpoint via env properties / Secrets Manager. For blue/green, data tier must be outside.
- **Managed platform updates** in a weekly maintenance window (minor/patch), done as immutable.
- Worker environments + SQS + `cron.yaml` for periodic tasks.
- App version **lifecycle policy** (max count/age) to avoid hitting the application version quota.
- Saved configurations / `eb config` to clone envs.

## Environment tiers and notifications
- **Web server tier**: ELB + ASG serving HTTP. **Worker tier**: instances poll an SQS queue (the SQS daemon posts messages to your app); scales on queue depth; `cron.yaml` for periodic jobs. A web tier can offload long work to a worker tier through SQS.
- **Notifications**: EventBridge rules on Beanstalk events: environment operations (create/update/terminate start, success, fail), resource status (ASG/ELB/EC2 created/deleted), managed updates (started/failed), and **environment health status** changes -> SNS / Lambda. (Beanstalk can also send its own SNS email notifications.)

---

[← EC2 Image Builder](ec2-image-builder.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon ECS, EKS and Fargate →](ecs-eks.md)
