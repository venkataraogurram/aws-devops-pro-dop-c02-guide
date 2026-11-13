[← Lab 13](../13-iam-boundary-abac/README.md) | [Labs index](../README.md) | [🏠 Home](../../README.md) | [Lab 15 →](../15-organizations-scp/README.md)

# Lab 14 - GuardDuty findings and CloudTrail API calls -> EventBridge -> automated response

**Goal:** generate GuardDuty **sample findings**, route only **high-severity** ones to email and a responder Lambda, and alert on a sensitive **API call** (`CreateAccessKey`) through the CloudTrail -> EventBridge integration. Optionally see the findings aggregated in Security Hub.

**Exam topics:** GuardDuty detector and findings format/severity, numeric filtering on severity, EventBridge targets (SNS + Lambda), automated response design (isolate instance, disable key), "AWS API Call via CloudTrail" events (need a trail; IAM events arrive in **us-east-1**), log file validation.
**Services:** [Security detection](../../services/security-detection.md), [EventBridge](../../services/eventbridge.md), [CloudTrail](../../services/cloudtrail.md)
**Time:** ~1 h | **Cost:** ~$0 (GuardDuty and Security Hub have 30-day free trials; disable them afterwards if you don't want them)

**Run this lab in `us-east-1`.** The IAM API-call rule only fires there.

## Step 1 - Prerequisites check
```bash
export AWS_REGION=us-east-1 AWS_DEFAULT_REGION=us-east-1
aws guardduty list-detectors --query DetectorIds                                   # empty = GuardDuty off in this Region
aws cloudtrail describe-trails --query 'trailList[].[Name,IsMultiRegionTrail,HomeRegion]' --output table
aws cloudtrail get-trail-status --name <trail-name> --query IsLogging              # for each trail listed
```
- No trail that is logging? Deploy with `CreateTrail=true` (creates a multi-Region trail with log file validation).
- GuardDuty off? Turn it on (starts the 30-day free trial in this Region):
  `aws guardduty create-detector --enable --query DetectorId --output text`

## Step 2 - Deploy the rules
```bash
cd labs/14-guardduty-security-response
aws cloudformation deploy --stack-name dop-lab14 --template-file template.yaml --capabilities CAPABILITY_IAM \
  --parameter-overrides NotificationEmail=you@example.com CreateTrail=false     # or true, see step 1
```
Confirm the SNS subscription email.

## Step 3 - Generate sample findings
```bash
D=$(aws guardduty list-detectors --query 'DetectorIds[0]' --output text)
aws guardduty create-sample-findings --detector-id $D \
  --finding-types 'CryptoCurrency:EC2/BitcoinTool.B!DNS' 'UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS' 'Recon:EC2/PortProbeUnprotectedPort'
aws guardduty list-findings --detector-id $D --finding-criteria '{"Criterion":{"service.additionalInfo.sample":{"Eq":["true"]}}}' --query 'FindingIds' | head
```
Within about 5 minutes:
- **Emails** arrive for the high-severity types only. `PortProbeUnprotectedPort` is lower severity and doesn't match `severity >= 7`. (Check each sample's actual severity in the console. Sample severities are fixed per type.)
- **Responder logs** show what an automated response would do:
  ```bash
  aws logs tail /aws/lambda/dop-lab14-responder --since 15m --format short
  ```
  Expected: `WOULD isolate i-99999999 ...` for the EC2 finding and `WOULD deactivate access key ...` for the IAM one. Sample findings point to fake resources, so the lab responder only prints.

**Finding names:** `ThreatPurpose:ResourceType/ThreatFamily.DetectionMechanism!Artifact`, e.g. `CryptoCurrency:EC2/BitcoinTool.B!DNS`.

## Step 4 - Alert on a sensitive API call
Create (and immediately delete) an access key for a throwaway IAM user:
```bash
aws iam create-user --user-name dop-lab14-temp
KEY=$(aws iam create-access-key --user-name dop-lab14-temp --query AccessKey.AccessKeyId --output text)
aws iam delete-access-key --user-name dop-lab14-temp --access-key-id $KEY
aws iam delete-user --user-name dop-lab14-temp
```
Within a few minutes you get **"CreateAccessKey called by arn:aws:...:user/you for user dop-lab14-temp"**. The path: IAM API call -> CloudTrail -> EventBridge (default bus in us-east-1) -> rule -> SNS. Faster than querying CloudTrail logs in S3. The same pattern catches `StopLogging`, `DeleteTrail`, `AuthorizeSecurityGroupIngress`, `PutBucketPolicy`, root logins, and so on.

## Step 5 (optional) - Security Hub aggregation
```bash
aws securityhub enable-security-hub --enable-default-standards
sleep 300
aws securityhub get-findings --filters '{"ProductName":[{"Value":"GuardDuty","Comparison":"EQUALS"}]}' --max-items 5 \
  --query 'Findings[].[Types[0],Severity.Label,Title]' --output table
```
GuardDuty findings show up in Security Hub in the ASFF format, next to the security standard control results (FSBP/CIS). Across an org: a **delegated administrator** + **cross-Region aggregation**.

## Cleanup
```bash
aws guardduty archive-findings --detector-id $D --finding-ids $(aws guardduty list-findings --detector-id $D --finding-criteria '{"Criterion":{"service.additionalInfo.sample":{"Eq":["true"]}}}' --query 'FindingIds' --output text)
aws cloudformation delete-stack --stack-name dop-lab14
aws cloudformation wait stack-delete-complete --stack-name dop-lab14
aws logs delete-log-group --log-group-name /aws/lambda/dop-lab14-responder
# only if you turned them on for this lab and don't want them:
# aws guardduty delete-detector --detector-id $D
# aws securityhub disable-security-hub
```
If you deployed with `CreateTrail=true`, the stack deletion fails on the non-empty trail bucket. Empty it with `aws s3 rm s3://<TrailBucketName> --recursive` and delete the stack again.

## Exam takeaways
- Detect (GuardDuty) -> route (EventBridge, filter by type/severity) -> respond (Lambda / Step Functions / SSM Automation) -> notify (SNS).
- **Isolation pattern**: swap security groups to an isolation SG, snapshot EBS, tag, keep the instance for forensics, investigate with Detective.
- "AWS API Call via CloudTrail" rules need a **trail with logging on**. Global-service events (IAM, STS global endpoint, CloudFront, Route 53) arrive in **us-east-1**.
