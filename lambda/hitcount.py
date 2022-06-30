"""Proxy lambda function that uses DynamoDB to log a call to an underlying lambda function."""

import json
import os
import boto3

ddb = boto3.resource('dynamodb')
table: boto3 = ddb.Table(os.environ['HITS_TABLE_NAME'])
_lambda = boto3.client('lambda')


def handler(event, context):
    print(f"request: {json.dumps(event)}")

    # add + 1 to counter in DynamoDB
    table.update_item(
        Key={'path': event['path']},
        UpdateExpression='ADD hits :incr',
        ExpressionAttributeValues={':incr': 1}
    )

    # call downstream lambda function
    resp = _lambda.invoke(
        FunctionName=os.environ['DOWNSTREAM_FUNCTION_NAME'],
        Payload=json.dumps(event)
    )

    # Get body of response of downstream function
    body = resp['Payload'].read()
    print(f'response: {body}')

    return json.loads(body)
