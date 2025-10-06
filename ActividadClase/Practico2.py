# Importar deque desde collections para manejar la cola de BFS
from collections import deque
# Importar heapq para manejar la cola de prioridad de A* (montículo)
import heapq

# Representación del edificio como una cuadrícula
# 1 = camino libre, 0 = bloqueado, 'E' = salida de emergencia
edificio = [
    [1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1],
    [0, 0, 1, 0, 1],
    [1, 1, 1, 1, 'E']
]

# Definir las coordenadas de inicio y objetivo (salida de emergencia)
start = (0, 0)  # Punto de inicio (arriba a la izquierda)
goal = (4, 4)   # Salida de emergencia (abajo a la derecha)

# Función BFS (Breadth-First Search)
def bfs(grid, start, goal):
    # Obtener el número de filas y columnas del grid
    rows, cols = len(grid), len(grid[0])
    # Inicializar la cola (deque) con el nodo inicial y la ruta desde el inicio
    queue = deque([(start, [start])])  # La cola contiene una tupla: (nodo actual, ruta)
    # Conjunto de nodos visitados para evitar visitar el mismo nodo más de una vez
    visited = set()

    # Mientras haya nodos en la cola por explorar
    while queue:
        # Extraer el primer nodo de la cola
        (x, y), path = queue.popleft()

        # Si hemos alcanzado el objetivo, retornamos la ruta
        if (x, y) == goal:
            return path

        # Si el nodo ya ha sido visitado, lo saltamos
        if (x, y) in visited:
            continue
        visited.add((x, y))  # Marcar el nodo como visitado

        # Explorar los vecinos (arriba, abajo, izquierda, derecha)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            # Verificar que el vecino esté dentro del grid y no sea un bloqueado (0)
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 0 and (nx, ny) not in visited:
                # Añadir el vecino a la cola con la nueva ruta
                queue.append(((nx, ny), path + [(nx, ny)]))

    return None  # Si no se encuentra una ruta

# Función DFS (Depth-First Search)
def dfs(grid, start, goal, visited=None, path=None):
    # Si no hay un conjunto de nodos visitados, inicializarlo
    if visited is None:
        visited = set()
    # Si no hay una lista de camino, inicializarla
    if path is None:
        path = []

    x, y = start  # Extraer las coordenadas del nodo actual

    # Si hemos alcanzado el objetivo, retornar la ruta
    if (x, y) == goal:
        return path + [goal]

    # Marcar el nodo actual como visitado
    visited.add((x, y))

    # Explorar los vecinos (arriba, abajo, izquierda, derecha)
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Direcciones posibles
    for dx, dy in neighbors:
        nx, ny = x + dx, y + dy
        # Comprobar que el vecino está dentro del grid y no ha sido visitado ni es un bloqueado
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 0 and (nx, ny) not in visited:
            # Llamar recursivamente a DFS para explorar el vecino
            result = dfs(grid, (nx, ny), goal, visited, path + [(x, y)])
            if result:  # Si se encuentra un resultado (una ruta)
                return result

    return None  # Si no se encuentra una ruta

# Función A* (A-star)
def a_star(grid, start, goal):
    # Inicializar la lista abierta (open list) que contiene nodos por explorar
    open_list = []
    # Agregar el nodo de inicio con costo 0 a la lista abierta
    heapq.heappush(open_list, (0, start))  # (costo estimado, posición del nodo)
    
    # Diccionarios para rastrear el camino y costos de los nodos
    came_from = {}  # De qué nodo venimos para reconstruir el camino
    g_costs = {start: 0}  # Costo de llegar al nodo desde el inicio
    f_costs = {start: heuristic(start, goal)}  # Costo estimado total (g + heurística)

    # Mientras haya nodos por explorar en la lista abierta
    while open_list:
        # Extraer el nodo con el menor costo total (f_cost)
        _, current = heapq.heappop(open_list)

        # Si hemos llegado al objetivo, reconstruimos el camino y lo retornamos
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Devolver la ruta en el orden correcto

        x, y = current
        # Explorar los vecinos (arriba, abajo, izquierda, derecha)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            # Verificar que el vecino esté dentro del grid y no sea bloqueado
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 0:
                # Calcular el costo temporal para llegar al vecino
                tentative_g = g_costs[(x, y)] + 1
                if (nx, ny) not in g_costs or tentative_g < g_costs[(nx, ny)]:
                    # Actualizar los costos y el camino de llegada
                    came_from[(nx, ny)] = (x, y)
                    g_costs[(nx, ny)] = tentative_g
                    f_costs[(nx, ny)] = tentative_g + heuristic((nx, ny), goal)
                    heapq.heappush(open_list, (f_costs[(nx, ny)], (nx, ny)))

    return None  # Si no se encuentra una ruta

# Heurística para A* (distancia Manhattan)
def heuristic(pos, goal):
    # Distancia Manhattan: suma de las diferencias absolutas de las coordenadas
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

# Función para imprimir el resultado de la ruta encontrada
def print_result(path, algorithm_name):
    # Si se encuentra una ruta, imprimirla
    if path:
        print(f"\nRuta encontrada usando {algorithm_name}:")
        print(" -> ".join([f"({x}, {y})" for x, y in path]))  # Mostrar las coordenadas de la ruta
    else:
        print(f"\nNo se encontró ruta usando {algorithm_name}.")

# Función principal para ejecutar todos los algoritmos
def run_search():
    # Ejecutar BFS
    print("Ejecutando BFS...")
    bfs_result = bfs(edificio, start, goal)
    print_result(bfs_result, "BFS")

    # Ejecutar DFS
    print("Ejecutando DFS...")
    dfs_result = dfs(edificio, start, goal)
    print_result(dfs_result, "DFS")

    # Ejecutar A*
    print("Ejecutando A*...")
    a_star_result = a_star(edificio, start, goal)
    print_result(a_star_result, "A*")

# Ejecutar la función principal
if __name__ == "__main__":
    run_search()
