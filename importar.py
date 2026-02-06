#!/usr/bin/env python3
import os
import pandas as pd
import psycopg2
import sys

# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'dbname': 'postgres',
    'user': 'odoo',
    'password': 'odoo'
}

CSV_FILE = 'listado.csv'
if os.path.exists('listado.csv'):
    CSV_FILE = 'listado.csv'

TABLE_NAME = 'import_centros'


def connect_db(cfg: dict):
    """Conectar a la base de datos usando un diccionario de credenciales."""
    try:
        print(f'Intentando conectar a {cfg.get("host")}:{cfg.get("port")}...')
        conn = psycopg2.connect(**cfg)
        print(f'Conexión OK en puerto {cfg.get("port")}')
        return conn
    except Exception as e:
        print('Error conectando a la base de datos:', repr(e))
        raise


def ensure_table(cursor, table_name: str, columns: list):
    """Crear la tabla si no existe, todas las columnas en tipo TEXT."""
    cols_def = ', '.join([f'"{c}" TEXT' for c in columns])
    sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({cols_def});'
    cursor.execute(sql)


def main():
    try:
        df = pd.read_csv(CSV_FILE, encoding='latin-1')
    except FileNotFoundError:
        print(f'Archivo no encontrado: {CSV_FILE}')
        sys.exit(1)
    except Exception as e:
        print('Error leyendo CSV:', repr(e))
        sys.exit(1)

    if df.empty:
        print('El CSV está vacío. Nada que importar.')
        return

    columns = list(df.columns)

    conn = None
    success = True
    try:
        conn = connect_db(DB_CONFIG)
        cur = conn.cursor()

        # Asegurar la tabla
        ensure_table(cur, TABLE_NAME, columns)

        # Preparar sentencia INSERT con placeholders por posición
        column_list = ', '.join([f'"{c}"' for c in columns])
        placeholders = ', '.join(['%s'] * len(columns))
        insert_sql = f'INSERT INTO {TABLE_NAME} ({column_list}) VALUES ({placeholders})'

        # Insertar fila a fila usando iloc
        for i in range(len(df)):
            row = df.iloc[i].tolist()
            # Convertir NaN a None y todo lo demás a string para TEXT
            params = [None if pd.isna(v) else str(v) for v in row]
            cur.execute(insert_sql, params)

    except Exception as e:
        success = False
        if conn:
            conn.rollback()
        print('Error durante la importación:', type(e), repr(e))
    finally:
        if conn:
            try:
                if success:
                    conn.commit()
                    print('Importación completada correctamente. Se ha hecho commit de los cambios.')
                else:
                    print('No se hizo commit debido a errores. Revise los mensajes anteriores.')
            finally:
                conn.close()


if __name__ == '__main__':
    main()
