import pygame
import sys
import game

def main_menu(screen):
    # Intenta cargar la imagen de fondo
    try:
        background = pygame.image.load("recursos/fondo.jpg").convert()
        background = pygame.transform.scale(background, (800, 600))
    except pygame.error as e:
        print(f"Error al cargar la imagen de fondo: {e}")
        return

    while True:
        screen.blit(background, (0, 0))  # Dibujar la imagen de fondo

        # Menú principal
        draw_text(screen, "Bienvenido a Marius Game", 36, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)
        draw_text(screen, "By Antoniiosc7", 28, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 3.1)
        draw_text(screen, "Presiona ESPACIO para jugar", 24, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 2)
        draw_text(screen, "Presiona Q para salir", 24, (0, 0, 0), screen.get_width() // 2, screen.get_height() * 3 // 4)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def draw_text(screen, text, size, color, x, y, padding_x=10, padding_y=5):
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
    
def restart_menu(screen):
    while True:
        screen.fill((255, 255, 255))

        # Menú de reinicio
        draw_text(screen, "HAS PAUSADO LA PARTIDA", 36, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 4)
        draw_text(screen, "Presiona R para reiniciar", 24, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 2)
        draw_text(screen, "Presiona M para volver al menú principal", 24, (0, 0, 0), screen.get_width() // 2, screen.get_height() // 3)
        draw_text(screen, "Presiona Q para salir", 24, (0, 0, 0), screen.get_width() // 2, screen.get_height() * 3 // 4)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v or event.key == pygame.K_ESCAPE:
                    return True
                if event.key == pygame.K_r:
                    return game.__name__
                elif event.key == pygame.K_m:
                    return main_menu(screen)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()