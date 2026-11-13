# AWS Certified DevOps Engineer - Professional (DOP-C02) Study Guide

**Version:** v2.0 (Nov 2026) | **Exam:** Tue, Dec 29, 2026

Complete DOP-C02 material in one repo:
- **service notes**, one file per service;
- **domain chapters** with the exam's cross-service scenarios;
- **step-by-step labs** with templates;
- **60 practice questions** and a **46-day plan**.

Built from the official [DOP-C02 exam guide](https://docs.aws.amazon.com/aws-certification/latest/devops-engineer-professional-02/devops-engineer-professional-02.html) (all 6 domains, every task statement, the in-scope services list). Facts checked against AWS documentation as of Nov 2026.

## Start here
1. Read [Chapter 0](00-exam-strategy.md): the exam format and how to read questions.
2. Follow the [46-day study plan](09-study-plan.md), one row per day. Each row links the service files and the lab for that day.
3. Study from the **[services](services/README.md)** folder: concepts, must-knows and traps per service.
4. Then read the **domain chapter** (01-06). It says what the domain tests and has the "scenario → answer" quick-map.
5. Do the matching **[lab](labs/README.md)** in a sandbox account.
6. Log every wrong practice answer in the [mistakes log](mistakes-log.md).
7. Last week: [Chapter 7](07-service-comparisons-numbers.md), the [cheat sheet](11-final-cheat-sheet.md), and your mistakes log.

## Repo layout
| Folder / file | What's inside |
|---|---|
| [services/](services/README.md) | 42 service files grouped by area (CI/CD, compute, IaC, governance, resilience, monitoring, security) |
| `00`-`11` chapters | Strategy, 6 domain chapters, comparisons, practice questions, plan, labs index, cheat sheet |
| [labs/](labs/README.md) | 16 practical labs: CloudFormation/SAM templates, code, CLI steps, "break it" exercises, cleanup |
| [mistakes-log.md](mistakes-log.md) | Your personal trap -> rule log |

## Chapters
| Chapter |
|---|
| [0. Exam facts and strategy](00-exam-strategy.md) |
| [1. Domain 1: SDLC Automation (22%)](01-sdlc-automation.md) |
| [2. Domain 2: Configuration Management and IaC (17%)](02-config-mgmt-iac.md) |
| [3. Domain 3: Resilient Cloud Solutions (15%)](03-resilient-cloud.md) |
| [4. Domain 4: Monitoring and Logging (15%)](04-monitoring-logging.md) |
| [5. Domain 5: Incident and Event Response (14%)](05-incident-event-response.md) |
| [6. Domain 6: Security and Compliance (17%)](06-security-compliance.md) |
| [7. "Which one?" comparisons + numbers](07-service-comparisons-numbers.md) |
| [8. 60 practice questions](08-practice-questions.md) |
| [9. 46-day study plan + exam-day checklist](09-study-plan.md) |
| [10. Hands-on labs](10-hands-on-labs.md) |
| [11. Final cheat sheet](11-final-cheat-sheet.md) |
| [My mistakes log](mistakes-log.md) |

Diagrams use Mermaid and render on GitHub. Practice answers are hidden behind "Answer" toggles.
