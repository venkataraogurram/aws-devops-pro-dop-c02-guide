[← SQS, SNS, Kinesis, Firehose and Lambda event handling](sqs-sns-kinesis.md) | [Services index](README.md) | [🏠 Home](../README.md) | [IAM, STS and IAM Identity Center →](iam-sts-identity-center.md)

# Athena, Glue and QuickSight (log analytics)

**Exam domains:** [Domain 4](../04-monitoring-logging.md) | **Hands-on:** none (read-only topic)

> These show up as the "analyse logs in S3" and "build a dashboard" answers. Exam scenarios are in the Domain 4 quick-map.

## Amazon Athena
- Serverless **SQL queries directly on data in S3** (CSV, JSON, Parquet, ORC, Avro). Pay per TB scanned. Uses the **Glue Data Catalog** for table definitions.
- Typical exam data: **CloudTrail logs, ALB/ELB access logs, VPC Flow Logs, S3 access logs, CloudFront logs** stored in S3. CloudTrail and VPC Flow Logs consoles can create the Athena table for you.
- **Make it faster and cheaper** (fewer bytes scanned):
  - use a **columnar format** (Parquet or ORC), e.g., convert with Glue or with Firehose record format conversion;
  - **compress** the data (gzip, Snappy, ZSTD);
  - **partition** by columns you filter on (e.g., `year/month/day`), and use partition projection;
  - use **larger files** (about 128 MB+) instead of many tiny files.
- **Federated query**: query other sources (DynamoDB, RDS/Aurora, Redshift, CloudWatch Logs, on-prem DBs) through Lambda-based data source connectors, and join them with S3 data.
- Results can feed **QuickSight** dashboards.

## AWS Glue
- Serverless ETL service. **Crawlers** scan S3 (or databases), infer schemas and create tables in the **Glue Data Catalog** (the central metadata store used by Athena, Redshift Spectrum, EMR).
- **Glue ETL jobs** (Spark or Python shell) transform data, e.g., convert CSV/JSON logs into **Parquet** for Athena. Can be triggered on a schedule or by events.
- Also: Glue DataBrew (visual data preparation), Glue Studio (visual ETL), job bookmarks (process only new data).

## Amazon QuickSight (Quick Sight)
- Serverless **BI dashboards**, with ML insights and pay-per-session pricing. In-memory engine **SPICE** for fast dashboards.
- Data sources: Athena, S3, Redshift, RDS/Aurora, OpenSearch, third-party SaaS. Exam use: dashboards over Athena queries on CloudTrail/Config/Inventory/CUR data for management.
- Users/groups with row-level and column-level security; embed dashboards in apps.

---

[← SQS, SNS, Kinesis, Firehose and Lambda event handling](sqs-sns-kinesis.md) | [Services index](README.md) | [🏠 Home](../README.md) | [IAM, STS and IAM Identity Center →](iam-sts-identity-center.md)
