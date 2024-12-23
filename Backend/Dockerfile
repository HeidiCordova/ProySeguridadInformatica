# Usa una imagen base de Python optimizada
FROM python:3.11-slim

# Crear un directorio de trabajo
WORKDIR /app

# Instalar dependencias (caché optimizado)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Gunicorn
RUN pip install gunicorn

# Copiar el resto del código fuente
COPY . .

# Exponer el puerto en el que corre la aplicación
EXPOSE 5000

# Usar Gunicorn para entornos de producción
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
