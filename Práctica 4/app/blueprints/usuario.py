from flask import Blueprint, request, jsonify
from app.models import Usuario
from app.database import db
import uuid

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")

# Listar todos los usuarios
@usuarios_bp.route("/", methods=["GET"])
def list_users():
    usuarios = Usuario.query.all()
    return jsonify([user.to_dict() for user in usuarios])

# Obtener un usuario por ID
@usuarios_bp.route("/<string:user_id>", methods=["GET"])
def load_user(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario.to_dict())

# Crear un nuevo usuario
@usuarios_bp.route("/", methods=["POST"])
def create_user():
    data = request.json
    if not all(key in data for key in ("username", "email", "password", "role")):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    nuevo_usuario = Usuario(
        id=str(uuid.uuid4()),
        username=data["username"],
        email=data["email"],
        role=data["role"]
    )
    nuevo_usuario.set_password(data["password"])
    
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    return jsonify(nuevo_usuario.to_dict()), 201

# Actualizar usuario
@usuarios_bp.route("/<string:user_id>", methods=["PUT"])
def update_user(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.json
    usuario.username = data.get("username", usuario.username)
    usuario.email = data.get("email", usuario.email)
    usuario.role = data.get("role", usuario.role)
    if "password" in data:
        usuario.set_password(data["password"])
    
    db.session.commit()
    return jsonify(usuario.to_dict())

# Eliminar usuario
@usuarios_bp.route("/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200
