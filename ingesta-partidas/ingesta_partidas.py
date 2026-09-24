import os
import csv
import psycopg2
import boto3
conn = psycopg2.connect(
host=os.environ.get("DB_HOST", "172.31.27.188"),
user=os.environ.get("DB_USER", "partidas_user"),
password=os.environ.get("DB_PASSWORD", "partidas_pass"),
dbname=os.environ.get("DB_NAME", "partidas_db"),
port=5432
)
s3_client = boto3.client("s3")
bucket_name = "ludoteca-storage"
def ingestar_tabla(nombre_tabla, nombre_archivo_csv, s3_key):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {nombre_tabla}")
    columnas = [desc[0] for desc in cursor.description]
    filas = cursor.fetchall()
    print(f"Se encontraron {len(filas)} registros en '{nombre_tabla}'.")
    cursor.close()
    with open(nombre_archivo_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columnas)
        writer.writerows(filas)
    print(f"Archivo CSV '{nombre_archivo_csv}' generado.")
    try:
        s3_client.upload_file(nombre_archivo_csv, bucket_name, s3_key)
        print(f"Subido a s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error al subir '{nombre_archivo_csv}': {e}")
ingestar_tabla("partidas", "partidas.csv", "microservicio2/partidas/partidas.csv")
ingestar_tabla("partida_jugadores", "partida_jugadores.csv", "microservicio2/partida_jugadores/partida_jugadores.csv")
conn.close()
