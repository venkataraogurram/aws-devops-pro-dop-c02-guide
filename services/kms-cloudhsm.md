[← Secrets Manager and Parameter Store](secrets-manager-parameter-store.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Certificate Manager (ACM) →](acm.md)

# AWS KMS, CloudHSM and encryption

**Exam domains:** [Domain 6](../06-security-compliance.md) | **Hands-on:** none (read-only topic)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## AWS KMS
- **Key types**: AWS owned (invisible), **AWS managed** (`aws/s3`, `aws/ebs` - can't change policy, **can't use cross-account**, auto-rotated yearly), **customer managed keys (CMK)** - you control key policy, grants, rotation (optional automatic rotation every 90 days to 7 years, default 1 year; or on-demand), deletion (7-30 days waiting period).
- Symmetric (AES-256, default) vs asymmetric (RSA/ECC sign/verify, encrypt) vs HMAC.
- **Envelope encryption**: KMS generates a data key (`GenerateDataKey`), data encrypted locally with plaintext data key, encrypted data key stored with data. Direct `Encrypt` limited to 4 KB.
- **Key policy + grants**; `kms:ViaService` condition (key usable only via S3/EBS in a Region); `kms:CallerAccount`.
- **Multi-Region keys**: replicas with same key material and ID in other Regions -> decrypt in DR Region without cross-Region calls.
- **Imported key material (BYOK)**, **custom key store** backed by **CloudHSM** (you control HSMs) or **external key store (XKS)**.
- KMS quota throttling (`ThrottlingException`) at high request rate -> S3 **Bucket Keys**, data key caching.
- Sharing encrypted resources cross-account (AMI, EBS snapshot, RDS snapshot, S3 objects): **must use a CMK** and grant the other account in the key policy; AWS managed keys can't be shared -> re-encrypt copy with a CMK.

## AWS CloudHSM
- Dedicated **single-tenant FIPS 140-3 Level 3** HSMs in your VPC; **you** manage keys and users (AWS can't access). Cluster across AZs for HA.
- Pick when: "regulatory requirement for single-tenant HSM / full control of keys / SSL offload / Oracle TDE / PKCS#11, JCE, CNG".

## Encryption by service (at rest)
| Service | How |
|---|---|
| S3 | **SSE-S3 default for all new objects**; SSE-KMS (audit via CloudTrail, key policy control); DSSE-KMS; SSE-C (customer-provided); client-side. Default bucket encryption; deny unencrypted uploads in bucket policy |
| EBS | **Encryption by default** per Region setting; snapshots of encrypted volumes are encrypted; can't encrypt existing volume in place (snapshot -> copy with encryption) |
| RDS / Aurora | Enable at creation; **can't encrypt existing unencrypted DB** -> snapshot -> copy encrypted -> restore. Read replicas same encryption |
| DynamoDB | Always encrypted (AWS owned, AWS managed or CMK) |
| EFS | At creation; in transit with TLS mount helper |
| CloudWatch Logs, SNS, SQS, Kinesis, Secrets Manager, Parameter SecureString | KMS |

## AMI sharing and copying with KMS
- **Share** an AMI with another account: modify the AMI launch permissions. If its snapshots are encrypted, they must use a **customer managed key**, and the key policy must let the target account use the key (`kms:DescribeKey`, `kms:ReEncrypt*`, `kms:CreateGrant`, `kms:Decrypt`). The target account then launches instances from it (often re-encrypting with its own key).
- **Copy** a shared AMI into your own account (so you own it and the source account can't remove it): the copy can be re-encrypted with **your** KMS key; you need permission on the source key to decrypt.
- **Move an instance to another AZ**: create an AMI (or EBS snapshot), then launch/restore in the target AZ. EBS volumes are AZ-scoped and can't move directly.

---

[← Secrets Manager and Parameter Store](secrets-manager-parameter-store.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Certificate Manager (ACM) →](acm.md)
