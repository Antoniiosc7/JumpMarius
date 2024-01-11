
import pygame
import utils
import menus.menuUtils as menuUtils
import menus.main as main
import sys
def game_over_menu(screen, game):
    options = ["Reiniciar partida", "Menu Principal", "Salir"]
    selected_option = 0

    background = utils.load_and_scale_background(game)
    screen.blit(background, (0, 0))


    while True:
        
        menuUtils.draw_text(screen, "¡Has perdido la partida!", 36, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)
        
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
                        return main.main_menu(screen, game)
                    elif option == "Salir":
                        pygame.quit()
                        sys.exit()    
        # Agrega un pequeño descanso para evitar procesar múltiples eventos por un solo toque de tecla
        #pygame.time.delay(100)       