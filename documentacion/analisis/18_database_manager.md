# Analisis: `database_manager.py`

## Rol
- Gestiona la base de datos SQLite `huv_oncologia.db` (tabla `informes_ihq`).
- Expone utilidades para inicializar el esquema, insertar registros y obtener un DataFrame.

## Esquema de la tabla
- Columna `id` autoincremental y `fecha_procesado` con timestamp.
- Columnas restantes corresponden al esquema de 55 columnas mas campos IHQ (`IHQ_*`).
- Clave logica: N. peticion (0. Numero de biopsia) (se usa para detectar duplicados).

## Funciones principales
- `init_db()`: crea la base y la tabla si no existen.
- `save_records(records)`: inserta registros, omite duplicados por numero de peticion y mantiene el orden de columnas.
- `get_all_records_as_dataframe()`: devuelve un DataFrame con todo el contenido de la tabla.

## Consideraciones
- No realiza actualizaciones; si un registro cambia se debe implementar UPDATE o eliminar e insertar.
- La tabla se define en el codigo; cualquier cambio exige migracion manual o recreacion.
- La base se crea en el directorio raiz del proyecto; en despliegues empaquetados se debe validar la ruta de escritura.

## Buenas practicas
- Ejecutar `init_db()` antes de leer o guardar registros.
- Realizar respaldos periodicos de `huv_oncologia.db`.
- Registrar en log los registros omitidos por duplicado para trazabilidad.

## Mejoras futuras
- Implementar operaciones de actualizacion/borrado seguro.
- Permitir configuracion de la ruta de la base via `config.ini` o variable de entorno.
- Evaluar normalizar el esquema si se integran Biopsia/Autopsia/Revision.