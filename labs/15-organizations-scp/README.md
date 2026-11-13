[← Lab 14](../14-guardduty-security-response/README.md) | [Labs index](../README.md) | [🏠 Home](../../README.md) | [Lab 16 →](../16-multi-region-dr/README.md)

# Lab 15 (optional) - AWS Organizations: SCPs on a test OU

**Goal:** attach two common SCPs to a test OU and watch them block actions in a member account, even for its administrators. The SCPs are a Region restriction, and protection for CloudTrail/GuardDuty/Config plus "can't leave the org".

**Exam topics:** SCPs set maximum permissions (deny-list strategy with `FullAWSAccess` kept), `NotAction` + `aws:RequestedRegion` for global services, inheritance via OUs, SCPs don't apply to the management account, testing via `OrganizationAccountAccessRole`.
**Services:** [Organizations and SCPs](../../services/organizations.md)
**Time:** ~1 h | **Cost:** $0

## Prerequisites (skip the lab if you don't have these)
- You can sign in to the **management account** of an organization with **all features** enabled. This must be a personal/sandbox org, never a work org.
- A **sandbox member account** you can move into a test OU, and the `OrganizationAccountAccessRole` in it (created automatically for accounts made with `CreateAccount`).
- The member account is **not** managed by Control Tower. Moving Control Tower accounts between OUs outside Control Tower causes drift.

Run these as the management account:
```bash
cd labs/15-organizations-scp
export MEMBER=111122223333          # your sandbox member account ID
ROOT=$(aws organizations list-roots --query 'Roots[0].Id' --output text)
aws organizations enable-policy-type --root-id $ROOT --policy-type SERVICE_CONTROL_POLICY 2>/dev/null || echo "SCPs already enabled"
PARENT=$(aws organizations list-parents --child-id $MEMBER --query 'Parents[0].Id' --output text); echo "member is in $PARENT"
```

## Step 1 - Test OU + SCPs
```bash
OU=$(aws organizations create-organizational-unit --parent-id $ROOT --name dop-lab15-test --query OrganizationalUnit.Id --output text)
P1=$(aws organizations create-policy --type SERVICE_CONTROL_POLICY --name dop-lab15-region-deny \
  --description "Deny everything outside us-east-1 except global services" --content file://scp-region-deny.json --query Policy.PolicySummary.Id --output text)
P2=$(aws organizations create-policy --type SERVICE_CONTROL_POLICY --name dop-lab15-protect-security \
  --description "Protect audit/detection services and block leaving the org" --content file://scp-protect-security.json --query Policy.PolicySummary.Id --output text)
aws organizations attach-policy --policy-id $P1 --target-id $OU
aws organizations attach-policy --policy-id $P2 --target-id $OU
aws organizations move-account --account-id $MEMBER --source-parent-id $PARENT --destination-parent-id $OU
aws organizations list-policies-for-target --target-id $OU --filter SERVICE_CONTROL_POLICY --query 'Policies[].Name'
```
`FullAWSAccess` is still attached at the root (inherited), so these SCPs work as a **deny list** on top of it.

## Step 2 - Test from inside the member account
```bash
eval "$(aws sts assume-role --role-arn arn:aws:iam::$MEMBER:role/OrganizationAccountAccessRole --role-session-name lab15 \
  --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' --output text \
  | awk '{print "export AWS_ACCESS_KEY_ID="$1" AWS_SECRET_ACCESS_KEY="$2" AWS_SESSION_TOKEN="$3}')"
aws sts get-caller-identity --query Arn
aws ec2 describe-vpcs --region us-east-1 --query 'length(Vpcs)'       # allowed
aws ec2 describe-vpcs --region eu-west-1 --query 'length(Vpcs)'       # AccessDenied ... explicit deny in a service control policy
aws iam list-roles --max-items 1 --query 'Roles[0].RoleName'          # allowed: IAM is in NotAction (global service)
aws organizations leave-organization                                  # AccessDenied (SCP), even though this role is admin
aws cloudtrail stop-logging --name any-trail-name                     # AccessDenied (SCP), not "trail not found"
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
```
The member role has `AdministratorAccess`, yet the SCP wins: **explicit deny anywhere = deny**. Run the same `describe-vpcs --region eu-west-1` as the **management account**. It works, because **SCPs never apply to the management account**.

**Why `NotAction` for global services?** Global services (IAM, Organizations, STS global endpoint, CloudFront, Route 53, Support) make requests in `us-east-1`, or with no specific Region. Without the exemption, a Region-deny SCP can break them.

## Cleanup
```bash
aws organizations move-account --account-id $MEMBER --source-parent-id $OU --destination-parent-id $PARENT
aws organizations detach-policy --policy-id $P1 --target-id $OU
aws organizations detach-policy --policy-id $P2 --target-id $OU
aws organizations delete-policy --policy-id $P1
aws organizations delete-policy --policy-id $P2
aws organizations delete-organizational-unit --organizational-unit-id $OU
```

## Exam takeaways
- SCPs **filter**, never grant. Effective = SCP allows (at every level) ∩ IAM allows, minus any explicit deny.
- Use SCPs to **prevent** (Region lock, protect security tooling, block leaving the org, block root access keys). Use Config/Security Hub to **detect**.
- SCPs don't apply to the management account or to service-linked roles. Keep workloads out of the management account.
