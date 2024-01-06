import pygame, sys, os, pandas as pd
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