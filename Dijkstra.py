import heapq
import networkx as nx
import matplotlib.pyplot as plt

# --------------------------------------------------
#  ALGORITMO DE DIJKSTRA (CON IMPRESIÓN PASO A PASO)
# --------------------------------------------------
def dijkstra(grafo, inicio, fin=None, mostrar_pasos=True):
    """
    grafo: diccionario de diccionarios
           { 'A': {'B': 4, 'C': 2}, ... }
    inicio: nodo de origen
    fin: nodo destino (opcional, si quieres ruta a uno en específico)
    mostrar_pasos: si True, imprime el proceso paso a paso
    """

    # 1. Inicializar distancias a infinito, excepto el inicio
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0

    # 2. Diccionario para reconstruir el camino
    anterior = {nodo: None for nodo in grafo}

    # 3. Cola de prioridad (min-heap): (distancia_acumulada, nodo)
    cola = [(0, inicio)]

    # 4. Conjunto de nodos visitados
    visitados = set()

    paso = 0

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        # Si ya está visitado, saltar
        if nodo_actual in visitados:
            continue

        visitados.add(nodo_actual)

        if mostrar_pasos:
            print(f"\n--- Paso {paso} ---")
            print(f"Nodo seleccionado: {nodo_actual}")
            print(f"Distancia confirmada a {nodo_actual}: {distancia_actual}")
            print("Distancias actuales:")
            for n, d in distancias.items():
                print(f"  {n}: {d}")
            paso += 1

        # Si ya llegamos al nodo fin y lo queremos solo a él, podemos cortar
        if fin is not None and nodo_actual == fin:
            break

        # 5. Relajar aristas vecinas
        for vecino, peso in grafo[nodo_actual].items():
            if vecino in visitados:
                continue

            nueva_dist = distancia_actual + peso

            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                anterior[vecino] = nodo_actual
                heapq.heappush(cola, (nueva_dist, vecino))

                if mostrar_pasos:
                    print(f"  Actualizando a {vecino}: nueva distancia = {nueva_dist} (viene de {nodo_actual})")

    return distancias, anterior


def reconstruir_camino(anterior, inicio, fin):
    """
    Reconstruye el camino más corto de inicio a fin usando el diccionario 'anterior'.
    """
    camino = []
    nodo = fin
    while nodo is not None:
        camino.append(nodo)
        nodo = anterior[nodo]
    camino.reverse()

    if not camino or camino[0] != inicio:
        return []  # No hay camino
    return camino


# -----------------------------------------
#  FUNCIÓN PARA DIBUJAR EL GRAFO Y LA RUTA
# -----------------------------------------
def dibujar_grafo(grafo, camino=None, titulo="Grafo - Algoritmo de Dijkstra"):
    """
    grafo: diccionario de diccionarios
    camino: lista con la ruta más corta (por ejemplo ['A', 'C', 'D'])
    titulo: título de la gráfica
    """

    G = nx.DiGraph()  # Dirigido; si tu grafo fuera no dirigido, usa Graph()

    # Añadir nodos y aristas con pesos
    for origen, vecinos in grafo.items():
        for destino, peso in vecinos.items():
            G.add_edge(origen, destino, weight=peso)

    pos = nx.spring_layout(G, seed=42)  # Layout automático

    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_size=800)

    # Dibujar todas las aristas
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20)

    # Etiquetas de nodos
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    # Etiquetas de pesos en las aristas
    etiquetas_aristas = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas_aristas, font_size=10)

    # Si hay camino, resaltar la ruta más corta
    if camino and len(camino) > 1:
        # Crear lista de aristas en el camino
        aristas_camino = list(zip(camino[:-1], camino[1:]))

        # Volver a dibujar esas aristas con más grosor y color diferente
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=aristas_camino,
            edge_color='red',
            width=3,
            arrowstyle='->',
            arrowsize=25
        )

        # Resaltar nodos del camino
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=camino,
            node_color='lightcoral',
            node_size=900
        )

    plt.title(titulo)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


# ---------------------------
#  EJEMPLO DE USO (MAIN)
# ---------------------------
if __name__ == "__main__":
    # Grafo de ejemplo (puedes modificarlo)
    grafo = {
        "A": {"B": 4, "C": 2},
        "B": {"C": 5, "D": 10},
        "C": {"D": 3},
        "D": {}
    }

    print("Nodos disponibles:", list(grafo.keys()))
    inicio = input("Ingresa el nodo de inicio: ").strip()
    fin = input("Ingresa el nodo de destino: ").strip()

    if inicio not in grafo or fin not in grafo:
        print("Error: alguno de los nodos no existe en el grafo.")
    else:
        print("\n>>> Ejecutando Dijkstra paso a paso...\n")
        distancias, anterior = dijkstra(grafo, inicio, fin, mostrar_pasos=True)

        camino = reconstruir_camino(anterior, inicio, fin)

        print("\n==============================")
        print("  RESULTADOS FINALES")
        print("==============================")
        print("Distancias mínimas desde", inicio)
        for nodo, dist in distancias.items():
            print(f"  {nodo}: {dist}")

        if camino:
            print(f"\nCamino más corto de {inicio} a {fin}: {' -> '.join(camino)}")
            print(f"Distancia total: {distancias[fin]}")
        else:
            print(f"\nNo existe camino desde {inicio} hasta {fin}.")

        # Dibujar grafo con el camino más corto resaltado
        dibujar_grafo(
            grafo,
            camino=camino,
            titulo=f"Ruta más corta de {inicio} a {fin} (Dijkstra)"
        )
