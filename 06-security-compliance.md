[← 5. Domain 5: Incident and Event Response (14%)](05-incident-event-response.md) | [🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [7. "Which one?" comparisons + numbers →](07-service-comparisons-numbers.md)

# Chapter 6 - Domain 6: Security and Compliance (17%)

> IAM at scale (policy evaluation, roles, federation, permission boundaries, SCPs, ABAC), secrets rotation, KMS/encryption, network security, and the detection services (GuardDuty, Inspector, Macie, Security Hub, Detective, Access Analyzer, Config).

## Services to study for this domain

Read these service files first, then the sections below.

- [Amazon ECR](services/ecr.md)
- [AWS Config](services/config.md)
- [AWS Organizations and SCPs](services/organizations.md)
- [AWS Control Tower](services/control-tower.md)
- [Amazon S3 (events, integrity, protection)](services/s3.md)
- [AWS CloudTrail](services/cloudtrail.md)
- [IAM, STS and IAM Identity Center](services/iam-sts-identity-center.md)
- [Secrets Manager and Parameter Store](services/secrets-manager-parameter-store.md)
- [AWS KMS, CloudHSM and encryption](services/kms-cloudhsm.md)
- [AWS Certificate Manager (ACM)](services/acm.md)
- [Network security (SG, NACL, WAF, Shield, Network Firewall)](services/network-security.md)
- [Security detection services (GuardDuty, Inspector, Macie, Security Hub, Detective, Access Analyzer)](services/security-detection.md)

## 6.1 Common threats -> controls (exam guide lists these threats)

| Threat | Prevent | Detect | Respond |
|---|---|---|---|
| Insecure web traffic (HTTP) | ALB redirect to HTTPS, CloudFront viewer policy, S3 `aws:SecureTransport` deny | Config `alb-http-to-https-redirection-check`, Security Hub | Auto remediation |
| Exposed access keys | No long-term keys (roles, OIDC), git-secrets / CodeGuru Security / secret scanning in pipeline | AWS Health `AWS_RISK_CREDENTIALS_EXPOSED`, GuardDuty `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS` | EventBridge -> Lambda deactivates key, reviews CloudTrail |
| S3 bucket public | Account-level **S3 Block Public Access**, SCP denying `s3:PutBucketPublicAccessBlock` changes, Object Ownership enforced | Config `s3-bucket-public-read/write-prohibited`, Access Analyzer, Macie, Trusted Advisor | Config auto remediation |
| S3 encryption disabled | Default encryption (SSE-S3 is now automatic), bucket policy deny non-KMS uploads | Config `s3-bucket-server-side-encryption-enabled`, Security Hub | Remediation runbook |
| Open SSH/RDP to world | SCP / Firewall Manager SG policies, Session Manager instead of SSH | Config `restricted-ssh`, `restricted-common-ports`, Trusted Advisor, Security Hub | Remove rule automatically |
| Root user usage | MFA on root, no root keys, SCP limits on member root (or centralised root access, delete member root creds) | CloudTrail metric filter on `userIdentity.type = Root` -> alarm | Notify |
| Compromised instance | IMDSv2, least privilege, patching | GuardDuty | Isolate SG, snapshot, Detective |

## 6.2 Security automation at scale (multi-account, multi-Region)
- **Organizations + delegated admin** for GuardDuty, Security Hub, Inspector, Macie, Detective, Config, Access Analyzer, Firewall Manager, Backup, CloudTrail (org trail).
- **Auto-enable** for new member accounts (GuardDuty/Security Hub/Inspector/Macie org settings).
- **Security Hub central configuration**: one policy applied to OUs (standards, controls, Regions) + cross-Region aggregation into a home Region.
- **Control Tower** controls (preventive/detective/proactive) on OUs.
- **StackSets** (service-managed) to deploy security roles/config.
- **SSM Automation** multi-account/multi-Region remediation; **Quick Setup** org configs.
- **Config conformance packs (org)** + **aggregator**.
- **Firewall Manager** for WAF/SG/Network Firewall policies everywhere.
- Pipeline security: **CodeGuru Reviewer/Security** (code and secret scanning; Reviewer accepts no new repository associations since Nov 7, 2025), **Inspector** (images, Lambda), Access Analyzer policy checks, **cfn-guard/cfn-lint/cfn-nag**, secrets scanning.

## 6.3 Domain 6 scenario quick-map

| Scenario | Answer |
|---|---|
| Workforce access to 100 accounts with corporate IdP | IAM Identity Center + external IdP (SAML + SCIM) + permission sets |
| GitHub Actions deploy to AWS without keys | IAM OIDC provider + role with trust condition on `sub` (repo:org/repo:ref:refs/heads/main) |
| Third-party SaaS needs access to our account | Cross-account role with **ExternalId** |
| App on EC2 needs S3 access | Instance profile role (never keys) |
| Pods need AWS access | IRSA or EKS Pod Identity |
| Devs create roles safely | Permissions boundary + condition on `iam:PermissionsBoundary` |
| Scale permissions with many projects | ABAC with tags |
| Nobody (even admins) in member accounts may disable CloudTrail | SCP deny `cloudtrail:StopLogging/DeleteTrail` |
| Bucket accessible only from our org | Bucket policy with `aws:PrincipalOrgID` (or RCP for whole org) |
| Bucket only via VPC endpoint | Bucket policy deny unless `aws:SourceVpce` |
| Rotate RDS password automatically | Secrets Manager managed rotation (or RDS `ManageMasterUserPassword`) |
| Share encrypted AMI/snapshot cross-account | Re-encrypt with CMK; key policy grants target account |
| Single-tenant HSM, full key control | CloudHSM (optionally KMS custom key store) |
| Multi-Region encryption for DR | KMS multi-Region keys |
| Certificate expiring (imported) | ACM `DaysToExpiry` / EventBridge expiry event / Config rule -> SNS |
| Find PII in S3 across org | Macie with automated discovery, delegated admin |
| Detect crypto mining / malicious IPs | GuardDuty |
| CVE scan of ECR images and EC2 | Inspector |
| One dashboard of all findings + CIS/FSBP compliance | Security Hub (delegated admin + cross-Region aggregation) |
| Investigate a GuardDuty finding's root cause | Detective |
| Find resources shared outside org | IAM Access Analyzer (org zone of trust) |
| Validate IAM policies in pipeline | Access Analyzer `ValidatePolicy` / custom policy checks |
| Block SQLi / bad bots / rate limit | WAF (managed rules, rate-based rule) |
| Block one malicious IP fast at subnet | NACL deny rule (or WAF IP set if web) |
| Egress allow-list of domains | Network Firewall domain list (or DNS Firewall) |
| Same WAF rules in every account | Firewall Manager |

---

[← 5. Domain 5: Incident and Event Response (14%)](05-incident-event-response.md) | [🏠 Home](README.md) | [Services](services/README.md) | [Labs](labs/README.md) | [7. "Which one?" comparisons + numbers →](07-service-comparisons-numbers.md)
