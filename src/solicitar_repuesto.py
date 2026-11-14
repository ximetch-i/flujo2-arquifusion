import uuid
from src.common import table, now

def lambda_handler(event, context):
    incident = event.get('incident', event)
    check = event.get('repuesto_check', {})
    machine = event.get('machine', {})
    repuesto_id = check.get('repuesto_id') or machine.get('repuesto_requerido') or incident.get('repuesto_id')
    if not repuesto_id: raise ValueError('No se puede crear pedido: falta repuesto_id en máquina o mensaje de prueba')
    pedido = {
        'pedido_id': f"PED-{uuid.uuid4().hex[:12].upper()}",
        'repuesto_id': repuesto_id,
        'incidente_id': incident.get('incidente_id', f"INC-{incident.get('machine_id','MAQ')}-{context.aws_request_id[:8]}"),
        'machine_id': incident['machine_id'],
        'cantidad': int(check.get('cantidad', 1)),
        'estado': 'PENDIENTE',
        'fecha': now(),
        'zona': check.get('zona') or machine.get('zona') or incident.get('zona')
    }
    table('ORDERS_TABLE').put_item(Item=pedido, ConditionExpression='attribute_not_exists(pedido_id)')
    return {'pedido': pedido, 'repuesto_faltante': True}
