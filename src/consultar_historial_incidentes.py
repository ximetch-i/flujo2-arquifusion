from boto3.dynamodb.conditions import Key
from src.common import table, response

def lambda_handler(event, context):
    params = event.get('queryStringParameters') or {}
    machine_id = params.get('machine_id')
    t = table('INCIDENTS_TABLE')
    if machine_id:
        result = t.query(IndexName='MachineHistoryIndex', KeyConditionExpression=Key('machine_id').eq(machine_id), ScanIndexForward=False)
        items = result.get('Items', [])
        while 'LastEvaluatedKey' in result:
            result = t.query(IndexName='MachineHistoryIndex', KeyConditionExpression=Key('machine_id').eq(machine_id), ScanIndexForward=False, ExclusiveStartKey=result['LastEvaluatedKey'])
            items.extend(result.get('Items', []))
    else:
        result = t.scan()
        items = result.get('Items', [])
        while 'LastEvaluatedKey' in result:
            result = t.scan(ExclusiveStartKey=result['LastEvaluatedKey'])
            items.extend(result.get('Items', []))
        items.sort(key=lambda x: x.get('fecha',''), reverse=True)
    return response(200, {'incidentes': items, 'total': len(items)})
