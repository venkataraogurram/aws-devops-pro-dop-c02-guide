[← Amazon Route 53](route53.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Backup →](aws-backup.md)

# CloudFront and Global Accelerator

**Exam domains:** [Domain 3](../03-resilient-cloud.md) | **Hands-on:** none (read-only topic)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## CloudFront
- **Origin groups** with primary + secondary origin -> **origin failover** on specific HTTP error codes (500, 502, 503, 504, 403, 404) or timeouts. Good for S3 bucket in 2 Regions (with CRR).
- Caching reduces origin load; cache behaviours per path; TTLs; invalidations.
- **AWS Global Accelerator**: static anycast IPs, routes to healthy endpoints in multiple Regions in seconds (TCP/UDP, non-HTTP, no DNS caching problem). Choose it over Route 53 when "clients cache DNS / need static IPs / fast failover".

---

[← Amazon Route 53](route53.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Backup →](aws-backup.md)
