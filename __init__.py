from flask import Flask, render_template

# Creamos la aplicación
app = Flask(__name__)

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

@app.route('/contacto')
def contacto():
    """Ruta para la página de contacto."""
    return render_template('contacto.html')

# --- Iniciar el servidor (para pruebas locales) ---
if __name__ == '__main__':
    # 'debug=True' hace que el servidor se reinicie solo con cada cambio.
    # NUNCA uses debug=True en producción (Alwaysdata).
    app.run(debug=True, port=5000)