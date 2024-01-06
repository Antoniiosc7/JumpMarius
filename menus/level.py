import pygame
import utils
import menus.menuUtils as menuUtils
import menus.main as main
import sys
def level_selection_menu(screen, game):
    levels = utils.get_available_levels()

    if not levels:
        print("No hay niveles disponibles.")
        return "main_menu", None

    selected_level = levels.index(utils.load_selected_level_from_csv()) if levels else 0

    while True:
        screen.fill((255, 255, 255))

        menuUtils.draw_text(screen, "Seleccion de nivel", 36, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)

        for i, level in enumerate(levels):
            size = 24
            color = (0, 0, 0)
            if i == selected_level:
                size = 28
                color = (255, 0, 0)
            menuUtils.draw_text(screen, level, size, color, screen.get_width() // 2, screen.get_height() // 2 + i * 40)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_level = (selected_level - 1) % len(levels)
                elif event.key == pygame.K_DOWN:
                    selected_level = (selected_level + 1) % len(levels)
                elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]:
                    return "main_menu", levels[selected_level]
                elif event.key == pygame.K_ESCAPE:
                    return "main_menu", None