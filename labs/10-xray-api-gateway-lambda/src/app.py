import json
import os
import time
import uuid

import boto3
from aws_xray_sdk.core import patch_all, xray_recorder

patch_all()  # trace boto3 calls (DynamoDB shows up as its own node in the trace map)
table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def handler(event, context):
    customer = (event.get("queryStringParameters") or {}).get("customer", "anonymous")

    # In Lambda you add annotations to a subsegment you create (not to the Lambda facade segment)
    with xray_recorder.in_subsegment("business-logic") as sub:
        sub.put_annotation("customer_id", customer)          # indexed: searchable in X-Ray
        sub.put_metadata("raw_event_path", event.get("path"))  # stored, not searchable

        if customer == "slow":
            time.sleep(2)                                      # visible as a long subsegment
        if customer == "fail":
            raise RuntimeError("simulated failure")            # API Gateway returns 502 for a failed Lambda proxy call

        order_id = str(uuid.uuid4())
        table.put_item(Item={"id": order_id, "customer": customer, "ts": int(time.time())})

    return {"statusCode": 200, "body": json.dumps({"order_id": order_id, "customer": customer})}
