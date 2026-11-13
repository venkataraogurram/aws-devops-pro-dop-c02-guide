[← Lab 08](../08-config-auto-remediation/README.md) | [Labs index](../README.md) | [🏠 Home](../../README.md) | [Lab 10 →](../10-xray-api-gateway-lambda/README.md)

# Lab 09 - CloudWatch Logs: metric filters, alarms, Logs Insights, subscriptions

**Goal:** send JSON application logs to CloudWatch Logs, then:
- turn `statusCode = 500` lines into a **metric** and **alarm** on it;
- extract latency values into a second metric;
- query the logs with **Logs Insights**;
- stream only ERROR events in near real time to a **Lambda** through a **subscription filter**.

**Exam topics:** filter pattern syntax for JSON, metric filters (only new events, metric value extraction), alarm settings (period, threshold, missing data), subscription filters (destinations, permissions, gzip/base64 payload), Logs Insights syntax, retention.
**Services:** [CloudWatch](../../services/cloudwatch.md)
**Time:** ~1 h | **Cost:** < $0.05

## Step 1 - Deploy
```bash
cd labs/09-cloudwatch-logs-alarms
aws cloudformation deploy --stack-name dop-lab09 --template-file template.yaml --capabilities CAPABILITY_IAM \
  --parameter-overrides NotificationEmail=you@example.com
```
Confirm the SNS subscription email.

## Step 2 - Send logs
```bash
aws logs create-log-stream --log-group-name /dop-lab09/app --log-stream-name app-1
python3 gen_events.py
aws logs put-log-events --log-group-name /dop-lab09/app --log-stream-name app-1 --log-events file://events.json
```
Expected: 30 events accepted, 10 of them with `"statusCode": 500` and `"level": "ERROR"`.

## Step 3 - Metric filter -> metric -> alarm
After 1-2 minutes:
```bash
aws cloudwatch get-metric-statistics --namespace DOP-Lab09 --metric-name Http500Count \
  --start-time $(date -u -v-15M +%Y-%m-%dT%H:%M:%SZ) --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 60 --statistics Sum --query 'Datapoints[].Sum'
aws cloudwatch describe-alarms --alarm-names dop-lab09-too-many-500s --query 'MetricAlarms[0].[StateValue,StateReason]'
```
(`date -v-15M` is the macOS syntax; on Linux use `date -u -d '15 min ago' ...`.)

Expected: a datapoint with Sum `10`, and the alarm in **ALARM** (10 > 5). You get the ALARM email, then an OK email a few minutes later (missing data = not breaching).

Test a pattern before you create a filter:
```bash
aws logs test-metric-filter --filter-pattern '{ $.statusCode = 500 && $.path = "/api/orders" }' \
  --log-event-messages '{"statusCode":500,"path":"/api/orders"}' '{"statusCode":200,"path":"/api/orders"}' \
  --query 'matches[].eventNumber'
```
Only event 1 matches. **Remember:** a metric filter only counts events that arrive **after** it is created. Old logs are not back-filled.

## Step 4 - Subscription filter -> Lambda (near real time)
```bash
aws logs tail /aws/lambda/dop-lab09-error-subscriber --since 15m --format short | grep "ERROR EVENT" | head
```
Expected: the 10 ERROR lines only. The `{ $.level = "ERROR" }` subscription filter sent them, gzip-compressed and base64-encoded (the function decodes them). The Lambda needed a **resource-based permission** for `logs.amazonaws.com`. A log group can have **2 subscription filters**. Other destinations: **Kinesis Data Streams, Data Firehose, OpenSearch** (and a cross-account **destination**).

## Step 5 - Logs Insights
Console: **CloudWatch > Logs Insights**, select `/dop-lab09/app`, last 1 hour. Try:
```
fields @timestamp, statusCode, path, latencyMs
| filter statusCode = 500
| sort @timestamp desc
| limit 20
```
```
stats count(*) as requests, avg(latencyMs) as avgLatency, max(latencyMs) as maxLatency by path
```
```
filter level = "ERROR"
| stats count(*) as errors by user
| sort errors desc
```
Or from the CLI:
```bash
QID=$(aws logs start-query --log-group-name /dop-lab09/app --start-time $(( $(date +%s) - 3600 )) --end-time $(date +%s) \
  --query-string 'stats count(*) by statusCode' --query queryId --output text); sleep 5
aws logs get-query-results --query-id $QID --query 'results'
```
Also open **Live Tail** on the log group and send the events again (Step 2) to watch them arrive.

## Step 6 - Latency metric from a value in the log
```bash
aws cloudwatch get-metric-statistics --namespace DOP-Lab09 --metric-name LatencyMs \
  --start-time $(date -u -v-15M +%Y-%m-%dT%H:%M:%SZ) --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 60 --statistics Average Maximum --query 'Datapoints[].[Average,Maximum]'
```
`MetricValue: $.latencyMs` publishes the number from each event. You could alarm on p99 latency or use **anomaly detection** on it. Anomaly detection needs history to train, so it isn't practical in a one-hour lab.

## Exam takeaways
- Count/extract from logs = **metric filter** -> alarm -> SNS/Lambda/Auto Scaling.
- Real-time processing = **subscription filter** -> Kinesis / Firehose / Lambda / OpenSearch. **Export to S3 is batch** (up to 12 h).
- Ad-hoc search = **Logs Insights** (`fields`, `filter`, `stats ... by`, `sort`, `parse`).
- Set **retention** on every log group (here 1 day). The default is never expire.

## Cleanup
```bash
aws cloudformation delete-stack --stack-name dop-lab09
aws cloudformation wait stack-delete-complete --stack-name dop-lab09
aws logs delete-log-group --log-group-name /aws/lambda/dop-lab09-error-subscriber
rm -f events.json
```
