import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Coche
from app.database import db

coches_bp = Blueprint("coches", __name__)

# Listar coches
@coches_bp.route("/")
def listar_coches():
    query = request.args.get("q", "").lower()
    coches_filtrados = Coche.query.filter(
        (Coche.marca.ilike(f"%{query}%")) | (Coche.modelo.ilike(f"%{query}%"))
    ).all() if query else Coche.query.all()
    return render_template("coches/list.html", coches=coches_filtrados, query=query)

# Mostrar detalle de un coche
@coches_bp.route("/<int:coche_id>")
def mostrar_coche(coche_id):
    coche = Coche.query.get(coche_id)
    return render_template("coches/show.html", coche=coche) if coche else ("Coche no encontrado", 404)

# Formulario para nuevo coche
@coches_bp.route("/new", methods=["GET", "POST"])
def formulario_nuevo():
    if request.method == "POST":
        nuevo_coche = Coche(
            marca=request.form["marca"],
            modelo=request.form["modelo"],
            anio=int(request.form["anio"]),
            precio=float(request.form["precio"]),
            descapotable=request.form.get("descapotable") == "on",
            cv=int(request.form["cv"])  # Aquí añades la opción de caballos
        )
        # Guardar el nuevo coche en la base de datos
        db.session.add(nuevo_coche)
        db.session.commit()

        flash("Coche creado exitosamente.", "success")
        return redirect(url_for("coches.listar_coches"))
    return render_template("coches/new.html")

# Formulario para editar coche
@coches_bp.route("/<int:coche_id>/edit")
def formulario_editar(coche_id):
    coche = Coche.query.get(coche_id)
    if coche:
        return render_template("coches/edit.html", coche=coche)
    else:
        return ("Coche no encontrado", 404)

# Editar coche (edit.html)
@coches_bp.route("/<int:coche_id>", methods=["POST"])
def editar_coche(coche_id):
    coche = Coche.query.get(coche_id)
    if coche:
        coche.marca = request.form["marca"]
        coche.modelo = request.form["modelo"]
        coche.anio = int(request.form["anio"])
        coche.precio = float(request.form["precio"])
        coche.descapotable = request.form.get("descapotable") == "on"
        coche.cv = int(request.form["cv"])  # Añadimos la actualización de caballos

        # Guardar cambios en la base de datos
        db.session.commit()

        flash("Coche editado exitosamente.", "success")
        return redirect(url_for("coches.listar_coches"))

    flash("Coche no encontrado.", "error")
    return ("Coche no encontrado", 404)


# Eliminar coche
@coches_bp.route("/<int:coche_id>/delete", methods=["POST"])
def eliminar_coche(coche_id):
    coche = Coche.query.get(coche_id)
    if coche:
        db.session.delete(coche)
        db.session.commit()
        flash("Coche eliminado exitosamente.", "success")
    else:
        flash("Coche no encontrado.", "error")
    return redirect(url_for("coches.listar_coches"))
