
from modelos import Apartamento, lista_apartamentos

class ErrorNegocio(Exception):
    """Clase base para errores del dominio de negocio."""
    pass

class ElementoNoEncontradoError(ErrorNegocio):
    """Se lanza cuando un ID de apartamento no existe."""
    pass

class DatosInvalidosError(ErrorNegocio):
    """Se lanza cuando los datos de entrada violan las reglas del sistema."""
    pass

def _generar_siguiente_id():
    """Genera un ID incremental único de forma segura."""
    if not lista_apartamentos:
        return 1
    return max(apto.id for apto in lista_apartamentos) + 1

def crear_apartamento(titulo, precio, ubicacion, disponible=True, imagen="default.jpg"):
    """
    Crea y agrega un nuevo apartamento a la colección.
    Valida entradas estrictamente usando la clase Apartamento.
    """
    try:
        nuevo_id = _generar_siguiente_id()
        # La instanciación de Apartamento ejecuta las validaciones internas
        nuevo_apto = Apartamento(
            id_apto=nuevo_id,
            titulo=titulo,
            precio=precio,
            ubicacion=ubicacion,
            disponible=disponible,
            imagen=imagen
        )
        lista_apartamentos.append(nuevo_apto)
        return nuevo_apto.to_dict()
    except ValueError as e:
        raise DatosInvalidosError(str(e))
    except Exception as e:
        raise DatosInvalidosError(f"Error inesperado al crear apartamento: {str(e)}")


def obtener_apartamento_por_id(id_apto):
    """
    Consulta un apartamento por ID. Retorna el diccionario del objeto.
    """
    try:
        id_num = int(id_apto)
    except (ValueError, TypeError):
        raise DatosInvalidosError("El ID proporcionado debe ser un número entero.")

    for apto in lista_apartamentos:
        if apto.id == id_num:
            return apto.to_dict()
            
    raise ElementoNoEncontradoError(f"No existe ningún apartamento con ID {id_num}.")


def actualizar_apartamento(id_apto, **datos_actualizados):
    """
    Modifica los atributos de un apartamento existente garantizando integridad.
    Soporta actualización parcial mediante argumentos con clave (**kwargs).
    """
    try:
        id_num = int(id_apto)
    except (ValueError, TypeError):
        raise DatosInvalidosError("El ID proporcionado debe ser un entero válido.")

    apto_obj = None
    for apto in lista_apartamentos:
        if apto.id == id_num:
            apto_obj = apto
            break

    if not apto_obj:
        raise ElementoNoEncontradoError(f"No se encontró el apartamento con ID {id_num} para actualizar.")

    try:
        # Actualización condicional y re-validada
        if "titulo" in datos_actualizados and datos_actualizados["titulo"] is not None:
            apto_obj.titulo = apto_obj._validar_titulo(datos_actualizados["titulo"])

        if "precio" in datos_actualizados and datos_actualizados["precio"] is not None:
            apto_obj.precio = apto_obj._validar_precio(datos_actualizados["precio"])

        if "ubicacion" in datos_actualizados and datos_actualizados["ubicacion"] is not None:
            apto_obj.ubicacion = apto_obj._validar_ubicacion(datos_actualizados["ubicacion"])

        if "disponible" in datos_actualizados and datos_actualizados["disponible"] is not None:
            apto_obj.disponible = bool(datos_actualizados["disponible"])

        if "imagen" in datos_actualizados and datos_actualizados["imagen"]:
            apto_obj.imagen = str(datos_actualizados["imagen"]).strip()

        return apto_obj.to_dict()

    except ValueError as e:
        raise DatosInvalidosError(str(e))


def eliminar_apartamento(id_apto):
    """
    Elimina un apartamento de la lista por su ID.
    """
    try:
        id_num = int(id_apto)
    except (ValueError, TypeError):
        raise DatosInvalidosError("El ID proporcionado debe ser un entero válido.")

    for idx, apto in enumerate(lista_apartamentos):
        if apto.id == id_num:
            eliminado = lista_apartamentos.pop(idx)
            return {"mensaje": f"Apartamento '{eliminado.titulo}' (ID: {id_num}) eliminado correctamente."}

    raise ElementoNoEncontradoError(f"No existe ningún apartamento con ID {id_num} para eliminar.")

def filtrar_y_ordenar_apartamentos(ubicacion=None, precio_min=None, precio_max=None, solo_disponibles=False, orden="precio_asc"):
    """
    Filtra y ordena la lista de apartamentos según criterios combinados.
    Evita excepciones parseando tipos de datos numéricos con seguridad.
    """
    resultados = list(lista_apartamentos)

    # 1. Filtrado por Ubicación
    if ubicacion and isinstance(ubicacion, str) and ubicacion.strip():
        term = ubicacion.strip().lower()
        resultados = [a for a in resultados if term in a.ubicacion.lower()]

    # 2. Filtrado por Rango de Precios
    if precio_min is not None:
        try:
            p_min = float(precio_min)
            resultados = [a for a in resultados if a.precio >= p_min]
        except (ValueError, TypeError):
            raise DatosInvalidosError("El precio mínimo debe ser un valor numérico.")

    if precio_max is not None:
        try:
            p_max = float(precio_max)
            resultados = [a for a in resultados if a.precio <= p_max]
        except (ValueError, TypeError):
            raise DatosInvalidosError("El precio máximo debe ser un valor numérico.")

    # 3. Filtrado por Disponibilidad
    if solo_disponibles:
        resultados = [a for a in resultados if a.disponible]

    # 4. Ordenamiento Algorítmico
    if orden == "precio_asc":
        resultados.sort(key=lambda a: a.precio)
    elif orden == "precio_desc":
        resultados.sort(key=lambda a: a.precio, reverse=True)
    elif orden == "titulo_asc":
        resultados.sort(key=lambda a: a.titulo.lower())

    return [apto.to_dict() for apto in resultados]

def calcular_tarifa_reserva_recursiva(noches, precio_por_noche, tasa_descuento_diaria=0.01, descuento_maximo=0.20):
    """
    Calcula el costo total de una reserva de forma RECURSIVA.
    Aplica un descuento acumulativo progresivo según el número de noche:
    - Noche 1: tarifa normal.
    - Noche N: aplica (N - 1) * tasa_descuento_diaria hasta un tope.
    
    Caso Base: noches == 0 -> costo total 0
    Paso Recursivo: Costo Noche N + costo de las (N-1) noches previas.
    """
    # Validaciones iniciales en la llamada raíz
    if not isinstance(noches, int) or noches < 0:
        raise DatosInvalidosError("El número de noches debe ser un número entero no negativo.")
    if not isinstance(precio_por_noche, (int, float)) or precio_por_noche <= 0:
        raise DatosInvalidosError("El precio por noche debe ser mayor a cero.")

    def _calcular_recursivo(n):
        # Caso Base
        if n == 0:
            return 0.0
        
        # Cálculo del descuento acumulado para la noche 'n'
        porcentaje_descuento = min((n - 1) * tasa_descuento_diaria, descuento_maximo)
        precio_noche_actual = precio_por_noche * (1 - porcentaje_descuento)

        # Llamada Recursiva
        return precio_noche_actual + _calcular_recursivo(n - 1)

    subtotal = _calcular_recursivo(noches)
    return round(subtotal, 2)
