[← Network security (SG, NACL, WAF, Shield, Network Firewall)](network-security.md) | [Services index](README.md) | [🏠 Home](../README.md)

# Security detection services (GuardDuty, Inspector, Macie, Security Hub, Detective, Access Analyzer)

**Exam domains:** [Domain 6](../06-security-compliance.md) | **Hands-on:** [Lab 14](../labs/14-guardduty-security-response/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## Security monitoring and detection services

| Service | What it does | Data sources / scope | Typical exam use |
|---|---|---|---|
| **Amazon GuardDuty** | **Threat detection** with ML/threat intel | CloudTrail management events, VPC Flow Logs, DNS logs (no need to enable these yourself), plus protection plans: S3 data events, EKS audit logs + runtime, ECS/EC2 runtime, RDS login activity, Lambda network, **Malware Protection** (EBS scan, S3 uploads) | "Detect compromised instances, crypto mining, unusual API calls, credential exfiltration". Findings -> EventBridge -> auto response. Org-wide with delegated admin, auto-enable new accounts. Trusted IP lists / threat lists, suppression rules |
| **Amazon Inspector** | **Vulnerability scanning** (CVEs + network reachability) | EC2 (via SSM Agent, or agentless EBS snapshot scanning), **ECR images** (enhanced scanning, on push + continuous), **Lambda** functions and code, CIS benchmark assessments | "Continuously scan for software vulnerabilities". Inspector score, findings to Security Hub/EventBridge. Classic Inspector had "assessment templates" (exam guide wording) - v2 is automatic |
| **Amazon Macie** | Sensitive data discovery in S3 | S3 | "Find PII in S3 buckets at scale" |
| **AWS Security Hub (CSPM)** | **Aggregates findings** (ASFF/OCSF) from GuardDuty, Inspector, Macie, Config, Access Analyzer, Firewall Manager, partners; runs **security standards** checks (AWS Foundational Security Best Practices, CIS, PCI DSS, NIST 800-53) via Config | Multi-account (delegated admin, central configuration), **cross-Region aggregation** | "Single pane of glass / security score / compliance standards across accounts". **Automation rules** (update/suppress findings), **custom actions** -> EventBridge -> remediation |
| **Amazon Detective** | **Investigate** root cause: graph of entities from CloudTrail, VPC Flow Logs, GuardDuty, EKS audit logs | Multi-account | "Analyse/visualise the security finding's root cause, who did what" (after GuardDuty finds) |
| **IAM Access Analyzer** | **External access** findings (resources shared outside zone of trust: S3, KMS, IAM roles, Lambda, SQS, Secrets Manager...), **unused access** findings, **policy validation** (lint + custom policy checks in CI: `check-no-new-access`, `check-access-not-granted`), **policy generation** from CloudTrail | Account or organization zone of trust | "Find resources shared with external accounts", "validate IAM policies in pipeline", "generate least-privilege policy from activity" |
| **AWS Config** | Configuration compliance ([AWS Config](config.md)) | All supported resources | "Detect non-compliant configuration" |
| **AWS Trusted Advisor** | Best-practice checks: cost, performance, **security** (open SGs, MFA on root, exposed keys, S3 permissions), fault tolerance, service limits | Full checks with Business+ support; org view | "Check service quotas / basic security checks"; events in EventBridge (us-east-1) |
| **CloudTrail / VPC Flow Logs / drift detection** | Auditing ([CloudTrail](cloudtrail.md), [CloudWatch](cloudwatch.md)) | | |

**Detect vs investigate vs aggregate vs remediate (don't mix them up):**
- GuardDuty = **detect threats**. Inspector = **find vulnerabilities**. Macie = **find sensitive data**. Config = **detect misconfiguration**. Access Analyzer = **find external/unused access**.
- Security Hub = **aggregate + score + standards**. Detective = **investigate**. 
- EventBridge + Lambda / SSM Automation = **remediate**. SCP / CFN Hook / IAM = **prevent**.

## Data classification: Amazon Macie
- Discovers and classifies **sensitive data in S3** (PII, financial, credentials) with managed + custom data identifiers; **automated sensitive data discovery** samples all buckets continuously; also bucket-level security posture (public, unencrypted, shared).
- Multi-account via delegated admin. Findings -> EventBridge/Security Hub -> remediation (e.g., move object, tag, alert).

## GuardDuty in more detail
- **Multi-account**: designate a **delegated administrator** (security account) from the management account; auto-enable for new accounts; the admin sees all findings and manages settings. (Invitation-based member accounts also exist.)
- **Trusted IP lists** (no findings for these public IPs) and **threat IP lists** (known bad IPs -> findings). Public IPs only. In a multi-account setup only the **administrator** account manages these lists.
- **Findings**: format `ThreatPurpose:ResourceType/ThreatFamilyName.DetectionMechanism!Artifact`, severity, sample findings for testing; **suppression rules** to auto-archive expected findings; export to S3; send to EventBridge (every finding) -> SNS/Lambda/Step Functions.
- **Enable with CloudFormation**: `AWS::GuardDuty::Detector` fails if a detector already exists; use a Lambda custom resource to enable conditionally, and StackSets for all accounts (or simply org auto-enable).

## Inspector in more detail
- **EC2 scanning** (agent-based) needs the instance to be an **SSM managed node**: SSM Agent running, IAM instance profile (or Default Host Management Configuration), outbound HTTPS 443 to Systems Manager endpoints. Inspector uses SSM Inventory to know installed packages. (Agentless scanning of EBS snapshots also exists.)
- **ECR** images scanned on push and continuously as new CVEs are published; **Lambda** functions and code scanned too.
- Findings include an **Inspector risk score**; sent to Security Hub and EventBridge.

## Trusted Advisor monitoring
- Check results can be sent as EventBridge events (from **us-east-1**) -> e.g., low-utilisation EC2 instances -> Lambda/SNS.
- **Service quotas checks**: Trusted Advisor checks 50+ quotas and publishes the `ServiceLimitUsage` metric in CloudWatch (**us-east-1**). Alarm at 80% usage -> SNS. **Service Quotas** service also has CloudWatch usage metrics and alarms for many quotas.

---

[← Network security (SG, NACL, WAF, Shield, Network Firewall)](network-security.md) | [Services index](README.md) | [🏠 Home](../README.md)
