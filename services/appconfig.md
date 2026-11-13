[← AWS Config](config.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Service Catalog →](service-catalog.md)

# AWS AppConfig

**Exam domains:** [Domain 2](../02-config-mgmt-iac.md) | **Hands-on:** none (read-only topic)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## AWS AppConfig
- Configuration profiles (freeform JSON/YAML/text from AppConfig hosted store, S3, Parameter Store, Secrets Manager, CodePipeline) or **feature flags**.
- **Validators**: JSON Schema or Lambda - bad config is rejected before deploy.
- **Deployment strategies**: `AppConfig.AllAtOnce`, `AppConfig.Linear50PercentEvery30Seconds`, `AppConfig.Linear20PercentEvery6Minutes`, `AppConfig.Canary10Percent20Minutes`, or custom (growth type linear/exponential, bake time).
- **Automatic rollback** when a linked **CloudWatch alarm** fires during deployment/bake time.
- App retrieves via AppConfig Agent / Lambda extension (`StartConfigurationSession`, `GetLatestConfiguration`) with local caching.

---

---

[← AWS Config](config.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Service Catalog →](service-catalog.md)
