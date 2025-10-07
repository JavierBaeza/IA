from collections import deque  # Importa la clase deque de la librería collections, que proporciona una cola eficiente.
import heapq  # Importa la librería heapq para manejar una cola de prioridad (min-heap) en A*.

# Representación del edificio como una matriz donde 1 es una celda accesible y 0 es una celda bloqueada.
# La letra 'E' representa el objetivo en la esquina inferior derecha.
edificio = [
    [1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1],
    [0, 0, 1, 0, 1],
    [1, 1, 1, 1, 'E']
]

# Coordenadas del inicio (esquina superior izquierda) y objetivo (esquina inferior derecha)
start = (0, 0)
goal = (4, 4)

# Algoritmo de búsqueda en anchura (BFS)
def bfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])  # Determina las dimensiones de la cuadrícula (número de filas y columnas).
    queue = deque([(start, [start])])  # Crea una cola (deque) que almacenará las posiciones y el camino recorrido hasta ahí.
    visited = set()  # Conjunto para rastrear las celdas visitadas y evitar ciclos.

    # Bucle principal del BFS
    while queue:
        (x, y), path = queue.popleft()  # Extrae el primer elemento de la cola: las coordenadas y el camino hasta ese punto.
        
        if (x, y) == goal:  # Si hemos llegado al objetivo, devuelve el camino encontrado.
            return path

        if (x, y) in visited:  # Si ya hemos visitado este punto, lo saltamos.
            continue
        visited.add((x, y))  # Marca el punto como visitado.

        # Explora las 4 direcciones (arriba, abajo, izquierda, derecha)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy  # Calcula las nuevas coordenadas.
            # Asegura que las nuevas coordenadas estén dentro de la cuadrícula y sean accesibles.
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 0 and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))  # Añade la nueva posición a la cola con el camino actualizado.

    return None  # Si no se encuentra la ruta, devuelve None.

# Algoritmo de búsqueda en profundidad (DFS)
def dfs(grid, start, goal, visited=None, path=None):
    if visited is None:  # Si no se ha pasado un conjunto de visitados, crea uno vacío.
        visited = set()
    if path is None:  # Si no se ha pasado un camino, comienza con uno vacío.
        path = []

    x, y = start  # Asigna las coordenadas del nodo actual.

    if (x, y) == goal:  # Si hemos llegado al objetivo, retorna el camino recorrido.
        return path + [goal]

    visited.add((x, y))  # Marca el nodo actual como visitado.

    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Definición de las 4 direcciones posibles.
    for dx, dy in neighbors:
        nx, ny = x + dx, y + dy  # Calcula las nuevas coordenadas.
        # Asegura que las nuevas coordenadas estén dentro de la cuadrícula y sean accesibles.
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 0 and (nx, ny) not in visited:
            result = dfs(grid, (nx, ny), goal, visited, path + [(x, y)])  # Llama recursivamente al DFS.
            if result:  # Si se encuentra una ruta, la retorna.
                return result

    return None  # Si no se encuentra la ruta, devuelve None.

# Algoritmo A* (A-star)
def a_star(grid, start, goal):
    open_list = []  # Lista abierta para la exploración (se usará como cola de prioridad).
    heapq.heappush(open_list, (0, start))  # Añade el nodo inicial con un costo de 0.
    
    came_from = {}  # Diccionario para reconstruir el camino recorrido.
    g_costs = {start: 0}  # Diccionario de costos g (distancia desde el inicio).
    f_costs = {start: heuristic(start, goal)}  # Diccionario de costos f (g + heurística).

    # Bucle principal del A*
    while open_list:
        _, current = heapq.heappop(open_list)  # Extrae el nodo con el menor costo f de la lista abierta.

        if current == goal:  # Si el nodo actual es el objetivo, reconstruye el camino.
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Devuelve el camino invertido (de inicio a fin).

        x, y = current  # Extrae las coordenadas actuales.
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Explora las 4 direcciones.
            nx, ny = x + dx, y + dy  # Calcula las nuevas coordenadas.
            # Asegura que las nuevas coordenadas estén dentro de la cuadrícula y sean accesibles.
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 0:
                tentative_g = g_costs[(x, y)] + 1  # Calcula el costo g del nuevo nodo.
                # Si el nodo no está en g_costs o se encontró un camino más corto, actualiza los costos.
                if (nx, ny) not in g_costs or tentative_g < g_costs[(nx, ny)]:
                    came_from[(nx, ny)] = (x, y)  # Registra el nodo anterior.
                    g_costs[(nx, ny)] = tentative_g  # Actualiza el costo g.
                    f_costs[(nx, ny)] = tentative_g + heuristic((nx, ny), goal)  # Actualiza el costo f.
                    heapq.heappush(open_list, (f_costs[(nx, ny)], (nx, ny)))  # Añade el nodo a la lista abierta.

    return None  # Si no se encuentra la ruta, devuelve None.

# Función heurística (distancia Manhattan)
def heuristic(pos, goal):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])  # Calcula la distancia Manhattan entre el nodo actual y el objetivo.

# Función para imprimir el resultado de cada algoritmo
def print_result(path, algorithm_name):
    if path:  # Si se encuentra un camino
        print(f"\nRuta encontrada usando {algorithm_name}:")
        print(" -> ".join([f"({x}, {y})" for x, y in path]))  # Imprime las coordenadas del camino.
    else:  # Si no se encuentra ruta
        print(f"\nNo se encontró ruta usando {algorithm_name}.")

# Función para ejecutar todos los algoritmos de búsqueda
def run_search():
    print("Ejecutando BFS...")
    bfs_result = bfs(edificio, start, goal)  # Ejecuta BFS
    print_result(bfs_result, "BFS")

    print("Ejecutando DFS...")
    dfs_result = dfs(edificio, start, goal)  # Ejecuta DFS
    print_result(dfs_result, "DFS")

    print("Ejecutando A*...")
    a_star_result = a_star(edificio, start, goal)  # Ejecuta A*
    print_result(a_star_result, "A*")

# Llamada principal a la función para ejecutar la búsqueda cuando el script se ejecute
if __name__ == "__main__":
    run_search()