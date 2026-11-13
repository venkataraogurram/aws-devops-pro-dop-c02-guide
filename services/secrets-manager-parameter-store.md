[← IAM, STS and IAM Identity Center](iam-sts-identity-center.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS KMS, CloudHSM and encryption →](kms-cloudhsm.md)

# Secrets Manager and Parameter Store

**Exam domains:** [Domain 1](../01-sdlc-automation.md), [Domain 6](../06-security-compliance.md) | **Hands-on:** [Lab 01](../labs/01-codebuild-codepipeline/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## Secrets in build and deploy

| Need | Use |
|---|---|
| DB password with automatic rotation | **Secrets Manager** (managed rotation for RDS/Aurora/Redshift/DocumentDB, Lambda rotation for others) |
| Config values, flags, non-rotating secrets, cheapest | **SSM Parameter Store** (String, StringList, SecureString with KMS) |
| Reference in CloudFormation | `{{resolve:secretsmanager:MySecret:SecretString:password}}`, `{{resolve:ssm:/path}}`, `{{resolve:ssm-secure:/path}}` (ssm-secure only for supported properties) |
| Reference in ECS task definition | `secrets` with `valueFrom` = Secrets Manager ARN or Parameter ARN (execution role needs read access) |
| Reference in CodeBuild | `env.secrets-manager` / `env.parameter-store` |
| Reference in Lambda | Fetch at runtime (cache with AWS Parameters and Secrets Lambda Extension). Environment variables are encrypted at rest but visible in console to those with permissions. |

---

## Secrets Manager vs Parameter Store (rotation)

| Feature | Secrets Manager | Parameter Store |
|---|---|---|
| Automatic rotation | **Yes** (managed rotation for RDS/Aurora/Redshift/DocumentDB, or Lambda rotation function; schedule up to every 4 h) | No (DIY with EventBridge + Lambda) |
| Cost | Per secret per month + API calls | Standard free; Advanced paid |
| Size | 64 KB | 4 KB standard / 8 KB advanced |
| Cross-Region replication | **Yes** (replica secrets) | No |
| Resource policy / cross-account | Yes | No (advanced params can be shared via RAM) |
| Versioning | Staging labels `AWSCURRENT`, `AWSPENDING`, `AWSPREVIOUS` | Version numbers + labels |
| Use | DB creds, API keys that must rotate | Config, AMI IDs, flags, cheap secrets |

Rotation Lambda steps: `createSecret` -> `setSecret` -> `testSecret` -> `finishSecret`. Rotation Lambda in VPC needs route to Secrets Manager endpoint and the DB. **Single-user** vs **alternating-users** rotation strategy (alternating = no downtime for high-concurrency apps).
Machine identity rotation: prefer **roles (auto-rotating temp creds)** over keys; for IAM user keys that must exist: Config `access-keys-rotated` + automation or Secrets Manager custom rotation.

---

[← IAM, STS and IAM Identity Center](iam-sts-identity-center.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS KMS, CloudHSM and encryption →](kms-cloudhsm.md)
