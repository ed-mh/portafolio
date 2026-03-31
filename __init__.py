from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import render_template, request, redirect, flash
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Leer las credenciales
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
name = os.getenv('DB_NAME')


# Creamos la aplicación
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# --- Definición de Rutas ---

@app.route('/')
def inicio():
    """Ruta para la página de inicio."""
    # render_template busca en la carpeta 'templates'
    return render_template('index.html')

@app.route('/proyectos')
def proyectos():
    """Ruta para la página de proyectos."""
    
    # En un caso real, aquí podrías cargar tus proyectos desde una base de datos o un archivo.
    # Por ahora, los definiremos directamente aquí como una lista de diccionarios.
    lista_proyectos = [
        {
            "titulo": "Análisis Sísmico Geoespacial",
            "descripcion": "Procesamiento de 50 años de registros del USGS" +
            " para caracterizar la tectónica de Chiapas."+
            " Uso de PyGMT para visualizar la zona de subducción y corrección estadística"+
            " de sesgos instrumentales.",
            "url": "https://github.com/ed-mh/An-lisis-de-Sismicidad-en-el-Sureste-de-M-xico.git"
        }
        ,
        {
            "titulo": "Supply Chain Intelligence | Optimización de Inventarios",
            "descripcion": "Proyecto 'End-to-End' que transforma datos operativos en indicadores estratégicos. " +
            "Desarrollo del flujo completo de ETL en Python, almacenamiento en MySQL y " +
            "visualización en Power BI, Incluye análisis estadístico de errores de pronóstico " +
            "y monitorización de KPIs de salud de stock.",
            "url": "/proyectos/supply-chain"
            # https://github.com/ed-mh/supply-chain-inventory-optimization.git
        }
        # 
        # ,
        # {
        #     "titulo": "Proyecto 3: App Web con Flask",
        #     "descripcion": "¡Este mismo portafolio puede ser tu tercer proyecto!",
        #     "url_github": "https://github.com/tu-usuario/mi-portafolio"
        # }
    ]
    
    return render_template('proyectos.html', proyectos=lista_proyectos)

@app.route('/proyectos/supply-chain')
def supply_chain_detalle():
    """Ruta para la página detallada del proyecto de Supply Chain."""
    return render_template('supply_chain.html')




# 1. Definir primero la ruta base 
basedir = os.path.abspath(os.path.dirname(__file__))

# # CONFIGURACIÓN CRUCIAL:
# # Aquí le decimos a Flask que use SQLite y dónde crear el archivo .db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mensajes.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Construir la URI de forma segura
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}/{name}'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Ahora sí, inicializamos la base de datos
db = SQLAlchemy(app)


class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)



@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        contenido = request.form.get('mensaje')

        nuevo_mensaje = Mensaje(nombre=nombre, email=email, contenido=contenido)
        
        try:
            db.session.add(nuevo_mensaje)
            db.session.commit()
            # Puedes usar flash si tienes configurada una secret_key
            return redirect('/contacto')
        except:
            return 'Hubo un error al guardar el mensaje.'
            
    return render_template('contacto.html') # Asegúrate que este sea el nombre de tu html
# --- Iniciar el servidor (para pruebas locales) ---
if __name__ == '__main__':
    # 'debug=True' hace que el servidor se reinicie solo con cada cambio.
    # NUNCA uses debug=True en producción (Alwaysdata).
    app.run(debug=False, port=5000)