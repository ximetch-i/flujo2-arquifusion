import os, json, uuid
from datetime import datetime, timezone
import boto3
from boto3.dynamodb.conditions import Key

DDB = boto3.resource('dynamodb')
SNS = boto3.client('sns')

def table(name):
    return DDB.Table(os.environ[name])

def now():
    return datetime.now(timezone.utc).isoformat()

def response(status, body):
    return {'statusCode': status, 'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}, 'body': json.dumps(body, default=str)}

def body_from_event(event):
    if isinstance(event, dict) and 'Records' in event:
        record = event['Records'][0]
        raw = record.get('body', '{}')
        data = json.loads(raw)
        # SNS->SQS puede entregar el sobre SNS si RawMessageDelivery no está habilitado.
        if isinstance(data, dict) and 'Message' in data:
            data = json.loads(data['Message'])
        return data
    if isinstance(event, dict) and 'body' in event and isinstance(event['body'], str):
        return json.loads(event['body'] or '{}')
    return event if isinstance(event, dict) else {}

def publish(topic_arn, message, attributes):
    SNS.publish(TopicArn=topic_arn, Message=json.dumps(message, default=str),
        MessageAttributes={k: {'DataType': 'String', 'StringValue': str(v).lower() if isinstance(v, bool) else str(v)} for k,v in attributes.items()})
