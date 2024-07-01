import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
ancho_ventana = 1280
largo_ventana = 720
ventana = pygame.display.set_mode((ancho_ventana, largo_ventana))
pygame.display.set_caption("Normandía")

# Cargar fondos e imágenes desde la carpeta "assets"
menu_BG = pygame.image.load('assets/background.jpg')
juego_BG = pygame.image.load('assets/background.jpg')
instrucciones_BG = pygame.image.load('assets/background.jpg')
victoria_BG = pygame.image.load('assets/background.jpg')
derrota_BG = pygame.image.load('assets/background.jpg')

# Cargar música desde la carpeta "assets" y configurar volumen
pygame.mixer.music.load('assets/Caribe.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Reproducir en bucle

musica_pausa = 'assets/pause.mp3'
musica_juego = 'assets/Final Destination.mp3'

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
azul = (0, 0, 255)
rojo = (255, 0, 0)
verde = (0, 255, 0)

# Fuente
fuente = pygame.font.Font(None, 45)

# Configuración del juego Battleship
tamaño_tablero = 15
tamaño_celda = 30
distancia = 150 #Esta inverso XD (Entre mas distancia, mas cerca los tableros) // Eso debido a que estoy calculando el origen del tablero con el margen de la ventana
origen_tableroCPU = (distancia, largo_ventana // 2 - (tamaño_tablero * tamaño_celda) // 2)
Origen_tableroUsuario = (ancho_ventana - distancia - tamaño_tablero * tamaño_celda, largo_ventana // 2 - (tamaño_tablero * tamaño_celda) // 2)

# Función para dibujar el botón
def Dibujar_boton(ventana, texto, x, y, ancho, largo, color):
    pygame.draw.rect(ventana, color, [x, y, ancho, largo])
    superficie_texto = fuente.render(texto, True, blanco)
    ventana.blit(superficie_texto, (x + (ancho - superficie_texto.get_width()) // 2, y + (largo - superficie_texto.get_height()) // 2))

# Función para mostrar texto en la pantalla
def mostrar_texto(texto, fuente, color, superficie, x, y):
    texto_objeto = fuente.render(texto, True, color)
    texto_rect = texto_objeto.get_rect()
    texto_rect.center = (x, y)
    superficie.blit(texto_objeto, texto_rect)

# Función para la pantalla de menú principal
def menu_principal():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if boton_instrucciones.collidepoint(x, y):
                        instrucciones()
                    if boton_opciones.collidepoint(x, y):
                        opciones()
                    if boton_salir.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()

        ventana.fill(blanco)
        ventana.blit(menu_BG, (0, 0))
        
        # Botones
        boton_jugar = pygame.Rect(540, 250, 200, 50)
        boton_instrucciones = pygame.Rect(540, 350, 200, 50)
        boton_opciones = pygame.Rect(540, 450, 200, 50)
        boton_salir = pygame.Rect(540, 550, 200, 50)
        
        pygame.draw.rect(ventana, negro, boton_jugar)
        pygame.draw.rect(ventana, negro, boton_instrucciones)
        pygame.draw.rect(ventana, negro, boton_opciones)
        pygame.draw.rect(ventana, negro, boton_salir)
        
        mostrar_texto("Jugar", fuente, blanco, ventana, 640, 275)
        mostrar_texto("Instrucciones", fuente, blanco, ventana, 640, 375)
        mostrar_texto("Opciones", fuente, blanco, ventana, 640, 475)
        mostrar_texto("Salir", fuente, blanco, ventana, 640, 575)

        pygame.display.update()

# Función para la pantalla de instrucciones
def instrucciones():
    instrucciones_on = True #Si es que la ventana de instrucciones está activa
    while instrucciones_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                instrucciones_on = False

        ventana.blit(instrucciones_BG, (0, 0))
        formato_texto = fuente.render("Instrucciones del Juego", True, blanco)
        ventana.blit(formato_texto, (ancho_ventana // 2 - formato_texto.get_width() // 2, largo_ventana // 2 - 100))

        # Añade más texto de instrucciones aquí
        texto_instrucciones = [
            "Muevete con W, A, S, D",
            "Presiona ENTER para lanzar una bomba",
            "Presiona ESC para pausar el juego"
        ]

        for i, line in enumerate(texto_instrucciones):
            line_surface = fuente.render(line, True, blanco)
            ventana.blit(line_surface, (ancho_ventana // 2 - line_surface.get_width() // 2, largo_ventana // 2 + i * 50))
            
        pygame.display.update()

# Función para la pantalla de opciones
def opciones():
    volumen_musica = 0.5  # Volumen predeterminado para música
    volumen_efectos = 0.5  # Volumen predeterminado para efectos de sonido

    boton_mas_musica = pygame.Rect(740, 360, 50, 50)
    boton_menos_musica = pygame.Rect(490, 360, 50, 50)
    boton_mas_efectos = pygame.Rect(740, 460, 50, 50)
    boton_menos_efectos = pygame.Rect(490, 460, 50, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if boton_mas_musica.collidepoint(x, y):
                        if volumen_musica < 1.0:
                            volumen_musica += 0.1
                            pygame.mixer.music.set_volume(volumen_musica)
                    if boton_menos_musica.collidepoint(x, y):
                        if volumen_musica > 0.0:
                            volumen_musica -= 0.1
                            pygame.mixer.music.set_volume(volumen_musica)
                    if boton_mas_efectos.collidepoint(x, y):
                        if volumen_efectos < 1.0:
                            volumen_efectos += 0.1
                            # Ajustar el volumen de los efectos de sonido aquí
                    if boton_menos_efectos.collidepoint(x, y):
                        if volumen_efectos > 0.0:
                            volumen_efectos -= 0.1
                            # Ajustar el volumen de los efectos de sonido aquí

        ventana.fill(blanco)
        ventana.blit(menu_BG, (0, 0))

        # Botones para volumen de música
        pygame.draw.rect(ventana, negro, boton_mas_musica)
        pygame.draw.rect(ventana, negro, boton_menos_musica)
        mostrar_texto("+", fuente, blanco, ventana, 765, 385)
        mostrar_texto("-", fuente, blanco, ventana, 515, 385)
        mostrar_texto(f"Volumen Música: {volumen_musica:.1f}", fuente, negro, ventana, 640, 300)

        # Botones para volumen de efectos de sonido
        pygame.draw.rect(ventana, negro, boton_mas_efectos)
        pygame.draw.rect(ventana, negro, boton_menos_efectos)
        mostrar_texto("+", fuente, blanco, ventana, 765, 485)
        mostrar_texto("-", fuente, blanco, ventana, 515, 485)
        mostrar_texto(f"Volumen Efectos: {volumen_efectos:.1f}", fuente, negro, ventana, 640, 420)

        pygame.display.update()


# Función para colocar barcos
def colocar_barcos():
    barcos = []
    tamaño_barcos = [(2,1), (2,1), (1,2), (1,2), (3,1), (1,3), (1,3), (3,1), (3,1), (1,4), (1,4), (4,1)]
    
    for tamaño in tamaño_barcos:
        posicionado = False
        while not posicionado:
            x = random.randint(0, tamaño_tablero - tamaño[0])
            y = random.randint(0, tamaño_tablero - tamaño[1])
            gen_barco = [(x + dx, y + dy) for dx in range(tamaño[0]) for dy in range(tamaño[1])]
            if not any(cell in ship for ship in barcos for cell in gen_barco):
                barcos.append(gen_barco)
                posicionado = True

    return barcos

# Función para verificar si todos los barcos han sido eliminados
def todoslosbarcosderribados(bombas, barcos):
    return all(celda in bombas for barco in barcos for celda in barco)

# Función para mostrar la pantalla de victoria o derrota
def mostrar_endscreen(victoria):
    pygame.mixer.music.load(musica_juego)
    pygame.mixer.music.set_volume(0.5) # Volumen de la musica
    pygame.mixer.music.play(-1)  # Reproducir en bucle

    pantalla_final = True
    while pantalla_final:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (ancho_ventana - 200) <= mouse_x <= (ancho_ventana - 50) and (largo_ventana - 100) <= mouse_y <= (largo_ventana - 50):
                    return

        ventana.blit(victoria_BG if victoria else derrota_BG, (0, 0))
        formato_texto = fuente.render("Victoria" if victoria else "Derrota", True, blanco)
        ventana.blit(formato_texto, (ancho_ventana // 2 - formato_texto.get_width() // 2, largo_ventana // 2 - 100))

        Dibujar_boton(ventana, "Regresar al Menu", ancho_ventana - 200, largo_ventana - 100, 150, 50, azul)
        
        pygame.display.flip()

# Función para cargar el contenido del juego principal
def iniciar_juego():
    pygame.mixer.music.load(musica_juego)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Reproducir en bucle

    # Variables del juego Battleship
    player_x, player_y = 0, 0
    player_bombs = []
    cpu_bombs = []
    barcos_usuario = colocar_barcos()
    barcos_cpu = colocar_barcos()

    reloj = pygame.time.Clock()
    ejecute_juego = True
    pausado = False
    posicion_musica = 0 #Dependencia para que al pausar el juego, el programa recuerde donde quedo pausada la cancion del juego

    while ejecute_juego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausado = not pausado
                    if pausado:
                        posicion_musica = pygame.mixer.music.get_pos() / 1000.0
                        pygame.mixer.music.load(musica_pausa)
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.load(musica_juego)
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1, start=posicion_musica)
                if not pausado:
                    if event.key == pygame.K_w and player_y > 0:
                        player_y -= 1
                    if event.key == pygame.K_s and player_y < tamaño_tablero - 1:
                        player_y += 1
                    if event.key == pygame.K_a and player_x > 0:
                        player_x -= 1
                    if event.key == pygame.K_d and player_x < tamaño_tablero - 1:
                        player_x += 1
                    if event.key == pygame.K_RETURN:
                        if (player_x, player_y) not in player_bombs:
                            player_bombs.append((player_x, player_y))
                            if todoslosbarcosderribados(player_bombs, barcos_cpu):
                                mostrar_endscreen(True)
                                return
                            while True:
                                cpu_x, cpu_y = random.randint(0, tamaño_tablero - 1), random.randint(0, tamaño_tablero - 1)
                                if (cpu_x, cpu_y) not in cpu_bombs:
                                    cpu_bombs.append((cpu_x, cpu_y))
                                    break
                            if todoslosbarcosderribados(cpu_bombs, barcos_usuario):
                                mostrar_endscreen(False)
                                return

            elif event.type == pygame.MOUSEBUTTONDOWN and pausado:
                mouse_x, mouse_y = event.pos
                # Verifica si el clic está dentro de los botones del menú de pausa
                if (ancho_ventana // 2 - 100) <= mouse_x <= (ancho_ventana // 2 + 100) and (largo_ventana // 2 - 50) <= mouse_y <= (largo_ventana // 2 + 50):
                    pausado = False
                    pygame.mixer.music.load(musica_juego)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1, start=posicion_musica)
                elif (ancho_ventana // 2 - 100) <= mouse_x <= (ancho_ventana // 2 + 100) and (largo_ventana // 2 + 60) <= mouse_y <= (largo_ventana // 2 + 110):
                    return

        ventana.blit(juego_BG, (0, 0))
        if not pausado:
            # Dibujar la cuadrícula de la CPU
            for fila in range(tamaño_tablero):
                for columna in range(tamaño_tablero):
                    color = blanco
                    if (columna, fila) in player_bombs:
                        color = rojo if any((columna, fila) in barco for barco in barcos_cpu) else azul
                    cpu_tablero = pygame.Rect(origen_tableroCPU[0] + columna * tamaño_celda, origen_tableroCPU[1] + fila * tamaño_celda, tamaño_celda, tamaño_celda)
                    pygame.draw.rect(ventana, color, cpu_tablero, 2)

            # Dibujar la cuadrícula del jugador
            for fila in range(tamaño_tablero):
                for columna in range(tamaño_tablero):
                    color = blanco
                    if (columna, fila) in cpu_bombs:
                        color = rojo if any((columna, fila) in barco for barco in barcos_usuario) else azul
                    elif any((columna, fila) in ship for ship in barcos_usuario):
                        color = verde
                    cpu_tablero = pygame.Rect(Origen_tableroUsuario[0] + columna * tamaño_celda, Origen_tableroUsuario[1] + fila * tamaño_celda, tamaño_celda, tamaño_celda)
                    pygame.draw.rect(ventana, color, cpu_tablero, 2)

            # Dibujar la selección del jugador en el tablero de la CPU
            tablero_usuario = pygame.Rect(origen_tableroCPU[0] + player_x * tamaño_celda, origen_tableroCPU[1] + player_y * tamaño_celda, tamaño_celda, tamaño_celda)
            pygame.draw.rect(ventana, verde, tablero_usuario)

            # Dibujar botón de pausa
            Dibujar_boton(ventana, "Pausa", 20, 20, 150, 50, azul)

            pygame.display.flip()
            reloj.tick(60)
        else:
            # Crear una superficie semi-transparente
            overlay = pygame.Surface((ancho_ventana, largo_ventana))
            overlay.set_alpha(128)  # 50% de transparencia
            overlay.fill(negro)
            ventana.blit(overlay, (0, 0))

            Dibujar_boton(ventana, "Continuar", ancho_ventana // 2 - 100, largo_ventana // 2 - 50, 200, 50, azul)
            Dibujar_boton(ventana, "Regresar al Menu", ancho_ventana // 2 - 100, largo_ventana // 2 + 60, 200, 50, azul)
            pygame.display.flip()

# Bucle principal
ejecute = True
while ejecute:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecute = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = evento.pos
            # Verifica si el clic está dentro de los botones
            if (ancho_ventana // 2 - 100) <= mouse_x <= (ancho_ventana // 2 + 100) and (largo_ventana // 3.2 - 25) <= mouse_y <= (largo_ventana // 2 + 50):
                # Cargar el contenido del juego principal
                iniciar_juego()
            elif (ancho_ventana // 2 - 100) <= mouse_x <= (ancho_ventana // 2 + 100) and (largo_ventana // 2 + 60) <= mouse_y <= (largo_ventana // 2 + 160):
                # Mostrar las instrucciones
                instrucciones()
            elif (ancho_ventana // 2 - 100) <= mouse_x <= (ancho_ventana // 2 + 100) and (largo_ventana // 2 - 50) <= mouse_y <= (largo_ventana // 2 + 50):
                # Mostrar Opciones
                opciones()
            elif (ancho_ventana // 2 - 100) <= mouse_x <= (ancho_ventana // 2 + 100) and (largo_ventana // 2 + 170) <= mouse_y <= (largo_ventana // 2 + 270):
                # Cerrar el juego
                ejecute = False

    # Rellenar la pantalla de blanco
    ventana.blit(menu_BG, (0, 0))
    
    # Dibujar los botones
    
    Dibujar_boton(ventana, "Jugar", ancho_ventana // 2 - 100, largo_ventana // 3.2 - 25, 200, 100, azul)
    Dibujar_boton(ventana, "Opciones", ancho_ventana // 2 - 100, largo_ventana // 2 - 50, 200, 100, azul)
    Dibujar_boton(ventana, "Instrucciones", ancho_ventana // 2 - 100, largo_ventana // 2 + 60, 200, 100, azul)
    Dibujar_boton(ventana, "Salir", ancho_ventana // 2 - 100, largo_ventana // 2 + 170, 200, 100, azul)
    
    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
