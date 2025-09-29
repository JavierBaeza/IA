# Importamos deque (cola eficiente) para BFS
from collections import deque

# -------- BFS: encuentra el camino más corto --------
def bfs_shortest_path_grid(grid, start, goal):
    R, C = 10, 10
    # Movimientos posibles: (fila, columna, letra)
    dirs = [(-1,0,'U'),(1,0,'D'),(0,-1,'L'),(0,1,'R')]
    q = deque([start])
    visited = {start}
    parent = {start: None}
    parent_move = {start: None}  # guarda el movimiento usado para llegar

    while q:
        cur = q.popleft()
        if cur == goal:
            break
        r, c = cur
        for dr, dc, mv in dirs:
            nr, nc = r+dr, c+dc
            nxt = (nr, nc)
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                parent_move[nxt] = mv
                q.append(nxt)

    # Reconstrucción del camino y movimientos
    path, moves = [], ""
    if goal in parent:
        x = goal
        seq = []
        while x is not None:
            path.append(x)
            if parent_move[x] is not None:
                seq.append(parent_move[x])
            x = parent[x]
        path.reverse()
        moves = "".join(reversed(seq))  # invertimos para ir de inicio a meta
    return path, moves

# -------- DFS: encuentra algún camino --------
def dfs_path_grid(grid, start, goal):
    R, C = 10, 10
    dirs = [(-1,0,'U'),(1,0,'D'),(0,-1,'L'),(0,1,'R')]
    visited = set()
    parent = {start: None}
    parent_move = {start: None}

    def dfs(u):
        if u == goal:
            return True
        r, c = u
        visited.add(u)
        for dr, dc, mv in dirs:
            nr, nc = r+dr, c+dc
            v = (nr, nc)
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and v not in visited:
                parent[v] = u
                parent_move[v] = mv
                if dfs(v):
                    return True
        return False

    found = dfs(start)
    path, moves = [], ""
    if found:
        x = goal
        seq = []
        while x is not None:
            path.append(x)
            if parent_move[x] is not None:
                seq.append(parent_move[x])
            x = parent[x]
        path.reverse()
        moves = "".join(reversed(seq))
    return path, moves

# -------- Función para marcar camino en la matriz --------
def matriz_con_camino(grid, path, start, goal):
    matriz = [row[:] for row in grid]
    for r, c in path:
        if (r, c) != start and (r, c) != goal:
            matriz[r][c] = "*"
    matriz[start[0]][start[1]] = "S"
    matriz[goal[0]][goal[1]] = "G"
    return matriz

# -------- Función para imprimir dos matrices lado a lado --------
def imprimir_lado_a_lado(matriz1, matriz2, titulo1="BFS", titulo2="DFS"):
    print(f"{titulo1:^30} | {titulo2:^30}")
    print("-"*30 + "+" + "-"*30)
    for f1, f2 in zip(matriz1, matriz2):
        fila1 = " ".join(str(x) for x in f1)
        fila2 = " ".join(str(x) for x in f2)
        print(f"{fila1:<30} | {fila2:<30}")

# -------- Programa principal --------
if __name__ == "__main__":
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

    # Ejecutamos BFS y DFS
    bfs_path, bfs_moves = bfs_shortest_path_grid(maze10, start, goal)
    dfs_path, dfs_moves = dfs_path_grid(maze10, start, goal)

    # Mostramos info de los caminos
    print("=== Comparación BFS vs DFS ===\n")
    print("BFS -> Camino más corto:", bfs_path)
    print("Longitud BFS:", len(bfs_path))
    print("Movimientos BFS:", bfs_moves, "\n")

    print("DFS -> Algún camino encontrado:", dfs_path)
    print("Longitud DFS:", len(dfs_path))
    print("Movimientos DFS:", dfs_moves, "\n")

    # Obtenemos matrices marcadas
    matriz_bfs = matriz_con_camino(maze10, bfs_path, start, goal)
    matriz_dfs = matriz_con_camino(maze10, dfs_path, start, goal)

    # Imprimimos matrices lado a lado
    imprimir_lado_a_lado(matriz_bfs, matriz_dfs, "Camino BFS", "Camino DFS")
