# ArquiFusion Corp — Flujo 2: Atención de incidentes

Implementación inicial del diagrama `Flujo 2 - Atención de incidentes`.
Incluye las 9 Lambdas, Step Functions, SNS, SQS + DLQ, DynamoDB y API Gateway.

## Cuenta y región

- Cuenta AWS esperada: `107681881936`
- Región: `us-east-1`
- Stage: `dev`
- Runtime: Python 3.12
- Rol IAM: rol preexistente `LabRole` (no se crea ningún rol IAM nuevo).

> La definición de Step Functions contiene ARNs de Lambda con la cuenta indicada y nombres `flujo2-dev-*`. Despliega con `--stage dev` en esa cuenta y región. Si cambias de cuenta, región o stage, actualiza los ARNs del estado en `serverless.yml`.

## Arquitectura implementada

1. `TemaIncidentes` → `ColaIncidentes` → `IniciarAtencion`.
2. `ColaIncidentes` tiene `ColaIncidentesDLQ` y `maxReceiveCount: 3`.
3. `IniciarAtencion` valida el evento y ejecuta `FlujoAtencionIncidente`.
4. Step Functions ejecuta `ConsultarEstadoMaquina` → `AsignarTecnico` → `VerificarRepuestos`.
5. Si hay stock, reserva una unidad de forma condicional. Si no hay stock, `SolicitarRepuesto` crea un registro `PENDIENTE` en `t_pedidos_repuesto`.
6. `RegistrarIncidente` guarda el incidente y `NotificarIncidente` publica notificaciones en `TemaNotificaciones`.
7. SNS filtra los mensajes por atributos `rol` y `repuesto_faltante` para técnico, supervisor, logística y operador.
8. API Gateway expone `GET /maquinas` y `GET /incidentes`. Se puede filtrar por `?machine_id=MAQ-001`.

## Requisitos previos en EC2

Instala Node.js/npm, Python 3.12, AWS CLI y Serverless Framework 3.40.0. Configura credenciales temporales de Learner Lab en la EC2 con `aws configure` o variables de entorno. No subas credenciales al repositorio.

```bash
npm install -g serverless@3.40.0
aws sts get-caller-identity
```

La identidad debe corresponder a la cuenta `107681881936` y la región debe ser `us-east-1`.

## Configurar correos SNS

Antes de desplegar, define los correos reales que recibirán cada rol:

```bash
export EMAIL_TECNICO='correo-tecnico@dominio.com'
export EMAIL_SUPERVISOR='correo-supervisor@dominio.com'
export EMAIL_LOGISTICA='correo-logistica@dominio.com'
export EMAIL_OPERADOR='correo-operador@dominio.com'
```

Si no defines estas variables, CloudFormation usará los valores de ejemplo `*@example.com`. Cámbialos antes del deploy. Después del despliegue, cada destinatario debe abrir el correo de AWS SNS y confirmar la suscripción.

## Despliegue

Desde la carpeta del repositorio:

```bash
serverless deploy --stage dev
```

Para revisar recursos y endpoints:

```bash
serverless info --stage dev
aws stepfunctions list-state-machines --region us-east-1
aws dynamodb list-tables --region us-east-1
```

## Datos de demostración

Después de desplegar, carga datos mínimos en las tablas:

```bash
python3 seed_data.py
```

El script requiere que la EC2 tenga credenciales AWS activas y permiso para escribir en DynamoDB.

## Prueba rápida sin Flujo 1

Puedes iniciar Step Functions manualmente desde la consola AWS o con CLI, usando `evento-prueba.json`:

```bash
aws stepfunctions start-execution \
  --state-machine-arn arn:aws:states:us-east-1:107681881936:stateMachine:FlujoAtencionIncidente \
  --input file://evento-prueba.json \
  --region us-east-1
```

Para probar la entrada completa SNS → SQS → Lambda, publica el mismo JSON en el topic `TemaIncidentes`:

```bash
aws sns publish \
  --topic-arn "$(aws sns list-topics --region us-east-1 --query 'Topics[?ends_with(TopicArn, `:TemaIncidentes`)].TopicArn | [0]' --output text)" \
  --message file://evento-prueba.json \
  --region us-east-1
```

## Contrato del mensaje recibido desde Flujo 1

```json
{
  "machine_id": "MAQ-001",
  "incidente_id": "INC-PRUEBA-001",
  "severidad": "urgente",
  "zona": "Lima Norte",
  "prob_falla": 0.92,
  "repuesto_id": "REP-001"
}
```

Campos mínimos: `machine_id`, `severidad`, `zona`. Para que el pedido de repuesto se cree cuando no haya stock, la máquina en `t_maquinas` debe tener `repuesto_requerido`, o el evento debe incluir `repuesto_id`.

## Esquema esperado de las tablas

- `t_maquinas`: PK `machine_id`; incluye `zona`, `estado`, `repuesto_requerido`.
- `t_tecnicos`: PK `zona`, SK `tecnico_id`; incluye `nombre`, `email`, `disponibilidad` (`DISPONIBLE` / `OCUPADO`).
- `t_repuestos`: PK `zona`, SK `repuesto_id`; incluye `nombre`, `stock` (número).
- `t_incidentes`: PK `incidente_id`; GSI `MachineHistoryIndex` (`machine_id`, `fecha`).
- `t_pedidos_repuesto`: PK `pedido_id`; GSI `EstadoFechaIndex` (`estado`, `fecha`). Incluye `repuesto_id`, `incidente_id`, `machine_id`, `cantidad`, `estado`, `fecha`, `zona`.

El GSI `EstadoFechaIndex` permite al Flujo 3 consultar pedidos por estado y fecha sin hacer un Scan. El flujo 3 debe sumar pedidos `PENDIENTE` y `EN_PROCESO` a la oferta futura, y no volver a contarlos cuando pasen a `ATENDIDO` y su cantidad se incorpore al stock.

## Permisos y advertencias importantes

Este proyecto reutiliza `LabRole`, pero no puede ampliar sus políticas desde `serverless.yml` porque el entorno Learner Lab no permite crear/administrar roles IAM. `LabRole` debe permitir, como mínimo:

- Lambda: ejecutar funciones y leer/escribir logs.
- DynamoDB: `GetItem`, `PutItem`, `Query`, `Scan`, `UpdateItem` en estas tablas e índices.
- Step Functions: `StartExecution` desde `IniciarAtencion`.
- Lambda Invoke: que Step Functions invoque las funciones del flujo.
- SNS: `Publish` en `TemaNotificaciones`.
- SQS: consumir `ColaIncidentes`.

Además, el rol `LabRole` debe poder ser asumido por `states.amazonaws.com` para actuar como rol de Step Functions. Si el trust policy de LabRole no incluye Step Functions, la creación/ejecución de la máquina de estados fallará y habrá que pedir al docente/administrador un rol autorizado; no se crea otro rol en este proyecto.

## Integración posterior con Flujo 1

Este despliegue crea un topic propio `TemaIncidentes` para pruebas. Al integrar con el Flujo 1, ambos flujos deben usar el mismo contrato JSON. Si Flow 1 está en otra cuenta AWS, se necesita configurar publicación cross-account en SNS y la política de la cola SQS; compartir solo el nombre `TemaIncidentes` no conecta las cuentas.

## Limitaciones de esta primera versión

- La asignación elige el primer técnico disponible por zona; una lógica de carga/turnos puede añadirse después.
- La reserva de repuesto descuenta una unidad al encontrar stock. Si posteriormente falla el registro del incidente, se debe agregar compensación para liberar esa reserva.
- La consulta sin `machine_id` usa Scan para mostrar todos los registros; es suficiente para una demo pequeña, no para grandes volúmenes.
- Las suscripciones de correo de SNS deben confirmarse manualmente.
