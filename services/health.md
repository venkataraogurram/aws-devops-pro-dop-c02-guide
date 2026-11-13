[← Amazon EventBridge](eventbridge.md) | [Services index](README.md) | [🏠 Home](../README.md) | [SQS, SNS, Kinesis, Firehose and Lambda event handling →](sqs-sns-kinesis.md)

# AWS Health

**Exam domains:** [Domain 5](../05-incident-event-response.md) | **Hands-on:** none (read-only topic)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

- **AWS Health Dashboard (your account)**: events affecting **your** resources (scheduled maintenance, retirements, service issues, account notifications) - vs Service Health Dashboard (public, all customers).
- **AWS Health API** (Business/Enterprise support for full API) and **EventBridge events** (`aws.health`) - free for all.
- **Organizational view**: aggregate Health events across org (from management or delegated admin).
- Classic patterns:
  - EC2 instance **scheduled retirement / maintenance** event -> EventBridge -> Lambda/SSM Automation stops and starts instance (moves to new hardware) or notifies.
  - **Exposed access key** event (`AWS_RISK_CREDENTIALS_EXPOSED`) -> EventBridge -> Lambda/Step Functions: **delete/deactivate key**, summarise CloudTrail activity, notify security.
  - Health events -> SNS / Chatbot to Slack.
- **AWS Health Aware (AHA)** solution for multi-account alerts.

## Two dashboards
- **Service history** (public): status of every AWS service in every Region, for all customers.
- **Your account health** (personalised): only events that affect **your** resources (operational issues, scheduled changes such as EC2 retirements and RDS maintenance, account notifications), with the list of affected resources. **Organizational view** aggregates this for all accounts.
- Health events in EventBridge can trigger remediation, e.g., EC2 retirement -> stop/start the instance via SSM Automation, or `AWS_RISK_CREDENTIALS_EXPOSED` -> delete the exposed key.

---

[← Amazon EventBridge](eventbridge.md) | [Services index](README.md) | [🏠 Home](../README.md) | [SQS, SNS, Kinesis, Firehose and Lambda event handling →](sqs-sns-kinesis.md)
