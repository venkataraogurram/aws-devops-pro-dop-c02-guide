[← CloudFront and Global Accelerator](cloudfront-global-accelerator.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Resilience Hub, FIS and Elastic Disaster Recovery →](resilience-hub-fis-drs.md)

# AWS Backup

**Exam domains:** [Domain 3](../03-resilient-cloud.md) | **Hands-on:** none (read-only topic)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

**AWS Backup**
- **Backup plans** (schedule, lifecycle: transition to cold storage, retention), **backup rules**, **resource assignment** by tags or ARNs.
- Supports EC2/EBS, RDS, Aurora, DynamoDB, EFS, FSx, S3, Storage Gateway, DocumentDB, Neptune, Redshift, Timestream, SAP HANA on EC2, VMware...
- **Cross-Region copy** and **cross-account copy** (within org) in the plan's copy action.
- **Vault Lock** (WORM: governance or compliance mode) - backups can't be deleted even by root -> ransomware protection. **Logically air-gapped vault**.
- **Organization backup policies** to apply plans to all accounts.
- **Restore testing** plans (automatic periodic restore validation).
- EventBridge events for job state (failed backups -> SNS).

**Service-native backups:** RDS automated backups (1-35 days, PITR to 5-min granularity) + manual snapshots (kept until deleted); DynamoDB PITR; EBS snapshots with DLM; S3 versioning + Object Lock + replication; Aurora **Backtrack** (MySQL, rewind in place without restore).

**Recovery procedures (automate them):** SSM Automation runbooks to restore/promote, CFN templates for DR stack, Route 53 failover records, regular **DR drills** with FIS / Aurora switchover / DRS drills.

---

[← CloudFront and Global Accelerator](cloudfront-global-accelerator.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Resilience Hub, FIS and Elastic Disaster Recovery →](resilience-hub-fis-drs.md)
