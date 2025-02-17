import pymysql
import os

class InstacartDb:
    """Clase para manejar la base de datos de Instacart."""
    _instancia = None
    def __new__(clase):
        """Implementa el patrón Singleton."""
        if clase._instancia is None:
            clase._instancia = super(InstacartDb, clase).__new__(clase)
            clase._instancia.conectar()
        return clase._instancia
        
    def conectar(self):
        """Conecta a la base de datos."""
        self.conn = pymysql.connect(
            host = os.environ['MYSQL_HOST'],
            port = int(os.environ['MYSQL_PORT']),
            user = os.environ['MYSQL_USER'],
            password = os.environ['MYSQL_PSWD'])
        db = 'instacart_db'
        cursor = self.cursor()
        cursor.execute(f"""CREATE DATABASE IF NOT EXISTS {db} DEFAULT CHARACTER SET UTF8MB4""")
        self.conn.select_db(db)

    def cursor(self):
        """Obtiene un cursor de la conexión."""
        return self.conn.cursor()

    def close(self):
        """Cierra la conexión a la base de datos."""
        self.conn.commit()
        self.conn.close()

    def __enter__(self):
        """Inicia el contexto de la conexión."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Finaliza el contexto de la conexión."""
        self.close()

    def excecute_sql(self, sql):
        """Ejecuta una consulta SQL."""
        cursor = self.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
        
    def create_table(self, nombre, columnas, adicional=''):
        """Crea una tabla en la base de datos."""
        nombre = nombre.upper()
        columnas = {columna.upper(): tipo.upper() for columna, tipo in columnas.items()}
        columnas_definicion = ", ".join([f"{columna} {tipo}" for columna, tipo in columnas.items()])
        if adicional:
            adicional = [adic.upper() for adic in adicional]
            columnas_definicion += ", " + ", ".join(adicional)
        cursor = self.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {nombre} ({columnas_definicion})""")
        return cursor.fetchall()
    
    def insert(self, tabla, datos):
        """Inserta datos en una tabla."""
        cursor = self.cursor()
        columnas = ', '.join(datos.keys())
        valores = ', '.join([f"'{valor}'" for valor in datos.values()])
        cursor.execute(f"""INSERT INTO {tabla} ({columnas}) VALUES ({valores})""")
        return cursor.fetchall()
    
    def create_aisles_table(self):
        """Crea la tabla 'aisles'."""
        columnas = {
            'aisle_id': 'INT PRIMARY KEY',
            'aisle': 'VARCHAR(255)'
        }
        return self.create_table('aisles', columnas)
    
    def create_departments_table(self):
        """Crea la tabla 'departments'."""
        columnas = {
            'department_id': 'INT PRIMARY KEY',
            'department': 'VARCHAR(255)'
        }
        return self.create_table('departments', columnas)
    
    def create_products_table(self):
        """Crea la tabla 'products'."""
        columnas = {
            'product_id': 'INT PRIMARY KEY',
            'product_name': 'VARCHAR(255)',
            'aisle_id': 'INT',
            'department_id': 'INT'
        }
        foreign_keys = [
            'FOREIGN KEY (aisle_id) REFERENCES aisles(aisle_id)',
            'FOREIGN KEY (department_id) REFERENCES departments(department_id)'
        ]
        return self.create_table('products', columnas, foreign_keys)
    
    def create_orders_table(self):
        """Crea la tabla 'orders'."""
        columnas = {
            'id_order': 'INT PRIMARY KEY AUTO_INCREMENT',
            'order_id': 'INT',
            'user_id': 'INT',
            'order_number': 'INT',
            'order_dow': 'INT',
            'order_hour_of_day': 'INT',
            'days_since_prior_order': 'FLOAT'
        }
        return self.create_table('orders', columnas)
    
    def create_order_products_table(self):
        """Crea la tabla 'order_products'."""
        columnas = {
            'order_id': 'INT',
            'product_id': 'INT',
            'add_to_cart_order': 'FLOAT',
            'reordered': 'BOOLEAN'
        }
        foreign_keys = [
            'FOREIGN KEY (product_id) REFERENCES products(product_id)'
        ]
        return self.create_table('order_products', columnas, foreign_keys)