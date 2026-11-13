[← AWS Lambda deployments](lambda.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Step Functions and Lambda automation →](step-functions.md)

# Amazon API Gateway

**Exam domains:** [Domain 1](../01-sdlc-automation.md), [Domain 3](../03-resilient-cloud.md) | **Hands-on:** [Lab 10](../labs/10-xray-api-gateway-lambda/README.md)

> Exam scenarios for this service are in each domain's quick-map table, and confusing pairs are in [Chapter 7](../07-service-comparisons-numbers.md).

## API Gateway deployments
- Stages (dev/test/prod), stage variables (point to Lambda alias `${stageVariables.alias}`).
- **Canary release** on a stage: % of traffic to the canary deployment, then promote.
- Also: Route 53 weighted between two APIs / custom domain base path mappings.

## Integrations and endpoint types
- **Integrations**: Lambda (proxy or custom), **HTTP** (any backend, e.g., ALB or on-prem), **AWS service** (call SQS `SendMessage`, Step Functions `StartExecution`, Kinesis `PutRecord` directly, no Lambda in the middle), mock.
- **Endpoint types**: **Edge-optimized** (default for REST, uses CloudFront edge for global clients), **Regional** (clients in the same Region, or put your own CloudFront in front), **Private** (only from your VPC through an interface VPC endpoint + resource policy).
- **Security**: IAM (SigV4) + resource policies (cross-account, IP, VPC endpoint), **Cognito user pools** authorizer, **Lambda authorizer** (token or request), API keys + usage plans (throttling/quotas, not real auth), WAF on REST APIs, mutual TLS with custom domains, ACM certificates (edge-optimized custom domains need the cert in **us-east-1**).

## Stages, stage variables and Lambda aliases
- Changes go live only after a **deployment** to a **stage** (`dev`, `test`, `prod`). Each stage has its own settings (logging, caching, throttling) and deployment history for rollback.
- **Stage variables** are like environment variables for a stage. Common use: Lambda ARN `...:function:my-fn:${stageVariables.lambdaAlias}` so `dev` stage calls the `dev` alias and `prod` calls `prod`. You must grant API Gateway `lambda:InvokeFunction` on each alias.
- **Canary deployment** on a stage: send X% of traffic to the new deployment, watch separate canary metrics/logs, then promote.
- Import/export **OpenAPI** definitions. **Request validation** (required params/headers, JSON body against a model schema) rejects bad requests with 400 before calling the backend.

## Caching, logging, throttling, errors
- Cache per stage: **TTL default 300 s, max 3600 s, 0 = off**. Cache size 0.5 GB-237 GB. Can be overridden per method.
- **Invalidate**: flush the whole stage cache in the console/API, or a client sends `Cache-Control: max-age=0` (needs `execute-api:InvalidateCache` permission if you require authorization, which you should).
- **Logging**: CloudWatch execution logs (ERROR/INFO, full request/response) and **access logs** (custom format), plus **X-Ray** tracing per stage.
- **Metrics**: `Count`, `CacheHitCount`, `CacheMissCount`, `Latency` (full time), `IntegrationLatency` (backend time), `4XXError`, `5XXError`.
- **Throttling**: account limit **10,000 rps with 5,000 burst** per Region (soft). Stage and method limits, usage plans per API key. Throttled clients get **429**.
- **Errors**: 400 bad request, 403 access denied / WAF blocked, **429** throttled or quota exceeded; **502** bad gateway (often a malformed Lambda proxy response), **503** service unavailable, **504** integration timeout (default **29 s** for REST).

---

[← AWS Lambda deployments](lambda.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Step Functions and Lambda automation →](step-functions.md)
