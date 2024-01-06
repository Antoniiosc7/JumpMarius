import utils
import pygame
import sys
import menus.menuUtils as menuUtils
import menus.config as config
import menus.level as level
import menus.character as character
def main_menu(screen, game):
    options = ["Comenzar nueva partida", "Seleccion de nivel", "Seleccion de personaje", "Configuracion", "Salir"]
    selected_option = 0
    background = utils.load_and_scale_background(game)
    while True:
        screen.blit(background, (0, 0))
        menuUtils.draw_text(screen, "Bienvenido a Jump Marius", 36, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)
        menuUtils.draw_text(screen, "By Antoniiosc7", 28, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 3.1)

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
                    if option == "Comenzar nueva partida":
                        return 'restart'
                    elif option == "Seleccion de nivel":
                        level_selection_menu_result, selected_level = level.level_selection_menu(screen, game)
                        if level_selection_menu_result == "main_menu":
                            if selected_level:
                                utils.save_selected_level_to_csv(selected_level)
                    elif option == "Seleccion de personaje":
                        character.character_selection_menu(screen, game)
                        
                    elif option == "Configuracion":
                        config_menu_result, new_resolution = config.config_menu(screen, game)
                        if config_menu_result == "main_menu":
                            if new_resolution:
                                game.change_resolution(new_resolution)
                                utils.save_resolution_to_csv(new_resolution)
                                utils.load_and_scale_background(game)  # Actualizar la imagen de fondo
                            #return "main_menu"
                    elif option == "Salir":
                        pygame.quit()
                        sys.exit()


