from modelos import Apartamento, lista_apartamentos, buscar_apartamento_por_id, filtrar_por_ubicacion

print("=== PROBANDO DATOS BASE DE APARTAMENTOS ===")
for apto in lista_apartamentos:
    print(apto)

print("\n=== PROBANDO BÚSQUEDA POR ID ===")
encontrado = buscar_apartamento_por_id(2)
if encontrado:
    print(f"¡Encontrado!: {encontrado.titulo}")
else:
    print("No se encontró el apartamento.")

print("\n=== PROBANDO FILTRADO POR UBICACIÓN ===")
resultados_centro = filtrar_por_ubicacion("centro")
print(f"Apartamentos en el Centro encontrados: {len(resultados_centro)}")
for apto in resultados_centro:
    print(f" - {apto.titulo}")