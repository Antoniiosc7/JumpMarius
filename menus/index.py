import menus.main as main
import menus.config as config
import menus.level as level
import menus.restart as restart
import menus.win as win
import menus.gameOver as gameOver
import menus.character as character

def index(screen, game, menu):
    if(menu == 1):
        return main.main_menu(screen, game)  # Llamar a la función main dentro del módulo menus.main
    elif(menu == 2):
        return restart.restart_menu(screen, game)
    elif(menu == 3):
        return gameOver.game_over_menu(screen, game)
    elif(menu == 4):
        return win.win_menu(screen, game)
    elif(menu == 5):
        return level.level_selection_menu(screen, game)
    elif(menu == 6):
        return character.character_selection_menu(screen, game)
    elif(menu == 7):
        return config.config_menu(screen, game)
    else:
        return None