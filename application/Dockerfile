# Este Dockerfile está diseñado para crear una imagen de la aplicación Flask definida en app.py
# Usamos una imagen base de Python 3.11 slim para mantener la imagen ligera
# Esta imagen es adecuada para aplicaciones Flask y permite una fácil instalación de dependencias
# Asegúrate de que todos los archivos y folders mencionados abajo estén
# presente en el mismo directorio que este Dockerfile

# Definimos la version de Python que queremos usar
# En este caso, usamos Python 3.11 slim para una imagen más ligera
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
# Aquí es donde se ejecutarán los comandos y se almacenarán los archivos de la aplicación
WORKDIR /app

# Copiamos y ejecutamos el archivo de requisitos al contenedor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de los archivos de la aplicación al contenedor
# Esto incluye app.py y la carpeta templates que contiene las plantillas HTML
COPY app.py .
COPY templates/ ./templates/

# Exponemos el puerto 80 para que la aplicación Flask pueda recibir tráfico HTTP
# Este es el puerto por defecto que Flask utiliza para servir la aplicación
EXPOSE 80

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
