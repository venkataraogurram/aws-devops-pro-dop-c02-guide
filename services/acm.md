[← AWS KMS, CloudHSM and encryption](kms-cloudhsm.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Network security (SG, NACL, WAF, Shield, Network Firewall) →](network-security.md)

# AWS Certificate Manager (ACM)

**Exam domains:** [Domain 6](../06-security-compliance.md) | **Hands-on:** none (read-only topic)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## In transit and PKI: AWS Certificate Manager (ACM)
- **Public certs free**, auto-renew (DNS validation renews automatically; email validation needs action). Deploy on **ELB, CloudFront (cert must be in us-east-1), API Gateway**, App Runner. You can't export public ACM private keys to EC2 (except exportable public certs feature, paid) -> for EC2 use ACM-integrated LB, or Nitro Enclaves.
- **Imported certificates** don't auto-renew -> monitor with **`DaysToExpiry`** metric / Config rule `acm-certificate-expiration-check` / EventBridge "ACM Certificate Approaching Expiration" events (45 days before by default).
- **AWS Private CA**: private PKI for internal TLS, mTLS, IoT; issues private certs usable in ACM.
- Enforce TLS: ALB HTTPS listener + redirect HTTP->HTTPS, security policies (TLS 1.2+), S3 `aws:SecureTransport`, RDS `rds.force_ssl`, CloudFront viewer protocol policy "Redirect HTTP to HTTPS".

---

[← AWS KMS, CloudHSM and encryption](kms-cloudhsm.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Network security (SG, NACL, WAF, Shield, Network Firewall) →](network-security.md)
