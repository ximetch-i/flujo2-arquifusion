import uuid
from src.common import table, now

def lambda_handler(event, context):
    incident = event.get('incident', event)
    machine = event.get('machine', {})
    tech = event.get('asignacion', {}).get('tecnico')
    check = event.get('repuesto_check', {})
    pedido = event.get('pedido', {}).get('pedido')
    item = {
        'incidente_id': incident.get('incidente_id', f"INC-{uuid.uuid4().hex[:12].upper()}"),
        'machine_id': incident['machine_id'], 'zona': machine.get('zona') or incident.get('zona'),
        'severidad': incident.get('severidad'), 'prob_falla': incident.get('prob_falla'),
        'estado': 'ABIERTO', 'fecha': now(),
        'tecnico_id': (tech or {}).get('tecnico_id'),
        'repuesto_id': check.get('repuesto_id'),
        'repuesto_faltante': not bool(check.get('hay_repuesto')),
        'pedido_id': (pedido or {}).get('pedido_id')
    }
    table('INCIDENTS_TABLE').put_item(Item=item)
    return {'incidente': item}
