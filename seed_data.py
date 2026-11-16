
import os
import boto3
from decimal import Decimal

# ==========================================
# CONFIGURACION
# ==========================================

REGION = os.getenv("AWS_REGION", "us-east-1")

MACHINES_TABLE = os.getenv("MACHINES_TABLE", "t_maquinas")
TECHNICIANS_TABLE = os.getenv("TECHNICIANS_TABLE", "t_tecnicos")
PARTS_TABLE = os.getenv("PARTS_TABLE", "t_repuestos")

dynamodb = boto3.resource("dynamodb", region_name=REGION)

machines_table = dynamodb.Table(MACHINES_TABLE)
technicians_table = dynamodb.Table(TECHNICIANS_TABLE)
parts_table = dynamodb.Table(PARTS_TABLE)


# ==========================================
# MAQUINAS: 30 REGISTROS DE FLUJO 1
# ==========================================

machines = [
    {
        "machine_id": "MAQ-012", "carga": 9.35, "combustible": 10.97,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.1352, "lon": -76.9943,
        "operador_email": "operador@example.com",
        "presion": 168.63, "repuesto_requerido": "REP-002",
        "rpm": 1670.65, "temperatura": 63.62,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 24.55, "vibracion": 4.99, "zona": "Lima Sur"
    },
    {
        "machine_id": "MAQ-018", "carga": 8.91, "combustible": 17.37,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.1753, "lon": -76.9761,
        "operador_email": "operador@example.com",
        "presion": 141.84, "repuesto_requerido": "REP-002",
        "rpm": 1116.11, "temperatura": 80.07,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 15.79, "vibracion": 3.03, "zona": "Lima Sur"
    },
    {
        "machine_id": "MAQ-020", "carga": 5.67, "combustible": 5.94,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.0361, "lon": -77.0504,
        "operador_email": "operador@example.com",
        "presion": 149.44, "repuesto_requerido": "REP-002",
        "rpm": 1678.35, "temperatura": 84.95,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 12.76, "vibracion": 1.26, "zona": "Lima Centro"
    },
    {
        "machine_id": "MAQ-011", "carga": 4.78, "combustible": 16.22,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.0575, "lon": -77.0335,
        "operador_email": "operador@example.com",
        "presion": 156.36, "repuesto_requerido": "REP-001",
        "rpm": 1501.13, "temperatura": 80.84,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 7.02, "vibracion": 2.78, "zona": "Lima Centro"
    },
    {
        "machine_id": "MAQ-013", "carga": 12.76, "combustible": 13.52,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -11.9734, "lon": -77.0624,
        "operador_email": "operador@example.com",
        "presion": 153.82, "repuesto_requerido": "REP-001",
        "rpm": 1677.06, "temperatura": 66.99,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 15.13, "vibracion": 5.24, "zona": "Lima Norte"
    },
    {
        "machine_id": "MAQ-021", "carga": 8.38, "combustible": 14.4,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.1668, "lon": -77.0157,
        "operador_email": "operador@example.com",
        "presion": 163.51, "repuesto_requerido": "REP-001",
        "rpm": 1899.47, "temperatura": 76.72,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 12.08, "vibracion": 1.82, "zona": "Lima Sur"
    },
    {
        "machine_id": "MAQ-017", "carga": 7.73, "combustible": 8.63,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.0764, "lon": -77.0534,
        "operador_email": "operador@example.com",
        "presion": 137.39, "repuesto_requerido": "REP-001",
        "rpm": 1542.78, "temperatura": 73.56,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 14.76, "vibracion": 4.09, "zona": "Lima Centro"
    },
    {
        "machine_id": "MAQ-006", "carga": 9.19, "combustible": 12.32,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.1641, "lon": -77.0174,
        "operador_email": "operador@example.com",
        "presion": 159.58, "repuesto_requerido": "REP-002",
        "rpm": 1516.8, "temperatura": 64.64,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 15.71, "vibracion": 3.67, "zona": "Lima Sur"
    },
    {
        "machine_id": "MAQ-009", "carga": 8.43, "combustible": 14.56,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.1435, "lon": -77.0097,
        "operador_email": "operador@example.com",
        "presion": 136.49, "repuesto_requerido": "REP-001",
        "rpm": 1920.07, "temperatura": 77.16,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 14.59, "vibracion": 5.04, "zona": "Lima Sur"
    },
    {
        "machine_id": "MAQ-007", "carga": 6.86, "combustible": 16.49,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -11.9283, "lon": -77.0654,
        "operador_email": "operador@example.com",
        "presion": 157.76, "repuesto_requerido": "REP-001",
        "rpm": 1560.04, "temperatura": 69.41,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 19.46, "vibracion": 2.26, "zona": "Lima Norte"
    },
    {
        "machine_id": "MAQ-010", "carga": 4.88, "combustible": 14.07,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -11.9339, "lon": -77.0966,
        "operador_email": "operador@example.com",
        "presion": 169.65, "repuesto_requerido": "REP-002",
        "rpm": 1509.64, "temperatura": 70.69,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 14.15, "vibracion": 3.3, "zona": "Lima Norte"
    },
    {
        "machine_id": "MAQ-024", "carga": 10.14, "combustible": 9.93,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.1283, "lon": -77.0051,
        "operador_email": "operador@example.com",
        "presion": 156.49, "repuesto_requerido": "REP-002",
        "rpm": 1455.99, "temperatura": 59.78,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 7.97, "vibracion": 5.21, "zona": "Lima Sur"
    },
    {
        "machine_id": "MAQ-004", "carga": 9.75, "combustible": 14.43,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -11.9463, "lon": -77.057,
        "operador_email": "operador@example.com",
        "presion": 157.33, "repuesto_requerido": "REP-002",
        "rpm": 1602.12, "temperatura": 68.58,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 5.23, "vibracion": 3.26, "zona": "Lima Norte"
    },
    {
        "machine_id": "MAQ-019", "carga": 5.84, "combustible": 16.78,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -11.9641, "lon": -77.0477,
        "operador_email": "operador@example.com",
        "presion": 129.26, "repuesto_requerido": "REP-001",
        "rpm": 1673.74, "temperatura": 76.24,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 18.53, "vibracion": 1.36, "zona": "Lima Norte"
    },
    {
        "machine_id": "MAQ-029", "carga": 5.89, "combustible": 11.52,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.073, "lon": -77.0423,
        "operador_email": "operador@example.com",
        "presion": 164.51, "repuesto_requerido": "REP-001",
        "rpm": 1333.83, "temperatura": 82.82,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 13.36, "vibracion": 1.7, "zona": "Lima Centro"
    },
    {
        "machine_id": "MAQ-025", "carga": 8.14, "combustible": 11.68,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -11.9315, "lon": -77.0486,
        "operador_email": "operador@example.com",
        "presion": 131.31, "repuesto_requerido": "REP-001",
        "rpm": 1240.52, "temperatura": 67.34,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 14.98, "vibracion": 4.37, "zona": "Lima Norte"
    },
    {
        "machine_id": "MAQ-015", "carga": 7.76, "combustible": 14.81,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.1539, "lon": -76.9928,
        "operador_email": "operador@example.com",
        "presion": 147.45, "repuesto_requerido": "REP-001",
        "rpm": 1370.59, "temperatura": 82.44,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 17.61, "vibracion": 1.97, "zona": "Lima Sur"
    },
    {
        "machine_id": "MAQ-022", "carga": 4.37, "combustible": 11.89,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -11.9671, "lon": -77.0921,
        "operador_email": "operador@example.com",
        "presion": 153.3, "repuesto_requerido": "REP-002",
        "rpm": 1713.3, "temperatura": 70.59,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 19.9, "vibracion": 3.47, "zona": "Lima Norte"
    },
    {
        "machine_id": "MAQ-027", "carga": 12.27, "combustible": 15.12,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.1329, "lon": -77.0029,
        "operador_email": "operador@example.com",
        "presion": 145.81, "repuesto_requerido": "REP-001",
        "rpm": 1337.99, "temperatura": 88.84,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 16.21, "vibracion": 6.99, "zona": "Lima Sur"
    },
    {
        "machine_id": "MAQ-008", "carga": 4.94, "combustible": 11.07,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.0536, "lon": -77.0456,
        "operador_email": "operador@example.com",
        "presion": 170.91, "repuesto_requerido": "REP-002",
        "rpm": 1900.01, "temperatura": 83.48,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 14.88, "vibracion": 2.53, "zona": "Lima Centro"
    },
    {
        "machine_id": "MAQ-002", "carga": 12.89, "combustible": 16.05,
        "estado": "operativa", "horas_uso": 1002.6536,
        "lat": -12.0599, "lon": -77.0594,
        "operador_email": "operador@example.com",
        "presion": 148.58, "repuesto_requerido": "REP-002",
        "rpm": 1774.85, "temperatura": 94.06,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 15.12, "vibracion": 3.69, "zona": "Lima Centro"
    },
    {
        "machine_id": "MAQ-005", "carga": 9.51, "combustible": 14.97,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.0345, "lon": -77.0524,
        "operador_email": "operador@example.com",
        "presion": 153.51, "repuesto_requerido": "REP-001",
        "rpm": 1780.32, "temperatura": 63.0,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 6.06, "vibracion": 3.69, "zona": "Lima Centro"
    },
    {
        "machine_id": "MAQ-001", "carga": 1.95, "combustible": 12.15,
        "estado": "operativa", "horas_uso": 1002.7538,
        "lat": -11.9416, "lon": -77.0985,
        "operador_email": "operador@example.com",
        "presion": 152.75, "repuesto_requerido": "REP-001",
        "rpm": 1709.41, "temperatura": 164.52,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 19.67, "vibracion": 19.55, "zona": "Lima Norte"
    },
    {
        "machine_id": "MAQ-028", "carga": 11.02, "combustible": 13.89,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -11.9219, "lon": -77.0652,
        "operador_email": "operador@example.com",
        "presion": 138.31, "repuesto_requerido": "REP-002",
        "rpm": 1589.16, "temperatura": 79.37,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 14.82, "vibracion": 2.2, "zona": "Lima Norte"
    },
    {
        "machine_id": "MAQ-026", "carga": 1.77, "combustible": 16.66,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.0664, "lon": -77.0437,
        "operador_email": "operador@example.com",
        "presion": 156.8, "repuesto_requerido": "REP-002",
        "rpm": 1443.29, "temperatura": 62.56,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 11.57, "vibracion": 2.02, "zona": "Lima Centro"
    },
    {
        "machine_id": "MAQ-014", "carga": 7.88, "combustible": 12.93,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.0432, "lon": -77.0163,
        "operador_email": "operador@example.com",
        "presion": 152.15, "repuesto_requerido": "REP-002",
        "rpm": 1853.0, "temperatura": 61.98,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 13.71, "vibracion": 2.53, "zona": "Lima Centro"
    },
    {
        "machine_id": "MAQ-030", "carga": 9.52, "combustible": 11.38,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.1453, "lon": -77.0176,
        "operador_email": "operador@example.com",
        "presion": 154.27, "repuesto_requerido": "REP-002",
        "rpm": 1864.93, "temperatura": 72.53,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 10.29, "vibracion": 0.81, "zona": "Lima Sur"
    },
    {
        "machine_id": "MAQ-023", "carga": 7.42, "combustible": 12.82,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -12.0505, "lon": -77.0474,
        "operador_email": "operador@example.com",
        "presion": 149.77, "repuesto_requerido": "REP-001",
        "rpm": 1851.64, "temperatura": 82.34,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 12.78, "vibracion": 3.4, "zona": "Lima Centro"
    },
    {
        "machine_id": "MAQ-016", "carga": 9.4, "combustible": 8.62,
        "estado": "operativa", "horas_uso": 1000.8667,
        "lat": -11.9425, "lon": -77.0495,
        "operador_email": "operador@example.com",
        "presion": 140.62, "repuesto_requerido": "REP-002",
        "rpm": 1555.66, "temperatura": 75.85,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 14.1, "vibracion": 4.58, "zona": "Lima Norte"
    },
    {
        "machine_id": "MAQ-003", "carga": 3.42, "combustible": 16.47,
        "estado": "operativa", "horas_uso": 1002.6536,
        "lat": -12.1358, "lon": -76.9794,
        "operador_email": "operador@example.com",
        "presion": 114.23, "repuesto_requerido": "REP-001",
        "rpm": 1159.74, "temperatura": 100.25,
        "timestamp": "2026-11-16T02:55:41+00:00",
        "velocidad": 10.66, "vibracion": 9.3, "zona": "Lima Sur"
    }
]


# ==========================================
# TECNICOS: 6 REGISTROS, 2 POR ZONA
# ==========================================

technicians = [
    {
        "zona": "Lima Norte",
        "tecnico_id": "TEC-001",
        "nombre": "Tecnico Norte 1",
        "email": "tecnico.norte1@example.com",
        "disponibilidad": "DISPONIBLE"
    },
    {
        "zona": "Lima Norte",
        "tecnico_id": "TEC-002",
        "nombre": "Tecnico Norte 2",
        "email": "tecnico.norte2@example.com",
        "disponibilidad": "DISPONIBLE"
    },
    {
        "zona": "Lima Centro",
        "tecnico_id": "TEC-003",
        "nombre": "Tecnico Centro 1",
        "email": "tecnico.centro1@example.com",
        "disponibilidad": "DISPONIBLE"
    },
    {
        "zona": "Lima Centro",
        "tecnico_id": "TEC-004",
        "nombre": "Tecnico Centro 2",
        "email": "tecnico.centro2@example.com",
        "disponibilidad": "DISPONIBLE"
    },
    {
        "zona": "Lima Sur",
        "tecnico_id": "TEC-005",
        "nombre": "Tecnico Sur 1",
        "email": "tecnico.sur1@example.com",
        "disponibilidad": "DISPONIBLE"
    },
    {
        "zona": "Lima Sur",
        "tecnico_id": "TEC-006",
        "nombre": "Tecnico Sur 2",
        "email": "tecnico.sur2@example.com",
        "disponibilidad": "DISPONIBLE"
    }
]


# ==========================================
# REPUESTOS: 6 REGISTROS, 2 POR ZONA
# ==========================================

spare_parts = [
    {
        "zona": "Lima Norte",
        "repuesto_id": "REP-001",
        "nombre": "Filtro industrial",
        "stock": 2
    },
    {
        "zona": "Lima Norte",
        "repuesto_id": "REP-002",
        "nombre": "Bomba hidraulica",
        "stock": 0
    },
    {
        "zona": "Lima Centro",
        "repuesto_id": "REP-001",
        "nombre": "Filtro industrial",
        "stock": 0
    },
    {
        "zona": "Lima Centro",
        "repuesto_id": "REP-002",
        "nombre": "Bomba hidraulica",
        "stock": 3
    },
    {
        "zona": "Lima Sur",
        "repuesto_id": "REP-001",
        "nombre": "Filtro industrial",
        "stock": 2
    },
    {
        "zona": "Lima Sur",
        "repuesto_id": "REP-002",
        "nombre": "Bomba hidraulica",
        "stock": 0
    }
]


# ==========================================
# FUNCIONES PARA CARGAR DYNAMODB
# ==========================================

def convertir_a_decimal(valor):
    """
    DynamoDB no acepta float directamente mediante boto3.
    Convertimos los valores decimales a Decimal.
    """
    if isinstance(valor, float):
        return Decimal(str(valor))

    if isinstance(valor, dict):
        return {
            clave: convertir_a_decimal(valor_interno)
            for clave, valor_interno in valor.items()
        }

    if isinstance(valor, list):
        return [convertir_a_decimal(elemento) for elemento in valor]

    return valor


def cargar_datos(tabla, registros):
    """
    Inserta o reemplaza los registros usando las claves
    primarias definidas en cada tabla.
    """
    with tabla.batch_writer() as batch:
        for registro in registros:
            batch.put_item(
                Item=convertir_a_decimal(registro)
            )

    print(
        f"{tabla.name}: "
        f"{len(registros)} registros insertados/actualizados."
    )


# ==========================================
# EJECUCION DEL SEED
# ==========================================

if __name__ == "__main__":

    print("Iniciando carga de datos de Flujo 2...\n")

    cargar_datos(machines_table, machines)
    cargar_datos(technicians_table, technicians)
    cargar_datos(parts_table, spare_parts)

    print("\nCarga de datos finalizada.")
