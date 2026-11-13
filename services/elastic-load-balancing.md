[← Amazon EC2 Auto Scaling](ec2-auto-scaling.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS CloudFormation →](cloudformation.md)

# Elastic Load Balancing and compute high availability

**Exam domains:** [Domain 3](../03-resilient-cloud.md), [Domain 4](../04-monitoring-logging.md) | **Hands-on:** [Lab 12](../labs/12-auto-scaling-lifecycle-hooks/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## Compute and load balancing

| Service | HA mechanism |
|---|---|
| EC2 | ASG across **multiple AZs** behind a load balancer. Single instance = SPOF. EC2 **auto recovery** (CloudWatch alarm `StatusCheckFailed_System` -> recover action, keeps instance ID/IP; default simplified auto recovery for supported types) |
| ELB | ALB/NLB nodes in each enabled AZ. **Cross-zone load balancing**: ALB always on (can turn off per target group), NLB/GWLB off by default (charges inter-AZ). Turn on to avoid uneven distribution when AZs have different instance counts |
| ECS | Service with tasks spread across AZs (`spread` placement on `attribute:ecs.availability-zone` default for Fargate), multiple subnets |
| EKS | Managed node groups across AZs, pod topology spread constraints, PodDisruptionBudgets |
| Lambda | Runs in multiple AZs automatically. If in VPC, give subnets in multiple AZs |

**ALB/NLB health checks + recovery from backend failure**
- Target group health check: protocol, path (`/health`), port, healthy/unhealthy threshold, interval, timeout, success codes.
- ALB routes only to healthy targets. If **all** targets are unhealthy, ALB **fails open** (routes to all).
- ASG health check type **ELB** (not just EC2) so ASG **replaces** instances that fail the LB health check. Health check grace period so booting instances aren't killed.
- **Deregistration delay** (connection draining, default 300 s) to finish in-flight requests on scale-in/deploy.
- Route 53 health check + failover for multi-Region.

## ALB and NLB features
- **ALB listener rules**: route by path, host header, HTTP header, method, query string, source IP. Actions: forward, redirect (e.g., HTTP -> HTTPS), fixed response, authenticate (Cognito/OIDC).
- **Weighted target groups**: one rule forwards to two target groups with weights (e.g., 90/10) -> blue/green or canary at the load balancer, without DNS changes.
- **Dual-stack**: ALB/NLB can accept IPv4 and IPv6 clients (`dualstack` IP address type). Targets can be IPv4 or IPv6.
- **NLB + PrivateLink**: put an NLB in front of your service and create a **VPC endpoint service**; consumers in other VPCs/accounts connect through an interface endpoint. Works even when VPC CIDRs **overlap** (VPC peering doesn't).
- ALB is in front of Lambda, ECS, EC2, IPs; NLB gives static IPs per AZ and TLS passthrough/termination.

## NAT gateway and high availability
- Private subnets reach the internet through a **NAT gateway** in a public subnet (managed, scales automatically, no security groups).
- A NAT gateway lives in **one AZ**. For AZ-level fault tolerance, create **one NAT gateway per AZ** and route each private subnet to the NAT in its own AZ.
- NAT instance = old self-managed alternative (you handle HA, patching, source/destination check off).

---

[← Amazon EC2 Auto Scaling](ec2-auto-scaling.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS CloudFormation →](cloudformation.md)
