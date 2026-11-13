[← AWS X-Ray](xray.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon EventBridge →](eventbridge.md)

# AWS CloudTrail

**Exam domains:** [Domain 4](../04-monitoring-logging.md), [Domain 6](../06-security-compliance.md) | **Hands-on:** [Lab 14](../labs/14-guardduty-security-response/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

| Concept | Detail |
|---|---|
| **Event history** | Last **90 days** of **management events** free, per Region, no setup |
| **Trail** | Deliver events to **S3** (and optionally **CloudWatch Logs**, SNS on file delivery). **Multi-Region trail** (recommended) and **organization trail** (from management/delegated admin account, all member accounts, members can't modify it) |
| **Management events** | Control plane (CreateBucket, RunInstances, ConsoleLogin...). Read/write separation. Logged by default on trails |
| **Data events** | High-volume data plane: **S3 object-level** (GetObject/PutObject/DeleteObject), Lambda Invoke, DynamoDB item-level, etc. **Not logged by default**, extra cost. Use advanced event selectors to filter |
| **Insights events** | Detects **unusual API call rates or error rates** (e.g., spike in `TerminateInstances` or AccessDenied) -> anomalous activity |
| **Network activity events** | API calls through VPC endpoints (for data perimeter) |
| **Log file integrity validation** | SHA-256 digest files each hour -> prove logs weren't modified/deleted (`aws cloudtrail validate-logs`). Common answer for "prove logs not tampered" |
| **Encryption** | SSE-S3 default; **SSE-KMS** with CMK for extra control |
| **CloudTrail Lake** | Managed event data store with **SQL queries**, long retention (up to ~10 years), can ingest non-AWS events, org-wide. Use for "query API activity with SQL without managing Athena" |
| **Delivery delay** | Events delivered to S3 within ~**5 minutes** on average (not real time); EventBridge gets management events near real time |
| **Protection** | S3 bucket policy (only CloudTrail writes), MFA delete / Object Lock, separate Log Archive account, SCP denying `StopLogging`/`DeleteTrail` |

**CloudTrail + EventBridge:** EventBridge receives events with detail-type **"AWS API Call via CloudTrail"**. Per the EventBridge docs, this **needs a CloudTrail trail with logging enabled**; S3 object-level (data) events additionally need data event selectors on the trail. Read-only management events can be matched on the default bus (opt-in rule setting). Pattern: rule on `eventName: ["DeleteBucket","StopLogging","AuthorizeSecurityGroupIngress"]` -> SNS / Lambda remediation.
**CloudTrail -> CloudWatch Logs -> metric filter -> alarm** = the classic CIS benchmark alerts (root login, console login without MFA, IAM policy changes, unauthorized API calls, NACL/SG changes).

**Querying CloudTrail logs in S3:** Athena (create table from CloudTrail console, partition projection) or CloudTrail Lake.

---

[← AWS X-Ray](xray.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon EventBridge →](eventbridge.md)
