import json
import os

import boto3

codedeploy = boto3.client("codedeploy")
lambda_client = boto3.client("lambda")


def handler(event, context):
    """BeforeAllowTraffic hook: test the NEW version before any traffic reaches it."""
    status = "Succeeded"
    try:
        resp = lambda_client.invoke(
            FunctionName=os.environ["TARGET_VERSION_ARN"],
            Payload=json.dumps({"healthcheck": True}),
        )
        body = json.loads(resp["Payload"].read() or "{}")
        if resp.get("FunctionError") or body.get("statusCode") != 200:
            status = "Failed"
    except Exception as exc:  # any error = fail the deployment
        print("pre-traffic test error:", exc)
        status = "Failed"

    print("pre-traffic test result:", status)
    codedeploy.put_lifecycle_event_hook_execution_status(
        deploymentId=event["DeploymentId"],
        lifecycleEventHookExecutionId=event["LifecycleEventHookExecutionId"],
        status=status,
    )
    return status
