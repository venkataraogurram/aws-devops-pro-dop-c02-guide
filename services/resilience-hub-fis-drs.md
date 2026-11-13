[← AWS Backup](aws-backup.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon CloudWatch (metrics, alarms, logs, agent, synthetics) →](cloudwatch.md)

# Resilience Hub, FIS and Elastic Disaster Recovery

**Exam domains:** [Domain 3](../03-resilient-cloud.md) | **Hands-on:** none (read-only topic)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## AWS Elastic Disaster Recovery (DRS)

continuous block-level replication of servers (on-prem, other cloud, EC2) to a low-cost staging area in AWS; launch recovery instances in minutes (RPO seconds, RTO minutes); failback supported; non-disruptive **drills**. Pick it for "lift-and-shift servers DR with minimal RPO and low cost".

## AWS Resilience Hub

define the app (from CFN/ Terraform/ Resource groups/ EKS), set RTO/RPO **resiliency policy**, it **assesses** whether the architecture meets them, recommends fixes, generates CloudWatch alarms, SOPs (SSM docs) and **FIS experiments**. Runs in pipelines for continuous assessment.

## AWS Fault Injection Service (FIS)

chaos engineering. Experiment templates with actions (stop/terminate EC2, throttle API, inject CPU stress via SSM, fail AZ power interruption scenario, Aurora/RDS failover, ECS/EKS task kill, network disruption) with **stop conditions** = CloudWatch alarms. Use to **test** resilience and DR runbooks.

---

[← AWS Backup](aws-backup.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon CloudWatch (metrics, alarms, logs, agent, synthetics) →](cloudwatch.md)
