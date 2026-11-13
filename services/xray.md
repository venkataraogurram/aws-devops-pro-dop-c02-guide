[← Amazon CloudWatch (metrics, alarms, logs, agent, synthetics)](cloudwatch.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS CloudTrail →](cloudtrail.md)

# AWS X-Ray

**Exam domains:** [Domain 4](../04-monitoring-logging.md) | **Hands-on:** [Lab 10](../labs/10-xray-api-gateway-lambda/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

- **Traces** (end-to-end request) made of **segments** (one per service) and **subsegments** (downstream calls, SQL, HTTP). **Service map** shows latency/errors between components. **Trace Analytics**, **Insights** (anomaly detection on traces), **groups** (filter expression).
- **Annotations** = indexed key-value -> **searchable/filterable** (`annotation.customer_id = "123"`). **Metadata** = not indexed, just stored.
- **Sampling rules** (default: first request per second + 5% of additional) to control cost.
- How to enable per service:

| Service | How |
|---|---|
| **Lambda** | Turn on **active tracing** (`TracingConfig: Active`); execution role needs `xray:PutTraceSegments`, `xray:PutTelemetryRecords` (`AWSXRayDaemonWriteAccess`); use X-Ray SDK / Powertools / ADOT to trace downstream calls |
| **API Gateway** | Enable X-Ray tracing on the **stage** |
| **EC2 / on-prem** | Run the **X-Ray daemon** (UDP 2000) or CloudWatch agent / ADOT collector; instrument app with SDK; instance role with X-Ray write |
| **ECS** | Run X-Ray daemon / ADOT collector as a **sidecar container** in the task (task role with X-Ray permissions) |
| **EKS** | X-Ray daemon / ADOT collector as a **DaemonSet** |
| **Elastic Beanstalk** | Enable the X-Ray daemon option in env config (`.ebextensions`: `aws:elasticbeanstalk:xray: XRayEnabled: true`) |
| SNS, SQS, Step Functions, AppSync, ELB | Pass trace header / enable tracing (ALB adds `X-Amzn-Trace-Id` header but does not send segments) |

- **AWS Distro for OpenTelemetry (ADOT)** = vendor-neutral way to send traces/metrics to X-Ray, CloudWatch, AMP. X-Ray SDKs/daemon are moving to OpenTelemetry - for exam, both are valid answers; pick the one offered.
- **CloudWatch Application Signals**: automatic APM (SLOs, service dashboards) using ADOT. **CloudWatch ServiceLens** combined traces+metrics+logs view (older).

---

[← Amazon CloudWatch (metrics, alarms, logs, agent, synthetics)](cloudwatch.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS CloudTrail →](cloudtrail.md)
