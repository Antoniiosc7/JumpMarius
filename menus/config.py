import pygame
import utils
import menus.menuUtils as menuUtils
import menus.main as main
import sys
def config_menu(screen, game):
    options = ["320 x 240", "640 x 480", "1280 x 960", "Volver al menú principal"]
    selected_option = 0

    while True:
        screen.fill((255, 255, 255))

        menuUtils.draw_text(screen, "Configuración", 36, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)

        for i, option in enumerate(options):
            size = 24
            color = (0, 0, 0)
            if i == selected_option:
                size = 28
                color = (255, 0, 0)
            menuUtils.draw_text(screen, option, size, color, screen.get_width() // 2, screen.get_height() // 2 + i * 40)

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
                        return main.main_menu(screen, game), game.current_resolution  # Devuelve al menú principal y la resolución

                    # Aquí actualizamos la resolución en el juego y guardamos en el archivo CSV
                    try:
                        game.screen = pygame.display.set_mode(game.current_resolution)
                        utils.save_resolution_to_csv(game.current_resolution)
                    except Exception as e:
                        print(f"Error al guardar la resolución: {e}")
