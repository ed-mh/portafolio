# =========================================================
# 1. LAS HERRAMIENTAS (Imports)
# Aquí traemos todas las librerías que Python necesita para trabajar.
# =========================================================
import os                        # Para leer rutas y archivos del sistema operativo
from datetime import datetime    # Para manejar fechas (útil para saber cuándo publicaste un blog)
from flask import Flask, render_template, request, redirect, url_for# Las herramientas principales de Flask
from flask_sqlalchemy import SQLAlchemy                     # El "traductor" que conecta Flask con tu base de datos
from dotenv import load_dotenv                              # Para ocultar tus contraseñas en un archivo .env

# =========================================================
# 2. CONFIGURACIÓN INICIAL (Preparando el terreno)
# =========================================================
# Esto carga las variables secretas (como contraseñas) de tu archivo .env
load_dotenv()

# Guardamos tus credenciales de Alwaysdata en variables para usarlas más abajo
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
name = os.getenv('DB_NAME')

# Aquí "nace" tu aplicación web. Le decimos a Flask que empiece a funcionar.
app = Flask(__name__)

# Una llave de seguridad obligatoria en Flask para proteger formularios y sesiones
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Le decimos a Flask EXACTAMENTE dónde y cómo conectarse a tu base de datos MySQL en Alwaysdata
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}/{name}'
# Apagamos una función de rastreo que consume mucha memoria y no necesitamos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Conectamos la base de datos (SQLAlchemy) a tu aplicación (app)
db = SQLAlchemy(app)

# =========================================================
# 3. EL ARCHIVERO (Modelos de Base de Datos)
# Aquí definimos la "forma" que tendrán los datos guardados.
# Piensa en cada 'class' como una tabla de Excel.
# =========================================================

# Tabla para guardar los mensajes que te dejen en la sección de contacto
class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)         # Un número único para cada mensaje (1, 2, 3...)
    nombre = db.Column(db.String(100), nullable=False)   # Texto de máximo 100 letras. No puede estar vacío (nullable=False)
    email = db.Column(db.String(120), nullable=False)    # El correo del visitante
    contenido = db.Column(db.Text, nullable=False)       # El mensaje largo
    fecha = db.Column(db.DateTime, default=datetime.utcnow) # Guarda la fecha y hora exacta en automático

# Tabla para guardar los artículos de tu nuevo Blog
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)         # Número único del artículo
    titulo = db.Column(db.String(200), nullable=False)   # El título de tu análisis
    resumen = db.Column(db.String(300), nullable=False)  # Un texto cortito para atrapar al lector
    contenido = db.Column(db.Text, nullable=False)       # Todo el desarrollo de tu artículo
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow) # Fecha automática

# =========================================================
# 4. EL MAPA DEL SITIO (Rutas o Vistas)
# Aquí le decimos a Flask qué mostrar cuando alguien escribe una URL.
# =========================================================

# El decorador @app.route('/') define la página principal (Ej: www.tu-portafolio.com/)
@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST': # Si el usuario está enviando datos...
        # Atrapamos lo que el usuario escribió en las cajas de texto del HTML
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        contenido = request.form.get('mensaje')

        # Empaquetamos esa información usando el "molde" (Modelo) que creamos arriba
        nuevo_mensaje = Mensaje(nombre=nombre, email=email, contenido=contenido)
        
        try:
            # Intentamos guardar el paquete en la base de datos
            db.session.add(nuevo_mensaje)
            db.session.commit() # Confirmamos el guardado
            return redirect('/') # Recargamos la página para limpiar el formulario
        except:
            return 'Hubo un error al guardar el mensaje.'
    # render_template toma un archivo HTML, lo procesa y se lo envía al navegador del usuario
    return render_template('index.html')

# Cuando el usuario entra a www.tu-portafolio.com/proyectos
@app.route('/proyectos')
def proyectos():
    # Esta es una lista temporal de tus proyectos. En el futuro, 
    # esto también podría venir de la base de datos, igual que el blog.
    lista_proyectos = [
        {
            "titulo": "Análisis de la Sismicidad en el Sureste de México",
            "descripcion": "Análisis exploratorio de datos (EDA) y geoespacial de la actividad sísmica de Chiapas y el sureste de México,"
            "una de las zonas tectónicas más complejas de América debido a la interacción de las placas de Cocos, Norteamérica y del Caribe.",
            "url": "/proyectos/analisis-sismos"
        },
        {
            "titulo": "Supply Chain Intelligence | Optimización de Inventarios",
            "descripcion": "Proyecto 'End-to-End' que transforma datos operativos en indicadores estratégicos."
            "Desarrollo del flujo completo de ETL en Python, almacenamiento en MySQL y visualización en Power BI,"
            "incluye análisis estadístico de errores de pronóstico y monitorización de KPIs de salud de stock.",
            "url": "/proyectos/supply-chain"
        }
    ]
    # Le pasamos la 'lista_proyectos' al HTML para que la dibuje en pantalla
    return render_template('proyectos.html', proyectos=lista_proyectos)

@app.route('/proyectos/analisis-sismos')
def sismos_chiapas():
    return render_template('proyecto_sismos.html', title="Análisis de Sismicidad en Chiapas")

@app.route('/proyectos/supply-chain')
def supply_chain_detalle():
    return render_template('supply_chain.html')

# Esta ruta acepta dos métodos: GET (cuando el usuario entra a ver la página) 
# y POST (cuando el usuario da clic en "Enviar" un formulario)
@app.route('/contacto')
def redirect_to_home():
    # El código 301 indica que la redirección es permanente
    return redirect(url_for('inicio'), code=301)


            
    # Si el método es GET (solo entró a mirar), le mostramos el formulario vacío
    return render_template('contacto.html')

# --- RUTAS DEL BLOG ---

# Ruta para ver el menú principal de tu blog
@app.route('/blog')
def blog():
    # Vamos a la base de datos, buscamos TODOS los posts y los ordenamos por fecha (del más nuevo al más viejo)
    entradas = Post.query.order_by(Post.fecha_publicacion.desc()).all()
    # Le pasamos esas entradas al HTML para que cree una lista
    return render_template('blog.html', posts=entradas)

# Esta ruta es dinámica. El <int:post_id> significa que Flask espera un número.
# Ej: /blog/1 mostrará tu primer artículo, /blog/2 el segundo, etc.
@app.route('/blog/<int:post_id>')
def leer_post(post_id):
    # Buscamos en la base de datos el artículo con ese número exacto.
    # Si alguien escribe /blog/999 y no existe, Flask mostrará un error 404 de "Página no encontrada"
    entrada = Post.query.get_or_404(post_id)
    # Le mandamos solo ESE artículo al diseño del HTML
    return render_template('post.html', post=entrada)


# =========================================================
# 5. EL INTERRUPTOR DE ENCENDIDO
# =========================================================
# Esto le dice a Python: "Si estás corriendo este archivo directamente, enciende el servidor web"
if __name__ == '__main__':
    # debug=True ayuda a ver errores detallados mientras programas en tu computadora.
    # ¡Importante!: Al subirlo a Alwaysdata, la plataforma se encarga de arrancar la app de otra manera.
    app.run(debug=True, port=5000)