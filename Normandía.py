import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
ancho_ventana = 1280
alto_ventana = 720
pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Normandía")

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
azul = (0, 0, 255)
rojo = (255, 0, 0)
verde = (0, 255, 0)

# Iniciar el mixer + añadir los diferentes mp3s a usar
pygame.mixer.init()
cancion_juego = "assets/Final Destination.mp3"
cancion_pausa = "assets/pause.mp3"
cancion_menu = "assets/Caribe.mp3"
cancion_derrota = "assets/loser.mp3"
cancion_victoria = "assets/victoria.mp3"

pygame.mixer.music.load(cancion_juego)

# Fuente
font = pygame.font.Font(None, 74)

# Configuración del juego Battleship
n_filas = 15
tam_celdas = 30
margen = 20
tablero_usuario = (margen, alto_ventana // 2 - (n_filas * tam_celdas) // 2)
tablero_cpu = (ancho_ventana - margen - n_filas * tam_celdas, alto_ventana // 2 - (n_filas * tam_celdas) // 2)

# Función para dibujar el botón
def dibujar_botones(pantalla, text, x, y, width, height, color):
    pygame.draw.rect(pantalla, color, [x, y, width, height])
    forma_texto = font.render(text, True, blanco)
    pantalla.blit(forma_texto, (x + (width - forma_texto.get_width()) // 2, y + (height - forma_texto.get_height()) // 2))

# Función para mostrar instrucciones
def mostrar_instrucciones():
    instrucciones_on = True
    while instrucciones_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                instrucciones_on = False

        pantalla.fill(negro)
        forma_texto = font.render("Instrucciones del Juego", True, blanco)
        pantalla.blit(forma_texto, (ancho_ventana // 2 - forma_texto.get_width() // 2, alto_ventana // 2 - 100))

        # Añade más texto de instrucciones aquí
        ins_texto = [
            "Muevete con W, A, S, D",
            "Presiona ENTER para lanzar una bomba",
            "Presiona ESC para pausar el juego"
        ]

        for i, line in enumerate(ins_texto):
            forma_linea = font.render(line, True, blanco)
            pantalla.blit(forma_linea, (ancho_ventana // 2 - forma_linea.get_width() // 2, alto_ventana // 2 + i * 50))

        pygame.display.flip()

# Función para colocar barcos
def pos_barcos():
    barcos = []
    tam_barcos = [(2, 2), (2, 2), (3, 3), (3, 3)]
    
    for tam in tam_barcos:
        posicionado = False
        while not posicionado:
            x = random.randint(0, n_filas - tam[0])
            y = random.randint(0, n_filas - tam[1])
            gen_barco = [(x + dx, y + dy) for dx in range(tam[0]) for dy in range(tam[1])]
            if not any(celda in barcos for barcos in barcos for celda in gen_barco):
                barcos.append(gen_barco)
                posicionado = True

    return barcos

# Función para cargar el contenido del juego principal
def juego():
    # Variables del juego Battleship
    player_x, player_y = 0, 0
    bombas_pj = []
    bombas_cpu = []
    barcos_jugador = pos_barcos()
    barcos_cpu = pos_barcos()

    reloj = pygame.time.Clock()
    actividad_juego = True
    pausa = False

    while actividad_juego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausa = not pausa
                if not pausa:
                    if event.key == pygame.K_w and player_y > 0:
                        player_y -= 1
                    if event.key == pygame.K_s and player_y < n_filas - 1:
                        player_y += 1
                    if event.key == pygame.K_a and player_x > 0:
                        player_x -= 1
                    if event.key == pygame.K_d and player_x < n_filas - 1:
                        player_x += 1
                    if event.key == pygame.K_RETURN:
                        bombas_pj.append((player_x, player_y))
                        cpu_x, cpu_y = random.randint(0, n_filas - 1), random.randint(0, n_filas - 1)
                        bombas_cpu.append((cpu_x, cpu_y))

            elif event.type == pygame.MOUSEBUTTONDOWN and pausa:
                mouse_x, mouse_y = event.pos
                # Verifica si el clic está dentro del botón de regresar al menú principal
                if (ancho_ventana // 2 - 100) <= mouse_x <= (ancho_ventana // 2 + 100) and (alto_ventana // 2 - 50) <= mouse_y <= (alto_ventana // 2 + 50):
                    return

        pantalla.fill(negro)
        if not pausa:
            # Dibujar la cuadrícula del jugador
            for fila in range(n_filas):
                for col in range(n_filas):
                    color = blanco
                    if (col, fila) in bombas_pj:
                        color = rojo if any((col, fila) in ship for ship in barcos_cpu) else azul
                    rect = pygame.Rect(tablero_usuario[0] + col * tam_celdas, tablero_usuario[1] + fila * tam_celdas, tam_celdas, tam_celdas)
                    pygame.draw.rect(pantalla, color, rect, 2)
            
            # Dibujar la cuadrícula de la CPU
            for fila in range(n_filas):
                for col in range(n_filas):
                    color = blanco
                    if (col, fila) in bombas_cpu:
                        color = rojo if any((col, fila) in ship for ship in barcos_jugador) else azul
                    rect = pygame.Rect(tablero_cpu[0] + col * tam_celdas, tablero_cpu[1] + fila * tam_celdas, tam_celdas, tam_celdas)
                    pygame.draw.rect(pantalla, color, rect, 2)

            # Dibujar el jugador
            player_rect = pygame.Rect(tablero_usuario[0] + player_x * tam_celdas, tablero_usuario[1] + player_y * tam_celdas, tam_celdas, tam_celdas)
            pygame.draw.rect(pantalla, verde, player_rect)

            # Dibujar botón de pausa
            dibujar_botones(pantalla, "Pausa", 20, 20, 150, 50, azul)

            pygame.display.flip()
            reloj.tick(60)
        else:
            pantalla.fill(negro)
            dibujar_botones(pantalla, "Regresar al Menu", ancho_ventana // 2 - 100, alto_ventana // 2 - 50, 200, 100, azul)
            pygame.display.flip()

# Bucle principal
act_ventana = True
while act_ventana:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            act_ventana = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Verifica si el clic está dentro de los botones
            if (ancho_ventana // 2 - 100) <= mouse_x <= (ancho_ventana // 2 + 100) and (alto_ventana // 2 - 50) <= mouse_y <= (alto_ventana // 2 + 50):
                # Cargar el contenido del juego principal
                juego()
            elif (ancho_ventana // 2 - 100) <= mouse_x <= (ancho_ventana // 2 + 100) and (alto_ventana // 2 + 60) <= mouse_y <= (alto_ventana // 2 + 160):
                # Mostrar las instrucciones
                mostrar_instrucciones()
            elif (ancho_ventana // 2 - 100) <= mouse_x <= (ancho_ventana // 2 + 100) and (alto_ventana // 2 + 170) <= mouse_y <= (alto_ventana // 2 + 270):
                # Cerrar el juego
                act_ventana = False

    # Rellenar la pantalla de blanco
    pantalla.fill(blanco)
    
    # Dibujar los botones
    dibujar_botones(pantalla, "Jugar", ancho_ventana // 2 - 100, alto_ventana // 2 - 50, 200, 100, azul)
    dibujar_botones(pantalla, "Instrucciones", ancho_ventana // 2 - 100, alto_ventana // 2 + 60, 200, 100, azul)
    dibujar_botones(pantalla, "Salir", ancho_ventana // 2 - 100, alto_ventana // 2 + 170, 200, 100, azul)
    
    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
