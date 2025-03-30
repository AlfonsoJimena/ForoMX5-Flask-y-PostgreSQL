from .app import app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    
    db.init_app(app)  # Inicializar db correctamente
    
    with app.app_context():
        from .models import Coche  # Importa los modelos aquí
        db.create_all()
    
    return app