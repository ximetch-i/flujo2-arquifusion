import os
from boto3.dynamodb.conditions import Key
from src.common import table

def lambda_handler(event, context):
    machine_id = event.get('machine_id')
    if not machine_id: raise ValueError('Falta machine_id')
    result = table('MACHINES_TABLE').get_item(Key={'machine_id': machine_id})
    machine = result.get('Item')
    if not machine:
        # Permite pruebas independientes del Flujo 1; el registro real debe existir al integrar.
        machine = {'machine_id': machine_id, 'zona': event.get('zona'), 'estado': 'DESCONOCIDO', 'repuesto_requerido': event.get('repuesto_id', 'REP-001')}
    return machine
