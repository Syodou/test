import pygame
import sys
from menu import menu_screen
from game import game_screen  # Asumiendo que el archivo de juego se llama game.py y tiene una función game_screen

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Menu")

    # Mostrar la pantalla del menú
    menu_screen(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Cuando se hace clic en cualquier parte de la pantalla, cambia a la pantalla del juego
                game_screen(screen)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
