import os
import csv
import mysql.connector
import boto3

def ingestar_tabla(conn, nombre_tabla, s3_key, bucket_name="ludoteca-storage"):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {nombre_tabla}")
    
    columnas = [column[0] for column in cursor.description]
    filas = cursor.fetchall()
    
    print(f"[{nombre_tabla}] Se encontraron {len(filas)} registros.")
    
    csv_filename = f"{nombre_tabla}.csv"
    
    # Escribir archivo CSV local
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columnas)
        writer.writerows(filas)
        
    print(f"[{nombre_tabla}] Archivo local '{csv_filename}' generado.")
    
    # Subir a S3
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(csv_filename, bucket_name, s3_key)
        print(f"[{nombre_tabla}] Subido con éxito a s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"[{nombre_tabla}] Error al subir a S3: {e}")
        
    cursor.close()

# Conexión principal a MySQL (Microservicio 1)
conn = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "172.31.27.188"),
    user=os.environ.get("DB_USER", "catalogo_user"),
    password=os.environ.get("DB_PASSWORD", "catalogo_pass"),
    database=os.environ.get("DB_NAME", "catalogo_db"),
    port=3306
)

# Ingesta de ambas tablas del Microservicio 1
ingestar_tabla(conn, "juegos", "microservicio1/juegos.csv")
ingestar_tabla(conn, "editoriales", "microservicio1/editoriales.csv")

conn.close()
