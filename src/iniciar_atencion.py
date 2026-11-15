import os, json, uuid, boto3
from src.common import body_from_event

sfn = boto3.client('stepfunctions')

def lambda_handler(event, context):
    # Un mensaje SQS por invocación; el mapping usa batchSize=1 para evitar duplicados parciales.
    incident = body_from_event(event)

    required = ['machine_id', 'severidad']
    missing = [k for k in required if not incident.get(k)]

    if missing:
        raise ValueError(f'Mensaje de incidente incompleto. Faltan: {missing}')

    if incident.get('severidad') != 'urgente':
        return {'ignored': True, 'reason': 'La severidad no es urgente'}

    incident.setdefault('incidente_id', f"INC-{uuid.uuid4().hex[:12].upper()}")

    execution_name = f"{incident['machine_id']}-{context.aws_request_id}"[:80]

    result = sfn.start_execution(
        stateMachineArn=os.environ['STATE_MACHINE_ARN'],
        name=execution_name,
        input=json.dumps(incident)
    )

    return {
        'started': True,
        'executionArn': result['executionArn'],
        'incident': incident
    }
