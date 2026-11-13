[← Amazon ECR](ecr.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Amplify (web and mobile app hosting) →](amplify.md)

# EC2 Image Builder

**Exam domains:** [Domain 1](../01-sdlc-automation.md), [Domain 2](../02-config-mgmt-iac.md) | **Hands-on:** none (read-only topic)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

**What:** Managed pipeline that builds, tests, and distributes AMIs or container images on a schedule.

Pieces:
- **Image recipe** (AMI) or **container recipe** = base image + **components**.
- **Components** = YAML documents (AWSTOE) with build and test phases (install agents, harden with CIS/STIG components, run tests).
- **Infrastructure configuration** = instance type, subnet, security group, IAM instance profile (needs `EC2InstanceProfileForImageBuilder` + `AmazonSSMManagedInstanceCore`), SNS topic, logs to S3.
- **Distribution settings** = copy AMI to other Regions, share with accounts/OUs, update a **launch template** with the new AMI ID, export to S3.
- **Pipeline** = schedule (cron) or "run when base image / components have updates".
- Integrates with **Inspector** for vulnerability scanning of the output image.
- **Lifecycle policies** deprecate/delete old AMIs and snapshots.

**Typical exam flow:** Image Builder builds monthly patched AMI -> distribution updates launch template -> SNS/EventBridge triggers -> ASG **instance refresh** to roll the new AMI.
Older pattern (still valid): SSM Automation runbook `AWS-UpdateLinuxAmi` / `AWS-UpdateWindowsAmi`, store AMI ID in **Parameter Store**, CFN references `{{resolve:ssm:/golden/ami}}` or `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>`.

---

## Sharing and tracking images
- Share AMIs, components, recipes with other accounts/OUs with **AWS RAM** (or distribution settings that share/copy the AMI to accounts and Regions).
- **Track the latest AMI**: Image Builder publishes to an **SNS topic** when an image is built -> Lambda writes the new AMI ID to **Parameter Store** -> CloudFormation templates/launch templates reference the parameter. (Distribution settings can also update a launch template directly.)
- Image Builder can be part of a CI/CD flow: CodePipeline triggers the image pipeline, then tests and deploys the new AMI.

---

[← Amazon ECR](ecr.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Amplify (web and mobile app hosting) →](amplify.md)
