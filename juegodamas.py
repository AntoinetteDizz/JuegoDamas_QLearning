import pygame
import sys
import random
import pickle  # Para guardar y cargar la tabla Q
import json
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------Constantes del juego
ANCHO_VENTANA = 400
ALTO_VENTANA = 400
TAMANO_CASILLA = 100

BLANCO = (255, 255, 255)
PBLANCAS = (245, 245, 225)  # Color para piezas blancas
PNEGRAS = (71, 71, 70)      # Color para piezas negras
GRIS = (169, 169, 169)      # Color gris para el borde
VERDE = (50, 205, 50)       # Verde para movimientos válidos
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_CLARO = (240, 217, 181)  # Color claro del tablero
COLOR_OSCURO = (181, 136, 99)  # Color oscuro del tablero
COLOR_AMARILLO = (255, 255, 0)  # Color para resaltar selección

TEXTO_COLOR = (50, 50, 60)  # Color del texto (negro)
RADIO_PIEZA = 40
RADIO_REINA = 45

# Parámetros de Q-Learning
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.9  # Factor de descuento
epsilon = 0.2  # Factor de exploración
q_table = {}  # Diccionario para almacenar los valores Q

# Inicialización de contadores
movimientos_totales = 0
fichas_blancas = 2  # Número inicial de fichas blancas
fichas_negras = 2   # Número inicial de fichas negras
#-------------------------------------------------------------------------------Constantes del juego


#-------------------------------------------------------------------------------Inicialización de Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Tablero de Damas 4x4")

# Inicializar fuente
fuente = pygame.font.Font(None, 36)

# Representación del tablero (1: ficha blanca, 2: ficha negra, 0: casilla vacía)
tablero = [[0 for _ in range(4)] for _ in range(4)]

# Inicialización de las piezas en el tablero (colocamos dos piezas por jugador)
tablero[0][0] = 1  # Ficha blanca en (0, 0)
tablero[0][2] = 1  # Ficha blanca en (0, 2)
tablero[3][1] = 2  # Ficha negra en (3, 1)
tablero[3][3] = 2  # Ficha negra en (3, 3)

# Variables para controlar la pieza seleccionada y su posición original
pieza_seleccionada = None
posicion_original = None
jugador_turno = 1  # 1 para jugador blanco, 2 para jugador negro
movimientos_disponibles = []  # Lista de movimientos válidos
#-------------------------------------------------------------------------------Inicialización de Pygame


#-------------------------------------------------------------------------------Archivo para estadísticas
STATS_FILE = "stats.json"

def cargar_estadisticas():
    try:
        with open(STATS_FILE, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print("Archivo no encontrado. Creando estadísticas iniciales...")
        estadisticas_iniciales = {
            "victorias_humano": 0,
            "victorias_ia": 0,
            "partidas_jugadas": 0
        }
        guardar_estadisticas(estadisticas_iniciales)
        return estadisticas_iniciales

# Función para guardar estadísticas
def guardar_estadisticas(estadisticas):
    try:
        with open(STATS_FILE, "w") as archivo:
            json.dump(estadisticas, archivo, indent=4)
        #print("Estadísticas guardadas correctamente.")
    except Exception as e:
        print(f"Error al guardar estadísticas: {e}")

estadisticas = cargar_estadisticas()

# Función para graficar resultados
def graficar_resultados():
    # Generar datos para la gráfica
    partidas = list(range(1, estadisticas["partidas_jugadas"] + 1))
    victorias_ia = [estadisticas["victorias_ia"]] * len(partidas)
    victorias_humano = [estadisticas["victorias_humano"]] * len(partidas)

    plt.figure(figsize=(10, 6))
    plt.plot(partidas, victorias_ia, label="Victorias IA", marker="o", color="red")
    plt.plot(partidas, victorias_humano, label="Victorias Humano", marker="o", color="blue")

    plt.xlabel("Número de Partidas Jugadas")
    plt.ylabel("Número de Victorias")
    plt.title("Desempeño en Partidas")
    plt.legend()
    plt.grid()
    plt.tight_layout()

    plt.show()
#-------------------------------------------------------------------------------Archivo para estadísticas


#-------------------------------------------------------------------------------Tablero
def dibujar_tablero():
    # Dibuja el tablero y las piezas
    for fila in range(4):
        for columna in range(4):
            rect = pygame.Rect(columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA)
            
            # Alternar colores del tablero
            if (fila + columna) % 2 == 0:
                pygame.draw.rect(pantalla, COLOR_OSCURO, rect)
            else:
                pygame.draw.rect(pantalla, COLOR_CLARO, rect)
            
            # Dibujar piezas
            pieza = tablero[fila][columna]
            if pieza == 1:  # Ficha blanca
                pygame.draw.circle(pantalla, COLOR_BLANCO, rect.center, RADIO_PIEZA)
            elif pieza == 2:  # Ficha negra
                pygame.draw.circle(pantalla, COLOR_NEGRO, rect.center, RADIO_PIEZA)
            elif pieza == -1:  # Reina blanca
                pygame.draw.circle(pantalla, COLOR_BLANCO, rect.center, RADIO_PIEZA)
                pygame.draw.circle(pantalla, COLOR_AMARILLO, rect.center, RADIO_REINA, 2)
            elif pieza == -2:  # Reina negra
                pygame.draw.circle(pantalla, COLOR_NEGRO, rect.center, RADIO_PIEZA)
                pygame.draw.circle(pantalla, COLOR_AMARILLO, rect.center, RADIO_REINA, 2)

    # Dibujar borde amarillo si hay una pieza seleccionada
    if posicion_original:
        fila, columna = posicion_original
        rect = pygame.Rect(columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA)
        pygame.draw.rect(pantalla, COLOR_AMARILLO, rect, 3)

# Función para dibujar los movimientos disponibles
def dibujar_movimientos_disponibles():
    for fila, columna in movimientos_disponibles:
        pygame.draw.rect(pantalla, VERDE, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))

# Función para dibujar las piezas
def dibujar_fichas():
    for fila in range(4):
        for columna in range(4):
            if tablero[fila][columna] == 1 or tablero[fila][columna] == -1:  # Ficha blanca o reina blanca
                pygame.draw.circle(pantalla, GRIS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 3)
                pygame.draw.circle(pantalla, PBLANCAS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3)
            elif tablero[fila][columna] == 2 or tablero[fila][columna] == -2:  # Ficha negra o reina negra
                pygame.draw.circle(pantalla, GRIS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 3)
                pygame.draw.circle(pantalla, PNEGRAS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3)
#-------------------------------------------------------------------------------Tablero


#-------------------------------------------------------------------------------Jugador Humano
def manejar_eventos():
    global pieza_seleccionada, posicion_original, jugador_turno, movimientos_disponibles, movimientos_totales, fichas_negras

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            fila = y // TAMANO_CASILLA
            columna = x // TAMANO_CASILLA

            # Asegurarse de que solo las piezas blancas (jugador) puedan ser seleccionadas
            if jugador_turno == 1:  # Si es el turno del jugador (jugador 1 controla las piezas blancas)
                if pieza_seleccionada:
                    if (fila, columna) in movimientos_disponibles:
                        # Mover la pieza
                        movimientos_totales += 1
                        tablero[fila][columna] = pieza_seleccionada
                        tablero[posicion_original[0]][posicion_original[1]] = 0
                        
                        # Convertir en reina si llegamos al borde del tablero
                        if (pieza_seleccionada == 1 and fila == 3) or (pieza_seleccionada == 2 and fila == 0):
                            tablero[fila][columna] = -pieza_seleccionada  # Convertir a reina (negativa para indicar que es reina)
                        
                        # Eliminar pieza capturada si hay captura
                        if abs(fila - posicion_original[0]) == 2:
                            fila_rival = (fila + posicion_original[0]) // 2
                            columna_rival = (columna + posicion_original[1]) // 2
                            tablero[fila_rival][columna_rival] = 0
                            fichas_negras -= 1  # Restamos una ficha negra
                        
                        pieza_seleccionada = None
                        posicion_original = None
                        movimientos_disponibles = []
                        jugador_turno = 2  # Cambiar turno a la IA
                    else:
                        # Si no es un movimiento válido
                        pieza_seleccionada = None
                        posicion_original = None
                        movimientos_disponibles = []
                elif tablero[fila][columna] in (1, -1):  # Solo seleccionar piezas blancas (jugador 1)
                    pieza_seleccionada = tablero[fila][columna]
                    posicion_original = (fila, columna)
                    movimientos_disponibles = obtener_movimientos_validos(fila, columna)
#-------------------------------------------------------------------------------Jugador Humano


#-------------------------------------------------------------------------------Movimientos validos
def obtener_movimientos_validos(fila, columna):
    movimientos = []
    pieza = tablero[fila][columna]

    if pieza == -1 or pieza == -2:  # Reinas (blanca o negra)
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Movimiento en todas direcciones
    elif pieza == 1:  # Ficha blanca normal
        direcciones = [(1, -1), (1, 1)]  # Solo hacia adelante (abajo)
    elif pieza == 2:  # Ficha negra normal
        direcciones = [(-1, -1), (-1, 1)]  # Solo hacia adelante (arriba)
    
    for d_fila, d_columna in direcciones:
        nueva_fila, nueva_columna = fila + d_fila, columna + d_columna
        # Movimiento simple
        if 0 <= nueva_fila < 4 and 0 <= nueva_columna < 4 and tablero[nueva_fila][nueva_columna] == 0:
            movimientos.append((nueva_fila, nueva_columna))

        # Movimiento de captura
        salto_fila, salto_columna = fila + 2 * d_fila, columna + 2 * d_columna
        if (0 <= salto_fila < 4 and 0 <= salto_columna < 4 and
            tablero[nueva_fila][nueva_columna] not in (0, pieza) and
            tablero[salto_fila][salto_columna] == 0):
            movimientos.append((salto_fila, salto_columna))
    
    return movimientos
#-------------------------------------------------------------------------------Movimientos validos


#-------------------------------------------------------------------------------Archivo de Entrenamiento de Agente
def obtener_estado(tablero):
    # Convierte el tablero en un estado único representado como tupla de tuplas
    return tuple(tuple(fila) for fila in tablero)

def guardar_q_table(filename="q_table.pkl"):
    try:
        with open(filename, "wb") as file:
            pickle.dump(q_table, file)
        #print("Tabla Q guardada con éxito.")
    except Exception as e:
        print(f"Error al guardar la tabla Q: {e}")


def cargar_q_table(filename="q_table.pkl"):
    global q_table
    try:
        with open(filename, "rb") as file:
            q_table = pickle.load(file)
    except FileNotFoundError:
        q_table = {}
        print("Archivo no encontrado, inicializando tabla Q vacía.")
#-------------------------------------------------------------------------------Archivo de Entrenamiento de Agente


#-------------------------------------------------------------------------------Seleccion de accion del Agente
def seleccionar_accion(estado, acciones_validas):
    if not acciones_validas:
        return None  # Si no hay acciones válidas, retorna None
    if random.uniform(0, 1) < epsilon:
        return random.choice(acciones_validas)  # Exploración
    if estado in q_table and q_table[estado]:
        return max(q_table[estado], key=q_table[estado].get, default=random.choice(acciones_validas))  # Explotación
    return random.choice(acciones_validas)  # Si no hay Q para el estado, explora
#-------------------------------------------------------------------------------Seleccion de accion del Agente


#-------------------------------------------------------------------------------Actualizar Q
def actualizar_q(estado, accion, recompensa, nuevo_estado):
    max_q_nuevo_estado = max(q_table.get(nuevo_estado, {}).values(), default=0)
    q_actual = q_table.setdefault(estado, {}).get(accion, 0)
    q_table[estado][accion] = q_actual + alpha * (recompensa + gamma * max_q_nuevo_estado - q_actual)
#-------------------------------------------------------------------------------Actualizar Q


#-------------------------------------------------------------------------------Jugador Agente
def movimiento_ia_qlearning():
    global movimientos_totales, fichas_blancas, fichas_negras, jugador_turno

    estado = obtener_estado(tablero)  # Convertir tablero a un estado único
    acciones_validas = []

    # Generar acciones válidas
    for fila in range(4):
        for columna in range(4):
            if tablero[fila][columna] in (2, -2):  # IA (negras o reinas negras)
                movimientos = obtener_movimientos_validos(fila, columna)
                for movimiento in movimientos:
                    acciones_validas.append((fila, columna, movimiento[0], movimiento[1]))

    if not acciones_validas:
        print("No hay acciones válidas para la IA.")
        return False  # No hay movimientos posibles

    # Seleccionar acción usando epsilon-greedy
    accion = seleccionar_accion(estado, acciones_validas)

    if accion is None:
        print("No se pudo seleccionar una acción válida.")
        return False  # Salir si no hay una acción válida

    # Realizar la acción
    fila, columna, nueva_fila, nueva_columna = accion
    recompensa = 0
    tablero[nueva_fila][nueva_columna] = tablero[fila][columna]
    tablero[fila][columna] = 0
    # Verificar si capturó una pieza
    if abs(nueva_fila - fila) == 2:  # Solo en movimientos de captura (distancia 2)
        fila_rival = (fila + nueva_fila) // 2  # Calcula la fila de la pieza intermedia
        columna_rival = (columna + nueva_columna) // 2  # Calcula la columna de la pieza intermedia
        pieza_rival = tablero[fila_rival][columna_rival]  # Obtiene la pieza en la posición intermedia

        # Verificar que la pieza rival es del oponente antes de eliminarla
        if pieza_rival in (1, -1):  # Si la pieza rival es una pieza blanca o reina blanca
            tablero[fila_rival][columna_rival] = 0  # Elimina la pieza rival
            fichas_blancas -= 1  # Actualiza la cantidad de piezas blancas
            recompensa = 5  # Recompensa por capturar


    # Convertir a reina si aplica
    if nueva_fila == 0:
        tablero[nueva_fila][nueva_columna] = -2  # Reina negra
        recompensa += 5  # Recompensa por convertirse en reina

    # Actualizar las fichas restantes
    fichas_blancas = sum(1 for fila in tablero for celda in fila if celda == 1 or celda == -1)
    fichas_negras = sum(1 for fila in tablero for celda in fila if celda == 2 or celda == -2)

    # Actualizar tabla Q
    nuevo_estado = obtener_estado(tablero)
    actualizar_q(estado, accion, recompensa, nuevo_estado)

    jugador_turno = 1  # Cambiar turno al jugador
    movimientos_totales += 1
    return True
#-------------------------------------------------------------------------------Jugador Agente


#-------------------------------------------------------------------------------Fin de Juego
def mostrar_mensaje_fin(mensaje):
    texto = fuente.render(mensaje, True, TEXTO_COLOR)
    pantalla.blit(texto, (10, ALTO_VENTANA - 40))  # Mueve el mensaje al área inferior del tablero
    pygame.display.update()
    pygame.time.wait(3000)  # Espera 3 segundos antes de cerrar el juego
    pygame.quit()
    sys.exit()

def verificar_fin_juego():
    global movimientos_totales, fichas_blancas, fichas_negras

    # Inicializamos recompensa_final
    recompensa_final = 0  # Recompensa neutral por empate o sin resultado final

    # Verificar si el juego ha terminado
    if movimientos_totales == 64:
        mostrar_mensaje_fin("Es un Empate")
        recompensa_final = 0  # Recompensa por empate (neutral)
    elif fichas_blancas == 0:
        
        recompensa_final = 10  # Recompensa por ganar (para la IA, que juega con piezas negras)
        #-----------------------------------------------------------------------
        estadisticas["victorias_ia"] += 1
        estadisticas["partidas_jugadas"] += 1
        print(f"Victorias IA: {estadisticas['victorias_ia']}, Partidas Jugadas: {estadisticas['partidas_jugadas']}")
        guardar_estadisticas(estadisticas)
        # Actualiza la tabla Q con recompensa final (sin acción futura, ya que el juego terminó)
        estado = obtener_estado(tablero)
        actualizar_q(estado, None, recompensa_final, None)  # No hay acción futura al final del juego
        #-------------------------------------------------------------------------------
        mostrar_mensaje_fin("¡Ganan las piezas negras!")
    elif fichas_negras == 0:
        recompensa_final = -10  # Penalización por perder (para la IA, que juega con piezas negras)
        #-------------------------------------------------------------------------------
        estadisticas["victorias_humano"] += 1
        estadisticas["partidas_jugadas"] += 1
        print(f"Victorias Humano: {estadisticas['victorias_humano']}, Partidas Jugadas: {estadisticas['partidas_jugadas']}")
        guardar_estadisticas(estadisticas)
        # Actualiza la tabla Q con recompensa final (sin acción futura, ya que el juego terminó)
        estado = obtener_estado(tablero)
        actualizar_q(estado, None, recompensa_final, None)  # No hay acción futura al final del juego
        #-------------------------------------------------------------------------------
        mostrar_mensaje_fin("¡Ganan las piezas blancas!")
#-------------------------------------------------------------------------------Fin de Juego


#-------------------------------------------------------------------------------Juego Principal
while True:
    # Cargar tabla Q al inicio
    cargar_q_table()

    pantalla.fill(BLANCO)
    dibujar_tablero()
    dibujar_fichas()
    dibujar_movimientos_disponibles()
    verificar_fin_juego()

    # Llamar a la función de eventos para manejar los clics y otros eventos
    manejar_eventos()

    if jugador_turno == 2:  # Turno de la IA
        if movimiento_ia_qlearning():
            jugador_turno = 1

    pygame.display.flip()
    pygame.time.Clock().tick(60)

    # Guardar tabla Q al finalizar
    guardar_q_table()

    # Guardar estadisticas
    guardar_estadisticas(estadisticas)
#-------------------------------------------------------------------------------Juego Principal