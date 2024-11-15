FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los requisitos e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY . .

# Crea el directorio para la base de datos y asigna permisos
RUN mkdir -p /data && chmod 755 /data

# Expone el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]