[Services index](README.md) | [🏠 Home](../README.md) | [AWS CodeBuild →](codebuild.md)

# AWS CodeCommit (and Git sources)

**Exam domains:** [Domain 1](../01-sdlc-automation.md) | **Hands-on:** [Lab 01](../labs/01-codebuild-codepipeline/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

**What:** Managed private Git repos in AWS. Returned to full GA in Nov 2025.

Must-knows:
- Auth: HTTPS Git credentials (IAM user), SSH keys (IAM user), or **git-remote-codecommit** with IAM roles / temporary creds (best for federated users / SSO).
- Access control is **IAM policies** (e.g., deny `codecommit:GitPush` to `refs/heads/main` for developers using a condition on `codecommit:References`). This is how you "protect the main branch".
- **Approval rule templates** = require N approvals on pull requests (like branch protection).
- **Notifications** (via CodeStar Notifications -> SNS / Chatbot) and **triggers** (SNS or Lambda on push).
- **EventBridge** events: `referenceCreated`, `referenceUpdated`, `pullRequestCreated`, `pullRequestSourceBranchUpdated`, etc. Use these to start CodeBuild for PR validation.
- Encrypted at rest with KMS, in transit with HTTPS/SSH.
- Cross-account access: create a role in the repo account, users in other account assume it.

**Pattern: "Run tests on every pull request and post result back to the PR"**
EventBridge rule on `pullRequestCreated` / `pullRequestSourceBranchUpdated` -> CodeBuild project -> Lambda/CodeBuild posts comment and approval state on the PR.
With **GitHub/Bitbucket/GitLab** as source, CodeBuild **webhooks** with filter groups (`PULL_REQUEST_CREATED`, `PULL_REQUEST_UPDATED`, `PUSH`, branch/file filters) do the same natively.

**Other sources:** GitHub, GitHub Enterprise, Bitbucket, GitLab connect to CodePipeline through **AWS CodeConnections** (formerly CodeStar Connections). The connection is created "PENDING" and must be completed in the console (OAuth handshake) once.

---

## Migrating and replicating repositories
- **Migrate** an existing Git repo: `git clone --mirror <old-url>`, then `git push --mirror` (or `--all` + `--tags`) to the CodeCommit URL. No special tool needed.
- **Cross-Region replication** is not a built-in feature. Pattern: EventBridge rule on `referenceCreated` / `referenceUpdated` in the source Region -> CodeBuild project or ECS task that clones the repo and pushes it to a repo in the second Region. Use case: lower-latency pulls for distant teams, or a backup copy.
- **Branch protection** = IAM deny on `GitPush` / `PutFile` / `MergeBranchesBy*` for `refs/heads/main` (condition key `codecommit:References`), plus approval rule templates on pull requests.

## Managed policies and limiting them to one repository
- AWS managed policies: **`AWSCodeCommitFullAccess`** (everything, including create/delete repositories), **`AWSCodeCommitPowerUser`** (full use of repositories, but **can't delete** repositories), **`AWSCodeCommitReadOnly`**.
- Exam pattern: "developers need full use of CodeCommit but must not delete repositories" -> `AWSCodeCommitPowerUser`.
- To limit a managed policy to **one repository**, attach an extra policy with an explicit **Deny** on `codecommit:*` for every repository ARN except the allowed one (`NotResource`), or a Deny with a condition on the branch (`codecommit:References`). An explicit deny overrides the managed policy's allow.

---

[Services index](README.md) | [🏠 Home](../README.md) | [AWS CodeBuild →](codebuild.md)
