import pygame
import sys
import pandas as pd
import os


def save_resolution_to_csv(resolution):
    current_data = load_config_from_csv()
    current_data['Width'], current_data['Height'] = resolution
    save_config_to_csv(current_data)

def load_resolution_from_csv():
    try:
        config_df = pd.read_csv('config.csv')
        resolution = (config_df['Width'].iloc[0], config_df['Height'].iloc[0])
        print("Resolution loaded:", resolution)
        return resolution
    except (FileNotFoundError, pd.errors.EmptyDataError, IndexError, ValueError):
        return None

def save_selected_character_to_csv(selected_character):
    current_data = load_config_from_csv()
    current_data['Character'] = selected_character
    save_config_to_csv(current_data)

def load_selected_character_from_csv():
    try:
        config_df = pd.read_csv('config.csv')
        selected_character = config_df['Character'].iloc[0]
        return selected_character
    except (FileNotFoundError, pd.errors.EmptyDataError, IndexError, ValueError):
        return "Character1"  # Valor predeterminado si no se encuentra en el archivo o hay un error

def save_config_to_csv(data):
    config_df = pd.DataFrame(data)
    config_df.to_csv('config.csv', index=False)

def load_config_from_csv():
    try:
        config_df = pd.read_csv('config.csv')
        return config_df.to_dict(orient='list')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return {'Width': [], 'Height': [], 'Character': []}
    
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
                        character_selection_menu_result, new_character = character_selection_menu(screen, game)
                        
                    elif option == "Configuracion":
                        config_menu_result, new_resolution = config_menu(screen, game)
                        if config_menu_result == "main_menu":
                            if new_resolution:
                                game.change_resolution(new_resolution)
                                save_resolution_to_csv(new_resolution)
                                load_and_scale_background(game)  # Actualizar la imagen de fondo
                            #return "main_menu"
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
    screen.blit(rect_surface, (text_rect.topleft[0] - padding_x - 1, text_rect.topleft[1] - padding_y - 1))
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
                if event.key == pygame.K_ESCAPE:
                    return 'continue'
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
    options = ["Reiniciar partida", "Menu Principal", "Salir"]
    selected_option = 0

    background = load_and_scale_background(game)
    screen.blit(background, (0, 0))


    while True:
        
        draw_text(screen, "¡Has perdido la partida!", 36, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)
        
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
                if event.key == pygame.K_ESCAPE:
                    game.reset_game()
                    return 'restart'
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]:
                    option = options[selected_option]
                    if option == "Reiniciar partida":
                        game.reset_game()
                        return 'restart'
                    elif option == "Menu Principal":
                        return main_menu(screen, game)
                    elif option == "Salir":
                        pygame.quit()
                        sys.exit()    
        # Agrega un pequeño descanso para evitar procesar múltiples eventos por un solo toque de tecla
        #pygame.time.delay(100)       

def config_menu(screen, game):
    options = ["320 x 240", "640 x 480", "1280 x 960", "Volver al menú principal"]
    selected_option = 0

    while True:
        screen.fill((255, 255, 255))

        draw_text(screen, "Configuración", 36, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)

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


def win_menu(screen, game):
    options = ["Volver al menú principal", "Salir"]
    selected_option = 0

    background = load_and_scale_background(game)
    screen.blit(background, (0, 0))

    while True:
        draw_text(screen, "¡Enhorabuena, has ganado!", 36, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)

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
                    if option == "Volver al menú principal":
                        game.reset_game()
                        return main_menu(screen, game)
                    elif option == "Salir":
                        pygame.quit()
                        sys.exit()
                        
def character_selection_menu(screen, game):
    characters = ["Ninja1", "Ninja2", "Ninja3"]
    selected_character = characters.index(game.get_selected_character())
    character_images = {}

    # Obtener la resolución actual del archivo CSV
    resolution = load_resolution_from_csv()

    # Definir dimensiones de personajes según la resolución
    if resolution == (1280, 960):
        character_dimensions = (80, 150)
        side_character_dimensions = (int(80 * 0.85), int(150 * 0.85))  # Reducción del 15%
    elif resolution == (640, 480):
        character_dimensions = (40, 75)
        side_character_dimensions = (int(40 * 0.85), int(75 * 0.85))  # Reducción del 15%
    elif resolution == (320, 240):
        character_dimensions = (20, 38)
        side_character_dimensions = (int(20 * 0.85), int(38 * 0.85))  # Reducción del 15%
    else:
        # Resolución por defecto
        character_dimensions = (80, 150)
        side_character_dimensions = (int(80 * 0.85), int(150 * 0.85))  # Reducción del 15%

    # Cargar y escalar la imagen de fondo
    background = pygame.image.load("recursos/character_selection.png").convert()

    if resolution:
        background = pygame.transform.scale(background, resolution)

    for character in characters:
        image_path = os.path.join("recursos/visualizaciones/", f"{character}.png")
        if os.path.exists(image_path):
            character_images[character] = pygame.image.load(image_path)
        else:
            print("No se encontró la imagen para:", character)

    while True:
        screen.blit(background, (0, 0))

        draw_text(screen, "Selecciona un personaje", 55, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)

        # Dibujar personajes adyacentes
        for i in range(-1, 2):
            if i == 0:  # Omitir el personaje central
                continue

            index = (selected_character + i) % len(characters)
            x_position = screen.get_width() // 2 + i * (screen.get_width()//12)
            size = character_dimensions if i != 0 else (int(character_dimensions[0] // 1.25), int(character_dimensions[1] // 1.25))

            draw_character(screen, characters[index], character_images.get(characters[index]),
                           x_position, screen.get_height() // 1.5, size, draw_name=True)

        draw_text(screen, "Pulsa Enter o Espacio para seleccionar", 24, (0, 0, 0),
                  screen.get_width() // 2, screen.get_height() - 50)

        # Dibujar el personaje central con nombre
        draw_character(screen, characters[selected_character], character_images.get(characters[selected_character]),
                       screen.get_width() // 2, screen.get_height() // 2, character_dimensions, draw_name=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    selected_character = (selected_character + 1) % len(characters)
                elif event.key == pygame.K_LEFT:
                    selected_character = (selected_character - 1) % len(characters)
                elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]:
                    new_character = characters[selected_character]
                    game.set_selected_character(new_character)
                    save_selected_character_to_csv(new_character)
                    return "main_menu", new_character
                elif event.key == pygame.K_ESCAPE:
                    return "main_menu", None

def draw_character(screen, character, image, x, y, size, draw_name=False):
    # Dibuja la imagen del personaje
    if image is not None:
        image = pygame.transform.scale(image, size)
        rect = image.get_rect(center=(x, y))
        screen.blit(image, rect.topleft)

        # Dibuja el nombre del personaje si es necesario
        if draw_name:
            draw_text(screen, character, 24, (0, 0, 0), x, y + size[1] // 2 + 10)

if __name__ == "__main__":
    from game import Juego

    resolution = load_resolution_from_csv()
    if resolution:
        Juego(resolution).run()
    else:
        Juego().run()

