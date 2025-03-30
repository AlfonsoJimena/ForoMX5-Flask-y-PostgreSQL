from app.database import db
from app.models import Coche, Usuario

def seedCoche():
    # Obtener los usuarios creados previamente
    usuario1 = Usuario.query.filter_by(username="admin").first()  # Usuario admin
    usuario2 = Usuario.query.filter_by(username="user").first()  # Usuario user

    # Crear los coches y asignar los usuario_id correspondientes
    coche1 = Coche(id=1, marca="Mazda", modelo="MX-5 Miata", cv=100, manual=True, anio=1990, precio=3000, descapotable=True, usuario_id=usuario1.id)
    coche2 = Coche(id=2, marca="Porsche", modelo="911 Carrera", cv=280, manual=True, anio=2005, precio=25000, descapotable=False, usuario_id=usuario2.id)
    coche3 = Coche(id=3, marca="Toyota", modelo="Corolla", cv=120, manual=False, anio=2010, precio=10000, descapotable=False, usuario_id=usuario1.id)

    # Agregar los coches a la base de datos
    db.session.add(coche1)
    db.session.add(coche2)
    db.session.add(coche3)
    db.session.commit()

    print("Car data inserted successfully.")




