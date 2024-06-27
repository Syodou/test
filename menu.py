import pygame

def menu_screen(screen, background):
    screen.blit(background, [0, 0])  # Dibujar la imagen de fondo
    font = pygame.font.Font(None, 74)
    text = font.render("Menu", True, (255, 255, 255))
    screen.blit(text, (640, 360))
    pygame.display.flip()

def game_screen(screen):
    font = pygame.font.Font(None, 74)
    text = font.render("Game", True, (255, 255, 255))
    screen.blit(text, (640, 360))
    pygame.display.flip()

# Inicializar pygame
pygame.init()

# Configurar la pantalla y el reloj
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

    clock.tick(60)

# Salir de pygame
pygame.quit()
