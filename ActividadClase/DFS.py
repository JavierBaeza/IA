# -------- DFS: encuentra algún camino en una cuadrícula 10x10 --------
def dfs_path_grid(grid, start, goal):
    R, C = 10, 10
    
    # Movimientos posibles (incluyo letras por si quieres reconstruir movimientos)
    dirs = [(-1,0,'U'),(1,0,'D'),(0,-1,'L'),(0,1,'R')]
    
    # Conjunto de celdas visitadas
    visited = set()
    
    # Diccionario de padres (para reconstruir el camino)
    parent = {start: None}

    # Función recursiva DFS
    def dfs(u):
        # Si llegamos a la meta, terminamos
        if u == goal:
            return True
        r, c = u
        visited.add(u)
        
        # Probar vecinos en orden
        for dr, dc, mv in dirs:
            nr, nc = r+dr, c+dc
            v = (nr, nc)
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and v not in visited:
                parent[v] = u
                if dfs(v):    # llamada recursiva
                    return True
        return False

    # Ejecutamos DFS desde el inicio
    found = dfs(start)
    
    # Reconstrucción del camino
    path = []
    if found:
        x = goal
        while x is not None:
            path.append(x)
            x = parent[x]
        path.reverse()
    return path

# -------- Función para imprimir matriz con camino --------
def imprimir_matriz_con_camino(grid, path, start, goal):
    matriz = [row[:] for row in grid]
    for r, c in path:
        if (r, c) != start and (r, c) != goal:
            matriz[r][c] = "*"
    matriz[start[0]][start[1]] = "S"
    matriz[goal[0]][goal[1]] = "G"
    for fila in matriz:
        print(" ".join(str(x) for x in fila))

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

    # Ejecutamos DFS
    path = dfs_path_grid(maze10, start, goal)

    # Mostramos resultados
    print("=== DFS ===")
    print("Camino encontrado:", path)
    print("Longitud:", len(path))
    print("\nMatriz con camino DFS:")
    imprimir_matriz_con_camino(maze10, path, start, goal)
