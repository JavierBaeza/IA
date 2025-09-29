# Importamos deque (cola eficiente) de la librería estándar
from collections import deque

# -------- BFS: encuentra el camino más corto en una cuadrícula 10x10 --------
def bfs_shortest_path_grid(grid, start, goal):
    # Dimensiones fijas de la grilla: 10 filas x 10 columnas
    R, C = 10, 10
    
    # Posibles movimientos: arriba, abajo, izquierda, derecha
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    
    # Cola (FIFO) para explorar los nodos pendientes
    q = deque([start])
    
    # Conjunto de nodos visitados, inicializado con el inicio
    visited = {start}
    
    # Diccionario para reconstruir el camino: guarda el padre de cada nodo
    parent = {start: None}

    # Mientras la cola no esté vacía
    while q:
        # Tomamos el primer elemento de la cola
        cur = q.popleft()
        
        # Si llegamos al objetivo, salimos del ciclo
        if cur == goal:
            break
        
        # Extraemos coordenadas de la celda actual
        r, c = cur
        
        # Recorremos los posibles movimientos
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc   # nuevas coordenadas
            nxt = (nr, nc)        # celda siguiente
            
            # Verificamos:
            # 1) que esté dentro de los límites
            # 2) que sea camino libre (0)
            # 3) que no se haya visitado antes
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and nxt not in visited:
                # Marcamos como visitado
                visited.add(nxt)
                # Guardamos el "padre" para reconstruir el camino después
                parent[nxt] = cur
                # Encolamos esta celda para explorarla más adelante
                q.append(nxt)

    # Reconstrucción del camino (si se encontró el objetivo)
    path = []
    if goal in parent:
        x = goal
        while x is not None:
            path.append(x)
            x = parent[x]   # retrocedemos hasta el inicio
        path.reverse()      # invertimos para ir de inicio a meta
    return path

# -------- Función para imprimir la matriz con el camino marcado --------
def imprimir_matriz_con_camino(grid, path, start, goal):
    # Creamos una copia de la grilla para no modificar la original
    matriz = [row[:] for row in grid]
    
    # Recorremos las celdas del camino y marcamos con "*"
    for r, c in path:
        if (r, c) != start and (r, c) != goal:  # no marcamos inicio ni meta
            matriz[r][c] = "*"
    
    # Marcamos inicio y meta
    matriz[start[0]][start[1]] = "S"
    matriz[goal[0]][goal[1]] = "G"
    
    # Imprimimos la matriz en formato "bonito"
    for fila in matriz:
        print(" ".join(str(x) for x in fila))

# -------- Programa principal --------
if __name__ == "__main__":
    # Definimos el laberinto 10x10 (0 = libre, 1 = pared)
    maze10 = [
        [0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,1,0],
        [0,1,1,1,1,1,1,0,1,0],
        [0,1,0,0,0,0,1,0,1,0],
        [0,1,0,1,1,0,1,0,1,0],
        [0,1,0,1,0,0,0,0,1,0],
        [0,1,0,1,0,1,1,1,1,0],
        [0,0,0,1,0,0,0,0,0,0],
        [1,1,0,1,1,1,1,1,1,0],
    ]
    start, goal = (0,0), (9,9)

    # Ejecutamos BFS
    path = bfs_shortest_path_grid(maze10, start, goal)

    # Mostramos resultados
    print("=== BFS ===")
    print("Camino más corto:", path)
    print("Longitud:", len(path))
    print("\nMatriz con camino BFS:")
    imprimir_matriz_con_camino(maze10, path, start, goal)
