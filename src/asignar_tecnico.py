from boto3.dynamodb.conditions import Key
from src.common import table

def lambda_handler(event, context):
    zona = event.get('machine', {}).get('zona') or event.get('zona')
    if not zona: raise ValueError('No se encontró zona para asignar técnico')
    t = table('TECHNICIANS_TABLE')
    result = t.query(KeyConditionExpression=Key('zona').eq(zona))
    candidates = [x for x in result.get('Items', []) if x.get('disponibilidad', 'DISPONIBLE') == 'DISPONIBLE']
    if not candidates:
        return {'tecnico': None, 'asignacion_estado': 'SIN_TECNICO_DISPONIBLE'}
    tech = sorted(candidates, key=lambda x: x.get('tecnico_id',''))[0]
    t.update_item(Key={'zona': zona, 'tecnico_id': tech['tecnico_id']},
        UpdateExpression='SET disponibilidad = :busy',
        ConditionExpression='disponibilidad = :available',
        ExpressionAttributeValues={':busy':'OCUPADO', ':available':'DISPONIBLE'})
    return {'tecnico': tech, 'asignacion_estado': 'ASIGNADO'}
