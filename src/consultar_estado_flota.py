from src.common import table, response

def lambda_handler(event, context):
    params = event.get('queryStringParameters') or {}
    machine_id = params.get('machine_id')
    t = table('MACHINES_TABLE')
    if machine_id:
        item = t.get_item(Key={'machine_id': machine_id}).get('Item')
        items = [item] if item else []
    else:
        result = t.scan()
        items = result.get('Items', [])
        while 'LastEvaluatedKey' in result:
            result = t.scan(ExclusiveStartKey=result['LastEvaluatedKey'])
            items.extend(result.get('Items', []))
    return response(200, {'maquinas': items, 'total': len(items)})
