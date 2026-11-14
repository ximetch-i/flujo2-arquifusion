import os
from src.common import publish

def lambda_handler(event, context):
    if event.get('error'):
        err = event['error']
        publish(os.environ['NOTIFICATIONS_TOPIC_ARN'], {'rol':'supervisor','mensaje':'Falló la atención automática de un incidente','error':str(err)}, {'rol':'supervisor','repuesto_faltante':False})
        return {'notified_roles':['supervisor'], 'error_alert':True}
    incident = event.get('incident', event)
    registered = event.get('registro', {}).get('incidente', {})
    assignment = event.get('asignacion', {})
    tech = assignment.get('tecnico') or {}
    check = event.get('repuesto_check', {})
    order = event.get('pedido', {}).get('pedido') or {}
    missing = not bool(check.get('hay_repuesto'))
    base = {
        'machine_id': incident.get('machine_id'), 'incidente_id': registered.get('incidente_id'),
        'tecnico': tech.get('nombre', tech.get('tecnico_id', 'Sin técnico asignado')),
        'repuesto': check.get('repuesto_id', 'No especificado'),
        'pedido_id': order.get('pedido_id'),
        'mensaje': f"Incidente {incident.get('severidad')} en máquina {incident.get('machine_id')}"
    }
    topic = os.environ['NOTIFICATIONS_TOPIC_ARN']
    roles = ['tecnico', 'supervisor', 'operador']
    if missing: roles.append('logistica')
    for role in roles:
        msg = dict(base, rol=role, repuesto_faltante=missing)
        publish(topic, msg, {'rol': role, 'machine_id': base['machine_id'], 'repuesto_faltante': missing})
    return {'notified_roles': roles, 'repuesto_faltante': missing, 'notification': base}
