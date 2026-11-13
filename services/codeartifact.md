[← AWS CodeDeploy](codedeploy.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon ECR →](ecr.md)

# AWS CodeArtifact

**Exam domains:** [Domain 1](../01-sdlc-automation.md) | **Hands-on:** none (read-only topic)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## AWS CodeArtifact
**What:** Managed package repository for npm, PyPI, Maven/Gradle, NuGet, Swift, Ruby gems, Cargo, generic.

- **Domain** = container for repositories, one KMS key, shared storage (a package version stored once per domain). Cross-account sharing is via the **domain policy**.
- **Repository** with **upstream repositories** (chain) and **external connection** (npmjs.com, PyPI, Maven Central...). An internal repo -> upstream "public-proxy" repo -> external connection = cache public packages + host private ones.
- Auth: `aws codeartifact login --tool npm|pip|twine --domain X --repository Y` (gets an auth token, default 12 h, max 12 h). In CodeBuild run it in `pre_build`.
- **Package origin controls**: block a package name from being pulled from upstream (protects against dependency-confusion attacks).
- Events in EventBridge when a package version is published/changed -> trigger a pipeline.

**Scenario:** "Developers must only use approved open-source packages, builds must not reach the public internet" -> CodeArtifact with external connection on a separate repo, CodeBuild in VPC with CodeArtifact VPC endpoints (`codeartifact.api`, `codeartifact.repositories`) + S3 gateway endpoint.

## Upstreams, retention and policies
- A repository can have up to 10 **upstream repositories**, and **one external connection** (npmjs, PyPI, Maven Central, NuGet...).
- **Retention**: when a package version is fetched through upstreams, CodeArtifact keeps a copy in the **downstream repository that requested it** and in the repository with the external connection. Intermediate repositories don't keep it. The retained copy isn't affected if the version is later removed upstream.
- **Domain**: one per org/team, shares storage (deduplication) and one KMS key across its repositories. Cross-account access through the **domain policy** and **repository policies** (resource-based).
- **EventBridge events** when a package version is created/modified/deleted -> start a CodePipeline / CodeBuild to rebuild dependent apps.

---

[← AWS CodeDeploy](codedeploy.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon ECR →](ecr.md)
