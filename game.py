import pygame

def game_screen(screen):
    screen.fill((0, 0, 255))  # Llenar la pantalla de azul para distinguir del menú
    font = pygame.font.Font(None, 74)
    text = font.render("Game", True, (255, 255, 255))
    screen.blit(text, (640, 360))
    pygame.display.flip()

    # Mantener la pantalla del juego hasta que se cierre
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
