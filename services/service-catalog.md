[← AWS AppConfig](appconfig.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Organizations and SCPs →](organizations.md)

# AWS Service Catalog

**Exam domains:** [Domain 2](../02-config-mgmt-iac.md) | **Hands-on:** none (read-only topic)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

- **Portfolio** (collection of **products**; product = CFN template or Terraform config with versions).
- Share portfolios with accounts or the whole **organization / OU**; import in member accounts.
- **Constraints**:
  - **Launch constraint**: IAM role Service Catalog uses to launch the product -> **end users don't need permissions for the underlying resources** (least privilege, very common answer).
  - **Template constraint**: restrict parameter values (e.g., only t3.small/t3.medium).
  - **Notification constraint**: stack events to SNS.
  - **Tag update constraint**, **StackSet constraint** (deploy product to multiple accounts/Regions).
- **TagOptions**: enforce consistent tags on provisioned products.
- End users need `AWSServiceCatalogEndUserFullAccess` + portfolio access (via IAM principal association).
- Update products by publishing new versions; users update provisioned products.
- **AppRegistry**: define applications and attribute groups.

**Scenario:** "Developers must create only approved, compliant EC2/RDS configurations without admin permissions" -> Service Catalog product + launch constraint + template constraint.

---

## Keeping products in sync with a repository
Store product templates in a Git repo with a mapping file (product -> template). A pipeline (CodePipeline -> CodeBuild or Lambda) creates or updates Service Catalog products and new versions on each commit. Users always see the latest approved versions.

---

[← AWS AppConfig](appconfig.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Organizations and SCPs →](organizations.md)
