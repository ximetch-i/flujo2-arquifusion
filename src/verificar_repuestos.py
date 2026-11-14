from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from src.common import table

def lambda_handler(event, context):
    zona = event.get('machine', {}).get('zona') or event.get('zona')
    repuesto_id = event.get('machine', {}).get('repuesto_requerido') or event.get('repuesto_id')
    if not zona or not repuesto_id:
        return {'hay_repuesto': False, 'repuesto_id': repuesto_id, 'cantidad': 1, 'motivo': 'No se indicó repuesto requerido'}
    t = table('PARTS_TABLE')
    result = t.query(KeyConditionExpression=Key('zona').eq(zona))
    item = next((x for x in result.get('Items', []) if x.get('repuesto_id') == repuesto_id), None)
    if not item or int(item.get('stock', 0)) < 1:
        return {'hay_repuesto': False, 'repuesto_id': repuesto_id, 'cantidad': 1, 'zona': zona}
    # Reserva una unidad atómicamente para que dos incidentes no consuman el mismo stock.
    try:
        t.update_item(Key={'zona': zona, 'repuesto_id': repuesto_id},
            UpdateExpression='SET stock = stock - :one',
            ConditionExpression='stock >= :one',
            ExpressionAttributeValues={':one': 1})
        return {'hay_repuesto': True, 'repuesto_id': repuesto_id, 'cantidad': 1, 'zona': zona}
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {'hay_repuesto': False, 'repuesto_id': repuesto_id, 'cantidad': 1, 'zona': zona}
        raise
