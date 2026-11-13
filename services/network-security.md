[← AWS Certificate Manager (ACM)](acm.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Security detection services (GuardDuty, Inspector, Macie, Security Hub, Detective, Access Analyzer) →](security-detection.md)

# Network security (SG, NACL, WAF, Shield, Network Firewall)

**Exam domains:** [Domain 6](../06-security-compliance.md) | **Hands-on:** [Lab 08](../labs/08-config-auto-remediation/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

| Layer | Control | Key facts |
|---|---|---|
| Instance / ENI | **Security group** | **Stateful**, allow rules only, reference other SGs. Default: deny inbound, allow outbound |
| Subnet | **Network ACL** | **Stateless** (allow return traffic, ephemeral ports 1024-65535), allow + **deny** rules, numbered order. Use to **block a specific IP** |
| Routing | Route tables | Private subnet -> NAT; isolate with no IGW route |
| VPC perimeter | **AWS Network Firewall** | Managed stateful/stateless firewall, Suricata rules, **domain filtering** (allow only `*.amazonaws.com`), IPS. Centralised inspection with Transit Gateway. **Firewall Manager** to deploy across accounts |
| Edge L7 | **AWS WAF** | On CloudFront, ALB, API Gateway, AppSync, Cognito, App Runner, Verified Access. Web ACL rules: managed rule groups (Core rule set, SQLi, known bad inputs, IP reputation, Bot Control), rate-based rules, geo match, IP sets. Logs to S3/CW/Firehose |
| DDoS | **AWS Shield** | **Standard** free (L3/L4) on all; **Advanced** paid: 24x7 Shield Response Team, cost protection, L7 with WAF, advanced metrics, proactive engagement |
| Org-wide | **AWS Firewall Manager** | Centrally enforce WAF rules, Shield Advanced, SGs, Network Firewall, Route 53 Resolver DNS Firewall policies across accounts (needs Organizations + Config) |
| DNS | **Route 53 Resolver DNS Firewall** | Block queries to malicious domains |
| Private access | **VPC endpoints**: gateway (S3, DynamoDB, free) and **interface (PrivateLink)** | Keep traffic off internet; **endpoint policies** restrict which buckets/actions; bucket policy `aws:SourceVpce` |
| Sharing | **AWS RAM** | Share subnets (VPC sharing), Transit Gateway, Resolver rules, Prefix lists, License Manager configs, Private CA... with accounts/OUs |
| Remote access | Client VPN, Site-to-Site VPN, **Verified Access** | |

**Defense in depth example (exam style):** CloudFront + **WAF** + **Shield** -> ALB with **ACM** cert in public subnets (SG allows 443 from CloudFront prefix list) -> app in private subnets (SG from ALB SG only) -> RDS in isolated subnets (SG from app SG, encryption KMS) -> **GuardDuty** + **Config rules** + **Security Hub** + **Inspector** + **Detective** monitoring, **NACLs** to block bad IPs, **Network Firewall** for egress filtering.

## WAF vs Firewall Manager vs Shield
- **WAF**: you define web ACLs and rules per resource (ALB, CloudFront, API Gateway, AppSync, Cognito...). **Managed rule groups** from AWS (core rule set, SQLi, known bad inputs, IP reputation, anonymous IP list, Bot Control, ATP/ACFP fraud) and Marketplace vendors.
- **WAF logging**: send full request logs to CloudWatch Logs, S3, or Data Firehose (name must start with `aws-waf-logs-`).
- **Firewall Manager**: manage WAF, Shield Advanced, security groups, Network Firewall, Route 53 Resolver DNS Firewall, and third-party firewall **policies across all accounts** of the org. New accounts/resources get the rules automatically. For WAF policies you choose: **identify only** (create the web ACL but don't attach, report non-compliance) or **auto remediate** (attach to all in-scope resources).
- **Shield Advanced**: DDoS protection with the response team, cost protection, health-based detection. Firewall Manager can enforce Shield Advanced protections org-wide.

## Protect an ALB so only CloudFront can reach it
CloudFront adds a **secret custom header** (e.g., `X-Origin-Verify: <random value>`) to origin requests. A WAF rule on the ALB (or an ALB listener rule) allows only requests with that header. Store the value in **Secrets Manager** with a rotation Lambda that updates both the CloudFront origin header and the WAF rule. Also restrict the ALB security group to the CloudFront managed prefix list. (CloudFront VPC origins are a newer option that keeps the ALB fully private.)

---

[← AWS Certificate Manager (ACM)](acm.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Security detection services (GuardDuty, Inspector, Macie, Security Hub, Detective, Access Analyzer) →](security-detection.md)
