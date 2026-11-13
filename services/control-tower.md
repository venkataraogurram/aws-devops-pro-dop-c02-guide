[← AWS Organizations and SCPs](organizations.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon S3 (events, integrity, protection) →](s3.md)

# AWS Control Tower

**Exam domains:** [Domain 2](../02-config-mgmt-iac.md), [Domain 6](../06-security-compliance.md) | **Hands-on:** none (read-only topic)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

**What:** Sets up and governs a multi-account **landing zone** using Organizations, IAM Identity Center, CloudTrail, Config, Service Catalog, StackSets.

| Component | Detail |
|---|---|
| **Landing zone** | Creates Security OU with **Log Archive** + **Audit** accounts, org CloudTrail, Config in all governed Regions, IAM Identity Center, optional region deny |
| **Controls (guardrails)** | **Preventive** = SCPs/RCPs (e.g., disallow deleting log archive). **Detective** = AWS Config rules (e.g., detect public S3 buckets). **Proactive** = CloudFormation Hooks (block non-compliant resources before they're created). Behaviour: mandatory / strongly recommended / elective |
| **Account Factory** | Provision new accounts with baseline via console / Service Catalog product. **Account Factory Customization (AFC)** = blueprints (CFN/Terraform) applied at creation |
| **AFT (Account Factory for Terraform)** | GitOps account vending: account request in a repo -> pipeline creates + customises accounts with Terraform |
| **CfCT (Customizations for Control Tower)** | CodePipeline that deploys CFN templates + SCPs (manifest file) to accounts/OUs, triggered on lifecycle events |
| **Lifecycle events** | `CreateManagedAccount`, `UpdateManagedAccount`, `RegisterOrganizationalUnit`, etc. in EventBridge -> trigger automation for new accounts |
| **Drift** | Changes made outside Control Tower (e.g., moving account between OUs in Organizations, editing CT SCPs) -> repair / re-register OU |
| **Enroll existing accounts** | Register OU / enroll account (needs `AWSControlTowerExecution` role) |
| **Landing zone versions** | Update landing zone to get new features |

**Scenario:** "Standardise new accounts with network, roles, security tools, least effort" -> Control Tower Account Factory (+ AFC blueprints or CfCT/AFT). "Detect and alert on non-compliance across all accounts" -> CT detective controls / Config + Security Hub. "Block creation of unencrypted resources before they are created" -> CT proactive control (Hook).

---

## Control (guardrail) levels and examples
- **Mandatory**: always on, e.g., disallow changes to the Log Archive bucket policy / public read of log archive.
- **Strongly recommended**: AWS best practices, e.g., detect EBS volumes without encryption, detect root user without MFA.
- **Elective**: common enterprise choices, e.g., disallow S3 delete actions without MFA.
- Detective control finds NON_COMPLIANT resources (e.g., untagged resources) -> SNS/EventBridge -> Lambda notifies or fixes.

## How Control Tower uses other services
- Uses **AWS Config** for detective controls: enables Config in governed Regions, delivers configuration history/snapshots to the **Log Archive** bucket, creates an aggregator in the Audit account.
- Uses **CloudFormation StackSets** to create baseline resources (Config, CloudTrail, roles, logging) in each enrolled account.

## Bringing an existing account under Control Tower
1. Invite/move the account into the organization (if not already).
2. Create the `AWSControlTowerExecution` role in the account (trusted by the management account).
3. Optionally evaluate it first: deploy Config conformance packs that mirror the controls, check results, then remove the temporary Config recorder/delivery channel (Control Tower creates its own).
4. Move the account into a registered OU and **enroll** it (or register the whole OU).

---

[← AWS Organizations and SCPs](organizations.md) | [Services index](README.md) | [🏠 Home](../README.md) | [Amazon S3 (events, integrity, protection) →](s3.md)
