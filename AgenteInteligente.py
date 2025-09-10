# npc_reflejo_con_hp_grid.py
# NPC de reflejo simple en un grid sin obstáculos, con vida del jugador.
# Requisitos: Python 3.x

import random #Movimientos aleatorios

W, H = 10, 7  # ancho x alto del grid (10 columnas, 7 filas) 

def manhattan(a, b):
    """Distancia Manhattan: casillas que separan dos posiciones (sin diagonales)."""
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def vecinos(p):
    """Devuelve las posiciones vecinas válidas (arriba, abajo, izquierda, derecha)."""
    x, y = p
    cand = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    return [(i,j) for (i,j) in cand if 0 <= i < W and 0 <= j < H]

def paso_hacia(src, dst):
    """
    Movimiento simple: da un paso desde src (origen, posición del NPC)
    hacia dst (destino, posición del jugador) dentro del grid.
    """
    x,y = src; tx,ty = dst
    opciones = []
    if tx > x: opciones.append((x+1,y))
    if tx < x: opciones.append((x-1,y))
    if ty > y: opciones.append((x,y+1))
    if ty < y: opciones.append((x,y-1))
    opciones = [o for o in opciones if 0 <= o[0] < W and 0 <= o[1] < H]
    return random.choice(opciones) if opciones else src

def dibujar(player, npc, turno, log, hp_player):
    """Imprime el estado actual del grid en consola."""
    print(f"Turno {turno} | {log}")
    for y in range(H):
        fila = ""
        for x in range(W):
            if (x,y) == player: fila += "P"   # jugador
            elif (x,y) == npc:  fila += "E"   # enemigo (NPC)
            else:               fila += "."   # celda vacía
        print(fila)
    print(f"HP Jugador: {hp_player}")
    print("-"*W)

def main():
    random.seed(1)         # semilla para reproducibilidad
    player = (2, 2)        # posición inicial del jugador
    npc    = (7, 4)        # posición inicial del NPC
    hp_player = 20         # vida inicial del jugador
    MAX_TURNS = 50         # máximo de turnos para evitar bucle infinito

    for t in range(1, MAX_TURNS+1):
        # 1) Jugador se mueve al azar (o se queda en su celda)
        movs = vecinos(player) + [player]
        player = random.choice(movs)

        # 2) NPC decide por reglas de reflejo simple
        d = manhattan(npc, player)
        log = ""
        if d == 1 or d == 0:  # adyacente ⇒ ataca
            dmg = random.randint(2,5)
            hp_player = max(0, hp_player - dmg)
            log = f"NPC ATTACK (daño {dmg})"
        elif d <= 4:  # cerca ⇒ persigue
            npc = paso_hacia(npc, player)
            log = "NPC CHASE (se acerca)"
        else:  # lejos ⇒ deambula
            movs = vecinos(npc) + [npc]
            npc = random.choice(movs)
            log = "NPC WANDER (deambula)"

        # mostrar estado del turno
        dibujar(player, npc, t, log, hp_player)

        # condición de fin
        if hp_player == 0:
            print(">> El jugador ha sido derrotado en el turno", t)
            break
    else:
        print(">> Se alcanzó el máximo de turnos sin que muera el jugador.")

if __name__ == "__main__":
    main()