import os
import json
import pymongo
import boto3

mongo_host = os.environ.get("DB_HOST", "172.31.27.188")
mongo_port = int(os.environ.get("DB_PORT", 27017))
db_name = os.environ.get("DB_NAME", "ludoteca_membresias")

mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/{db_name}"

client = pymongo.MongoClient(mongo_uri)
db = client[db_name]
collection = db["clientes"]

documentos = list(collection.find())
print(f"[clientes] Se encontraron {len(documentos)} documentos.")

client.close()

# Formato NDJSON: un documento JSON por línea, sin indentación,
# sin corchetes envolviendo todo - esto es lo que Athena/Glue necesitan
# para leer "una fila = un documento".
json_filename = "clientes.json"
with open(json_filename, "w", encoding="utf-8") as file:
    for doc in documentos:
        file.write(json.dumps(doc, ensure_ascii=False, default=str) + "\n")

print(f"[clientes] Archivo local '{json_filename}' generado con éxito.")

s3_client = boto3.client("s3")
bucket_name = "ludoteca-storage"
s3_key = "microservicio3/clientes/clientes.json"

try:
    s3_client.upload_file(json_filename, bucket_name, s3_key)
    print(f"[clientes] Subido con éxito a s3://{bucket_name}/{s3_key}")
except Exception as e:
    print(f"[clientes] Error al subir a S3: {e}")
