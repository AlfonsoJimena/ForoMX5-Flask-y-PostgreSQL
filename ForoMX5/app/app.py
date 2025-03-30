from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.engine.url import make_url
import secrets
from app.database import db
import click
from flask.cli import with_appcontext
import app.models


# Inicializamos Flask
app = Flask(__name__, static_folder='public', static_url_path="", template_folder='templates')

# Configuración de la base de datos 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password_database@localhost:0000/foromx5?client_encoding=UTF8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.config['SECRET_KEY'] = secrets.token_hex(24)

# Inicializamos SQLAlchemy y Migraciones
migrate = Migrate(app, db)  # Iniciar migrate con la app y db

# Verificar y crear la base de datos si no existe
db_url = make_url(app.config['SQLALCHEMY_DATABASE_URI'])
if not database_exists(db_url):
    create_database(db_url)

# Middleware antes de procesar cada request
@app.before_request
def registrar_peticiones():
    print(f"Petición: {request.method} {request.path}")

# Middleware después de procesar cada request
@app.after_request
def modificar_respuesta(response):
    response.headers["X-Developer"] = "TuNombre"
    return response

# Importar y registrar blueprint
from app.blueprints.coche import coches_bp
app.register_blueprint(coches_bp, url_prefix="/coches")

# Importar manejadores de errores
from app.errors.handlers import init_error_handlers
init_error_handlers(app)

# Rutas principales
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)

# Custom command for seeding the users database
@click.command(name='seed')
@with_appcontext
def seed():
    from app.models.seeders.usuario import seedUsuario # <- Comentar esta línea para evitar cargar usuarios
    from app.models.seeders import seedCoche
    seedUsuario()                                      # <- Comentar esta línea para evitar cargar usuarios
    seedCoche()

# Añadir el comando a la aplicación
app.cli.add_command(seed)



