"""Carga datos mínimos de demostración en las tablas DynamoDB del Flujo 2."""
import boto3
from decimal import Decimal

REGION = 'us-east-1'
ddb = boto3.resource('dynamodb', region_name=REGION)

items = {
    't_maquinas': [
        {'machine_id': 'MAQ-001', 'zona': 'Lima Norte', 'estado': 'OPERATIVA', 'repuesto_requerido': 'REP-001', 'operador_email': 'operador@example.com'}
    ],
    't_tecnicos': [
        {'zona': 'Lima Norte', 'tecnico_id': 'TEC-001', 'nombre': 'Técnico Demo', 'email': 'tecnico@example.com', 'disponibilidad': 'DISPONIBLE'}
    ],
    't_repuestos': [
        {'zona': 'Lima Norte', 'repuesto_id': 'REP-001', 'nombre': 'Filtro industrial', 'stock': 2}
    ]
}

for table_name, rows in items.items():
    t = ddb.Table(table_name)
    for item in rows:
        t.put_item(Item=item)
    print(f'{table_name}: {len(rows)} registro(s) insertado(s)')
