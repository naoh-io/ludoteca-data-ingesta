FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ingesta_catalogo.py .
CMD ["python", "ingesta_catalogo.py"]
