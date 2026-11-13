[← 9. 46-day study plan + exam-day checklist](09-study-plan.md) | [🏠 Home](README.md) | [11. Final cheat sheet →](11-final-cheat-sheet.md)

# Chapter 10 - Hands-on Labs (cheap, in your sandbox account)

> Use a non-production sandbox account. Delete resources after each lab. Most labs cost cents if you clean up the same day. Avoid leaving NAT gateways, ALBs, Aurora, or Global Accelerator running.

| Lab | What to build | What you learn | Time |
|---|---|---|---|
| **L1** | CodeCommit (or GitHub via CodeConnections) repo + CodeBuild project with a buildspec that runs unit tests, publishes a JUnit report, and reads a value from Parameter Store | buildspec phases, env secrets, reports, logs | 1 h |
| **L2** | CodePipeline V2: Source -> Build -> Manual approval -> Deploy to S3 static site. Add a trigger with a file path filter. Add an EventBridge rule -> SNS email on pipeline FAILED | Stages, approvals, triggers, notifications | 1.5 h |
| **L3** | CodeDeploy to 2 EC2 instances (ASG, tagged), agent installed via SSM State Manager, appspec with hooks. Break `ValidateService` on purpose and watch the rollback. Then try blue/green | Hooks, agent, logs, rollback | 2 h |
| **L4** | SAM Lambda with `AutoPublishAlias` + `Canary10Percent5Minutes` + an alarm. Deploy v2 with an error and watch the rollback in CodeDeploy | Lambda traffic shifting | 1 h |
| **L5** | CFN template: parameters, mappings, conditions, outputs/exports, a second stack with `ImportValue`. Create a change set that renames a bucket (see the "Replacement" flag). Set a stack policy and try the update | Change sets, replacement, stack policy | 1.5 h |
| **L6** | EC2 with `cfn-init` + `cfn-signal` + CreationPolicy. Break a package name and watch CREATE_FAILED. Add cfn-hup and update metadata. Run drift detection after a manual SG change | Bootstrapping, signals, drift | 1.5 h |
| **L7** | `cdk init` a small stack (S3 + Lambda with `grantRead`), `cdk diff`, `cdk deploy`, look at the synthesized template | L2 constructs, bootstrap | 1 h |
| **L8** | SSM: Session Manager into an instance with no SSH port. Run Command with rate control. State Manager association for the CloudWatch agent. Patch Manager scan. Inventory | Fleet management end to end | 2 h |
| **L9** | AWS Config: enable a managed rule `restricted-ssh` with auto remediation `AWS-DisablePublicAccessForSecurityGroup`. Open port 22 to the world and watch it get fixed | Detect + auto-remediate | 1 h |
| **L10** | Route 53 failover (if you own a test domain) with a health check, or read the console flow. S3 CRR between two Regions | Failover, replication | 1 h |
| **L11** | ASG with target tracking + lifecycle hook + instance refresh. Change the health check type to ELB | Scaling and health checks | 1.5 h |
| **L12** | CloudWatch Logs: metric filter on JSON logs -> alarm -> SNS. Logs Insights queries. Subscription filter -> Lambda | Logs pipeline | 1 h |
| **L13** | Lambda + API Gateway with X-Ray on. Add an annotation and search for it. CloudWatch Synthetics heartbeat canary | Tracing, synthetics | 1 h |
| **L14** | EventBridge rule on EC2 state change -> SNS. Custom bus + `PutEvents`. SQS with DLQ, `maxReceiveCount` 3, a failing Lambda consumer | Events and failure handling | 1 h |
| **L15** | Create a CFN stack that fails (bad AMI ID) and practise finding the first FAILED event. Run an ECS task with a wrong image and read the stopped reason | Troubleshooting | 45 min |
| **L16** | IAM: role with a permissions boundary. Test with the IAM policy simulator. An ABAC policy with tags. Access Analyzer policy validation | IAM evaluation | 1 h |
| **L17** | Enable GuardDuty (30-day trial) + Security Hub (30-day trial) + Inspector (15-day trial) and generate GuardDuty **sample findings**. Build an EventBridge rule on GuardDuty findings -> SNS | Detection + response | 1 h |

**Cleanup checklist after every lab:** delete CFN stacks, empty and delete S3 buckets, terminate EC2/ASGs, delete NAT gateways/ALBs, disable trials you don't need, check **Billing > Bills** the next day.

---

[← 9. 46-day study plan + exam-day checklist](09-study-plan.md) | [🏠 Home](README.md) | [11. Final cheat sheet →](11-final-cheat-sheet.md)
