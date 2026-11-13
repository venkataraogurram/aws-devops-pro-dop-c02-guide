[← AWS CloudFormation](cloudformation.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Systems Manager →](systems-manager.md)

# AWS SAM and AWS CDK

**Exam domains:** [Domain 2](../02-config-mgmt-iac.md) | **Hands-on:** [Lab 03](../labs/03-sam-lambda-canary/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

**SAM**
- `Transform: AWS::Serverless-2016-10-31`; resource types `AWS::Serverless::Function`, `::Api`, `::HttpApi`, `::SimpleTable`, `::LayerVersion`, `::StateMachine`, `::Application` (nested from Serverless Application Repository).
- CLI: `sam init`, `sam build`, `sam local invoke` / `sam local start-api` (Docker), `sam deploy --guided`, `sam sync --watch` (fast dev), `sam pipeline init` (generate CI/CD pipeline), `sam logs`.
- `DeploymentPreference` = CodeDeploy canary/linear for Lambda (see [Lambda deployments](lambda.md)).
- `Policies:` with SAM policy templates (e.g., `DynamoDBReadPolicy`) = easy least privilege.

**CDK**
- Constructs: **L1** (`Cfn*`, 1:1 with CFN), **L2** (intent-based with defaults, e.g., `s3.Bucket`, `bucket.grantRead(fn)`), **L3 / patterns** (e.g., `ApplicationLoadBalancedFargateService`).
- App -> Stacks -> Constructs. `cdk init`, `cdk synth` (template), `cdk diff`, `cdk deploy`, `cdk destroy`.
- **`cdk bootstrap`** creates the `CDKToolkit` stack (S3 asset bucket, ECR repo, deploy roles) per account/Region. Cross-account deploy: bootstrap target with `--trust <tools-account>`.
- **CDK Pipelines** (`pipelines.CodePipeline`): self-mutating pipeline that updates itself when you change the pipeline code; add stages/waves per account/Region.
- **Aspects** to apply rules to all constructs (e.g., enforce encryption, add tags). **cdk-nag** for compliance checks.
- Unit test infra with `assertions` module (`Template.fromStack`).

---

## SAM Accelerate (`sam sync`)
- `sam sync` - sync code and infrastructure.
- `sam sync --code` - push only code changes and skip CloudFormation (updates in seconds). Dev use only.
- `sam sync --code --resource AWS::Serverless::Function` - only Lambda functions and their dependencies; `--resource-id <LogicalId>` for one resource.
- `sam sync --watch` - watch files and sync automatically on change.

## CDK vs SAM
| | SAM | CDK |
|---|---|---|
| Focus | Serverless (Lambda, API Gateway, DynamoDB, Step Functions) | Any AWS resource |
| Authoring | Declarative YAML/JSON | Programming languages |
| Output | CloudFormation (via the SAM transform) | CloudFormation (via `cdk synth`) |
| Getting started | `sam init` templates | `cdk init` |

You can use **SAM CLI to test CDK apps locally**: run `cdk synth`, then `sam local invoke -t cdk.out/MyStack.template.json MyFunction`.

---

[← AWS CloudFormation](cloudformation.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Systems Manager →](systems-manager.md)
