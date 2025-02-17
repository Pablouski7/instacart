import os
import snowflake.connector
from instacart_db import InstacartDb

USER = os.getenv('SNOWFLAKE_USER')
PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
WAREHOUSE = os.getenv('SNOWFLAKE_DEFAULT_WH')
DATABASE = os.getenv('SNOWFLAKE_DEFAULT_DB')
SCHEMA = os.getenv('SNOWFLAKE_DEFAULT_SCHEMA')
ROLE = os.getenv('SNOWFLAKE_ROLE')

# Conectar a Snowflake
conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE,
    database=DATABASE,
    schema=SCHEMA,
    role=ROLE
    )

tables_names = ['AISLES', 'DEPARTMENTS', 'ORDERS', 'ORDER_PRODUCTS', 'PRODUCTS']

def get_tables_mysql():
    """Obtiene las tablas de MySQL."""
    tables = []
    with InstacartDb() as db:
        for table in tables_names:
            sql = f"SELECT * FROM {table} ORDER BY 1"
            result = db.excecute_sql(sql)
            tables.append(result)
    return tables

def get_tables_snowflake():
    """Obtiene las tablas de Snowflake."""
    tables = []
    for table in tables_names:
        sql = f"SELECT * FROM {table} ORDER BY 1"
        cursor = conn.cursor()
        cursor.execute(sql)
        tables.append(tuple(cursor.fetchall()))
    return tables   

def compare_tables():
    """Compara las tablas de MySQL y Snowflake."""
    # Obtener las tablas de MySQL y Snowflake
    tables_mysql = get_tables_mysql()
    tables_snowflake = get_tables_snowflake()
    
    for i, table in enumerate(tables_mysql):
        # Convertir cada fila a tupla para asegurar que sean hashables
        table_mysql = [tuple(row) for row in table]
        table_sf = [tuple(row) for row in tables_snowflake[i]]
        
        # Convertir las listas a conjuntos para hacer la comparación
        set_mysql = set(table_mysql)
        set_sf = set(table_sf)
        
        if set_mysql == set_sf:
            print(f'Table {tables_names[i]} is the same in both databases')
        else:
            print(f'Table {tables_names[i]} is different in both databases')
            print(f'Differences in table {tables_names[i]}:')
            
            # Diferencias: filas presentes en MySQL pero no en Snowflake
            diff_mysql = set_mysql - set_sf
            # Diferencias: filas presentes en Snowflake pero no en MySQL
            diff_sf = set_sf - set_mysql
            
            if diff_mysql:
                print('In MySQL but not in Snowflake:')
                for row in diff_mysql:
                    print(row)
            if diff_sf:
                print('In Snowflake but not in MySQL:')
                for row in diff_sf:
                    print(row)

def main():
    """Función principal."""
    compare_tables()

if __name__ == '__main__':
    main()