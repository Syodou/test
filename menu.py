import pygame

def menu_screen(screen):
    screen.fill((0, 0, 0))  # Llenar la pantalla de negro
    font = pygame.font.Font(None, 74)
    text = font.render("Menu", True, (255, 255, 255))
    screen.blit(text, (640, 360))
    pygame.display.flip()
