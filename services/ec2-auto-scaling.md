[← AWS Step Functions and Lambda automation](step-functions.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Elastic Load Balancing and compute high availability →](elastic-load-balancing.md)

# Amazon EC2 Auto Scaling

**Exam domains:** [Domain 3](../03-resilient-cloud.md), [Domain 4](../04-monitoring-logging.md), [Domain 5](../05-incident-event-response.md) | **Hands-on:** [Lab 12](../labs/12-auto-scaling-lifecycle-hooks/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## EC2 Auto Scaling (very heavily tested)

**Scaling policy types**

| Policy | How | Use |
|---|---|---|
| **Target tracking** | Keep a metric at a target (e.g., CPU 50%, `ALBRequestCountPerTarget` 1000, SQS backlog per instance) | Default best answer; ASG creates alarms for you |
| **Step scaling** | Different adjustments for different alarm breach sizes | Big spikes need bigger jumps |
| Simple scaling | One adjustment + cooldown | Legacy |
| **Scheduled** | Change min/max/desired at times | Known patterns (business hours, Monday 9 AM) |
| **Predictive scaling** | ML forecast from 14 days history, scales **ahead** of load | Recurring daily/weekly patterns, slow-boot apps. Use "forecast only" mode first |

**Other must-knows**
- **Launch templates** (versions, mixed instances) - launch configurations are legacy.
- **Mixed instances policy**: On-Demand base + % Spot, multiple instance types, allocation strategies (`price-capacity-optimized` for Spot). **Capacity Rebalancing** replaces Spot instances at elevated interruption risk.
- **Warm pools**: pre-initialised stopped/hibernated/running instances -> fast scale-out for apps with long boot/init time.
- **Lifecycle hooks**: `autoscaling:EC2_INSTANCE_LAUNCHING` / `TERMINATING` -> instance waits in `Pending:Wait` / `Terminating:Wait` (heartbeat timeout default 1 h, range 30 s-2 h; extend with `RecordLifecycleActionHeartbeat`; total wait max 48 h or 100 x heartbeat, whichever is smaller) so you can install software or **copy logs before termination**. Notify via EventBridge/SNS/SQS -> Lambda / SSM Run Command, then `complete-lifecycle-action` (CONTINUE/ABANDON).
- **Termination policies**: Default (AZ balance -> oldest launch template/config -> closest to next billing hour), OldestInstance, NewestInstance, OldestLaunchTemplate, AllocationStrategy, custom Lambda. **Instance scale-in protection** for specific instances.
- **Suspend processes** (Launch, Terminate, HealthCheck, ReplaceUnhealthy, AZRebalance, AlarmNotification, ScheduledActions, AddToLoadBalancer, InstanceRefresh) - e.g., suspend `ReplaceUnhealthy` while debugging, `AZRebalance` to avoid churn.
- **Standby** state: take instance out of service for troubleshooting without terminating.
- **Instance refresh**: rolling replacement to a new launch template/AMI with min healthy %, warm-up, checkpoints, **auto rollback** on failure/alarm.
- **Default instance warmup** so new instances' metrics don't trigger more scaling too early.
- Health checks: EC2 (status checks) default; add **ELB** health checks; custom via `set-instance-health`.
- Scaling metric for queue workers: **backlog per instance** = `ApproximateNumberOfMessagesVisible` / running instances (custom metric) with target tracking.

## More scaling details
- **Good metrics to scale on**: average CPU, `RequestCountPerTarget` (ALB), average network in/out, or a custom metric (e.g., queue backlog per instance).
- **Cooldown** (default 300 s, for simple scaling): after a scaling activity, wait before the next one so metrics settle. Target tracking and step scaling use **instance warmup** instead.
- **Notifications**: ASG SNS notifications for launch/terminate/fail, or EventBridge events (`EC2 Instance Launch Successful/Unsuccessful`, `EC2 Instance Terminate Successful/Unsuccessful`, lifecycle actions).

## Warm pools in detail
- Problem: apps with long boot/initialisation (updates, data hydration, config scripts). Old fixes were over-provisioning (cost) or golden AMIs (only partly helps).
- A warm pool keeps **pre-initialised instances** next to the ASG. Warm instance state:
  - **Stopped**: cheapest (you pay only for EBS), slower to serve (must start).
  - **Hibernated**: memory saved to disk, faster resume than stopped, pay for EBS.
  - **Running**: fastest, but you pay for the instance (like over-provisioning).
- **Instance reuse policy**: by default, scale-in terminates instances. With reuse, scale-in returns instances to the warm pool instead.
- **Lifecycle hooks also fire** when instances enter the warm pool and when they move into service, so init scripts run once at warm-up time, not on every scale-out.

## AWS Application Auto Scaling
One scaling API (target tracking, step, scheduled) for non-EC2 resources: **ECS services**, **DynamoDB tables and GSIs**, **Aurora replicas**, **Lambda provisioned concurrency**, **ElastiCache (Redis/Valkey) replication groups**, **EMR clusters**, Spot Fleet, and **custom resources** (your own API).

---

[← AWS Step Functions and Lambda automation](step-functions.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Elastic Load Balancing and compute high availability →](elastic-load-balancing.md)
