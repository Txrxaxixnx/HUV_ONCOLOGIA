# database_manager.py
import sqlite3
from pathlib import Path

DB_FILE = "huv_oncologia.db"
TABLE_NAME = "informes_ihq"

def init_db():
    """Crea la base de datos y la tabla si no existen."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Usamos TEXT para todas las columnas por simplicidad, SQLite es flexible.
    # Podríamos ser más estrictos con los tipos (INTEGER, REAL) si fuera necesario.
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        "N. peticion (0. Numero de biopsia)" TEXT,
        "Hospitalizado" TEXT, "Sede" TEXT, "EPS" TEXT, "Servicio" TEXT,
        "Médico tratante" TEXT, "Especialidad" TEXT, "Ubicación" TEXT, "N. Autorizacion" TEXT,
        "Identificador Unico" TEXT, "Datos Clinicos" TEXT, "Fecha ordenamiento" TEXT,
        "Tipo de documento" TEXT, "N. de identificación" TEXT, "Primer nombre" TEXT,
        "Segundo nombre" TEXT, "Primer apellido" TEXT, "Segundo apellido" TEXT,
        "Fecha de nacimiento" TEXT, "Edad" TEXT, "Genero" TEXT, "Número celular" TEXT,
        "Direccion de correo electronico" TEXT, "Direccion de correo electronico 2" TEXT,
        "Contacto de emergencia" TEXT, "Departamento" TEXT, "Teléfono del contacto" TEXT,
        "Municipio" TEXT, "N. muestra" TEXT, "CUPS" TEXT,
        "Tipo de examen (4, 12, Metodo de obtención de la muestra, factor de certeza para el diagnóstico)" TEXT,
        "Procedimiento (11. Tipo de estudio para el diagnóstico)" TEXT,
        "Organo (1. Muestra enviada a patología)" TEXT, "Tarifa" TEXT, "Valor" TEXT,
        "Copago" TEXT, "Descuento" TEXT, "Fecha de ingreso (2. Fecha de la muestra)" TEXT,
        "Fecha finalizacion (3. Fecha del informe)" TEXT, "Usuario finalizacion" TEXT,
        "Usuario asignacion micro" TEXT, "Fecha asignacion micro" TEXT, "Malignidad" TEXT,
        "Condicion" TEXT, "Descripcion macroscopica" TEXT,
        "Descripcion microscopica (8,9, 10,12,. Invasión linfovascular y perineural, indice mitótico/Ki67, Inmunohistoquímica, tamaño tumoral)" TEXT,
        "Descripcion Diagnostico (5,6,7 Tipo histológico, subtipo histológico, margenes tumorales)" TEXT,
        "Diagnostico Principal" TEXT, "Comentario" TEXT, "Informe adicional" TEXT,
        "Congelaciones /Otros estudios" TEXT, "Liquidos (5 Tipo histologico)" TEXT,
        "Citometria de flujo (5 Tipo histologico)" TEXT, "Hora Desc. macro" TEXT, "Responsable macro" TEXT,
        "IHQ_HER2" TEXT, "IHQ_KI-67" TEXT, "IHQ_RECEPTOR_ESTROGENO" TEXT,
        "IHQ_RECEPTOR_PROGESTAGENOS" TEXT, "IHQ_PDL-1" TEXT, "IHQ_ESTUDIOS_SOLICITADOS" TEXT,
        "IHQ_P16_ESTADO" TEXT, "IHQ_P16_PORCENTAJE" TEXT,
        fecha_procesado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_records(records: list[dict]):
    """Guarda una lista de registros (diccionarios) en la base de datos."""
    if not records:
        return
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Obtenemos las columnas de la tabla para asegurar el orden correcto
    cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
    table_columns = [col[1] for col in cursor.fetchall() if col[1] not in ('id', 'fecha_procesado')]
    
    for record in records:
        # Evitamos duplicados basados en el número de petición
        peticion = record.get("N. peticion (0. Numero de biopsia)", "")
        cursor.execute(f"SELECT id FROM {TABLE_NAME} WHERE \"N. peticion (0. Numero de biopsia)\" = ?", (peticion,))
        if cursor.fetchone():
            print(f"Registro {peticion} ya existe. Omitiendo.")
            continue

        # Creamos una tupla de valores en el orden correcto
        values = [record.get(col, '') for col in table_columns]
        placeholders = ', '.join(['?'] * len(table_columns))
        
        # Formateamos los nombres de columna para que sean seguros en SQL
        column_names = ', '.join([f'"{col}"' for col in table_columns])
        
        cursor.execute(f"INSERT INTO {TABLE_NAME} ({column_names}) VALUES ({placeholders})", values)

    conn.commit()
    conn.close()

def get_all_records_as_dataframe():
    """Obtiene todos los registros de la BD y los devuelve como un DataFrame de Pandas."""
    import pandas as pd
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    return df