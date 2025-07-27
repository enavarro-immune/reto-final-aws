# Este es el archivo principal de la aplicación Flask que maneja la lógica de la aplicación web
# Importa las librerías necesarias para manejar la zona horaria y las fechas
# Configura la aplicación Flask y define las rutas para manejar las solicitudes HTTP
# La aplicación muestra la hora actual en dos zonas horarias y calcula los días restantes hasta una
# fecha objetivo ingresada por el usuario
import os
from flask import Flask, render_template, request
import pytz
from datetime import datetime, date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))

# Configuramos las rutas de la aplicación Flask 
@app.route("/health") # Ruta para verificar la salud de la aplicación
def health():
    return "OK", 200

@app.route("/", methods=["GET", "POST"]) # Ruta principal que maneja tanto GET como POST
def index():
    cr_time = datetime.now(pytz.timezone('America/Costa_Rica'))
    es_time = datetime.now(pytz.timezone('Europe/Madrid'))

    days_remaining = None
    user_date = None
    error = None

    if request.method == "POST":
        user_date_str = request.form.get("target_date")
        try:
            user_date = datetime.strptime(user_date_str, "%Y-%m-%d").date()
            today = date.today()
            days_remaining = (user_date - today).days
        except ValueError:
            error = "Invalid date format. Please use YYYY-MM-DD."

    return render_template(
        "index.html", # Renderiza la plantilla index.html con los datos necesarios
        cr_time=cr_time.strftime("%Y-%m-%d %H:%M:%S"),
        es_time=es_time.strftime("%Y-%m-%d %H:%M:%S"),
        days_remaining=days_remaining,
        user_date=user_date,
        error=error
    )

if __name__ == "__main__": 
    # Inicia la aplicación Flask
    # Configura el host y el puerto para que la aplicación sea accesible desde cualquier IP
    app.run(host="0.0.0.0", port=80)
