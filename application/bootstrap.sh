#!/bin/bash
# Este script se utiliza para configurar el entorno de la aplicación Time-App en una instancia EC2
# Incluye la instalación de Docker, AWS CLI, descarga de archivos de la aplicación desde S3,
# y la construcción y ejecución de un contenedor Docker para la aplicación.
sudo yum update -y
sudo yum install -y docker # Instala Docker en la instancia
sudo systemctl start docker # Inicia el servicio Docker
sudo systemctl enable docker # Habilita Docker para que se inicie al arrancar la instancia
sudo usermod -aG docker ec2-user 

# Instala AWS CLI para interactuar con servicios de AWS
sudo yum install -y aws-cli

# Directorio local para la aplicación
LOCAL_DIR="/home/ec2-user/app"
mkdir -p $LOCAL_DIR
cd $LOCAL_DIR

# Descarga los archivos necesarios para la aplicación desde un bucket de S3
aws s3 cp s3://casf47/Dockerfile ./Dockerfile
aws s3 cp s3://casf47/app.py ./app.py
aws s3 cp s3://casf47/requirements.txt ./requirements.txt
aws s3 cp s3://casf47/templates/ ./templates/ --recursive # Descarga recursiva de la carpeta templates

# Construye la imagen Docker de la aplicación
sudo docker build -t time-app-image .
sudo docker run -d -p 80:80 --name time-app time-app-image
