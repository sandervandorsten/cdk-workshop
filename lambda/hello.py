"""Simple Hello World Lambda function"""

import json


def handler(event, context):
    print(f"request: {json.dumps(event)}")

    try:
        msg = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/plain"
            },
            "body": f"maat, CDK! You have hit the following URL: {event['path']}\n"
        }
        return msg
    except Exception as exc:
        print(exc)
