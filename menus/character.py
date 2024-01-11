import pygame
import utils
import menus.menuUtils as menuUtils
import menus.main as main
import sys, os
def character_selection_menu(screen, game):
    characters = ["Ninja1", "Ninja2", "Ninja3"]
    selected_character = characters.index(game.get_selected_character())
    character_images = {}

    # Obtener la resolución actual del archivo CSV
    resolution = utils.load_resolution_from_csv()

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

        menuUtils.draw_text(screen, "Selecciona un personaje", 55, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)

        # Dibujar personajes adyacentes
        for i in range(-1, 2):
            if i == 0:  # Omitir el personaje central
                continue

            index = (selected_character + i) % len(characters)
            x_position = screen.get_width() // 2 + i * (screen.get_width()//12)
            size = character_dimensions if i != 0 else (int(character_dimensions[0] // 1.25), int(character_dimensions[1] // 1.25))

            draw_character(screen, characters[index], character_images.get(characters[index]),
                           x_position, screen.get_height() // 1.5, size, draw_name=True)

        menuUtils.draw_text(screen, "Pulsa Enter o Espacio para seleccionar", 24, (0, 0, 0),
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
                    utils.save_selected_character_to_csv(new_character)
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
            menuUtils.draw_text(screen, character, 24, (0, 0, 0), x, y + size[1] // 2 + 10)