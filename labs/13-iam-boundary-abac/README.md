[← Lab 12](../12-auto-scaling-lifecycle-hooks/README.md) | [Labs index](../README.md) | [🏠 Home](../../README.md) | [Lab 14 →](../14-guardduty-security-response/README.md)

# Lab 13 - IAM: permissions boundary delegation, ABAC with session tags, Access Analyzer checks

**Goal:**
- let a "team lead" role create IAM roles **only with a permissions boundary**, and prove that even `AdministratorAccess` on such a role can't escape the boundary;
- grant access by **tags** (ABAC) using **session tags**;
- validate policies with **IAM Access Analyzer** the way a pipeline would.

**Exam topics:** permissions boundaries (effective permissions = identity ∩ boundary), `iam:PermissionsBoundary` condition, denying boundary tampering, ABAC with `aws:PrincipalTag` / `aws:ResourceTag`, `sts:TagSession`, policy simulator, Access Analyzer `validate-policy` and custom policy checks.
**Services:** [IAM, STS and Identity Center](../../services/iam-sts-identity-center.md), [Security detection](../../services/security-detection.md)
**Time:** ~1 h | **Cost:** $0 (custom policy checks cost a fraction of a cent each)

Run everything as your normal admin user unless a step says "as the team lead". Prepare the policy files with your account ID:
```bash
cd labs/13-iam-boundary-abac
mkdir -p /tmp/lab13 && for f in policies/*.json; do sed "s/ACCOUNT_ID/$ACCOUNT_ID/g" $f > /tmp/lab13/$(basename $f); done
as_role() { eval "$(aws sts assume-role --role-arn $1 --role-session-name lab13 ${2:+--tags $2} \
  --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' --output text \
  | awk '{print "export AWS_ACCESS_KEY_ID="$1" AWS_SECRET_ACCESS_KEY="$2" AWS_SESSION_TOKEN="$3}')"; aws sts get-caller-identity --query Arn --output text; }
back_to_admin() { unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN; aws sts get-caller-identity --query Arn --output text; }
```
(If you use `aws configure export-credentials` style env vars for your admin session, re-export them instead of `unset`.)

## Part A - Permissions boundary delegation

### A1. Create the boundary, the team-lead policy and the team-lead role
```bash
aws iam create-policy --policy-name DopLab13Boundary --policy-document file:///tmp/lab13/boundary.json
aws iam create-policy --policy-name DopLab13TeamLead --policy-document file:///tmp/lab13/teamlead.json
aws iam create-role --role-name dop-lab13-teamlead --assume-role-policy-document file:///tmp/lab13/trust-account.json
aws iam attach-role-policy --role-name dop-lab13-teamlead --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/DopLab13TeamLead
sleep 10
```

### A2. As the team lead: try to create roles
```bash
as_role arn:aws:iam::$ACCOUNT_ID:role/dop-lab13-teamlead
# 1) without a boundary -> AccessDenied
aws iam create-role --path /app/ --role-name dop-lab13-noboundary --assume-role-policy-document file:///tmp/lab13/trust-lambda.json
# 2) with the required boundary -> works
aws iam create-role --path /app/ --role-name dop-lab13-app --assume-role-policy-document file:///tmp/lab13/trust-lambda.json \
  --permissions-boundary arn:aws:iam::$ACCOUNT_ID:policy/DopLab13Boundary --query Role.Arn
# 3) try to "escalate": attach AdministratorAccess -> allowed (the role has the boundary)
aws iam attach-role-policy --role-name dop-lab13-app --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
# 4) try to remove the boundary or change the boundary policy -> AccessDenied (explicit deny)
aws iam delete-role-permissions-boundary --role-name dop-lab13-app
back_to_admin
```
Expected: 1 and 4 fail with `AccessDenied`; 2 and 3 succeed.

### A3. Prove the boundary caps the role
```bash
aws iam simulate-principal-policy --policy-source-arn arn:aws:iam::$ACCOUNT_ID:role/app/dop-lab13-app \
  --action-names s3:GetObject ec2:RunInstances iam:CreateUser \
  --query 'EvaluationResults[].[EvalActionName,EvalDecision]' --output table
```
Expected: `s3:GetObject allowed`, `ec2:RunInstances implicitDeny`, `iam:CreateUser implicitDeny`. The role has `AdministratorAccess`, but **effective permissions = identity policy ∩ boundary**. This is how you let teams create roles without letting them create an admin role.

## Part B - ABAC with session tags

### B1. Tagged resources and one ABAC role
```bash
aws ssm put-parameter --name /dop-lab13/blue/config --type String --value "blue team config" --tags Key=Project,Value=blue
aws ssm put-parameter --name /dop-lab13/red/config --type String --value "red team config" --tags Key=Project,Value=red
aws iam create-role --role-name dop-lab13-abac --assume-role-policy-document file:///tmp/lab13/trust-account-with-tags.json
aws iam put-role-policy --role-name dop-lab13-abac --policy-name abac --policy-document file:///tmp/lab13/abac.json
sleep 10
```

### B2. Same role, different session tag, different access
```bash
as_role arn:aws:iam::$ACCOUNT_ID:role/dop-lab13-abac Key=Project,Value=blue
aws ssm get-parameter --name /dop-lab13/blue/config --query Parameter.Value   # allowed
aws ssm get-parameter --name /dop-lab13/red/config  --query Parameter.Value   # AccessDenied
back_to_admin
as_role arn:aws:iam::$ACCOUNT_ID:role/dop-lab13-abac Key=Project,Value=red
aws ssm get-parameter --name /dop-lab13/red/config --query Parameter.Value    # allowed now
back_to_admin
```
**One policy, no per-project policies.** A new project only needs tags. In IAM Identity Center, the session tags come from the IdP user attributes ("attributes for access control"). The trust policy needs **`sts:TagSession`** to accept session tags.

## Part C - Access Analyzer policy checks (pipeline style)
```bash
aws accessanalyzer validate-policy --policy-type IDENTITY_POLICY --policy-document file:///tmp/lab13/bad-policy.json \
  --query 'findings[].[findingType,issueCode,findingDetails]' --output table
```
Expected findings:
- an **ERROR** for the invalid action `s3:GetObjects`;
- a **SECURITY_WARNING** for `iam:PassRole` with `Resource: *`;
- a **SUGGESTION** that `dynamodb:GetItem` is redundant next to `dynamodb:*`.

In CI, fail the build on ERROR/SECURITY_WARNING.

Custom policy check: does the team-lead policy grant `iam:CreateUser`?
```bash
aws accessanalyzer check-access-not-granted --policy-type IDENTITY_POLICY \
  --policy-document file:///tmp/lab13/teamlead.json --access '[{"actions":["iam:CreateUser"]}]' --query '[result,message]'
```
Expected: `PASS`. Other checks: `check-no-new-access` (does a policy change grant more than before?) and `check-no-public-access` (resource policies).

## Cleanup
```bash
back_to_admin
aws iam detach-role-policy --role-name dop-lab13-app --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
aws iam delete-role --role-name dop-lab13-app
aws iam detach-role-policy --role-name dop-lab13-teamlead --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/DopLab13TeamLead
aws iam delete-role --role-name dop-lab13-teamlead
aws iam delete-role-policy --role-name dop-lab13-abac --policy-name abac
aws iam delete-role --role-name dop-lab13-abac
aws iam delete-policy --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/DopLab13TeamLead
aws iam delete-policy --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/DopLab13Boundary
aws ssm delete-parameters --names /dop-lab13/blue/config /dop-lab13/red/config
rm -rf /tmp/lab13
```

## Exam takeaways
- **Boundary = maximum**, never grants. Delegate with a condition on `iam:PermissionsBoundary` + deny boundary removal/editing.
- **ABAC** scales with tags: `aws:PrincipalTag/X` == `aws:ResourceTag/X`.
- **Access Analyzer**: validate policies in CI, custom checks, external/unused access findings.
