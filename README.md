# Importación de Centros Educativos a PostgreSQL (ETL)

Resumen
------
Este repositorio contiene un script `importar.py` que realiza un proceso ETL simple para leer un CSV (por ejemplo `listado.csv`) y volcar sus registros en una tabla PostgreSQL llamada `import_centros`.

Requisitos
----------
- Python 3.10+
- Docker Desktop con contenedores de Odoo/Postgres activos
- Bibliotecas Python: `pandas`, `psycopg2-binary`

Instalación de dependencias
---------------------------
1. Crear y activar un entorno virtual (opcional pero recomendado):

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# o en cmd
.\.venv\Scripts\activate
```

2. Instalar dependencias desde `requirements.txt`:

```bash
pip install -r requirements.txt
```

Preparar infraestructura
------------------------
Asegúrate de que Docker Desktop esté ejecutándose y que el servicio de base de datos PostgreSQL esté accesible. En este repositorio de ejemplo el `docker-compose.yaml` mapea el puerto del host `5433` al puerto del contenedor `5432`. `importar.py` intentará automáticamente conectar en los puertos `5432` y `5433` si el puerto predeterminado no funciona.

Ejecución
---------
1. Coloca `listado.csv` (o `centros_educativos.csv`) en la misma carpeta que `importar.py`.
2. Ejecuta:

```bash
python importar.py
```

Salida esperada
---------------
- Mensaje: `Importación completada correctamente. Se ha hecho commit de los cambios.` si todo va bien.

Verificación en pgAdmin
-----------------------
1. Conéctate al servidor PostgreSQL desde pgAdmin (usa las mismas credenciales definidas en `DB_CONFIG`).
2. Ejecuta:

```sql
SELECT * FROM import_centros;
```

Captura de pantalla (requisito del entregable)
-------------------------------------------
La captura debe mostrar:
- Terminal de VS Code con el mensaje de éxito del script.
- Ventana de pgAdmin mostrando el resultado del `SELECT` con los datos cargados.
- La barra de tareas o el reloj del sistema visible (para verificar la autoría y fecha/hora).

Notas
-----
- El script crea la tabla `import_centros` con todas las columnas en `TEXT` para flexibilidad.
- Inserta cada fila usando `iloc` de `pandas` y realiza `commit()` únicamente si no hubo errores durante la inserción.
- Si el CSV tiene columnas con nombres especiales, el script las delimita con comillas al crear la tabla e insertar.

Control de versiones
--------------------
Sube este repositorio a tu perfil de GitHub/GitLab y realiza commits claros: por ejemplo `add importar.py`, `add sample csv`, `add README`.
