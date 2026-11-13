[🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [1. Domain 1: SDLC Automation (22%) →](01-sdlc-automation.md)

# Chapter 0 - Exam Facts and Strategy

## 0.1 Exam facts (from the official DOP-C02 exam guide)

| Item | Value |
|---|---|
| Exam code | DOP-C02 (AWS Certified DevOps Engineer - Professional) |
| Questions | 75 total = 65 scored + 10 unscored (unscored ones are not marked) |
| Time | 180 minutes (about 2.4 minutes per question) |
| Question types | Multiple choice (1 of 4) and multiple response (2+ of 5+) |
| Score | Scaled 100-1000, pass = **750** |
| Scoring model | Compensatory: you need to pass the exam overall, not each domain |
| Guessing | No penalty. **Never leave a question blank.** |
| Validity | 3 years |

### Domain weights (plan your study time by these)

| # | Domain | Weight | Approx. scored questions |
|---|---|---|---|
| 1 | SDLC Automation | 22% | ~14 |
| 2 | Configuration Management and IaC | 17% | ~11 |
| 3 | Resilient Cloud Solutions | 15% | ~10 |
| 4 | Monitoring and Logging | 15% | ~10 |
| 5 | Incident and Event Response | 14% | ~9 |
| 6 | Security and Compliance | 17% | ~11 |

Domains 1 + 2 + 6 = 56% of the exam. CodePipeline/CodeBuild/CodeDeploy, CloudFormation, Systems Manager, Organizations/Control Tower, IAM/KMS and EventBridge show up across almost every domain.

### ESL accommodation (do this today if you have not)

Non-native English speakers can request the **"ESL +30 minutes"** accommodation in your AWS Certification account (Certmetrics > Request Exam Accommodations). That turns 180 minutes into 210. Request it before the exam. If your exam is already scheduled when it is approved, check whether the extra time is applied to the existing booking; if not, reschedule the same slot so the accommodation attaches. Verify this yourself in the portal, the rules may change.

### What is NOT on the exam (from the official guide)
The guide says the target candidate is **not** expected to:
- have advanced networking knowledge (advanced routing algorithms, failover techniques);
- give deep-level security recommendations to developers;
- design, query or tune the performance of databases;
- develop full-stack application code.

So this repo covers networking and databases only as far as DevOps questions need them: high availability, replication, failover, backups, scaling, security groups/NACLs. It doesn't cover routing protocols, SQL tuning or application code.

**How this repo decides what to keep:** a topic stays if it is on the official in-scope services list, is named in a task statement, or is in the "Technologies and Concepts" list. One exception: a non-listed service stays as a short note if it regularly appears as an answer option in DOP-C02 style questions (**Global Accelerator**, **Firewall Manager**, and the Glue Data Catalog behind Athena tables).

## 0.2 How DOP-C02 questions are written

- Long scenarios (5-10 lines), 4-5 long answer options that differ in 1-2 words.
- Almost every question has a **qualifier**. The qualifier decides the answer:

| Qualifier in question | What it usually points to |
|---|---|
| "LEAST operational overhead" / "LEAST management effort" | Fully managed / native feature over custom scripts, Lambda, cron jobs or EC2 |
| "MOST cost-effective" | Fewest always-on resources; serverless; backup and restore over warm standby |
| "MINIMUM downtime" / "zero downtime" | Blue/green, immutable, traffic shifting, Route 53 weighted, CNAME swap |
| "As quickly as possible" / "fastest recovery" | Already-running resources (warm standby, multi-site, Aurora Global DB) |
| "Near real time" | EventBridge, Kinesis, CloudWatch Logs subscription filters (not S3 export, not CloudTrail to S3 + Athena) |
| "Must be auditable" / "prove" | CloudTrail (with log file validation), AWS Config history |
| "Prevent" | SCP / RCP, IAM deny, Control Tower preventive control, permission boundary, CFN Hook, stack policy |
| "Detect" | AWS Config rule, GuardDuty, Security Hub, Access Analyzer, Control Tower detective control |
| "Automatically remediate" | Config rule + SSM Automation remediation, or EventBridge rule + Lambda / SSM Automation |
| "Across all accounts in the organization" | Organizations + delegated admin + StackSets (service-managed) / org trail / Config aggregator / org conformance pack |
| "Without SSH / bastion" | Systems Manager Session Manager / Run Command |
| "Rollback automatically" | CodeDeploy alarms + auto-rollback, CFN rollback triggers, ECS circuit breaker, AppConfig alarm rollback |

### Answer-elimination rules that work on this exam

1. **Custom code loses to a native feature.** If one option writes a Lambda function to poll something every 5 minutes, and another uses a built-in integration (EventBridge rule, Config managed rule, CodeDeploy auto-rollback), pick the built-in one.
2. **Cron on EC2 almost never wins.** Use EventBridge Scheduler / EventBridge rule schedule / SSM Maintenance Window / State Manager.
3. **Manual steps lose** when the question asks for automation ("the team logs in and runs...").
4. **Long-term access keys on instances or in code = wrong.** Use IAM roles, instance profiles, IRSA / EKS Pod Identity, task roles.
5. **Secrets in environment variables in plain text / in the repo = wrong.** Use Secrets Manager or Parameter Store SecureString.
6. **"Polling CloudTrail logs in S3"** is slower than EventBridge rule on the CloudTrail event.
7. **Options that break something already required** ("disable encryption", "make the bucket public", "open 0.0.0.0/0") are distractors.
8. For multi-response questions, the correct options usually **work together** (one sets up the source, the other the action). Check that each picked option is true on its own.
9. If two answers both work, re-read the qualifier and choose by overhead, cost or speed.

## 0.3 Time strategy on exam day

- First pass: answer everything, max ~2 minutes each. If unsure, pick your best guess, **flag** it, move on.
- Aim to finish the first pass with 40+ minutes left.
- Second pass: only flagged questions. Don't change an answer without a concrete reason.
- Read the **last sentence first** (the actual ask + qualifier), then the scenario.
- Underline mentally: number of accounts/Regions, RTO/RPO values, "existing" resources, compliance words.

## 0.4 Service status changes (2024-2026) you should know

The exam question bank was written over several years. Some services in it have changed status. Answer from the exam's point of view, but know the facts:

| Service | Status | Exam impact |
|---|---|---|
| AWS CodeCommit | Closed to new customers July 2024, **returned to full general availability on Nov 24, 2025**. Widely used in questions. | Know it as a Git source for CodePipeline, triggers, EventBridge events, approval rule templates, IAM-based access. |
| AWS CodeStar | Discontinued (July 2024) | Rarely the right answer now. |
| AWS OpsWorks (Chef/Puppet) | End of life (May 2024) | Still in the in-scope list. Know: Chef/Puppet managed config management; today the answer is usually Systems Manager. |
| Amazon Inspector Classic | Replaced by Inspector (v2) | Exam guide still says "assessment templates" (Classic). Inspector v2 scans EC2, ECR images and Lambda continuously, no templates. |
| AWS Proton | Closed to new customers Oct 7, 2025; **support ends Oct 7, 2026** | Know what it is (platform team templates for environments + services). Rarely the right answer now. |
| SSM Change Manager | Closed to new customers from **Nov 7, 2025** | Know the concept (change requests + approvals). Change Calendar is still a normal SSM feature. |
| AWS Chatbot | Renamed **Amazon Q Developer in chat applications** (Feb 2025) | Questions may still say "Chatbot": SNS -> Slack/Teams notifications. |
| Amazon ECS native blue/green | ECS added built-in blue/green (2025) plus linear/canary without CodeDeploy | Most exam questions still expect **CodeDeploy** for ECS blue/green. |
| AWS App Runner | Closed to new customers from **Apr 30, 2026**; AWS now recommends **Amazon ECS Express Mode** | Still in the in-scope list. Know it as "simplest managed web app from source/image". |
| SSM Incident Manager | Closed to new customers from **Nov 7, 2025** | Know the concept: response plans, contacts, escalation, runbooks. |
| Security Hub | Original product renamed **Security Hub CSPM**; a new unified Security Hub launched in 2025 | Questions refer to "Security Hub" findings, standards, aggregation. Same concepts. |

If a question offers a discontinued service and a current managed service that does the same job, prefer the current one.

## 0.5 Recommended extra resources (all official or widely used)

- Official exam guide: https://docs.aws.amazon.com/aws-certification/latest/devops-engineer-professional-02/devops-engineer-professional-02.html
- AWS Skill Builder: **"AWS Certified DevOps Engineer - Professional Official Practice Question Set"** (free, 20 questions) and the **Official Practice Exam** (subscription). Take the free set in week 1 as a baseline.
- AWS whitepapers to skim: "Practicing Continuous Integration and Continuous Delivery on AWS", "Blue/Green Deployments on AWS", "Disaster Recovery of Workloads on AWS", "Organizing Your AWS Environment Using Multiple Accounts", "Infrastructure as Code".
- A third-party practice exam bank (Tutorials Dojo / similar) for weeks 5-6. Do at least **3 full timed mocks** before Dec 29 and read every explanation, including for the ones you got right.

---

[🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [1. Domain 1: SDLC Automation (22%) →](01-sdlc-automation.md)
