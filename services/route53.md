[← Databases and storage: HA and replication](databases-storage.md) | [Services index](README.md) | [🏠 Home](../README.md) | [CloudFront and Global Accelerator →](cloudfront-global-accelerator.md)

# Amazon Route 53

**Exam domains:** [Domain 3](../03-resilient-cloud.md), [Domain 4](../04-monitoring-logging.md) | **Hands-on:** [Lab 16](../labs/16-multi-region-dr/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## DNS and edge: Route 53

| Routing policy | Use |
|---|---|
| Simple | One record, no health checks |
| **Failover** | Active-passive: primary record with health check, secondary used when primary unhealthy (DR) |
| **Weighted** | Split traffic by % (blue/green, canary across Regions) |
| **Latency** | Send users to lowest-latency Region (active-active) |
| Geolocation | By user's country/continent (compliance, localisation). Add default record |
| Geoproximity | By distance with bias (Traffic Flow) |
| Multivalue answer | Up to 8 healthy records, client-side LB |
| IP-based | By client CIDR |

**Health checks**: endpoint (HTTP/HTTPS/TCP, string matching, from global checkers), **calculated** (combine child checks with AND/OR/threshold), **CloudWatch alarm-based** (for private resources - Route 53 checkers can't reach private IPs, so alarm on a metric and attach a health check to the alarm). **Evaluate target health** on alias records (ALB health propagates). **Route 53 ARC** (Application Recovery Controller): readiness checks + routing controls for highly reliable manual failover; **Region switch** for orchestrated multi-Region failover plans.

## Records and hosted zones
- Record types to know: **A** (IPv4), **AAAA** (IPv6), **CNAME** (name -> name, not allowed at the zone apex), **NS**, and **Alias** (Route 53 extension: points to AWS resources such as ALB, CloudFront, S3 website, API Gateway; works at the apex; free queries; can evaluate target health).
- **Public hosted zone**: answers internet queries. **Private hosted zone**: answers only inside associated VPCs (can be shared with VPCs in other accounts).
- TTL: lower TTL before a planned migration so clients pick up changes quickly.

---

[← Databases and storage: HA and replication](databases-storage.md) | [Services index](README.md) | [🏠 Home](../README.md) | [CloudFront and Global Accelerator →](cloudfront-global-accelerator.md)
