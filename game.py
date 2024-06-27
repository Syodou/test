import pygame
import sys

def menu_screen(screen, background):
    screen.blit(background, [0, 0])  # Dibujar la imagen de fondo
    font = pygame.font.Font(None, 74)
    text = font.render("Menu", True, (255, 255, 255))
    screen.blit(text, (640, 360))
    pygame.display.flip()

def game_screen(screen):
    blanco = (255, 255, 255)
    negro = (0, 0, 0)
    azul = (0, 0, 255)
    gris = (200, 200, 200)
    ancho_ventana = 1280
    alto_ventana = 720
    tam_celda = 30
    num_filas = 15
    num_columnas = 15

    def crear_tablero(superficie, color_celda):
        for fila in range(num_filas):
            for columna in range(num_columnas):
                rect = pygame.Rect(columna * tam_celda, fila * tam_celda, tam_celda, tam_celda)
                pygame.draw.rect(superficie, color_celda, rect, 1)  # Dibujar con borde de 1 píxel

    tablero1 = pygame.Surface((num_columnas * tam_celda, num_filas * tam_celda))
    tablero1.fill(blanco)
    crear_tablero(tablero1, negro)

    tablero2 = pygame.Surface((num_columnas * tam_celda, num_filas * tam_celda))
    tablero2.fill(gris)
    crear_tablero(tablero2, negro)

    tablero1_rect = tablero1.get_rect(center=(ancho_ventana // 4, alto_ventana // 2))
    tablero2_rect = tablero2.get_rect(center=(3 * ancho_ventana // 4, alto_ventana // 2))

    boton_pausa = pygame.Rect(ancho_ventana - 110, 10, 100, 50)
    fuente = pygame.font.SysFont(None, 40)

    pausado = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_pausa.collidepoint(event.pos):
                    pausado = not pausado

        screen.fill(blanco)
        screen.blit(tablero1, tablero1_rect.topleft)
        screen.blit(tablero2, tablero2_rect.topleft)

        pygame.draw.rect(screen, azul, boton_pausa)
        texto_pausa = fuente.render("Pause" if not pausado else "Resume", True, blanco)
        screen.blit(texto_pausa, (boton_pausa.x + 10, boton_pausa.y + 10))

        if pausado:
            overlay = pygame.Surface((ancho_ventana, alto_ventana))
            overlay.set_alpha(128)  # Valor de transparencia (0-255)
            overlay.fill(negro)
            screen.blit(overlay, (0, 0))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode([1280, 720])
pygame.display.set_caption("Normandía")
clock = pygame.time.Clock()

# Cargar la imagen de fondo desde la carpeta "assets"
background = pygame.image.load("assets/background.jpg").convert()

# Inicializar el mixer de pygame y cargar la música de fondo
pygame.mixer.init()
pygame.mixer.music.load("assets/menu.mp3")

# Establecer el volumen (valor entre 0.0 y 1.0)
volume = 0.5
pygame.mixer.music.set_volume(volume)

# Reproducir en loop
pygame.mixer.music.play(-1)

# Estado inicial del programa
on_menu = True

# Bucle principal del programa
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and on_menu:
            on_menu = False
            pygame.mixer.music.stop()  # Detener la música al cambiar al juego

    if on_menu:
        menu_screen(screen, background)
    else:
        game_screen(screen)
        done = True  # Salir del bucle principal después de cambiar al juego

    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()
