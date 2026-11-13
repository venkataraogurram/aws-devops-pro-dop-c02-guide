[← 8. 60 practice questions](08-practice-questions.md) | [🏠 Home](README.md) | [10. Hands-on labs →](10-hands-on-labs.md)

# Chapter 9 - 46-Day Study Plan (Nov 14 - Dec 29, 2026)

> Plan: **weekdays ~3 hours**, **weekends ~6 hours** (about 175 hours total). Move days around your shifts. Don't skip the review and mock days.

## 9.1 How to study each chapter (method)
1. **Read** the chapter section once fully (don't take notes yet).
2. **Do the lab** for that topic ([Chapter 10 - Labs](10-hands-on-labs.md)). Even 30 minutes in the console fixes a concept better than 3 re-reads.
3. **Cover the quick-map table** at the end of the chapter and answer each scenario from memory.
4. **Practice questions** for that domain (Chapter 8 + your practice exam bank).
5. For every wrong answer, write one line in a **[mistakes log](mistakes-log.md)**: *the trap -> the rule*. Re-read the log every morning.

## 9.2 Day-by-day plan

### Week 1 (Nov 14-20): Exam strategy + Domain 1 SDLC (22%)
| Day | Date | Topics | Lab |
|---|---|---|---|
| 1 | Sat Nov 14 | Ch 0 (strategy). Take the **free official practice question set** on Skill Builder as a baseline. Ch 1.1-1.3 (pipeline concepts, CodeCommit, CodeBuild) | [L1](10-hands-on-labs.md) |
| 2 | Sun Nov 15 | Ch 1.4-1.6 (artifacts, Image Builder, CodePipeline incl. cross-account) | [L2](10-hands-on-labs.md) |
| 3 | Mon Nov 16 | Ch 1.7 CodeDeploy: AppSpec, hooks order, configs | [L3](10-hands-on-labs.md) |
| 4 | Tue Nov 17 | Ch 1.7 cont.: agent, rollbacks, troubleshooting table. Memorise the hook order | - |
| 5 | Wed Nov 18 | Ch 1.8 deployment strategies: Beanstalk policies, ECS, Lambda/SAM, API GW | [L4](10-hands-on-labs.md) |
| 6 | Thu Nov 19 | Ch 1.9-1.10 secrets + quick-map. Q1-Q12 | - |
| 7 | Fri Nov 20 | Domain 1 practice set (30+ questions from your bank). Mistakes log | - |

### Week 2 (Nov 21-27): Domain 2 Configuration Management and IaC (17%)
| Day | Date | Topics | Lab |
|---|---|---|---|
| 8 | Sat Nov 21 | Ch 2.1-2.2 CloudFormation: template, functions, dynamic refs, stack lifecycle tools | [L5](10-hands-on-labs.md) |
| 9 | Sun Nov 22 | Ch 2.2 cont.: helper scripts, CreationPolicy, UpdatePolicy, multi-stack, StackSets, custom resources, Hooks, errors | [L6](10-hands-on-labs.md) |
| 10 | Mon Nov 23 | Ch 2.3 SAM + CDK; Ch 2.4 AppConfig | [L7](10-hands-on-labs.md) |
| 11 | Tue Nov 24 | Ch 2.5 Systems Manager (all capabilities) | [L8](10-hands-on-labs.md) |
| 12 | Wed Nov 25 | Ch 2.6-2.7 Organizations, SCPs, Control Tower | - |
| 13 | Thu Nov 26 | Ch 2.8-2.11 Config, Service Catalog, Step Functions, quick-map. Q13-Q24 | [L9](10-hands-on-labs.md) |
| 14 | Fri Nov 27 | Domain 2 practice set. Re-read mistakes log for D1 + D2 | - |

### Week 3 (Nov 28 - Dec 4): Domain 3 Resilience (15%) + Domain 4 Monitoring (15%)
| Day | Date | Topics | Lab |
|---|---|---|---|
| 15 | Sat Nov 28 | Ch 3.1-3.3 DR strategies, Multi-AZ/multi-Region per service, Route 53, CloudFront, Global Accelerator | [L10](10-hands-on-labs.md) |
| 16 | Sun Nov 29 | Ch 3.4-3.6 Auto Scaling deep dive, other scaling, decoupling, backups. Q25-Q35 | [L11](10-hands-on-labs.md) |
| 17 | Mon Nov 30 | Domain 3 practice set | - |
| 18 | Tue Dec 1 | Ch 4.1-4.3 metrics, alarms, Logs, filter syntax, Logs Insights, real-time pipelines | [L12](10-hands-on-labs.md) |
| 19 | Wed Dec 2 | Ch 4.4-4.7 CloudWatch agent, dashboards, X-Ray, Synthetics | [L13](10-hands-on-labs.md) |
| 20 | Thu Dec 3 | Ch 4.8-4.12 CloudTrail, other logs, log security/lifecycle, quick-map. Q36-Q45 | - |
| 21 | Fri Dec 4 | Domain 4 practice set | - |

### Week 4 (Dec 5-11): Domain 5 Incident (14%) + Domain 6 Security (17%)
| Day | Date | Topics | Lab |
|---|---|---|---|
| 22 | Sat Dec 5 | Ch 5.1-5.3 EventBridge, Health, SQS/SNS/Kinesis/Lambda failure handling | [L14](10-hands-on-labs.md) |
| 23 | Sun Dec 6 | Ch 5.4-5.7 auto-remediation, troubleshooting tables, quick-map. Q46-Q54 | [L15](10-hands-on-labs.md) |
| 24 | Mon Dec 7 | Ch 6.1 IAM (evaluation logic, conditions, ABAC, boundaries, STS) | [L16](10-hands-on-labs.md) |
| 25 | Tue Dec 8 | Ch 6.2-6.3 secrets, KMS, CloudHSM, ACM, Macie | - |
| 26 | Wed Dec 9 | Ch 6.4-6.5 network security, detection services | [L17](10-hands-on-labs.md) |
| 27 | Thu Dec 10 | Ch 6.6-6.7 security at scale, quick-map. Q55-Q60 | - |
| 28 | Fri Dec 11 | Domain 5 + 6 practice sets | - |

### Week 5 (Dec 12-18): Consolidate + first full mocks
| Day | Date | Plan |
|---|---|---|
| 29 | Sat Dec 12 | **Full mock exam 1** (75 Q, 180 min, timed, no notes). Review **all** explanations (3 h) |
| 30 | Sun Dec 13 | Ch 7 comparisons + numbers. Re-study the weakest domain from mock 1 |
| 31 | Mon Dec 14 | Re-study 2nd weakest domain. Redo Chapter 8 questions you got wrong |
| 32 | Tue Dec 15 | CloudFormation + CodeDeploy + SSM revision (highest-frequency services) |
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

[← 8. 60 practice questions](08-practice-questions.md) | [🏠 Home](README.md) | [10. Hands-on labs →](10-hands-on-labs.md)
