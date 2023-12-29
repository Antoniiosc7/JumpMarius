import pygame
import sys
import pandas as pd


def save_resolution_to_csv(resolution):
    resolution_df = pd.DataFrame([resolution], columns=['Width', 'Height'])
    resolution_df.to_csv('config.csv', index=False)


def load_resolution_from_csv():
    try:
        resolution_df = pd.read_csv('config.csv')
        resolution = (resolution_df['Width'].iloc[0], resolution_df['Height'].iloc[0])
        print("Resolution loaded:", resolution)
        return resolution
    except (FileNotFoundError, pd.errors.EmptyDataError, IndexError, ValueError):
        return None
    
def load_and_scale_background(game):
    # Obtener la resolución del archivo CSV
    resolution = load_resolution_from_csv()

    # Cargar y escalar la imagen de fondo
    background = pygame.image.load("recursos/Clouds7.png").convert()

    if resolution:
        background = pygame.transform.scale(background, resolution)

    return background

def main_menu(screen, game):
    options = ["Comenzar nueva partida", "Seleccion de nivel", "Seleccion de personaje", "Configuracion", "Salir"]
    selected_option = 0
    background = load_and_scale_background(game)
    while True:
        
        
        screen.blit(background, (0, 0))


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
                        config_menu_result, new_resolution = config_menu(screen, game)
                        if config_menu_result == "main_menu":
                            if new_resolution:
                                game.change_resolution(new_resolution)
                                save_resolution_to_csv(new_resolution)
                                load_and_scale_background(game)  # Actualizar la imagen de fondo
                            return "main_menu"
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
    options = ["Continuar partida", "Reiniciar partida", "Menu Principal", "Salir"]
    selected_option = 0

    background = load_and_scale_background(game)
    screen.blit(background, (0, 0))


    while True:
        
        draw_text(screen, "Has pausado la partida", 36, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)
        draw_text(screen, "¿Que deseas hacer?", 28, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 3.1)

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
                    if option == "Continuar partida":
                        return 'continue'
                    elif option == "Reiniciar partida":
                        game.reset_game()
                        return 'restart'
                    elif option == "Menu Principal":
                        return main_menu(screen, game)
                    elif option == "Salir":
                        pygame.quit()
                        sys.exit()
                
def game_over_menu(screen, game):
    options = {
        pygame.K_r: "restart",
        pygame.K_m: "main_menu",
        pygame.K_q: "quit"
    }
    
    while True:
        screen.fill((255, 255, 255))
  
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

def config_menu(screen, game):
    options = ["320 x 240", "640 x 480", "1280 x 960", "Volver al menú principal"]
    selected_option = 0

    while True:
        screen.fill((255, 255, 255))

        draw_text2(screen, "Configuración", 36, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)

        for i, option in enumerate(options):
            size = 24
            color = (0, 0, 0)
            if i == selected_option:
                size = 28
                color = (255, 0, 0)
            draw_text2(screen, option, size, color, screen.get_width() // 2, screen.get_height() // 2 + i * 40)

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
                    if option == "320 x 240":
                        game.current_resolution = (320, 240)
                    elif option == "640 x 480":
                        game.current_resolution = (640, 480)
                    elif option == "1280 x 960":
                        game.current_resolution = (1280, 960)
                    elif option == "Volver al menú principal":
                        return main_menu(screen, game), game.current_resolution  # Devuelve al menú principal y la resolución

                    # Aquí actualizamos la resolución en el juego y guardamos en el archivo CSV
                    try:
                        game.screen = pygame.display.set_mode(game.current_resolution)
                        save_resolution_to_csv(game.current_resolution)
                    except Exception as e:
                        print(f"Error al guardar la resolución: {e}")
                    
def draw_text2(screen, text, size, color, x, y, padding_x=10, padding_y=5, death_count=None):
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
        
if __name__ == "__main__":
    from game import Juego

    resolution = load_resolution_from_csv()
    if resolution:
        Juego(resolution).run()
    else:
        Juego().run()

