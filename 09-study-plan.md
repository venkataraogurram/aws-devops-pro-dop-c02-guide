[← 8. 60 practice questions](08-practice-questions.md) | [🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [10. Hands-on labs →](10-hands-on-labs.md)

# Chapter 9 - 46-Day Study Plan (Nov 14 - Dec 29, 2026)

> Plan: **weekdays ~3 hours**, **weekends ~6 hours** (about 175 hours total). Move days around your shifts. Don't skip the review and mock days.

## 9.1 How to study each chapter (method)
1. **Read** the chapter section once fully (don't take notes yet).
2. **Do the lab** for that topic ([labs folder](labs/README.md)). Even 30 minutes in the console fixes a concept better than 3 re-reads.
3. **Cover the quick-map table** at the end of the chapter and answer each scenario from memory.
4. **Practice questions** for that domain (Chapter 8 + your practice exam bank).
5. For every wrong answer, write one line in a **[mistakes log](mistakes-log.md)**: *the trap -> the rule*. Re-read the log every morning.

## 9.2 Day-by-day plan

### Week 1 (Nov 14-20): Exam strategy + Domain 1 SDLC (22%)
| Day | Date | Topics | Lab |
|---|---|---|---|
| 1 | Sat Nov 14 | [Ch 0](00-exam-strategy.md) strategy. Take the **free official practice question set** on Skill Builder as a baseline. [Ch 1](01-sdlc-automation.md) big picture, [CodeCommit](services/codecommit.md), [CodeBuild](services/codebuild.md) | [Lab 01](labs/01-codebuild-codepipeline/README.md) steps 1-4 |
| 2 | Sun Nov 15 | [CodePipeline](services/codepipeline.md) (incl. cross-account), [CodeArtifact](services/codeartifact.md), [ECR](services/ecr.md), [Image Builder](services/ec2-image-builder.md), [Amplify](services/amplify.md) | [Lab 01](labs/01-codebuild-codepipeline/README.md) steps 5-7, [Lab 04](labs/04-ecs-circuit-breaker/README.md) step 3 |
| 3 | Mon Nov 16 | [CodeDeploy](services/codedeploy.md): AppSpec, hook order, configs | [Lab 02](labs/02-codedeploy-ec2-rollback/README.md) |
| 4 | Tue Nov 17 | [CodeDeploy](services/codedeploy.md) again: agent, rollbacks, troubleshooting. Memorise the hook order | - |
| 5 | Wed Nov 18 | [Ch 1](01-sdlc-automation.md) deployment strategies, [Elastic Beanstalk](services/elastic-beanstalk.md), [ECS/EKS](services/ecs-eks.md), [Lambda](services/lambda.md), [API Gateway](services/api-gateway.md) | [Lab 03](labs/03-sam-lambda-canary/README.md), [Lab 04](labs/04-ecs-circuit-breaker/README.md) |
| 6 | Thu Nov 19 | [Secrets](services/secrets-manager-parameter-store.md) + Domain 1 quick-map. Q1-Q12 | - |
| 7 | Fri Nov 20 | Domain 1 practice set (30+ questions from your bank). Mistakes log | - |

### Week 2 (Nov 21-27): Domain 2 Configuration Management and IaC (17%)
| Day | Date | Topics | Lab |
|---|---|---|---|
| 8 | Sat Nov 21 | [CloudFormation](services/cloudformation.md) part 1: template, functions, dynamic refs, stack lifecycle tools | [Lab 05](labs/05-cloudformation-signals-changesets-drift/README.md) |
| 9 | Sun Nov 22 | [CloudFormation](services/cloudformation.md) part 2: helper scripts, UpdatePolicy, multi-stack, StackSets, custom resources, hooks, errors | [Lab 06](labs/06-stacksets-multi-region/README.md) |
| 10 | Mon Nov 23 | [SAM and CDK](services/sam-cdk.md), [AppConfig](services/appconfig.md), [Step Functions](services/step-functions.md), [Ch 2](02-config-mgmt-iac.md) | - |
| 11 | Tue Nov 24 | [Systems Manager](services/systems-manager.md) (all capabilities) | [Lab 07](labs/07-systems-manager-fleet/README.md) |
| 12 | Wed Nov 25 | [Organizations and SCPs](services/organizations.md), [Control Tower](services/control-tower.md) | [Lab 15](labs/15-organizations-scp/README.md) (optional) |
| 13 | Thu Nov 26 | [AWS Config](services/config.md), [Service Catalog](services/service-catalog.md), Domain 2 quick-map. Q13-Q24 | [Lab 08](labs/08-config-auto-remediation/README.md) |
| 14 | Fri Nov 27 | Domain 2 practice set. Re-read mistakes log for D1 + D2 | - |

### Week 3 (Nov 28 - Dec 4): Domain 3 Resilience (15%) + Domain 4 Monitoring (15%)
| Day | Date | Topics | Lab |
|---|---|---|---|
| 15 | Sat Nov 28 | [Ch 3](03-resilient-cloud.md) DR strategies, [Databases and storage](services/databases-storage.md), [S3](services/s3.md), [Route 53](services/route53.md), [CloudFront/GA](services/cloudfront-global-accelerator.md) | [Lab 16](labs/16-multi-region-dr/README.md) |
| 16 | Sun Nov 29 | [Auto Scaling](services/ec2-auto-scaling.md), [ELB](services/elastic-load-balancing.md), [AWS Backup](services/aws-backup.md), [Resilience Hub/FIS/DRS](services/resilience-hub-fis-drs.md). Q25-Q35 | [Lab 12](labs/12-auto-scaling-lifecycle-hooks/README.md) |
| 17 | Mon Nov 30 | Domain 3 practice set | - |
| 18 | Tue Dec 1 | [CloudWatch](services/cloudwatch.md): metrics, alarms, Logs, filter syntax, Logs Insights, agent | [Lab 09](labs/09-cloudwatch-logs-alarms/README.md) |
| 19 | Wed Dec 2 | [X-Ray](services/xray.md), CloudWatch Synthetics, [Athena/Glue/QuickSight](services/analytics-athena-glue-quicksight.md) | [Lab 10](labs/10-xray-api-gateway-lambda/README.md) |
| 20 | Thu Dec 3 | [CloudTrail](services/cloudtrail.md), [Ch 4](04-monitoring-logging.md) other logs, log security, quick-map. Q36-Q45 | - |
| 21 | Fri Dec 4 | Domain 4 practice set | - |

### Week 4 (Dec 5-11): Domain 5 Incident (14%) + Domain 6 Security (17%)
| Day | Date | Topics | Lab |
|---|---|---|---|
| 22 | Sat Dec 5 | [EventBridge](services/eventbridge.md), [Health](services/health.md), [SQS/SNS/Kinesis](services/sqs-sns-kinesis.md) | [Lab 11](labs/11-eventbridge-sqs-dlq/README.md) |
| 23 | Sun Dec 6 | [Ch 5](05-incident-event-response.md) auto-remediation, troubleshooting tables, quick-map. Q46-Q54 | [Lab 04](labs/04-ecs-circuit-breaker/README.md) step 2, [Lab 05](labs/05-cloudformation-signals-changesets-drift/README.md) step 2 |
| 24 | Mon Dec 7 | [IAM, STS, Identity Center](services/iam-sts-identity-center.md) | [Lab 13](labs/13-iam-boundary-abac/README.md) |
| 25 | Tue Dec 8 | [KMS/CloudHSM](services/kms-cloudhsm.md), [ACM](services/acm.md), [Secrets Manager](services/secrets-manager-parameter-store.md) | - |
| 26 | Wed Dec 9 | [Network security](services/network-security.md), [Detection services](services/security-detection.md) | [Lab 14](labs/14-guardduty-security-response/README.md) |
| 27 | Thu Dec 10 | [Ch 6](06-security-compliance.md) threats/controls, security at scale, quick-map. Q55-Q60 | - |
| 28 | Fri Dec 11 | Domain 5 + 6 practice sets | - |

### Week 5 (Dec 12-18): Consolidate + first full mocks
| Day | Date | Plan |
|---|---|---|
| 29 | Sat Dec 12 | **Full mock exam 1** (75 Q, 180 min, timed, no notes). Review **all** explanations (3 h) |
| 30 | Sun Dec 13 | Ch 7 comparisons + numbers. Re-study the weakest domain from mock 1 |
| 31 | Mon Dec 14 | Re-study 2nd weakest domain. Redo Chapter 8 questions you got wrong |
| 32 | Tue Dec 15 | [CloudFormation](services/cloudformation.md) + [CodeDeploy](services/codedeploy.md) + [SSM](services/systems-manager.md) revision (highest-frequency services) |
| 33 | Wed Dec 16 | Security + Organizations/Control Tower revision |
| 34 | Thu Dec 17 | Monitoring + EventBridge patterns revision |
| 35 | Fri Dec 18 | 40-question timed domain-mixed set |

### Week 6 (Dec 19-25): Mocks 2 and 3
| Day | Date | Plan |
|---|---|---|
| 36 | Sat Dec 19 | **Full mock 2** + full review |
| 37 | Sun Dec 20 | Fix weak areas from mock 2. All quick-map tables |
| 38 | Mon Dec 21 | DR/resilience + scaling revision. Lifecycle hook orders again |
| 39 | Tue Dec 22 | Official Skill Builder practice exam (if you have access) or mock 3 |
| 40 | Wed Dec 23 | Review mock 3. Mistakes log end to end |
| 41 | Thu Dec 24 | Chapter 7 + [Chapter 11 cheat sheet](11-final-cheat-sheet.md) |
| 42 | Fri Dec 25 | **Full mock 4** (target 80%+) |

### Final days
| Day | Date | Plan |
|---|---|---|
| 43 | Sat Dec 26 | Review mock 4. Weakest 2 topics only |
| 44 | Sun Dec 27 | [Chapter 11 cheat sheet](11-final-cheat-sheet.md), all quick-maps, mistakes log |
| 45 | Mon Dec 28 | **Light day**: cheat sheet once, Chapter 0 strategy. Check exam ID/location/online-proctor setup. Sleep early |
| 46 | **Tue Dec 29** | **EXAM.** Read the cheat sheet once in the morning. No new topics |

**Target before booking-confirmation day (Dec 22):** 75%+ on mocks consistently. If you are below 65% on Dec 22, consider rescheduling (AWS allows rescheduling up to 24 hours before the appointment; check your Pearson VUE terms).

## 9.3 Exam-day checklist
- [ ] Online: system test done a day before, clean desk, ID ready, webcam works, no second monitor. Test centre: arrive 30 min early with 2 IDs if required.
- [ ] ESL +30 min accommodation applied (check on the confirmation).
- [ ] Sleep 7+ hours. Light food, water.
- [ ] Strategy: read the last line first, find the qualifier, eliminate 2 options, flag and move on after ~2 min.
- [ ] Answer every question. No penalty for guessing.

---

[← 8. 60 practice questions](08-practice-questions.md) | [🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [10. Hands-on labs →](10-hands-on-labs.md)
