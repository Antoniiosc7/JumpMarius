import pygame
import sys
def musica():
    pygame.mixer.Sound('recursos/sfx/music.wav')
    pygame.mixer.music.set_volume(0.1)
    
import pygame
import sys

def musica():
    pygame.mixer.Sound('recursos/sfx/music.wav')
    pygame.mixer.music.set_volume(0.1)

def main_menu(screen):
    options = ["Comenzar nueva partida", "Seleccion de nivel", "Seleccion de personaje", "Configuracion", "Salir"]
    selected_option = 0

    background = pygame.image.load("recursos/Clouds7.png").convert()
    background = pygame.transform.scale(background, (800, 600))

    while True:
        screen.blit(background, (0, 0))
        musica()

        draw_text(screen, "Bienvenido a Jump Marius", 36, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)
        draw_text(screen, "By Antoniiosc7", 28, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 3.1)

        for i, option in enumerate(options):
            size = 24
            color = (0, 0, 0)
            if i == selected_option:
                size = 28
                color = (255, 0, 0)
            draw_text(screen, option, size, color, screen.get_width() // 2, screen.get_height() // 2 + i * 40)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]:
                    option = options[selected_option]
                    if option == "Comenzar nueva partida":
                        return 'restart'
                    elif option == "Seleccion de nivel":
                        pass
                    elif option == "Seleccion de personaje":
                        pass
                    elif option == "Configuracion":
                        pass
                    elif option == "Salir":
                        pygame.quit()
                        sys.exit()

def draw_text(screen, text, size, color, x, y, padding_x=10, padding_y=5, death_count=None):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))

    # Ajustar el tamaño del rectángulo con un margen alrededor del texto
    rect_width = text_rect.width + 2 * padding_x
    rect_height = text_rect.height + 2 * padding_y

    # Crear un rectángulo con transparencia
    rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    pygame.draw.rect(rect_surface, (255, 255, 255, 128), rect_surface.get_rect(), border_radius=5)

    # Superponer el rectángulo sobre la pantalla
    screen.blit(rect_surface, (text_rect.topleft[0] - padding_x, text_rect.topleft[1] - padding_y))
    screen.blit(text_surface, text_rect.topleft)

    # Mostrar el contador de muertes si se proporciona
    if death_count is not None:
        death_text = f'Muertes: {death_count}'
        death_font = pygame.font.Font(None, 24)
        death_surface = death_font.render(death_text, True, color)
        death_rect = death_surface.get_rect(center=(x, y + text_rect.height + padding_y))
        screen.blit(death_surface, death_rect.topleft)

def restart_menu(screen, game):
    options = {
        pygame.K_r: "restart",
        pygame.K_m: "main_menu",
        pygame.K_q: "quit"
    }
    selected_option = None
    musica()
    background = pygame.image.load("recursos/Clouds7.png").convert()
    background = pygame.transform.scale(background, (800, 600))

    while True:
        screen.blit(background, (0, 0))  # Dibujar la imagen de fondo
        draw_text(screen, "HAS PAUSADO LA PARTIDA", 36, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)
        draw_text(screen, "Presiona R para reiniciar", 24, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 2)
        draw_text(screen, "Presiona M para volver al menú principal", 24, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 3)
        draw_text(screen, "Presiona Q para salir", 24, (0, 0, 0), screen.get_width() // 2, screen.get_height() * 3 // 4, death_count=game.death_count)


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                option = options.get(event.key)
                if option is not None:
                    selected_option = option

        if selected_option is not None:
            if selected_option == "restart":
                game.reset_game()
                return 'restart'
            elif selected_option == "main_menu":
                return "main_menu"
            elif selected_option == "quit":
                pygame.quit()
                sys.exit()
            elif selected_option == "continue":
                return True
            else:
                selected_option = None
                
def game_over_menu(screen, game):
    options = {
        pygame.K_r: "restart",
        pygame.K_m: "main_menu",
        pygame.K_q: "quit"
    }
    
    while True:
        screen.fill((255, 255, 255))
        musica()
        # Menú de Game Over
        draw_text(screen, "¡Has perdido!", 36, (255, 0, 0), screen.get_width() // 2, screen.get_height() // 4)
        draw_text(screen, "Presiona R para reiniciar", 24, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 2)
        draw_text(screen, "Presiona M para volver al menú principal", 24, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 3)
        draw_text(screen, "Presiona Q para salir", 24, (0, 0, 0), screen.get_width() // 2, screen.get_height() * 3 // 4, death_count=game.death_count)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                option = options.get(event.key)
                if option is not None:
                    if option == "restart":
                        game.reset_game()
                        return "restart"
                    elif option == "main_menu":
                        return "main_menu"
                    elif option == "quit":
                        pygame.quit()
                        sys.exit()
        
        # Agrega un pequeño descanso para evitar procesar múltiples eventos por un solo toque de tecla
        pygame.time.delay(100)

