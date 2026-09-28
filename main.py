import heapq


# ==========================================================
# BASE DE CONOCIMIENTO
# ==========================================================

# Conexiones entre estaciones
conexiones = {
    "Niquía": ["Bello"],
    "Bello": ["Niquía", "Madera"],
    "Madera": ["Bello", "Acevedo"],
    "Acevedo": ["Madera", "Caribe"],
    "Caribe": ["Acevedo", "Universidad"],
    "Universidad": ["Caribe", "Hospital"],
    "Hospital": ["Universidad", "Prado"],
    "Prado": ["Hospital", "Parque Berrío"],
    "Parque Berrío": ["Prado", "San Antonio"],
    "San Antonio": [
        "Parque Berrío",
        "Alpujarra",
        "Cisneros"
    ],
    "Alpujarra": ["San Antonio", "Exposiciones"],
    "Exposiciones": ["Alpujarra", "Industriales"],
    "Industriales": ["Exposiciones", "Poblado"],
    "Poblado": ["Industriales", "Aguacatala"],
    "Aguacatala": ["Poblado", "Ayurá"],
    "Ayurá": ["Aguacatala", "Envigado"],
    "Envigado": ["Ayurá", "Itagüí"],
    "Itagüí": ["Envigado"],

    # Línea B
    "Cisneros": ["San Antonio", "Suramericana"],
    "Suramericana": ["Cisneros", "Estadio"],
    "Estadio": ["Suramericana", "Floresta"],
    "Floresta": ["Estadio", "Santa Lucía"],
    "Santa Lucía": ["Floresta", "San Javier"],
    "San Javier": ["Santa Lucía"]
}


# Líneas del sistema
lineas = {
    "Linea A": [
        "Niquía", "Bello", "Madera", "Acevedo", "Caribe",
        "Universidad", "Hospital", "Prado", "Parque Berrío",
        "San Antonio", "Alpujarra", "Exposiciones",
        "Industriales", "Poblado", "Aguacatala",
        "Ayurá", "Envigado", "Itagüí"
    ],

    "Linea B": [
        "San Antonio", "Cisneros", "Suramericana",
        "Estadio", "Floresta", "Santa Lucía", "San Javier"
    ]
}


# ==========================================================
# REGLAS LÓGICAS
# ==========================================================

def estan_conectadas(origen, destino):
    """
    Regla 1:
    Si una estación aparece en las conexiones de otra,
    entonces existe una conexión directa.
    """
    return destino in conexiones.get(origen, [])


def misma_linea(estacion1, estacion2):
    """
    Regla 2:
    Dos estaciones pertenecen a la misma línea
    si aparecen dentro de la misma línea.
    """
    for linea, estaciones in lineas.items():
        if estacion1 in estaciones and estacion2 in estaciones:
            return True

    return False


def es_transbordo(estacion):
    """
    Regla 3:
    Una estación es de transbordo si pertenece a más de una línea.
    """
    cantidad_lineas = 0

    for estaciones in lineas.values():
        if estacion in estaciones:
            cantidad_lineas += 1

    return cantidad_lineas > 1


# ==========================================================
# HEURÍSTICA
# ==========================================================

def heuristica(actual, destino):
    """
    Heurística sencilla basada en una estimación.
    Para este proyecto utilizamos 0 como estimación cuando
    no tenemos coordenadas geográficas.

    Esto permite aplicar la estructura de A* y garantizar
    una búsqueda por costo.
    """
    return 0


# ==========================================================
# ALGORITMO A*
# ==========================================================

def buscar_ruta(origen, destino):

    if origen not in conexiones:
        return None

    if destino not in conexiones:
        return None

    cola = []

    # (costo_total, costo_recorrido, estación, ruta)
    heapq.heappush(
        cola,
        (0, 0, origen, [origen])
    )

    visitados = set()

    while cola:

        _, costo, actual, ruta = heapq.heappop(cola)

        if actual == destino:
            return ruta

        if actual in visitados:
            continue

        visitados.add(actual)

        for vecino in conexiones[actual]:

            if vecino not in visitados:

                nuevo_costo = costo + 1

                prioridad = (
                    nuevo_costo +
                    heuristica(vecino, destino)
                )

                heapq.heappush(
                    cola,
                    (
                        prioridad,
                        nuevo_costo,
                        vecino,
                        ruta + [vecino]
                    )
                )

    return None


# ==========================================================
# MOSTRAR RESULTADO
# ==========================================================

def mostrar_ruta(ruta):

    if not ruta:
        print("\nNo se encontró una ruta.")
        return

    print("\n===================================")
    print("       RUTA ENCONTRADA")
    print("===================================\n")

    for i, estacion in enumerate(ruta):

        if i < len(ruta) - 1:
            print(estacion + " -> ", end="")
        else:
            print(estacion)

    print("\nNúmero de estaciones recorridas:",
          len(ruta) - 1)

    # Mostrar si hay transbordo
    transbordos = []

    for estacion in ruta:

        if es_transbordo(estacion):
            transbordos.append(estacion)

    if transbordos:
        print("Posibles estaciones de transbordo:",
              ", ".join(transbordos))

    else:
        print("No se requiere transbordo.")


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    print("==========================================")
    print(" SISTEMA INTELIGENTE DE RUTAS - METRO")
    print("==========================================")

    print("\nEstaciones disponibles:")

    estaciones = sorted(conexiones.keys())

    for estacion in estaciones:
        print("-", estacion)

    origen = input("\nIngrese la estación de origen: ")
    destino = input("Ingrese la estación de destino: ")

    origen = origen.strip().title()
    destino = destino.strip().title()

    if origen not in conexiones:
        print("\nLa estación de origen no existe.")

        return

    if destino not in conexiones:
        print("\nLa estación de destino no existe.")

        return

    if origen == destino:
        print("\nEl origen y el destino son iguales.")

        return

    ruta = buscar_ruta(origen, destino)

    mostrar_ruta(ruta)


if __name__ == "__main__":
    main()