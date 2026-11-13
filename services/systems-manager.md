[← AWS SAM and AWS CDK](sam-cdk.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Config →](config.md)

# AWS Systems Manager

**Exam domains:** [Domain 2](../02-config-mgmt-iac.md), [Domain 4](../04-monitoring-logging.md), [Domain 5](../05-incident-event-response.md) | **Hands-on:** [Lab 07](../labs/07-systems-manager-fleet/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

**Prerequisites for a managed node** (classic troubleshooting question: "instance not showing in Fleet Manager / Run Command"):
1. **SSM Agent** installed and running (pre-installed on Amazon Linux, Windows AMIs, Ubuntu snaps).
2. **IAM instance profile** with `AmazonSSMManagedInstanceCore` (or enable **Default Host Management Configuration**, which gives EC2 instances permissions without an instance profile, needs IMDSv2).
3. **Network** to `ssm`, `ssmmessages`, `ec2messages` endpoints: internet/NAT, or **interface VPC endpoints** for private subnets (+ S3 gateway endpoint for patches/logs).
4. On-premises: create a **hybrid activation** (activation code + ID), register; nodes appear with `mi-` prefix.

| Capability | What | Key exam points |
|---|---|---|
| **Run Command** | Run a document (e.g., `AWS-RunShellScript`, `AWS-RunPowerShellScript`) on many nodes | Targets by tags/resource groups; **rate control** (concurrency, error threshold); output to S3/CloudWatch; no SSH needed |
| **State Manager** | **Associations** that keep nodes in a desired state on a schedule | Install/keep agents (CloudWatch agent, CodeDeploy agent), enforce config, run Ansible playbooks/Chef recipes (`AWS-ApplyAnsiblePlaybooks`, `AWS-ApplyChefRecipes`), join domain. Re-applied on schedule = drift correction |
| **Patch Manager** | Scan/install OS (and some app) patches | **Patch baselines** (predefined per OS or custom: approval rules, auto-approve after N days, approved/rejected lists, compliance severity), **patch groups** (tag key `Patch Group` or `PatchGroup`), `AWS-RunPatchBaseline` document with Operation `Scan` or `Install`, **Maintenance Windows** for timing, **Patch policies (Quick Setup)** for org-wide multi-account/multi-Region patching. Compliance results in Compliance / Security Hub |
| **Maintenance Windows** | Schedule tasks (Run Command, Automation, Lambda, Step Functions) in a time window | Patching on Sunday 2-4 AM; max concurrency/errors |
| **Automation** | Runbooks (documents) with steps (`aws:executeAwsApi`, `aws:runCommand`, `aws:approve`, `aws:executeScript`, `aws:branch`) | Remediation for Config rules, EventBridge targets, AMI baking (`AWS-UpdateLinuxAmi`), `AWS-RestartEC2Instance`, `AWS-StopEC2Instance`, `AWS-DisablePublicAccessForSecurityGroup`, `AWS-ConfigureS3BucketLogging`. **Multi-account / multi-Region** execution. Approval steps. Rate control |
| **Inventory** | Collect software, files, network config, Windows roles/updates, custom inventory | **Resource Data Sync** to S3 -> **Athena / QuickSight** for org-wide reports |
| **Compliance** | Patch + association compliance status | Feed to Security Hub / Config |
| **Session Manager** | Browser/CLI shell to instances; **no SSH keys, no open port 22, no bastion** | IAM-controlled; **session logging to S3 / CloudWatch Logs** (KMS encrypted); port forwarding; audit in CloudTrail |
| **Parameter Store** | Hierarchical config/secrets | Standard (free, 4 KB, 10,000 params/Region) vs Advanced (8 KB, 100,000, **parameter policies**: expiration, notification). SecureString with KMS. **Public parameters** (latest AMI IDs). Versioned. EventBridge events on change |
| **Distributor** | Package and distribute software (agents) | `AWS-ConfigureAWSPackage` |
| **Fleet Manager** | UI to manage nodes (files, processes, users, logs) | |
| **OpsCenter** | **OpsItems** = operational issues aggregated (from CloudWatch alarms, Config, EventBridge, Security Hub) with runbooks to fix | "Central place for ops engineers to see and remediate issues" |
| **Incident Manager** | Response plans, on-call contacts/escalation, chat channels, runbooks, post-incident analysis | Closed to new customers (Nov 2025) - know concept |
| **Change Manager** | Change requests with approvals, change calendar | Controlled changes |
| **Change Calendar** | Block automation during business events | "Don't patch during Black Friday" |
| **Explorer** | Ops dashboard across accounts/Regions | |
| **Application Manager** | App-level view (CFN stacks, resource groups) | |
| **Quick Setup** | One-click org-wide setup (host management, patch policies, DHMC, Config recording) | Least overhead for org-wide SSM baseline |

**Scenario examples**
- "Run a script on 2,000 instances, stop if more than 5% fail" -> Run Command with rate control (concurrency + error threshold).
- "Ensure CloudWatch agent is always installed and configured on all instances, including new ones" -> State Manager association (tag-based target) + config in Parameter Store.
- "Patch all instances in 40 accounts monthly and report compliance centrally" -> Quick Setup patch policy (or Maintenance Window + `AWS-RunPatchBaseline`) + Resource Data Sync / Security Hub.
- "Engineers must not SSH; all sessions recorded" -> Session Manager with S3/CloudWatch logging, remove port 22.
- "Collect installed software list across all accounts and query" -> Inventory + Resource Data Sync to S3 + Athena.

---

## Tags, resource groups and documents
- **Tags** + **Resource Groups** (group resources by tag or CloudFormation stack) are how SSM targets fleets. **Tag Editor** finds and tags resources across Regions in bulk.
- **SSM Documents** (JSON/YAML): `Command` (Run Command, State Manager), `Automation` (runbooks), `Session`, `Package` (Distributor), `Policy`. AWS provides hundreds; you can write and share your own (e.g., "install Apache").

## Hybrid and edge
- **Hybrid activation** for on-premises servers/VMs: create an activation (code + ID, with an IAM service role), install SSM Agent, register. Nodes show as `mi-...`.
- **Automate activations**: for many servers, a Lambda or script creates activations on demand (e.g., called from the server's bootstrap) and stores codes in Parameter Store/Secrets Manager.
- **IoT Greengrass** core devices can be managed by SSM through the Greengrass Systems Manager Agent component.

## OpsCenter example: clean up old EBS volumes
EventBridge schedule -> Lambda lists unattached EBS volumes older than N days -> creates **OpsItems** -> an operator (or automation) runs the `AWS-CreateSnapshot` / `AWS-DeleteSnapshot` (or delete volume) runbook from the OpsItem. Good example of "central operational work + runbooks + cost saving".

## Session Manager in a private subnet (no internet)
Needs interface VPC endpoints for `ssm`, `ssmmessages` (and `ec2messages` for older agents), plus `logs`/`kms` endpoints and an S3 gateway endpoint if session logging/encryption is used.

---

[← AWS SAM and AWS CDK](sam-cdk.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Config →](config.md)
