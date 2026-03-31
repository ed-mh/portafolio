# Importamos la app y la base de datos desde tu archivo principal 
# (Asumiendo que tu archivo principal se llama app.py, si se llama main.py, cambia "from app" a "from main")
from app import app, db, Post

# Creamos el contenido del post
titulo = "Mi primer análisis publicado"
resumen = "En este artículo explico por qué decidí integrar un blog a mi portafolio usando Flask."

# Aquí puedes usar HTML básico dentro del texto para darle formato (párrafos, negritas)
contenido_completo = """
    <p>¡Hola! Este es mi primer artículo.</p>
    <p>Como analista de datos, me di cuenta de que <strong>comunicar los resultados</strong> es tan importante como procesarlos.</p>
    <p>Pronto estaré subiendo tutoriales y descubrimientos sobre mis proyectos de Supply Chain y sismos.</p>
"""

# Usamos el "contexto de la aplicación" para que Flask nos deje hablar con la base de datos
with app.app_context():
    # 1. Empaquetamos los datos usando el modelo Post
    nueva_entrada = Post(
        titulo=titulo, 
        resumen=resumen, 
        contenido=contenido_completo
    )
    
    # 2. Lo agregamos a la sesión
    db.session.add(nueva_entrada)
    
    # 3. Guardamos los cambios en la base de datos
    db.session.commit()
    
    print("¡Post creado exitosamente en la base de datos!")
    