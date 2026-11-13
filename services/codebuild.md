[← AWS CodeCommit (and Git sources)](codecommit.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS CodePipeline →](codepipeline.md)

# AWS CodeBuild

**Exam domains:** [Domain 1](../01-sdlc-automation.md), [Domain 5](../05-incident-event-response.md) | **Hands-on:** [Lab 01](../labs/01-codebuild-codepipeline/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

**What:** Fully managed build service. Runs your commands in a fresh container per build. Pay per build minute. No build servers to manage.

## buildspec.yml (memorise this structure)

```yaml
version: 0.2

env:
  variables:                     # plain text, NOT for secrets
    APP_ENV: "test"
  parameter-store:               # value pulled from SSM Parameter Store at build start
    DB_USER: "/myapp/db/user"
  secrets-manager:               # secret-id:json-key:version-stage:version-id
    DB_PASS: "prod/myapp/db:password"
  exported-variables:            # make vars available to later pipeline actions
    - IMAGE_TAG
  git-credential-helper: yes

phases:
  install:
    runtime-versions:
      python: 3.12
    commands:
      - pip install -r requirements.txt
  pre_build:
    commands:
      - aws ecr get-login-password | docker login --username AWS --password-stdin $REPO_URI
      - export IMAGE_TAG=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c1-7)
  build:
    commands:
      - pytest --junitxml=reports/junit.xml --cov --cov-report=xml
      - docker build -t $REPO_URI:$IMAGE_TAG .
  post_build:
    commands:
      - docker push $REPO_URI:$IMAGE_TAG
      - printf '[{"name":"web","imageUri":"%s"}]' $REPO_URI:$IMAGE_TAG > imagedefinitions.json
    finally:
      - echo "always runs"

reports:                         # test + coverage reports shown in console
  pytest-reports:
    files: ["reports/junit.xml"]
    file-format: JUNITXML
  coverage:
    files: ["coverage.xml"]
    file-format: COBERTURAXML

artifacts:
  files:
    - imagedefinitions.json
    - appspec.yml
    - scripts/**/*

cache:
  paths:
    - '/root/.cache/pip/**/*'
```

Phase order: **install -> pre_build -> build -> post_build**. If `install` or `pre_build` fails, the build stops (build and post_build are skipped). If `build` fails, `post_build` **still runs** (check `$CODEBUILD_BUILD_SUCCEEDING`, 1 or 0). A phase's `finally` block runs even when that phase's commands fail.

## Must-knows

| Topic | Fact |
|---|---|
| Secrets | Use `parameter-store` / `secrets-manager` in buildspec or project env vars of type PARAMETER_STORE / SECRETS_MANAGER. Service role needs `ssm:GetParameters` / `secretsmanager:GetSecretValue` (+ `kms:Decrypt` for CMK). Never plain-text vars. |
| Docker builds | Enable **privileged mode** on the project to run the Docker daemon (docker build). |
| Caching | **S3 cache** (shared across hosts, survives) or **local cache**: source cache, Docker layer cache, custom cache. Speeds up dependency download. |
| VPC | Build inside your VPC to reach private RDS/ElastiCache etc. Needs **private subnets + NAT gateway** (or VPC endpoints) for internet/AWS APIs. CodeBuild in a public subnet does NOT get a public IP. |
| Timeout | Build timeout 5 min to 36 hours (default 60 min). Separate **queued timeout**. |
| Logs | CloudWatch Logs and/or S3. Build metrics in CloudWatch (`AWS/CodeBuild`). |
| Reports | Test reports: JUnit XML, NUnit, TestNG, Cucumber JSON, Visual Studio TRX. Coverage: JaCoCo, Cobertura, Clover, SimpleCov, LCOV. |
| Batch builds | Build graph / build list / build matrix: parallel builds with different env or images. |
| Compute | EC2 on-demand, **reserved capacity fleets**, Lambda compute (fast start, short builds), custom images from ECR, Windows/ARM/GPU. |
| Local debugging | CodeBuild local agent (run buildspec on your machine), **Session Manager** debug (pause build with `codebuild-breakpoint`). |
| Events | Build state change events in EventBridge (`CodeBuild Build State Change`) -> SNS/Chatbot notifications. |
| Artifacts encryption | Uses KMS (default `aws/s3` key or a CMK). Cross-account pipelines need a CMK. |

**Traps**
- "Build can't reach the internet after being placed in VPC" -> add NAT gateway / endpoints, not a public subnet.
- "Docker daemon not running" -> privileged mode.
- "Build is slow downloading dependencies" -> enable caching (S3 or local), or use CodeArtifact as a proxy cache.
- "Store DB password for build" -> Secrets Manager / Parameter Store SecureString referenced in buildspec.

---

## Triggers, badges and local builds
- **Ways to start a build**: from CodePipeline; EventBridge rule (CodeCommit events, schedules); Lambda calling `StartBuild`; **webhooks** for GitHub / GitHub Enterprise / Bitbucket / GitLab with filter groups (event type, branch, file path, actor).
- **Validate pull requests**: webhook filter on `PULL_REQUEST_CREATED`, `PULL_REQUEST_UPDATED`, `PULL_REQUEST_REOPENED`; CodeBuild reports the status back to the PR (GitHub/Bitbucket). For CodeCommit use EventBridge PR events -> CodeBuild -> post a comment/approval.
- **Build badges**: an embeddable image URL that shows the latest build status for a branch (shown in a README). Enable on the project.
- **Local builds**: run the CodeBuild agent image locally with `codebuild_build.sh` to test a buildspec before pushing.
- **Security**: build in a VPC for private resources; secrets from Secrets Manager / Parameter Store; artifacts encrypted with KMS; service role permissions; CloudTrail logs CodeBuild API calls.

---

[← AWS CodeCommit (and Git sources)](codecommit.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS CodePipeline →](codepipeline.md)
