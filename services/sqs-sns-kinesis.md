[← AWS Health](health.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Athena, Glue and QuickSight (log analytics) →](analytics-athena-glue-quicksight.md)

# SQS, SNS, Kinesis, Firehose and Lambda event handling

**Exam domains:** [Domain 3](../03-resilient-cloud.md), [Domain 5](../05-incident-event-response.md) | **Hands-on:** [Lab 11](../labs/11-eventbridge-sqs-dlq/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

| Service | Model | Key facts |
|---|---|---|
| **SQS Standard** | Queue (pull), at-least-once, best-effort order, unlimited throughput | Visibility timeout (default 30 s, up to 12 h; set ≥ 6x Lambda timeout for Lambda triggers), retention 1 min-14 days (default 4 days), message up to **1 MiB** (since Aug 2025, was 256 KB), long polling (`WaitTimeSeconds` up to 20), delay queues (0-15 min). **DLQ** with `maxReceiveCount` redrive policy; **DLQ redrive** back to source |
| **SQS FIFO** | Exactly-once processing, strict order per **message group ID** | 300 TPS (3,000 with batching, higher with high-throughput mode), deduplication ID / content-based dedup (5-min window), name ends `.fifo` |
| **SNS** | Pub/sub push, fan-out | Subscribers: SQS, Lambda, HTTP/S, email, SMS, mobile, Firehose. **Message filtering** (subscription filter policy on attributes or body). FIFO topics -> FIFO queues. DLQ per subscription. **Fan-out = SNS -> multiple SQS** |
| **EventBridge** | Event router with rules | Content-based routing to 20+ target types, SaaS, cross-account; lower throughput than SNS but richer filtering |
| **Kinesis Data Streams** | Ordered stream (shards), replay, multiple consumers | Retention 24 h default up to 365 days; per shard 1 MB/s or 1,000 records/s in, 2 MB/s out; **enhanced fan-out** (dedicated 2 MB/s per consumer); partition key -> shard ordering; on-demand mode |
| **Data Firehose** | Managed delivery (no consumers to write) | Buffer by size/time, transform with Lambda, convert to Parquet/ORC, destinations S3/Redshift/OpenSearch/Splunk/HTTP. Near real-time (not real-time) |
| **Lambda** | Compute triggered by events | Sync (API GW), async (S3, SNS, EventBridge - 2 retries, **on-failure destination** or DLQ), poll-based **event source mapping** (SQS, Kinesis, DynamoDB Streams, MSK: batch size, batching window, **bisect batch on error**, **maximum retry attempts**, **maximum record age**, on-failure destination, **partial batch response** `ReportBatchItemFailures`) |
| **Step Functions** | Orchestration | Retries/Catch, parallel, human approval, long-running |

**Patterns (exam names them):**
- **Fan-out**: SNS topic -> many SQS queues / Lambdas (or EventBridge rule with multiple targets).
- **Queuing / buffering / load levelling**: producer -> SQS -> consumers scale on depth.
- **Event streaming**: Kinesis with multiple consumer apps reading same stream, ordered per key, replay.
- **Choreography** (services react to events via EventBridge) vs **orchestration** (Step Functions controls the flow).
- **Poison message handling**: DLQ + alarm on `ApproximateNumberOfMessagesVisible` of DLQ.

**Lambda failure handling cheat-sheet**

| Invocation type | Retries | Where failures go |
|---|---|---|
| Synchronous (API GW, SDK invoke) | None by Lambda (caller retries) | Caller gets error |
| Asynchronous (S3, SNS, EventBridge, CloudWatch Logs) | 2 retries (configurable 0-2), event age up to 6 h | **On-failure destination** (SQS/SNS/Lambda/EventBridge/S3) or DLQ (SQS/SNS) |
| SQS event source | Message reappears after visibility timeout until `maxReceiveCount` | Queue's **redrive DLQ** (configure on the SQS queue) |
| Kinesis / DynamoDB Streams | Retries until success or record expires (blocks shard!) | Set max retry attempts / max record age / bisect batch + **on-failure destination** |

## Kinesis Data Streams capacity modes
- **Provisioned**: you choose the shard count (1 MB/s or 1,000 records/s in, 2 MB/s out per shard), pay per shard-hour, scale by splitting/merging (`UpdateShardCount`).
- **On-demand**: no capacity planning, scales automatically from about 4 MB/s write by default, pay per GB in/out.

## Kinesis Data Streams vs Data Firehose
| | Data Streams | Data Firehose |
|---|---|---|
| Purpose | Stream storage for custom consumers | Load streaming data into destinations |
| Consumers | You write them (Lambda, KCL, Flink) | Fully managed delivery to S3, Redshift, OpenSearch, Splunk, HTTP endpoints, Snowflake... |
| Latency | Real time (~70-200 ms) | Near real time (buffer 0-900 s) |
| Retention / replay | 24 h-365 days, replay | No storage, no replay |
| Scaling | Provisioned or on-demand | Automatic |

**Managed Service for Apache Flink**: run Flink apps (Java, Python, SQL via Studio) to analyse streams from Kinesis Data Streams or MSK in real time.

## SNS dead-letter queues
Each **subscription** can have its own SQS DLQ (redrive policy). Messages that SNS can't deliver after its retry policy (e.g., endpoint down, Lambda deleted) go there. FIFO topics need FIFO DLQs.

---

[← AWS Health](health.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Athena, Glue and QuickSight (log analytics) →](analytics-athena-glue-quicksight.md)
