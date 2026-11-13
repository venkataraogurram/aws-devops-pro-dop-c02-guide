[← Amazon S3 (events, integrity, protection)](s3.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon Route 53 →](route53.md)

# Databases and storage: HA and replication

**Exam domains:** [Domain 3](../03-resilient-cloud.md) | **Hands-on:** [Lab 16](../labs/16-multi-region-dr/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## Data layer

| Service | Same-Region HA | Cross-Region |
|---|---|---|
| **RDS** (MySQL/PG/MariaDB/Oracle/SQL Server) | **Multi-AZ instance** (sync standby, automatic failover 60-120 s, DNS endpoint stays same) or **Multi-AZ DB cluster** (1 writer + 2 readable standbys, failover ~35 s). Read replicas = scale reads (async) | **Cross-Region read replica** (async), **promote** for DR (manual, breaks replication). Automated backups **cross-Region replication**. Snapshot copy |
| **Aurora** | Storage 6 copies across 3 AZs; up to 15 replicas; failover to replica ~30 s (set **failover priority tiers**). Reader endpoint load balances | **Aurora Global Database**: up to 10 secondary Regions (was 5 before May 2025; older questions may say 5), replication typically < 1 s, **RPO ~1 s, RTO < 1 min**. **Managed planned switchover** (no data loss, for drills) vs **failover** (unplanned, `failover-global-cluster` with allow data loss). **Write forwarding** from secondary. **Global writer endpoint** |
| **Aurora Serverless v2** | Scales ACUs in seconds; Multi-AZ via readers | Can be part of Global Database |
| **DynamoDB** | Multi-AZ by default | **Global tables**: multi-Region, multi-active (write anywhere), last writer wins; replication usually < 1 s. Multi-Region strong consistency option (MRSC). Needs Streams (managed). **PITR** (restore to any second in the last 1-35 days, configurable) + on-demand backups, cross-Region via AWS Backup |
| **ElastiCache (Redis OSS / Valkey)** | Multi-AZ with auto-failover (replicas) | **Global Datastore** (cross-Region replica clusters, promote secondary) |
| **MemoryDB** | Multi-AZ durable transaction log | Multi-Region (active-active) |
| **S3** | 3+ AZs by default (except One Zone-IA) | **CRR** (Cross-Region Replication, needs versioning both sides; **S3 RTC** = 99.99% in 15 min SLA); **SRR** same-Region; **Multi-Region Access Points** with failover controls; replicate existing objects with **Batch Replication** |
| **EFS** | Regional (multi-AZ) | **EFS replication** to another Region (RPO ~minutes), failover by making replica writable |
| **EBS** | Replicated within one AZ only | **Snapshots** (incremental, stored in S3) copied cross-Region; Data Lifecycle Manager (DLM) for scheduled snapshots + cross-Region copy |
| **Redshift** | Multi-AZ (RA3) | Cross-Region snapshot copy |
| **DocumentDB** | Replicas across AZs | Global clusters |

## RDS details
- **Read replicas**: up to 15 for MySQL/MariaDB/PostgreSQL (fewer for Oracle and SQL Server), asynchronous, readable, same AZ / cross-AZ / cross-Region; can be promoted to a standalone DB. Apps must use the replica's own endpoint. Replication traffic to a replica in the **same Region is free**; cross-Region replication traffic is charged.
- **Single-AZ -> Multi-AZ**: just modify the DB, **no downtime**. RDS takes a snapshot, restores it as a standby in another AZ, then sets up synchronous replication.
- A read replica can itself be Multi-AZ (useful for DR).

## Aurora details
- **Aurora Replicas auto scaling** adds/removes readers on CPU or connections; the **reader endpoint** load-balances across them.
- **Unplanned failover**: Aurora promotes the replica with the highest priority (lowest tier number) and the cluster endpoint follows it.
- **Cross-Region read replicas** (Aurora MySQL) or, better, **Global Database** for DR and low-latency global reads.

## ElastiCache
| | Redis OSS / Valkey | Memcached |
|---|---|---|
| Replication / Multi-AZ failover | Yes | No |
| Persistence / backups | Yes (snapshots, AOF) | No |
| Scaling | Replicas + shards | Add nodes (sharding), multi-threaded |

- **Cluster mode disabled**: one shard, one primary + **up to 5 replicas**, scale reads by adding replicas, scale writes only vertically.
- **Cluster mode enabled**: data partitioned across multiple shards (up to 500 nodes per cluster in total), each shard with a primary + up to 5 replicas; scale writes horizontally; online resharding.

## DynamoDB details
- **Capacity**: provisioned (RCU/WCU, optional auto scaling) or **on-demand** (pay per request).
- **DAX**: in-memory cache in front of DynamoDB, microsecond reads, no app changes beyond the DAX client. **DAX vs ElastiCache**: DAX for caching individual items/queries of DynamoDB; ElastiCache for caching computed/aggregated results or data from other sources.
- **DynamoDB Streams**: ordered item changes, 24 h retention, consumed by Lambda / KCL (or use **Kinesis Data Streams for DynamoDB** for longer retention and more consumers). Used for global tables, triggers, analytics.
- **TTL**: deletes expired items automatically at no cost, in the background (not instantly); deletions appear in Streams.
- **Backups**: PITR (continuous) + on-demand backups (also through AWS Backup, cross-Region/account copy).
- **S3 integration**: export to S3 (needs PITR, no RCU used) for analytics with Athena; import from S3 into a **new** table.

## S3 replication notes
- Versioning must be on in **both** buckets; buckets can be in different accounts; IAM role for S3 to replicate.
- Only **new** objects replicate after you enable it. Existing objects: **S3 Batch Replication** (also retries failed replications).
- Delete markers can be replicated (optional). Deletes of a specific version are **not** replicated (protects against malicious deletes).
- **No chaining**: bucket 1 -> 2 -> 3 does not copy objects from 1 to 3.

## AWS DMS (Database Migration Service)
- Migrate databases to AWS while the **source stays online**. Runs on a replication instance (or DMS Serverless).
- Homogeneous (Oracle -> Oracle) or heterogeneous (Oracle -> Aurora PostgreSQL). For heterogeneous, convert the schema first with **AWS SCT (Schema Conversion Tool)** or DMS Schema Conversion.
- **Full load + CDC (change data capture)** = continuous replication, minimal-downtime cutover.
- **Multi-AZ** replication instance = synchronous standby in another AZ for HA of the migration itself.
- **Monitoring**: CloudWatch metrics for the replication instance and task (e.g., CDC latency), and task logs in CloudWatch Logs.

## AWS Storage Gateway (hybrid storage)
- Gives on-premises apps access to AWS storage: **S3 File Gateway** (NFS/SMB -> S3), **FSx File Gateway** (SMB -> FSx for Windows), **Volume Gateway** (iSCSI block volumes backed by S3 + EBS snapshots), **Tape Gateway** (virtual tape library -> S3/Glacier).
- **File Gateway cache**: if objects are added to the bucket directly (not through the gateway), the on-prem file share won't see them until the cache is refreshed. Call the **`RefreshCache` API** (e.g., from Lambda on an S3 event or schedule) or turn on **automated cache refresh** (refresh after a set time).

---

[← Amazon S3 (events, integrity, protection)](s3.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon Route 53 →](route53.md)
