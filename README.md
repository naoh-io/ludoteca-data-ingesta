cat > README.md << 'EOF'
# Ludoteca - Pipeline de Ingesta de Datos

Contenedores de ingesta del proyecto **Ludoteca / Red de Cafés de Juegos de Mesa** (CS2032 - Cloud Computing, UTEC).

Cada contenedor hace `pull` del 100% de los datos de un microservicio, genera un archivo CSV/JSON, y lo sube a un bucket S3 (`ludoteca-storage`), donde luego AWS Glue lo cataloga para ser consultado con AWS Athena.

## Contenedores

| Carpeta | Microservicio origen | Motor | Tablas/colecciones |
|---|---|---|---|
| `ingesta-catalogo/` | Microservicio 1 | MySQL | juegos, editoriales |
| `ingesta-partidas/` | Microservicio 2 | PostgreSQL | partidas, partida_jugadores |
| `ingesta-membresias/` | Microservicio 3 | MongoDB | clientes (con reservas embebidas) |

## Cómo correr cada uno

Cada carpeta tiene su propio `Dockerfile` y `requirements.txt`. Ejemplo con el de catálogo:

```bash
cd ingesta-catalogo
docker build -t ingesta-catalogo .
docker run --rm \
  -e DB_HOST=<ip-vm-basededatos> \
  -e DB_USER=catalogo_user \
  -e DB_PASSWORD=catalogo_pass \
  -e DB_NAME=catalogo_db \
  -v ~/.aws/credentials:/root/.aws/credentials:ro \
  ingesta-catalogo
```

Ajusta las variables de entorno según el microservicio (ver tabla de arriba). El de membresías no requiere `DB_USER` ni `DB_PASSWORD` (MongoDB sin autenticación en este proyecto).

## Requisitos

- Docker
- Credenciales de AWS con permisos de escritura sobre el bucket S3 destino (montadas vía `~/.aws/credentials` o variables de entorno estándar)
EOF
