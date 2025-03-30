from app.database import db


class Coche(db.Model):
    __tablename__ = "coches"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    marca = db.Column(db.String(255), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    cv = db.Column(db.Integer, nullable=False)
    manual = db.Column(db.Boolean, default=True)
    anio = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descapotable = db.Column(db.Boolean, default=False)

    # Clave foránea que hace referencia a 'Usuario.id'
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False) # <- Comentar esta línea en caso de que de error durante la correción del primer apartado

