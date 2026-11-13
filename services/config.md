[← AWS Systems Manager](systems-manager.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS AppConfig →](appconfig.md)

# AWS Config

**Exam domains:** [Domain 2](../02-config-mgmt-iac.md), [Domain 4](../04-monitoring-logging.md), [Domain 5](../05-incident-event-response.md), [Domain 6](../06-security-compliance.md) | **Hands-on:** [Lab 08](../labs/08-config-auto-remediation/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

- **Configuration recorder** records resource configuration items (all supported types or selected; continuous or daily recording). **Delivery channel** to S3 (+ SNS).
- **Rules**: AWS **managed rules** (e.g., `s3-bucket-public-read-prohibited`, `encrypted-volumes`, `restricted-ssh`, `required-tags`, `approved-amis-by-id`, `cloudtrail-enabled`, `iam-user-mfa-enabled`, `access-keys-rotated`, `rds-multi-az-support`, `acm-certificate-expiration-check`) or **custom rules** (Lambda or **Guard** DSL).
- Triggers: **configuration change** (resource changes) and/or **periodic** (1, 3, 6, 12, 24 h).
- **Remediation**: attach an **SSM Automation** document; **automatic** remediation with retry attempts, or manual (button). Needs an automation assume role.
- **Conformance packs**: bundle of rules + remediations (YAML) deployed as one; **organization conformance packs** from management/delegated admin.
- **Organization rules** deploy a rule to all accounts.
- **Aggregator**: multi-account + multi-Region view of config and compliance (in delegated admin/security account). Read-only view, doesn't remediate by itself.
- **Advanced queries**: SQL-like query of current configuration across aggregator.
- Config **does not prevent** - it detects after the fact (use SCP/Hook to prevent).
- Config + EventBridge: `Config Rules Compliance Change` events -> SNS/Lambda.
- Resource timeline and relationships = "who changed this SG and when" (with CloudTrail link).

**Scenario:** "Automatically enable S3 default encryption / block public access on any non-compliant bucket in all accounts" -> Org Config rule (or conformance pack) + auto remediation SSM document (e.g., `AWS-EnableS3BucketEncryption`, `AWS-ConfigureS3BucketPublicAccessBlock`).

---

## Organization rules vs conformance packs
| | Organization rules | Conformance packs |
|---|---|---|
| Scope | All accounts in the organization | One account, or the organization (organization conformance packs) |
| Contents | One rule at a time | Many rules + remediations in one YAML package |
| Managed from | Management / delegated admin account | Account, or management / delegated admin for org packs |

**Conformance packs in CI/CD**: keep the pack YAML (managed rules, custom Lambda rules, SSM remediation documents) in a repo; CodePipeline + CodeBuild/CloudFormation deploy it on every change, so compliance rules are versioned and reviewed like code.

---

[← AWS Systems Manager](systems-manager.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS AppConfig →](appconfig.md)
