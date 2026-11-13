[← Lab 15](../15-organizations-scp/README.md) | [Labs index](../README.md) | [🏠 Home](../../README.md)

# Lab 16 - Multi-Region DR building blocks: S3 CRR, DynamoDB global table, Route 53 failover

**Goal:** see three cross-Region features work in a few minutes:
- **S3 Cross-Region Replication** (and what is *not* replicated);
- a **DynamoDB global table** written from both Regions;
- **Route 53 failover** driven by a **CloudWatch alarm-based health check**, the way you'd monitor a private endpoint.

**Exam topics:** CRR requirements (versioning both sides, IAM role), replication status, delete marker behaviour, existing objects (Batch Replication), global tables (multi-active, last writer wins), failover routing, alarm-based health checks, `InsufficientDataHealthStatus`, TTL and RTO.
**Services:** [Databases and storage](../../services/databases-storage.md), [S3](../../services/s3.md), [Route 53](../../services/route53.md)
**Time:** ~1.5 h | **Cost:** < $0.50 (hosted zone is free if deleted within 12 hours; health check prorated; tiny S3/DynamoDB usage)

Regions: primary `us-east-1`, DR `us-west-2`. Nothing in this lab is reachable from the internet. The DNS records point to documentation-only IP addresses.

## Step 1 - Deploy the DR side first, then the primary
```bash
cd labs/16-multi-region-dr
aws cloudformation deploy --region us-west-2 --stack-name dop-lab16-dr --template-file dr-region.yaml
DR_ARN=$(aws cloudformation describe-stacks --region us-west-2 --stack-name dop-lab16-dr --query "Stacks[0].Outputs[?OutputKey=='ReplicaBucketArn'].OutputValue" --output text)
DR_BUCKET=${DR_ARN##*:}
aws cloudformation deploy --region us-east-1 --stack-name dop-lab16-primary --template-file primary.yaml \
  --capabilities CAPABILITY_IAM --parameter-overrides ReplicaBucketArn=$DR_ARN
out() { aws cloudformation describe-stacks --region us-east-1 --stack-name dop-lab16-primary --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text; }
export SRC=$(out SourceBucketName) ZONE=$(out HostedZoneId) HC=$(out HealthCheckId)
```
(If Route 53 rejects the zone name `dop-lab16.example.com`, change it, and the two record names, to another domain-style name.)

## Step 2 - S3 Cross-Region Replication
```bash
echo "order export v1" > /tmp/export.txt
aws s3 cp /tmp/export.txt s3://$SRC/exports/export.txt --region us-east-1
sleep 30
aws s3api head-object --bucket $SRC --key exports/export.txt --region us-east-1 --query ReplicationStatus     # PENDING -> COMPLETED
aws s3api head-object --bucket $DR_BUCKET --key exports/export.txt --region us-west-2 --query ReplicationStatus # REPLICA
```
Now delete it in the source:
```bash
aws s3 rm s3://$SRC/exports/export.txt --region us-east-1
aws s3 ls s3://$DR_BUCKET/exports/ --region us-west-2      # still there
```
Because `DeleteMarkerReplication` is **Disabled**, the delete marker stays in the source. The DR copy survives accidental or malicious deletes. (Deleting a specific **version** is never replicated.) Objects that existed **before** replication was turned on are not copied. Use **S3 Batch Replication** for those.

## Step 3 - DynamoDB global table: write anywhere
```bash
aws dynamodb put-item --region us-east-1 --table-name dop-lab16-orders --item '{"id":{"S":"o-1"},"from":{"S":"us-east-1"}}'
sleep 3
aws dynamodb get-item --region us-west-2 --table-name dop-lab16-orders --key '{"id":{"S":"o-1"}}' --query Item
aws dynamodb put-item --region us-west-2 --table-name dop-lab16-orders --item '{"id":{"S":"o-2"},"from":{"S":"us-west-2"}}'
sleep 3
aws dynamodb scan --region us-east-1 --table-name dop-lab16-orders --query 'Items[].[id.S,from.S]' --output table
```
Expected: both items readable in both Regions within about a second. Both Regions accept writes (**multi-active**). If both Regions write the same item at the same time, the **last writer wins**. Check replication lag: CloudWatch metric `ReplicationLatency` (namespace `AWS/DynamoDB`).

## Step 4 - Route 53 failover on an alarm-based health check
The primary's "health" is a heartbeat metric. In real life a canary or your app would publish it. Here you publish it yourself.
```bash
beat() { aws cloudwatch put-metric-data --region us-east-1 --namespace DOP-Lab16 --metric-name PrimaryHealthy --value $1; }
ask() { aws route53 test-dns-answer --hosted-zone-id $ZONE --record-name app.dop-lab16.example.com --record-type A --query RecordData --output text; }

# healthy: send a heartbeat every 30 s for ~3 minutes
for i in $(seq 1 6); do beat 1; sleep 30; done
aws cloudwatch describe-alarms --region us-east-1 --alarm-names dop-lab16-primary-unhealthy --query 'MetricAlarms[0].StateValue'
ask
```
Expected: alarm `OK`, DNS answer `192.0.2.10` (primary). The health check shows **Healthy** in **Route 53 > Health checks** (its status follows the alarm state).

Now "fail" the primary. Stop the heartbeat (missing data = breaching) or send 0:
```bash
beat 0; sleep 120
aws cloudwatch describe-alarms --region us-east-1 --alarm-names dop-lab16-primary-unhealthy --query 'MetricAlarms[0].StateValue'
ask
```
Expected: alarm `ALARM`, health check **Unhealthy** in the console, DNS answer `198.51.100.10` (secondary). Send heartbeats again and it fails back to the primary.

**RTO thinking:** detection (alarm period + evaluation) + health check reaction + **DNS TTL (60 s here)** + clients' own DNS caching. That's why the exam says "Global Accelerator" when clients cache DNS or you need sub-minute failover with static IPs.

## Cleanup
```bash
aws s3api delete-bucket-replication --bucket $SRC --region us-east-1
../tools/empty-versioned-bucket.sh $SRC us-east-1
../tools/empty-versioned-bucket.sh $DR_BUCKET us-west-2
aws cloudformation delete-stack --region us-east-1 --stack-name dop-lab16-primary
aws cloudformation wait stack-delete-complete --region us-east-1 --stack-name dop-lab16-primary
aws cloudformation delete-stack --region us-west-2 --stack-name dop-lab16-dr
rm -f /tmp/export.txt
```
(Run the empty script twice if it reports leftovers. The global table's us-west-2 replica is deleted with the stack.)

## Exam takeaways
- **CRR**: versioning on both buckets + a role. New objects only (Batch Replication for existing ones). Delete markers optional, version deletes never. **RTC** for a 15-minute SLA.
- **Global tables** = multi-Region active-active key-value data with seconds of RPO.
- **Route 53 failover** + health checks. **Alarm-based health checks** for private or custom health signals. TTL affects RTO.
- Map these to DR strategies: S3 CRR + global tables are the **data layer** of pilot light / warm standby / active-active.
