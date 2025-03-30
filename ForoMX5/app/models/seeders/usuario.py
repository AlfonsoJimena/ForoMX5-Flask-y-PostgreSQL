from app.database import db
from app.models import Usuario

def seedUsuario():

    usuario1 = Usuario(username="admin", email="admin@example.com", role="admin")
    usuario1.set_password("admin123")  # Hashear contraseña

    usuario2 = Usuario(username="user", email="user@example.com", role="user")
    usuario2.set_password("user123")  # Hashear contraseña

    # Agregar a la base de datos
    db.session.add(usuario1)
    db.session.add(usuario2)
    db.session.commit()

    print("User data inserted successfully.")



