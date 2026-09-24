from flask import Flask, render_template, request, redirect, url_for, flash

from modelos import obtener_todos_los_apartamentos
from logica import (
    crear_apartamento,
    obtener_apartamento_por_id,
    actualizar_apartamento,
    eliminar_apartamento,
    filtrar_y_ordenar_apartamentos,
    calcular_tarifa_reserva_recursiva,
    ErrorNegocio,
    DatosInvalidosError,
    ElementoNoEncontradoError
)


app = Flask(__name__)
app.secret_key = "clave-secreta-olimpiadas"


# =========================================================
# PÁGINA PRINCIPAL
# =========================================================

@app.route("/")
def inicio():

    try:
        ubicacion = request.args.get("ubicacion", "").strip()
        precio_min = request.args.get("precio_min", "").strip()
        precio_max = request.args.get("precio_max", "").strip()
        solo_disponibles = request.args.get("solo_disponibles") == "on"
        orden = request.args.get("orden", "precio_asc")

        # Si no hay filtros, mostramos todos
        if not ubicacion and not precio_min and not precio_max and not solo_disponibles:
            apartamentos = [
                apto.to_dict()
                for apto in obtener_todos_los_apartamentos()
            ]
        else:
            apartamentos = filtrar_y_ordenar_apartamentos(
                ubicacion=ubicacion or None,
                precio_min=precio_min or None,
                precio_max=precio_max or None,
                solo_disponibles=solo_disponibles,
                orden=orden
            )

        return render_template(
            "index.html",
            apartamentos=apartamentos,
            filtros={
                "ubicacion": ubicacion,
                "precio_min": precio_min,
                "precio_max": precio_max,
                "solo_disponibles": solo_disponibles,
                "orden": orden
            },
            editar=None
        )

    except ErrorNegocio as e:
        flash(str(e), "error")

        apartamentos = [
            apto.to_dict()
            for apto in obtener_todos_los_apartamentos()
        ]

        return render_template(
            "index.html",
            apartamentos=apartamentos,
            filtros={},
            editar=None
        )


# =========================================================
# CREAR APARTAMENTO
# =========================================================

@app.route("/crear", methods=["POST"])
def crear():

    try:
        titulo = request.form.get("titulo", "").strip()
        precio = request.form.get("precio", "").strip()
        ubicacion = request.form.get("ubicacion", "").strip()
        imagen = request.form.get("imagen", "").strip() or "default.jpg"

        disponible = request.form.get("disponible") == "on"

        crear_apartamento(
            titulo=titulo,
            precio=precio,
            ubicacion=ubicacion,
            disponible=disponible,
            imagen=imagen
        )

        flash("¡Apartamento publicado correctamente!", "success")

    except DatosInvalidosError as e:
        flash(str(e), "error")

    except ErrorNegocio as e:
        flash(str(e), "error")

    return redirect(url_for("inicio"))


# =========================================================
# MOSTRAR FORMULARIO DE EDICIÓN
# =========================================================

@app.route("/editar/<int:id_apto>")
def editar(id_apto):

    try:
        apartamento = obtener_apartamento_por_id(id_apto)

        apartamentos = [
            apto.to_dict()
            for apto in obtener_todos_los_apartamentos()
        ]

        return render_template(
            "index.html",
            apartamentos=apartamentos,
            filtros={},
            editar=apartamento
        )

    except ErrorNegocio as e:
        flash(str(e), "error")
        return redirect(url_for("inicio"))


# =========================================================
# GUARDAR EDICIÓN
# =========================================================

@app.route("/editar/<int:id_apto>", methods=["POST"])
def guardar_edicion(id_apto):

    try:
        titulo = request.form.get("titulo", "").strip()
        precio = request.form.get("precio", "").strip()
        ubicacion = request.form.get("ubicacion", "").strip()
        imagen = request.form.get("imagen", "").strip()
        disponible = request.form.get("disponible") == "on"

        actualizar_apartamento(
            id_apto,
            titulo=titulo,
            precio=precio,
            ubicacion=ubicacion,
            disponible=disponible,
            imagen=imagen
        )

        flash("Apartamento actualizado correctamente.", "success")

    except ErrorNegocio as e:
        flash(str(e), "error")

    return redirect(url_for("inicio"))


# =========================================================
# ELIMINAR
# =========================================================

@app.route("/eliminar/<int:id_apto>", methods=["POST"])
def eliminar(id_apto):

    try:
        resultado = eliminar_apartamento(id_apto)
        flash(resultado["mensaje"], "success")

    except ErrorNegocio as e:
        flash(str(e), "error")

    return redirect(url_for("inicio"))


# =========================================================
# CALCULAR RESERVA
# =========================================================

@app.route("/reserva", methods=["POST"])
def reserva():

    try:
        id_apto = request.form.get("id_apto")
        noches_texto = request.form.get("noches", "").strip()

        apartamento = obtener_apartamento_por_id(id_apto)

        if not apartamento["disponible"]:
            raise DatosInvalidosError(
                "Este apartamento no está disponible actualmente."
            )

        try:
            noches = int(noches_texto)
        except ValueError:
            raise DatosInvalidosError(
                "La cantidad de noches debe ser un número entero."
            )

        total = calcular_tarifa_reserva_recursiva(
            noches,
            apartamento["precio"]
        )

        flash(
            f"Reserva para '{apartamento['titulo']}': "
            f"{noches} noche(s) — Total: ${total:,.2f}",
            "success"
        )

    except ErrorNegocio as e:
        flash(str(e), "error")

    return redirect(url_for("inicio"))


# =========================================================
# ERRORES
# =========================================================

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return redirect(url_for("inicio"))


@app.errorhandler(500)
def error_servidor(error):
    return """
    <h1>Ocurrió un error</h1>
    <p>Volvé a la página principal e intentá nuevamente.</p>
    <a href="/">Volver</a>
    """, 500


# =========================================================
# EJECUCIÓN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)