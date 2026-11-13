[← Lab 09](../09-cloudwatch-logs-alarms/README.md) | [Labs index](../README.md) | [🏠 Home](../../README.md) | [Lab 11 →](../11-eventbridge-sqs-dlq/README.md)

# Lab 10 - X-Ray tracing: API Gateway -> Lambda -> DynamoDB

**Goal:** turn on tracing at every hop and read the **trace map**. Find the slow and failing requests, and filter traces by a business value with an **annotation**. Also see what API Gateway returns when the Lambda fails.

**Exam topics:** X-Ray on the API Gateway **stage**, Lambda **active tracing**, SDK instrumentation of downstream calls, annotations (indexed) vs metadata, filter expressions, API Gateway 502 on a failed Lambda proxy integration, IAM-authorised APIs.
**Services:** [X-Ray](../../services/xray.md), [API Gateway](../../services/api-gateway.md), [Lambda](../../services/lambda.md)
**Time:** ~1 h | **Cost:** < $0.05 (X-Ray free tier: 100,000 traces recorded/month)

## Step 1 - Deploy
```bash
cd labs/10-xray-api-gateway-lambda
sam build
sam deploy --stack-name dop-lab10 --capabilities CAPABILITY_IAM --resolve-s3 --no-confirm-changeset
export URL=$(aws cloudformation describe-stacks --stack-name dop-lab10 --query "Stacks[0].Outputs[0].OutputValue" --output text); echo $URL
```

## Step 2 - Call the API (SigV4-signed, no anonymous access)
The API uses **IAM authorization**. `curl` can sign requests itself. First export your current credentials:
```bash
eval "$(aws configure export-credentials --format env)"
sig() { curl -s --aws-sigv4 "aws:amz:$AWS_REGION:execute-api" --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
  ${AWS_SESSION_TOKEN:+-H "x-amz-security-token: $AWS_SESSION_TOKEN"} -w '  HTTP %{http_code}\n' "$1"; }
curl -s -w '  HTTP %{http_code}\n' "$URL?customer=alice"     # unsigned -> 403 (Missing Authentication Token / forbidden)
for c in alice bob carol alice bob; do sig "$URL?customer=$c"; done
sig "$URL?customer=slow"
sig "$URL?customer=fail"
```
Expected:
- the unsigned call gets **403**;
- the signed calls get **200** with an order ID;
- `slow` takes about 2 s;
- `fail` returns **502** (`Internal server error`), because the Lambda proxy integration got an error instead of a valid response.

## Step 3 - Read the traces
Console: **CloudWatch > X-Ray traces > Trace map** (or **Application Signals**, depending on the console version). Wait about a minute after the calls.
- The map shows `Client -> dop-lab10-api/prod -> dop-lab10-order (Lambda) -> DynamoDB`. The Lambda node has a red/orange part for the `fail` call.
- **Traces**: open the `slow` trace. The `business-logic` subsegment takes ~2 s and the DynamoDB `PutItem` is short. That's how you find where the time goes.
- Open the `fail` trace. The exception and stack trace are on the subsegment.

## Step 4 - Filter by annotation
In **Traces**, use the filter expression:
```
annotation.customer_id = "alice"
```
Then try `responsetime > 1` and `fault = true` (or `error = true`). From the CLI:
```bash
aws xray get-trace-summaries --start-time $(( $(date +%s) - 1800 )) --end-time $(date +%s) \
  --filter-expression 'annotation.customer_id = "alice"' --query 'TraceSummaries[].[Id,ResponseTime]' --output table
```
Expected: only alice's traces. **Metadata can't be used in filters.** Only annotations are indexed.

## Step 5 - What enabled each part
| Hop | Setting in `template.yaml` | Exam wording |
|---|---|---|
| API Gateway | `TracingEnabled: true` on the stage | "Enable X-Ray tracing on the API Gateway stage" |
| Lambda | `Tracing: Active` | "Enable active tracing" (+ X-Ray write permissions, which SAM added) |
| DynamoDB call | `patch_all()` from the X-Ray SDK in the code | "Instrument the application with the X-Ray SDK" (or ADOT) |
| ECS/EC2 (not here) | X-Ray daemon / ADOT collector sidecar or agent, UDP 2000 | "Run the X-Ray daemon as a sidecar" |

## Cleanup
```bash
sam delete --stack-name dop-lab10 --no-prompts
aws logs delete-log-group --log-group-name /aws/lambda/dop-lab10-order
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
```

## Exam takeaways
- Tracing must be enabled **per hop**. Downstream AWS calls need SDK/ADOT instrumentation.
- **Annotations** = filterable. **Metadata** = not.
- 502 from API Gateway with Lambda proxy = the function errored or returned a malformed response. **504** = integration timeout (29 s default).
