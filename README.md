# Proyecto: Aplicación de Q-Learning en la Creación de un Agente Inteligente para el Juego de Damas

## Descripción

Este proyecto implementa un agente autónomo para jugar al juego de **Damas** utilizando **Q-Learning**. El juego es una versión simplificada de las damas en un tablero de 4x4. El agente utiliza aprendizaje por refuerzo para aprender a jugar, enfrentándose a un jugador humano. Además, se guarda una tabla Q para almacenar las decisiones aprendidas y se lleva un registro de las estadísticas de las partidas jugadas.

## Funcionalidades

- **Interfaz Gráfica con Pygame**: 
  - El tablero es visualizado usando la librería Pygame.
  - El jugador humano puede hacer clic sobre las piezas para moverlas.
  - El agente (IA) mueve automáticamente siguiendo las decisiones aprendidas.

- **Sistema de Aprendizaje por Refuerzo (Q-Learning)**: 
  - El agente aprende a través de interacciones con el entorno, utilizando la tabla Q.
  - Se implementa el algoritmo de **epsilon-greedy** para equilibrar exploración y explotación de las acciones.

- **Estadísticas**:
  - Se lleva un registro de las victorias del humano y de la IA.
  - El número total de partidas jugadas también se guarda.
  - Las estadísticas se guardan y cargan de un archivo JSON.

## Requisitos

- Python 3.x
- Pygame (`pip install pygame`)
- Matplotlib (`pip install matplotlib`)


## Ejecutar el juego
1.  Una vez que tengas los archivos en tu computadora, navega al directorio del proyecto usando la terminal o el explorador de archivos.
2. Ejecuta el archivo juego_damas.py con el siguiente comando en la terminal:
     ``
    python juegodamas.py
    ``
3. El juego se abrirá en una ventana de Pygame. El jugador humano controla las piezas blancas, mientras que la IA controla las piezas negras.


## Instrucciones de Uso

1. **Configuración**: 
   - Asegúrate de tener las librerías `pygame` y `matplotlib` instaladas.

2. **Ejecución**: 
   - Ejecuta el script en un entorno de Python con acceso a las librerías mencionadas.

3. **Juego**:
   - El juego comienza con un tablero de 4x4 con dos piezas de cada color en posiciones iniciales predeterminadas.
   - El jugador humano toma el turno primero (las piezas blancas).
   - En cada turno, el jugador puede seleccionar una de sus piezas y moverla.
   - La IA jugará después del turno del jugador humano y tomará decisiones basadas en lo que ha aprendido mediante Q-Learning.

4. **Finalización del Juego**:
   - El juego termina cuando un jugador captura todas las piezas del adversario o cuando no hay movimientos válidos restantes.
   - La IA y el humano tienen diferentes recompensas y penalizaciones para reflejar las victorias o derrotas.

5. **Estadísticas**:
   - Las estadísticas de victorias de la IA y el humano se almacenan en un archivo `stats.json`.
   - La tabla Q se guarda en un archivo `q_table.pkl` para que el agente pueda continuar aprendiendo a través de múltiples ejecuciones del juego.
