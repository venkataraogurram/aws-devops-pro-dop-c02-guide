[← AWS CodeArtifact](codeartifact.md) | [Services index](README.md) | [🏠 Home](../README.md) | [EC2 Image Builder →](ec2-image-builder.md)

# Amazon ECR

**Exam domains:** [Domain 1](../01-sdlc-automation.md), [Domain 6](../06-security-compliance.md) | **Hands-on:** [Lab 04](../labs/04-ecs-circuit-breaker/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## Amazon ECR
**What:** Managed Docker/OCI image registry.

| Feature | Fact |
|---|---|
| Lifecycle policies | Expire images by count or age, by tag status/prefix (e.g., keep last 10 `prod-*`, delete untagged after 1 day). |
| Tag immutability | Prevents overwriting a tag (e.g., `v1.2`). Good for traceability. |
| Basic scanning | On push or manual, OS-package CVEs. |
| Enhanced scanning | **Amazon Inspector**: continuous scanning, OS + programming-language packages, findings in Inspector/Security Hub/EventBridge. |
| Replication | Cross-Region and cross-account (registry-level setting, filters by repo prefix). |
| Pull-through cache | Cache images from Docker Hub, Quay, GitHub, ECR Public, K8s registry, etc. |
| Cross-account pull | **Repository policy** allowing the other account's principal `ecr:BatchGetImage`, `ecr:GetDownloadUrlForLayer` (+ `ecr:GetAuthorizationToken` in their IAM policy). |
| Encryption | AES-256 or KMS. |

**Pattern: "Block deployment of images with CRITICAL vulnerabilities"** -> Enhanced scanning -> EventBridge `Inspector2 Finding` with severity CRITICAL -> Lambda/Step Functions stops the pipeline or tags image; or a CodeBuild step that checks scan results before deploy.

---

[← AWS CodeArtifact](codeartifact.md) | [Services index](README.md) | [🏠 Home](../README.md) | [EC2 Image Builder →](ec2-image-builder.md)
