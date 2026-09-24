class Apartamento:
    """
    TDA (Tipo de Dato Abstracto) que representa un apartamento temporal 
    en el sistema de alquileres.
    """
    def __init__(self, id_apto, titulo, precio, ubicacion, disponible=True, imagen="default.jpg"):
        self.id = id_apto
        self.titulo = self._validar_titulo(titulo)
        self.precio = self._validar_precio(precio)
        self.ubicacion = self._validar_ubicacion(ubicacion)
        self.disponible = bool(disponible)
        self.imagen = imagen  # Útil para la interfaz web (Integrante 3)

    # --- Validaciones internas (Encapsulamiento del TDA) ---
    def _validar_titulo(self, titulo):
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError("El título del apartamento no puede estar vacío.")
        return titulo.strip()

    def _validar_precio(self, precio):
        try:
            p = float(precio)
            if p <= 0:
                raise ValueError
            return p
        except (ValueError, TypeError):
            raise ValueError("El precio debe ser un número mayor a cero.")

    def _validar_ubicacion(self, ubicacion):
        if not isinstance(ubicacion, str) or not ubicacion.strip():
            raise ValueError("La ubicación no puede estar vacía.")
        return ubicacion.strip()

    def __str__(self):
        estado = "🟢 Disponible" if self.disponible else "🔴 Ocupado"
        return f"[{self.id}] {self.titulo} - ${self.precio:,.2f} ({self.ubicacion}) | {estado}"

    def to_dict(self):
        """
        Convierte la instancia en un diccionario. 
        Fundamental para que Flask pueda serializar a JSON o manejar formularios.
        """
        return {
            "id": self.id,
            "titulo": self.titulo,
            "precio": self.precio,
            "ubicacion": self.ubicacion,
            "disponible": self.disponible,
            "imagen": self.imagen
        }


# --- Datos Base (Mock Data) variados y realistas para la web ---
lista_apartamentos = [
    Apartamento(1, "Loft Moderno en el Centro", 45000.0, "Centro", True, "loft_centro.jpg"),
    Apartamento(2, "Depto con Vista al Mar", 85000.0, "Costa", True, "depto_costa.jpg"),
    Apartamento(3, "Cabaña Alpina en las Sierras", 60000.0, "Sierras", False, "cabana_sierras.jpg"),
    Apartamento(4, "Estudio Ejecutivo", 40000.0, "Centro", True, "estudio_ejecutivo.jpg"),
    Apartamento(5, "Duplex Amplio Familiar", 110000.0, "Norte", True, "duplex_norte.jpg")
]

# --- Funciones de Utilidad y Búsqueda (Para que tus compañeros las usen directo) ---

def obtener_todos_los_apartamentos():
    """Retorna la lista completa de apartamentos."""
    return lista_apartamentos

def buscar_apartamento_por_id(id_buscado):
    """
    Busca y retorna un apartamento según su ID. 
    Retorna None si no lo encuentra.
    """
    for apto in lista_apartamentos:
        if apto.id == int(id_buscado):
            return apto
    return None

def filtrar_por_ubicacion(ubicacion_buscada):
    """
    Retorna una lista con los apartamentos que coincidan con la ubicación buscada 
    (ignorando mayúsculas/minúsculas).
    """
    ubicacion_buscada = ubicacion_buscada.strip().lower()
    return [apto for apto in lista_apartamentos if ubicacion_buscada in apto.ubicacion.lower()]