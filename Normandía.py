import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Normandía")

# Cargar fondos e imágenes desde la carpeta "assets"
menu_background = pygame.image.load('assets/background.jpg')
game_background = pygame.image.load('assets/background.jpg')
instructions_background = pygame.image.load('assets/background.jpg')
victory_background = pygame.image.load('assets/background.jpg')
defeat_background = pygame.image.load('assets/background.jpg')

# Cargar música desde la carpeta "assets"
pygame.mixer.music.load('assets/Caribe.mp3')
pygame.mixer.music.play(-1)  # Reproducir en bucle
pause_music = 'assets/pause.mp3'
game_music = 'assets/Final Destination.mp3'

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Fuente
font = pygame.font.Font(None, 74)

# Configuración del juego Battleship
grid_size = 15
cell_size = 30
margin = 20
cpu_grid_origin = (margin, screen_height // 2 - (grid_size * cell_size) // 2)
user_grid_origin = (screen_width - margin - grid_size * cell_size, screen_height // 2 - (grid_size * cell_size) // 2)

# Función para dibujar el botón
def draw_button(screen, text, x, y, width, height, color):
    pygame.draw.rect(screen, color, [x, y, width, height])
    text_surface = font.render(text, True, white)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

# Función para mostrar instrucciones
def show_instructions():
    instructions_running = True
    while instructions_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                instructions_running = False

        screen.blit(instructions_background, (0, 0))
        text_surface = font.render("Instrucciones del Juego", True, white)
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, screen_height // 2 - 100))

        # Añade más texto de instrucciones aquí
        instructions_text = [
            "Muevete con W, A, S, D",
            "Presiona ENTER para lanzar una bomba",
            "Presiona ESC para pausar el juego"
        ]

        for i, line in enumerate(instructions_text):
            line_surface = font.render(line, True, white)
            screen.blit(line_surface, (screen_width // 2 - line_surface.get_width() // 2, screen_height // 2 + i * 50))

        pygame.display.flip()

# Función para colocar barcos
def place_ships():
    ships = []
    ship_sizes = [(2, 1), (2, 1), (3, 1), (3, 1)]
    
    for size in ship_sizes:
        placed = False
        while not placed:
            x = random.randint(0, grid_size - size[0])
            y = random.randint(0, grid_size - size[1])
            new_ship = [(x + dx, y + dy) for dx in range(size[0]) for dy in range(size[1])]
            if not any(cell in ship for ship in ships for cell in new_ship):
                ships.append(new_ship)
                placed = True

    return ships

# Función para verificar si todos los barcos han sido eliminados
def all_ships_sunk(bombs, ships):
    return all(cell in bombs for ship in ships for cell in ship)

# Función para mostrar la pantalla de victoria o derrota
def show_end_screen(win):
    pygame.mixer.music.load('assets/Final Destinarion.mp3')
    pygame.mixer.music.play(-1)  # Reproducir en bucle

    end_running = True
    while end_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (screen_width - 200) <= mouse_x <= (screen_width - 50) and (screen_height - 100) <= mouse_y <= (screen_height - 50):
                    return

        screen.blit(victory_background if win else defeat_background, (0, 0))
        text_surface = font.render("Victoria" if win else "Derrota", True, white)
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, screen_height // 2 - 100))

        draw_button(screen, "Regresar al Menu", screen_width - 200, screen_height - 100, 150, 50, blue)
        
        pygame.display.flip()

# Función para cargar el contenido del juego principal
def run_game():
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1)  # Reproducir en bucle

    # Variables del juego Battleship
    player_x, player_y = 0, 0
    player_bombs = []
    cpu_bombs = []
    player_ships = place_ships()
    cpu_ships = place_ships()

    clock = pygame.time.Clock()
    running = True
    paused = False
    game_music_pos = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        game_music_pos = pygame.mixer.music.get_pos() / 1000.0
                        pygame.mixer.music.load(pause_music)
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.load(game_music)
                        pygame.mixer.music.play(-1, start=game_music_pos)
                if not paused:
                    if event.key == pygame.K_w and player_y > 0:
                        player_y -= 1
                    if event.key == pygame.K_s and player_y < grid_size - 1:
                        player_y += 1
                    if event.key == pygame.K_a and player_x > 0:
                        player_x -= 1
                    if event.key == pygame.K_d and player_x < grid_size - 1:
                        player_x += 1
                    if event.key == pygame.K_RETURN:
                        if (player_x, player_y) not in player_bombs:
                            player_bombs.append((player_x, player_y))
                            if all_ships_sunk(player_bombs, cpu_ships):
                                show_end_screen(True)
                                return
                            while True:
                                cpu_x, cpu_y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
                                if (cpu_x, cpu_y) not in cpu_bombs:
                                    cpu_bombs.append((cpu_x, cpu_y))
                                    break
                            if all_ships_sunk(cpu_bombs, player_ships):
                                show_end_screen(False)
                                return

            elif event.type == pygame.MOUSEBUTTONDOWN and paused:
                mouse_x, mouse_y = event.pos
                # Verifica si el clic está dentro de los botones del menú de pausa
                if (screen_width // 2 - 100) <= mouse_x <= (screen_width // 2 + 100) and (screen_height // 2 - 50) <= mouse_y <= (screen_height // 2 + 50):
                    paused = False
                    pygame.mixer.music.load(game_music)
                    pygame.mixer.music.play(-1, start=game_music_pos)
                elif (screen_width // 2 - 100) <= mouse_x <= (screen_width // 2 + 100) and (screen_height // 2 + 60) <= mouse_y <= (screen_height // 2 + 110):
                    return

        screen.blit(game_background, (0, 0))
        if not paused:
            # Dibujar la cuadrícula de la CPU
            for row in range(grid_size):
                for col in range(grid_size):
                    color = white
                    if (col, row) in player_bombs:
                        color = red if any((col, row) in ship for ship in cpu_ships) else blue
                    rect = pygame.Rect(cpu_grid_origin[0] + col * cell_size, cpu_grid_origin[1] + row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, color, rect, 2)

            # Dibujar la cuadrícula del jugador
            for row in range(grid_size):
                for col in range(grid_size):
                    color = white
                    if (col, row) in cpu_bombs:
                        color = red if any((col, row) in ship for ship in player_ships) else blue
                    elif any((col, row) in ship for ship in player_ships):
                        color = green
                    rect = pygame.Rect(user_grid_origin[0] + col * cell_size, user_grid_origin[1] + row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, color, rect, 2)

            # Dibujar la selección del jugador
            player_rect = pygame.Rect(user_grid_origin[0] + player_x * cell_size, user_grid_origin[1] + player_y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, green, player_rect)

            # Dibujar botón de pausa
            draw_button(screen, "Pausa", 20, 20, 150, 50, blue)

            pygame.display.flip()
            clock.tick(60)
        else:
            # Crear una superficie semi-transparente
            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(128)  # 50% de transparencia
            overlay.fill(black)
            screen.blit(overlay, (0, 0))

            draw_button(screen, "Continuar", screen_width // 2 - 100, screen_height // 2 - 50, 200, 50, blue)
            draw_button(screen, "Regresar al Menu", screen_width // 2 - 100, screen_height // 2 + 60, 200, 50, blue)
            pygame.display.flip()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Verifica si el clic está dentro de los botones
            if (screen_width // 2 - 100) <= mouse_x <= (screen_width // 2 + 100) and (screen_height // 2 - 50) <= mouse_y <= (screen_height // 2 + 50):
                # Cargar el contenido del juego principal
                run_game()
                pygame.mixer.music.load('assets/Caribe.mp3')
                pygame.mixer.music.play(-1)  # Reproducir en bucle
            elif (screen_width // 2 - 100) <= mouse_x <= (screen_width // 2 + 100) and (screen_height // 2 + 60) <= mouse_y <= (screen_height // 2 + 160):
                # Mostrar las instrucciones
                show_instructions()
            elif (screen_width // 2 - 100) <= mouse_x <= (screen_width // 2 + 100) and (screen_height // 2 + 170) <= mouse_y <= (screen_height // 2 + 270):
                # Cerrar el juego
                running = False

    # Rellenar la pantalla de blanco
    screen.blit(menu_background, (0, 0))
    
    # Dibujar los botones
    draw_button(screen, "Jugar", screen_width // 2 - 100, screen_height // 2 - 50, 200, 100, blue)
    draw_button(screen, "Instrucciones", screen_width // 2 - 100, screen_height // 2 + 60, 200, 100, blue)
    draw_button(screen, "Salir", screen_width // 2 - 100, screen_height // 2 + 170, 200, 100, blue)
    
    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()

