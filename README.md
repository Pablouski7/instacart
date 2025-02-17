# Pset #1 Instacart

Este proyecto procesa los datos de un negocio, desde su capa RAW hasta la capa CLEAN, mediante el uso de Mage AI y Snowflake. Además, realiza un análisis sobre la calidad de los datos para limpiarlos adecuadamente y generar insights finales sobre los datos limpios, con el fin de presentar los resultados de todo el proceso y descubrir relaciones y patrones en los datos.

## Requisitos

- Python 3.8+
- MySQL
- Snowflake
- Docker

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/Pablouski7/Instacart_project.git
    cd personal-data-engine
    ```

2. Crea un entorno virtual y actívalo:

    ```bash
    python -m venv venv
    source venv/bin/activate  
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Configura las variables de entorno:

    Copia el archivo `.env.example` a `.env y edítalo con tus credenciales:

    ```bash
    cp .env.example .env
    ```

### Mage AI

Mage AI se utilizó en este proyecto para la orquestación de datos. Puedes iniciar Mage AI con el siguiente comando:
sudo docker run -it --network host -p 6789:6789 -v $(pwd):/home/src --restart=always --env-file ../.env mageai/mageai /app/run_app.sh mage start instacart_project 

Por cuestiones de almacenamiento se decidio subir solo las pipelines en zip por lo que se pueden utilizar estas directamente en cualquier instancia de mage ai.

## Uso

### Cargar datos en MySQL

1. Asegúrate de que tu servidor MySQL esté en funcionamiento y que las credenciales en el archivo `.env` sean correctas.

2. Ejecuta el script principal para cargar los datos en MySQL:

    ```bash
    python scripts/main.py
    ```

### Cargar datos de MySQL a Snowflake RAW

1. Correr la tubería ELT

### Comparar tablas entre MySQL y Snowflake

1. Asegúrate de que las credenciales de Snowflake en el archivo `.env` sean correctas.

2. Ejecuta el script de comprobaciones iniciales que verifica que los datos cargados a Snowflake esten en su estado integro:

    ```bash
    python scripts/comprobaciones_iniciales.py
    ```


### Verificar calidad de los datos

1. Correr notebook `notebooks/eda.ipynb`

### Cargar datos de MySQL a Snowflake CLEAN

1. Correr la tubería ETL

### Realizar análisis a partir del modelado

1. Correr notebook `notebooks/insights.ipynb`

## Estructura del Proyecto

- `docs/`: Documentación adicional del proyecto.
- `scripts/main.py`: Carga los datos de los archivos CSV en la base de datos MySQL.
- `scripts/instacart_db.py`: Clase para manejar la conexión y operaciones con la base de datos MySQL.
- `scripts/comprobaciones_iniciales.py`: Compara las tablas entre MySQL y Snowflake.
- `requirements.txt`: Lista de dependencias del proyecto.
- `.env.example`: Archivo de ejemplo para configurar las variables de entorno.

